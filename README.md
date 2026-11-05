# Technical Test

Repo ini berisi tiga tugas. Pemetaan file:

| Tugas | Isi | File |
| --- | --- | --- |
| Task 1 | Implementasi cosine similarity | [`similarity.py`](similarity.py) |
| Task 2 | Desain arsitektur OCR invoice di AWS (penjelasan + diagram) | [`Task 2.md`](Task%202.md), [`Task 2.drawio`](Task%202.drawio) |
| Task 3 | Backend FastAPI sentiment analysis (README ini) | `app/`, `tests/`, `Dockerfile`, `requirements*.txt` |

---

# Task 3 — Sentiment Analysis API

Backend FastAPI untuk sentiment analysis customer feedback. Endpoint menerima teks, menjalankan model HuggingFace, lalu mengembalikan sentimen (`positive`/`negative`) beserta confidence.

Model: [`distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english).

## Struktur

```
app/
  main.py       # API layer (routing, error handling)
  schemas.py    # request/response validation
  inference.py  # logic inference model (dipisah dari API)
tests/
  test_api.py
Dockerfile
requirements.txt
requirements-dev.txt
```

## Jalankan lokal

Butuh Python 3.12.

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

API di `http://127.0.0.1:8000`. Dokumentasi interaktif: `/docs`.

Model diunduh saat startup pertama (butuh koneksi internet, disimpan di cache HF).

## Uji API

```bash
curl http://127.0.0.1:8000/health
# {"status":"healthy"}

curl -X POST http://127.0.0.1:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"The product is amazing and works perfectly!\"}"
# {"text":"The product is amazing and works perfectly!","sentiment":"positive","confidence":0.9999}
```

## Test

```bash
pytest
```

Kasus: health, prediksi positif, prediksi negatif, trim spasi, teks kosong (422), field `text` hilang (422), teks terlalu panjang (422).

## Docker

```bash
docker build -t sentiment-api .
docker run --rm -p 8000:8000 sentiment-api
```

Model sudah diunduh saat build, jadi container tidak perlu internet saat runtime. Jalankan uji API di atas terhadap `http://127.0.0.1:8000`.

## Endpoint

### GET /health

```json
{"status": "healthy"}
```

### POST /predict

Request:

```json
{"text": "The product is amazing and works perfectly!"}
```

Response `200`:

```json
{
  "text": "The product is amazing and works perfectly!",
  "sentiment": "positive",
  "confidence": 0.9999
}
```

Aturan validasi:
- `text` wajib, tidak boleh kosong/hanya spasi, maksimal 5000 karakter, spasi di-trim.
- Input tidak valid -> `422`.
- Model gagal dimuat -> `503`; inference gagal -> `500`.
