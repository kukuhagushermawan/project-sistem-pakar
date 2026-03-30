# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Sistem Pakar Diagnosis Kerusakan Laptop
### Pendekatan Hybrid: Rule-Frame & Backward Chaining dengan Certainty Factor

**Standar Acuan:** IEEE 830-1998 (IEEE Recommended Practice for Software Requirements Specifications)

| Item | Detail |
|---|---|
| **Versi** | 1.0 |
| **Tanggal** | 27 Maret 2026 |
| **Status** | Draft |
| **Disusun oleh** | [Nama Mahasiswa / Tim] |

---

## 1.0 Pendahuluan

### 1.1 Tujuan Dokumen

Dokumen Software Requirements Specification (SRS) ini bertujuan untuk mendefinisikan secara lengkap dan terstruktur seluruh kebutuhan fungsional serta non-fungsional dari **Sistem Pakar Diagnosis Kerusakan Laptop (LaptopDoc)**. Dokumen ini menjadi acuan utama bagi tim pengembang dalam melakukan perancangan, implementasi, dan pengujian sistem.

Dokumen ini ditujukan untuk:
- **Tim pengembang** — sebagai panduan teknis implementasi.
- **Dosen pengampu** — sebagai bahan evaluasi akademik.
- **Penguji** — sebagai dasar skenario pengujian.

### 1.2 Ruang Lingkup Produk

**LaptopDoc** adalah prototype sistem pakar berbasis web yang mampu mendiagnosis kerusakan laptop melalui konsultasi interaktif. Sistem meliputi:

- **10 jenis kerusakan** laptop (K01-K10) yang terstruktur dalam Frame.
- **25 gejala** (G01-G25) yang ditanyakan secara step-by-step.
- **12 rule** inferensi (R1-R12) dengan pendekatan Backward Chaining.
- **Certainty Factor (CF)** untuk menghitung tingkat keyakinan diagnosis.
- **Explanation Facility** berupa fasilitas "Mengapa" dan "Bagaimana".
- **Visualisasi pohon inferensi** menggunakan Graphviz.

Sistem berjalan pada platform web (Streamlit/Python) dan diakses melalui browser.

### 1.3 Definisi, Akronim, dan Singkatan

| Istilah | Definisi |
|---|---|
| **Sistem Pakar** | Program komputer yang meniru pengetahuan dan kemampuan penalaran seorang pakar dalam domain tertentu |
| **Frame** | Struktur representasi pengetahuan berbasis slot (atribut) untuk menyimpan data entitas secara terorganisir |
| **Rule** | Representasi pengetahuan dalam format IF-THEN untuk logika pengambilan keputusan |
| **Hybrid Rule-Frame** | Pendekatan kombinasi yang menggunakan Frame untuk data faktual dan Rule untuk logika inferensi |
| **Backward Chaining** | Metode inferensi yang dimulai dari hipotesis/goal, kemudian mencari fakta/gejala pendukung (goal-driven) |
| **Forward Chaining** | Metode inferensi yang dimulai dari fakta, kemudian menarik kesimpulan (data-driven) — tidak digunakan |
| **Certainty Factor (CF)** | Metode untuk mengukur tingkat keyakinan pakar dan pengguna terhadap suatu proposisi, bernilai 0.0–1.0 |
| **CF Pakar** | Nilai keyakinan pakar terhadap suatu rule/kerusakan |
| **CF User** | Nilai keyakinan pengguna terhadap suatu gejala yang dialami |
| **Explanation Facility** | Komponen sistem pakar yang menjelaskan proses penalaran (Mengapa/Bagaimana) |
| **Inference Engine** | Mesin penalaran yang mengevaluasi rule terhadap fakta untuk menghasilkan kesimpulan |
| **Knowledge Base** | Basis pengetahuan yang menyimpan Frame (data kerusakan) dan Rule (logika inferensi) |
| **Streamlit** | Framework Python open-source untuk membangun aplikasi web data secara cepat |
| **Graphviz** | Library visualisasi graph/tree untuk menampilkan pohon inferensi |
| **IEEE 830** | Standar IEEE untuk penulisan dokumen SRS |
| **BSOD** | Blue Screen of Death — layar error fatal pada sistem operasi Windows |
| **BIOS** | Basic Input/Output System — firmware dasar pada komputer |

### 1.4 Referensi

1. IEEE Std 830-1998, *IEEE Recommended Practice for Software Requirements Specifications*.
2. Turban, E., Aronson, J. E., & Liang, T. P. (2005). *Decision Support Systems and Intelligent Systems*. Pearson.
3. Giarratano, J. C., & Riley, G. D. (2005). *Expert Systems: Principles and Programming*. Thomson Course Technology.
4. Shortliffe, E. H., & Buchanan, B. G. (1975). *A Model of Inexact Reasoning in Medicine*. Mathematical Biosciences, 23, 351-379.
5. Dokumentasi Streamlit — https://docs.streamlit.io/
6. Dokumentasi Graphviz — https://graphviz.readthedocs.io/

---

## 2.0 Deskripsi Keseluruhan

### 2.1 Perspektif Produk

LaptopDoc merupakan sistem **standalone** yang berdiri sendiri tanpa integrasi ke sistem eksternal. Sistem beroperasi sebagai aplikasi web lokal menggunakan framework Streamlit (Python).

```
┌─────────────────────────────────────────────────────────┐
│                    WEB BROWSER                          │
│              (Chrome / Firefox / Edge)                  │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP (localhost:8501)
┌──────────────────────▼──────────────────────────────────┐
│              STREAMLIT APPLICATION                       │
│                                                         │
│  ┌─── UI Layer ──────────────────────────────────────┐  │
│  │ • Halaman Beranda                                 │  │
│  │ • Wizard Konsultasi (step-by-step)                │  │
│  │ • Halaman Hasil + Visualisasi                     │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌─── Engine Layer ──────────────────────────────────┐  │
│  │ • Backward Chaining Engine                        │  │
│  │ • Certainty Factor Calculator                     │  │
│  │ • Explanation Facility (Why / How)                │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌─── Knowledge Base Layer ──────────────────────────┐  │
│  │ • Frame (K01-K10)  • Rule (R1-R12)                │  │
│  │ • Gejala (G01-G25)                                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Fungsi Produk (Ringkasan)

| ID | Fungsi | Deskripsi Singkat |
|---|---|---|
| FP-01 | Konsultasi Diagnosis | Wizard step-by-step berbasis Backward Chaining |
| FP-02 | Perhitungan CF | Menghitung CF kombinasi dan CF final |
| FP-03 | Explanation: Mengapa | Menjelaskan alasan pertanyaan gejala |
| FP-04 | Explanation: Bagaimana | Menjelaskan proses perhitungan diagnosis |
| FP-05 | Visualisasi Pohon Inferensi | Graph visual proses backward chaining |
| FP-06 | Halaman Beranda | Informasi sistem dan panduan penggunaan |
| FP-07 | Riwayat Session | Menyimpan hasil konsultasi selama session aktif |

### 2.3 Karakteristik Pengguna

| Karakteristik | Detail |
|---|---|
| **Pengguna Primer** | Pengguna awam laptop yang mengalami masalah teknis |
| **Pengguna Sekunder** | Teknisi pemula yang membutuhkan panduan diagnosis |
| **Tingkat Keahlian** | Tidak memerlukan pengetahuan teknis komputer |
| **Frekuensi Penggunaan** | Ad-hoc (saat mengalami masalah laptop) |
| **Pelatihan** | Tidak diperlukan — antarmuka self-explanatory |

### 2.4 Batasan & Asumsi

**Batasan:**
1. Sistem hanya mendiagnosis 10 jenis kerusakan yang telah didefinisikan.
2. Diagnosis terbatas pada gejala yang bisa diamati pengguna (tanpa alat ukur).
3. Sistem tidak terhubung ke database eksternal; data di-hardcode.
4. Không mendukung multi-user concurrent (single session).
5. Bahasa antarmuka: Bahasa Indonesia saja.

**Asumsi:**
1. Pengguna menjawab pertanyaan gejala dengan jujur sesuai kondisi laptop.
2. Basis pengetahuan dianggap valid untuk kebutuhan prototype akademik.
3. Lingkungan operasi memiliki Python 3.8+ dan Graphviz terinstal.

---

## 3.0 Kebutuhan Fungsional

### FR-001: Memulai Sesi Konsultasi

| Atribut | Detail |
|---|---|
| **ID** | FR-001 |
| **Deskripsi** | Sistem menyediakan tombol "Mulai Konsultasi" di halaman beranda untuk memulai sesi diagnosis baru. Saat diklik, sistem menginisialisasi Backward Chaining engine dan memulai dari hipotesis pertama (K01). |
| **Input** | Klik tombol "Mulai Konsultasi" |
| **Output** | Halaman wizard konsultasi ditampilkan dengan pertanyaan gejala pertama |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — Fungsional Utama |

---

### FR-002: Menampilkan Pertanyaan Gejala (Step-by-Step)

| Atribut | Detail |
|---|---|
| **ID** | FR-002 |
| **Deskripsi** | Sistem menampilkan pertanyaan gejala satu per satu (wizard step-by-step). Setiap pertanyaan menampilkan: teks gejala, kode gejala, dan opsi jawaban berupa skala CF User. Pertanyaan ditentukan oleh rule yang sedang dievaluasi oleh Backward Chaining engine. |
| **Input** | State engine: hipotesis aktif, rule aktif, gejala aktif |
| **Output** | Satu pertanyaan gejala dengan 5 opsi radio button |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — UI/UX, butir (3a) |

---

### FR-003: Menerima Jawaban dengan Skala CF User

| Atribut | Detail |
|---|---|
| **ID** | FR-003 |
| **Deskripsi** | Sistem menerima jawaban pengguna untuk setiap gejala dalam bentuk **skala Certainty Factor User** dengan 5 opsi: (0.0) Tidak — gejala tidak dialami; (0.4) Kurang yakin — kadang terasa; (0.6) Cukup yakin — cukup sering; (0.8) Yakin — jelas tampak; (1.0) Sangat yakin — benar-benar terjadi. |
| **Input** | Pilihan radio button (0.0 / 0.4 / 0.6 / 0.8 / 1.0) |
| **Output** | Nilai CF User disimpan, engine melanjutkan evaluasi |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — butir (4) |

---

### FR-004: Evaluasi Backward Chaining per Hipotesis

| Atribut | Detail |
|---|---|
| **ID** | FR-004 |
| **Deskripsi** | Sistem mengevaluasi hipotesis kerusakan secara iteratif (K01 → K10) menggunakan Backward Chaining. Untuk setiap hipotesis, sistem mencari rule yang konklusinya = hipotesis tersebut, lalu mengevaluasi premis/gejala satu per satu. **Jika CF User = 0.0 pada salah satu premis, hipotesis dinyatakan GAGAL dan engine lanjut ke hipotesis berikutnya.** Jika semua premis terpenuhi (CF > 0), sistem menghitung CF kombinasi. |
| **Input** | Jawaban CF User per gejala |
| **Output** | Status hipotesis: TERBUKTI (dengan CF final) atau GAGAL |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — Fungsional Utama, butir (1) |

---

### FR-005: Menghitung Certainty Factor Kombinasi

| Atribut | Detail |
|---|---|
| **ID** | FR-005 |
| **Deskripsi** | Sistem menghitung CF kombinasi menggunakan formula: `CF_combine(CF1, CF2) = CF1 + CF2 × (1 - CF1)` secara iteratif untuk >2 gejala. CF final per hipotesis dihitung dengan: `CF_final = CF_pakar × CF_user_kombinasi`. Untuk kerusakan dengan multiple rules (K08 memiliki R8, R11, R12), CF antar-rule juga dikombinasikan. |
| **Input** | List CF User per gejala yang terpenuhi, CF Pakar dari rule |
| **Output** | CF final per kerusakan (0.0 – 1.0) |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — Struktur Basis Pengetahuan |

---

### FR-006: Menampilkan Explanation Facility — "Mengapa" (Why)

| Atribut | Detail |
|---|---|
| **ID** | FR-006 |
| **Deskripsi** | Pada setiap pertanyaan gejala, sistem menyediakan tombol **"Mengapa?"**. Saat diklik, sistem menampilkan penjelasan: *"Saya menanyakan gejala [Kode — Teks Gejala] untuk mengevaluasi hipotesis kerusakan [Kode — Nama Kerusakan]. Gejala ini merupakan premis dari rule [Rx] dengan CF Pakar = [nilai]."* |
| **Input** | Klik tombol "Mengapa?" |
| **Output** | Teks penjelasan ditampilkan dalam expander/panel |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — Explanation Facility, butir (2) |

---

### FR-007: Menampilkan Explanation Facility — "Bagaimana" (How)

| Atribut | Detail |
|---|---|
| **ID** | FR-007 |
| **Deskripsi** | Di halaman hasil diagnosis, sistem menampilkan detail **"Bagaimana"** untuk setiap kerusakan yang terbukti, meliputi: (a) Rule yang triggered beserta ID-nya; (b) Gejala yang terpenuhi beserta CF User masing-masing; (c) Langkah-langkah perhitungan CF kombinasi secara eksplisit; (d) Hasil CF final. |
| **Input** | Hasil diagnosis dari engine |
| **Output** | Panel/expander detail perhitungan per kerusakan |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — Explanation Facility, butir (2) |

---

### FR-008: Menampilkan Ranking Hasil Diagnosis

| Atribut | Detail |
|---|---|
| **ID** | FR-008 |
| **Deskripsi** | Setelah seluruh hipotesis (K01-K10) dievaluasi, sistem menampilkan **ranking diagnosis** yang diurutkan berdasarkan CF final tertinggi. Setiap item menampilkan: kode kerusakan, nama kerusakan, CF final (persentase), penyebab, dan solusi yang diambil dari Frame. Hanya kerusakan yang terbukti (CF > 0) yang ditampilkan. |
| **Input** | Hasil evaluasi seluruh hipotesis |
| **Output** | Daftar/card kerusakan terurut berdasarkan CF final |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — Fungsional Utama |

---

### FR-009: Menampilkan Visualisasi Pohon Inferensi

| Atribut | Detail |
|---|---|
| **ID** | FR-009 |
| **Deskripsi** | Sistem menampilkan **visualisasi pohon inferensi** di halaman hasil menggunakan Graphviz. Node terdiri dari: hipotesis (kerusakan) dengan warna hijau (terbukti), merah (gagal), atau abu-abu (tidak dievaluasi); dan gejala dengan label CF User. Edge menunjukkan hubungan rule dengan label rule ID dan CF Pakar. |
| **Input** | Hasil evaluasi seluruh hipotesis dan rule |
| **Output** | Graphviz Digraph yang di-render di halaman hasil |
| **Prioritas** | Tinggi |
| **Sumber** | Elicitasi kebutuhan — Non-Fungsional, butir (8) |

---

### FR-010: Menampilkan Halaman Beranda

| Atribut | Detail |
|---|---|
| **ID** | FR-010 |
| **Deskripsi** | Sistem menyediakan halaman beranda yang menampilkan: judul dan deskripsi singkat sistem, fitur utama, panduan cara penggunaan, dan tombol "Mulai Konsultasi" untuk memulai sesi. |
| **Input** | Akses URL aplikasi |
| **Output** | Halaman beranda informatif |
| **Prioritas** | Sedang |
| **Sumber** | Umum |

---

### FR-011: Menyimpan Riwayat Konsultasi (Session)

| Atribut | Detail |
|---|---|
| **ID** | FR-011 |
| **Deskripsi** | Sistem menyimpan riwayat hasil konsultasi selama session browser masih aktif. Pengguna dapat melihat kembali hasil diagnosis sebelumnya tanpa harus melakukan konsultasi ulang. Riwayat hilang jika browser ditutup. |
| **Input** | Hasil konsultasi yang telah diselesaikan |
| **Output** | Daftar riwayat konsultasi yang dapat di-klik |
| **Prioritas** | Rendah |
| **Sumber** | Best practice UX |

---

### FR-012: Konsultasi Ulang

| Atribut | Detail |
|---|---|
| **ID** | FR-012 |
| **Deskripsi** | Sistem menyediakan tombol "Konsultasi Ulang" di halaman hasil untuk memulai sesi konsultasi baru. Klik tombol ini mereset state engine dan mengarahkan kembali ke halaman wizard konsultasi. |
| **Input** | Klik tombol "Konsultasi Ulang" |
| **Output** | State engine direset, halaman wizard ditampilkan ulang |
| **Prioritas** | Sedang |
| **Sumber** | Best practice UX |

---

### Ringkasan Kebutuhan Fungsional

| ID | Deskripsi | Prioritas | Sumber |
|---|---|---|---|
| FR-001 | Memulai sesi konsultasi | Tinggi | Elicitasi — Fungsional |
| FR-002 | Menampilkan pertanyaan gejala step-by-step | Tinggi | Elicitasi — UI/UX |
| FR-003 | Menerima jawaban skala CF User (5 level) | Tinggi | Elicitasi — UI/UX |
| FR-004 | Evaluasi Backward Chaining per hipotesis | Tinggi | Elicitasi — Fungsional |
| FR-005 | Menghitung Certainty Factor kombinasi | Tinggi | Elicitasi — Knowledge Base |
| FR-006 | Explanation Facility: "Mengapa" (Why) | Tinggi | Elicitasi — Explanation |
| FR-007 | Explanation Facility: "Bagaimana" (How) | Tinggi | Elicitasi — Explanation |
| FR-008 | Menampilkan ranking hasil diagnosis | Tinggi | Elicitasi — Fungsional |
| FR-009 | Visualisasi pohon inferensi (Graphviz) | Tinggi | Elicitasi — Non-Fungsional |
| FR-010 | Halaman beranda informatif | Sedang | Umum |
| FR-011 | Riwayat konsultasi (session-based) | Rendah | Best practice UX |
| FR-012 | Konsultasi ulang (reset) | Sedang | Best practice UX |

---

## 4.0 Kebutuhan Non-Fungsional

### 4.1 Kebutuhan Performa

| ID | Kebutuhan | Target | Metrik |
|---|---|---|---|
| NFR-001 | Waktu respons per pertanyaan gejala | < 1 detik | Waktu antara klik "Lanjut" hingga pertanyaan berikutnya ditampilkan |
| NFR-002 | Waktu perhitungan CF seluruh hipotesis | < 2 detik | Waktu dari gejala terakhir hingga hasil diagnosis ditampilkan |
| NFR-003 | Waktu render visualisasi pohon inferensi | < 3 detik | Waktu render Graphviz diagram di halaman hasil |
| NFR-004 | Ukuran halaman | < 5 MB | Total asset yang dimuat per halaman |

### 4.2 Kebutuhan Keamanan

| ID | Kebutuhan | Deskripsi |
|---|---|---|
| NFR-005 | Input validation | Semua input pengguna divalidasi sebelum diproses oleh engine (hanya menerima nilai CF yang valid: 0.0, 0.4, 0.6, 0.8, 1.0) |
| NFR-006 | Tidak ada data sensitif | Sistem tidak menyimpan data pribadi pengguna; semua data bersifat session-based dan anonim |
| NFR-007 | Lokal deployment | Sistem berjalan di localhost, tidak terpapar ke jaringan publik secara default |

### 4.3 Kebutuhan Keandalan & Portabilitas

| ID | Kebutuhan | Deskripsi |
|---|---|---|
| NFR-008 | Browser compatibility | Sistem kompatibel dengan browser modern: Google Chrome (v90+), Mozilla Firefox (v85+), Microsoft Edge (v90+) |
| NFR-009 | OS portability | Sistem dapat dijalankan pada Windows, macOS, dan Linux (dimanapun Python 3.8+ dan Streamlit tersedia) |
| NFR-010 | Error handling | Sistem menampilkan pesan error yang informatif jika terjadi kegagalan (misal: library Graphviz tidak terinstal) |
| NFR-011 | Session stability | Session state Streamlit dijaga stabil selama konsultasi berlangsung tanpa kehilangan progress |
| NFR-012 | Zero-configuration | Sistem dapat dijalankan hanya dengan `pip install -r requirements.txt` dan `streamlit run app.py` tanpa konfigurasi tambahan |

---

## 5.0 Kebutuhan Antarmuka Eksternal

### 5.1 Antarmuka Pengguna (User Interface)

Sistem memiliki **3 halaman utama** yang diakses melalui navigasi sidebar:

| Halaman | Komponen UI Utama |
|---|---|
| **Beranda** | Judul, deskripsi, card fitur, tombol "Mulai Konsultasi", panduan penggunaan |
| **Konsultasi** | Progress bar hipotesis, teks pertanyaan gejala, radio button CF User (5 opsi), tombol "Mengapa?", tombol "Lanjut" |
| **Hasil Diagnosis** | Card ranking kerusakan (kode, nama, CF%, penyebab, solusi), expander "Bagaimana?" per item, visualisasi pohon inferensi (Graphviz), tombol "Konsultasi Ulang" |

**Prinsip UI:**
- **Wizard-based** — Satu pertanyaan per langkah untuk mendemonstrasikan proses Backward Chaining.
- **Progressive disclosure** — Detail teknis (CF, rule) tersembunyi dalam expander, hanya tampil jika diminta.
- **Visual feedback** — Progress bar, warna status (hijau/merah), ikon kontekstual.

### 5.2 Antarmuka Perangkat Keras

| Komponen | Kebutuhan Minimum |
|---|---|
| **Prosesor** | Dual-core 1.5 GHz atau setara |
| **RAM** | 2 GB (4 GB disarankan) |
| **Storage** | 100 MB ruang kosong |
| **Display** | Resolusi minimal 1024×768 |
| **Jaringan** | Tidak diperlukan (offline-capable setelah instalasi) |

### 5.3 Antarmuka Perangkat Lunak

| Software | Versi Minimum | Keterangan |
|---|---|---|
| **Python** | 3.8+ | Runtime utama |
| **Streamlit** | 1.30.0+ | Framework web UI |
| **Graphviz (Python)** | 0.20+ | Library visualisasi pohon inferensi |
| **Graphviz (System)** | 2.40+ | Executable sistem untuk rendering graph |
| **pip** | 20.0+ | Package manager Python |
| **Web Browser** | Chrome 90+ / Firefox 85+ / Edge 90+ | Klien akses |

### 5.4 Antarmuka Komunikasi

Sistem berkomunikasi melalui **protokol HTTP** pada `localhost:8501` (port default Streamlit). Tidak ada antarmuka API eksternal, database remote, atau layanan pihak ketiga yang digunakan.

---

> *Dokumen SRS ini disusun berdasarkan standar IEEE 830-1998 untuk proyek LaptopDoc — Sistem Pakar Diagnosis Kerusakan Laptop. Versi 1.0 — Maret 2026.*
