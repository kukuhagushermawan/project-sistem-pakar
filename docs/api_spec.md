# DOKUMENTASI API RESTful — OpenAPI 3.0
## Sistem Pakar Diagnosis Kerusakan Laptop — Laptop Diagnostic Expert
### Komunikasi Frontend UI ↔ Inference Engine Backend

| Item | Detail |
|---|---|
| **Versi API** | v1.0 |
| **Tanggal** | 28 Maret 2026 |
| **Base URL** | `http://localhost:8501/api/v1` |
| **Format** | JSON (`application/json`) |
| **Standar** | OpenAPI Specification 3.0.3 |

---

## Ringkasan Endpoint

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/diagnosis/start` | Inisiasi sesi konsultasi baru, kembalikan gejala pertama |
| `POST` | `/diagnosis/answer` | Kirim jawaban CF User, dapatkan gejala berikut / hasil akhir |
| `GET` | `/diagnosis/explain/why/{gejala_id}` | Penjelasan "Mengapa gejala ini ditanyakan?" |
| `GET` | `/diagnosis/result/{session_id}` | Ambil hasil diagnosis lengkap + pohon inferensi |

---

## 1. `GET /api/v1/diagnosis/start`

### Deskripsi

Menginisiasi sesi konsultasi baru. Engine melakukan:
1. Generate `session_id` unik (UUID v4).
2. Inisialisasi Backward Chaining dari hipotesis pertama (**K01**).
3. Cari rule yang konklusinya K01 → ditemukan **R1**.
4. Ambil premis pertama R1 → **G01**.
5. Kembalikan data gejala pertama yang harus ditanyakan.

### Request

```
GET /api/v1/diagnosis/start
Content-Type: application/json
```

**Parameters:** Tidak ada.

### Response: `200 OK`

```json
{
  "status": "success",
  "data": {
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "state": "in_progress",
    "current_hypothesis": {
      "kode": "K01",
      "nama": "Adaptor/Charger Rusak",
      "index": 1,
      "total": 10
    },
    "current_rule": {
      "rule_id": "R1",
      "cf_rule": 0.90,
      "total_premises": 3,
      "current_premise_index": 1
    },
    "question": {
      "kode_gejala": "G01",
      "teks_gejala": "Laptop tidak menyala saat tombol power ditekan",
      "deskripsi_detail": "Saat tombol power ditekan, tidak ada respons apapun (tidak ada lampu, suara, atau tampilan).",
      "kategori": "daya",
      "cf_options": [
        {"value": 0.0, "label": "Tidak",        "hint": "Gejala tidak dialami"},
        {"value": 0.4, "label": "Kurang yakin",  "hint": "Kadang terasa"},
        {"value": 0.6, "label": "Cukup yakin",   "hint": "Cukup sering"},
        {"value": 0.8, "label": "Yakin",          "hint": "Jelas tampak"},
        {"value": 1.0, "label": "Sangat yakin",   "hint": "Benar-benar terjadi"}
      ]
    },
    "progress": {
      "hypotheses_evaluated": 0,
      "hypotheses_total": 10,
      "percentage": 0
    }
  },
  "timestamp": "2026-03-28T17:00:00+07:00"
}
```

### Response: `500 Internal Server Error`

```json
{
  "status": "error",
  "error": {
    "code": "ENGINE_INIT_FAILED",
    "message": "Gagal menginisialisasi inference engine. Knowledge Base tidak dapat dimuat.",
    "detail": "ModuleNotFoundError: No module named 'knowledge_base.frames'"
  },
  "timestamp": "2026-03-28T17:00:00+07:00"
}
```

---

## 2. `POST /api/v1/diagnosis/answer`

### Deskripsi

Menerima jawaban CF User untuk gejala aktif, memproses Backward Chaining, lalu mengembalikan **salah satu** dari:
- **Gejala berikutnya** — jika masih ada premis/hipotesis yang perlu dievaluasi.
- **Hasil akhir diagnosis** — jika seluruh hipotesis (K01–K10) telah selesai dievaluasi.

**Logika internal:**
1. Simpan `cf_user` untuk `kode_gejala` ke cache jawaban.
2. Jika `cf_user == 0.0` → **short-circuit**: hipotesis aktif GAGAL, lompat ke hipotesis berikutnya.
3. Jika `cf_user > 0.0` dan masih ada premis → lanjut ke gejala berikutnya dalam rule.
4. Jika semua premis rule terpenuhi → hitung CF combine & CF final, hipotesis TERBUKTI.
5. Jika ada hipotesis tersisa → lanjut ke hipotesis berikutnya.
6. Jika K10 sudah dievaluasi → kembalikan hasil akhir.

### Request

```
POST /api/v1/diagnosis/answer
Content-Type: application/json
```

**Request Body:**

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "kode_gejala": "G01",
  "cf_user": 0.8
}
```

| Field | Tipe | Wajib | Validasi |
|---|---|---|---|
| `session_id` | `string` (UUID) | Ya | Harus valid, session aktif |
| `kode_gejala` | `string` | Ya | Format `G[01-25]`, harus cocok dengan gejala yang sedang ditanyakan |
| `cf_user` | `number` | Ya | Hanya nilai: `0.0`, `0.4`, `0.6`, `0.8`, `1.0` |

### Response A: `200 OK` — Gejala Berikutnya

Dikembalikan jika masih ada gejala/hipotesis yang perlu dievaluasi.

```json
{
  "status": "success",
  "data": {
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "state": "in_progress",
    "event": "next_question",
    "short_circuit": false,
    "current_hypothesis": {
      "kode": "K01",
      "nama": "Adaptor/Charger Rusak",
      "index": 1,
      "total": 10
    },
    "current_rule": {
      "rule_id": "R1",
      "cf_rule": 0.90,
      "total_premises": 3,
      "current_premise_index": 2
    },
    "question": {
      "kode_gejala": "G02",
      "teks_gejala": "Lampu indikator charger tidak menyala",
      "deskripsi_detail": "Saat adaptor/charger dipasang ke laptop, lampu LED pada adaptor atau laptop tidak menyala.",
      "kategori": "daya",
      "cf_options": [
        {"value": 0.0, "label": "Tidak",        "hint": "Gejala tidak dialami"},
        {"value": 0.4, "label": "Kurang yakin",  "hint": "Kadang terasa"},
        {"value": 0.6, "label": "Cukup yakin",   "hint": "Cukup sering"},
        {"value": 0.8, "label": "Yakin",          "hint": "Jelas tampak"},
        {"value": 1.0, "label": "Sangat yakin",   "hint": "Benar-benar terjadi"}
      ]
    },
    "progress": {
      "hypotheses_evaluated": 0,
      "hypotheses_total": 10,
      "percentage": 5
    }
  },
  "timestamp": "2026-03-28T17:00:05+07:00"
}
```

### Response B: `200 OK` — Short-Circuit (Hipotesis Gagal)

Dikembalikan ketika `cf_user == 0.0` → hipotesis aktif langsung GAGAL dan engine lompat ke hipotesis berikutnya.

```json
{
  "status": "success",
  "data": {
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "state": "in_progress",
    "event": "hypothesis_failed",
    "short_circuit": true,
    "failed_hypothesis": {
      "kode": "K02",
      "nama": "Baterai Rusak/Drop",
      "reason": "Gejala G03 tidak dialami (CF User = 0.0). Premis tidak terpenuhi."
    },
    "current_hypothesis": {
      "kode": "K03",
      "nama": "RAM Bermasalah",
      "index": 3,
      "total": 10
    },
    "current_rule": {
      "rule_id": "R3",
      "cf_rule": 0.80,
      "total_premises": 2,
      "current_premise_index": 1
    },
    "question": {
      "kode_gejala": "G06",
      "teks_gejala": "Terdengar bunyi beep saat startup",
      "deskripsi_detail": "Laptop mengeluarkan bunyi beep berulang saat dinyalakan, sebelum tampilan muncul.",
      "kategori": "daya",
      "cf_options": [
        {"value": 0.0, "label": "Tidak",        "hint": "Gejala tidak dialami"},
        {"value": 0.4, "label": "Kurang yakin",  "hint": "Kadang terasa"},
        {"value": 0.6, "label": "Cukup yakin",   "hint": "Cukup sering"},
        {"value": 0.8, "label": "Yakin",          "hint": "Jelas tampak"},
        {"value": 1.0, "label": "Sangat yakin",   "hint": "Benar-benar terjadi"}
      ]
    },
    "progress": {
      "hypotheses_evaluated": 2,
      "hypotheses_total": 10,
      "percentage": 20
    }
  },
  "timestamp": "2026-03-28T17:00:15+07:00"
}
```

### Response C: `200 OK` — Konsultasi Selesai (Hasil Akhir)

Dikembalikan ketika **seluruh hipotesis K01–K10 telah selesai dievaluasi**.

```json
{
  "status": "success",
  "data": {
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "state": "completed",
    "event": "consultation_complete",
    "summary": {
      "total_hypotheses": 10,
      "proven": 3,
      "failed": 7,
      "total_questions_asked": 18
    },
    "ranking": [
      {
        "rank": 1,
        "kode_kerusakan": "K01",
        "nama_kerusakan": "Adaptor/Charger Rusak",
        "cf_final": 0.90,
        "cf_percentage": "90%",
        "status": "TERBUKTI",
        "penyebab": "Suplai daya adaptor tidak stabil",
        "solusi_singkat": "Periksa output adaptor, coba charger lain",
        "solusi_detail": "1. Periksa lampu indikator adaptor.\n2. Coba gunakan adaptor lain yang kompatibel.\n3. Periksa kabel apakah ada kerusakan fisik.",
        "rules_triggered": ["R1"],
        "how_explanation": {
          "rule_id": "R1",
          "cf_rule": 0.90,
          "premises": [
            {"kode_gejala": "G01", "teks": "Laptop tidak menyala saat tombol power ditekan", "cf_user": 0.8},
            {"kode_gejala": "G02", "teks": "Lampu indikator charger tidak menyala", "cf_user": 0.6},
            {"kode_gejala": "G18", "teks": "Adaptor atau kabel charger longgar/tidak stabil", "cf_user": 1.0}
          ],
          "cf_steps": [
            "CF_combine(0.8, 0.6) = 0.8 + 0.6 × (1 - 0.8) = 0.92",
            "CF_combine(0.92, 1.0) = 0.92 + 1.0 × (1 - 0.92) = 1.00",
            "CF_final = CF_pakar × CF_user_kombinasi = 0.90 × 1.00 = 0.90"
          ],
          "cf_user_combined": 1.00,
          "cf_final": 0.90
        }
      },
      {
        "rank": 2,
        "kode_kerusakan": "K04",
        "nama_kerusakan": "Overheating Sistem Pendingin",
        "cf_final": 0.83,
        "cf_percentage": "83%",
        "status": "TERBUKTI",
        "penyebab": "Kipas/heatsink/thermal paste buruk",
        "solusi_singkat": "Bersihkan kipas, ganti thermal paste",
        "rules_triggered": ["R4"],
        "how_explanation": { "...": "..." }
      }
    ],
    "inference_tree": "... (lihat bagian Pohon Inferensi di bawah)",
    "trace_log": "... (lihat bagian Trace Log di bawah)"
  },
  "timestamp": "2026-03-28T17:02:30+07:00"
}
```

### Error Responses

#### `400 Bad Request` — Validasi Input Gagal

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_CF_VALUE",
    "message": "Nilai cf_user tidak valid. Hanya nilai 0.0, 0.4, 0.6, 0.8, 1.0 yang diterima.",
    "field": "cf_user",
    "received": 0.5
  },
  "timestamp": "2026-03-28T17:00:10+07:00"
}
```

#### `400 Bad Request` — Gejala Tidak Sesuai

```json
{
  "status": "error",
  "error": {
    "code": "SYMPTOM_MISMATCH",
    "message": "Gejala yang dikirim (G05) tidak sesuai dengan gejala yang sedang ditanyakan (G02).",
    "expected": "G02",
    "received": "G05"
  },
  "timestamp": "2026-03-28T17:00:10+07:00"
}
```

#### `404 Not Found` — Session Tidak Ditemukan

```json
{
  "status": "error",
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "Session ID tidak ditemukan atau sudah kedaluwarsa.",
    "session_id": "invalid-uuid-here"
  },
  "timestamp": "2026-03-28T17:00:10+07:00"
}
```

#### `409 Conflict` — Session Sudah Selesai

```json
{
  "status": "error",
  "error": {
    "code": "SESSION_COMPLETED",
    "message": "Sesi konsultasi sudah selesai. Gunakan GET /diagnosis/start untuk sesi baru.",
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  },
  "timestamp": "2026-03-28T17:00:10+07:00"
}
```

---

## 3. `GET /api/v1/diagnosis/explain/why/{gejala_id}`

### Deskripsi

Mengembalikan penjelasan **"Mengapa gejala ini ditanyakan?"** — Explanation Facility (Why). Menjelaskan hubungan antara gejala aktif, rule yang sedang dievaluasi, dan hipotesis kerusakan.

### Request

```
GET /api/v1/diagnosis/explain/why/G09?session_id=a1b2c3d4-...
Content-Type: application/json
```

| Parameter | Lokasi | Tipe | Wajib | Keterangan |
|---|---|---|---|---|
| `gejala_id` | Path | `string` | Ya | Kode gejala (G01–G25) |
| `session_id` | Query | `string` | Ya | UUID session konsultasi aktif |

### Response: `200 OK`

```json
{
  "status": "success",
  "data": {
    "gejala": {
      "kode": "G09",
      "teks": "Laptop mati sendiri setelah beberapa menit penggunaan"
    },
    "explanation": {
      "why_text": "Sistem menanyakan gejala G09 (Laptop mati sendiri setelah beberapa menit) untuk mengevaluasi hipotesis kerusakan K04 — Overheating Sistem Pendingin. Gejala ini merupakan premis ke-2 dari Rule R4 dengan bobot CF Pakar = 0.88.",
      "hypothesis": {
        "kode": "K04",
        "nama": "Overheating Sistem Pendingin"
      },
      "rule": {
        "rule_id": "R4",
        "cf_rule": 0.88,
        "deskripsi": "IF laptop cepat panas (G08) AND mati sendiri (G09) AND kipas bising (G10) THEN overheating (K04)",
        "all_premises": [
          {"kode": "G08", "teks": "Laptop cepat panas",                      "status": "answered", "cf_user": 0.8},
          {"kode": "G09", "teks": "Laptop mati sendiri setelah beberapa menit","status": "current",  "cf_user": null},
          {"kode": "G10", "teks": "Kipas sangat bising / ventilasi panas",     "status": "pending",  "cf_user": null}
        ]
      },
      "reasoning": "Jika gejala ini terpenuhi (CF User > 0.0), keyakinan terhadap hipotesis K04 akan meningkat. Jika tidak (CF User = 0.0), hipotesis K04 akan langsung dinyatakan GAGAL dan sistem akan melanjutkan ke hipotesis berikutnya."
    }
  },
  "timestamp": "2026-03-28T17:00:20+07:00"
}
```

### Response: `404 Not Found`

```json
{
  "status": "error",
  "error": {
    "code": "SYMPTOM_NOT_FOUND",
    "message": "Kode gejala G99 tidak ditemukan dalam Knowledge Base.",
    "gejala_id": "G99"
  },
  "timestamp": "2026-03-28T17:00:20+07:00"
}
```

---

## 4. `GET /api/v1/diagnosis/result/{session_id}`

### Deskripsi

Mengambil hasil diagnosis lengkap beserta **pohon inferensi** dan **trace log** untuk sesi yang sudah selesai.

### Request

```
GET /api/v1/diagnosis/result/a1b2c3d4-e5f6-7890-abcd-ef1234567890
Content-Type: application/json
```

### Response: `200 OK`

Response body sama dengan **Response C** pada endpoint `POST /answer` (state: `completed`), ditambah dengan field `inference_tree` dan `trace_log` dalam format lengkap berikut:

---

## 5. Format JSON: Pohon Inferensi & Trace Log

### 5.1 Struktur `inference_tree`

Format tree yang dapat dirender oleh frontend menjadi visualisasi (Graphviz/D3.js/custom renderer).

```json
{
  "inference_tree": {
    "metadata": {
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "total_nodes": 35,
      "total_edges": 30,
      "generated_at": "2026-03-28T17:02:30+07:00"
    },
    "nodes": [
      {
        "id": "K01",
        "type": "hypothesis",
        "label": "K01 — Adaptor/Charger Rusak",
        "status": "proven",
        "cf_final": 0.90,
        "style": {"color": "#10B981", "shape": "box"}
      },
      {
        "id": "K02",
        "type": "hypothesis",
        "label": "K02 — Baterai Rusak/Drop",
        "status": "failed",
        "cf_final": 0.0,
        "style": {"color": "#EF4444", "shape": "box"}
      },
      {
        "id": "K03",
        "type": "hypothesis",
        "label": "K03 — RAM Bermasalah",
        "status": "failed",
        "cf_final": 0.0,
        "style": {"color": "#EF4444", "shape": "box"}
      },
      {
        "id": "R1",
        "type": "rule",
        "label": "R1 [CF=0.90]",
        "style": {"color": "#3B82F6", "shape": "diamond"}
      },
      {
        "id": "G01",
        "type": "symptom",
        "label": "G01: Laptop tidak menyala (CF=0.8)",
        "cf_user": 0.8,
        "style": {"color": "#06B6D4", "shape": "ellipse"}
      },
      {
        "id": "G02",
        "type": "symptom",
        "label": "G02: Lampu charger mati (CF=0.6)",
        "cf_user": 0.6,
        "style": {"color": "#06B6D4", "shape": "ellipse"}
      },
      {
        "id": "G18",
        "type": "symptom",
        "label": "G18: Adaptor longgar (CF=1.0)",
        "cf_user": 1.0,
        "style": {"color": "#06B6D4", "shape": "ellipse"}
      },
      {
        "id": "G03",
        "type": "symptom",
        "label": "G03: Hanya menyala saat charger (CF=0.0)",
        "cf_user": 0.0,
        "style": {"color": "#EF4444", "shape": "ellipse"}
      }
    ],
    "edges": [
      {"from": "K01", "to": "R1",  "label": "evaluated_by"},
      {"from": "R1",  "to": "G01", "label": "premise_1"},
      {"from": "R1",  "to": "G02", "label": "premise_2"},
      {"from": "R1",  "to": "G18", "label": "premise_3"},
      {"from": "K02", "to": "R2",  "label": "evaluated_by"},
      {"from": "R2",  "to": "G03", "label": "premise_1 [FAILED]"}
    ]
  }
}
```

### 5.2 Struktur `trace_log`

Log kronologis setiap langkah inferensi engine — untuk debugging, audit, dan Explanation Facility "Bagaimana".

```json
{
  "trace_log": [
    {
      "step": 1,
      "timestamp": "2026-03-28T17:00:01+07:00",
      "action": "EVALUATE_HYPOTHESIS",
      "hypothesis": "K01",
      "rule": "R1",
      "detail": "Mulai evaluasi hipotesis K01 via Rule R1"
    },
    {
      "step": 2,
      "timestamp": "2026-03-28T17:00:03+07:00",
      "action": "ASK_SYMPTOM",
      "hypothesis": "K01",
      "rule": "R1",
      "symptom": "G01",
      "detail": "Menanyakan gejala G01 (premis 1/3 dari R1)"
    },
    {
      "step": 3,
      "timestamp": "2026-03-28T17:00:05+07:00",
      "action": "RECEIVE_ANSWER",
      "hypothesis": "K01",
      "rule": "R1",
      "symptom": "G01",
      "cf_user": 0.8,
      "result": "CONTINUE",
      "detail": "CF User = 0.8 > 0.0 → lanjut ke premis berikutnya"
    },
    {
      "step": 6,
      "timestamp": "2026-03-28T17:00:11+07:00",
      "action": "CALCULATE_CF",
      "hypothesis": "K01",
      "rule": "R1",
      "cf_steps": [
        {"operation": "combine", "cf1": 0.8, "cf2": 0.6, "result": 0.92},
        {"operation": "combine", "cf1": 0.92, "cf2": 1.0, "result": 1.00},
        {"operation": "final",   "cf_rule": 0.90, "cf_user_combined": 1.00, "cf_final": 0.90}
      ],
      "detail": "Semua premis terpenuhi. CF Final K01 = 0.90 (90%)"
    },
    {
      "step": 7,
      "timestamp": "2026-03-28T17:00:11+07:00",
      "action": "HYPOTHESIS_PROVEN",
      "hypothesis": "K01",
      "cf_final": 0.90,
      "detail": "Hipotesis K01 TERBUKTI dengan CF = 0.90"
    },
    {
      "step": 8,
      "timestamp": "2026-03-28T17:00:12+07:00",
      "action": "EVALUATE_HYPOTHESIS",
      "hypothesis": "K02",
      "rule": "R2",
      "detail": "Mulai evaluasi hipotesis K02 via Rule R2"
    },
    {
      "step": 10,
      "timestamp": "2026-03-28T17:00:15+07:00",
      "action": "RECEIVE_ANSWER",
      "hypothesis": "K02",
      "rule": "R2",
      "symptom": "G03",
      "cf_user": 0.0,
      "result": "SHORT_CIRCUIT",
      "detail": "CF User = 0.0 → Hipotesis K02 GAGAL. Skip premis G04, G05."
    },
    {
      "step": 11,
      "timestamp": "2026-03-28T17:00:15+07:00",
      "action": "HYPOTHESIS_FAILED",
      "hypothesis": "K02",
      "cf_final": 0.0,
      "reason": "short_circuit_on_G03",
      "detail": "Hipotesis K02 GAGAL (short-circuit pada G03)"
    }
  ]
}
```

---

## 6. Ringkasan Error Codes

| HTTP Status | Error Code | Penyebab |
|---|---|---|
| `400` | `INVALID_CF_VALUE` | Nilai `cf_user` bukan salah satu dari [0.0, 0.4, 0.6, 0.8, 1.0] |
| `400` | `SYMPTOM_MISMATCH` | Kode gejala tidak sesuai dengan gejala yang sedang aktif |
| `400` | `MISSING_FIELD` | Field wajib (`session_id`, `kode_gejala`, `cf_user`) tidak ada |
| `404` | `SESSION_NOT_FOUND` | Session ID tidak valid atau sudah expired |
| `404` | `SYMPTOM_NOT_FOUND` | Kode gejala tidak ada dalam Knowledge Base |
| `409` | `SESSION_COMPLETED` | Session sudah selesai, tidak bisa submit answer lagi |
| `500` | `ENGINE_INIT_FAILED` | Knowledge Base gagal dimuat saat inisialisasi |
| `500` | `ENGINE_ERROR` | Error tidak terduga pada inference engine |

---

## 7. Catatan Implementasi untuk Streamlit

> Karena prototype Laptop Diagnostic Expert menggunakan **Streamlit** (bukan REST API server terpisah), komunikasi Frontend↔Engine terjadi via **function call langsung** (Python import), bukan HTTP request. Dokumentasi API ini berfungsi sebagai:
>
> 1. **Contract specification** — mendefinisikan format data yang dipertukarkan antar layer.
> 2. **Referensi akademik** — mendemonstrasikan pemahaman desain API RESTful.
> 3. **Future-proofing** — jika sistem di-migrate ke arsitektur client-server (FastAPI + React), kontrak API ini langsung dapat diimplementasikan.
>
> Pada implementasi Streamlit, setiap endpoint direpresentasikan sebagai **method** pada class `BackwardChainingEngine`:
>
> | API Endpoint | Streamlit Equivalent |
> |---|---|
> | `GET /diagnosis/start` | `engine = BackwardChainingEngine(); engine.start()` |
> | `POST /diagnosis/answer` | `engine.submit_answer(kode_gejala, cf_user)` |
> | `GET /diagnosis/explain/why/{id}` | `ExplanationFacility.why(symptom, hypothesis, rule)` |
> | `GET /diagnosis/result/{id}` | `engine.get_results()` + `engine.get_trace_log()` |

---

> *Dokumentasi API RESTful disusun berdasarkan OpenAPI 3.0.3 untuk proyek Laptop Diagnostic Expert — Sistem Pakar Diagnosis Kerusakan Laptop. Versi 1.0 — Maret 2026.*
