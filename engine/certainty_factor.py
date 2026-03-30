# ============================================================
# engine/certainty_factor.py
# Kalkulator Certainty Factor — Formula Shortliffe & Buchanan
#
# Referensi formula:
#   CF_combine(CF1, CF2) = CF1 + CF2 × (1 - CF1)
#   CF_final = CF_pakar × CF_user_kombinasi
# ============================================================

import logging

logger = logging.getLogger("laptopdoc.engine.cf")


def _validate_cf(value: float, name: str = "CF") -> None:
    """
    Validasi bahwa nilai CF berada dalam rentang 0.0 - 1.0.

    Args:
        value: Nilai CF yang akan divalidasi.
        name: Nama parameter (untuk pesan error).

    Raises:
        TypeError: Jika value bukan int atau float.
        ValueError: Jika value di luar rentang [-1.0, 1.0].
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"{name} harus bertipe numerik (int/float), "
            f"diterima: {type(value).__name__}"
        )
    if not (-1.0 <= value <= 1.0):
        raise ValueError(
            f"{name} harus dalam rentang -1.0 hingga 1.0, "
            f"diterima: {value}"
        )


class CertaintyFactor:
    """
    Kalkulator Certainty Factor untuk Sistem Pakar LaptopDoc.

    Menyediakan method statis untuk:
    - combine_cf(): Kombinasi 2 nilai CF.
    - combine_cf_list(): Kombinasi list CF secara iteratif.
    - calculate_cf_kombinasi(): Hitung CF final (CF_pakar × CF_user_kombinasi).
    - combine_multi_rules(): Gabung CF dari multiple rules ke 1 kerusakan.

    Semua method melakukan validasi input dan logging otomatis.
    """

    @staticmethod
    def combine_cf(cf1: float, cf2: float) -> float:
        """
        Kombinasikan dua nilai CF menggunakan formula MYCIN:
        1. Jika kedua CF > 0: CF1 + CF2 * (1 - CF1)
        2. Jika salah satu CF < 0: (CF1 + CF2) / (1 - min(|CF1|, |CF2|))
        3. Jika kedua CF < 0: CF1 + CF2 * (1 + CF1)

        Args:
            cf1: Nilai CF pertama (-1.0 hingga 1.0).
            cf2: Nilai CF kedua (-1.0 hingga 1.0).

        Returns:
            float: Nilai CF kombinasi (-1.0 hingga 1.0).

        Raises:
            TypeError: Jika cf1 atau cf2 bukan numerik.
            ValueError: Jika cf1 atau cf2 di luar rentang [-1.0, 1.0].

        Example:
            >>> CertaintyFactor.combine_cf(0.8, 0.6)
            0.92
        """
        _validate_cf(cf1, "cf1")
        _validate_cf(cf2, "cf2")

        if cf1 >= 0 and cf2 >= 0:
            result = cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            result = cf1 + cf2 * (1 + cf1)
        else:
            denominator = 1 - min(abs(cf1), abs(cf2))
            if denominator == 0:
                result = 1.0 if (cf1 + cf2) > 0 else -1.0 # Edge case
            else:
                result = (cf1 + cf2) / denominator

        result = round(result, 4)

        logger.debug("combine_cf(%.2f, %.2f) = %.4f", cf1, cf2, result)
        return result

    @staticmethod
    def combine_cf_list(cf_list: list[float]) -> float:
        """
        Kombinasikan list CF secara iteratif menggunakan combine_cf.
        CF_combine(CF1, CF2, CF3) = CF_combine(CF_combine(CF1, CF2), CF3)

        Args:
            cf_list: List nilai CF (setiap elemen 0.0 - 1.0).
                     Minimal 1 elemen untuk hasil bermakna.

        Returns:
            float: Nilai CF kombinasi keseluruhan. 0.0 jika list kosong.

        Raises:
            TypeError: Jika elemen list bukan numerik.
            ValueError: Jika elemen list di luar rentang [0.0, 1.0].

        Example:
            >>> CertaintyFactor.combine_cf_list([0.8, 0.6, 1.0])
            1.0
        """
        if not cf_list:
            return 0.0

        # Validasi setiap elemen
        for i, cf in enumerate(cf_list):
            _validate_cf(cf, f"cf_list[{i}]")

        result = cf_list[0]
        for i in range(1, len(cf_list)):
            result = CertaintyFactor.combine_cf(result, cf_list[i])

        logger.info("combine_cf_list(%s) = %.4f", cf_list, result)
        return result

    @staticmethod
    def calculate_cf_kombinasi(cf_pakar: float, cf_user_list: list[float]) -> float:
        """
        Hitung CF final (kombinasi CF Pakar dan CF User).

        Formula:
            CF_final = CF_pakar × CF_user_kombinasi

        dimana CF_user_kombinasi dihitung dengan min() atas
        seluruh jawaban CF User yang terpenuhi (karena menggunakan AND).

        Args:
            cf_pakar: Nilai CF pakar/rule (0.0 - 1.0).
                      Contoh: 0.90 untuk Rule R1.
            cf_user_list: List nilai CF User per gejala yang terpenuhi.
                          Contoh: [0.8, 0.6, 1.0] untuk 3 gejala.

        Returns:
            float: CF final (0.0 - 1.0). 0.0 jika cf_user_list kosong.

        Raises:
            TypeError: Jika cf_pakar atau elemen list bukan numerik.
            ValueError: Jika cf_pakar atau elemen list di luar [0.0, 1.0].

        Example:
            >>> CertaintyFactor.calculate_cf_kombinasi(0.90, [0.8, 0.6, 1.0])
            0.54
        """
        _validate_cf(cf_pakar, "cf_pakar")

        if not cf_user_list:
            return 0.0

        for i, cf in enumerate(cf_user_list):
            _validate_cf(cf, f"cf_user_list[{i}]")

        cf_user_combined = min(cf_user_list)
        cf_final = round(cf_pakar * cf_user_combined, 4)

        logger.info(
            "calculate_cf_kombinasi(cf_pakar=%.2f, users=%s) → "
            "cf_user_combined=%.4f → cf_final=%.4f",
            cf_pakar, cf_user_list, cf_user_combined, cf_final,
        )
        return cf_final

    # Alias untuk backward compatibility
    calculate_final = calculate_cf_kombinasi

    @staticmethod
    def combine_multi_rules(cf_finals: list[float]) -> float:
        """
        Kombinasikan CF final dari multiple rules yang mengarah ke
        kerusakan yang sama (jika ada lebih dari 1 rule).

        Menggunakan formula combine_cf secara iteratif atas
        semua CF final per-rule.

        Args:
            cf_finals: List CF final per rule (setiap elemen 0.0 - 1.0).

        Returns:
            float: CF gabungan antar-rule. 0.0 jika list kosong.

        Example:
            >>> CertaintyFactor.combine_multi_rules([0.56, 0.408])
            0.7395
        """
        if not cf_finals:
            return 0.0

        result = CertaintyFactor.combine_cf_list(cf_finals)
        logger.info("combine_multi_rules(%s) = %.4f", cf_finals, result)
        return result
