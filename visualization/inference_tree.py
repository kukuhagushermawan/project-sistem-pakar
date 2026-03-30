# ============================================================
# visualization/inference_tree.py
# @module  : visualization.inference_tree
# @desc    : Visualisasi pohon inferensi Backward Chaining
#            menggunakan Graphviz (st.graphviz_chart)
# ============================================================

import streamlit as st
import logging

logger = logging.getLogger("laptopdoc.visualization")

# Warna node sesuai UI Design Spec (Bright Dark Mode)
COLORS = {
    "proven": "#10B981",     # Green Success
    "failed": "#EF4444",     # Red Danger
    "rule": "#38BDF8",       # Primary Sky Blue
    "symptom_pos": "#22D3EE", # Cyan
    "symptom_neg": "#F87171", # Soft Red Danger
    "bg": "#162032",         # Bright Dark Midpoint
    "text": "#F8FAFC",       # Text Light
    "border": "rgba(255, 255, 255, 0.12)",
}


def render_inference_tree(results: list[dict], trace_log: list[dict]):
    """
    Render pohon inferensi menggunakan Graphviz.

    Membuat directed graph yang menunjukkan:
    - Node hipotesis (kotak hijau/merah)
    - Node rule (diamond biru)
    - Node gejala (ellipse cyan/merah)
    - Edge menghubungkan hipotesis → rule → gejala

    Args:
        results: List hasil diagnosis dari engine.get_all_results()
        trace_log: List trace log dari engine.get_trace_log()
    """
    try:
        dot_source = _build_dot(results, trace_log)
        st.graphviz_chart(dot_source, use_container_width=True)
    except Exception as e:
        logger.warning("Graphviz rendering failed: %s", e)
        st.info(
            "Visualisasi Graphviz tidak tersedia. "
            "Pastikan Graphviz terinstal di sistem.\n\n"
            "Install: `sudo apt install graphviz` atau download dari "
            "[graphviz.org](https://graphviz.org/download/)"
        )
        raise


def _build_dot(results: list[dict], trace_log: list[dict]) -> str:
    """
    Bangun DOT source string untuk Graphviz.

    Args:
        results: List hasil diagnosis.
        trace_log: List trace entries.

    Returns:
        str: DOT source untuk di-render.
    """
    lines = [
        'digraph InferenceTree {',
        '    rankdir=LR;',
        '    bgcolor="#162032";',
        '    node [fontname="Inter" fontsize=10 style=filled margin="0.2,0.1" shape=box rounded=true];',
        '    edge [fontname="Inter" fontsize=8 color="#475569"];',
        '',
    ]

    # Bangun lookup gejala per hipotesis dari trace
    symptom_data = {}  # {hypothesis: [(symptom, cf_user), ...]}
    rule_data = {}     # {hypothesis: [rule_id, ...]}

    for entry in trace_log:
        hyp = entry.get("hypothesis", "")
        action = entry.get("action", "")

        if action in ("RECEIVE_ANSWER", "CACHE_HIT"):
            if hyp not in symptom_data:
                symptom_data[hyp] = []
            symptom_data[hyp].append({
                "symptom": entry.get("symptom", ""),
                "cf_user": entry.get("cf_user", 0.0),
            })

        if action == "EVALUATE_HYPOTHESIS":
            rule_id = entry.get("rule")
            if rule_id and hyp not in rule_data:
                rule_data[hyp] = []
            if rule_id:
                rule_data[hyp].append(rule_id)

        if action == "CALCULATE_CF":
            rule_id = entry.get("rule")
            if hyp in rule_data and rule_id not in rule_data[hyp]:
                rule_data[hyp].append(rule_id)

    # Render hypothesis nodes
    for result in results:
        kode = result["kode_kerusakan"]
        nama = result.get("nama_kerusakan", "")
        status = result["status"]
        cf = result["cf_final"]

        if status == "TERBUKTI":
            color = COLORS["proven"]
            label = f"{kode}\\n{nama}\\nCF={cf*100:.0f}%"
        else:
            color = COLORS["failed"]
            label = f"{kode}\\n{nama}\\nGAGAL"

        lines.append(
            f'    "{kode}" [label="{label}" shape=box '
            f'fillcolor="{color}" fontcolor="white" '
            f'penwidth=2 color="{color}"];'
        )

    # Render rule nodes dan gejala
    rendered_symptoms = set()

    for result in results:
        kode = result["kode_kerusakan"]
        rules = rule_data.get(kode, [])

        for rule_id in rules:
            # Rule node
            rule_node = f"{kode}_{rule_id}"
            lines.append(
                f'    "{rule_node}" [label="{rule_id}" shape=diamond '
                f'fillcolor="{COLORS["rule"]}" fontcolor="white" '
                f'width=0.8 height=0.5];'
            )
            # Edge: hypothesis → rule
            lines.append(f'    "{kode}" -> "{rule_node}";')

        # Symptom nodes
        symptoms = symptom_data.get(kode, [])
        for sym in symptoms:
            sym_code = sym["symptom"]
            cf_user = sym["cf_user"]
            sym_node = f"{kode}_{sym_code}"

            # Warna berdasarkan CF
            if cf_user > 0:
                sym_color = COLORS["symptom_pos"]
            else:
                sym_color = COLORS["symptom_neg"]

            label = f"{sym_code}\\nCF={cf_user}"
            lines.append(
                f'    "{sym_node}" [label="{label}" shape=ellipse '
                f'fillcolor="{sym_color}" fontcolor="white" '
                f'width=0.7 height=0.4];'
            )

            # Edge: rule → symptom (attach to first rule)
            if rules:
                rule_node = f"{kode}_{rules[0]}"
                lines.append(f'    "{rule_node}" -> "{sym_node}";')

    lines.append('}')
    return '\n'.join(lines)
