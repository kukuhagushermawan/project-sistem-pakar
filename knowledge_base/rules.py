# ============================================================
# knowledge_base/rules.py
# Rule Base Backward Chaining (R1-R12) — Representasi Prosedural
# Setiap rule: IF [premis gejala] THEN [konklusi kerusakan]
# ============================================================

RULES: list[dict] = [
    {
        "rule_id": "R1",
        "premis": ["G01", "G02", "G18"],
        "konklusi": "K01",
        "cf_rule": 0.90,
        "deskripsi_rule": (
            "IF laptop tidak menyala (G01) AND lampu charger mati (G02) "
            "AND adaptor longgar/rusak (G18) THEN adaptor/charger rusak (K01)"
        ),
    },
    {
        "rule_id": "R2",
        "premis": ["G03", "G04", "G05"],
        "konklusi": "K02",
        "cf_rule": 0.85,
        "deskripsi_rule": (
            "IF hanya menyala saat charger (G03) AND baterai tidak mengisi (G04) "
            "AND baterai cepat habis (G05) THEN baterai rusak/drop (K02)"
        ),
    },
    {
        "rule_id": "R3",
        "premis": ["G06", "G07"],
        "konklusi": "K03",
        "cf_rule": 0.80,
        "deskripsi_rule": (
            "IF bunyi beep saat startup (G06) AND layar blank dengan power menyala (G07) "
            "THEN RAM bermasalah (K03)"
        ),
    },
    {
        "rule_id": "R4",
        "premis": ["G08", "G09", "G10"],
        "konklusi": "K04",
        "cf_rule": 0.88,
        "deskripsi_rule": (
            "IF laptop cepat panas (G08) AND mati sendiri (G09) "
            "AND kipas bising/ventilasi panas (G10) THEN overheating (K04)"
        ),
    },
    {
        "rule_id": "R5",
        "premis": ["G07", "G16", "G17"],
        "konklusi": "K05",
        "cf_rule": 0.82,
        "deskripsi_rule": (
            "IF layar blank (G07) AND layar bergaris/berkedip (G16) "
            "AND monitor eksternal normal (G17) THEN LCD/display bermasalah (K05)"
        ),
    },
    {
        "rule_id": "R6",
        "premis": ["G11", "G12", "G13"],
        "konklusi": "K06",
        "cf_rule": 0.84,
        "deskripsi_rule": (
            "IF gagal boot (G11) AND laptop lambat/hang (G12) "
            "AND bisa BIOS tapi gagal OS (G13) THEN HDD/SSD bermasalah (K06)"
        ),
    },
    {
        "rule_id": "R7",
        "premis": ["G14", "G15"],
        "konklusi": "K07",
        "cf_rule": 0.78,
        "deskripsi_rule": (
            "IF beberapa tombol tidak berfungsi (G14) AND keyboard input ganda (G15) "
            "THEN keyboard rusak (K07)"
        ),
    },
    {
        "rule_id": "R8",
        "premis": ["G19", "G20", "G21"],
        "konklusi": "K08",
        "cf_rule": 0.75,
        "deskripsi_rule": (
            "IF LED berkedip tanpa start (G19) AND hidup sebentar lalu mati (G20) "
            "AND tidak ada tampilan/beep (G21) THEN motherboard bermasalah (K08)"
        ),
    },
    {
        "rule_id": "R9",
        "premis": ["G22"],
        "konklusi": "K09",
        "cf_rule": 0.76,
        "deskripsi_rule": (
            "IF touchpad tidak merespons/pointer meloncat (G22) "
            "THEN touchpad bermasalah (K09)"
        ),
    },
    {
        "rule_id": "R10",
        "premis": ["G23"],
        "konklusi": "K10",
        "cf_rule": 0.74,
        "deskripsi_rule": (
            "IF WiFi sering putus/tidak deteksi jaringan (G23) "
            "THEN modul WiFi bermasalah (K10)"
        ),
    },

    {
        "rule_id": "R11",
        "premis": ["G24"],
        "konklusi": "K08",
        "cf_rule": 0.70,
        "deskripsi_rule": (
            "IF suara speaker pecah/tidak keluar (G24) "
            "THEN motherboard bermasalah — jalur audio IC (K08)"
        ),
    },
    {
        "rule_id": "R12",
        "premis": ["G25"],
        "konklusi": "K08",
        "cf_rule": 0.68,
        "deskripsi_rule": (
            "IF port USB tidak deteksi perangkat (G25) "
            "THEN motherboard bermasalah — jalur USB controller (K08)"
        ),
    },
]


# ============================================================
# Pre-indexed lookup: Rule berdasarkan konklusi (kode_kerusakan)
# Digunakan oleh Backward Chaining engine untuk O(1) lookup
# ============================================================
RULES_BY_CONCLUSION: dict[str, list[dict]] = {}
for _rule in RULES:
    _key = _rule["konklusi"]
    if _key not in RULES_BY_CONCLUSION:
        RULES_BY_CONCLUSION[_key] = []
    RULES_BY_CONCLUSION[_key].append(_rule)
