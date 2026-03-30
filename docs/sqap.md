# SOFTWARE QUALITY ASSURANCE PLAN (SQAP)
## Sistem Pakar Diagnosis Kerusakan Laptop — LaptopDoc
### Pengujian Fungsionalitas Web & Akurasi Inference Engine

**Standar Acuan:** IEEE Std 730-2014 (IEEE Standard for Software Quality Assurance Processes)

| Item | Detail |
|---|---|
| **Versi** | 1.0 |
| **Tanggal** | 28 Maret 2026 |
| **Status** | Final |
| **Dokumen Referensi** | SRS v1.0 (IEEE 830), UML Analysis v1.0 (UML 2.5), KB Design v1.0 (ISO/IEC 9075), Architecture Design v1.0 (IEEE 1016) |

---

## 1.0 Tujuan & Ruang Lingkup SQA

### 1.1 Tujuan

Dokumen Software Quality Assurance Plan (SQAP) ini bertujuan untuk:

1. **Mendefinisikan proses penjaminan kualitas** yang sistematis dan terukur untuk seluruh siklus pengembangan sistem pakar LaptopDoc.
2. **Menjamin kebenaran logika inferensi** — memastikan Backward Chaining Engine mengevaluasi hipotesis secara goal-driven tanpa infinite loop, deadlock, atau missing path.
3. **Memvalidasi akurasi kalkulasi Certainty Factor** — memverifikasi bahwa formula `CF_final = CF_pakar × CF_user_kombinasi` dan `CF_combine(CF1, CF2) = CF1 + CF2 × (1 - CF1)` menghasilkan nilai yang benar secara matematis.
4. **Memastikan integritas Knowledge Base** — memverifikasi bahwa 10 Frame, 25 Gejala, dan 12 Rule saling konsisten, tidak ada orphan, dan tidak ada kontradiksi antar rule.
5. **Menjamin kualitas antarmuka pengguna** — memastikan wizard konsultasi Streamlit responsif, navigasi berfungsi, dan Explanation Facility menampilkan penjelasan yang akurat.

### 1.2 Ruang Lingkup

SQAP ini mencakup **dua domain pengujian** yang berjalan secara paralel:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    RUANG LINGKUP SQA LaptopDoc                      │
│                                                                      │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  DOMAIN 1: Pengujian Fungsionalitas UI Web           │           │
│  │  (Streamlit / Python)                                │           │
│  │                                                      │           │
│  │  • Navigasi halaman (Beranda → Konsultasi → Hasil)   │           │
│  │  • Widget wizard (radio button, progress bar, button)│           │
│  │  • Rendering Explanation Facility (expander Why/How) │           │
│  │  • Rendering visualisasi pohon inferensi (Graphviz)  │           │
│  │  • Session state persistence selama konsultasi       │           │
│  │  • Validasi input (hanya CF valid: 0.0-1.0)          │           │
│  │  • Responsivitas halaman (< 1 detik per pertanyaan)  │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  DOMAIN 2: Pengujian Akurasi Logika Inference Engine │           │
│  │  & Knowledge Base                                    │           │
│  │                                                      │           │
│  │  • Kebenaran algoritma Backward Chaining             │           │
│  │  • Akurasi perhitungan CF combine & CF final         │           │
│  │  • Konsistensi Knowledge Base (Frame ↔ Rule ↔ Gejala)│           │
│  │  • Early termination saat CF User = 0.0              │           │
│  │  • Multi-rule evaluation (K08 → R8, R11, R12)        │           │
│  │  • Shared symptom caching (G07 → R3, R5)             │           │
│  │  • Ranking hasil diagnosis berdasarkan CF tertinggi  │           │
│  │  • Explanation Facility accuracy (Why & How content) │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  DI LUAR RUANG LINGKUP (Out of Scope)                │           │
│  │                                                      │           │
│  │  ✗ Performance testing skala besar (> 100 concurrent)│           │
│  │  ✗ Security / penetration testing                    │           │
│  │  ✗ Cross-platform mobile testing                     │           │
│  │  ✗ Load testing / stress testing                     │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2.0 Manajemen SQA

### 2.1 Organisasi & Tanggung Jawab

| No | Peran | Personel | Tanggung Jawab SQA |
|---|---|---|---|
| 1 | **SQA Lead / QA Manager** | Ketua Tim | Menyusun SQAP, memantau quality gates, mereview laporan defect, menyetujui rilis. |
| 2 | **Developer / Programmer** | Anggota Tim 1 | Menulis kode, menjalankan unit test, memperbaiki defect, memenuhi standar PEP 8. |
| 3 | **Tester** | Anggota Tim 2 | Menyusun test case, menjalankan integration test & E2E test, melaporkan defect. |
| 4 | **Knowledge Engineer** | Ketua Tim / Anggota Tim 1 | Memvalidasi kebenaran Knowledge Base (Frame, Rule, bobot CF), mereview konsistensi rule. |
| 5 | **Reviewer / Evaluator** | Dosen Pengampu | Melakukan UAT sign-off, memberikan feedback kualitas, menilai hasil akhir. |

```
             ┌─────────────────────┐
             │    Dosen Pengampu   │
             │   (UAT Evaluator)   │
             └─────────┬───────────┘
                       │ evaluasi & sign-off
             ┌─────────▼───────────┐
             │    SQA Lead         │
             │  (Ketua Tim)        │
             └───┬────────────┬────┘
                 │            │
        ┌────────▼──┐   ┌────▼───────────┐
        │ Developer │   │    Tester      │
        │ + Knowledge│   │               │
        │  Engineer  │   │               │
        └────────────┘   └───────────────┘
```

### 2.2 Quality Gates dalam SDLC

Setiap Quality Gate memiliki **kriteria masuk** (entry criteria) dan **kriteria keluar** (exit criteria) yang wajib dipenuhi sebelum proyek berlanjut ke fase berikutnya.

---

#### Gate 1: Requirements Review ✅

| Aspek | Detail |
|---|---|
| **Tujuan** | Memvalidasi bahwa seluruh kebutuhan fungsional dan non-fungsional telah terdefinisi dengan jelas, lengkap, dan konsisten. |
| **Deliverable** | SRS v1.0 (IEEE 830), Project Charter v1.0 |
| **Reviewer** | SQA Lead + Dosen Pengampu |

**Checklist Komponen Sistem Pakar:**

| No | Item Review | Status |
|---|---|---|
| 1 | Semua 12 FR (FR-001 s/d FR-012) memiliki deskripsi, input, output, dan prioritas | ☐ |
| 2 | Metode inferensi sudah ditentukan: **Backward Chaining** (bukan Forward Chaining) | ☐ |
| 3 | Representasi pengetahuan sudah ditentukan: **Hybrid Rule-Frame** | ☐ |
| 4 | Skala CF User sudah didefinisikan: 5 level (0.0, 0.4, 0.6, 0.8, 1.0) | ☐ |
| 5 | Formula CF combine dan CF final sudah dinyatakan secara eksplisit | ☐ |
| 6 | Explanation Facility (Why & How) sudah menjadi FR tersendiri (FR-006, FR-007) | ☐ |
| 7 | Scope kerusakan (10) dan gejala (25) sudah final | ☐ |
| 8 | Traceability Matrix FR → UC lengkap (100% coverage) | ☐ |

**Exit Criteria:** Semua item checklist ☑, tidak ada TBD pada FR prioritas Tinggi.

---

#### Gate 2: Design Review ✅

| Aspek | Detail |
|---|---|
| **Tujuan** | Memvalidasi desain arsitektur, desain Knowledge Base, dan representasi pengetahuan sebelum implementasi dimulai. |
| **Deliverable** | UML Analysis v1.0, KB Design v1.0 (ISO 9075), Architecture Design v1.0 (IEEE 1016) |
| **Reviewer** | SQA Lead + Knowledge Engineer |

**Checklist Komponen Sistem Pakar:**

| No | Item Review | Status |
|---|---|---|
| 1 | **Validasi Frame:** 10 Frame (K01-K10) memiliki slot lengkap (kode, nama, penyebab, solusi, cf_pakar) | ☐ |
| 2 | **Validasi Rule:** 12 Rule (R1-R12) memiliki premis, konklusi, dan cf_rule yang konsisten | ☐ |
| 3 | **Validasi Gejala:** 25 Gejala (G01-G25) tidak ada duplikasi teks dan tidak ambigu | ☐ |
| 4 | **Konsistensi Rule → Frame:** Setiap konklusi rule merujuk ke kode_kerusakan yang valid | ☐ |
| 5 | **Konsistensi Rule → Gejala:** Setiap premis rule merujuk ke kode_gejala yang valid | ☐ |
| 6 | **No orphan Frame:** Setiap Frame memiliki minimal 1 Rule yang mengujinya | ☐ |
| 7 | **No orphan Gejala:** Setiap Gejala digunakan di minimal 1 Rule | ☐ |
| 8 | **No rule contradiction:** Tidak ada 2 rule dengan premis identik tetapi konklusi berbeda | ☐ |
| 9 | **Multi-rule correctness:** K08 memiliki 3 rule (R8, R11, R12) — CF combine antar-rule valid | ☐ |
| 10 | **Shared symptom identified:** G07 digunakan di R3 dan R5 — caching diperlukan | ☐ |
| 11 | **Arsitektur Layered 3-tier** sudah didefinisikan dan setiap layer memiliki tanggung jawab jelas | ☐ |
| 12 | **ADR-001 (Explanation Facility)** sudah disetujui: Trace Log pattern | ☐ |

**Exit Criteria:** Semua item ☑, desain Knowledge Base lolos validasi konsistensi 100%.

---

#### Gate 3: Code Review + Unit Test ✅

| Aspek | Detail |
|---|---|
| **Tujuan** | Memverifikasi kualitas kode dan **akurasi perhitungan Certainty Factor** melalui unit test otomatis. |
| **Deliverable** | Source code seluruh modul, laporan unit test, laporan coverage |
| **Reviewer** | SQA Lead + Developer (peer review) |

**Checklist Komponen Sistem Pakar:**

| No | Item Review | Status |
|---|---|---|
| 1 | Kode mengikuti standar **PEP 8** (diperiksa via `flake8` / `pylint`) | ☐ |
| 2 | Setiap fungsi publik memiliki **docstring** | ☐ |
| 3 | **Unit Test CF Calculator** lolos: | |
| | a. `combine_cf(0.8, 0.6)` = `0.92` | ☐ |
| | b. `combine_cf(0.92, 1.0)` = `1.0` | ☐ |
| | c. `calculate_final(0.90, [0.8, 0.6, 1.0])` = `0.90` | ☐ |
| | d. Edge case: semua CF user = 0.0 → hasil `0.0` | ☐ |
| | e. Edge case: CF user tunggal → `CF_final = cf_pakar × cf_user` | ☐ |
| | f. Combined multi-rule: `combine_cf(cf_R8, combine_cf(cf_R11, cf_R12))` | ☐ |
| 4 | **Unit Test Backward Chaining** lolos: | |
| | a. Hipotesis GAGAL jika satu premis = 0.0 (early termination) | ☐ |
| | b. Hipotesis TERBUKTI jika semua premis > 0.0 | ☐ |
| | c. Iterasi K01→K10 lengkap tanpa skip | ☐ |
| | d. Shared symptom (G07) tidak ditanyakan ulang | ☐ |
| | e. Multi-rule K08 mengevaluasi R8, R11, R12 secara berurutan | ☐ |
| 5 | **Unit Test Explanation Facility** lolos: | |
| | a. `why()` menghasilkan teks yang menyebut kode gejala, hipotesis, dan rule | ☐ |
| | b. `how()` menghasilkan langkah perhitungan CF yang benar | ☐ |
| 6 | **Unit Test Knowledge Base Integrity** lolos: | |
| | a. Semua kode_kerusakan di Rule merujuk ke Frame yang ada | ☐ |
| | b. Semua kode_gejala di Rule merujuk ke Gejala yang ada | ☐ |
| | c. Tidak ada duplikasi rule_id | ☐ |
| 7 | **Code coverage ≥ 80%** (diukur via `pytest-cov`) | ☐ |

**Exit Criteria:** Semua unit test PASS, coverage ≥ 80%, tidak ada defect severity Critical/High yang belum diperbaiki.

---

#### Gate 4: Integration Test ✅

| Aspek | Detail |
|---|---|
| **Tujuan** | Memastikan **alur Backward Chaining end-to-end** berjalan dari hipotesis pertama hingga seluruh hipotesis dievaluasi, tanpa infinite loop, tanpa crash, dan tanpa data loss. |
| **Deliverable** | Laporan integration test, laporan E2E test |
| **Reviewer** | SQA Lead + Tester |

**Checklist Komponen Sistem Pakar:**

| No | Item Review | Status |
|---|---|---|
| 1 | **Skenario E2E: Full Positive** | |
| | Jawab semua gejala K01 dengan CF > 0.0 → K01 muncul di hasil dengan CF benar | ☐ |
| 2 | **Skenario E2E: Full Negative** | |
| | Jawab semua gejala dengan CF = 0.0 → tidak ada kerusakan terbukti | ☐ |
| 3 | **Skenario E2E: Mixed** | |
| | K01 terbukti, K02 gagal, K04 terbukti → ranking K01 > K04 (jika CF K01 lebih tinggi) | ☐ |
| 4 | **Skenario E2E: Multi-Rule K08** | |
| | R8 gagal, R11 terbukti, R12 terbukti → K08 terbukti via R11+R12 combine | ☐ |
| 5 | **Skenario E2E: Shared Symptom G07** | |
| | G07 dijawab saat evaluasi K03 → saat evaluasi K05, G07 TIDAK ditanyakan ulang | ☐ |
| 6 | **No infinite loop:** Konsultasi selesai dalam waktu < 60 detik (10 hipotesis × max gejala) | ☐ |
| 7 | **Session state persistence:** Refresh halaman di tengah konsultasi → jawaban tidak hilang | ☐ |
| 8 | **Navigasi halaman:** Beranda → Konsultasi → Hasil → Konsultasi Ulang → Beranda | ☐ |
| 9 | **Explanation accuracy:** Teks "Mengapa?" dan "Bagaimana?" sesuai dengan rule dan CF aktual | ☐ |
| 10 | **Visualisasi:** Pohon inferensi ter-render tanpa error, node warna sesuai status) | ☐ |

**Exit Criteria:** Semua skenario E2E PASS, tidak ada infinite loop, session state stabil.

---

#### Gate 5: UAT Sign-off ✅

| Aspek | Detail |
|---|---|
| **Tujuan** | Mendapatkan persetujuan formal dari **Dosen Pengampu** bahwa prototype memenuhi kebutuhan akademik dan siap untuk dinilai/didemokan. |
| **Deliverable** | Prototype berjalan + dokumentasi lengkap |
| **Reviewer** | Dosen Pengampu (Product Owner) |

**Checklist UAT:**

| No | Item | Status |
|---|---|---|
| 1 | Prototype dapat dijalankan dengan `pip install -r requirements.txt && streamlit run app.py` | ☐ |
| 2 | Halaman Beranda informatif dan memiliki tombol "Mulai Konsultasi" | ☐ |
| 3 | Wizard konsultasi menampilkan pertanyaan step-by-step | ☐ |
| 4 | Skala CF User (5 level) berfungsi dan jelas labelnya | ☐ |
| 5 | Tombol "Mengapa?" menampilkan penjelasan yang relevan | ☐ |
| 6 | Hasil diagnosis menampilkan ranking dengan CF persentase | ☐ |
| 7 | Detail "Bagaimana?" menampilkan langkah perhitungan CF | ☐ |
| 8 | Pohon inferensi ter-visualisasi dengan warna hijau/merah | ☐ |
| 9 | Tombol "Konsultasi Ulang" mereset sesi dengan benar | ☐ |
| 10 | Dokumentasi teknis lengkap (SRS, UML, KB Design, SDD, SQAP) | ☐ |

**Exit Criteria:** Dosen Pengampu memberikan persetujuan tertulis (tanda tangan / approval).

---

## 3.0 Dokumentasi SQA

### 3.1 Daftar Dokumen

| Kode | Nama Dokumen | Dibuat Oleh | Direview Oleh | Jadwal |
|---|---|---|---|---|
| DOC-001 | Project Charter v1.0 | Ketua Tim | Dosen Pengampu | Minggu ke-0 ✅ |
| DOC-002 | SRS v1.0 (IEEE 830) | Ketua Tim | Dosen Pengampu | Minggu ke-0 ✅ |
| DOC-003 | UML Analysis v1.0 (UML 2.5) | Ketua Tim | SQA Lead | Minggu ke-0 ✅ |
| DOC-004 | Knowledge Base Design v1.0 (ISO 9075) | Knowledge Engineer | SQA Lead | Minggu ke-0 ✅ |
| DOC-005 | Architecture Design v1.0 (IEEE 1016) | Developer | SQA Lead | Minggu ke-0 ✅ |
| DOC-006 | **SQAP v1.0 (IEEE 730) — Dokumen ini** | SQA Lead | Dosen Pengampu | Minggu ke-0 ✅ |
| DOC-007 | Test Plan & Test Cases | Tester | SQA Lead | Minggu ke-1 |
| DOC-008 | Unit Test Report | Developer | SQA Lead | Minggu ke-1 |
| DOC-009 | Integration Test Report | Tester | SQA Lead | Minggu ke-2 |
| DOC-010 | Defect Log | Tester | SQA Lead | Minggu ke-1 – ke-3 |
| DOC-011 | UAT Sign-off Form | Tester | Dosen Pengampu | Minggu ke-3 |
| DOC-012 | Final Quality Report | SQA Lead | Dosen Pengampu | Minggu ke-3 |

### 3.2 Siklus Review Dokumen

```
Dokumen Dibuat → Internal Review (Peer) → Revisi → SQA Lead Review → Approval
       │                                                     │
       └── Jika ditolak, kembali ke revisi ──────────────────┘
```

---

## 4.0 Standar, Praktik & Konvensi

### 4.1 Coding Standard: PEP 8 (Python)

| Aspek | Konvensi | Contoh |
|---|---|---|
| **Variabel & fungsi** | `snake_case` | `combine_cf()`, `cf_user_list` |
| **Class** | `PascalCase` | `BackwardChainingEngine`, `ExplanationFacility` |
| **Konstanta** | `UPPER_SNAKE_CASE` | `FRAMES`, `RULES`, `RULES_BY_CONCLUSION` |
| **Modul / file** | `snake_case.py` | `backward_chaining.py`, `certainty_factor.py` |
| **Indentasi** | 4 spasi | — |
| **Line length** | Maks 120 karakter | — |
| **Docstring** | Google style / reStructuredText | Setiap fungsi publik wajib |
| **Import** | Urutan: stdlib → third-party → local | `import streamlit as st` |
| **Type hints** | Disarankan untuk fungsi publik | `def combine_cf(cf1: float, cf2: float) -> float:` |

### 4.2 Code Coverage

| Metrik | Target Minimum | Tool |
|---|---|---|
| **Line coverage** | ≥ **80%** | `pytest-cov` |
| **Branch coverage** | ≥ **70%** | `pytest-cov` |
| **Module coverage** | 100% modul engine/ dan knowledge_base/ | `pytest-cov` |

### 4.3 Tools Wajib

| Kategori | Tool | Versi | Kegunaan |
|---|---|---|---|
| **Unit Testing** | `pytest` | ≥ 7.0 | Framework testing utama Python |
| **Coverage** | `pytest-cov` | ≥ 4.0 | Mengukur code coverage |
| **Linting** | `flake8` | ≥ 6.0 | Memastikan kepatuhan PEP 8 |
| **Type Checking** | `mypy` (opsional) | ≥ 1.0 | Static type checking |
| **Formatting** | `black` (opsional) | ≥ 23.0 | Auto-formatter kode Python |
| **Browser Testing** | Manual / Streamlit testing | — | E2E testing via browser |

### 4.4 Perintah Testing Standar

```bash
# Unit test + coverage report
pytest tests/ -v --cov=engine --cov=knowledge_base --cov-report=term-missing

# Linting
flake8 engine/ knowledge_base/ ui/ --max-line-length=120

# Jalankan tes spesifik modul CF
pytest tests/test_certainty_factor.py -v

# Jalankan tes spesifik Backward Chaining
pytest tests/test_backward_chaining.py -v

# Jalankan tes integritas Knowledge Base
pytest tests/test_knowledge_base.py -v
```

---

## 5.0 Manajemen Defect

### 5.1 Siklus Hidup Defect

```
┌───────────┐     ┌────────────┐     ┌─────────────┐     ┌─────────┐
│    NEW     │────►│  ASSIGNED  │────►│ IN PROGRESS │────►│  FIXED  │
│            │     │            │     │             │     │         │
│ Tester     │     │ SQA Lead   │     │ Developer   │     │Developer│
│ menemukan  │     │ assign ke  │     │ memperbaiki │     │ commit  │
│ defect     │     │ developer  │     │ kode        │     │ fix     │
└───────────┘     └────────────┘     └─────────────┘     └────┬────┘
                                                               │
                        ┌──────────┐     ┌──────────────┐      │
                        │  CLOSED  │◄────│   VERIFIED   │◄─────┘
                        │          │     │              │
                        │ SQA Lead │     │ Tester       │
                        │ menutup  │     │ verifikasi   │
                        │ defect   │     │ fix berhasil │
                        └──────────┘     └──────────────┘
                              ▲                │
                              │    REOPEN      │ Jika fix gagal
                              └────────────────┘
```

### 5.2 Kategori Severity

| Level | Severity | Deskripsi | Contoh pada LaptopDoc | SLA Perbaikan |
|---|---|---|---|---|
| **S1** | **Critical** | Sistem crash / data loss / hasil diagnosis salah total | Backward Chaining infinite loop; CF final selalu 0.0 meskipun semua gejala terpenuhi | **< 4 jam** |
| **S2** | **High** | Fitur utama tidak berfungsi | Tombol "Mengapa?" tidak menampilkan penjelasan; ranking diagnosis tidak sorted; shared symptom ditanyakan ulang | **< 8 jam** |
| **S3** | **Medium** | Fitur berfungsi tetapi tidak sesuai spesifikasi | CF ditampilkan tanpa format persentase; progress bar tidak update; teks gejala terpotong | **< 24 jam** |
| **S4** | **Low** | Kosmetik / minor UX issue | Typo di teks gejala; spacing UI tidak rapi; warna node pohon inferensi kurang kontras | **< 48 jam** |

### 5.3 Template Laporan Defect

```
DEF-[NNN]
├── Judul         : [Deskripsi singkat defect]
├── Severity      : S1/S2/S3/S4
├── Status        : New/Assigned/In Progress/Fixed/Verified/Closed
├── Ditemukan oleh: [Nama]
├── Ditugaskan ke : [Nama]
├── Tanggal       : [DD/MM/YYYY]
├── Modul         : [engine/ui/knowledge_base/visualization]
├── Langkah Reproduksi:
│   1. [Langkah 1]
│   2. [Langkah 2]
│   3. [Langkah ...]
├── Hasil Aktual  : [Yang terjadi]
├── Hasil Diharapkan: [Yang seharusnya]
└── Bukti         : [Screenshot / log / test output]
```

---

## 6.0 Tinjauan & Audit

### 6.1 Proses Audit Kualitas Kode

| No | Aktivitas Audit | Frekuensi | Pelaksana | Metode |
|---|---|---|---|---|
| 1 | **Peer Code Review** | Setiap commit / PR | Developer (peer) | Manual review kode; fokus pada readability, error handling, dan kesesuaian PEP 8. |
| 2 | **Automated Linting** | Setiap commit | CI / Manual | `flake8` scan terhadap seluruh modul `engine/`, `knowledge_base/`, `ui/`. Zero violation policy. |
| 3 | **Unit Test Regression** | Setiap commit | Developer | `pytest` dijalankan sebelum push. Semua test harus PASS. |
| 4 | **Coverage Audit** | Setiap minggu | SQA Lead | Memastikan coverage ≥ 80%. Jika turun di bawah threshold, developer wajib menambah test. |
| 5 | **Knowledge Base Integrity Audit** | Sebelum Gate 2 & Gate 4 | Knowledge Engineer | Validasi silang: setiap Rule merujuk ke Frame dan Gejala yang valid. Tidak ada orphan. |
| 6 | **CF Calculation Spot Check** | Sebelum Gate 3 | SQA Lead | Hitung manual CF untuk 3 skenario, bandingkan dengan output sistem. Deviasi = 0. |
| 7 | **Final Quality Audit** | Sebelum Gate 5 | SQA Lead | Review menyeluruh: semua test PASS, coverage tercapai, defect critical/high = 0, dokumentasi lengkap. |

### 6.2 Alur Audit

```
                   ┌──────────────────────┐
                   │   1. Jadwalkan Audit  │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  2. Kumpulkan Artefak │
                   │  (kode, test, report) │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  3. Evaluasi terhadap │
                   │     standar & target  │
                   └──────────┬───────────┘
                              │
               ┌──────────────┼──────────────┐
               │                             │
      ┌────────▼────────┐          ┌─────────▼────────┐
      │ 4a. LOLOS       │          │ 4b. TIDAK LOLOS  │
      │ → Lanjut ke     │          │ → Catat temuan   │
      │   gate berikut  │          │ → Buat action    │
      └─────────────────┘          │   items          │
                                   │ → Re-audit       │
                                   └──────────────────┘
```

---

## 7.0 Risiko Kualitas

### 7.1 Daftar Risiko

| ID | Risiko | Kategori | Prob. | Dampak | Skor | Mitigasi |
|---|---|---|---|---|---|---|
| **RQ-01** | **Kesalahan pembobotan CF pakar yang menyebabkan misdiagnosis** — Bobot CF_rule yang tidak akurat menyebabkan sistem memberikan diagnosis dengan urutan ranking yang salah, menghasilkan rekomendasi solusi yang tidak tepat. | 🔬 **Sistem Pakar** | Sedang | **Tinggi** | **8** | Validasi bobot CF dengan literatur teknis. Uji dengan minimal 5 skenario realistis. Spot check manual: hitung CF tangan vs output sistem. Toleransi deviasi = 0.0 (harus identik). |
| **RQ-02** | **Rule yang saling bertentangan atau redundan** — Dua rule dengan premis identik atau sangat mirip mengarah ke konklusi berbeda, menyebabkan ambiguitas diagnosis. Atau rule redundan yang tidak memberikan value tambahan. | 🔬 **Sistem Pakar** | Rendah | **Tinggi** | **6** | Audit Knowledge Base di Gate 2: cross-check setiap rule. Pastikan setiap kombinasi premis unik. Dokumentasikan shared symptom (G07) dan justifikasinya. |
| **RQ-03** | **Backward Chaining infinite loop atau deadlock** — Bug pada algoritma menyebabkan engine tidak pernah selesai mengevaluasi hipotesis, sehingga konsultasi tidak bisa diselesaikan. | Logika Engine | Rendah | **Critical** | **7** | Implementasi counter / timeout: maks 10 hipotesis × maks premis per rule. Unit test untuk memvalidasi terminasi. Integration test skenario worst-case (semua gejala dijawab). |
| **RQ-04** | **Session state Streamlit hilang di tengah konsultasi** — User kehilangan progress jika Streamlit melakukan rerun otomatis atau koneksi WebSocket terputus. | Web Framework | Sedang | Sedang | **6** | Simpan semua state di `st.session_state`. Hindari operasi yang memicu full rerun. Test: refresh halaman di tengah konsultasi → state harus bertahan. |
| **RQ-05** | **Library Graphviz gagal diinstal / render error** — Graphviz memerlukan binary sistem yang mungkin tidak ada di environment tertentu, menyebabkan visualisasi pohon inferensi crash. | Dependency | Sedang | Sedang | **5** | Implementasi fallback: jika `graphviz` tidak tersedia, tampilkan representasi teks pohon inferensi. Sediakan instruksi instalasi di README. |
| **RQ-06** | **Gejala ambigu menyebabkan jawaban user tidak akurat** — Teks gejala tidak cukup jelas sehingga user bingung membedakan gejala yang mirip, menghasilkan CF User yang tidak merepresentasikan kondisi sebenarnya. | UX / KB | Tinggi | Sedang | **7** | Review teks gejala di Gate 2 oleh minimal 2 orang non-teknis. Tambahkan `deskripsi_detail` (tooltip) untuk setiap gejala. UAT: minta 3 user mencoba dan kumpulkan feedback. |
| **RQ-07** | **Code coverage di bawah target 80%** — Developer fokus pada fitur sehingga mengabaikan penulisan unit test, menyebabkan bug lolos ke production. | Proses | Sedang | Sedang | **5** | Enforce coverage check di setiap Gate 3. SQA Lead melakukan coverage audit mingguan. Blokir rilis jika coverage < 80%. |

### 7.2 Matriks Risiko

```
              ┌───────────────────────────────────────────────┐
              │               DAMPAK                          │
              │   Rendah    │   Sedang    │   Tinggi/Critical │
 ┌────────────┼─────────────┼─────────────┼───────────────────┤
 │ Tinggi     │             │   RQ-06     │                   │
 │            │             │             │                   │
P├────────────┼─────────────┼─────────────┼───────────────────┤
R│ Sedang     │             │  RQ-04      │  ★ RQ-01          │
O│            │             │  RQ-05      │                   │
B├────────────┼─────────────┼─────────────┼───────────────────┤
 │ Rendah     │             │  RQ-07      │  RQ-02            │
 │            │             │             │  RQ-03            │
 └────────────┴─────────────┴─────────────┴───────────────────┘
 
 ★ = Risiko prioritas tertinggi
```

---

## 8.0 Metrik yang Diukur

### 8.1 Definisi Metrik

| No | Metrik | Formula | Target | Kapan Diukur |
|---|---|---|---|---|
| 1 | **Code Coverage (%)** | `(Baris kode yang dieksekusi oleh test / Total baris kode) × 100` | **≥ 80%** | Setiap commit; audit mingguan |
| 2 | **Defect Density (bug/KLOC)** | `(Jumlah defect ditemukan / Ukuran kode dalam KLOC) × 1000` | **≤ 10 bug/KLOC** | Setelah Gate 3 dan Gate 4 |
| 3 | **Defect Removal Efficiency / DRE (%)** | `(Defect ditemukan sebelum rilis / Total defect termasuk post-rilis) × 100` | **≥ 90%** | Setelah Gate 5 (UAT) |
| 4 | **Mean Time To Repair / MTTR (jam)** | `Total waktu perbaikan semua defect / Jumlah defect yang diperbaiki` | **≤ 8 jam** (rata-rata) | Dihitung dari defect log |
| 5 | **Test Pass Rate (%)** | `(Jumlah test case PASS / Total test case yang dijalankan) × 100` | **100%** saat rilis | Setiap test run |

### 8.2 Dashboard Metrik (Template)

```
╔══════════════════════════════════════════════════════════════════════╗
║                  QUALITY METRICS DASHBOARD — LaptopDoc              ║
║                  Snapshot: [Tanggal]                                ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. CODE COVERAGE                                                    ║
║     ┌──────────────────────────────────────┐                        ║
║     │ engine/              [████████░░] 85%│  ← Target: ≥ 80%      ║
║     │ knowledge_base/      [██████████] 98%│                        ║
║     │ ui/                  [██████░░░░] 62%│  ← Perlu ditingkatkan ║
║     │ visualization/       [████████░░] 78%│                        ║
║     │ ─────────────────────────────────────│                        ║
║     │ Overall:             [████████░░] 81%│  ✅ LOLOS              ║
║     └──────────────────────────────────────┘                        ║
║                                                                      ║
║  2. DEFECT DENSITY                                                   ║
║     Total defects: [N] | KLOC: [M] | Density: [N/M] bug/KLOC       ║
║     Target: ≤ 10 bug/KLOC | Status: [✅/❌]                         ║
║                                                                      ║
║  3. DEFECT REMOVAL EFFICIENCY (DRE)                                  ║
║     Pre-release defects: [A] | Post-release: [B]                    ║
║     DRE: A / (A + B) × 100 = [X]%                                   ║
║     Target: ≥ 90% | Status: [✅/❌]                                  ║
║                                                                      ║
║  4. MEAN TIME TO REPAIR (MTTR)                                       ║
║     Total repair hours: [H] | Defects fixed: [F]                    ║
║     MTTR: H / F = [Y] jam                                            ║
║     Target: ≤ 8 jam | Status: [✅/❌]                                ║
║                                                                      ║
║  5. TEST PASS RATE                                                   ║
║     Unit tests:        [P1]/[T1] = [X1]%                            ║
║     Integration tests: [P2]/[T2] = [X2]%                            ║
║     E2E tests:         [P3]/[T3] = [X3]%                            ║
║     ─────────────────────────────────────                            ║
║     Overall:           [PT]/[TT] = [XT]%                            ║
║     Target: 100% saat rilis | Status: [✅/❌]                       ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  DEFECT SUMMARY BY SEVERITY                                         ║
║  ┌──────────┬──────┬────────┬─────────┬──────────┬────────┐         ║
║  │ Severity │ New  │Assigned│In Progr.│  Fixed   │ Closed │         ║
║  ├──────────┼──────┼────────┼─────────┼──────────┼────────┤         ║
║  │ Critical │  0   │   0    │    0    │    0     │   0    │         ║
║  │ High     │  0   │   0    │    0    │    0     │   0    │         ║
║  │ Medium   │  0   │   0    │    0    │    0     │   0    │         ║
║  │ Low      │  0   │   0    │    0    │    0     │   0    │         ║
║  └──────────┴──────┴────────┴─────────┴──────────┴────────┘         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 8.3 Jadwal Pengukuran

| Gate | Metrik yang Diukur | Threshold Kelulusan |
|---|---|---|
| Gate 3 (Code Review) | Code Coverage, Test Pass Rate | Coverage ≥ 80%, Pass Rate = 100% |
| Gate 4 (Integration) | Test Pass Rate, Defect Density | Pass Rate = 100%, Density ≤ 10 |
| Gate 5 (UAT) | DRE, MTTR, Open Critical/High | DRE ≥ 90%, MTTR ≤ 8, Critical/High = 0 |

---

> *Dokumen SQAP ini disusun berdasarkan standar IEEE 730-2014 untuk proyek LaptopDoc — Sistem Pakar Diagnosis Kerusakan Laptop. Quality Gates disesuaikan untuk mencakup validasi komponen Sistem Pakar (Knowledge Base, Inference Engine, Certainty Factor). Versi 1.0 — Maret 2026.*
