# DOKUMEN DESAIN BASIS PENGETAHUAN
## Sistem Pakar Diagnosis Kerusakan Laptop — LaptopDoc
### Knowledge Representation & Data Architecture

**Standar Acuan:** ISO/IEC 9075 (SQL Standard) — Adaptasi untuk Knowledge Base Sistem Pakar

| Item | Detail |
|---|---|
| **Versi** | 1.0 |
| **Tanggal** | 28 Maret 2026 |
| **Status** | Final |
| **Dokumen Referensi** | SRS v1.0, UML Analysis v1.0, Project Charter v1.0 |

---

## 1. ERD / Knowledge Representation (Format Tekstual)

### 1.1 Identifikasi Entitas

Sistem pakar LaptopDoc memiliki **4 entitas utama** yang merepresentasikan komponen Knowledge Base:

| No | Entitas | Peran dalam Sistem Pakar | Jumlah Record |
|---|---|---|---|
| 1 | **Frame Kerusakan** | Representasi deklaratif/faktual — menyimpan data kerusakan laptop | 10 (K01–K10) |
| 2 | **Gejala** | Premis/fakta yang ditanyakan kepada pengguna selama konsultasi | 25 (G01–G25) |
| 3 | **Rule** | Representasi prosedural — logika IF-THEN Backward Chaining | 12 (R1–R12) |
| 4 | **Rule Premis** | Tabel jembatan (junction) yang menghubungkan Rule ke Gejala | 30 relasi |

### 1.2 Diagram ER — Tekstual

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE BASE — ERD DIAGRAM                         │
└──────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────┐         ┌──────────────────────────┐
  │   FRAME_KERUSAKAN     │         │          GEJALA           │
  │  (Entitas Kuat)       │         │    (Entitas Kuat)         │
  ├───────────────────────┤         ├──────────────────────────┤
  │ PK kode_kerusakan     │         │ PK kode_gejala            │
  │    nama_kerusakan     │         │    teks_gejala            │
  │    penyebab           │         │    deskripsi_detail       │
  │    solusi_singkat      │         │    kategori               │
  │    solusi_detail       │         └──────────┬───────────────┘
  │    cf_pakar            │                    │
  └──────────┬────────────┘                    │
             │                                 │
             │ 1                            N  │
             │                                 │
             │        ┌──────────────────┐     │
             │        │      RULE         │     │
             │        │ (Entitas Kuat)    │     │
             │        ├──────────────────┤     │
             └───────►│ PK rule_id        │     │
              N    1  │    kode_kerusakan │     │
                      │    cf_rule        │     │
           (konklusi) │    deskripsi_rule │     │
                      └────────┬─────────┘     │
                               │               │
                               │ 1             │
                               │               │
                      ┌────────▼───────────┐   │
                      │   RULE_PREMIS      │   │
                      │ (Tabel Jembatan)   │   │
                      ├────────────────────┤   │
                      │ PK,FK rule_id      ├───┘
                      │ PK,FK kode_gejala  │  N
                      │     urutan_premis  │
                      └────────────────────┘
```

### 1.3 Penjelasan Relasi

| Relasi | Kardinalitas | Deskripsi |
|---|---|---|
| **FRAME_KERUSAKAN → RULE** | `1 : N` | Satu kerusakan **dapat** dibuktikan oleh 1 atau lebih rule. Contoh: K08 (Motherboard) memiliki 3 rule (R8, R11, R12). |
| **RULE → RULE_PREMIS** | `1 : N` | Satu rule memiliki 1 atau lebih premis/gejala. Contoh: R1 memiliki 3 premis (G01, G02, G18). |
| **GEJALA → RULE_PREMIS** | `1 : N` | Satu gejala **dapat** digunakan di beberapa rule sekaligus. Contoh: G07 digunakan di R3 (K03) dan R5 (K05). |
| **RULE ↔ GEJALA** | `N : M` (via RULE_PREMIS) | Relasi many-to-many antara rule dan gejala, dihubungkan melalui tabel jembatan `RULE_PREMIS`. |

### 1.4 Pemetaan Relasi Rule → Kerusakan (Backward Chaining)

Diagram berikut menunjukkan bagaimana Rule menghubungkan Gejala ke Kerusakan dalam konteks Backward Chaining:

```
HIPOTESIS (Goal)          RULE (IF-THEN)              PREMIS (Gejala)
═══════════════          ═══════════════             ═══════════════════

K01 (Adaptor)    ◄────── R1  [CF=0.90] ◄──── G01 ∧ G02 ∧ G18

K02 (Baterai)    ◄────── R2  [CF=0.85] ◄──── G03 ∧ G04 ∧ G05

K03 (RAM)        ◄────── R3  [CF=0.80] ◄──── G06 ∧ G07*

K04 (Overheating)◄────── R4  [CF=0.88] ◄──── G08 ∧ G09 ∧ G10

K05 (LCD)        ◄────── R5  [CF=0.82] ◄──── G07* ∧ G16 ∧ G17

K06 (HDD/SSD)    ◄────── R6  [CF=0.84] ◄──── G11 ∧ G12 ∧ G13

K07 (Keyboard)   ◄────── R7  [CF=0.78] ◄──── G14 ∧ G15

                ┌─ R8  [CF=0.75] ◄──── G19 ∧ G20 ∧ G21
K08 (Motherboard)◄─┤
                ├─ R11 [CF=0.70] ◄──── G24
                └─ R12 [CF=0.68] ◄──── G25

K09 (Touchpad)   ◄────── R9  [CF=0.76] ◄──── G22

K10 (WiFi)       ◄────── R10 [CF=0.74] ◄──── G23

* G07 = gejala bersama (shared symptom), digunakan di R3 dan R5
```

> **Catatan Backward Chaining:** Arah panah menunjukkan alur *inferensi*, bukan alur *data*. Engine memulai dari HIPOTESIS (kanan ke kiri pada diagram konvensional), mencari RULE yang konklusinya = hipotesis tersebut, lalu menanyakan PREMIS/gejala kepada pengguna.

---

## 2. Kamus Data (Data Dictionary)

### 2.1 Entitas: `frame_kerusakan`

Menyimpan data faktual (deklaratif) kerusakan laptop dalam format Frame.

| No | Nama Field | Tipe Data | Ukuran | Null? | Key | Keterangan |
|---|---|---|---|---|---|---|
| 1 | `kode_kerusakan` | `VARCHAR` | 3 | NOT NULL | **PK** | Kode unik kerusakan, format: `Knn` (K01–K10) |
| 2 | `nama_kerusakan` | `VARCHAR` | 100 | NOT NULL | — | Nama deskriptif kerusakan laptop |
| 3 | `penyebab` | `TEXT` | — | NOT NULL | — | Penyebab utama terjadinya kerusakan |
| 4 | `solusi_singkat` | `VARCHAR` | 200 | NOT NULL | — | Rekomendasi solusi ringkas (ditampilkan di card hasil) |
| 5 | `solusi_detail` | `TEXT` | — | NULL | — | Penjelasan solusi lebih lengkap (ditampilkan di expander) |
| 6 | `cf_pakar` | `DECIMAL(3,2)` | — | NOT NULL | — | Nilai Certainty Factor pakar untuk kerusakan ini, range: `0.00–1.00`. Merepresentasikan keyakinan pakar terhadap validitas diagnosis. |
| 7 | `kategori` | `VARCHAR` | 50 | NULL | — | Kategori kerusakan (daya, komponen, storage, periferal, konektivitas) |

**Constraint:**
- `CHECK (cf_pakar >= 0.00 AND cf_pakar <= 1.00)`
- `CHECK (kode_kerusakan LIKE 'K__')`

### 2.2 Entitas: `gejala`

Menyimpan data gejala yang ditanyakan kepada pengguna selama konsultasi.

| No | Nama Field | Tipe Data | Ukuran | Null? | Key | Keterangan |
|---|---|---|---|---|---|---|
| 1 | `kode_gejala` | `VARCHAR` | 3 | NOT NULL | **PK** | Kode unik gejala, format: `Gnn` (G01–G25) |
| 2 | `teks_gejala` | `VARCHAR` | 200 | NOT NULL | — | Teks pertanyaan gejala yang ditampilkan ke pengguna |
| 3 | `deskripsi_detail` | `TEXT` | — | NULL | — | Penjelasan tambahan / tooltip untuk memperjelas gejala |
| 4 | `kategori` | `VARCHAR` | 50 | NULL | — | Kategori gejala (daya, visual, performa, input, konektivitas) |

**Constraint:**
- `CHECK (kode_gejala LIKE 'G__')`

### 2.3 Entitas: `rule`

Menyimpan logika inferensi IF-THEN untuk Backward Chaining.

| No | Nama Field | Tipe Data | Ukuran | Null? | Key | Keterangan |
|---|---|---|---|---|---|---|
| 1 | `rule_id` | `VARCHAR` | 3 | NOT NULL | **PK** | ID unik rule, format: `Rn` atau `Rnn` (R1–R12) |
| 2 | `kode_kerusakan` | `VARCHAR` | 3 | NOT NULL | **FK** | Kode kerusakan yang menjadi konklusi rule → referensi ke `frame_kerusakan.kode_kerusakan` |
| 3 | `cf_rule` | `DECIMAL(3,2)` | — | NOT NULL | — | Nilai CF pakar spesifik untuk rule ini, range: `0.00–1.00`. Bisa berbeda dengan `cf_pakar` pada frame jika rule merepresentasikan jalur pembuktian parsial. |
| 4 | `deskripsi_rule` | `TEXT` | — | NULL | — | Deskripsi tekstual rule dalam format IF-THEN (untuk Explanation Facility) |

**Constraint:**
- `FOREIGN KEY (kode_kerusakan) REFERENCES frame_kerusakan(kode_kerusakan)`
- `CHECK (cf_rule >= 0.00 AND cf_rule <= 1.00)`

### 2.4 Entitas: `rule_premis`

Tabel jembatan (junction table) yang menghubungkan rule ke gejala-gejala premisnya.

| No | Nama Field | Tipe Data | Ukuran | Null? | Key | Keterangan |
|---|---|---|---|---|---|---|
| 1 | `rule_id` | `VARCHAR` | 3 | NOT NULL | **PK, FK** | ID rule → referensi ke `rule.rule_id` |
| 2 | `kode_gejala` | `VARCHAR` | 3 | NOT NULL | **PK, FK** | Kode gejala premis → referensi ke `gejala.kode_gejala` |
| 3 | `urutan_premis` | `INTEGER` | — | NOT NULL | — | Urutan evaluasi premis dalam rule (1, 2, 3, ...) |

**Constraint:**
- `PRIMARY KEY (rule_id, kode_gejala)` — composite key
- `FOREIGN KEY (rule_id) REFERENCES rule(rule_id)`
- `FOREIGN KEY (kode_gejala) REFERENCES gejala(kode_gejala)`
- `CHECK (urutan_premis > 0)`

### 2.5 Entitas: `sesi_konsultasi` (Session-based / Runtime)

Data runtime yang disimpan di session state selama konsultasi berlangsung.

| No | Nama Field | Tipe Data | Ukuran | Null? | Key | Keterangan |
|---|---|---|---|---|---|---|
| 1 | `session_id` | `VARCHAR` | 36 | NOT NULL | **PK** | UUID unik per sesi konsultasi |
| 2 | `waktu_mulai` | `DATETIME` | — | NOT NULL | — | Timestamp awal sesi konsultasi |
| 3 | `waktu_selesai` | `DATETIME` | — | NULL | — | Timestamp akhir sesi (null jika belum selesai) |
| 4 | `status` | `VARCHAR` | 20 | NOT NULL | — | Status sesi: `berlangsung`, `selesai` |

### 2.6 Entitas: `jawaban_konsultasi` (Session-based / Runtime)

Menyimpan jawaban CF User per gejala selama sesi konsultasi.

| No | Nama Field | Tipe Data | Ukuran | Null? | Key | Keterangan |
|---|---|---|---|---|---|---|
| 1 | `session_id` | `VARCHAR` | 36 | NOT NULL | **PK, FK** | Referensi ke `sesi_konsultasi.session_id` |
| 2 | `kode_gejala` | `VARCHAR` | 3 | NOT NULL | **PK, FK** | Kode gejala yang dijawab → referensi ke `gejala.kode_gejala` |
| 3 | `cf_user` | `DECIMAL(2,1)` | — | NOT NULL | — | Nilai CF User, valid: `0.0, 0.4, 0.6, 0.8, 1.0` |
| 4 | `waktu_jawab` | `DATETIME` | — | NOT NULL | — | Timestamp saat gejala dijawab |

**Constraint:**
- `CHECK (cf_user IN (0.0, 0.4, 0.6, 0.8, 1.0))`

### 2.7 Entitas: `hasil_diagnosis` (Session-based / Runtime)

Menyimpan hasil diagnosis per kerusakan per sesi.

| No | Nama Field | Tipe Data | Ukuran | Null? | Key | Keterangan |
|---|---|---|---|---|---|---|
| 1 | `session_id` | `VARCHAR` | 36 | NOT NULL | **PK, FK** | Referensi ke `sesi_konsultasi.session_id` |
| 2 | `kode_kerusakan` | `VARCHAR` | 3 | NOT NULL | **PK, FK** | Referensi ke `frame_kerusakan.kode_kerusakan` |
| 3 | `status_hipotesis` | `VARCHAR` | 10 | NOT NULL | — | Status: `TERBUKTI` atau `GAGAL` |
| 4 | `cf_final` | `DECIMAL(4,3)` | — | NOT NULL | — | Nilai CF final hasil kalkulasi, range: `0.000–1.000` |
| 5 | `ranking` | `INTEGER` | — | NULL | — | Posisi ranking berdasarkan CF final (1 = tertinggi) |

---

## 3. Strategi Implementasi Knowledge Base

### 3.1 Analisis Opsi Penyimpanan

| Kriteria | JSON/Dict (Python) | SQLite | PostgreSQL |
|---|---|---|---|
| **Kecepatan akses** | ⚡ Sangat cepat (in-memory) | 🔶 Cepat (file-based) | 🔶 Cepat (server-based) |
| **Kompleksitas setup** | ✅ Zero-config | 🔶 Minimal (1 file) | ❌ Perlu server |
| **Cocok untuk prototype** | ✅ Ideal | 🔶 Cukup | ❌ Berlebihan |
| **Query relasional** | ❌ Manual lookup | ✅ SQL native | ✅ SQL native |
| **Portabilitas** | ✅ Copy-paste code | ✅ 1 file .db | ❌ Perlu install |
| **Kalkulasi CF runtime** | ✅ Langsung compute | 🔶 Perlu fetch dulu | 🔶 Perlu fetch dulu |
| **Demo readiness** | ✅ `streamlit run app.py` | ✅ Otomatis load | ❌ Perlu setup DB |
| **Ukuran data (10K+25G+12R)** | ✅ < 5 KB | 🔶 Overkill | ❌ Overkill |

### 3.2 Rekomendasi: Python Dictionary (In-Memory)

> **Keputusan:** Gunakan **Python Dictionary / List of Dictionaries** sebagai format penyimpanan Knowledge Base.

**Justifikasi:**

1. **Performa kalkulasi CF sangat cepat** — Data sudah berada di RAM, tidak ada I/O overhead. Operasi lookup `dict[key]` memiliki kompleksitas O(1).

2. **Dataset sangat kecil** — 10 frame + 25 gejala + 12 rule = total < 50 record. Menggunakan RDBMS untuk dataset sekecil ini justru menambah overhead tanpa manfaat.

3. **Zero-configuration** — Sesuai NFR-012 pada SRS: *"Sistem dapat dijalankan hanya dengan `pip install -r requirements.txt` dan `streamlit run app.py` tanpa konfigurasi tambahan."*

4. **Akses data deterministik** — Backward Chaining memerlukan traversal urut (K01→K10) dan lookup rule berdasarkan konklusi. Keduanya mudah dilakukan dengan dictionary.

5. **Streamlit session state native** — Data runtime (jawaban user, status hipotesis) disimpan di `st.session_state` yang sudah berbasis dictionary.

### 3.3 Arsitektur Penyimpanan

```
┌────────────────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE BASE ARCHITECTURE                         │
│                                                                        │
│  ┌─── STATIC DATA (Hardcoded Python) ──────────────────────────────┐  │
│  │                                                                  │  │
│  │  knowledge_base/                                                 │  │
│  │  ├── frames.py      → FRAMES: Dict[str, FrameDict]             │  │
│  │  │                     Key = kode_kerusakan ("K01"..."K10")     │  │
│  │  │                     Value = {nama, penyebab, solusi, cf}     │  │
│  │  │                                                               │  │
│  │  ├── symptoms.py    → SYMPTOMS: Dict[str, SymptomDict]         │  │
│  │  │                     Key = kode_gejala ("G01"..."G25")        │  │
│  │  │                     Value = {teks, deskripsi, kategori}      │  │
│  │  │                                                               │  │
│  │  └── rules.py       → RULES: List[RuleDict]                    │  │
│  │                        Setiap item = {rule_id, premis[], konklusi, cf}│
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
│  ┌─── RUNTIME DATA (Streamlit Session State) ──────────────────────┐  │
│  │                                                                  │  │
│  │  st.session_state["engine"]     → Instance BackwardChainingEngine│  │
│  │  st.session_state["answers"]    → {kode_gejala: cf_user}       │  │
│  │  st.session_state["results"]    → [{kode_kerusakan, cf_final}] │  │
│  │  st.session_state["history"]    → [list of past sessions]      │  │
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Strategi Optimasi Kalkulasi CF

| Strategi | Implementasi |
|---|---|
| **Pre-indexed rule lookup** | Dictionary `RULES_BY_CONCLUSION: Dict[str, List[RuleDict]]` — key = `kode_kerusakan`, value = list of rules. Lookup instant O(1). |
| **Cached symptom answers** | `st.session_state["answers"]` menyimpan semua jawaban. Jika gejala sudah pernah dijawab (shared symptom G07), gunakan cache tanpa bertanya ulang. |
| **Early termination** | Jika `cf_user == 0.0` pada premis manapun → langsung skip hipotesis, tanpa menghitung CF combine. |
| **Lazy CF combine** | CF combine dihitung hanya setelah **semua premis terpenuhi**, bukan per-premis. |

---

## 4. Schema Definisi — DDL & JSON Schema

### 4.1 DDL (SQL — Referensi Akademik)

Meskipun implementasi menggunakan Python Dictionary, DDL berikut disediakan sebagai **referensi formal** sesuai standar ISO/IEC 9075 dan untuk keperluan dokumentasi akademik.

```sql
-- ============================================================
-- DDL: LaptopDoc Knowledge Base
-- Standar: ISO/IEC 9075 (SQL:2016)
-- Catatan: DDL referensi akademik, implementasi via Python Dict
-- ============================================================

-- -----------------------------------------------------------
-- TABEL 1: Frame Kerusakan (Representasi Deklaratif)
-- Menyimpan data faktual kerusakan laptop
-- -----------------------------------------------------------
CREATE TABLE frame_kerusakan (
    kode_kerusakan   VARCHAR(3)      NOT NULL,
    nama_kerusakan   VARCHAR(100)    NOT NULL,
    penyebab         TEXT            NOT NULL,
    solusi_singkat    VARCHAR(200)    NOT NULL,
    solusi_detail     TEXT            DEFAULT NULL,
    cf_pakar         DECIMAL(3,2)    NOT NULL,
    kategori         VARCHAR(50)     DEFAULT NULL,

    -- Constraint
    CONSTRAINT pk_frame_kerusakan PRIMARY KEY (kode_kerusakan),
    CONSTRAINT chk_kode_kerusakan CHECK (kode_kerusakan LIKE 'K__'),
    CONSTRAINT chk_cf_pakar       CHECK (cf_pakar >= 0.00 AND cf_pakar <= 1.00)
);

-- -----------------------------------------------------------
-- TABEL 2: Gejala (Premis Backward Chaining)
-- Menyimpan data gejala yang ditanyakan ke pengguna
-- -----------------------------------------------------------
CREATE TABLE gejala (
    kode_gejala      VARCHAR(3)      NOT NULL,
    teks_gejala      VARCHAR(200)    NOT NULL,
    deskripsi_detail TEXT            DEFAULT NULL,
    kategori         VARCHAR(50)     DEFAULT NULL,

    -- Constraint
    CONSTRAINT pk_gejala           PRIMARY KEY (kode_gejala),
    CONSTRAINT chk_kode_gejala     CHECK (kode_gejala LIKE 'G__')
);

-- -----------------------------------------------------------
-- TABEL 3: Rule (Representasi Prosedural IF-THEN)
-- Menyimpan logika inferensi Backward Chaining
-- -----------------------------------------------------------
CREATE TABLE rule (
    rule_id          VARCHAR(3)      NOT NULL,
    kode_kerusakan   VARCHAR(3)      NOT NULL,
    cf_rule          DECIMAL(3,2)    NOT NULL,
    deskripsi_rule   TEXT            DEFAULT NULL,

    -- Constraint
    CONSTRAINT pk_rule             PRIMARY KEY (rule_id),
    CONSTRAINT fk_rule_kerusakan   FOREIGN KEY (kode_kerusakan)
                                   REFERENCES frame_kerusakan(kode_kerusakan)
                                   ON DELETE CASCADE
                                   ON UPDATE CASCADE,
    CONSTRAINT chk_cf_rule         CHECK (cf_rule >= 0.00 AND cf_rule <= 1.00)
);

-- -----------------------------------------------------------
-- TABEL 4: Rule Premis (Junction Table)
-- Menghubungkan Rule dengan Gejala (relasi many-to-many)
-- -----------------------------------------------------------
CREATE TABLE rule_premis (
    rule_id          VARCHAR(3)      NOT NULL,
    kode_gejala      VARCHAR(3)      NOT NULL,
    urutan_premis    INTEGER         NOT NULL,

    -- Constraint
    CONSTRAINT pk_rule_premis      PRIMARY KEY (rule_id, kode_gejala),
    CONSTRAINT fk_premis_rule      FOREIGN KEY (rule_id)
                                   REFERENCES rule(rule_id)
                                   ON DELETE CASCADE,
    CONSTRAINT fk_premis_gejala    FOREIGN KEY (kode_gejala)
                                   REFERENCES gejala(kode_gejala)
                                   ON DELETE CASCADE,
    CONSTRAINT chk_urutan          CHECK (urutan_premis > 0)
);

-- -----------------------------------------------------------
-- INDEX untuk optimasi query Backward Chaining
-- -----------------------------------------------------------
CREATE INDEX idx_rule_konklusi   ON rule(kode_kerusakan);
CREATE INDEX idx_premis_rule     ON rule_premis(rule_id);
CREATE INDEX idx_premis_gejala   ON rule_premis(kode_gejala);
```

---

### 4.2 JSON Schema — Implementasi Aktual (Python Dictionary)

Schema berikut mendefinisikan struktur data yang diimplementasikan dalam kode Python.

#### 4.2.1 Schema: Frame Kerusakan (`frames.py`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "laptopdoc/frame_kerusakan",
  "title": "Frame Kerusakan Laptop",
  "description": "Schema untuk representasi Frame (slot-based) kerusakan laptop K01-K10",
  "type": "object",
  "patternProperties": {
    "^K(0[1-9]|10)$": {
      "type": "object",
      "properties": {
        "kode_kerusakan": {
          "type": "string",
          "pattern": "^K(0[1-9]|10)$",
          "description": "Kode unik kerusakan"
        },
        "nama_kerusakan": {
          "type": "string",
          "maxLength": 100,
          "description": "Nama deskriptif kerusakan"
        },
        "penyebab": {
          "type": "string",
          "description": "Penyebab utama kerusakan"
        },
        "solusi_singkat": {
          "type": "string",
          "maxLength": 200,
          "description": "Solusi ringkas untuk tampilan card"
        },
        "solusi_detail": {
          "type": "string",
          "description": "Penjelasan solusi lengkap"
        },
        "cf_pakar": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "description": "Certainty Factor pakar (0.00-1.00)"
        },
        "kategori": {
          "type": "string",
          "enum": ["daya", "komponen", "storage", "periferal", "konektivitas"],
          "description": "Kategori kerusakan"
        }
      },
      "required": ["kode_kerusakan", "nama_kerusakan", "penyebab", "solusi_singkat", "cf_pakar"]
    }
  },
  "additionalProperties": false
}
```

**Contoh Data:**

```python
# knowledge_base/frames.py

FRAMES = {
    "K01": {
        "kode_kerusakan": "K01",
        "nama_kerusakan": "Adaptor/charger rusak",
        "penyebab": "Suplai daya adaptor tidak stabil atau kabel rusak",
        "solusi_singkat": "Periksa output adaptor, coba charger lain",
        "solusi_detail": "1. Periksa lampu indikator adaptor.\n"
                         "2. Coba gunakan adaptor/charger lain yang kompatibel.\n"
                         "3. Periksa kabel apakah ada kerusakan fisik.\n"
                         "4. Ukur output tegangan dengan multimeter jika memungkinkan.",
        "cf_pakar": 0.90,
        "kategori": "daya"
    },
    "K02": {
        "kode_kerusakan": "K02",
        "nama_kerusakan": "Baterai rusak/drop",
        "penyebab": "Sel baterai melemah atau charging circuit error",
        "solusi_singkat": "Kalibrasi baterai, cek battery health",
        "solusi_detail": "1. Cek battery health melalui software diagnostik.\n"
                         "2. Lakukan kalibrasi: charge 100% → discharge hingga mati → charge lagi.\n"
                         "3. Jika health < 40%, pertimbangkan ganti baterai.",
        "cf_pakar": 0.85,
        "kategori": "daya"
    }
    # ... K03 hingga K10 (mengikuti pola yang sama)
}
```

#### 4.2.2 Schema: Gejala (`symptoms.py`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "laptopdoc/gejala",
  "title": "Gejala Kerusakan Laptop",
  "description": "Schema untuk data gejala G01-G25 yang ditanyakan ke pengguna",
  "type": "object",
  "patternProperties": {
    "^G(0[1-9]|1[0-9]|2[0-5])$": {
      "type": "object",
      "properties": {
        "kode_gejala": {
          "type": "string",
          "pattern": "^G(0[1-9]|1[0-9]|2[0-5])$",
          "description": "Kode unik gejala"
        },
        "teks_gejala": {
          "type": "string",
          "maxLength": 200,
          "description": "Teks pertanyaan gejala"
        },
        "deskripsi_detail": {
          "type": "string",
          "description": "Tooltip penjelasan tambahan"
        },
        "kategori": {
          "type": "string",
          "enum": ["daya", "visual", "performa", "input", "konektivitas", "audio"],
          "description": "Kategori gejala"
        }
      },
      "required": ["kode_gejala", "teks_gejala"]
    }
  },
  "additionalProperties": false
}
```

**Contoh Data:**

```python
# knowledge_base/symptoms.py

SYMPTOMS = {
    "G01": {
        "kode_gejala": "G01",
        "teks_gejala": "Laptop tidak menyala saat tombol power ditekan",
        "deskripsi_detail": "Saat tombol power ditekan, tidak ada respons apapun "
                           "(tidak ada lampu, suara, atau tampilan).",
        "kategori": "daya"
    },
    "G02": {
        "kode_gejala": "G02",
        "teks_gejala": "Lampu indikator charger tidak menyala",
        "deskripsi_detail": "Saat adaptor/charger dipasang ke laptop, lampu LED "
                           "pada adaptor atau laptop tidak menyala.",
        "kategori": "daya"
    }
    # ... G03 hingga G25 (mengikuti pola yang sama)
}
```

#### 4.2.3 Schema: Rule Base (`rules.py`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "laptopdoc/rule",
  "title": "Rule Base Backward Chaining",
  "description": "Schema untuk 12 rule inferensi IF-THEN (R1-R12)",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "rule_id": {
        "type": "string",
        "pattern": "^R(1[0-2]|[1-9])$",
        "description": "ID unik rule"
      },
      "premis": {
        "type": "array",
        "items": {
          "type": "string",
          "pattern": "^G(0[1-9]|1[0-9]|2[0-5])$"
        },
        "minItems": 1,
        "description": "List kode gejala premis (urut sesuai evaluasi)"
      },
      "konklusi": {
        "type": "string",
        "pattern": "^K(0[1-9]|10)$",
        "description": "Kode kerusakan yang menjadi konklusi rule"
      },
      "cf_rule": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0,
        "description": "CF pakar untuk rule ini"
      },
      "deskripsi_rule": {
        "type": "string",
        "description": "Deskripsi IF-THEN dalam bahasa alami"
      }
    },
    "required": ["rule_id", "premis", "konklusi", "cf_rule"]
  }
}
```

**Contoh Data:**

```python
# knowledge_base/rules.py

RULES = [
    {
        "rule_id": "R1",
        "premis": ["G01", "G02", "G18"],
        "konklusi": "K01",
        "cf_rule": 0.90,
        "deskripsi_rule": "IF laptop tidak menyala (G01) "
                          "AND lampu charger mati (G02) "
                          "AND adaptor longgar (G18) "
                          "THEN adaptor/charger rusak (K01)"
    },
    {
        "rule_id": "R2",
        "premis": ["G03", "G04", "G05"],
        "konklusi": "K02",
        "cf_rule": 0.85,
        "deskripsi_rule": "IF laptop hanya menyala saat charger (G03) "
                          "AND baterai tidak mengisi (G04) "
                          "AND baterai cepat habis (G05) "
                          "THEN baterai rusak/drop (K02)"
    },
    {
        "rule_id": "R3",
        "premis": ["G06", "G07"],
        "konklusi": "K03",
        "cf_rule": 0.80,
        "deskripsi_rule": "IF bunyi beep saat startup (G06) "
                          "AND layar blank dengan power menyala (G07) "
                          "THEN RAM bermasalah (K03)"
    },
    {
        "rule_id": "R4",
        "premis": ["G08", "G09", "G10"],
        "konklusi": "K04",
        "cf_rule": 0.88,
        "deskripsi_rule": "IF laptop cepat panas (G08) "
                          "AND mati sendiri (G09) "
                          "AND kipas bising (G10) "
                          "THEN overheating (K04)"
    },
    {
        "rule_id": "R5",
        "premis": ["G07", "G16", "G17"],
        "konklusi": "K05",
        "cf_rule": 0.82,
        "deskripsi_rule": "IF layar blank (G07) "
                          "AND layar bergaris/berkedip (G16) "
                          "AND monitor eksternal normal (G17) "
                          "THEN LCD/display bermasalah (K05)"
    },
    {
        "rule_id": "R6",
        "premis": ["G11", "G12", "G13"],
        "konklusi": "K06",
        "cf_rule": 0.84,
        "deskripsi_rule": "IF gagal boot (G11) "
                          "AND laptop lambat/hang (G12) "
                          "AND bisa masuk BIOS tapi gagal OS (G13) "
                          "THEN HDD/SSD bermasalah (K06)"
    },
    {
        "rule_id": "R7",
        "premis": ["G14", "G15"],
        "konklusi": "K07",
        "cf_rule": 0.78,
        "deskripsi_rule": "IF beberapa tombol tidak berfungsi (G14) "
                          "AND keyboard input ganda (G15) "
                          "THEN keyboard rusak (K07)"
    },
    {
        "rule_id": "R8",
        "premis": ["G19", "G20", "G21"],
        "konklusi": "K08",
        "cf_rule": 0.75,
        "deskripsi_rule": "IF LED berkedip tanpa start (G19) "
                          "AND hidup sebentar lalu mati (G20) "
                          "AND tidak ada tampilan/beep (G21) "
                          "THEN motherboard bermasalah (K08)"
    },
    {
        "rule_id": "R9",
        "premis": ["G22"],
        "konklusi": "K09",
        "cf_rule": 0.76,
        "deskripsi_rule": "IF touchpad tidak merespons/pointer meloncat (G22) "
                          "THEN touchpad bermasalah (K09)"
    },
    {
        "rule_id": "R10",
        "premis": ["G23"],
        "konklusi": "K10",
        "cf_rule": 0.74,
        "deskripsi_rule": "IF WiFi sering putus/tidak deteksi jaringan (G23) "
                          "THEN modul WiFi bermasalah (K10)"
    },
    {
        "rule_id": "R11",
        "premis": ["G24"],
        "konklusi": "K08",
        "cf_rule": 0.70,
        "deskripsi_rule": "IF suara speaker pecah/tidak keluar (G24) "
                          "THEN motherboard bermasalah — jalur audio (K08)"
    },
    {
        "rule_id": "R12",
        "premis": ["G25"],
        "konklusi": "K08",
        "cf_rule": 0.68,
        "deskripsi_rule": "IF port USB tidak deteksi perangkat (G25) "
                          "THEN motherboard bermasalah — jalur USB (K08)"
    }
]

# ---------------------------------------------------------
# Pre-indexed lookup: Rule berdasarkan konklusi (kode_kerusakan)
# Digunakan oleh Backward Chaining engine untuk O(1) lookup
# ---------------------------------------------------------
RULES_BY_CONCLUSION = {}
for rule in RULES:
    key = rule["konklusi"]
    if key not in RULES_BY_CONCLUSION:
        RULES_BY_CONCLUSION[key] = []
    RULES_BY_CONCLUSION[key].append(rule)

# Hasil RULES_BY_CONCLUSION:
# {
#     "K01": [R1],
#     "K02": [R2],
#     ...
#     "K08": [R8, R11, R12],  ← 3 jalur pembuktian
#     ...
# }
```

---

### 4.3 Ringkasan Statistik Knowledge Base

| Metrik | Nilai |
|---|---|
| Total Frame (Kerusakan) | **10** (K01–K10) |
| Total Gejala | **25** (G01–G25) |
| Total Rule | **12** (R1–R12) |
| Total Relasi Premis | **30** |
| Shared Symptoms | **1** (G07 → R3, R5) |
| Multi-Rule Conclusions | **1** kerusakan (K08 → R8, R11, R12) |
| Range CF Pakar | **0.68 – 0.90** |
| Rata-rata premis per rule | **2.5** |

---

> *Dokumen ini disusun berdasarkan standar ISO/IEC 9075 yang diadaptasi untuk Knowledge Base Sistem Pakar. Proyek LaptopDoc — Sistem Pakar Diagnosis Kerusakan Laptop. Versi 1.0 — Maret 2026.*
