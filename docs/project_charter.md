# PROJECT CHARTER
## Sistem Pakar Diagnosis Kerusakan Laptop
### Pendekatan Hybrid: Rule-Frame & Backward Chaining dengan Certainty Factor

---

## 1.0 Informasi Proyek

Proyek ini dikembangkan oleh kelompok mahasiswa Ilmu Komputer UGM:

| NIM | Nama |
|---|---|
| 24/537757/PA/22793 | Andra Kusnaedi Ilyaz |
| 24/533487/PA/22582 | Azhar Maulana |
| 24/539383/PA/22903 | Bobby Rahman Hartanto |
| 24/533395/PA/22573 | Kukuh Agus Hermawan |
| 24/545406/PA/23176 | Rayhan Haldi Hermawan |


---

## 2.0 Latar Belakang & Rumusan Masalah

### 2.1 Latar Belakang

Diagnosis kerusakan laptop tidak selalu dapat diputuskan secara pasti karena
gejala yang diberikan pengguna sering tidak lengkap, samar, atau tingkat keyakinan-
nya berbeda-beda. Oleh sebab itu, rancangan laporan ini dibuat menggunakan model
backward chaining dengan menambahkan certainty factor agar sistem masih dapat
memberikan kesimpulan yang valid meskipun tidak semua rule terpenuhi.

Versi deterministik memiliki keterbatasan karena suatu hipotesis baru dapat
dinyatakan benar apabila seluruh premisnya terpenuhi. Dalam praktiknya, kondi-
si tersebut tidak selalu terjadi, sebab pengguna sering kali hanya memiliki tingkat
keyakinan parsial terhadap gejala yang dialami. Oleh karena itu, sistem dirancang
agar mampu menerima derajat keyakinan pada setiap gejala dan mengolahnya men-
jadi tingkat keyakinan terhadap hipotesis yang diuji. Dengan pendekatan ini, hasil
diagnosis tidak hanya berupa satu keputusan yang bersifat mutlak, tetapi juga dapat
menampilkan beberapa hipotesis lain beserta nilai Certainty Factor tertinggi sebagai
dasar penentuan kesimpulan utama.


### 2.2 Rumusan Masalah
Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam pro-
yek ini adalah sebagai berikut:
1. Bagaimana sistem pakar diagnosis kerusakan laptop yang baik?
2. Apa saja gejala, penyebab kerusakan, dan solusi perbaikan laptop yang bisa
dirumuskan ke dalam sistem pakar?
3. Bagaimana penerapan backward chaining untuk proses diagnosis berbasis goal?
4. Bagaimana implementasi certainty factor agar sistem dapat menangani ketidakpastian?
5. Bagaimana kesediaan explanation facility untuk pengguna?

---

## 3.0 Tujuan 
1. Membangun prototipe sistem pakar diagnosis kerusakan lapto
2. Mengidentifikasi gejala, penyebab kerusakan, dan solusi perbaikan laptop yang
bisa dirumuskan ke dalam sistem pakar.
3. Menerapkan backward chaining untuk proses diagnosis berbasis goal.
4. Menambahkan certainty factor agar sistem dapat menangani ketidakpastian
5. Menyediakan explanation facility yang menjelaskan why dan how, termasuk
perhitungan CF.

## 4.0 Ruang Lingkup (Scope)

### 4.1 In Scope ✅

| No | Item |
|---|---|
| 1 | Diagnosis 10 jenis kerusakan laptop (K01-K10) |
| 2 | Evaluasi 25 gejala (G01-G25) melalui konsultasi interaktif |
| 3 | Representasi pengetahuan hybrid: 10 Frame + 12 Rule |
| 4 | Inference engine: Backward Chaining (goal-driven, iteratif) |
| 5 | Perhitungan Certainty Factor (CF pakar × CF user kombinasi) |
| 6 | Explanation Facility: "Mengapa" (per pertanyaan) dan "Bagaimana" (per hasil) |
| 7 | Visualisasi pohon inferensi menggunakan Graphviz |
| 8 | Antarmuka wizard step-by-step (satu pertanyaan per langkah) |
| 9 | Skala keyakinan user: 5 level (0.0, 0.4, 0.6, 0.8, 1.0) |
| 10 | Deployment lokal: `streamlit run app.py` |

### 4.2 Out of Scope ❌

| No | Item | Alasan |
|---|---|---|
| 1 | Halaman Admin CRUD (kelola knowledge base via UI) | Fokus prototype pada konsultasi |
| 2 | Database persisten (PostgreSQL/MySQL) | Data di-hardcode dalam modul Python |
| 3 | Autentikasi pengguna (login/register) | Tidak diperlukan untuk demo |
| 4 | Mobile-native app (iOS/Android) | Prototype web-based saja |
| 5 | Diagnosis kerusakan di luar 10 kategori | Batasan scope basis pengetahuan |
| 6 | Integrasi API pihak ketiga | Prototype mandiri |
| 7 | Multi-bahasa (i18n) | Bahasa Indonesia saja |

---

## 5.0 Stakeholder & Peran

| Stakeholder | Peran | Tanggung Jawab |
|---|---|---|
| **Dosen Pengampu** | Product Owner / Evaluator | Menentukan requirement, menilai hasil akhir |
| **Mahasiswa / Tim** | Developer & Analyst | Analisis, desain, implementasi, testing, dokumentasi |
| **Pengguna Target** | End User (simulasi) | Menguji coba konsultasi diagnosis saat demo |

---

## 6.0 Asumsi & Kendala

### 6.1 Asumsi

1. Basis pengetahuan (10 kerusakan, 25 gejala, 12 rule, bobot CF) dianggap **valid dan representatif** untuk kebutuhan prototype akademik.
2. Pengguna mampu memahami dan menjawab pertanyaan gejala dengan **jujur** sesuai kondisi laptop.
3. Lingkungan pengembangan dan demo memiliki **Python 3.8+** dan koneksi internet untuk instalasi dependency awal.
5. Skala CF User (5 level) dianggap cukup granular untuk menangkap tingkat keyakinan pengguna.

### 6.2 Kendala

1. **Waktu terbatas** — Pengembangan harus selesai sesuai deadline mata kuliah.
2. **Scope terbatas** — Hanya 10 kerusakan dan 25 gejala; diagnosis di luar scope tidak ditangani.
3. **Satu teknologi** — Prototype hanya menggunakan Streamlit (Python), tanpa backend terpisah.
4. **Tidak ada validasi pakar real** — Bobot CF disusun berdasarkan literatur, bukan konsultasi langsung dengan teknisi.
5. **Session-based** — Riwayat konsultasi hilang saat browser ditutup (tidak ada persistensi).

---

## 7.0 Risiko Awal

| ID | Risiko | Dampak | Probabilitas | Mitigasi |
|---|---|---|---|---|
| RSK-01 | Bobot CF tidak akurat → diagnosis menyesatkan | Tinggi | Sedang | Validasi ulang bobot dengan literatur; uji coba dengan skenario realistis |
| RSK-02 | Gejala ambigu → user bingung memilih jawaban | Sedang | Tinggi | Teks gejala diperjelas; tambahkan tooltip/deskripsi |
| RSK-03 | Visualisasi pohon inferensi terlalu kompleks saat semua rule dievaluasi | Sedang | Sedang | Grouping per kerusakan, filter hanya rule yang triggered |
| RSK-04 | Library Graphviz gagal di environment tertentu | Sedang | Rendah | Fallback ke text-based tree; sediakan instruksi instalasi |
| RSK-05 | Performa lambat jika backward chaining menanyakan terlalu banyak gejala | Rendah | Rendah | Max 25 gejala cukup ringan; optimasi skip gejala yang sudah dijawab |
| RSK-06 | Streamlit session state konflik saat multiple user | Rendah | Sedang | Untuk demo, cukup 1 user; dokumentasikan limitasi |
| RSK-07 | Deadline mepet → fitur visualization tidak sempurna | Sedang | Sedang | Prioritaskan core (BC + CF + Explanation); visualization sebagai fitur bonus |

---





> *Dokumen ini merupakan Project Charter resmi untuk proyek Laptop Diagnostic Expert — Sistem Pakar Diagnosis Kerusakan Laptop. Versi 1.0 — Maret 2026.*
