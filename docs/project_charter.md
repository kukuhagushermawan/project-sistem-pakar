# PROJECT CHARTER
## Sistem Pakar Diagnosis Kerusakan Laptop
### Pendekatan Hybrid: Rule-Frame & Backward Chaining dengan Certainty Factor

---

## 1.0 Informasi Proyek

| Item | Detail |
|---|---|
| **Nama Proyek** | LaptopDoc — Sistem Pakar Diagnosis Kerusakan Laptop |
| **Kode Proyek** | SP-LAPTOP-2026 |
| **Klien/Lembaga** | Program Studi Teknik Informatika — Mata Kuliah Sistem Pakar |
| **Jenis Proyek** | Proyek Akademik (Prototype) |
| **Manajer Proyek** | [Nama Mahasiswa / Ketua Kelompok] |
| **Tanggal Mulai** | 27 Maret 2026 |
| **Target Selesai** | [Sesuaikan dengan deadline mata kuliah] |
| **Versi Dokumen** | 1.0 |
| **Status** | Draft |

---

## 2.0 Latar Belakang & Permasalahan

### 2.1 Latar Belakang

Laptop merupakan perangkat komputasi yang banyak digunakan di kalangan mahasiswa, pekerja, dan masyarakat umum. Seiring intensitas penggunaan yang tinggi, kerusakan pada laptop menjadi hal yang tidak terhindarkan. Namun, tidak semua pengguna memiliki pengetahuan teknis yang memadai untuk mengidentifikasi jenis kerusakan yang dialami.

Proses diagnosis kerusakan laptop secara konvensional memerlukan keahlian seorang teknisi berpengalaman, yang belum tentu selalu tersedia — terutama di daerah dengan keterbatasan akses layanan servis. Di sisi lain, perkembangan teknologi kecerdasan buatan, khususnya **Sistem Pakar (Expert System)**, memungkinkan pengetahuan seorang pakar untuk dikodifikasi dan diakses oleh pengguna awam melalui antarmuka yang sederhana.

### 2.2 Permasalahan

1. **Keterbatasan akses terhadap teknisi laptop** — Pengguna awam kesulitan mendiagnosis kerusakan laptop secara mandiri.
2. **Diagnosis awal yang tidak akurat** — Tanpa panduan terstruktur, pengguna sering salah mengidentifikasi penyebab kerusakan, yang berpotensi memperburuk kondisi perangkat.
3. **Biaya servis yang tidak efisien** — Ketidaktahuan pengguna terhadap jenis kerusakan menyebabkan biaya perbaikan membengkak karena trial-and-error.
4. **Kebutuhan sistem cerdas yang transparan** — Sistem diagnosis perlu mampu menjelaskan logika di balik kesimpulannya (Explanation Facility), bukan sekadar memberikan output.

---

## 3.0 Tujuan & Manfaat Sistem

### 3.1 Tujuan

1. Membangun prototype sistem pakar berbasis web yang mampu mendiagnosis **10 jenis kerusakan laptop** berdasarkan **25 gejala** menggunakan pendekatan **Backward Chaining**.
2. Mengimplementasikan representasi pengetahuan **hybrid (Rule-Frame)** untuk memisahkan data faktual (Frame) dari logika inferensi (Rule).
3. Menerapkan metode **Certainty Factor (CF)** untuk menghitung tingkat keyakinan diagnosis.
4. Menyediakan **Explanation Facility** yang mencakup fasilitas "Mengapa" (Why) dan "Bagaimana" (How) pada setiap proses konsultasi.
5. Menyediakan **visualisasi pohon inferensi** sebagai representasi visual proses pengambilan keputusan.

### 3.2 Manfaat

| Untuk | Manfaat |
|---|---|
| **Pengguna Awam** | Mendapatkan diagnosis awal kerusakan laptop secara mandiri, cepat, dan transparan |
| **Teknisi Pemula** | Referensi terstruktur untuk mempercepat identifikasi masalah |
| **Akademik** | Demonstrasi implementasi nyata konsep Sistem Pakar (Backward Chaining, CF, Explanation Facility) |
| **Institusi** | Prototype yang dapat dikembangkan lebih lanjut sebagai layanan bantuan teknis |

---

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
| **Asisten Dosen** | Reviewer (opsional) | Review teknis, feedback kualitas kode |

---

## 6.0 Asumsi & Kendala

### 6.1 Asumsi

1. Basis pengetahuan (10 kerusakan, 25 gejala, 12 rule, bobot CF) dianggap **valid dan representatif** untuk kebutuhan prototype akademik.
2. Pengguna mampu memahami dan menjawab pertanyaan gejala dengan **jujur** sesuai kondisi laptop.
3. Lingkungan pengembangan dan demo memiliki **Python 3.8+** dan koneksi internet untuk instalasi dependency awal.
4. Sistem cukup berjalan di **localhost** tanpa memerlukan deployment cloud.
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

## 8.0 Milestone Utama

| No | Milestone | Deliverable | Estimasi |
|---|---|---|---|
| M1 | Analisis & Elicitasi Kebutuhan | Dokumen kebutuhan, jawaban klarifikasi | ✅ Selesai |
| M2 | Project Charter & SRS Draft | Dokumen Project Charter + SRS IEEE 830 | ✅ Selesai |
| M3 | Desain Arsitektur & Knowledge Base | Implementation Plan, struktur folder, rule base | ✅ Selesai |
| M4 | Implementasi Knowledge Base | `frames.py`, `rules.py`, `symptoms.py` | Minggu ke-1 |
| M5 | Implementasi Inference Engine | `backward_chaining.py`, `certainty_factor.py` | Minggu ke-1 |
| M6 | Implementasi UI Konsultasi | `app.py`, `consultation.py`, `result.py` | Minggu ke-2 |
| M7 | Implementasi Explanation Facility | Fitur "Mengapa" dan "Bagaimana" | Minggu ke-2 |
| M8 | Implementasi Visualisasi | Pohon inferensi (Graphviz) | Minggu ke-2 |
| M9 | Testing & Validasi | Unit test, E2E testing, validasi CF | Minggu ke-3 |
| M10 | Demo & Presentasi | Prototype berjalan + dokumentasi final | Minggu ke-3 |

---

## 9.0 Persetujuan

Dengan menandatangani dokumen ini, pihak-pihak di bawah menyetujui isi Project Charter dan memberikan otorisasi untuk memulai pelaksanaan proyek.

| Peran | Nama | Tanda Tangan | Tanggal |
|---|---|---|---|
| **Dosen Pengampu / Pembimbing** | _________________________ | _____________ | ____/____/2026 |
| **Ketua Tim / Manajer Proyek** | _________________________ | _____________ | ____/____/2026 |
| **Anggota Tim 1** | _________________________ | _____________ | ____/____/2026 |
| **Anggota Tim 2** | _________________________ | _____________ | ____/____/2026 |

---

> *Dokumen ini merupakan Project Charter resmi untuk proyek LaptopDoc — Sistem Pakar Diagnosis Kerusakan Laptop. Versi 1.0 — Maret 2026.*
