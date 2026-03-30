# SPESIFIKASI DESAIN ANTARMUKA (UI Design Specification)
## Sistem Pakar Diagnosis Kerusakan Laptop — Laptop Diagnostic Expert
### Standar Aksesibilitas: WCAG 2.1 Level AA

| Item | Detail |
|---|---|
| **Versi** | 1.0 |
| **Tanggal** | 28 Maret 2026 |
| **Status** | Final |
| **Dokumen Referensi** | SRS v1.0, Architecture Design v1.0 (IEEE 1016) |

---

## 1. Design System

### 1.1 Palet Warna

Tema: **Professional IT / Technician** — nuansa biru-slate gelap dengan aksen cyan untuk kesan teknologi modern dan terpercaya.

| Token | Hex | Penggunaan |
|---|---|---|
| `--color-bg-primary` | `#0F172A` | Background utama (dark mode) |
| `--color-bg-secondary` | `#1E293B` | Card, panel, sidebar |
| `--color-bg-tertiary` | `#334155` | Hover state, input background |
| `--color-surface` | `#1E293B` | Surface card dan container |
| `--color-border` | `#475569` | Border default |
| `--color-border-focus` | `#06B6D4` | Border saat focus (aksesibilitas) |
| `--color-text-primary` | `#F8FAFC` | Teks utama (contrast ratio ≥ 7:1) |
| `--color-text-secondary` | `#94A3B8` | Teks pendukung (contrast ratio ≥ 4.5:1) |
| `--color-text-muted` | `#64748B` | Placeholder, label minor |
| `--color-accent` | `#06B6D4` | Aksen utama (cyan) — tombol, link, highlight |
| `--color-accent-hover` | `#0891B2` | Hover state aksen |
| `--color-success` | `#10B981` | Status terbukti, CF tinggi, node hijau |
| `--color-danger` | `#EF4444` | Status gagal, error, node merah |
| `--color-warning` | `#F59E0B` | Peringatan, CF sedang |
| `--color-info` | `#3B82F6` | Info panel, tooltip, "Mengapa?" |
| `--color-neutral` | `#6B7280` | Node abu-abu (tidak dievaluasi) |

**WCAG 2.1 Compliance:**
- Teks utama di atas background gelap: contrast ratio **15.4:1** (AAA).
- Teks sekunder di atas background gelap: contrast ratio **5.6:1** (AA).
- Semua elemen interaktif memiliki focus indicator `--color-border-focus` (3px solid cyan).

### 1.2 Tipografi

| Level | Font | Weight | Size | Line Height | Penggunaan |
|---|---|---|---|---|---|
| Display | Inter | 700 (Bold) | 32px | 1.2 | Judul halaman utama |
| Heading 1 | Inter | 600 (SemiBold) | 24px | 1.3 | Section heading |
| Heading 2 | Inter | 600 | 20px | 1.35 | Sub-section, nama kerusakan |
| Body | Inter | 400 (Regular) | 16px | 1.6 | Teks pertanyaan gejala, deskripsi |
| Body Small | Inter | 400 | 14px | 1.5 | Label, keterangan CF, metadata |
| Caption | Inter | 500 (Medium) | 12px | 1.4 | Badge, tag, kode gejala |
| Monospace | JetBrains Mono | 400 | 14px | 1.5 | Kode rule, perhitungan CF |

**Sumber Font:** Google Fonts — `Inter` (sans-serif), `JetBrains Mono` (monospace).

### 1.3 Komponen UI Standar

#### 1.3.1 Tombol (Button)

```
┌─────────────────────────────────────────────────────┐
│ VARIANT        │ STYLE                              │
├─────────────────────────────────────────────────────┤
│ Primary        │ bg: --accent, text: #0F172A        │
│                │ radius: 8px, padding: 12px 24px    │
│                │ hover: --accent-hover              │
│                │ Icon kiri: ▶ (play)                │
│                │ Contoh: [▶ Mulai Konsultasi]       │
├─────────────────────────────────────────────────────┤
│ Secondary      │ bg: transparent, border: --border  │
│                │ text: --text-primary                │
│                │ hover: bg --bg-tertiary             │
│                │ Contoh: [↻ Konsultasi Ulang]       │
├─────────────────────────────────────────────────────┤
│ Info / Why     │ bg: transparent, text: --info       │
│                │ border: --info, radius: 6px         │
│                │ Icon kiri: (?) — circle-question    │
│                │ Contoh: [(?) Mengapa ditanyakan?]   │
├─────────────────────────────────────────────────────┤
│ Ghost          │ bg: transparent, text: --text-sec   │
│                │ hover: underline                    │
│                │ Contoh: Lihat detail >              │
└─────────────────────────────────────────────────────┘
```

#### 1.3.2 Komponen Pilihan Skala Keyakinan (CF User)

**Desain Terpilih: Segmented Radio Card — 5 opsi horizontal**

Setiap opsi ditampilkan sebagai card kecil yang dapat diklik. Pendekatan ini lebih intuitif daripada slider karena memberikan label deskriptif yang jelas untuk setiap level.

```
Pertanyaan: Apakah laptop tidak menyala saat tombol power ditekan?

┌────────────────────────────────────────────────────────────────────┐
│  Pilih tingkat keyakinan Anda:                                    │
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │  ╳  Tidak│ │ ~ Kurang │ │ ◐ Cukup  │ │ ● Yakin  │ │ ◉ Sangat ││
│  │          │ │   yakin  │ │   yakin  │ │          │ │   yakin  ││
│  │   0.0    │ │   0.4    │ │   0.6    │ │   0.8    │ │   1.0    ││
│  │          │ │          │ │          │ │          │ │          ││
│  │ Gejala   │ │ Kadang   │ │ Cukup   │ │ Jelas    │ │ Pasti    ││
│  │ tidak    │ │ terasa   │ │ sering  │ │ tampak   │ │ terjadi  ││
│  │ dialami  │ │          │ │         │ │          │ │          ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘│
│   ░░░░░░░░░░   ░░░░░░░░░░   ░░░░░░░░░░  ░░░░░░░░░░   ░░░░░░░░░░│
│   merah muda    kuning       kuning-hijau  hijau        hijau tua │
│                                                                    │
│  Card yang dipilih:                                               │
│  border: 2px solid --accent (cyan), bg: rgba(6,182,212,0.1)      │
│  Scale transform: 1.02 (micro-animation)                         │
└────────────────────────────────────────────────────────────────────┘
```

**Spesifikasi Teknis Komponen CF:**

| Properti | Nilai |
|---|---|
| Layout | Flexbox horizontal, gap: 8px, wrap pada mobile |
| Card size | Min-width: 100px, padding: 12px |
| Border radius | 10px |
| State: default | `bg: --bg-secondary`, `border: --border` |
| State: hover | `bg: --bg-tertiary`, `border: --text-muted`, cursor pointer |
| State: selected | `bg: rgba(6,182,212,0.1)`, `border: 2px solid --accent` |
| State: focus | `outline: 3px solid --border-focus`, offset: 2px |
| Transition | `all 0.2s ease` |
| Color bar bawah | Gradient merah→kuning→hijau sesuai level CF |
| Icon | SVG monoline (bukan emoji): ╳, ~, ◐, ●, ◉ |
| Aksesibilitas | `role="radiogroup"`, setiap card `role="radio"`, `aria-checked`, navigasi keyboard (Arrow keys) |

#### 1.3.3 Card Hasil Diagnosis

```
┌────────────────────────────────────────────────────────────────┐
│  ┌── Status Badge ──────────────────────────── CF Badge ────┐  │
│  │ [TERBUKTI]                                     [87%]     │  │
│  │                                                          │  │
│  │  K01 — Adaptor/Charger Rusak                             │  │
│  │                                                          │  │
│  │  Penyebab: Suplai daya adaptor tidak stabil              │  │
│  │                                                          │  │
│  │  Solusi: Periksa output adaptor, coba charger lain       │  │
│  │                                                          │  │
│  │  ┌──────────── CF Bar ──────────────────────────────┐    │  │
│  │  │ ████████████████████████████░░░░░  87%           │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                          │  │
│  │  [(i) Bagaimana diagnosis ini diperoleh?]                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘

Style:
- bg: --bg-secondary
- border-left: 4px solid --success (hijau) jika CF ≥ 70%
- border-left: 4px solid --warning (kuning) jika CF 40%-69%
- border-left: 4px solid --danger  (merah)  jika CF < 40%
- CF Badge: pill shape, bg sesuai range
```

#### 1.3.4 Panel Explanation

```
Explanation "Mengapa?" (Why) — tampil inline saat konsultasi:
┌─ (?) ──────────────────────────────────────────────────────────┐
│  Mengapa pertanyaan ini ditanyakan?                            │
│                                                                │
│  Sistem sedang mengevaluasi hipotesis:                         │
│  K01 — Adaptor/Charger Rusak                                  │
│                                                                │
│  Gejala ini (G01) merupakan premis dari Rule R1               │
│  dengan bobot CF Pakar = 0.90                                  │
│                                                                │
│  Jika gejala ini terpenuhi, keyakinan terhadap                │
│  hipotesis K01 akan meningkat.                                 │
└────────────────────────────────────────────────────────────────┘

Explanation "Bagaimana?" (How) — tampil di halaman hasil:
┌─ (i) ──────────────────────────────────────────────────────────┐
│  Detail Perhitungan — K01 (Adaptor Rusak)                     │
│                                                                │
│  Rule R1 [CF Pakar = 0.90]                                     │
│  ├─ G01: Laptop tidak menyala       CF User = 0.8 (Yakin)    │
│  ├─ G02: Lampu charger mati         CF User = 0.6 (Cukup)    │
│  └─ G18: Adaptor longgar            CF User = 1.0 (Sangat)   │
│                                                                │
│  Perhitungan CF Kombinasi:                                     │
│  ┌─────────────────────────────────────────────────────┐      │
│  │ Step 1: CF_combine(0.8, 0.6) = 0.8+0.6×0.2 = 0.92 │      │
│  │ Step 2: CF_combine(0.92, 1.0) = 0.92+1.0×0.08 = 1.0│      │
│  │ CF Final: 0.90 × 1.0 = 0.90 (90%)                  │      │
│  └─────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────┘
```

#### 1.3.5 Iconography

Semua ikon menggunakan **Lucide Icons** (open-source, MIT license) — gaya outline konsisten, stroke-width 1.5px.

| Fungsi | Icon Lucide | Kode |
|---|---|---|
| Mulai konsultasi | `play` | Tombol CTA utama |
| Mengapa? (Why) | `circle-help` | Tombol explanation |
| Bagaimana? (How) | `info` | Expander detail CF |
| Lanjut | `arrow-right` | Tombol next step |
| Terbukti | `circle-check` | Badge status hijau |
| Gagal | `circle-x` | Badge status merah |
| Konsultasi ulang | `refresh-cw` | Tombol reset |
| Riwayat | `clock` | Menu sidebar |
| Beranda | `home` | Menu sidebar |
| Diagnosis | `stethoscope` | Menu sidebar |

---

## 2. Sitemap / Navigasi

### 2.1 Hierarki Halaman

```
Laptop Diagnostic Expert (Root)
│
├── [1] Halaman Beranda (/home)
│       ├── Hero section: judul + deskripsi
│       ├── Fitur utama (3 card)
│       ├── Cara penggunaan (steps)
│       └── CTA: [▶ Mulai Konsultasi]
│
├── [2] Halaman Konsultasi (/consultation)
│       ├── Progress bar hipotesis (K01-K10)
│       ├── Pertanyaan gejala aktif
│       ├── Pilihan CF User (5 segmented cards)
│       ├── Tombol [(?) Mengapa?] → inline expansion
│       └── Tombol [→ Lanjut]
│
├── [3] Halaman Hasil Diagnosis (/result)
│       ├── Ringkasan: jumlah terbukti / total
│       ├── Ranking card (CF tertinggi di atas)
│       ├── Expander "Bagaimana?" per card
│       ├── Visualisasi pohon inferensi (Graphviz)
│       ├── Tombol [↻ Konsultasi Ulang]
│       └── Tombol [Simpan ke Riwayat]
│
└── [4] Riwayat Konsultasi (/history)
        ├── List sesi sebelumnya
        └── Klik → lihat detail hasil
```

### 2.2 Navigasi

```
┌──────────────────┐
│    SIDEBAR        │
│                   │
│  Laptop Diagnostic Expert  │
│  ─────────        │
│                   │
│  [home] Beranda       │
│  [stethoscope] Konsultasi │
│  [clock] Riwayat       │
│                   │
│  ─────────        │
│  v1.0 | 2026      │
└──────────────────┘
```

Navigasi sidebar tetap terlihat (persistent) di desktop, collapsible di mobile.

---

## 3. Wireframe Tekstual

### 3.1 Layar Konsultasi

```
┌─────────────────────────────────────────────────────────────────────────┐
│ [SIDEBAR]  │                    KONSULTASI DIAGNOSIS                   │
│            │                                                           │
│ [home]     │  Evaluasi Hipotesis: K04 — Overheating                    │
│ Beranda    │  ┌────────────────────────────────────────────────────┐   │
│            │  │ ░░░░░░░░░░░░░░░▓▓▓▓░░░░░░░░░░░░░░░░░░░  4 / 10  │   │
│ [steth.]   │  └────────────────────────────────────────────────────┘   │
│ Konsultasi │                                                           │
│            │  ┌────────────────────────────────────────────────────┐   │
│ [clock]    │  │                                                    │   │
│ Riwayat    │  │   Pertanyaan 2 dari 3 (Rule R4)                   │   │
│            │  │                                                    │   │
│            │  │   G09 — Laptop mati sendiri setelah                │   │
│            │  │          beberapa menit penggunaan                 │   │
│            │  │                                                    │   │
│            │  │   Apakah Anda mengalami gejala ini?                │   │
│            │  │                                                    │   │
│            │  └────────────────────────────────────────────────────┘   │
│            │                                                           │
│            │  Pilih tingkat keyakinan Anda:                            │
│            │                                                           │
│            │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│            │  │╳ Tidak │ │~ Kurang│ │◐ Cukup │ │● Yakin │ │◉Sangat │ │
│            │  │  0.0   │ │  0.4   │ │  0.6   │ │  0.8   │ │  1.0   │ │
│            │  │        │ │  yakin │ │  yakin │ │        │ │  yakin │ │
│            │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │
│            │                                                           │
│            │  ┌─ [(?) Mengapa pertanyaan ini ditanyakan?] ──────────┐ │
│            │  │                                                     │ │
│            │  │  Sistem sedang mengevaluasi hipotesis:               │ │
│            │  │  K04 — Overheating Sistem Pendingin                 │ │
│            │  │                                                     │ │
│            │  │  Gejala G09 merupakan premis ke-2 dari Rule R4      │ │
│            │  │  dengan bobot CF Pakar = 0.88                       │ │
│            │  │                                                     │ │
│            │  └─────────────────────────────────────────────────────┘ │
│            │                                                           │
│            │                            [→ Lanjut]                     │
│            │                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Layar Hasil Diagnosis

```
┌─────────────────────────────────────────────────────────────────────────┐
│ [SIDEBAR]  │                  HASIL DIAGNOSIS                          │
│            │                                                           │
│            │  Konsultasi selesai — 3 kemungkinan kerusakan ditemukan   │
│            │                                                           │
│            │  ┌── #1 DIAGNOSIS UTAMA ────────────────────── [90%] ──┐ │
│            │  │ [circle-check] TERBUKTI                              │ │
│            │  │                                                      │ │
│            │  │ K01 — Adaptor/Charger Rusak                          │ │
│            │  │                                                      │ │
│            │  │ Penyebab: Suplai daya adaptor tidak stabil           │ │
│            │  │ Solusi:  Periksa output adaptor, coba charger lain   │ │
│            │  │                                                      │ │
│            │  │ ████████████████████████████████████████░░  90%      │ │
│            │  │                                                      │ │
│            │  │ [(i) Bagaimana diagnosis ini diperoleh?]             │ │
│            │  │ ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐ │ │
│            │  │   Rule R1 [CF Pakar = 0.90]                        │ │
│            │  │ │ ├─ G01: CF=0.8  ├─ G02: CF=0.6  ├─ G18: CF=1.0 │ │ │
│            │  │   Step 1: combine(0.8,0.6) = 0.92                  │ │
│            │  │ │ Step 2: combine(0.92,1.0) = 1.00                 │ │ │
│            │  │   CF Final = 0.90 × 1.00 = 0.90                   │ │
│            │  │ └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘ │ │
│            │  └──────────────────────────────────────────────────────┘ │
│            │                                                           │
│            │  ┌── #2 ──────────────────────────────────── [83%] ──┐  │
│            │  │ K04 — Overheating Sistem Pendingin                 │  │
│            │  │ ...                                                │  │
│            │  └────────────────────────────────────────────────────┘  │
│            │                                                           │
│            │  ─── Visualisasi Pohon Inferensi ───────────────────────  │
│            │                                                           │
│            │       [K01]●───R1──┬──G01 (0.8)                          │
│            │                    ├──G02 (0.6)                          │
│            │                    └──G18 (1.0)                          │
│            │       [K02]✗───R2──┬──G03 (0.0) ← GAGAL                 │
│            │       [K03]○       (tidak dievaluasi karena skip)        │
│            │       [K04]●───R4──┬──G08 (0.8)                          │
│            │                    ├──G09 (0.6)                          │
│            │                    └──G10 (0.8)                          │
│            │       ...                                                │
│            │                                                           │
│            │  ● = terbukti (hijau)   ✗ = gagal (merah)               │
│            │  ○ = tidak dievaluasi (abu-abu)                          │
│            │                                                           │
│            │  [↻ Konsultasi Ulang]                                    │
│            │                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. UX Flow (Alur Backward Chaining)

### 4.1 Flow Diagram Step-by-Step

```
START
  │
  ▼
┌─────────────────────────────┐
│ [1] User membuka aplikasi   │
│     Halaman Beranda tampil  │
└──────────────┬──────────────┘
               │ Klik [▶ Mulai Konsultasi]
               ▼
┌─────────────────────────────┐
│ [2] Engine inisialisasi     │
│     Hipotesis aktif = K01   │
│     Cari Rule → R1          │
│     Premis R1 = [G01,G02,G18]│
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ [3] Tampilkan pertanyaan    │◄─────────────────────────────┐
│     gejala pertama dari     │                              │
│     premis rule aktif       │                              │
│                             │                              │
│     Progress bar: K[n]/10   │                              │
│     Teks gejala: G[nn]      │                              │
│     Opsi CF: 5 card         │                              │
│     + Tombol [? Mengapa?]   │                              │
└──────────────┬──────────────┘                              │
               │                                             │
               │ User memilih CF                             │
               ▼                                             │
┌─────────────────────────────┐                              │
│ [4] EVALUASI JAWABAN        │                              │
│                             │                              │
│  ┌───── CF = 0.0? ────┐    │                              │
│  │                     │    │                              │
│  ▼ YA                  ▼ TIDAK                             │
│                                                            │
│ ┌──────────────┐  ┌──────────────────────┐                │
│ │[5] SHORT-    │  │[6] Simpan CF User    │                │
│ │CIRCUIT!      │  │    Masih ada premis? │                │
│ │              │  │    ┌──────┐ ┌──────┐ │                │
│ │Hipotesis K[n]│  │    │ YA   │ │TIDAK │ │                │
│ │dinyatakan    │  │    └──┬───┘ └──┬───┘ │                │
│ │GAGAL         │  │       │        │     │                │
│ │              │  │       │        ▼     │                │
│ │Skip semua    │  │       │  ┌──────────┐│                │
│ │premis tersisa│  │       │  │[7] Hitung││                │
│ └──────┬───────┘  │       │  │CF combine││                │
│        │          │       │  │CF final  ││                │
│        │          │       │  │K[n]=     ││                │
│        │          │       │  │TERBUKTI  ││                │
│        │          └───────│──└────┬─────┘│                │
│        │                  │      │       │                │
└────────┼──────────────────┘      │       │                │
         │                         │       │                │
         │◄────────────────────────┘       │                │
         │                                 │                │
         ▼                                 │ Lanjut ke      │
┌─────────────────────────────┐            │ premis         │
│ [8] Masih ada hipotesis?    │            │ berikutnya     │
│     ┌──────┐  ┌──────┐     │            └────────────────┘
│     │ YA   │  │TIDAK │     │                     │
│     └──┬───┘  └──┬───┘     │     Kembali ke [3] ─┘
│        │         │          │
│  K[n+1]│    ┌────▼────────┐ │
│  lanjut│    │[9] SELESAI  │ │
│        │    │Sort ranking │ │
│        │    │by CF desc   │ │
│        │    │Tampilkan    │ │
│        │    │halaman HASIL│ │
│        │    └─────────────┘ │
└────┬───┘────────────────────┘
     │
     └──── Kembali ke [2] dengan hipotesis berikutnya
```

### 4.2 Skenario Short-Circuit (Early Termination)

| Step | Event | UI Response |
|---|---|---|
| 1 | Engine evaluasi K02 via R2, premis pertama = G03 | Tampilkan pertanyaan G03 |
| 2 | User pilih CF = **0.0** (Tidak) | Card "Tidak" ter-select (border merah) |
| 3 | User klik [→ Lanjut] | — |
| 4 | **SHORT-CIRCUIT:** Engine langsung skip G04, G05 | Animasi: progress bar K02 → merah, lompat ke K03 |
| 5 | Engine evaluasi K03 via R3 | Tampilkan pertanyaan G06 (premis R3) |

**Feedback visual short-circuit:** Progress bar segment K02 berubah merah, toast notification kecil: *"Hipotesis K02 gugur — lanjut ke K03"* (muncul 2 detik, lalu fade out).

---

## 5. Responsive Design

### 5.1 Breakpoints

| Breakpoint | Lebar | Target Device |
|---|---|---|
| **Mobile** | < 768px | Smartphone (portrait) |
| **Tablet** | 768px – 1024px | Tablet, smartphone landscape |
| **Desktop** | > 1024px | Laptop, monitor |

### 5.2 Adaptasi per Breakpoint

| Komponen | Desktop (> 1024px) | Mobile (< 768px) |
|---|---|---|
| **Sidebar** | Persistent, lebar 250px | Collapsed (hamburger menu), overlay saat dibuka |
| **CF User Cards** | 5 card horizontal (flexbox row) | 5 card vertical stack (flexbox column), full-width |
| **Card Hasil** | Max-width 800px, centered | Full-width, padding 12px |
| **Pohon Inferensi** | Render full Graphviz, horizontal scroll jika perlu | Simplified text-based tree, atau horizontal scroll container |
| **Progress Bar** | Inline text "K04 / K10" + bar | Bar only, teks di atas bar |
| **Expander Why/How** | Inline di bawah pertanyaan | Full-width accordion |
| **Tombol Lanjut** | Kanan bawah, ukuran normal | Full-width sticky bottom, ukuran besar (min-height 48px per WCAG) |
| **Teks Gejala** | Font 16px | Font 16px (tidak diperkecil — WCAG minimum) |
| **Spacing** | Padding 24px | Padding 16px |

### 5.3 Layout Sketsa Mobile

```
┌──────────────────────┐
│ [≡]  Laptop Diagnostic Expert  │  ← Hamburger menu
├──────────────────────┤
│                      │
│ Evaluasi: K04        │
│ ████████░░░ 4/10     │
│                      │
│ ┌──────────────────┐ │
│ │ G09 — Laptop mati│ │
│ │ sendiri setelah  │ │
│ │ beberapa menit   │ │
│ └──────────────────┘ │
│                      │
│ ┌──────────────────┐ │
│ │ ╳ Tidak    (0.0) │ │
│ └──────────────────┘ │
│ ┌──────────────────┐ │
│ │ ~ Kurang   (0.4) │ │
│ └──────────────────┘ │
│ ┌──────────────────┐ │
│ │       ...        │ │
│ └──────────────────┘ │
│ ┌──────────────────┐ │
│ │ ◉ Sangat   (1.0) │ │
│ └──────────────────┘ │
│                      │
│ [? Mengapa?]         │
│                      │
│ ┌──────────────────┐ │
│ │    → Lanjut      │ │  ← sticky bottom
│ └──────────────────┘ │
└──────────────────────┘
```

### 5.4 Aksesibilitas (WCAG 2.1 Level AA)

| Kriteria WCAG | Implementasi |
|---|---|
| **1.4.3 Contrast (AA)** | Semua teks memenuhi rasio kontras minimum 4.5:1 (body) dan 3:1 (large text) |
| **1.4.11 Non-text Contrast** | UI components (tombol, card CF, progress bar) memiliki kontras ≥ 3:1 terhadap background |
| **2.1.1 Keyboard** | Semua elemen interaktif accessible via keyboard (Tab, Enter, Arrow keys untuk radio group) |
| **2.4.7 Focus Visible** | Focus ring cyan 3px pada semua elemen interaktif |
| **2.5.5 Target Size** | Semua target sentuh minimal 44×44px (mobile) |
| **3.3.2 Labels** | Setiap input memiliki label yang terlihat dan `aria-label` |

---

> *Dokumen UI Design Specification disusun berdasarkan standar WCAG 2.1 Level AA untuk proyek Laptop Diagnostic Expert — Sistem Pakar Diagnosis Kerusakan Laptop. Versi 1.0 — Maret 2026.*
