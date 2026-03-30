# ============================================================
# knowledge_base/symptoms.py
# Data Gejala (G01-G25) — Premis untuk Rule Backward Chaining
# ============================================================

SYMPTOMS: dict[str, dict] = {
    "G01": {
        "kode_gejala": "G01",
        "teks_gejala": "Laptop tidak menyala saat tombol power ditekan",
        "deskripsi_detail": (
            "Saat tombol power ditekan, tidak ada respons apapun "
            "(tidak ada lampu, suara, atau tampilan)."
        ),
        "kategori": "daya",
    },
    "G02": {
        "kode_gejala": "G02",
        "teks_gejala": "Lampu indikator charger tidak menyala",
        "deskripsi_detail": (
            "Saat adaptor/charger dipasang ke laptop, lampu LED "
            "pada adaptor atau laptop tidak menyala."
        ),
        "kategori": "daya",
    },
    "G03": {
        "kode_gejala": "G03",
        "teks_gejala": "Laptop hanya menyala saat charger terpasang",
        "deskripsi_detail": (
            "Laptop berfungsi normal saat charger terhubung, "
            "tetapi langsung mati jika charger dicabut."
        ),
        "kategori": "daya",
    },
    "G04": {
        "kode_gejala": "G04",
        "teks_gejala": "Baterai tidak mengisi (charging) meskipun charger terpasang",
        "deskripsi_detail": (
            "Ikon baterai tidak menunjukkan status charging, "
            "atau persentase baterai tidak bertambah meskipun charger terhubung."
        ),
        "kategori": "daya",
    },
    "G05": {
        "kode_gejala": "G05",
        "teks_gejala": "Baterai cepat habis meskipun baru diisi penuh",
        "deskripsi_detail": (
            "Baterai terisi penuh (100%) tetapi hanya bertahan "
            "kurang dari 1 jam dalam penggunaan normal."
        ),
        "kategori": "daya",
    },
    "G06": {
        "kode_gejala": "G06",
        "teks_gejala": "Terdengar bunyi beep berulang saat startup",
        "deskripsi_detail": (
            "Laptop mengeluarkan bunyi beep berulang (bisa pendek atau panjang) "
            "saat dinyalakan, sebelum tampilan muncul di layar."
        ),
        "kategori": "daya",
    },
    "G07": {
        "kode_gejala": "G07",
        "teks_gejala": "Layar blank/hitam tetapi lampu power menyala",
        "deskripsi_detail": (
            "Lampu indikator power menyala, kipas mungkin berputar, "
            "tetapi layar tetap hitam tanpa tampilan apapun."
        ),
        "kategori": "visual",
    },
    "G08": {
        "kode_gejala": "G08",
        "teks_gejala": "Laptop terasa sangat panas saat digunakan",
        "deskripsi_detail": (
            "Bagian bawah atau area sekitar keyboard terasa sangat panas, "
            "terutama setelah penggunaan 10-30 menit."
        ),
        "kategori": "performa",
    },
    "G09": {
        "kode_gejala": "G09",
        "teks_gejala": "Laptop mati sendiri setelah beberapa menit penggunaan",
        "deskripsi_detail": (
            "Laptop tiba-tiba mati tanpa peringatan (bukan shutdown biasa) "
            "setelah digunakan beberapa menit."
        ),
        "kategori": "performa",
    },
    "G10": {
        "kode_gejala": "G10",
        "teks_gejala": "Kipas laptop sangat bising atau ventilasi terasa sangat panas",
        "deskripsi_detail": (
            "Suara kipas terdengar sangat keras, atau udara yang keluar "
            "dari ventilasi terasa panas tidak normal."
        ),
        "kategori": "performa",
    },
    "G11": {
        "kode_gejala": "G11",
        "teks_gejala": "Muncul pesan 'No bootable device' atau gagal boot",
        "deskripsi_detail": (
            "Saat startup, muncul pesan error seperti 'No bootable device found', "
            "'Boot device not found', atau 'Operating System not found'."
        ),
        "kategori": "performa",
    },
    "G12": {
        "kode_gejala": "G12",
        "teks_gejala": "Laptop sangat lambat dan sering hang/freeze",
        "deskripsi_detail": (
            "Laptop terasa sangat lambat dalam membuka aplikasi, "
            "sering not responding, atau freeze total."
        ),
        "kategori": "performa",
    },
    "G13": {
        "kode_gejala": "G13",
        "teks_gejala": "Bisa masuk BIOS tetapi gagal masuk sistem operasi",
        "deskripsi_detail": (
            "Tekan F2/Del bisa masuk BIOS setup, tetapi saat boot normal "
            "gagal masuk ke Windows/Linux (stuck atau error)."
        ),
        "kategori": "performa",
    },
    "G14": {
        "kode_gejala": "G14",
        "teks_gejala": "Beberapa tombol keyboard tidak berfungsi",
        "deskripsi_detail": (
            "Satu atau beberapa tombol tidak merespons saat ditekan, "
            "sementara tombol lain masih berfungsi normal."
        ),
        "kategori": "input",
    },
    "G15": {
        "kode_gejala": "G15",
        "teks_gejala": "Keyboard mengetik sendiri atau menghasilkan input ganda",
        "deskripsi_detail": (
            "Muncul karakter tanpa ditekan (ghost typing), "
            "atau satu kali tekan menghasilkan 2-3 karakter yang sama."
        ),
        "kategori": "input",
    },
    "G16": {
        "kode_gejala": "G16",
        "teks_gejala": "Layar bergaris, berkedip-kedip, atau ada artefak visual",
        "deskripsi_detail": (
            "Tampilan layar menunjukkan garis horizontal/vertikal, "
            "berkedip (flicker), atau muncul titik/kotak warna acak."
        ),
        "kategori": "visual",
    },
    "G17": {
        "kode_gejala": "G17",
        "teks_gejala": "Tampilan pada monitor eksternal normal (saat dihubungkan HDMI/VGA)",
        "deskripsi_detail": (
            "Saat laptop dihubungkan ke monitor/TV eksternal, "
            "tampilan di monitor tersebut normal tanpa masalah."
        ),
        "kategori": "visual",
    },
    "G18": {
        "kode_gejala": "G18",
        "teks_gejala": "Adaptor atau kabel charger longgar, terkelupas, atau tidak stabil",
        "deskripsi_detail": (
            "Kabel adaptor terlihat rusak fisik (terkelupas, tertekuk), "
            "atau colokan charger tidak terpasang dengan kuat di port laptop."
        ),
        "kategori": "daya",
    },
    "G19": {
        "kode_gejala": "G19",
        "teks_gejala": "LED power berkedip tetapi laptop tidak start normal",
        "deskripsi_detail": (
            "Lampu LED power menyala atau berkedip saat tombol power ditekan, "
            "tetapi laptop tidak melanjutkan proses booting."
        ),
        "kategori": "daya",
    },
    "G20": {
        "kode_gejala": "G20",
        "teks_gejala": "Laptop hidup sebentar (1-3 detik) lalu mati lagi",
        "deskripsi_detail": (
            "Saat dinyalakan, kipas dan lampu menyala sebentar "
            "(1-3 detik) kemudian mati total secara berulang."
        ),
        "kategori": "daya",
    },
    "G21": {
        "kode_gejala": "G21",
        "teks_gejala": "Tidak ada tampilan di layar dan tidak ada bunyi beep",
        "deskripsi_detail": (
            "Laptop benar-benar 'mati': tidak ada tampilan, "
            "tidak ada bunyi beep, meskipun ada sedikit tanda listrik masuk."
        ),
        "kategori": "daya",
    },
    "G22": {
        "kode_gejala": "G22",
        "teks_gejala": "Touchpad tidak merespons atau pointer meloncat-loncat",
        "deskripsi_detail": (
            "Touchpad sama sekali tidak merespons sentuhan, "
            "atau kursor bergerak sendiri / meloncat secara acak."
        ),
        "kategori": "input",
    },
    "G23": {
        "kode_gejala": "G23",
        "teks_gejala": "WiFi sering putus atau tidak mendeteksi jaringan apapun",
        "deskripsi_detail": (
            "Koneksi WiFi sering disconnect tanpa alasan, "
            "atau laptop tidak mendeteksi jaringan WiFi yang tersedia."
        ),
        "kategori": "konektivitas",
    },

    "G24": {
        "kode_gejala": "G24",
        "teks_gejala": "Suara speaker pecah, terdistorsi, atau tidak keluar suara sama sekali",
        "deskripsi_detail": (
            "Speaker laptop mengeluarkan suara pecah/kresek, "
            "atau tidak ada suara meskipun volume sudah dinaikkan."
        ),
        "kategori": "audio",
    },
    "G25": {
        "kode_gejala": "G25",
        "teks_gejala": "Port USB tidak mendeteksi perangkat yang dihubungkan",
        "deskripsi_detail": (
            "Flashdisk, mouse, atau perangkat USB lain tidak terdeteksi "
            "saat dihubungkan ke port USB laptop."
        ),
        "kategori": "periferal",
    },
}
