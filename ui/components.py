# ============================================================
# ui/components.py
# @module  : ui.components
# @desc    : Komponen UI reusable untuk Laptop Diagnostic Expert Streamlit App
# @author  : Tim Pengembang Laptop Diagnostic Expert
# @date    : 2026-03-28
# @version : 1.0.0
# ============================================================

import streamlit as st


# ── Konstanta Skala CF ────────────────────────────────────────

CF_OPTIONS = [
    ("Tidak (Gejala Tidak Dialami)", 0.0),
    ("Kurang Yakin (Kadang Terasa)", 0.4),
    ("Cukup Yakin (Cukup Sering Terjadi)", 0.6),
    ("Yakin (Jelas Tampak)", 0.8),
    ("Sangat Yakin (Pasti Terjadi)", 1.0),
]

CF_LABELS = [opt[0] for opt in CF_OPTIONS]
CF_VALUES = {opt[0]: opt[1] for opt in CF_OPTIONS}


def render_hero():
    """Render hero section halaman beranda."""
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="glow-title">Laptop Diagnostic Expert</h1>
            <p style="font-size:0.95rem; color: var(--text-secondary); margin-bottom: 1.5rem; font-family:'JetBrains Mono', monospace; letter-spacing: 0.5px;">Mata Kuliah Sistem Pakar — Computer Science UGM 2026</p>
            <p>
                Platform sistem pakar untuk mendiagnosis kerusakan laptop berbasis
                <strong>Backward Chaining</strong> dan <strong>Certainty Factor</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards():
    """Render 3 feature cards di halaman beranda."""
    features = [
        {
            "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#06B6D4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
            "title": "Backward Chaining",
            "desc": "Inferensi goal-driven — sistem menguji hipotesis kerusakan satu per satu",
        },
        {
            "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#06B6D4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
            "title": "Certainty Factor",
            "desc": "Kalkulasi tingkat keyakinan diagnosis berdasarkan jawaban Anda",
        },
        {
            "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#06B6D4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
            "title": "Explanation Facility",
            "desc": "Transparansi penuh — lihat mengapa dan bagaimana kesimpulan dicapai",
        },
    ]

    cards_html = '<div class="feature-cards-container">\n'
    for feat in features:
        cards_html += f"""<div class="feature-card">
    <div class="icon">{feat['icon']}</div>
    <h3>{feat['title']}</h3>
    <p>{feat['desc']}</p>
</div>
"""
    cards_html += '</div>'
    
    st.markdown(cards_html, unsafe_allow_html=True)


def render_question_card(question: dict):
    """
    Render card pertanyaan gejala.

    Args:
        question: Dict dari engine.get_current_question()
    """
    kode = question["kode_gejala"]
    teks = question["teks_gejala"]
    detail = question.get("deskripsi_detail", "")
    kategori = question.get("kategori", "umum").upper()

    st.markdown(
        f"""
        <div class="question-card">
            <span class="badge">{kode} &bull; {kategori}</span>
            <div class="question-text">{teks}</div>
            <div class="question-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_bar(question: dict):
    """
    Render progress bar hipotesis dan informasi step.

    Args:
        question: Dict dari engine.get_current_question()
    """
    hyp = question["hypothesis"]
    rule = question["rule"]

    # Progress keseluruhan (hipotesis)
    progress = (hyp["index"] - 1) / hyp["total"]
    st.progress(progress, text=f"Hipotesis {hyp['index']} dari {hyp['total']}")

    # Info step saat ini
    st.markdown(
        f"""
        <div class="step-info">
            <span class="hypothesis-name">
                Hipotesis: {hyp['kode']} ({hyp['nama']})
            </span>
            <span class="step-counter">
                Rule R{rule['rule_id']} • Premis {rule['current_premise_index']}/{rule['total_premises']}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cf_selector(key: str = "cf_input") -> float | None:
    """
    Render radio selector untuk skala keyakinan CF User.

    Args:
        key: Unique key untuk widget Streamlit.

    Returns:
        float | None: Nilai CF yang dipilih, None jika belum memilih.
    """
    selected = st.radio(
        "Pilih tingkat keyakinan Anda:",
        options=CF_LABELS,
        index=None,
        key=key,
        help="Pilih seberapa yakin Anda mengalami gejala ini.",
    )

    if selected is not None:
        return CF_VALUES[selected]
    return None


def render_why_explanation(why_text: str):
    """
    Render panel explanation 'Mengapa gejala ini ditanyakan?'

    Args:
        why_text: Teks penjelasan dari ExplanationFacility.why()
    """
    st.markdown(
        f"""
        <div class="why-box">
            <strong>Mengapa gejala ini ditanyakan?</strong>
            <div style="margin-top:0.75rem;">
                {why_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(result: dict, rank: int):
    """
    Render card hasil diagnosis.

    Args:
        result: Dict hasil diagnosis dari engine
        rank: Peringkat (1-based)
    """
    cf = result["cf_final"]
    cf_pct = f"{cf * 100:.1f}%"

    # Tentukan warna berdasarkan CF
    if cf >= 0.7:
        cf_class = "cf-high"
        rank_class = "rank-1" if rank == 1 else "rank-2"
    elif cf >= 0.4:
        cf_class = "cf-medium"
        rank_class = "rank-other"
    else:
        cf_class = "cf-low"
        rank_class = "rank-other"

    prefix = "DIAGNOSIS UTAMA" if rank == 1 else f"#{rank}"

    st.markdown(
        f"""
        <div class="result-card {rank_class}">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                <strong style="font-size:0.9rem;">{prefix}</strong>
                <span class="cf-badge {cf_class}">{cf_pct}</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.35rem; color: var(--text-primary);">
                {result['kode_kerusakan']} &bull; {result['nama_kerusakan']}
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_metrics(summary: dict):
    """
    Render summary metrics (terbukti / gagal / total).

    Args:
        summary: Dict {"total", "proven", "failed"}
    """
    cols = st.columns(3)
    metrics = [
        (str(summary["proven"]), "Terbukti", "#10B981"),
        (str(summary["failed"]), "Gagal", "#EF4444"),
        (str(summary["total"]), "Total Hipotesis", "#06B6D4"),
    ]
    for col, (value, label, color) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="summary-box">
                    <div class="metric-value" style="color:{color};">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
