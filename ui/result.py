# ============================================================
# ui/result.py
# @module  : ui.result
# @desc    : Halaman Hasil Diagnosis — ranking, solusi,
#            Explanation Facility (How), dan pohon inferensi
# @author  : Tim Pengembang LaptopDoc
# @date    : 2026-03-28
# @version : 1.0.0
# ============================================================

import streamlit as st
import logging

from knowledge_base import get_frame
from engine.backward_chaining import BackwardChainingEngine
from engine.certainty_factor import CertaintyFactor
from engine.explanation import ExplanationFacility
from ui.components import render_result_card, render_summary_metrics
from visualization.inference_tree import render_inference_tree

logger = logging.getLogger("laptop_diagnostic_expert.ui.result")


def _build_summary(engine: BackwardChainingEngine) -> dict:
    """
    Bangun ringkasan hasil diagnosis.

    Args:
        engine: Instance engine yang sudah selesai.

    Returns:
        dict: {"total", "proven", "failed"}
    """
    all_results = engine.get_all_results()
    proven = [r for r in all_results if r["status"] == "TERBUKTI"]
    return {
        "total": len(all_results),
        "proven": len(proven),
        "failed": len(all_results) - len(proven),
    }


def _render_how_explanation(result: dict, engine: BackwardChainingEngine):
    """
    Render bagian 'Bagaimana kesimpulan ini didapat?' (How Explanation).

    Args:
        result: Dict hasil diagnosis satu kerusakan.
        engine: Engine instance untuk akses trace log.
    """
    kode = result["kode_kerusakan"]
    trace_log = engine.get_trace_log()

    # Filter trace untuk hipotesis ini
    relevant_traces = [
        t for t in trace_log
        if t.get("hypothesis") == kode
    ]

    # Tampilkan rule yang triggered
    rules_triggered = result.get("rules_triggered", [])
    if rules_triggered:
        st.markdown(f"**Rule yang terpenuhi:** <span style='background:var(--bg-card); padding:2px 8px; border-radius:4px; font-family:monospace; border:1px solid var(--border);'>{', '.join(rules_triggered)}</span>", unsafe_allow_html=True)

    # Tampilkan gejala dan CF User
    st.markdown('<div style="margin-top:1.5rem; margin-bottom:0.5rem; font-weight:600; color:var(--text-primary);">Gejala yang dievaluasi:</div>', unsafe_allow_html=True)

    answer_traces = [
        t for t in relevant_traces
        if t.get("action") in ("RECEIVE_ANSWER", "CACHE_HIT")
    ]

    for trace in answer_traces:
        symptom_code = trace.get("symptom", "")
        cf_user = trace.get("cf_user", 0.0)
        status_badge = "<span style='background:#065F46; color:#34D399; padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:700;'>TERPENUHI</span>" if cf_user > 0 else "<span style='background:#7F1D1D; color:#F87171; padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:700;'>TIDAK</span>"
        st.markdown(
            f"""<div class="trace-step">
            {status_badge} <strong style="margin-left:10px; color:var(--text-primary);">{symptom_code}</strong> &mdash; CF User: {cf_user}
            </div>""",
            unsafe_allow_html=True,
        )

    # Tampilkan langkah perhitungan CF
    calc_traces = [
        t for t in relevant_traces
        if t.get("action") in ("CALCULATE_CF", "COMBINE_MULTI_RULES")
    ]

    if calc_traces:
        st.markdown('<div style="margin-top:1.5rem; margin-bottom:0.75rem; font-weight:600; color:var(--text-primary);">Langkah Perhitungan Certainty Factor</div>', unsafe_allow_html=True)
        for calc in calc_traces:
            action = calc.get("action")
            
            if action == "CALCULATE_CF":
                rule_id = calc.get("rule", "")
                cf_steps = calc.get("cf_steps", [])

                steps_text = f"# Menghitung Rule {rule_id}\n"
                for step in cf_steps:
                    op = step.get("operation", "")
                    if op == "combine":
                        steps_text += (
                            f"CF_combine({step['cf1']}, {step['cf2']}) "
                            f"= {step['result']:.4f}\n"
                        )
                    elif op == "min":
                        cf_users_str = ", ".join(f"{v}" for v in step["cf_users"])
                        steps_text += f"\nKarena premis menggunakan AND:\n"
                        steps_text += f"CF_user_kombinasi = min({cf_users_str}) = {step['result']:.4f}\n"
                    elif op == "final":
                        steps_text += (
                            f"\nCF_{rule_id} = CF_pakar x CF_user_kombinasi\n"
                            f"CF_{rule_id} = {step['cf_rule']} x "
                            f"{step['cf_user_combined']:.4f} "
                            f"= {step['cf_final']:.4f}\n"
                        )

                st.code(steps_text, language="python")
                
            elif action == "COMBINE_MULTI_RULES":
                rules_cf = calc.get("rules_cf", [])
                final_combined = calc.get("cf_final_combined", 0.0)
                
                steps_text = f"# Kombinasi Antar-Rule untuk Kesimpulan {kode}\n"
                steps_text += f"# Karena terdapat {len(rules_cf)} rule menuju {kode}, lakukan CF combine:\n\n"
                
                from engine.certainty_factor import CertaintyFactor
                temp = rules_cf[0]
                for i in range(1, len(rules_cf)):
                    next_val = rules_cf[i]
                    steps_text += f"Tahap {i}: CFcombine({temp:.4f}, {next_val:.4f})\n"
                    temp = CertaintyFactor.combine_cf(temp, next_val)
                    steps_text += f"         = {temp:.4f}\n"
                
                st.code(steps_text, language="python")

    # CF Final
    cf_pct = f"{result['cf_final'] * 100:.1f}%"
    st.markdown(f"""
        <div style="margin-top:1.5rem; padding:1rem; border-radius:8px; background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.2); text-align:center;">
            <strong style="color:#10B981; font-size:1.1rem;">CF Final {kode}: {cf_pct}</strong>
        </div>
    """, unsafe_allow_html=True)


def _render_solution(result: dict):
    """
    Render solusi detail untuk kerusakan.

    Args:
        result: Dict hasil diagnosis.
    """
    frame = get_frame(result["kode_kerusakan"])
    if not frame:
        st.warning("Detail solusi tidak tersedia.")
        return

    st.markdown("<h4 style='color:var(--text-primary); margin-bottom:0.5rem;'>Penyebab</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:var(--text-secondary); margin-bottom:1.5rem;'>{frame.get('penyebab', '-')}</p>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='color:var(--text-primary); margin-bottom:0.5rem;'>Solusi & Tindakan Rekomendasi</h4>", unsafe_allow_html=True)

    solusi = frame.get("solusi_detail", frame.get("solusi_singkat", "-"))
    for line in solusi.split("\n"):
        if line.strip():
            st.markdown(f"<div style='color:var(--text-secondary); margin-bottom:0.25rem;'>&bull; {line.strip()}</div>", unsafe_allow_html=True)


def render_result_page():
    """
    Render halaman hasil diagnosis lengkap.
    """
    st.markdown("## Hasil Diagnosis")

    # ── Validasi Engine ────────────────────────────────────
    if "engine" not in st.session_state:
        st.warning("Belum ada sesi konsultasi. Silakan mulai dari Beranda.")
        if st.button("Kembali ke Beranda"):
            st.session_state["page"] = "home"
            st.rerun()
        return

    engine: BackwardChainingEngine = st.session_state["engine"]

    # ── Summary Metrics ────────────────────────────────────
    try:
        summary = _build_summary(engine)
        render_summary_metrics(summary)
    except Exception as e:
        logger.error("Error building summary: %s", e)
        st.error("Gagal membangun ringkasan hasil.")

    st.markdown("---")

    # ── Ambil Hasil Ranking ────────────────────────────────
    try:
        ranking = engine.get_results()
    except Exception as e:
        logger.error("Error getting results: %s", e)
        st.error(f"Gagal mengambil hasil diagnosis: {e}")
        return

    if not ranking:
        # Tidak ada kerusakan terbukti
        st.warning(
            "**Tidak ditemukan kerusakan yang cocok.**\n\n"
            "Kemungkinan penyebab:\n"
            "- Gejala yang Anda alami tidak cocok dengan basis pengetahuan.\n"
            "- Coba konsultasi ulang dengan jawaban yang lebih spesifik."
        )
    else:
        # ── Diagnosis Utama (Rank #1) ──────────────────────
        top = ranking[0]
        st.markdown("### Diagnosis Utama")

        render_result_card(top, rank=1)

        # Solusi untuk diagnosis utama
        with st.expander("Lihat Solusi Detail", expanded=True):
            _render_solution(top)

        # How Explanation untuk diagnosis utama
        with st.expander("Penjelasan Inferensi", expanded=False):
            _render_how_explanation(top, engine)

        # ── Kerusakan Lain yang Terbukti ───────────────────
        if len(ranking) > 1:
            st.markdown("---")
            st.markdown("### Kemungkinan Lain")

            for i, result in enumerate(ranking[1:], start=2):
                render_result_card(result, rank=i)

                with st.expander(
                    f"Detail {result['kode_kerusakan']} — {result['nama_kerusakan']}",
                    expanded=False,
                ):
                    _render_solution(result)
                    st.markdown("---")
                    _render_how_explanation(result, engine)

    # ── Visualisasi Pohon Inferensi ────────────────────────
    st.markdown("---")
    st.markdown("### Pohon Inferensi")
    st.caption("Visualisasi alur evaluasi Backward Chaining")

    try:
        all_results = engine.get_all_results()
        trace_log = engine.get_trace_log()
        render_inference_tree(all_results, trace_log)
    except Exception as e:
        logger.warning("Graphviz not available, showing text tree: %s", e)
        _render_text_tree(engine)

    # ── Tombol Konsultasi Ulang dan Kembali ────────────────
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Konsultasi Ulang", use_container_width=True, type="primary"):
            # Reset semua state konsultasi
            for key in ["engine", "question_counter", "cf_selected",
                         "consultation_started"]:
                st.session_state.pop(key, None)
            st.session_state["page"] = "consultation"
            st.session_state["consultation_started"] = True
            st.rerun()

    with col2:
        if st.button("Kembali ke Beranda", use_container_width=True):
            for key in ["engine", "question_counter", "cf_selected",
                         "consultation_started"]:
                st.session_state.pop(key, None)
            st.session_state["page"] = "home"
            st.rerun()


def _render_text_tree(engine: BackwardChainingEngine):
    """
    Fallback: render pohon inferensi sebagai teks jika Graphviz tidak tersedia.

    Args:
        engine: Engine instance untuk akses results dan trace.
    """
    all_results = engine.get_all_results()
    trace_log = engine.get_trace_log()

    tree_text = ""
    for result in all_results:
        kode = result["kode_kerusakan"]
        status = result["status"]
        cf = result["cf_final"]

        icon = "[+]" if status == "TERBUKTI" else "[x]"
        tree_text += f"{icon} [{kode}] {result['nama_kerusakan']}"

        if status == "TERBUKTI":
            tree_text += f" — CF: {cf * 100:.1f}%\n"

            # Cari gejala terkait
            related = [
                t for t in trace_log
                if t.get("hypothesis") == kode
                   and t.get("action") in ("RECEIVE_ANSWER", "CACHE_HIT")
            ]
            for t in related:
                sym = t.get("symptom", "")
                cf_u = t.get("cf_user", 0.0)
                tree_text += f"  |-- {sym}: CF={cf_u}\n"
        else:
            tree_text += " — GAGAL\n"
            # Cari alasan gagal
            fail_trace = [
                t for t in trace_log
                if t.get("hypothesis") == kode
                   and t.get("action") == "HYPOTHESIS_FAILED"
            ]
            if fail_trace:
                reason = fail_trace[0].get("reason", "Premis tidak terpenuhi")
                tree_text += f"  |-- Alasan: {reason}\n"

        tree_text += "\n"

    st.code(tree_text, language="text")
