# ============================================================
# config.py
# Konfigurasi umum LaptopDoc — konvensi & logging
# ============================================================

import logging
import sys

# ============================================================
# KONFIGURASI APLIKASI
# ============================================================

APP_NAME = "LaptopDoc"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistem Pakar Diagnosis Kerusakan Laptop"

# Nilai CF User yang valid
VALID_CF_VALUES = {0.0, 0.4, 0.6, 0.8, 1.0}

# Label untuk setiap CF value
CF_LABELS = {
    0.0: ("Tidak", "Gejala tidak dialami"),
    0.4: ("Kurang yakin", "Kadang terasa"),
    0.6: ("Cukup yakin", "Cukup sering"),
    0.8: ("Yakin", "Jelas tampak"),
    1.0: ("Sangat yakin", "Benar-benar terjadi"),
}


# ============================================================
# KONFIGURASI LOGGING
# ============================================================
#
# Strategi logging khusus untuk melacak Traceability /
# Explanation Facility saat Backward Chaining berjalan.
#
# Logger hierarchy:
#   laptopdoc                    → root logger aplikasi
#   laptopdoc.engine.bc          → Backward Chaining engine
#   laptopdoc.engine.cf          → Certainty Factor calculator
#   laptopdoc.engine.explanation → Explanation Facility
#   laptopdoc.ui                 → Streamlit UI layer
#
# Format log:
#   [2026-03-28 17:00:05] [INFO ] [engine.bc] Hipotesis K01 TERBUKTI (CF=0.90)
#   [2026-03-28 17:00:05] [DEBUG] [engine.cf] combine_cf(0.80, 0.60) = 0.9200
#

def setup_logging(level: str = "INFO") -> None:
    """
    Inisialisasi logging untuk seluruh aplikasi LaptopDoc.

    Args:
        level: Level logging (DEBUG/INFO/WARNING/ERROR).
               Gunakan DEBUG saat development untuk melihat
               setiap langkah inferensi dan kalkulasi CF.
    """
    log_format = (
        "[%(asctime)s] [%(levelname)-5s] [%(name)s] %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    # Root logger aplikasi
    root_logger = logging.getLogger("laptopdoc")
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter(log_format, datefmt=date_format)
    )

    # Hindari duplikasi handler jika dipanggil berulang
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

    root_logger.info(
        "%s v%s — Logging initialized (level=%s)",
        APP_NAME, APP_VERSION, level,
    )
