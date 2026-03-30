# ============================================================
# knowledge_base/frames.py
# Frame Kerusakan Laptop (K01-K10) — Representasi Deklaratif
# Setiap Frame menyimpan slot: kode, nama, penyebab, solusi, cf_pakar
# ============================================================

FRAMES: dict[str, dict] = {
    "K01": {
        "kode_kerusakan": "K01",
        "nama_kerusakan": "Adaptor/Charger Rusak",
        "penyebab": "Suplai daya adaptor tidak stabil atau kabel rusak",
        "solusi_singkat": "Periksa output adaptor, coba charger lain",
        "solusi_detail": (
            "1. Periksa lampu indikator adaptor.\n"
            "2. Coba gunakan adaptor/charger lain yang kompatibel.\n"
            "3. Periksa kabel apakah ada kerusakan fisik (terkelupas, patah).\n"
            "4. Ukur output tegangan adaptor dengan multimeter jika memungkinkan."
        ),
        "cf_pakar": 0.90,
        "kategori": "daya",
    },
    "K02": {
        "kode_kerusakan": "K02",
        "nama_kerusakan": "Baterai Rusak/Drop",
        "penyebab": "Sel baterai melemah atau charging circuit error",
        "solusi_singkat": "Kalibrasi baterai, cek battery health",
        "solusi_detail": (
            "1. Cek battery health melalui software diagnostik bawaan.\n"
            "2. Lakukan kalibrasi: charge 100% → discharge hingga mati → charge lagi.\n"
            "3. Jika health < 40%, pertimbangkan ganti baterai.\n"
            "4. Pastikan charger yang digunakan kompatibel dan berfungsi."
        ),
        "cf_pakar": 0.85,
        "kategori": "daya",
    },
    "K03": {
        "kode_kerusakan": "K03",
        "nama_kerusakan": "RAM Bermasalah",
        "penyebab": "RAM longgar, pin kotor, atau modul rusak",
        "solusi_singkat": "Lepas-pasang RAM, bersihkan pin kontak",
        "solusi_detail": (
            "1. Matikan laptop dan lepas baterai (jika removable).\n"
            "2. Buka slot RAM, lepas modul RAM.\n"
            "3. Bersihkan pin kontak dengan penghapus pensil putih.\n"
            "4. Pasang kembali RAM hingga terdengar 'klik'.\n"
            "5. Jika masih bermasalah, coba tukar slot atau ganti RAM."
        ),
        "cf_pakar": 0.80,
        "kategori": "komponen",
    },
    "K04": {
        "kode_kerusakan": "K04",
        "nama_kerusakan": "Overheating Sistem Pendingin",
        "penyebab": "Kipas kotor, heatsink tersumbat, atau thermal paste mengering",
        "solusi_singkat": "Bersihkan kipas, ganti thermal paste",
        "solusi_detail": (
            "1. Bersihkan ventilasi dan kipas dari debu menggunakan compressed air.\n"
            "2. Ganti thermal paste pada prosesor dan GPU.\n"
            "3. Gunakan cooling pad sebagai solusi sementara.\n"
            "4. Pastikan ventilasi tidak tertutup saat penggunaan."
        ),
        "cf_pakar": 0.88,
        "kategori": "komponen",
    },
    "K05": {
        "kode_kerusakan": "K05",
        "nama_kerusakan": "LCD/Fleksibel Display Bermasalah",
        "penyebab": "Panel LCD rusak atau kabel fleksibel display putus/longgar",
        "solusi_singkat": "Tes monitor eksternal, cek kabel fleksibel",
        "solusi_detail": (
            "1. Hubungkan laptop ke monitor eksternal (HDMI/VGA).\n"
            "2. Jika tampilan eksternal normal → masalah di LCD/kabel fleksibel.\n"
            "3. Periksa kabel fleksibel display (buka engsel dengan hati-hati).\n"
            "4. Bawa ke teknisi untuk penggantian panel LCD jika diperlukan."
        ),
        "cf_pakar": 0.82,
        "kategori": "komponen",
    },
    "K06": {
        "kode_kerusakan": "K06",
        "nama_kerusakan": "HDD/SSD atau Boot System Bermasalah",
        "penyebab": "Storage rusak, bad sector, atau boot record corrupt",
        "solusi_singkat": "Cek storage di BIOS, uji disk, repair OS",
        "solusi_detail": (
            "1. Masuk BIOS → cek apakah HDD/SSD terdeteksi.\n"
            "2. Jalankan CHKDSK (Windows) atau fsck (Linux) untuk cek bad sector.\n"
            "3. Coba repair boot menggunakan USB instalasi OS.\n"
            "4. Jika storage tidak terdeteksi di BIOS → kemungkinan rusak fisik."
        ),
        "cf_pakar": 0.84,
        "kategori": "storage",
    },
    "K07": {
        "kode_kerusakan": "K07",
        "nama_kerusakan": "Keyboard Rusak",
        "penyebab": "Matriks keyboard rusak atau kabel fleksibel keyboard putus",
        "solusi_singkat": "Bersihkan keyboard, uji dengan keyboard eksternal",
        "solusi_detail": (
            "1. Bersihkan keyboard dari debu dan kotoran.\n"
            "2. Coba hubungkan keyboard USB eksternal untuk verifikasi.\n"
            "3. Jika keyboard eksternal normal → masalah di keyboard internal.\n"
            "4. Periksa kabel fleksibel keyboard atau ganti keyboard internal."
        ),
        "cf_pakar": 0.78,
        "kategori": "periferal",
    },
    "K08": {
        "kode_kerusakan": "K08",
        "nama_kerusakan": "Motherboard/Power IC Bermasalah",
        "penyebab": "Komponen board-level rusak (power IC, audio IC, USB controller)",
        "solusi_singkat": "Periksa board level, servis ke teknisi berpengalaman",
        "solusi_detail": (
            "1. Ini adalah kerusakan level board yang memerlukan skill teknis tinggi.\n"
            "2. Bawa ke teknisi yang menguasai reparasi board-level.\n"
            "3. Jangan mencoba memperbaiki sendiri tanpa peralatan yang sesuai.\n"
            "4. Pertimbangkan cost vs benefit perbaikan dibanding ganti unit."
        ),
        "cf_pakar": 0.75,
        "kategori": "komponen",
    },
    "K09": {
        "kode_kerusakan": "K09",
        "nama_kerusakan": "Touchpad Bermasalah",
        "penyebab": "Driver corrupt, kabel fleksibel longgar, atau modul touchpad rusak",
        "solusi_singkat": "Aktifkan di BIOS, instal ulang driver touchpad",
        "solusi_detail": (
            "1. Pastikan touchpad tidak dinonaktifkan (cek Fn+key disable touchpad).\n"
            "2. Cek di BIOS apakah touchpad diaktifkan.\n"
            "3. Instal ulang driver touchpad dari situs resmi vendor.\n"
            "4. Jika tetap bermasalah → kemungkinan kerusakan hardware touchpad."
        ),
        "cf_pakar": 0.76,
        "kategori": "periferal",
    },
    "K10": {
        "kode_kerusakan": "K10",
        "nama_kerusakan": "Modul WiFi Bermasalah",
        "penyebab": "Driver corrupt, modul WiFi longgar, atau antena putus",
        "solusi_singkat": "Instal ulang driver, reset network settings",
        "solusi_detail": (
            "1. Reset network settings: Settings → Network & Internet → Network Reset.\n"
            "2. Instal ulang driver WiFi dari situs resmi vendor.\n"
            "3. Cek Device Manager apakah modul WiFi terdeteksi.\n"
            "4. Jika tidak terdeteksi → kemungkinan modul WiFi fisik longgar/rusak."
        ),
        "cf_pakar": 0.74,
        "kategori": "konektivitas",
    },
}
