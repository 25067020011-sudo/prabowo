"""
Scraper berita kasus penyadapan Prabowo -> CSV.

Menyimpan metadata saja (judul, tanggal, URL, sumber, deskripsi singkat),
bukan teks artikel utuh.

Pemakaian:
    pip install requests beautifulsoup4
    python scrape_penyadapan.py
    python scrape_penyadapan.py --out data.csv --delay 2 --max-articles 200
    python scrape_penyadapan.py --ignore-robots
"""

import argparse
import csv
import json
import re
import signal
import sys
import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

# Halaman awal (tag/ringkasan) yang memuat link berita terkait.
SEED_URLS = [
    "https://www.jawapos.com/tag/prabowo-disadap",
    "https://www.jawapos.com/tag/tersangka-penyadapan",
    "https://www.antaranews.com/berita/5830319/hukum-kemarin-lsp-tersangka-hingga-prabowo-tahu-disadap",
    "https://www.jpnn.com/news/prabowo-tahu-disadap-dari-laporan-kapolri-jenderal-suyudi",
    "https://www.viva.co.id/berita/nasional/1941746-prabowo-hingga-ribuan-nomor-telepon-diduga-disadap-dpr-didesak-bentuk-pansus-penyadapan",
]

# Domain yang diizinkan untuk dikunjungi.
ALLOWED_DOMAINS = {
    "www.jawapos.com", "jawapos.com",
    "www.antaranews.com", "antaranews.com",
    "www.jpnn.com", "jpnn.com",
    "www.viva.co.id", "viva.co.id",
    "news.okezone.com", "okezone.com",
}

# Kata kunci untuk relevansi artikel & link.
KEYWORDS = re.compile(r"sadap|penyadapan|disadap|intersep", re.IGNORECASE)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
}

_robots_cache = {}


def is_allowed_by_robots(session, url, user_agent, timeout=10):
    """
    Cek robots.txt menggunakan session dengan header kustom.
    Jika robots.txt 404 (tidak ditemukan), dianggap diizinkan (standar web).
    Jika 403 atau timeout, fallback diizinkan dengan peringatan agar tidak memblokir semua scraping.
    """
    p = urlparse(url)
    base = f"{p.scheme}://{p.netloc}"

    if base not in _robots_cache:
        rp = RobotFileParser()
        robots_url = f"{base}/robots.txt"
        try:
            res = session.get(robots_url, timeout=timeout)
            if res.status_code == 200:
                rp.parse(res.text.splitlines())
                _robots_cache[base] = rp
            elif res.status_code == 404:
                # 404 artinya tidak ada pembatasan robots.txt
                _robots_cache[base] = True
            else:
                # 403 / error lain: sering terjadi jika CDN memblokir bot
                print(f"[robots.txt {res.status_code}] {base} -> fallback: izinkan")
                _robots_cache[base] = True
        except Exception as e:
            print(f"[robots.txt error] {base} ({e}) -> fallback: izinkan")
            _robots_cache[base] = True

    cached = _robots_cache[base]
    if cached is True:
        return True
    if cached is False:
        return False
    return cached.can_fetch(user_agent, url)


def fetch(session, url, delay, check_robots=True):
    """Fetch URL dengan penundaan dan error handling."""
    if check_robots and not is_allowed_by_robots(session, url, session.headers.get("User-Agent", "")):
        print(f"[skip robots] {url}")
        return None
    time.sleep(delay)
    try:
        r = session.get(url, timeout=20)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"[gagal] {url} -> {e}")
        return None


def get_meta(soup, *names):
    """Ambil konten dari meta tag berdasarkan property atau name."""
    for n in names:
        tag = soup.find("meta", attrs={"property": n}) or soup.find("meta", attrs={"name": n})
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def extract_date(soup):
    """Ekstraksi tanggal publikasi dari meta tag, JSON-LD, atau elemen HTML time."""
    # 1. Dari meta tag umum
    date = get_meta(
        soup,
        "article:published_time",
        "article:modified_time",
        "datePublished",
        "pubdate",
        "publishdate",
        "og:updated_time",
    )
    if date:
        return date

    # 2. Dari JSON-LD (<script type="application/ld+json">)
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            if not script.string:
                continue
            data = json.loads(script.string.strip())
            # Jika JSON-LD berupa array atau object
            items = data if isinstance(data, list) else [data]
            for item in items:
                if not isinstance(item, dict):
                    continue
                if "datePublished" in item:
                    return str(item["datePublished"])
                # Kadang ada di dalam graph: {"@graph": [...]}
                if "@graph" in item and isinstance(item["@graph"], list):
                    for g in item["@graph"]:
                        if isinstance(g, dict) and "datePublished" in g:
                            return str(g["datePublished"])
        except (json.JSONDecodeError, TypeError, KeyError):
            continue

    # 3. Dari tag <time>
    time_tag = soup.find("time")
    if time_tag:
        if time_tag.get("datetime"):
            return time_tag["datetime"].strip()
        text = time_tag.get_text(" ", strip=True)
        if text:
            return text

    return ""


def extract_links(html, base_url):
    """Ambil link kandidat artikel yang relevan dari sebuah halaman."""
    soup = BeautifulSoup(html, "html.parser")
    found = {}
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"]).split("#")[0]
        p = urlparse(href)
        if p.scheme not in ("http", "https") or p.netloc not in ALLOWED_DOMAINS:
            continue
        # Lewati halaman tag/kategori/video/share; ambil yang mirip artikel.
        if re.search(r"/(tag|tags|video|foto|search|terkini|terpopuler)(/|$)", p.path):
            continue
        if "api.whatsapp.com" in href or len(p.path.strip("/")) < 8:
            continue
        text = a.get_text(" ", strip=True)
        if KEYWORDS.search(href) or KEYWORDS.search(text):
            found[href] = text
    return found


def parse_article(html, url):
    """Ekstraksi metadata artikel: judul, tanggal, deskripsi, sumber."""
    soup = BeautifulSoup(html, "html.parser")

    # Judul
    title = get_meta(soup, "og:title", "twitter:title")
    if not title:
        h1 = soup.find("h1")
        title = h1.get_text(" ", strip=True) if h1 else ""

    # Tanggal
    date = extract_date(soup)

    # Deskripsi
    desc = get_meta(soup, "og:description", "twitter:description", "description")
    if desc:
        desc = re.sub(r"\s+", " ", desc).strip()

    return {
        "url": url,
        "source": urlparse(url).netloc.replace("www.", ""),
        "title": title,
        "published": date,
        "description": desc[:300],
    }


def save_results(rows, filepath, also_export_excel=False):
    """Simpan list row ke file CSV atau Excel (.xlsx)."""
    seen, unique = set(), []
    for r in rows:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    # Simpan ke Excel jika ekstensi .xlsx atau flag also_export_excel aktif
    if filepath.endswith(".xlsx") or also_export_excel:
        excel_path = filepath if filepath.endswith(".xlsx") else filepath.rsplit(".", 1)[0] + ".xlsx"
        try:
            import pandas as pd
            df = pd.DataFrame(unique)
            df.to_excel(excel_path, index=False)
            print(f"[Export] Berhasil menyimpan file Excel ke: {excel_path}")
        except Exception as e:
            print(f"[Peringatan] Gagal menyimpan format Excel ({e}).")

    # Selalu simpan ke CSV jika bukan .xlsx saja
    if not filepath.endswith(".xlsx"):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["url", "source", "title", "published", "description"])
            w.writeheader()
            w.writerows(unique)

    return len(unique)


def main():
    ap = argparse.ArgumentParser(description="Scraper metadata berita kasus penyadapan Prabowo.")
    ap.add_argument("--out", default="penyadapan_prabowo.csv", help="Nama file output CSV atau Excel (.xlsx) (default: penyadapan_prabowo.csv)")
    ap.add_argument("--delay", type=float, default=2.0, help="Jeda waktu antar request dalam detik (default: 2.0)")
    ap.add_argument("--max-articles", type=int, default=150, help="Maksimal artikel yang diambil (default: 150)")
    ap.add_argument("--ignore-robots", action="store_true", help="Abaikan pengecekan robots.txt jika terhambat CDN")
    ap.add_argument("--excel", action="store_true", help="Simpan salinan dalam format Excel (.xlsx) sekaligus")
    args = ap.parse_args()

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    candidates = {}
    rows = []

    # Penanganan Ctrl+C (Graceful exit) agar data yang sudah di-scrape tidak hilang
    def handle_interrupt(sig, frame):
        print(f"\n[Interupsi] Pengambilan dihentikan pengguna. Menyimpan {len(rows)} data yang telah terkumpul...")
        if rows:
            saved_count = save_results(rows, args.out, also_export_excel=args.excel)
            print(f"Data tersimpan: {saved_count} artikel di {args.out}")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)

    print("=== [1/3] Mengumpulkan link dari halaman awal (seed URLs) ===")
    for seed in SEED_URLS:
        html = fetch(session, seed, args.delay, check_robots=not args.ignore_robots)
        if not html:
            continue
        # Catatan: seed yang berupa halaman tag tidak dimasukkan sebagai artikel
        is_seed_tag = bool(re.search(r"/(tag|tags)/", urlparse(seed).path))
        if not is_seed_tag:
            candidates.setdefault(seed, "")

        extracted = extract_links(html, seed)
        for link, text in extracted.items():
            candidates.setdefault(link, text)
        print(f"[seed] {seed} -> total kandidat terkumpul: {len(candidates)}")

    print(f"\n=== [2/3] Mengambil metadata dari maksimal {args.max_articles} kandidat ===")
    processed = 0
    candidate_urls = list(candidates.keys())

    while candidate_urls and processed < args.max_articles:
        url = candidate_urls.pop(0)
        processed += 1
        html = fetch(session, url, args.delay, check_robots=not args.ignore_robots)
        if not html:
            continue

        row = parse_article(html, url)
        if row["title"] and (KEYWORDS.search(row["title"]) or KEYWORDS.search(row["description"]) or KEYWORDS.search(url)):
            rows.append(row)
            print(f"[{len(rows)}/{args.max_articles}] {row['source']} | {row['title'][:70]}")

            # BFS discovery: perluas kandidat dari artikel terkait jika target belum tercapai
            if len(candidate_urls) < args.max_articles * 2:
                more_links = extract_links(html, url)
                for link, text in more_links.items():
                    if link not in candidates:
                        candidates[link] = text
                        candidate_urls.append(link)

    print(f"\n=== [3/3] Menyimpan hasil ===")
    saved_count = save_results(rows, args.out, also_export_excel=args.excel)
    print(f"Selesai! {saved_count} artikel unik berhasil disimpan ke '{args.out}'.")


if __name__ == "__main__":
    main()
