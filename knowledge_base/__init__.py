# ============================================================
# knowledge_base/__init__.py
# Ekspor publik Knowledge Base — akses terpusat ke seluruh data
# ============================================================

from .frames import FRAMES
from .symptoms import SYMPTOMS
from .rules import RULES, RULES_BY_CONCLUSION


def get_frame(kode_kerusakan: str) -> dict | None:
    """Ambil data Frame kerusakan berdasarkan kode (K01-K10)."""
    return FRAMES.get(kode_kerusakan)


def get_symptom(kode_gejala: str) -> dict | None:
    """Ambil data gejala berdasarkan kode (G01-G25)."""
    return SYMPTOMS.get(kode_gejala)


def get_rules_for(kode_kerusakan: str) -> list[dict]:
    """Ambil semua rule yang konklusinya = kode_kerusakan."""
    return RULES_BY_CONCLUSION.get(kode_kerusakan, [])


def get_all_hypotheses() -> list[str]:
    """Ambil daftar kode kerusakan terurut (K01-K10) untuk iterasi BC."""
    return sorted(FRAMES.keys())
