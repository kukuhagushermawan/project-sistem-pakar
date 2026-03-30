# ============================================================
# ui/home.py
# @module  : ui.home
# @desc    : Halaman Beranda Laptop Diagnostic Expert — intro & CTA
# @author  : Tim Pengembang Laptop Diagnostic Expert
# @date    : 2026-03-28
# @version : 1.0.0
# ============================================================

import streamlit as st
from ui.components import render_hero, render_feature_cards


def render_home_page():
    """
    Render halaman beranda dengan hero section, fitur utama,
    cara penggunaan, dan tombol CTA 'Mulai Konsultasi'.
    """
    # Hero section
    render_hero()

    # Feature cards
    render_feature_cards()

    st.markdown("---")

    # Cara penggunaan
    st.markdown("### Cara Penggunaan")
    cols = st.columns(4)
    steps = [
        ("01", "Mulai", "Klik tombol untuk memulai konsultasi diagnosis"),
        ("02", "Jawab", "Pilih tingkat keyakinan untuk setiap gejala"),
        ("03", "Analisis", "Sistem memproses jawaban dengan Backward Chaining"),
        ("04", "Hasil", "Lihat diagnosis, solusi, dan penjelasan lengkap"),
    ]
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(
                f"""
                <div style="text-align:center; padding:0.75rem;">
                    <div style="font-size:1.4rem; font-weight:700; color:#06B6D4;
                    font-family:'JetBrains Mono',monospace;">{num}</div>
                    <strong>{title}</strong>
                    <p style="font-size:0.8rem; color:#94A3B8; margin-top:0.25rem;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Informasi cakupan
    st.markdown("### Cakupan Diagnosis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jenis Kerusakan", "10")
    with col2:
        st.metric("Gejala Terdeteksi", "25")
    with col3:
        st.metric("Rule Inferensi", "12")

    st.markdown("")

    # CTA Button
    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.button(
            "Mulai Konsultasi",
            use_container_width=True,
            type="primary",
            key="btn_start",
        ):
            st.session_state["page"] = "consultation"
            st.session_state["consultation_started"] = True
            st.rerun()
