# DOKUMEN ANALISIS: UML 2.5
## Sistem Pakar Diagnosis Kerusakan Laptop — Laptop Diagnostic Expert
### Pendekatan Hybrid: Rule-Frame & Backward Chaining dengan Certainty Factor

**Standar Acuan:** UML 2.5 (OMG Unified Modeling Language Specification)

| Item | Detail |
|---|---|
| **Versi** | 1.0 |
| **Tanggal** | 28 Maret 2026 |
| **Status** | Final |
| **Dokumen Referensi** | SRS Laptop Diagnostic Expert v1.0, Project Charter v1.0 |

---

## 1. Daftar Aktor

| ID | Aktor | Stereotip | Deskripsi | Justifikasi |
|---|---|---|---|---|
| **A-01** | **Pengguna Awam** | `<<primary>>` | Pengguna laptop tanpa latar belakang teknis yang mengalami masalah pada laptopnya dan ingin mendapatkan diagnosis awal secara mandiri. | Aktor utama yang menggunakan seluruh fitur konsultasi. Sumber: SRS §2.3 — Pengguna Primer. |
| **A-02** | **Teknisi Pemula** | `<<primary>>` | Teknisi pemula / mahasiswa teknik yang membutuhkan panduan terstruktur untuk mengidentifikasi kerusakan laptop sebelum melakukan perbaikan. | Menggunakan fitur yang sama dengan Pengguna Awam, namun memanfaatkan detail teknis (CF, rule, pohon inferensi) secara lebih mendalam. Sumber: SRS §2.3 — Pengguna Sekunder. |
| **A-03** | **Sistem Inference Engine** | `<<system>>` | Komponen internal mesin penalaran Backward Chaining yang secara otomatis mengevaluasi hipotesis, menghitung Certainty Factor, dan menghasilkan diagnosis. | Aktor sistem yang bekerja di background selama proses konsultasi. Sumber: SRS §2.1 — Engine Layer. |

### Generalisasi Aktor

```
            ┌──────────────┐
            │   Pengguna   │
            │   (abstract)  │
            └──────┬───────┘
                   │ {generalization}
          ┌────────┴────────┐
          │                 │
  ┌───────▼───────┐  ┌─────▼──────────┐
  │ Pengguna Awam │  │ Teknisi Pemula │
  │    (A-01)     │  │     (A-02)     │
  └───────────────┘  └────────────────┘
```

> **Catatan:** Pengguna Awam dan Teknisi Pemula memiliki hak akses yang identik terhadap seluruh fitur sistem. Pembedaan dibuat untuk memperjelas *persona* pengguna dalam konteks akademik. Keduanya digeneralisasikan sebagai **Pengguna** yang berinteraksi langsung dengan sistem konsultasi.

---

## 2. Use Case Diagram — Deskripsi Tekstual

### 2.1 Daftar Use Case

| ID | Nama Use Case | Prioritas | Sumber FR |
|---|---|---|---|
| UC-01 | Melihat Halaman Beranda | Sedang | FR-010 |
| UC-02 | Memulai Sesi Konsultasi | Tinggi | FR-001 |
| UC-03 | Melakukan Konsultasi Backward Chaining | Tinggi | FR-002, FR-004 |
| UC-04 | Memasukkan Skala Keyakinan (CF User) | Tinggi | FR-003 |
| UC-05 | Mengakses Explanation Facility — "Mengapa" (Why) | Tinggi | FR-006 |
| UC-06 | Menghitung Certainty Factor | Tinggi | FR-005 |
| UC-07 | Melihat Hasil Diagnosis (Ranking) | Tinggi | FR-008 |
| UC-08 | Mengakses Explanation Facility — "Bagaimana" (How) | Tinggi | FR-007 |
| UC-09 | Melihat Visualisasi Pohon Inferensi | Tinggi | FR-009 |
| UC-10 | Melihat Riwayat Konsultasi | Rendah | FR-011 |
| UC-11 | Melakukan Konsultasi Ulang | Sedang | FR-012 |

### 2.2 Relasi Use Case (Format UML)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM BOUNDARY: Laptop Diagnostic Expert             │
│                                                                             │
│                                                                             │
│   ┌──────────────────────┐                                                  │
│   │ UC-01: Melihat       │                                                  │
│   │ Halaman Beranda      │                                                  │
│   └──────────┬───────────┘                                                  │
│              │ <<extend>>                                                    │
│   ┌──────────▼───────────┐        ┌────────────────────────────────┐        │
│   │ UC-02: Memulai Sesi  ├───────►│ UC-03: Melakukan Konsultasi   │        │
│   │ Konsultasi           │include │ Backward Chaining             │        │
│   └──────────────────────┘        └─────────┬──────────┬──────────┘        │
│                                             │          │                    │
│                              <<include>>    │          │ <<include>>        │
│                           ┌─────────────────┘          └──────────┐        │
│                           ▼                                       ▼        │
│   ┌────────────────────────────────┐   ┌───────────────────────────────┐   │
│   │ UC-04: Memasukkan Skala       │   │ UC-06: Menghitung Certainty   │   │
│   │ Keyakinan (CF User)           │   │ Factor                        │   │
│   └────────────────────────────────┘   └───────────────────────────────┘   │
│                                                                             │
│   ┌────────────────────────────────┐                                        │
│   │ UC-05: Mengakses Explanation  │   <<extend>> dari UC-03                │
│   │ Facility — "Mengapa" (Why)    │   (opsional saat pertanyaan gejala)    │
│   └────────────────────────────────┘                                        │
│                                                                             │
│   ┌────────────────────────────────┐                                        │
│   │ UC-07: Melihat Hasil          │   <<include>> dari UC-03               │
│   │ Diagnosis (Ranking)           │                                         │
│   └─────────┬──────────┬──────────┘                                        │
│             │          │                                                    │
│   <<extend>>│          │<<extend>>                                          │
│        ┌────▼────┐  ┌──▼──────────────────────────────┐                    │
│        │ UC-08:  │  │ UC-09: Melihat Visualisasi      │                    │
│        │"Bagaimana"│ │ Pohon Inferensi                 │                    │
│        │ (How)   │  └─────────────────────────────────┘                    │
│        └─────────┘                                                          │
│                                                                             │
│   ┌────────────────────────────────┐                                        │
│   │ UC-10: Melihat Riwayat        │   <<extend>> dari UC-07                │
│   │ Konsultasi                    │                                         │
│   └────────────────────────────────┘                                        │
│                                                                             │
│   ┌────────────────────────────────┐                                        │
│   │ UC-11: Melakukan Konsultasi   │   <<extend>> dari UC-07                │
│   │ Ulang                         │                                         │
│   └────────────────────────────────┘                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

          ┌───────────────┐                  ┌────────────────────────┐
          │   Pengguna    │                  │  Sistem Inference      │
          │ (A-01, A-02)  │                  │  Engine (A-03)         │
          └───────┬───────┘                  └──────────┬─────────────┘
                  │ berinteraksi dengan:                │ terlibat dalam:
                  ├─── UC-01                            ├─── UC-03 (evaluasi)
                  ├─── UC-02                            ├─── UC-04 (proses input)
                  ├─── UC-03                            ├─── UC-06 (kalkulasi)
                  ├─── UC-04                            └─── UC-07 (generate)
                  ├─── UC-05
                  ├─── UC-07
                  ├─── UC-08
                  ├─── UC-09
                  ├─── UC-10
                  └─── UC-11
```

### 2.3 Tabel Relasi Use Case

| Use Case Sumber | Relasi | Use Case Target | Penjelasan |
|---|---|---|---|
| UC-01 | `<<extend>>` | UC-02 | Dari halaman beranda, pengguna **dapat** memulai konsultasi (opsional). |
| UC-02 | `<<include>>` | UC-03 | Memulai sesi konsultasi **selalu** menjalankan proses Backward Chaining. |
| UC-03 | `<<include>>` | UC-04 | Setiap evaluasi gejala dalam Backward Chaining **selalu** meminta input CF User. |
| UC-03 | `<<include>>` | UC-06 | Proses Backward Chaining **selalu** menghitung Certainty Factor untuk setiap hipotesis. |
| UC-03 | `<<extend>>` | UC-05 | Saat pertanyaan gejala ditampilkan, pengguna **dapat** meminta penjelasan "Mengapa?" (opsional). |
| UC-03 | `<<include>>` | UC-07 | Setelah semua hipotesis dievaluasi, sistem **selalu** menampilkan hasil diagnosis. |
| UC-07 | `<<extend>>` | UC-08 | Pada halaman hasil, pengguna **dapat** melihat detail "Bagaimana?" (opsional). |
| UC-07 | `<<extend>>` | UC-09 | Pada halaman hasil, pengguna **dapat** melihat pohon inferensi (opsional). |
| UC-07 | `<<extend>>` | UC-10 | Pengguna **dapat** melihat riwayat konsultasi sebelumnya (opsional). |
| UC-07 | `<<extend>>` | UC-11 | Pengguna **dapat** memulai konsultasi ulang dari halaman hasil (opsional). |

---

## 3. Spesifikasi Use Case Detail

### 3.1 UC-03: Melakukan Konsultasi Backward Chaining

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  UC-03: Melakukan Konsultasi Backward Chaining                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  +-- Aktor       : Pengguna (A-01: Pengguna Awam / A-02: Teknisi Pemula), ║
║  |                 Sistem Inference Engine (A-03)                           ║
║  |                                                                          ║
║  +-- Deskripsi   : Pengguna melakukan konsultasi diagnosis kerusakan       ║
║  |                 laptop melalui wizard interaktif step-by-step.          ║
║  |                 Sistem Inference Engine mengevaluasi hipotesis           ║
║  |                 kerusakan (K01-K10) secara iteratif menggunakan         ║
║  |                 metode Backward Chaining. Untuk setiap hipotesis,       ║
║  |                 engine mencari rule yang mengarah ke hipotesis           ║
║  |                 tersebut, lalu menanyakan premis/gejala satu per        ║
║  |                 satu kepada pengguna.                                   ║
║  |                                                                          ║
║  +-- Precondition:                                                         ║
║  |    1. Pengguna telah mengakses sistem melalui browser.                  ║
║  |    2. Pengguna telah mengklik tombol "Mulai Konsultasi" (UC-02).       ║
║  |    3. Backward Chaining engine telah diinisialisasi.                    ║
║  |    4. Knowledge Base (10 Frame, 12 Rule, 25 Gejala) telah dimuat.      ║
║  |                                                                          ║
║  +-- Basic Flow  :                                                         ║
║  |    1. Engine memilih hipotesis pertama (K01) sebagai goal aktif.        ║
║  |    2. Engine mencari rule yang konklusinya = hipotesis aktif.           ║
║  |    3. Engine mengambil premis/gejala pertama dari rule tersebut.        ║
║  |    4. Sistem menampilkan pertanyaan gejala kepada pengguna:             ║
║  |       - Kode gejala (misal: G01)                                       ║
║  |       - Teks deskriptif gejala                                         ║
║  |       - Progress bar posisi hipotesis saat ini                         ║
║  |    5. Pengguna memilih skala CF User (<<include>> UC-04).              ║
║  |    6. Engine menerima nilai CF User dan menyimpannya.                   ║
║  |    7. [Branching] Jika CF User > 0.0:                                  ║
║  |       a. Engine melanjutkan ke premis/gejala berikutnya dalam rule.     ║
║  |       b. Ulangi langkah 4-6 untuk setiap premis.                       ║
║  |    8. Setelah semua premis rule terevaluasi, engine menghitung          ║
║  |       CF kombinasi (<<include>> UC-06).                                ║
║  |    9. Hipotesis dinyatakan TERBUKTI dengan CF final yang dihitung.     ║
║  |   10. Engine berpindah ke hipotesis berikutnya (K02, K03, ..., K10).   ║
║  |   11. Ulangi langkah 2-10 untuk setiap hipotesis.                     ║
║  |   12. Setelah semua hipotesis dievaluasi, hasil diagnosis              ║
║  |       ditampilkan (<<include>> UC-07).                                 ║
║  |                                                                          ║
║  +-- Alternative :                                                         ║
║  |    ALT-1: Hipotesis GAGAL (CF User = 0.0 pada salah satu premis)       ║
║  |       7a. Jika CF User = 0.0:                                          ║
║  |           - Hipotesis aktif dinyatakan GAGAL.                           ║
║  |           - Engine langsung berpindah ke hipotesis berikutnya           ║
║  |             (lanjut ke langkah 10).                                     ║
║  |           - Premis yang tersisa TIDAK ditanyakan.                       ║
║  |                                                                          ║
║  |    ALT-2: Hipotesis memiliki multiple rules (misal: K08 → R8,R11,R12)  ║
║  |       2a. Engine menemukan >1 rule untuk hipotesis yang sama.           ║
║  |       2b. Semua rule dievaluasi secara berurutan.                       ║
║  |       8a. CF antar-rule dikombinasikan menggunakan formula              ║
║  |           CF_combine secara iteratif.                                   ║
║  |                                                                          ║
║  |    ALT-3: Gejala sudah pernah dijawab di hipotesis sebelumnya          ║
║  |       4a. Jika gejala sudah pernah dijawab, engine menggunakan         ║
║  |           nilai CF User yang telah tersimpan.                           ║
║  |       4b. Pertanyaan TIDAK ditampilkan ulang (skip).                    ║
║  |                                                                          ║
║  |    ALT-4: Pengguna mengklik "Mengapa?" (opsional)                      ║
║  |       4c. Sistem menampilkan Explanation Facility "Mengapa"            ║
║  |           (<<extend>> UC-05).                                          ║
║  |       4d. Setelah penjelasan dibaca, kembali ke langkah 5.             ║
║  |                                                                          ║
║  +-- Exception   :                                                         ║
║  |    EXC-1: Knowledge Base gagal dimuat                                   ║
║  |       - Sistem menampilkan pesan error informatif.                      ║
║  |       - Pengguna diarahkan kembali ke halaman beranda.                  ║
║  |                                                                          ║
║  |    EXC-2: Session state hilang di tengah konsultasi                     ║
║  |       - Sistem mendeteksi state tidak konsisten.                        ║
║  |       - Pengguna diminta memulai ulang konsultasi.                      ║
║  |                                                                          ║
║  +-- Postcondition:                                                        ║
║       1. Seluruh hipotesis (K01-K10) telah dievaluasi.                    ║
║       2. Setiap hipotesis memiliki status: TERBUKTI (CF > 0) atau GAGAL.  ║
║       3. Hasil diagnosis tersimpan di session state.                       ║
║       4. Halaman hasil diagnosis ditampilkan kepada pengguna.              ║
║                                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

### 3.2 UC-04: Memasukkan Skala Keyakinan (CF User)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  UC-04: Memasukkan Skala Keyakinan (CF User)                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  +-- Aktor       : Pengguna (A-01: Pengguna Awam / A-02: Teknisi Pemula)  ║
║  |                                                                          ║
║  +-- Deskripsi   : Pengguna memberikan tingkat keyakinan terhadap suatu   ║
║  |                 gejala yang ditanyakan oleh sistem. Jawaban berupa      ║
║  |                 skala numerik Certainty Factor User (CF User) dengan    ║
║  |                 5 level yang masing-masing merepresentasikan tingkat    ║
║  |                 kepercayaan pengguna bahwa gejala tersebut dialami.     ║
║  |                                                                          ║
║  +-- Precondition:                                                         ║
║  |    1. Proses konsultasi Backward Chaining sedang berlangsung (UC-03).  ║
║  |    2. Pertanyaan gejala telah ditampilkan di layar.                     ║
║  |    3. Radio button dengan 5 opsi CF tersedia dan aktif.                 ║
║  |                                                                          ║
║  +-- Basic Flow  :                                                         ║
║  |    1. Sistem menampilkan 5 opsi radio button:                          ║
║  |       ┌─────────────────────────────────────────────────────────┐       ║
║  |       │ ○ (0.0) Tidak        — Gejala tidak dialami            │       ║
║  |       │ ○ (0.4) Kurang yakin — Kadang terasa                   │       ║
║  |       │ ○ (0.6) Cukup yakin  — Cukup sering                   │       ║
║  |       │ ○ (0.8) Yakin        — Jelas tampak                    │       ║
║  |       │ ○ (1.0) Sangat yakin — Benar-benar terjadi             │       ║
║  |       └─────────────────────────────────────────────────────────┘       ║
║  |    2. Pengguna memilih salah satu opsi.                                ║
║  |    3. Pengguna mengklik tombol "Lanjut".                               ║
║  |    4. Sistem memvalidasi bahwa salah satu opsi telah dipilih.          ║
║  |    5. Nilai CF User disimpan ke session state dengan key = kode gejala.║
║  |    6. Engine melanjutkan evaluasi premis berikutnya                     ║
║  |       (kembali ke UC-03, langkah 7).                                   ║
║  |                                                                          ║
║  +-- Alternative :                                                         ║
║  |    ALT-1: Pengguna memilih CF = 0.0 (Tidak mengalami gejala)          ║
║  |       5a. Nilai CF = 0.0 disimpan.                                     ║
║  |       6a. Engine langsung menandai hipotesis sebagai GAGAL.            ║
║  |       6b. Engine berpindah ke hipotesis berikutnya.                     ║
║  |                                                                          ║
║  +-- Exception   :                                                         ║
║  |    EXC-1: Pengguna mengklik "Lanjut" tanpa memilih opsi               ║
║  |       - Sistem menampilkan pesan validasi:                              ║
║  |         "Silakan pilih tingkat keyakinan Anda sebelum melanjutkan."    ║
║  |       - Tombol "Lanjut" tetap non-aktif/tidak memproses.              ║
║  |                                                                          ║
║  |    EXC-2: Nilai CF yang diterima di luar range valid                    ║
║  |       - Sistem menolak input dan menampilkan error.                     ║
║  |       - Hanya nilai [0.0, 0.4, 0.6, 0.8, 1.0] yang diterima.         ║
║  |                                                                          ║
║  +-- Postcondition:                                                        ║
║       1. Nilai CF User untuk gejala aktif tersimpan dalam session state.  ║
║       2. Engine telah menerima input dan siap melanjutkan evaluasi.       ║
║       3. Jika CF = 0.0 → hipotesis aktif berstatus GAGAL.                ║
║       4. Jika CF > 0.0 → engine melanjutkan ke premis/gejala berikutnya. ║
║                                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

### 3.3 UC-05: Mengakses Explanation Facility — "Mengapa" (Why)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  UC-05: Mengakses Explanation Facility — "Mengapa" (Why)                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  +-- Aktor       : Pengguna (A-01: Pengguna Awam / A-02: Teknisi Pemula)  ║
║  |                                                                          ║
║  +-- Deskripsi   : Pengguna mengakses fasilitas penjelasan "Mengapa?"     ║
║  |                 untuk memahami alasan di balik pertanyaan gejala yang   ║
║  |                 ditampilkan oleh sistem. Fitur ini menunjukkan          ║
║  |                 transparansi proses penalaran Backward Chaining         ║
║  |                 dengan menjelaskan hubungan antara gejala yang          ║
║  |                 ditanyakan, rule yang sedang dievaluasi, dan            ║
║  |                 hipotesis kerusakan yang sedang diuji.                  ║
║  |                                                                          ║
║  +-- Precondition:                                                         ║
║  |    1. Proses konsultasi Backward Chaining sedang berlangsung (UC-03).  ║
║  |    2. Pertanyaan gejala sedang ditampilkan di layar.                    ║
║  |    3. Tombol "Mengapa?" tersedia dan aktif.                            ║
║  |    4. Engine state memiliki informasi hipotesis aktif dan rule aktif.   ║
║  |                                                                          ║
║  +-- Basic Flow  :                                                         ║
║  |    1. Pengguna mengklik tombol "Mengapa?" di samping pertanyaan gejala.║
║  |    2. Sistem mengambil informasi dari engine state:                     ║
║  |       - Kode dan teks gejala yang sedang ditanyakan (misal: G01).      ║
║  |       - Rule yang sedang dievaluasi (misal: R1).                       ║
║  |       - CF Pakar dari rule tersebut.                                    ║
║  |       - Hipotesis kerusakan yang sedang diuji (misal: K01).            ║
║  |    3. Sistem merangkai teks penjelasan dengan template:                ║
║  |       ┌─────────────────────────────────────────────────────────┐       ║
║  |       │ 💡 Mengapa saya menanyakan ini?                        │       ║
║  |       │                                                         │       ║
║  |       │ Saya menanyakan gejala [G01 — Laptop tidak menyala     │       ║
║  |       │ sama sekali] untuk mengevaluasi hipotesis kerusakan     │       ║
║  |       │ [K01 — Kerusakan Power Supply / Adaptor].               │       ║
║  |       │                                                         │       ║
║  |       │ Gejala ini merupakan premis dari rule [R1] dengan       │       ║
║  |       │ CF Pakar = 0.9                                          │       ║
║  |       └─────────────────────────────────────────────────────────┘       ║
║  |    4. Teks penjelasan ditampilkan dalam komponen expander/panel.       ║
║  |    5. Pengguna membaca penjelasan.                                     ║
║  |    6. Pengguna melanjutkan menjawab pertanyaan gejala                  ║
║  |       (kembali ke UC-04).                                              ║
║  |                                                                          ║
║  +-- Alternative :                                                         ║
║  |    ALT-1: Pengguna tidak mengklik "Mengapa?"                           ║
║  |       - Penjelasan tidak ditampilkan.                                   ║
║  |       - Tidak ada dampak pada alur konsultasi.                          ║
║  |       - Pengguna langsung menjawab pertanyaan (UC-04).                 ║
║  |                                                                          ║
║  |    ALT-2: Pengguna mengklik "Mengapa?" berulang kali                   ║
║  |       - Expander toggle (buka/tutup) tanpa efek samping.               ║
║  |       - Teks penjelasan tetap sama selama gejala yang sama aktif.      ║
║  |                                                                          ║
║  +-- Exception   :                                                         ║
║  |    EXC-1: Engine state tidak tersedia / corrupt                         ║
║  |       - Sistem menampilkan pesan fallback:                              ║
║  |         "Informasi penjelasan tidak tersedia saat ini."                ║
║  |       - Alur konsultasi tetap berlanjut normal.                         ║
║  |                                                                          ║
║  +-- Postcondition:                                                        ║
║       1. Penjelasan "Mengapa?" telah ditampilkan (jika diminta).          ║
║       2. Tidak ada perubahan pada state engine atau proses inferensi.     ║
║       3. Pengguna dapat melanjutkan menjawab pertanyaan gejala.           ║
║                                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 4. Traceability Matrix: FR → UC

Matriks ketertelusuran berikut menghubungkan setiap Functional Requirement (FR-xxx) dari dokumen SRS ke Use Case (UC-xxx) yang mengimplementasikannya.

| FR-ID | Deskripsi FR | UC-ID | Nama Use Case | Cakupan |
|---|---|---|---|---|
| FR-001 | Memulai sesi konsultasi | **UC-02** | Memulai Sesi Konsultasi | Penuh |
| FR-002 | Menampilkan pertanyaan gejala step-by-step | **UC-03** | Melakukan Konsultasi Backward Chaining | Penuh |
| FR-003 | Menerima jawaban skala CF User (5 level) | **UC-04** | Memasukkan Skala Keyakinan (CF User) | Penuh |
| FR-004 | Evaluasi Backward Chaining per hipotesis | **UC-03** | Melakukan Konsultasi Backward Chaining | Penuh |
| FR-005 | Menghitung Certainty Factor kombinasi | **UC-06** | Menghitung Certainty Factor | Penuh |
| FR-006 | Explanation Facility: "Mengapa" (Why) | **UC-05** | Mengakses Explanation Facility — "Mengapa" (Why) | Penuh |
| FR-007 | Explanation Facility: "Bagaimana" (How) | **UC-08** | Mengakses Explanation Facility — "Bagaimana" (How) | Penuh |
| FR-008 | Menampilkan ranking hasil diagnosis | **UC-07** | Melihat Hasil Diagnosis (Ranking) | Penuh |
| FR-009 | Visualisasi pohon inferensi (Graphviz) | **UC-09** | Melihat Visualisasi Pohon Inferensi | Penuh |
| FR-010 | Halaman beranda informatif | **UC-01** | Melihat Halaman Beranda | Penuh |
| FR-011 | Riwayat konsultasi (session-based) | **UC-10** | Melihat Riwayat Konsultasi | Penuh |
| FR-012 | Konsultasi ulang (reset) | **UC-11** | Melakukan Konsultasi Ulang | Penuh |

### Ringkasan Cakupan

| Metrik | Nilai |
|---|---|
| Total Functional Requirements | 12 |
| Total Use Cases | 11 |
| FR yang tercakup UC | **12/12 (100%)** |
| UC tanpa FR (orphan) | **0** |
| Cakupan keseluruhan | **100% — Penuh** |

> **Kesimpulan:** Seluruh kebutuhan fungsional (FR-001 s.d. FR-012) dari dokumen SRS telah di-*trace* ke minimal satu Use Case. Tidak ada kebutuhan fungsional yang tidak tercakup, dan tidak ada Use Case yang tidak memiliki sumber kebutuhan.

---

### Matriks Silang (Cross-Reference)

|  | UC-01 | UC-02 | UC-03 | UC-04 | UC-05 | UC-06 | UC-07 | UC-08 | UC-09 | UC-10 | UC-11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **FR-001** | | ✓ | | | | | | | | | |
| **FR-002** | | | ✓ | | | | | | | | |
| **FR-003** | | | | ✓ | | | | | | | |
| **FR-004** | | | ✓ | | | | | | | | |
| **FR-005** | | | | | | ✓ | | | | | |
| **FR-006** | | | | | ✓ | | | | | | |
| **FR-007** | | | | | | | | ✓ | | | |
| **FR-008** | | | | | | | ✓ | | | | |
| **FR-009** | | | | | | | | | ✓ | | |
| **FR-010** | ✓ | | | | | | | | | | |
| **FR-011** | | | | | | | | | | ✓ | |
| **FR-012** | | | | | | | | | | | ✓ |

---

> *Dokumen UML Analysis ini disusun berdasarkan standar UML 2.5 untuk proyek Laptop Diagnostic Expert — Sistem Pakar Diagnosis Kerusakan Laptop. Merujuk pada SRS v1.0 dan Project Charter v1.0. Versi 1.0 — Maret 2026.*
