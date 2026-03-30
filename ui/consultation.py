# ============================================================
# ui/consultation.py
# @module  : ui.consultation
# @desc    : Halaman Konsultasi Wizard — step-by-step diagnosis
# @author  : Tim Pengembang Laptop Diagnostic Expert
# @date    : 2026-03-28
# @version : 1.0.0
# ============================================================

import streamlit as st
import logging

from engine.backward_chaining import BackwardChainingEngine
from engine.explanation import ExplanationFacility
from ui.components import (
    render_question_card,
    render_progress_bar,
    render_cf_selector,
    render_why_explanation,
)

logger = logging.getLogger("laptop_diagnostic_expert.ui.consultation")


def _init_engine():
    """
    Inisialisasi BackwardChainingEngine di session_state jika belum ada.
    Dipanggil saat halaman konsultasi pertama kali dimuat.
    """
    if "engine" not in st.session_state:
        try:
            engine = BackwardChainingEngine()
            engine.start()
            st.session_state["engine"] = engine
            st.session_state["question_counter"] = 0
            st.session_state["cf_selected"] = None
            logger.info("Engine initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize engine: %s", e)
            st.error(
                f"Gagal menginisialisasi Inference Engine: {e}\n\n"
                "Pastikan Knowledge Base tersedia."
            )
            st.stop()


def _process_answer(engine: BackwardChainingEngine, question: dict, cf_value: float):
    """
    Proses jawaban CF User dan tentukan langkah berikutnya.

    Args:
        engine: Instance BackwardChainingEngine aktif.
        question: Dict pertanyaan gejala saat ini.
        cf_value: Nilai CF User yang dipilih.
    """
    try:
        kode_gejala = question["kode_gejala"]
        result = engine.submit_answer(kode_gejala, cf_value)

        # Log untuk traceability
        logger.info(
            "Answer submitted: %s = %.1f → %s (short_circuit=%s)",
            kode_gejala, cf_value,
            result["event"], result["short_circuit"],
        )

        # Increment question counter untuk unique widget keys
        st.session_state["question_counter"] += 1
        st.session_state["cf_selected"] = None

        # Cek apakah ada pertanyaan berikutnya
        next_q = engine.get_current_question()
        if next_q is None or engine.is_finished():
            # Konsultasi selesai → pindah ke halaman hasil
            st.session_state["page"] = "result"
            logger.info("Consultation complete, moving to results")

    except ValueError as ve:
        st.error(f"Nilai CF tidak valid: {ve}")
        logger.error("Invalid CF value: %s", ve)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses jawaban: {e}")
        logger.error("Error processing answer: %s", e)


def render_consultation_page():
    """
    Render halaman konsultasi wizard step-by-step.

    Alur:
    1. Inisialisasi engine (jika belum).
    2. Ambil pertanyaan gejala berikutnya dari engine.
    3. Tampilkan progress bar, question card, CF selector.
    4. Tampilkan tombol "Mengapa?" (Why Explanation).
    5. Proses jawaban dan lanjut ke gejala berikutnya.
    """
    st.markdown("## Konsultasi Diagnosis")
    st.caption("Jawab setiap pertanyaan gejala dengan tingkat keyakinan Anda.")

    # ── Inisialisasi Engine ────────────────────────────────
    _init_engine()
    engine: BackwardChainingEngine = st.session_state["engine"]

    # ── Ambil Pertanyaan Saat Ini ──────────────────────────
    question = engine.get_current_question()

    if question is None or engine.is_finished():
        # Konsultasi selesai → redirect ke hasil
        st.session_state["page"] = "result"
        st.rerun()
        return

    # ── Render Progress Bar ────────────────────────────────
    render_progress_bar(question)

    # ── Render Question Card ───────────────────────────────
    render_question_card(question)

    # ── Render CF Selector ─────────────────────────────────
    st.markdown("")
    counter = st.session_state.get("question_counter", 0)
    cf_value = render_cf_selector(key=f"cf_input_{counter}")

    # ── Why Explanation (Mengapa?) ─────────────────────────
    with st.expander("Mengapa gejala ini ditanyakan?", expanded=False):
        try:
            hyp = question["hypothesis"]
            rule = question["rule"]
            why_text = ExplanationFacility.why(
                kode_gejala=question["kode_gejala"],
                kode_kerusakan=hyp["kode"],
                rule={
                    "rule_id": rule["rule_id"],
                    "cf_rule": rule["cf_rule"],
                },
                premise_index=rule["current_premise_index"],
            )
            render_why_explanation(why_text)
        except Exception as e:
            st.warning(f"Penjelasan tidak tersedia: {e}")

    st.markdown("")

    # ── Tombol Lanjut ──────────────────────────────────────
    col_spacer, col_btn = st.columns([3, 1])
    with col_btn:
        btn_disabled = cf_value is None
        if st.button(
            "Lanjut →",
            use_container_width=True,
            type="primary",
            disabled=btn_disabled,
            key=f"btn_next_{counter}",
        ):
            _process_answer(engine, question, cf_value)
            st.rerun()

    # Pesan validasi jika belum memilih
    if cf_value is None:
        st.info("Pilih tingkat keyakinan terlebih dahulu untuk melanjutkan.")

    # ── Tombol Batalkan ────────────────────────────────────
    st.markdown("---")
    if st.button("Batalkan Konsultasi", key="btn_cancel"):
        # Reset semua state
        for key in ["engine", "question_counter", "cf_selected",
                     "consultation_started"]:
            st.session_state.pop(key, None)
        st.session_state["page"] = "home"
        st.rerun()
