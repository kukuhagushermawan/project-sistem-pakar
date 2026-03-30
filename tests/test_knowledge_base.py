# ============================================================
# tests/test_knowledge_base.py
# Unit Test — Integritas Knowledge Base
# Target: Validasi konsistensi Frame ↔ Rule ↔ Gejala
# ============================================================

import pytest
from knowledge_base import FRAMES, SYMPTOMS, RULES, RULES_BY_CONCLUSION


class TestFramesIntegrity:
    """Validasi 10 Frame kerusakan."""

    def test_total_frames(self):
        assert len(FRAMES) == 10

    def test_frame_kode_format(self):
        for kode in FRAMES:
            assert kode.startswith("K"), f"Kode {kode} tidak dimulai dengan 'K'"
            assert len(kode) == 3, f"Kode {kode} harus 3 karakter"

    def test_frame_required_slots(self):
        required = ["kode_kerusakan", "nama_kerusakan", "penyebab", "solusi_singkat", "cf_pakar"]
        for kode, frame in FRAMES.items():
            for slot in required:
                assert slot in frame, f"Frame {kode} missing slot: {slot}"

    def test_frame_cf_range(self):
        for kode, frame in FRAMES.items():
            cf = frame["cf_pakar"]
            assert 0.0 <= cf <= 1.0, f"Frame {kode} CF={cf} di luar range"


class TestSymptomsIntegrity:
    """Validasi 25 Gejala."""

    def test_total_symptoms(self):
        assert len(SYMPTOMS) == 25
        for kode in SYMPTOMS:
            assert kode.startswith("G"), f"Kode {kode} tidak dimulai dengan 'G'"

    def test_symptom_required_fields(self):
        for kode, symptom in SYMPTOMS.items():
            assert "teks_gejala" in symptom, f"Gejala {kode} missing teks_gejala"

    def test_no_duplicate_text(self):
        texts = [s["teks_gejala"] for s in SYMPTOMS.values()]
        assert len(texts) == len(set(texts)), "Ada duplikasi teks gejala"


class TestRulesIntegrity:
    """Validasi 12 Rule dan konsistensi referensi silang."""

    def test_total_rules(self):
        assert len(RULES) == 12

    def test_no_duplicate_rule_id(self):
        ids = [r["rule_id"] for r in RULES]
        assert len(ids) == len(set(ids)), "Ada duplikasi rule_id"

    def test_rule_konklusi_references_valid_frame(self):
        """Setiap konklusi rule harus merujuk ke Frame yang ada."""
        for rule in RULES:
            assert rule["konklusi"] in FRAMES, (
                f"Rule {rule['rule_id']} konklusi {rule['konklusi']} "
                f"tidak ada di FRAMES"
            )

    def test_rule_premis_references_valid_symptom(self):
        """Setiap premis rule harus merujuk ke Gejala yang ada."""
        for rule in RULES:
            for premis in rule["premis"]:
                assert premis in SYMPTOMS, (
                    f"Rule {rule['rule_id']} premis {premis} "
                    f"tidak ada di SYMPTOMS"
                )

    def test_rule_cf_range(self):
        for rule in RULES:
            assert 0.0 <= rule["cf_rule"] <= 1.0, (
                f"Rule {rule['rule_id']} CF={rule['cf_rule']} di luar range"
            )

    def test_no_orphan_frames(self):
        """Setiap Frame harus memiliki minimal 1 Rule."""
        concluded = {r["konklusi"] for r in RULES}
        for kode in FRAMES:
            assert kode in concluded, f"Frame {kode} tidak memiliki Rule (orphan)"

    def test_no_orphan_symptoms(self):
        """Setiap Gejala harus digunakan di minimal 1 Rule."""
        used = set()
        for rule in RULES:
            used.update(rule["premis"])
        for kode in SYMPTOMS:
            assert kode in used, f"Gejala {kode} tidak digunakan di Rule (orphan)"

    def test_k08_has_three_rules(self):
        """K08 (Motherboard) harus memiliki 3 rule (R8, R11, R12)."""
        k08_rules = RULES_BY_CONCLUSION.get("K08", [])
        assert len(k08_rules) == 3
        rule_ids = {r["rule_id"] for r in k08_rules}
        assert rule_ids == {"R8", "R11", "R12"}

    def test_shared_symptom_g07(self):
        """G07 harus digunakan di R3 (K03) dan R5 (K05)."""
        rules_with_g07 = [r["rule_id"] for r in RULES if "G07" in r["premis"]]
        assert "R3" in rules_with_g07
        assert "R5" in rules_with_g07

    def test_no_contradictory_rules(self):
        """Tidak ada 2 rule dengan premis identik tapi konklusi berbeda."""
        seen = {}
        for rule in RULES:
            premis_key = tuple(sorted(rule["premis"]))
            if premis_key in seen:
                assert seen[premis_key] == rule["konklusi"], (
                    f"Kontradiksi: premis {premis_key} → "
                    f"{seen[premis_key]} vs {rule['konklusi']}"
                )
            seen[premis_key] = rule["konklusi"]
