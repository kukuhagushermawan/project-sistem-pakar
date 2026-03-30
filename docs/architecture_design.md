# DOKUMEN ARSITEKTUR SISTEM (SDD)
## Sistem Pakar Diagnosis Kerusakan Laptop — LaptopDoc
### Software Design Description — IEEE 1016

**Standar Acuan:** IEEE Std 1016-2009 (IEEE Standard for Information Technology — Systems Design — Software Design Descriptions)

| Item | Detail |
|---|---|
| **Versi** | 1.0 |
| **Tanggal** | 28 Maret 2026 |
| **Status** | Final |
| **Dokumen Referensi** | SRS v1.0 (IEEE 830), UML Analysis v1.0  (UML 2.5), Knowledge Base Design v1.0 (ISO/IEC 9075) |

---

## 1.0 Gambaran Arsitektur

### 1.1 Pola Arsitektur: Layered Architecture (3-Tier)

Sistem LaptopDoc mengadopsi pola **Layered Architecture** (Arsitektur Berlapis) dengan 3 lapisan utama yang memisahkan tanggung jawab secara vertikal:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    ╔═══════════════════════════════╗                     │
│                    ║     PRESENTATION LAYER        ║                     │
│                    ║    (Antarmuka Web Prototype)   ║                     │
│                    ║                               ║                     │
│                    ║  • Halaman Beranda             ║                     │
│                    ║  • Wizard Konsultasi           ║                     │
│                    ║  • Halaman Hasil Diagnosis     ║                     │
│                    ║  • Visualisasi Pohon Inferensi ║                     │
│                    ╚══════════════╤════════════════╝                     │
│                                   │                                      │
│                          API Internal (Function Call)                    │
│                                   │                                      │
│                    ╔══════════════╧════════════════╗                     │
│                    ║    BUSINESS LOGIC LAYER       ║                     │
│                    ║   (Inference Engine & CF)      ║                     │
│                    ║                               ║                     │
│                    ║  • Backward Chaining Engine    ║                     │
│                    ║  • Certainty Factor Calculator ║                     │
│                    ║  • Explanation Facility        ║                     │
│                    ╚══════════════╤════════════════╝                     │
│                                   │                                      │
│                          Direct Import (Python Module)                  │
│                                   │                                      │
│                    ╔══════════════╧════════════════╗                     │
│                    ║       DATA LAYER              ║                     │
│                    ║  (Knowledge Base Management)   ║                     │
│                    ║                               ║                     │
│                    ║  • Frame Kerusakan (K01-K10)   ║                     │
│                    ║  • Rule Base (R1-R12)          ║                     │
│                    ║  • Data Gejala (G01-G25)       ║                     │
│                    ╚═══════════════════════════════╝                     │
│                                                                         │
│                    ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐                    │
│                      CROSS-CUTTING: Session State                       │
│                    │   (Streamlit st.session_state)  │                    │
│                    └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Justifikasi Pola Arsitektur

| Aspek | Justifikasi |
|---|---|
| **Separation of Concerns** | Setiap lapisan memiliki tanggung jawab tunggal: UI menampilkan, Engine menalar, KB menyimpan data. Perubahan di satu lapisan tidak berdampak ke lapisan lain. |
| **Testability** | Engine dan CF Calculator dapat diuji secara independen (unit test) tanpa memerlukan UI. |
| **Modifiability** | Knowledge Base dapat diperluas (tambah rule/frame) tanpa mengubah logika inferensi. |
| **Academic Clarity** | Pemetaan langsung ke komponen Sistem Pakar (Knowledge Base, Inference Engine, User Interface, Explanation Facility) — mudah dipresentasikan. |
| **Prototype Suitability** | Tanpa overhead arsitektur kompleks (microservices, API gateway). Layered cukup untuk skala prototype akademik. |

### 1.3 Prinsip Desain

| No | Prinsip | Implementasi |
|---|---|---|
| 1 | **Single Responsibility** | Setiap modul Python hanya menangani satu concern (misal: `certainty_factor.py` hanya menghitung CF). |
| 2 | **Dependency Inversion** | UI Layer bergantung pada abstraksi Engine, bukan implementasi detail KB. |
| 3 | **Information Hiding** | Detail penyimpanan Knowledge Base (dictionary structure) tersembunyi di balik fungsi akses publik. |
| 4 | **Loose Coupling** | Engine tidak mengetahui detail rendering UI. UI hanya memanggil method publik Engine. |
| 5 | **High Cohesion** | Semua fungsi terkait Backward Chaining berada di satu modul (`backward_chaining.py`). |

---

## 2.0 Lapisan Arsitektur — Desain Detail

### 2.1 Presentation Layer (Antarmuka Web Prototype)

#### 2.1.1 Tanggung Jawab

- Menampilkan antarmuka pengguna (UI) melalui browser.
- Menangkap input pengguna (jawaban CF User, klik tombol).
- Menyajikan output sistem (hasil diagnosis, explanation, visualisasi).
- Mengelola navigasi antar halaman (sidebar).

#### 2.1.2 Komponen

```
ui/
├── home.py            # Halaman Beranda
├── consultation.py    # Wizard Konsultasi Step-by-Step
├── result.py          # Halaman Hasil Diagnosis
└── components.py      # Komponen UI Reusable (card, progress bar, dll.)

visualization/
└── inference_tree.py  # Visualisasi Pohon Inferensi (Graphviz)

assets/
└── style.css          # Custom CSS

.streamlit/
└── config.toml        # Konfigurasi tema Streamlit
```

#### 2.1.3 Diagram Komponen Presentation Layer

```
┌─────────────────────────── PRESENTATION LAYER ──────────────────────────┐
│                                                                          │
│  ┌──────────────┐    ┌───────────────────┐    ┌──────────────────────┐  │
│  │  home.py     │    │ consultation.py   │    │    result.py         │  │
│  │              │    │                   │    │                      │  │
│  │ • Deskripsi  │───►│ • Progress bar    │───►│ • Ranking card       │  │
│  │ • Fitur      │    │ • Pertanyaan      │    │ • Expander "How"     │  │
│  │ • Tombol     │    │ • Radio CF User   │    │ • Pohon inferensi    │  │
│  │   "Mulai"    │    │ • Tombol "Why?"   │    │ • Tombol "Ulang"     │  │
│  └──────────────┘    │ • Tombol "Lanjut" │    └──────────┬───────────┘  │
│                      └─────────┬─────────┘               │              │
│                                │                         │              │
│  ┌─────────────────────────────┼─────────────────────────┘              │
│  │                             │                                        │
│  ▼                             ▼                                        │
│  ┌──────────────┐    ┌───────────────────┐                              │
│  │ components.py│    │inference_tree.py  │                              │
│  │              │    │                   │                              │
│  │ • Card       │    │ • Graphviz Digraph│                              │
│  │ • Badge CF   │    │ • Node warna      │                              │
│  │ • Alert      │    │ • Edge label      │                              │
│  └──────────────┘    └───────────────────┘                              │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 2.1.4 Alur Navigasi Halaman

```
                    ┌───────────┐
                    │  BERANDA  │
                    │ (home.py) │
                    └─────┬─────┘
                          │ Klik "Mulai Konsultasi"
                          ▼
              ┌────────────────────────┐
              │      KONSULTASI        │
              │  (consultation.py)     │◄─────┐
              │                        │      │ Loop: pertanyaan
              │  Pertanyaan 1 → 2 → N  │──────┘ gejala berikutnya
              └────────────┬───────────┘
                           │ Semua hipotesis selesai
                           ▼
              ┌────────────────────────┐
              │    HASIL DIAGNOSIS     │
              │     (result.py)        │
              │                        │
              │  Ranking + How + Tree  │
              └────────────┬───────────┘
                           │ Klik "Konsultasi Ulang"
                           ▼
                    Kembali ke BERANDA
```

#### 2.1.5 Widget Mapping ke Streamlit

| Kebutuhan UI | Widget Streamlit | Keterangan |
|---|---|---|
| Pertanyaan gejala | `st.markdown()` | Teks gejala dengan kode |
| Input CF User | `st.radio()` | 5 opsi (0.0, 0.4, 0.6, 0.8, 1.0) |
| Tombol "Mengapa?" | `st.expander()` | Toggle panel explanation |
| Tombol "Lanjut" | `st.button()` | Submit jawaban, lanjut step |
| Progress hipotesis | `st.progress()` | Bar visual posisi K01-K10 |
| Card hasil | `st.container()` + `st.columns()` | Layout card kerusakan |
| Detail "Bagaimana" | `st.expander()` | Perhitungan CF detail |
| Pohon inferensi | `st.graphviz_chart()` | Render Digraph native |
| Navigasi | `st.sidebar.radio()` | Sidebar menu halaman |
| Session state | `st.session_state` | Penyimpanan data runtime |

---

### 2.2 Business Logic Layer (Inference Engine & CF Calculator)

#### 2.2.1 Tanggung Jawab

- Menjalankan proses penalaran **Backward Chaining** (goal-driven).
- Menghitung **Certainty Factor** kombinasi dan final.
- Menghasilkan penjelasan **Explanation Facility** (Why & How).
- Mengelola state inferensi (hipotesis aktif, rule aktif, jawaban tersimpan).

#### 2.2.2 Komponen

```
engine/
├── __init__.py
├── backward_chaining.py    # Mesin inferensi utama
├── certainty_factor.py     # Kalkulator CF
└── explanation.py          # Generator penjelasan Why/How
```

#### 2.2.3 Diagram Kelas — Business Logic Layer

```
┌──────────────────────────── BUSINESS LOGIC LAYER ───────────────────────┐
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐        │
│  │               BackwardChainingEngine                         │        │
│  ├──────────────────────────────────────────────────────────────┤        │
│  │ - hypotheses: List[str]          # [K01..K10]               │        │
│  │ - current_hypothesis_idx: int    # Index hipotesis aktif    │        │
│  │ - current_rule: RuleDict         # Rule yang sedang evaluasi│        │
│  │ - current_premise_idx: int       # Index premis aktif       │        │
│  │ - answers: Dict[str, float]      # {kode_gejala: cf_user}  │        │
│  │ - results: List[DiagnosisResult] # Hasil per hipotesis      │        │
│  │ - trace: List[TraceEntry]        # Log jejak inferensi      │        │
│  ├──────────────────────────────────────────────────────────────┤        │
│  │ + start() → void                                            │        │
│  │ + get_current_question() → QuestionDict | None              │        │
│  │ + submit_answer(kode_gejala, cf_user) → EngineState         │        │
│  │ + get_results() → List[DiagnosisResult]                     │        │
│  │ + is_finished() → bool                                      │        │
│  │ + get_progress() → (current, total)                         │        │
│  │ - _evaluate_hypothesis(kode) → HypothesisResult             │        │
│  │ - _find_rules(kode_kerusakan) → List[RuleDict]              │        │
│  │ - _next_hypothesis() → void                                 │        │
│  └──────────────────────┬───────────────────────────────────────┘        │
│                         │ uses                                           │
│              ┌──────────┴──────────┐                                    │
│              ▼                     ▼                                    │
│  ┌───────────────────┐  ┌──────────────────────────────────────┐        │
│  │ CertaintyFactor   │  │      ExplanationFacility              │        │
│  ├───────────────────┤  ├──────────────────────────────────────┤        │
│  │                   │  │                                      │        │
│  │+combine_cf(       │  │+why(symptom, hypothesis, rule)       │        │
│  │   cf1, cf2)→float │  │   → str                             │        │
│  │                   │  │                                      │        │
│  │+calculate_final(  │  │+how(diagnosis_result)                │        │
│  │   cf_pakar,       │  │   → HowExplanation                  │        │
│  │   cf_user_list)   │  │                                      │        │
│  │   → float         │  │-_format_cf_steps(cf_list)            │        │
│  │                   │  │   → str                             │        │
│  │+combine_multi_    │  │                                      │        │
│  │  rules(cf_list)   │  │-_format_rule_detail(rule, answers)   │        │
│  │   → float         │  │   → str                             │        │
│  └───────────────────┘  └──────────────────────────────────────┘        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 2.2.4 Algoritma Backward Chaining — Pseudocode

```
ALGORITHM backward_chaining_consultation():
INPUT:  Knowledge Base (FRAMES, RULES, SYMPTOMS)
OUTPUT: List<DiagnosisResult> ranked by CF_final DESC

BEGIN
    hypotheses ← [K01, K02, K03, ..., K10]   // ordered
    results    ← []
    answers    ← {}                           // cache jawaban

    FOR EACH hypothesis IN hypotheses:
        rules ← RULES_BY_CONCLUSION[hypothesis]
        cf_per_rule ← []

        FOR EACH rule IN rules:
            cf_user_list ← []
            rule_passed  ← TRUE

            FOR EACH symptom IN rule.premis:
                IF symptom IN answers:
                    cf_user ← answers[symptom]       // gunakan cache
                ELSE:
                    cf_user ← ASK_USER(symptom)      // tanya ke user
                    answers[symptom] ← cf_user        // simpan cache
                ENDIF

                IF cf_user == 0.0:
                    rule_passed ← FALSE
                    BREAK                             // early termination
                ELSE:
                    cf_user_list.APPEND(cf_user)
                ENDIF
            ENDFOR

            IF rule_passed:
                cf_user_combined ← COMBINE_CF(cf_user_list)
                cf_final         ← rule.cf_rule × cf_user_combined
                cf_per_rule.APPEND(cf_final)
            ENDIF
        ENDFOR

        IF cf_per_rule IS NOT EMPTY:
            cf_hypothesis ← COMBINE_MULTI_RULES(cf_per_rule)
            results.APPEND({hypothesis, cf_hypothesis, status: TERBUKTI})
        ELSE:
            results.APPEND({hypothesis, cf: 0.0, status: GAGAL})
        ENDIF
    ENDFOR

    SORT results BY cf_final DESC
    RETURN results
END

// ---

FUNCTION COMBINE_CF(cf_list):
    result ← cf_list[0]
    FOR i ← 1 TO LENGTH(cf_list) - 1:
        result ← result + cf_list[i] × (1 - result)
    ENDFOR
    RETURN result
ENDFUNCTION
```

#### 2.2.5 Sequence Diagram — Interaksi Antar Komponen

```
┌─────┐     ┌─────────────┐     ┌──────────────────┐     ┌────────────┐     ┌──────┐
│ User│     │consultation │     │BackwardChaining   │     │ Certainty  │     │  KB  │
│     │     │   .py       │     │   Engine          │     │  Factor    │     │      │
└──┬──┘     └──────┬──────┘     └────────┬──────────┘     └─────┬──────┘     └──┬───┘
   │               │                     │                      │               │
   │  Klik Mulai   │                     │                      │               │
   │──────────────►│  engine.start()     │                      │               │
   │               │────────────────────►│  get_hypotheses()    │               │
   │               │                     │─────────────────────────────────────►│
   │               │                     │◄─────────────────── [K01..K10] ──────│
   │               │                     │  find_rules(K01)     │               │
   │               │                     │─────────────────────────────────────►│
   │               │                     │◄─────────────────── [R1] ───────────│
   │               │◄────── question ────│                      │               │
   │◄── tampilkan ─│                     │                      │               │
   │               │                     │                      │               │
   │  Jawab CF=0.8 │                     │                      │               │
   │──────────────►│  submit(G01, 0.8)   │                      │               │
   │               │────────────────────►│                      │               │
   │               │                     │                      │               │
   │  [loop gejala berikutnya...]        │                      │               │
   │               │                     │                      │               │
   │               │                     │  combine_cf()        │               │
   │               │                     │─────────────────────►│               │
   │               │                     │◄──── cf_combined ────│               │
   │               │                     │  calculate_final()   │               │
   │               │                     │─────────────────────►│               │
   │               │                     │◄──── cf_final ───────│               │
   │               │                     │                      │               │
   │               │  [loop hipotesis berikutnya...]            │               │
   │               │                     │                      │               │
   │               │◄─── results[] ──────│                      │               │
   │◄── tampilkan ─│                     │                      │               │
   │   hasil + viz │                     │                      │               │
   │               │                     │                      │               │
```

---

### 2.3 Data Layer (Knowledge Base Management)

#### 2.3.1 Tanggung Jawab

- Menyimpan basis pengetahuan secara **statis** (hardcoded Python dictionary).
- Menyediakan **fungsi akses** terstruktur untuk Engine.
- Mengelola **indexing** data untuk performa lookup optimal.

#### 2.3.2 Komponen

```
knowledge_base/
├── __init__.py        # Ekspor publik: FRAMES, RULES, SYMPTOMS, lookup functions
├── frames.py          # Dictionary Frame Kerusakan (K01-K10)
├── rules.py           # List Rule Base (R1-R12) + RULES_BY_CONCLUSION index
└── symptoms.py        # Dictionary Gejala (G01-G25)
```

#### 2.3.3 Diagram Komponen Data Layer

```
┌───────────────────────────── DATA LAYER ────────────────────────────────┐
│                                                                          │
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐    │
│  │    frames.py      │  │    rules.py       │  │   symptoms.py     │    │
│  ├───────────────────┤  ├───────────────────┤  ├───────────────────┤    │
│  │                   │  │                   │  │                   │    │
│  │ FRAMES = {        │  │ RULES = [         │  │ SYMPTOMS = {      │    │
│  │   "K01": {        │  │   {"rule_id":"R1",│  │   "G01": {        │    │
│  │     nama,         │  │    "premis":[...],│  │     teks_gejala,  │    │
│  │     penyebab,     │  │    "konklusi":"..",│  │     deskripsi,    │    │
│  │     solusi,       │  │    "cf_rule":0.90 │  │     kategori      │    │
│  │     cf_pakar      │  │   }, ...          │  │   }, ...          │    │
│  │   }, ...          │  │ ]                 │  │ }                 │    │
│  │ }                 │  │                   │  │                   │    │
│  │                   │  │ RULES_BY_         │  │                   │    │
│  │ 10 records        │  │ CONCLUSION = {    │  │ 25 records        │    │
│  │                   │  │  "K01":[R1],      │  │                   │    │
│  │                   │  │  "K08":[R8,R11,   │  │                   │    │
│  │                   │  │        R12], ...  │  │                   │    │
│  │                   │  │ }                 │  │                   │    │
│  │                   │  │ 12 rules          │  │                   │    │
│  └───────┬───────────┘  └───────┬───────────┘  └───────┬───────────┘    │
│          │                      │                      │                │
│          └──────────────────────┼──────────────────────┘                │
│                                 │                                       │
│                    ┌────────────▼────────────┐                          │
│                    │     __init__.py         │                          │
│                    ├────────────────────────┤                          │
│                    │ # Ekspor publik:        │                          │
│                    │ from .frames   import   │                          │
│                    │     FRAMES              │                          │
│                    │ from .rules    import   │                          │
│                    │     RULES,              │                          │
│                    │     RULES_BY_CONCLUSION │                          │
│                    │ from .symptoms import   │                          │
│                    │     SYMPTOMS            │                          │
│                    │                         │                          │
│                    │ # Fungsi akses:         │                          │
│                    │ get_frame(kode) → dict  │                          │
│                    │ get_symptom(kode) → dict│                          │
│                    │ get_rules_for(kode)     │                          │
│                    │   → List[dict]          │                          │
│                    └────────────────────────┘                          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 2.3.4 Strategi Akses Data

| Operasi | Metode | Kompleksitas | Digunakan Oleh |
|---|---|---|---|
| Ambil frame by kode | `FRAMES[kode_kerusakan]` | **O(1)** | Result page (tampilkan solusi) |
| Ambil gejala by kode | `SYMPTOMS[kode_gejala]` | **O(1)** | Consultation page (teks pertanyaan) |
| Cari rule by konklusi | `RULES_BY_CONCLUSION[kode_kerusakan]` | **O(1)** | BC Engine (cari rule untuk hipotesis) |
| Iterasi semua hipotesis | `list(FRAMES.keys())` | **O(n)** n=10 | BC Engine (iterasi K01→K10) |
| Cek gejala sudah dijawab | `kode in answers` | **O(1)** | BC Engine (cache check) |

---

### 2.4 Cross-Cutting Concern: Session State Management

```
┌────────────────────── SESSION STATE (st.session_state) ─────────────────┐
│                                                                          │
│  Diakses oleh SEMUA layer secara cross-cutting                          │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ Key                        │ Tipe         │ Deskripsi           │    │
│  ├────────────────────────────┼──────────────┼─────────────────────┤    │
│  │ "engine"                   │ BC Engine    │ Instance engine     │    │
│  │ "page"                     │ str          │ Halaman aktif       │    │
│  │ "answers"                  │ Dict         │ Cache jawaban CF    │    │
│  │ "results"                  │ List         │ Hasil diagnosis     │    │
│  │ "trace"                    │ List         │ Log jejak inferensi │    │
│  │ "history"                  │ List         │ Riwayat sesi        │    │
│  │ "consultation_started"     │ bool         │ Flag sesi aktif     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  Lifecycle: Dibuat saat "Mulai Konsultasi" → Bertahan selama tab       │
│  browser terbuka → Dihapus saat browser ditutup.                       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3.0 Teknologi Stack

### 3.1 Tabel Teknologi per Layer

| Layer | Teknologi | Versi Min | Alasan Pemilihan |
|---|---|---|---|
| **Presentation** | Streamlit | 1.30+ | Framework Python all-in-one untuk rapid prototyping web. Built-in widget (radio, expander, progress bar) langsung cocok dengan kebutuhan wizard konsultasi. Zero-config deployment: `streamlit run app.py`. |
| **Presentation** | Graphviz (Python) | 0.20+ | Library visualisasi graph/tree native di Streamlit via `st.graphviz_chart()`. Ideal untuk menampilkan pohon inferensi Backward Chaining. |
| **Presentation** | Custom CSS | — | Styling tambahan untuk card hasil diagnosis, badge CF, dan layout wizard. Diterapkan via `st.markdown(unsafe_allow_html=True)`. |
| **Business Logic** | Python Standard Library | 3.8+ | Tidak memerlukan library ML/AI eksternal. Logika Backward Chaining dan CF cukup diimplementasikan dengan Python murni (dictionary, list, loop). |
| **Data** | Python Dictionary (In-Memory) | — | Dataset kecil (10+25+12 records). Akses O(1) untuk lookup. Zero-configuration, tanpa install database. Paling cepat untuk kalkulasi CF saat demo. |
| **Session** | Streamlit Session State | — | Mekanisme bawaan Streamlit untuk menyimpan state antar interaksi user. Cocok untuk alur wizard step-by-step. Tidak perlu database/Redis. |
| **Runtime** | Python | 3.8+ | Bahasa utama. Ekosistem kaya untuk data science, namun di sini digunakan untuk logika if-then engine. Mudah dipahami oleh mahasiswa. |
| **Package Mgr** | pip | 20.0+ | Package manager standar Python. `pip install -r requirements.txt` untuk satu langkah instalasi. |
| **Version Control** | Git | — | Standar industri version control untuk kolaborasi tim dan tracking perubahan. |

### 3.2 Dependency Minimal

```
requirements.txt
─────────────────
streamlit>=1.30.0     # Framework web UI
graphviz>=0.20        # Visualisasi pohon inferensi
```

> **Total dependency: 2 package saja.** Meminimalkan risiko konflik dan mempercepat setup awal (`pip install` < 30 detik).

### 3.3 Justifikasi: Mengapa Bukan Framework Lain?

| Alternatif | Alasan Tidak Dipilih |
|---|---|
| **Flask/Django + React** | Overhead terlalu besar: perlu membangun REST API, CORS, frontend build system. Tidak efisien untuk prototype akademik. |
| **Jupyter Notebook** | Tidak cocok untuk demo interaktif multi-halaman wizard. Tidak memiliki session state yang reliable. |
| **Tkinter / PyQt** | Desktop-only, tidak web-based. Tidak bisa diakses melalui browser. |
| **CLIPS / Jess** | Bahasa rule-engine khusus. Kurang fleksibel untuk custom UI, CF calculation, dan explanation facility. Kurva belajar tinggi. |

---

## 4.0 Keputusan Arsitektur (ADR)

### ADR-001: Implementasi Explanation Facility dalam Alur Konsultasi

```
╔══════════════════════════════════════════════════════════════════════════╗
║  ADR-001: Implementasi Explanation Facility dalam Alur Konsultasi      ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║  Tanggal  : 28 Maret 2026                                              ║
║  Status   : ACCEPTED                                                    ║
║  Pembuat  : Tim Pengembang LaptopDoc                                    ║
║                                                                         ║
╠═════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║  1. KONTEKS                                                             ║
║  ═════════                                                              ║
║                                                                         ║
║  Explanation Facility adalah komponen vital dalam Sistem Pakar yang     ║
║  membedakannya dari black-box AI. LaptopDoc memerlukan dua jenis       ║
║  penjelasan:                                                            ║
║                                                                         ║
║  • "Mengapa" (Why) — Menjawab: Mengapa sistem bertanya gejala ini?     ║
║    Harus tersedia SAAT konsultasi berlangsung (per pertanyaan).         ║
║                                                                         ║
║  • "Bagaimana" (How) — Menjawab: Bagaimana sistem mencapai kesimpulan? ║
║    Harus tersedia SETELAH konsultasi selesai (per hasil diagnosis).     ║
║                                                                         ║
║  Pertanyaan arsitektural:                                               ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │ Bagaimana mengintegrasikan Explanation Facility ke dalam alur  │    ║
║  │ konsultasi Backward Chaining tanpa mengganggu flow wizard     │    ║
║  │ step-by-step dan tanpa menambah kompleksitas arsitektur?       │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                         ║
║  Terdapat 3 opsi yang dipertimbangkan:                                  ║
║                                                                         ║
║  Opsi A: Explanation sebagai modul terpisah yang di-query on-demand    ║
║  Opsi B: Explanation built-in di dalam Backward Chaining Engine        ║
║  Opsi C: Explanation sebagai modul terpisah + Trace Log pattern        ║
║                                                                         ║
╠═════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║  2. KEPUTUSAN                                                           ║
║  ════════════                                                           ║
║                                                                         ║
║  Memilih: ▶ OPSI C — Explanation sebagai modul terpisah                ║
║                       dengan Trace Log pattern                          ║
║                                                                         ║
║  Implementasi:                                                          ║
║                                                                         ║
║  2.1) Modul explanation.py yang TERPISAH dari backward_chaining.py     ║
║       ┌──────────────────────────────────────────────────────────┐      ║
║       │ engine/explanation.py                                     │      ║
║       │                                                           │      ║
║       │ class ExplanationFacility:                                │      ║
║       │     def why(symptom, hypothesis, rule) -> str             │      ║
║       │     def how(diagnosis_result, trace_log) -> HowDetail     │      ║
║       └──────────────────────────────────────────────────────────┘      ║
║                                                                         ║
║  2.2) Backward Chaining Engine merekam TRACE LOG selama inferensi      ║
║       ┌──────────────────────────────────────────────────────────┐      ║
║       │ Trace Log = List of TraceEntry:                           │      ║
║       │ {                                                         │      ║
║       │   "step": 1,                                              │      ║
║       │   "hypothesis": "K01",                                    │      ║
║       │   "rule": "R1",                                           │      ║
║       │   "symptom": "G01",                                       │      ║
║       │   "cf_user": 0.8,                                         │      ║
║       │   "action": "CONTINUE" | "FAIL" | "EVALUATE",             │      ║
║       │   "cf_intermediate": 0.8                                  │      ║
║       │ }                                                         │      ║
║       └──────────────────────────────────────────────────────────┘      ║
║                                                                         ║
║  2.3) "Mengapa" (Why) — Dipanggil SAAT konsultasi                      ║
║       • UI memanggil ExplanationFacility.why() dengan context dari     ║
║         engine state (hipotesis aktif, rule aktif, gejala aktif).       ║
║       • Ditampilkan dalam st.expander(), TIDAK mengganggu alur wizard. ║
║       • Bersifat read-only, tidak mengubah state engine.               ║
║                                                                         ║
║  2.4) "Bagaimana" (How) — Dipanggil SETELAH konsultasi                 ║
║       • UI memanggil ExplanationFacility.how() dengan trace log        ║
║         yang direkam selama proses inferensi.                          ║
║       • Merekonstruksi langkah-langkah CF calculation dari trace.      ║
║       • Ditampilkan per kerusakan dalam st.expander() di halaman hasil.║
║                                                                         ║
╠═════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║  3. KONSEKUENSI                                                         ║
║  ══════════════                                                         ║
║                                                                         ║
║  ✅ POSITIF:                                                            ║
║                                                                         ║
║  • Single Responsibility terjaga — Engine fokus inferensi,             ║
║    Explanation fokus penjelasan. Bisa diuji secara independen.          ║
║                                                                         ║
║  • Trace Log = audit trail — Setiap langkah inferensi terekam.         ║
║    Berguna untuk debugging, testing, dan demo akademik.                ║
║                                                                         ║
║  • "Why" tidak mengganggu flow — Ditampilkan dalam expander            ║
║    (progressive disclosure), user memilih untuk melihat atau tidak.    ║
║                                                                         ║
║  • "How" akurat — Direkonstruksi dari trace log aktual, bukan         ║
║    perhitungan ulang. Menjamin konsistensi antara proses dan           ║
║    penjelasan.                                                         ║
║                                                                         ║
║  • Scalable — Jika knowledge base diperluas, Explanation otomatis      ║
║    mengikuti karena berbasis trace log, bukan template hardcoded.      ║
║                                                                         ║
║  ⚠️ TRADE-OFF:                                                         ║
║                                                                         ║
║  • Memory overhead ringan — Trace log menyimpan entry per langkah      ║
║    inferensi (maks ~30 entry untuk 25 gejala). Negligible untuk        ║
║    dataset prototype ini.                                              ║
║                                                                         ║
║  • Coupling indirect — ExplanationFacility bergantung pada format      ║
║    TraceEntry dari Engine. Perubahan format trace memerlukan update     ║
║    di kedua modul. Dimitigasi dengan definisi TraceEntry yang jelas.   ║
║                                                                         ║
║  ❌ RISIKO:                                                             ║
║                                                                         ║
║  • Jika trace log tidak direkam dengan benar (bug di engine),          ║
║    penjelasan "Bagaimana" bisa tidak akurat. Mitigasi: unit test       ║
║    untuk memvalidasi kelengkapan trace log.                            ║
║                                                                         ║
╠═════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║  4. ALTERNATIF YANG DITOLAK                                             ║
║  ════════════════════════════                                            ║
║                                                                         ║
║  ┌─────┬──────────────────────────┬─────────────────────────────┐       ║
║  │Opsi │ Deskripsi                │ Alasan Ditolak              │       ║
║  ├─────┼──────────────────────────┼─────────────────────────────┤       ║
║  │  A  │ Explanation sebagai      │ Tidak memiliki konteks      │       ║
║  │     │ modul terpisah yang      │ inferensi historis. "How"   │       ║
║  │     │ di-query on-demand.      │ harus menghitung ulang CF   │       ║
║  │     │ Tanpa trace log.         │ → risiko inkonsistensi.     │       ║
║  ├─────┼──────────────────────────┼─────────────────────────────┤       ║
║  │  B  │ Explanation built-in     │ Melanggar SRP. Engine       │       ║
║  │     │ di BackwardChaining      │ menjadi terlalu besar.      │       ║
║  │     │ Engine (satu class).     │ Sulit diuji secara parsial. │       ║
║  └─────┴──────────────────────────┴─────────────────────────────┘       ║
║                                                                         ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

### Ringkasan Keputusan Arsitektur

| ADR | Keputusan | Status | Dampak |
|---|---|---|---|
| ADR-001 | Explanation Facility sebagai modul terpisah + Trace Log pattern | **Accepted** | Menjaga SRP, explanation akurat via trace log, progressive disclosure di UI |

---

## Lampiran: Mapping Arsitektur ke Komponen Sistem Pakar

| Komponen Sistem Pakar (Teori) | Layer Arsitektur | Modul Implementasi |
|---|---|---|
| **User Interface** | Presentation Layer | `ui/home.py`, `ui/consultation.py`, `ui/result.py` |
| **Knowledge Base** | Data Layer | `knowledge_base/frames.py`, `rules.py`, `symptoms.py` |
| **Inference Engine** | Business Logic Layer | `engine/backward_chaining.py` |
| **Working Memory** | Cross-Cutting (Session) | `st.session_state["answers"]`, `st.session_state["trace"]` |
| **Explanation Facility** | Business Logic Layer | `engine/explanation.py` |
| **Certainty Factor** | Business Logic Layer | `engine/certainty_factor.py` |
| **Visualization** | Presentation Layer | `visualization/inference_tree.py` |

```
┌─────────────────────────────── SISTEM PAKAR ──────────────────────────┐
│                                                                        │
│                    ┌───────────────────┐                               │
│                    │   USER INTERFACE  │  ← Presentation Layer        │
│                    └────────┬──────────┘                               │
│                             │                                          │
│              ┌──────────────┼──────────────┐                          │
│              │              │              │                           │
│              ▼              ▼              ▼                           │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│   │  INFERENCE   │ │ EXPLANATION  │ │  CERTAINTY   │                 │
│   │   ENGINE     │ │  FACILITY    │ │   FACTOR     │                 │
│   │ (Backward    │ │ (Why / How)  │ │ (Calculator) │ ← Business     │
│   │  Chaining)   │ │              │ │              │    Logic Layer  │
│   └──────┬───────┘ └──────────────┘ └──────────────┘                 │
│          │                                                            │
│          │         ┌──────────────┐                                   │
│          │         │   WORKING    │ ← Cross-Cutting                  │
│          │         │   MEMORY     │   (Session State)                │
│          │         └──────────────┘                                   │
│          │                                                            │
│          ▼                                                            │
│   ┌──────────────────────────────────────┐                           │
│   │          KNOWLEDGE BASE              │ ← Data Layer             │
│   │                                      │                           │
│   │  ┌──────────┐  ┌──────────────────┐  │                           │
│   │  │  FRAMES  │  │  RULES (IF-THEN) │  │                           │
│   │  │ (K01-K10)│  │  (R1-R12)        │  │                           │
│   │  └──────────┘  └──────────────────┘  │                           │
│   │  ┌──────────────────────────────┐    │                           │
│   │  │  GEJALA (G01-G25)           │    │                           │
│   │  └──────────────────────────────┘    │                           │
│   └──────────────────────────────────────┘                           │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

> *Dokumen Software Design Description ini disusun berdasarkan standar IEEE 1016-2009 untuk proyek LaptopDoc — Sistem Pakar Diagnosis Kerusakan Laptop. Versi 1.0 — Maret 2026.*
