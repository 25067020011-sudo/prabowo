# Proyek Scraping Kasus Penyadapan Prabowo

Repositori ini memuat skrip scraper untuk mengumpulkan metadata berita (judul, tanggal publikasi, ringkasan, URL, dan sumber) terkait isu/kasus penyadapan ponsel Prabowo dari portal berita nasional Indonesia.

## Struktur Berkas

- [scrape_penyadapan.py](file:///Users/jevin/Downloads/prabowo/prabowo/scrape_penyadapan.py) — Skrip utama web scraper (mendukung ekspor CSV dan Excel `.xlsx`).
- [baca_excel.py](file:///Users/jevin/Downloads/prabowo/prabowo/baca_excel.py) — Skrip pembaca data hasil scraping berformat Excel menggunakan pandas.
- [.gitignore](file:///Users/jevin/Downloads/prabowo/prabowo/.gitignore) — Mengabaikan cache python dan file output data CSV/Excel.

## Kebutuhan Sistem & Dependensi

Pastikan paket berikut telah terinstal di environment Python:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## Penggunaan Scraper

### 1. Menjalankan Scraper Standar (Output CSV)
```bash
python3 scrape_penyadapan.py
```
Hasil akan disimpan di `penyadapan_prabowo.csv`.

### 2. Menyimpan Langsung ke Format Excel (`.xlsx`)
```bash
python3 scrape_penyadapan.py --out data.xlsx
```
Atau simpan CSV sekaligus Excel:
```bash
python3 scrape_penyadapan.py --out data.csv --excel
```

### 3. Mengatur Parameter Tambahan
- `--delay <detik>`: Jeda waktu antar request (default: `2.0`).
- `--max-articles <jumlah>`: Batas maksimal artikel yang dikumpulkan (default: `150`).
- `--ignore-robots`: Mengabaikan cek `robots.txt` jika situs sasaran menerapkan proteksi Cloudflare/CDN ketat.

Contoh:
```bash
python3 scrape_penyadapan.py --out data.xlsx --delay 2.5 --max-articles 100 --ignore-robots
```

## Membaca Hasil di Python

Setelah `data.xlsx` terbentuk, jalankan:
```bash
python3 baca_excel.py
```
