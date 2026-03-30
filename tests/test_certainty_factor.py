# ============================================================
# tests/test_certainty_factor.py
# Unit Test — Kalkulator Certainty Factor
# Pola: Arrange-Act-Assert (AAA) per test method
# Target: Validasi formula CF, validasi input, edge cases
# ============================================================

import pytest
from engine.certainty_factor import CertaintyFactor, _validate_cf


# ============================================================
# TEST: Validasi Input CF
# ============================================================

class TestValidasiInputCF:
    """Test suite untuk validasi input CF (0.0 - 1.0)."""

    def test_cf_negatif_harus_ditolak(self):
        """CF < 0.0 harus raise ValueError."""
        # Arrange
        cf_negatif = -1.5

        # Act & Assert
        with pytest.raises(ValueError, match="harus dalam rentang"):
            _validate_cf(cf_negatif, "test_cf")

    def test_cf_diatas_satu_harus_ditolak(self):
        """CF > 1.0 harus raise ValueError."""
        # Arrange
        cf_besar = 1.5

        # Act & Assert
        with pytest.raises(ValueError, match="harus dalam rentang"):
            _validate_cf(cf_besar, "test_cf")

    def test_cf_string_harus_ditolak(self):
        """CF bertipe string harus raise TypeError."""
        # Arrange
        cf_string = "tinggi"

        # Act & Assert
        with pytest.raises(TypeError, match="harus bertipe numerik"):
            _validate_cf(cf_string, "test_cf")

    def test_cf_none_harus_ditolak(self):
        """CF bernilai None harus raise TypeError."""
        # Act & Assert
        with pytest.raises(TypeError):
            _validate_cf(None, "test_cf")

    def test_cf_nol_valid(self):
        """CF = 0.0 (batas bawah) harus diterima tanpa error."""
        # Arrange & Act & Assert (tidak ada exception)
        _validate_cf(0.0, "test_cf")

    def test_cf_satu_valid(self):
        """CF = 1.0 (batas atas) harus diterima tanpa error."""
        _validate_cf(1.0, "test_cf")

    def test_cf_integer_valid(self):
        """CF bertipe integer (misal: 1) harus diterima."""
        _validate_cf(1, "test_cf")


# ============================================================
# TEST: combine_cf() — Kombinasi Dua Nilai CF
# ============================================================

class TestCombineCF:
    """
    Test suite untuk CertaintyFactor.combine_cf().
    Formula: CF_combine(CF1, CF2) = CF1 + CF2 × (1 - CF1)
    """

    def test_kombinasi_standar_0_8_dan_0_6(self):
        """CF_combine(0.8, 0.6) = 0.8 + 0.6 × 0.2 = 0.92."""
        # Arrange
        cf1, cf2 = 0.8, 0.6

        # Act
        result = CertaintyFactor.combine_cf(cf1, cf2)

        # Assert
        assert result == pytest.approx(0.92, abs=1e-4)

    def test_kombinasi_dengan_1_0_menghasilkan_1_0(self):
        """CF_combine(X, 1.0) = X + 1.0×(1-X) = 1.0 untuk semua X."""
        # Arrange
        cf1 = 0.5

        # Act
        result = CertaintyFactor.combine_cf(cf1, 1.0)

        # Assert
        assert result == pytest.approx(1.0, abs=1e-4)

    def test_kombinasi_dengan_0_0_menghasilkan_cf1(self):
        """CF_combine(X, 0.0) = X + 0.0×(1-X) = X."""
        # Arrange
        cf1 = 0.7

        # Act
        result = CertaintyFactor.combine_cf(cf1, 0.0)

        # Assert
        assert result == pytest.approx(0.7, abs=1e-4)

    def test_kedua_nol_menghasilkan_nol(self):
        """CF_combine(0.0, 0.0) = 0.0."""
        # Arrange & Act
        result = CertaintyFactor.combine_cf(0.0, 0.0)

        # Assert
        assert result == pytest.approx(0.0, abs=1e-4)

    def test_kombinasi_0_4_dan_0_6(self):
        """CF_combine(0.4, 0.6) = 0.4 + 0.6×0.6 = 0.76."""
        # Arrange & Act
        result = CertaintyFactor.combine_cf(0.4, 0.6)

        # Assert
        assert result == pytest.approx(0.76, abs=1e-4)

    def test_input_out_of_range_lower_raise_error(self):
        """CF < -1.0 harus ditolak."""
        with pytest.raises(ValueError):
            CertaintyFactor.combine_cf(-1.5, 0.5)

    def test_input_diatas_satu_raise_error(self):
        """CF > 1.0 harus ditolak."""
        with pytest.raises(ValueError):
            CertaintyFactor.combine_cf(0.5, 1.5)


# ============================================================
# TEST: combine_cf_list() — Kombinasi List CF
# ============================================================

class TestCombineCFList:
    """Test suite untuk CertaintyFactor.combine_cf_list()."""

    def test_satu_elemen_mengembalikan_diri_sendiri(self):
        """List [0.8] → 0.8."""
        # Arrange
        cf_list = [0.8]

        # Act
        result = CertaintyFactor.combine_cf_list(cf_list)

        # Assert
        assert result == pytest.approx(0.8, abs=1e-4)

    def test_dua_elemen_sama_dengan_combine_cf(self):
        """List [0.8, 0.6] → sama dengan combine_cf(0.8, 0.6) = 0.92."""
        # Arrange
        cf_list = [0.8, 0.6]

        # Act
        result = CertaintyFactor.combine_cf_list(cf_list)

        # Assert
        assert result == pytest.approx(0.92, abs=1e-4)

    def test_tiga_elemen_iteratif(self):
        """
        List [0.8, 0.6, 1.0]:
        Step 1: combine(0.8, 0.6) = 0.92
        Step 2: combine(0.92, 1.0) = 1.0
        """
        # Arrange
        cf_list = [0.8, 0.6, 1.0]

        # Act
        result = CertaintyFactor.combine_cf_list(cf_list)

        # Assert
        assert result == pytest.approx(1.0, abs=1e-4)

    def test_list_kosong_mengembalikan_nol(self):
        """List [] → 0.0."""
        # Arrange & Act
        result = CertaintyFactor.combine_cf_list([])

        # Assert
        assert result == 0.0


# ============================================================
# TEST: calculate_cf_kombinasi() — CF Final (CF_pakar × CF_user)
# ============================================================

class TestCalculateCFKombinasi:
    """
    Test suite untuk CertaintyFactor.calculate_cf_kombinasi().
    Formula: CF_final = CF_pakar × CF_user_kombinasi
    """

    def test_simulasi_rule_r1_k01(self):
        """
        Simulasi R1 → K01 (Adaptor Rusak):
          CF_pakar = 0.90
          CF_users = [0.8, 0.6, 1.0]
          CF_user_combined = min(0.8, 0.6, 1.0) = 0.6
          CF_final = 0.90 × 0.6 = 0.54
        """
        # Arrange
        cf_pakar = 0.90
        cf_users = [0.8, 0.6, 1.0]

        # Act
        result = CertaintyFactor.calculate_cf_kombinasi(cf_pakar, cf_users)

        # Assert
        assert result == pytest.approx(0.54, abs=1e-4)

    def test_simulasi_rule_r4_k04(self):
        """
        Simulasi R4 → K04 (Overheating):
          CF_pakar = 0.88
          CF_users = [0.8, 0.6, 0.8]
          CF_user_combined = min(0.8, 0.6, 0.8) = 0.6
          CF_final = 0.88 × 0.6 = 0.528
        """
        # Arrange
        cf_pakar = 0.88
        cf_users = [0.8, 0.6, 0.8]

        # Act
        result = CertaintyFactor.calculate_cf_kombinasi(cf_pakar, cf_users)

        # Assert
        expected = 0.528
        assert result == pytest.approx(expected, abs=1e-2)

    def test_cf_user_tunggal(self):
        """CF tunggal: CF_final = cf_pakar × cf_user langsung."""
        # Arrange
        cf_pakar = 0.76
        cf_users = [0.8]

        # Act
        result = CertaintyFactor.calculate_cf_kombinasi(cf_pakar, cf_users)

        # Assert
        assert result == pytest.approx(0.608, abs=1e-4)

    def test_semua_cf_user_nol_menghasilkan_nol(self):
        """Jika user menjawab 0.0, cf_user_combined = 0.0 → final = 0.0."""
        # Arrange & Act
        result = CertaintyFactor.calculate_cf_kombinasi(0.90, [0.0])

        # Assert
        assert result == pytest.approx(0.0, abs=1e-4)

    def test_list_kosong_menghasilkan_nol(self):
        """Tidak ada jawaban user → 0.0."""
        # Arrange & Act
        result = CertaintyFactor.calculate_cf_kombinasi(0.90, [])

        # Assert
        assert result == 0.0

    def test_alias_calculate_final_sama(self):
        """calculate_final harus alias dari calculate_cf_kombinasi."""
        # Arrange
        cf_pakar = 0.80
        cf_users = [0.6, 0.8]

        # Act
        result_alias = CertaintyFactor.calculate_final(cf_pakar, cf_users)
        result_asli = CertaintyFactor.calculate_cf_kombinasi(cf_pakar, cf_users)

        # Assert
        assert result_alias == result_asli

    def test_validasi_cf_pakar_out_of_range(self):
        """CF pakar < -1.0 harus ditolak."""
        with pytest.raises(ValueError):
            CertaintyFactor.calculate_cf_kombinasi(-1.5, [0.8])

    def test_validasi_cf_user_out_of_range(self):
        """CF user < -1.0 di dalam list harus ditolak."""
        with pytest.raises(ValueError):
            CertaintyFactor.calculate_cf_kombinasi(0.80, [0.8, -1.2])


# ============================================================
# TEST: combine_multi_rules() — Multi-Rule (Simulasi Kombinasi > 1 Rule)
# ============================================================

class TestCombineMultiRules:
    """Test suite untuk multi-rule CF combine."""

    def test_dua_rules_simulasi(self):
        """
        Simulasi jika ada hipotesis dengan 2 rule terbukti:
          CF_R11 = 0.70 × 0.8 = 0.56
          CF_R12 = 0.68 × 0.6 = 0.408
          Combine = 0.56 + 0.408 × (1-0.56) = 0.56 + 0.17952 = 0.7395
        """
        # Arrange
        cf_r1 = 0.70 * 0.8    # 0.56
        cf_r2 = 0.68 * 0.6    # 0.408

        # Act
        result = CertaintyFactor.combine_multi_rules([cf_r1, cf_r2])

        # Assert
        expected = 0.56 + 0.408 * (1 - 0.56)
        assert result == pytest.approx(expected, abs=1e-3)

    def test_satu_rule_mengembalikan_langsung(self):
        """Satu rule → kembalikan CF-nya langsung."""
        # Arrange & Act
        result = CertaintyFactor.combine_multi_rules([0.75])

        # Assert
        assert result == pytest.approx(0.75, abs=1e-4)

    def test_list_kosong(self):
        """Kosong → 0.0."""
        assert CertaintyFactor.combine_multi_rules([]) == 0.0
