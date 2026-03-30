# ============================================================
# app.py
# @module  : app
# @desc    : Entry point Streamlit — Laptop Diagnostic Expert Sistem Pakar
#            Diagnosis Kerusakan Laptop. Mengelola routing
#            halaman dan session state global.
# @author  : Tim Pengembang Laptop Diagnostic Expert
# @date    : 2026-03-28
# @version : 1.0.0
#
# Cara menjalankan:
#   streamlit run app.py
# ============================================================

import streamlit as st
import logging
import sys
import os

# ── Path setup agar modul bisa diimport ────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Konfigurasi logging ───────────────────────────────────
from config import setup_logging
setup_logging(level="INFO")

logger = logging.getLogger("laptop_diagnostic_expert.app")


# ============================================================
# KONFIGURASI HALAMAN STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Laptop Diagnostic Expert",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "# Laptop Diagnostic Expert v1.0\n"
            "Sistem Pakar Diagnosis Kerusakan Laptop\n\n"
            "Menggunakan **Backward Chaining** dan **Certainty Factor**.\n\n"
            "Proyek Akademik — Mata Kuliah Sistem Pakar, 2026."
        ),
    },
)


# ============================================================
# LOAD CUSTOM CSS
# ============================================================

def _load_css():
    """Load custom CSS dari assets/style.css."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        logger.warning("Custom CSS not found at %s", css_path)


_load_css()


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def _init_session_state():
    """
    Inisialisasi session state global.

    Variabel yang dikelola:
    - page: Halaman aktif ("home" | "consultation" | "result")
    - consultation_started: Flag apakah konsultasi sudah dimulai
    - engine: Instance BackwardChainingEngine (dibuat di consultation.py)
    - question_counter: Counter untuk unique widget keys
    - cf_selected: CF value yang sedang dipilih user
    """
    defaults = {
        "page": "home",
        "consultation_started": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_session_state()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

def _render_sidebar():
    """Render sidebar navigasi dengan menu halaman."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding:1.5rem 0;">
                <h2 style="margin:0; font-family:'Outfit',sans-serif; font-size:1.8rem; font-weight:700; background: linear-gradient(135deg, #00F4FF, #8B5CF6);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                Laptop Diagnostic Expert</h2>
                <p style="color:var(--accent-cyan); font-size:0.85rem; font-weight:600; margin-top:0.5rem; letter-spacing:0.5px;">
                Mata Kuliah Sistem Pakar<br>Computer Science UGM 2026</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Menu navigasi
        current_page = st.session_state.get("page", "home")

        if st.button(
            "Beranda",
            use_container_width=True,
            type="primary" if current_page == "home" else "secondary",
            key="nav_home",
        ):
            # Reset konsultasi jika kembali ke beranda
            for key in ["engine", "question_counter", "cf_selected",
                         "consultation_started"]:
                st.session_state.pop(key, None)
            st.session_state["page"] = "home"
            st.rerun()

        if st.button(
            "Konsultasi",
            use_container_width=True,
            type="primary" if current_page == "consultation" else "secondary",
            key="nav_consult",
        ):
            st.session_state["page"] = "consultation"
            st.session_state["consultation_started"] = True
            st.rerun()

        # Status konsultasi aktif
        if "engine" in st.session_state:
            st.markdown("---")
            engine = st.session_state["engine"]
            current, total = engine.get_progress()

            st.markdown(
                f"""
                <div style="background:#1E293B; border:1px solid #475569;
                border-radius:8px; padding:0.75rem; font-size:0.85rem;">
                    <strong style="color:#06B6D4;">Sesi Aktif</strong><br>
                    <span style="color:#94A3B8;">
                    Hipotesis: {current}/{total}<br>
                    Jawaban: {len(engine.answers)} gejala
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align:center; color:#64748B; font-size:0.7rem;">
                Laptop Diagnostic Expert v1.0<br>
                Backward Chaining &times; CF<br>
                &copy; 2026
            </div>
            """,
            unsafe_allow_html=True,
        )


_render_sidebar()


# ============================================================
# ROUTING HALAMAN
# ============================================================

def main():
    """
    Router utama — mengarahkan ke halaman sesuai session state.

    Routing:
    - "home"         → Halaman Beranda (ui/home.py)
    - "consultation" → Halaman Konsultasi Wizard (ui/consultation.py)
    - "result"       → Halaman Hasil Diagnosis (ui/result.py)
    """
    page = st.session_state.get("page", "home")

    try:
        if page == "home":
            from ui.home import render_home_page
            render_home_page()

        elif page == "consultation":
            from ui.consultation import render_consultation_page
            render_consultation_page()

        elif page == "result":
            from ui.result import render_result_page
            render_result_page()

        else:
            # Fallback ke beranda
            logger.warning("Unknown page: %s, redirecting to home", page)
            st.session_state["page"] = "home"
            st.rerun()

    except Exception as e:
        logger.error("Unhandled error on page '%s': %s", page, e, exc_info=True)
        st.error(
            f"Terjadi kesalahan yang tidak terduga:\n\n"
            f"`{type(e).__name__}: {e}`\n\n"
            f"Silakan muat ulang halaman atau kembali ke Beranda."
        )
        if st.button("Kembali ke Beranda"):
            for key in list(st.session_state.keys()):
                if key != "page":
                    st.session_state.pop(key, None)
            st.session_state["page"] = "home"
            st.rerun()


# ── Entry Point ────────────────────────────────────────────
if __name__ == "__main__":
    main()
