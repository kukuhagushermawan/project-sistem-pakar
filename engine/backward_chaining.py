# ============================================================
# engine/backward_chaining.py
# Inference Engine — Backward Chaining (Goal-Driven)
#
# Dua API tersedia:
# 1. BackwardChainingEngine (class) — untuk Streamlit wizard (step-by-step)
# 2. backward_chain(goal, user_answers) — untuk batch/programmatic call
# ============================================================

import logging
from datetime import datetime

from knowledge_base import (
    FRAMES,
    SYMPTOMS,
    RULES,
    RULES_BY_CONCLUSION,
    get_rules_for,
    get_all_hypotheses,
)
from .certainty_factor import CertaintyFactor, _validate_cf

logger = logging.getLogger("laptop_diagnostic_expert.engine.bc")


# ============================================================
# FUNGSI PUBLIK: backward_chain(goal, user_answers)
# API sederhana untuk evaluasi batch (non-interaktif)
# ============================================================

def backward_chain(
    goal: str | None = None,
    user_answers: dict[str, float] | None = None,
) -> dict:
    """
    Jalankan inferensi Backward Chaining secara batch (non-interaktif).

    Fungsi ini mengevaluasi satu hipotesis tertentu (goal) ATAU
    seluruh hipotesis (K01-K10) jika goal=None, menggunakan
    jawaban CF User yang sudah disediakan.

    Alur logika:
    1. Jika goal diberikan → evaluasi hipotesis tersebut saja.
       Jika goal=None → evaluasi seluruh hipotesis K01-K10.
    2. Untuk setiap hipotesis, cari rule yang konklusinya = hipotesis.
    3. Evaluasi premis satu per satu:
       - Jika CF User = 0.0 → SHORT-CIRCUIT, hipotesis GAGAL, skip sisa premis.
       - Jika CF User > 0.0 → kumpulkan untuk CF combine.
    4. Hitung CF final = CF_pakar × CF_user_kombinasi.
    5. Rekam setiap langkah ke trace_log untuk Explanation Facility.

    Args:
        goal: Kode kerusakan yang akan dievaluasi (misal: "K01").
              Jika None, evaluasi seluruh hipotesis K01-K10.
        user_answers: Dictionary jawaban user {kode_gejala: cf_user}.
                      Contoh: {"G01": 0.8, "G02": 0.6, "G18": 1.0}
                      Jika gejala tidak ada di dict → dianggap 0.0 (tidak dialami).

    Returns:
        dict: Hasil diagnosis dengan struktur:
            {
                "results": [
                    {
                        "kode_kerusakan": "K01",
                        "nama_kerusakan": "Adaptor/Charger Rusak",
                        "cf_final": 0.90,
                        "status": "TERBUKTI" | "GAGAL",
                        "rules_evaluated": [{"rule_id", "cf_final", "status"}],
                    }, ...
                ],
                "ranking": [...],  # Hanya yang TERBUKTI, sorted by CF desc
                "trace_log": [...],  # Log jejak inferensi lengkap
                "summary": {"total": N, "proven": N, "failed": N},
            }

    Raises:
        ValueError: Jika goal bukan kode kerusakan valid (K01-K10).
        ValueError: Jika cf_user di luar rentang [0.0, 1.0].

    Example:
        >>> answers = {"G01": 0.8, "G02": 0.6, "G18": 1.0}
        >>> result = backward_chain(goal="K01", user_answers=answers)
        >>> result["ranking"][0]["cf_final"]
        0.9
    """
    if user_answers is None:
        user_answers = {}

    # --- Validasi input ---
    for kode, cf_val in user_answers.items():
        _validate_cf(cf_val, f"user_answers['{kode}']")

    # Tentukan hipotesis yang akan dievaluasi
    if goal is not None:
        if goal not in FRAMES:
            raise ValueError(
                f"Goal '{goal}' bukan kode kerusakan valid. "
                f"Gunakan salah satu dari: {sorted(FRAMES.keys())}"
            )
        hypotheses_to_eval = [goal]
    else:
        hypotheses_to_eval = get_all_hypotheses()

    # --- Jalankan inferensi ---
    results = []
    trace_log = []
    step = 0

    for hypothesis in hypotheses_to_eval:
        rules = get_rules_for(hypothesis)
        frame = FRAMES.get(hypothesis, {})

        step += 1
        trace_log.append({
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "action": "EVALUATE_HYPOTHESIS",
            "hypothesis": hypothesis,
            "detail": f"Mulai evaluasi {hypothesis} — {frame.get('nama_kerusakan', '')} "
                      f"({len(rules)} rule)",
        })

        if not rules:
            # Tidak ada rule untuk hipotesis ini
            results.append({
                "kode_kerusakan": hypothesis,
                "nama_kerusakan": frame.get("nama_kerusakan", ""),
                "cf_final": 0.0,
                "status": "GAGAL",
                "rules_evaluated": [],
                "reason": "Tidak ada rule untuk hipotesis ini",
            })
            step += 1
            trace_log.append({
                "step": step,
                "action": "HYPOTHESIS_FAILED",
                "hypothesis": hypothesis,
                "reason": "No rules found",
            })
            continue

        # Evaluasi setiap rule untuk hipotesis ini
        rule_cf_finals = []
        rules_evaluated = []

        for rule in rules:
            rule_id = rule["rule_id"]
            cf_rule = rule["cf_rule"]
            premises = rule["premis"]
            cf_users_for_rule = []
            rule_passed = True

            step += 1
            trace_log.append({
                "step": step,
                "action": "EVALUATE_RULE",
                "hypothesis": hypothesis,
                "rule": rule_id,
                "premises": premises,
                "cf_rule": cf_rule,
            })

            # Evaluasi premis satu per satu
            for p_idx, kode_gejala in enumerate(premises):
                cf_user = user_answers.get(kode_gejala, 0.0)

                step += 1
                trace_log.append({
                    "step": step,
                    "action": "CHECK_PREMISE",
                    "hypothesis": hypothesis,
                    "rule": rule_id,
                    "symptom": kode_gejala,
                    "teks_gejala": SYMPTOMS.get(kode_gejala, {}).get("teks_gejala", ""),
                    "premise_index": p_idx + 1,
                    "total_premises": len(premises),
                    "cf_user": cf_user,
                })

                if cf_user == 0.0:
                    # === SHORT-CIRCUIT ===
                    # Gejala dijawab 0.0 → rule GAGAL, skip premis tersisa
                    step += 1
                    trace_log.append({
                        "step": step,
                        "action": "SHORT_CIRCUIT",
                        "hypothesis": hypothesis,
                        "rule": rule_id,
                        "symptom": kode_gejala,
                        "detail": (
                            f"CF User = 0.0 untuk {kode_gejala}. "
                            f"Rule {rule_id} GAGAL. "
                            f"Skip {len(premises) - p_idx - 1} premis tersisa."
                        ),
                    })
                    rule_passed = False
                    break
                else:
                    # CF > 0 → kumpulkan
                    cf_users_for_rule.append(cf_user)

            # Hitung CF final untuk rule ini
            if rule_passed and cf_users_for_rule:
                cf_user_combined = min(cf_users_for_rule)
                cf_final_rule = CertaintyFactor.calculate_cf_kombinasi(
                    cf_rule, cf_users_for_rule
                )
                rule_cf_finals.append(cf_final_rule)

                # Rekam langkah perhitungan CF
                cf_steps = []
                if len(cf_users_for_rule) > 1:
                    cf_steps.append({
                        "operation": "min",
                        "cf_users": cf_users_for_rule.copy(),
                        "result": cf_user_combined,
                    })
                cf_steps.append({
                    "operation": "final",
                    "cf_rule": cf_rule,
                    "cf_user_combined": cf_user_combined,
                    "cf_final": cf_final_rule,
                    "formula": f"CF_final = {cf_rule} × {cf_user_combined:.4f} = {cf_final_rule:.4f}",
                })

                step += 1
                trace_log.append({
                    "step": step,
                    "action": "CALCULATE_CF",
                    "hypothesis": hypothesis,
                    "rule": rule_id,
                    "cf_users": cf_users_for_rule,
                    "cf_steps": cf_steps,
                    "cf_final": cf_final_rule,
                })

                rules_evaluated.append({
                    "rule_id": rule_id,
                    "cf_rule": cf_rule,
                    "cf_users": cf_users_for_rule,
                    "cf_final": cf_final_rule,
                    "status": "TERPENUHI",
                })
            else:
                rules_evaluated.append({
                    "rule_id": rule_id,
                    "cf_rule": cf_rule,
                    "cf_users": cf_users_for_rule,
                    "cf_final": 0.0,
                    "status": "GAGAL",
                })

        # Finalisasi hipotesis
        if rule_cf_finals:
            cf_hypothesis = CertaintyFactor.combine_multi_rules(rule_cf_finals)
            status = "TERBUKTI"

            if len(rule_cf_finals) > 1:
                step += 1
                trace_log.append({
                    "step": step,
                    "action": "COMBINE_MULTI_RULES",
                    "hypothesis": hypothesis,
                    "rules_cf": rule_cf_finals.copy(),
                    "cf_final_combined": cf_hypothesis,
                    "detail": f"Mengombinasikan {len(rule_cf_finals)} rule untuk {hypothesis}",
                })

            step += 1
            trace_log.append({
                "step": step,
                "action": "HYPOTHESIS_PROVEN",
                "hypothesis": hypothesis,
                "cf_final": cf_hypothesis,
                "rules_cf": rule_cf_finals,
                "detail": f"Hipotesis {hypothesis} TERBUKTI (CF={cf_hypothesis:.4f})",
            })
        else:
            cf_hypothesis = 0.0
            status = "GAGAL"

            step += 1
            trace_log.append({
                "step": step,
                "action": "HYPOTHESIS_FAILED",
                "hypothesis": hypothesis,
                "cf_final": 0.0,
                "detail": f"Hipotesis {hypothesis} GAGAL — tidak ada rule terpenuhi",
            })

        results.append({
            "kode_kerusakan": hypothesis,
            "nama_kerusakan": frame.get("nama_kerusakan", ""),
            "cf_final": cf_hypothesis,
            "cf_percentage": f"{cf_hypothesis * 100:.1f}%",
            "status": status,
            "rules_evaluated": rules_evaluated,
            "penyebab": frame.get("penyebab", ""),
            "solusi_singkat": frame.get("solusi_singkat", ""),
            "solusi_detail": frame.get("solusi_detail", ""),
        })

    # Bangun ranking (hanya yang TERBUKTI, sorted descending)
    ranking = sorted(
        [r for r in results if r["status"] == "TERBUKTI"],
        key=lambda x: x["cf_final"],
        reverse=True,
    )
    for i, item in enumerate(ranking):
        item["rank"] = i + 1

    proven_count = len(ranking)
    failed_count = len(results) - proven_count

    logger.info(
        "backward_chain selesai: %d terbukti, %d gagal dari %d hipotesis",
        proven_count, failed_count, len(results),
    )

    return {
        "results": results,
        "ranking": ranking,
        "trace_log": trace_log,
        "summary": {
            "total": len(results),
            "proven": proven_count,
            "failed": failed_count,
        },
    }


# ============================================================
# CLASS: BackwardChainingEngine (untuk Streamlit wizard)
# Mendukung interaksi step-by-step (satu pertanyaan per langkah)
# ============================================================

class BackwardChainingEngine:
    """
    Mesin inferensi Backward Chaining untuk mode interaktif (wizard).

    Digunakan oleh Streamlit UI untuk konsultasi step-by-step:
    setiap panggilan get_current_question() mengembalikan satu pertanyaan
    gejala, dan submit_answer() menerima jawaban lalu menentukan
    langkah selanjutnya.

    Alur:
        1. Iterasi hipotesis K01 → K10 secara berurutan.
        2. Untuk setiap hipotesis, cari rule yang konklusinya = hipotesis.
        3. Evaluasi premis/gejala satu per satu (wizard step-by-step).
        4. Jika CF User = 0.0 → SHORT-CIRCUIT: hipotesis GAGAL, skip sisa premis.
        5. Jika semua premis terpenuhi → hitung CF, hipotesis TERBUKTI.
        6. Setelah K10 selesai → ranking berdasarkan CF tertinggi.

    Attributes:
        hypotheses: List kode kerusakan terurut [K01..K10].
        answers: Cache jawaban user {kode_gejala: cf_user}.
        results: List hasil diagnosis per hipotesis.
        trace_log: Log jejak inferensi untuk Explanation Facility.

    Example:
        >>> engine = BackwardChainingEngine()
        >>> engine.start()
        >>> q = engine.get_current_question()
        >>> engine.submit_answer(q["kode_gejala"], 0.8)
    """

    def __init__(self):
        """Inisialisasi engine dengan state kosong."""
        self.hypotheses: list[str] = []
        self.current_hyp_idx: int = 0
        self.current_rules: list[dict] = []
        self.current_rule_idx: int = 0
        self.current_premise_idx: int = 0

        # Cache jawaban user: {kode_gejala: cf_user}
        self.answers: dict[str, float] = {}

        # Hasil diagnosis per hipotesis
        self.results: list[dict] = []

        # Trace log untuk Explanation Facility (ADR-001)
        self.trace_log: list[dict] = []
        self._step_counter: int = 0

        # CF per rule untuk hipotesis aktif
        self._current_cf_users: list[float] = []
        self._current_rule_cf_finals: list[float] = []

        self._finished: bool = False
        self._started: bool = False

    # ── Lifecycle ───────────────────────────────────────────

    def start(self) -> None:
        """
        Inisialisasi engine dan mulai dari hipotesis pertama (K01).

        Harus dipanggil sebelum get_current_question() atau submit_answer().
        Memuat daftar hipotesis dari Knowledge Base dan menyiapkan
        rule untuk hipotesis pertama.
        """
        self.hypotheses = get_all_hypotheses()
        self.current_hyp_idx = 0
        self._current_rule_cf_finals = []
        self._started = True

        logger.info("Engine started. Hypotheses: %s", self.hypotheses)
        self._load_rules_for_current_hypothesis()

    def is_finished(self) -> bool:
        """
        Apakah konsultasi sudah selesai?

        Returns:
            bool: True jika seluruh hipotesis telah dievaluasi.
        """
        return self._finished

    def get_progress(self) -> tuple[int, int]:
        """
        Ambil progress konsultasi saat ini.

        Returns:
            tuple[int, int]: (hipotesis_ke_n, total_hipotesis).
                Contoh: (3, 10) berarti sedang evaluasi hipotesis ke-3 dari 10.
        """
        total = len(self.hypotheses)
        current = min(self.current_hyp_idx + 1, total)
        return (current, total)

    # ── Internal State Management ──────────────────────────

    def _log_trace(self, action: str, **kwargs) -> None:
        """
        Rekam satu entry trace log untuk Explanation Facility.

        Setiap langkah inferensi direkam secara kronologis,
        memenuhi ADR-001 (Trace Log Pattern).

        Args:
            action: Jenis aksi (EVALUATE_HYPOTHESIS, ASK_SYMPTOM, dll.)
            **kwargs: Data tambahan yang relevan untuk aksi tersebut.
        """
        self._step_counter += 1
        entry = {
            "step": self._step_counter,
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "hypothesis": self._current_hypothesis_code(),
            **kwargs,
        }
        self.trace_log.append(entry)
        logger.debug("TRACE [%d] %s: %s", self._step_counter, action, kwargs)

    def _current_hypothesis_code(self) -> str:
        """
        Ambil kode hipotesis yang sedang aktif.

        Returns:
            str: Kode kerusakan (misal "K01"), atau "" jika sudah habis.
        """
        if self.current_hyp_idx < len(self.hypotheses):
            return self.hypotheses[self.current_hyp_idx]
        return ""

    def _load_rules_for_current_hypothesis(self) -> None:
        """Muat rules untuk hipotesis aktif dan reset semua index premis."""
        hyp = self._current_hypothesis_code()
        self.current_rules = get_rules_for(hyp)
        self.current_rule_idx = 0
        self.current_premise_idx = 0
        self._current_cf_users = []
        self._current_rule_cf_finals = []

        self._log_trace(
            "EVALUATE_HYPOTHESIS",
            rule=self.current_rules[0]["rule_id"] if self.current_rules else None,
            detail=f"Mulai evaluasi hipotesis {hyp} ({len(self.current_rules)} rule)",
        )

    # ── Question & Answer ──────────────────────────────────

    def get_current_question(self) -> dict | None:
        """
        Ambil pertanyaan gejala berikutnya yang harus ditanyakan ke user.

        Method ini secara otomatis:
        - Skip gejala yang sudah dijawab (shared symptom caching).
        - Finalisasi rule jika semua premis terpenuhi.
        - Pindah ke hipotesis berikutnya jika rule habis.

        Returns:
            dict | None: Dictionary berisi info gejala + context, atau
                None jika konsultasi sudah selesai. Struktur:
                {
                    "kode_gejala": "G01",
                    "teks_gejala": "...",
                    "deskripsi_detail": "...",
                    "hypothesis": {"kode", "nama", "index", "total"},
                    "rule": {"rule_id", "cf_rule", "total_premises", "current_premise_index"},
                }
        """
        if self._finished or not self._started:
            return None

        while self.current_hyp_idx < len(self.hypotheses):
            if not self.current_rules:
                self._mark_hypothesis_failed("Tidak ada rule untuk hipotesis ini")
                if not self._next_hypothesis():
                    return None
                continue

            rule = self.current_rules[self.current_rule_idx]
            premises = rule["premis"]

            if self.current_premise_idx < len(premises):
                kode_gejala = premises[self.current_premise_idx]

                # Shared symptom cache: skip jika sudah dijawab sebelumnya
                if kode_gejala in self.answers:
                    cached_cf = self.answers[kode_gejala]
                    logger.info("Cache hit: %s = %.1f", kode_gejala, cached_cf)
                    self._log_trace(
                        "CACHE_HIT",
                        rule=rule["rule_id"],
                        symptom=kode_gejala,
                        cf_user=cached_cf,
                    )
                    self._process_answer_internal(kode_gejala, cached_cf)
                    continue

                # Kembalikan pertanyaan untuk gejala ini
                symptom = SYMPTOMS.get(kode_gejala, {})
                self._log_trace(
                    "ASK_SYMPTOM",
                    rule=rule["rule_id"],
                    symptom=kode_gejala,
                    detail=f"Premis {self.current_premise_idx + 1}/{len(premises)} dari {rule['rule_id']}",
                )
                return {
                    "kode_gejala": kode_gejala,
                    "teks_gejala": symptom.get("teks_gejala", ""),
                    "deskripsi_detail": symptom.get("deskripsi_detail", ""),
                    "kategori": symptom.get("kategori", ""),
                    "hypothesis": {
                        "kode": self._current_hypothesis_code(),
                        "nama": FRAMES.get(
                            self._current_hypothesis_code(), {}
                        ).get("nama_kerusakan", ""),
                        "index": self.current_hyp_idx + 1,
                        "total": len(self.hypotheses),
                    },
                    "rule": {
                        "rule_id": rule["rule_id"],
                        "cf_rule": rule["cf_rule"],
                        "total_premises": len(premises),
                        "current_premise_index": self.current_premise_idx + 1,
                    },
                }
            else:
                # Semua premis rule ini terpenuhi → hitung CF
                self._finalize_current_rule()

                # Lanjut ke rule berikutnya (multi-rule) atau hipotesis berikutnya
                self.current_rule_idx += 1
                self.current_premise_idx = 0
                self._current_cf_users = []

                if self.current_rule_idx >= len(self.current_rules):
                    self._finalize_hypothesis()
                    if not self._next_hypothesis():
                        return None
                    continue

        self._finished = True
        return None

    def submit_answer(self, kode_gejala: str, cf_user: float) -> dict:
        """
        Terima jawaban CF User untuk gejala yang sedang ditanyakan.

        Args:
            kode_gejala: Kode gejala yang dijawab (harus sesuai pertanyaan aktif).
            cf_user: Nilai keyakinan user (hanya: 0.0, 0.4, 0.6, 0.8, 1.0).

        Returns:
            dict: Status pemrosesan:
                {"event": "next_question" | "hypothesis_failed", "short_circuit": bool}

        Raises:
            ValueError: Jika cf_user bukan salah satu dari {0.0, 0.4, 0.6, 0.8, 1.0}.
        """
        valid_cf = {0.0, 0.4, 0.6, 0.8, 1.0}
        if cf_user not in valid_cf:
            raise ValueError(
                f"CF User tidak valid: {cf_user}. "
                f"Hanya {sorted(valid_cf)} yang diterima."
            )

        # Simpan ke cache
        self.answers[kode_gejala] = cf_user

        self._log_trace(
            "RECEIVE_ANSWER",
            rule=(
                self.current_rules[self.current_rule_idx]["rule_id"]
                if self.current_rules else None
            ),
            symptom=kode_gejala,
            cf_user=cf_user,
            result="SHORT_CIRCUIT" if cf_user == 0.0 else "CONTINUE",
        )

        return self._process_answer_internal(kode_gejala, cf_user)

    # ── Internal Processing ────────────────────────────────

    def _process_answer_internal(self, kode_gejala: str, cf_user: float) -> dict:
        """
        Proses jawaban CF User (dari user langsung atau dari cache).

        Args:
            kode_gejala: Kode gejala yang dijawab.
            cf_user: Nilai CF User.

        Returns:
            dict: {"event": str, "short_circuit": bool}
        """
        if cf_user == 0.0:
            # SHORT-CIRCUIT: premis gagal → hipotesis gagal
            self._mark_hypothesis_failed(f"Short-circuit pada {kode_gejala}")
            self._next_hypothesis()
            return {"event": "hypothesis_failed", "short_circuit": True}

        # CF > 0 → kumpulkan dan lanjut ke premis berikutnya
        self._current_cf_users.append(cf_user)
        self.current_premise_idx += 1
        return {"event": "next_question", "short_circuit": False}

    def _finalize_current_rule(self) -> None:
        """Hitung CF final untuk rule aktif setelah semua premis terpenuhi."""
        rule = self.current_rules[self.current_rule_idx]
        cf_final = CertaintyFactor.calculate_cf_kombinasi(
            rule["cf_rule"], self._current_cf_users
        )
        self._current_rule_cf_finals.append(cf_final)

        # Rekam trace kalkulasi CF step-by-step
        cf_steps = []
        cf_user_combined = min(self._current_cf_users) if self._current_cf_users else 0.0
        
        if len(self._current_cf_users) > 1:
            cf_steps.append({
                "operation": "min",
                "cf_users": self._current_cf_users.copy(),
                "result": cf_user_combined,
            })
            
        cf_steps.append({
            "operation": "final",
            "cf_rule": rule["cf_rule"],
            "cf_user_combined": cf_user_combined,
            "cf_final": cf_final,
        })

        self._log_trace(
            "CALCULATE_CF",
            rule=rule["rule_id"],
            cf_steps=cf_steps,
            detail=f"CF Final {rule['rule_id']} = {cf_final:.4f}",
        )

    def _finalize_hypothesis(self) -> None:
        """Finalisasi hipotesis setelah semua rule-nya dievaluasi."""
        hyp = self._current_hypothesis_code()
        if self._current_rule_cf_finals:
            cf_final = CertaintyFactor.combine_multi_rules(
                self._current_rule_cf_finals
            )
            
            if len(self._current_rule_cf_finals) > 1:
                self._log_trace(
                    "COMBINE_MULTI_RULES",
                    rules_cf=self._current_rule_cf_finals.copy(),
                    cf_final_combined=cf_final,
                    detail=f"Mengombinasikan {len(self._current_rule_cf_finals)} rule secara berurutan",
                )

            self.results.append({
                "kode_kerusakan": hyp,
                "nama_kerusakan": FRAMES.get(hyp, {}).get("nama_kerusakan", ""),
                "cf_final": cf_final,
                "status": "TERBUKTI",
                "rules_triggered": [r["rule_id"] for r in self.current_rules],
            })
            self._log_trace(
                "HYPOTHESIS_PROVEN",
                cf_final=cf_final,
                detail=f"Hipotesis {hyp} TERBUKTI (CF={cf_final:.4f})",
            )
        else:
            self._mark_hypothesis_failed("Tidak ada rule yang terpenuhi")

    def _mark_hypothesis_failed(self, reason: str) -> None:
        """
        Tandai hipotesis aktif sebagai GAGAL.

        Args:
            reason: Deskripsi alasan kegagalan untuk trace log.
        """
        hyp = self._current_hypothesis_code()
        self.results.append({
            "kode_kerusakan": hyp,
            "nama_kerusakan": FRAMES.get(hyp, {}).get("nama_kerusakan", ""),
            "cf_final": 0.0,
            "status": "GAGAL",
            "rules_triggered": [],
        })
        self._log_trace(
            "HYPOTHESIS_FAILED",
            cf_final=0.0,
            reason=reason,
        )
        logger.info("Hipotesis %s GAGAL: %s", hyp, reason)

    def _next_hypothesis(self) -> bool:
        """
        Pindah ke hipotesis berikutnya dalam urutan.

        Returns:
            bool: True jika berhasil pindah, False jika sudah habis (K10 selesai).
        """
        self.current_hyp_idx += 1
        if self.current_hyp_idx >= len(self.hypotheses):
            self._finished = True
            logger.info("Semua hipotesis selesai dievaluasi.")
            return False
        self._load_rules_for_current_hypothesis()
        return True

    # ── Result Getters ─────────────────────────────────────

    def get_results(self) -> list[dict]:
        """
        Ambil hasil diagnosis yang terbukti, terurut berdasarkan CF tertinggi.

        Returns:
            list[dict]: List kerusakan yang TERBUKTI dengan field "rank" tambahan.
                Diurut descending berdasarkan cf_final.
        """
        proven = [r for r in self.results if r["status"] == "TERBUKTI"]
        proven.sort(key=lambda x: x["cf_final"], reverse=True)
        for i, result in enumerate(proven):
            result["rank"] = i + 1
        return proven

    def get_all_results(self) -> list[dict]:
        """
        Ambil semua hasil (termasuk yang GAGAL) untuk visualisasi pohon.

        Returns:
            list[dict]: Seluruh hasil diagnosis (TERBUKTI + GAGAL).
        """
        return self.results

    def get_trace_log(self) -> list[dict]:
        """
        Ambil trace log lengkap untuk Explanation Facility.

        Trace log berisi entry kronologis setiap langkah inferensi:
        EVALUATE_HYPOTHESIS, ASK_SYMPTOM, RECEIVE_ANSWER, CACHE_HIT,
        CALCULATE_CF, HYPOTHESIS_PROVEN, HYPOTHESIS_FAILED, SHORT_CIRCUIT.

        Returns:
            list[dict]: List trace entries terurut berdasarkan step number.
        """
        return self.trace_log
