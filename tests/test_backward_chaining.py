# ============================================================
# tests/test_backward_chaining.py
# Unit & Integration Test — Backward Chaining Engine
# Pola: Arrange-Act-Assert (AAA) per test method
# Target: Short-circuit, caching, trace log, fungsi backward_chain()
# ============================================================

import pytest
from engine.backward_chaining import BackwardChainingEngine, backward_chain


# ============================================================
# TEST: Fungsi backward_chain(goal, user_answers)
# API batch/non-interaktif
# ============================================================

class TestBackwardChainFunction:
    """Test suite untuk fungsi backward_chain(goal, user_answers)."""

    def test_single_goal_k01_terbukti(self):
        """K01 harus TERBUKTI jika semua gejala R1 dijawab positif."""
        # Arrange
        answers = {"G01": 0.8, "G02": 0.6, "G18": 1.0}

        # Act
        result = backward_chain(goal="K01", user_answers=answers)

        # Assert
        assert result["summary"]["proven"] == 1
        assert result["ranking"][0]["kode_kerusakan"] == "K01"
        assert result["ranking"][0]["cf_final"] == pytest.approx(0.54, abs=1e-2)
        assert result["ranking"][0]["status"] == "TERBUKTI"

    def test_single_goal_k01_gagal_short_circuit(self):
        """K01 harus GAGAL jika gejala pertama dijawab 0.0 (short-circuit)."""
        # Arrange
        answers = {"G01": 0.0}  # G01 = 0.0 → short-circuit

        # Act
        result = backward_chain(goal="K01", user_answers=answers)

        # Assert
        assert result["summary"]["proven"] == 0
        assert result["summary"]["failed"] == 1
        assert result["results"][0]["status"] == "GAGAL"

    def test_single_goal_k01_gagal_gejala_tidak_dijawab(self):
        """K01 GAGAL jika gejala tidak ada di answers (default 0.0)."""
        # Arrange
        answers = {}  # Kosong → semua default 0.0

        # Act
        result = backward_chain(goal="K01", user_answers=answers)

        # Assert
        assert result["results"][0]["status"] == "GAGAL"

    def test_evaluasi_seluruh_hipotesis(self):
        """Tanpa goal → evaluasi K01 sampai K10 (10 hipotesis)."""
        # Arrange
        answers = {
            "G01": 0.8, "G02": 0.6, "G18": 1.0,  # K01 terbukti
            "G08": 0.8, "G09": 0.6, "G10": 0.8,   # K04 terbukti
        }

        # Act
        result = backward_chain(goal=None, user_answers=answers)

        # Assert
        assert result["summary"]["total"] == 10
        assert result["summary"]["proven"] >= 2
        # K01 dan K04 harus ada di ranking
        ranking_codes = [r["kode_kerusakan"] for r in result["ranking"]]
        assert "K01" in ranking_codes
        assert "K04" in ranking_codes

    def test_ranking_sorted_descending(self):
        """Ranking harus terurut berdasarkan CF tertinggi."""
        # Arrange
        answers = {
            "G01": 0.8, "G02": 0.6, "G18": 1.0,  # K01 → CF tinggi
            "G22": 0.4,                             # K09 → CF rendah
        }

        # Act
        result = backward_chain(goal=None, user_answers=answers)

        # Assert
        if len(result["ranking"]) >= 2:
            assert result["ranking"][0]["cf_final"] >= result["ranking"][1]["cf_final"]

    def test_goal_tidak_valid_raise_error(self):
        """Goal yang bukan K01-K10 harus raise ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="bukan kode kerusakan valid"):
            backward_chain(goal="K99", user_answers={})

    def test_cf_user_out_of_range_raise_error(self):
        """CF User < -1.0 harus raise ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="harus dalam rentang"):
            backward_chain(goal="K01", user_answers={"G01": -1.5})

    def test_cf_user_diatas_satu_raise_error(self):
        """CF User > 1.0 harus raise ValueError."""
        with pytest.raises(ValueError):
            backward_chain(goal="K01", user_answers={"G01": 1.5})

    def test_single_rule_k08(self):
        """
        K08 memiliki 1 rule (R8).
        Jika R8 terbukti (G19, G20, G21 terjawab) → K08 TERBUKTI.
        """
        # Arrange — R8 terbukti
        answers = {
            "G19": 0.8,
            "G20": 0.6,
            "G21": 0.4,
        }

        # Act
        result = backward_chain(goal="K08", user_answers=answers)

        # Assert
        k08 = result["results"][0]
        assert k08["status"] == "TERBUKTI"
        assert k08["cf_final"] > 0

    def test_trace_log_ada_dan_kronologis(self):
        """Trace log harus ada dan step numbers naik berurutan."""
        # Arrange
        answers = {"G01": 0.8, "G02": 0.6, "G18": 1.0}

        # Act
        result = backward_chain(goal="K01", user_answers=answers)

        # Assert
        trace = result["trace_log"]
        assert len(trace) > 0

        steps = [entry["step"] for entry in trace]
        assert steps == sorted(steps), "Step numbers harus naik berurutan"

    def test_trace_log_berisi_short_circuit(self):
        """Trace log harus merekam event SHORT_CIRCUIT."""
        # Arrange
        answers = {"G01": 0.0}

        # Act
        result = backward_chain(goal="K01", user_answers=answers)

        # Assert
        actions = [entry["action"] for entry in result["trace_log"]]
        assert "SHORT_CIRCUIT" in actions

    def test_trace_log_berisi_calculate_cf(self):
        """Trace log harus merekam event CALCULATE_CF saat hipotesis terbukti."""
        # Arrange
        answers = {"G01": 0.8, "G02": 0.6, "G18": 1.0}

        # Act
        result = backward_chain(goal="K01", user_answers=answers)

        # Assert
        actions = [entry["action"] for entry in result["trace_log"]]
        assert "CALCULATE_CF" in actions

        # Cari entry CALCULATE_CF dan pastikan ada cf_steps
        calc_entries = [e for e in result["trace_log"] if e["action"] == "CALCULATE_CF"]
        assert len(calc_entries) > 0
        assert "cf_steps" in calc_entries[0]
        assert "cf_final" in calc_entries[0]

    def test_solusi_tersedia_untuk_hipotesis_terbukti(self):
        """Hasil yang TERBUKTI harus menyertakan penyebab dan solusi."""
        # Arrange
        answers = {"G01": 0.8, "G02": 0.6, "G18": 1.0}

        # Act
        result = backward_chain(goal="K01", user_answers=answers)

        # Assert
        k01 = result["results"][0]
        assert k01["penyebab"] != ""
        assert k01["solusi_singkat"] != ""
        assert k01["solusi_detail"] != ""


# ============================================================
# TEST: BackwardChainingEngine (class, untuk Streamlit wizard)
# ============================================================

class TestEngineInit:
    """Test inisialisasi BackwardChainingEngine."""

    def test_start_memuat_10_hipotesis(self):
        """Engine harus memuat 10 hipotesis (K01-K10) saat start()."""
        # Arrange
        engine = BackwardChainingEngine()

        # Act
        engine.start()

        # Assert
        assert len(engine.hypotheses) == 10

    def test_pertanyaan_pertama_adalah_g01(self):
        """Pertanyaan pertama harus G01 (premis pertama R1 untuk K01)."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act
        question = engine.get_current_question()

        # Assert
        assert question is not None
        assert question["kode_gejala"] == "G01"

    def test_belum_selesai_saat_start(self):
        """Engine belum finished setelah baru start."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act & Assert
        assert engine.is_finished() is False

    def test_progress_awal_1_dari_10(self):
        """Progress awal harus (1, 10)."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act
        current, total = engine.get_progress()

        # Assert
        assert current == 1
        assert total == 10


class TestEngineShortCircuit:
    """Test early termination saat CF User = 0.0."""

    def test_hipotesis_gagal_saat_cf_nol(self):
        """CF = 0.0 harus menyebabkan hipotesis aktif GAGAL."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act
        result = engine.submit_answer("G01", 0.0)

        # Assert
        assert result["short_circuit"] is True
        assert result["event"] == "hypothesis_failed"

    def test_skip_premis_tersisa_setelah_short_circuit(self):
        """Setelah short-circuit K01, pertanyaan berikutnya harus dari K02."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act — K01 gagal via G01=0.0
        engine.submit_answer("G01", 0.0)
        question = engine.get_current_question()

        # Assert — harus dari K02 (bukan G02 yang masih milik K01)
        assert question is not None
        assert question["hypothesis"]["kode"] == "K02"


class TestEngineHypothesisProven:
    """Test hipotesis terbukti saat semua premis terpenuhi."""

    def test_k01_terbukti_semua_positif(self):
        """K01 TERBUKTI jika semua premis R1 (G01, G02, G18) dijawab > 0."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act — jawab semua premis K01
        engine.submit_answer("G01", 0.8)
        engine.submit_answer("G02", 0.6)
        engine.submit_answer("G18", 1.0)

        # Panggil get_current_question() agar engine memproses
        # finalisasi rule dan hipotesis sebelum lanjut ke K02
        engine.get_current_question()

        # Assert
        proven = [r for r in engine.results if r["status"] == "TERBUKTI"]
        k01 = next((r for r in proven if r["kode_kerusakan"] == "K01"), None)
        assert k01 is not None
        assert k01["cf_final"] == pytest.approx(0.54, abs=1e-2)


class TestEngineCFValidation:
    """Test validasi input CF User pada engine."""

    def test_cf_tidak_valid_raise_error(self):
        """CF 0.5 (bukan skala valid) harus raise ValueError."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act & Assert
        with pytest.raises(ValueError):
            engine.submit_answer("G01", 0.5)

    def test_cf_valid_diterima(self):
        """CF 0.8 (skala valid) harus diterima tanpa error."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act (tidak boleh raise exception)
        result = engine.submit_answer("G01", 0.8)

        # Assert
        assert result["event"] == "next_question"


class TestEngineTraceLog:
    """Test recording trace log untuk Explanation Facility."""

    def test_trace_log_terekam_setelah_jawaban(self):
        """Trace log harus terisi setelah ada jawaban."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act
        engine.submit_answer("G01", 0.8)

        # Assert
        trace = engine.get_trace_log()
        assert len(trace) > 0

    def test_trace_entry_memiliki_field_wajib(self):
        """Setiap trace entry harus punya step, action, hypothesis."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act
        engine.submit_answer("G01", 0.8)

        # Assert
        for entry in engine.get_trace_log():
            assert "step" in entry
            assert "action" in entry
            assert "hypothesis" in entry

    def test_trace_merekam_receive_answer(self):
        """Action 'RECEIVE_ANSWER' harus ada di trace setelah submit."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act
        engine.submit_answer("G01", 0.8)

        # Assert
        actions = [e["action"] for e in engine.get_trace_log()]
        assert "RECEIVE_ANSWER" in actions

    def test_trace_merekam_short_circuit(self):
        """Short-circuit harus terekam sebagai event di trace."""
        # Arrange
        engine = BackwardChainingEngine()
        engine.start()

        # Act
        engine.submit_answer("G01", 0.0)

        # Assert
        actions = [e["action"] for e in engine.get_trace_log()]
        assert "HYPOTHESIS_FAILED" in actions
