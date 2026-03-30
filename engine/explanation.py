# ============================================================
# engine/explanation.py
# Explanation Facility — Why & How (ADR-001: Trace Log Pattern)
# ============================================================

import logging
from knowledge_base import get_frame, get_symptom

logger = logging.getLogger("laptop_diagnostic_expert.engine.explanation")


class ExplanationFacility:
    """Generator penjelasan Why (Mengapa) & How (Bagaimana)."""

    @staticmethod
    def why(
        kode_gejala: str,
        kode_kerusakan: str,
        rule: dict,
        premise_index: int,
    ) -> str:
        """
        Generate teks penjelasan 'Mengapa gejala ini ditanyakan?'

        Args:
            kode_gejala: Kode gejala aktif (misal: G01)
            kode_kerusakan: Kode kerusakan/hipotesis aktif (misal: K01)
            rule: Dict rule yang sedang dievaluasi
            premise_index: Urutan premis dalam rule (1-based)

        Returns:
            Teks penjelasan dalam bahasa Indonesia
        """
        symptom = get_symptom(kode_gejala)
        frame = get_frame(kode_kerusakan)

        if not symptom or not frame:
            return "Informasi penjelasan tidak tersedia saat ini."

        text = (
            f"<ul style='margin:0; padding-left:1.5rem; color: var(--text-secondary);'>"
            f"<li><strong>Hipotesis yang sedang diuji:</strong> {kode_kerusakan} ({frame['nama_kerusakan']})</li>"
            f"<li><strong>Gejala saat ini:</strong> {kode_gejala} ({symptom['teks_gejala']})</li>"
            f"<li><strong>Peran gejala:</strong> Premis ke-{premise_index} dari Rule {rule['rule_id']}</li>"
            f"<li><strong>Dampak jawaban:</strong> Jawaban Anda pada gejala ini akan langsung memengaruhi kepastian diagnosis {kode_kerusakan}.</li>"
            f"</ul>"
        )
        logger.debug("why() → %s / %s / %s", kode_gejala, kode_kerusakan, rule["rule_id"])
        return text

    @staticmethod
    def how(diagnosis: dict, trace_entries: list[dict]) -> dict:
        """
        Generate penjelasan detail 'Bagaimana diagnosis ini diperoleh?'

        Args:
            diagnosis: Dict hasil diagnosis (kode, cf_final, rules_triggered, dll.)
            trace_entries: List trace log entries terkait hipotesis ini

        Returns:
            Dict berisi detail perhitungan CF per rule
        """
        kode = diagnosis.get("kode_kerusakan", "")
        frame = get_frame(kode)
        if not frame:
            return {"error": "Frame tidak ditemukan"}

        # Filter trace untuk hipotesis ini
        relevant = [t for t in trace_entries if t.get("hypothesis") == kode]

        # Bangun detail per rule
        details = []
        for entry in relevant:
            if entry.get("action") == "CALCULATE_CF":
                details.append({
                    "rule_id": entry.get("rule", ""),
                    "cf_steps": entry.get("cf_steps", []),
                })

        result = {
            "kode_kerusakan": kode,
            "nama_kerusakan": frame["nama_kerusakan"],
            "cf_final": diagnosis.get("cf_final", 0.0),
            "rules_detail": details,
            "trace_count": len(relevant),
        }
        logger.debug("how() → %s (cf=%.4f)", kode, result["cf_final"])
        return result
