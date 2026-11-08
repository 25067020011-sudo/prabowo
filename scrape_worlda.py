#!/usr/bin/env python3
"""
Scraper untuk World A.LIVE (https://worlda.live/indonesia/newspaper)
Mengekstrak:
1. Edisi Koran Harian terkini (Lead story, secondary stories, briefing, dan index berita lainnya).
2. Detail liputan khusus topik Penyadapan Presiden Prabowo (114 artikel dengan timestamp jam dan media outlet).
3. Mengekspor dataset ke format CSV, JSON, serta format input pipeline World A.LIVE intelligence.
"""

import sys
import os
import json
import re
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

BASE_URL = "https://worlda.live"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "id,en;q=0.9",
}

def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")

def extract_entities_from_title(title):
    entities = []
    text_lower = title.lower()
    
    if "prabowo" in text_lower or "presiden" in text_lower:
        entities.append("Prabowo Subianto")
    if "listyo" in text_lower or "kapolri" in text_lower or "polri" in text_lower or "polisi" in text_lower:
        entities.append("Polri / Kapolri")
    if "bahlil" in text_lower:
        entities.append("Bahlil Lahadalia")
    if "jokowi" in text_lower:
        entities.append("Joko Widodo")
    if "habiburokhman" in text_lower or "gerindra" in text_lower:
        entities.append("Habiburokhman / Gerindra")
    if "hasto" in text_lower or "pdip" in text_lower:
        entities.append("Hasto Kristiyanto / PDIP")
    if "andi gani" in text_lower or "kspsi" in text_lower:
        entities.append("Andi Gani / KSPSI")
    if "mk" in text_lower or "mahkamah konstitusi" in text_lower:
        entities.append("Mahkamah Konstitusi")
    if "pakar" in text_lower or "akademisi" in text_lower or "ahli" in text_lower:
        entities.append("Pakar Hukum / Akademisi")
    if "makar" in text_lower:
        entities.append("Isu Makar")
    if "sadap" in text_lower or "penyadapan" in text_lower:
        entities.append("Penyadapan Ilegal")
        
    if not entities:
        entities.append("Isu Keamanan Nasional")
    return "; ".join(entities)

def scrape_newspaper():
    print(f"[*] Mengambil data dari {BASE_URL}/indonesia/newspaper ...")
    html = fetch_html(f"{BASE_URL}/indonesia/newspaper")
    soup = BeautifulSoup(html, "html.parser")
    
    meta_title = soup.title.string.strip() if soup.title else ""
    meta_desc = soup.find("meta", {"name": "description"})
    meta_desc_text = meta_desc["content"].strip() if meta_desc else ""
    
    print(f"[+] Judul Edisi: {meta_title}")
    print(f"[+] Ringkasan Utama: {meta_desc_text}")
    
    articles = []
    
    # 1. Artikel Berita Utama (Articles on Page)
    for art in soup.find_all("article"):
        h = art.find(["h1", "h2", "h3"])
        p = art.find("p")
        a = art.find("a")
        if h and h.get_text(strip=True):
            title = h.get_text(strip=True)
            link = a.get("href") if a else ""
            if link.startswith("/"):
                link = BASE_URL + link
            summary = p.get_text(strip=True) if p else ""
            articles.append({
                "kategori": "Berita Utama / Sorotan",
                "judul": title,
                "ringkasan": summary,
                "url": link,
                "sumber": "World A.LIVE Edisi Koran Harian"
            })
            
    # 2. Rubrik Index (Berita lainnya)
    for sec in soup.find_all("section", class_="index"):
        for li in sec.find_all("li"):
            a = li.find("a")
            title = li.get_text(strip=True)
            link = a.get("href") if a else ""
            if link.startswith("/"):
                link = BASE_URL + link
            if title:
                articles.append({
                    "kategori": "Berita Lainnya (Index)",
                    "judul": title,
                    "ringkasan": "",
                    "url": link,
                    "sumber": "World A.LIVE Index"
                })
                
    df_newspaper = pd.DataFrame(articles).drop_duplicates(subset=["judul"])
    print(f"[+] Berhasil mengekstrak {len(df_newspaper)} tajuk koran harian.")
    return df_newspaper, meta_title, meta_desc_text

def scrape_penyadapan_topic():
    topic_url = f"{BASE_URL}/indonesia/topics/51140/2026-11-07"
    print(f"[*] Mengambil linimasa lengkap berita penyadapan dari: {topic_url} ...")
    html = fetch_html(topic_url)
    soup = BeautifulSoup(html, "html.parser")
    
    records = []
    for sec in soup.find_all("section", class_="hour"):
        hour_val = sec.get("data-h", "")
        for li in sec.find_all("li", attrs={"data-report": True}):
            rep_id = li.get("data-report", "")
            time_el = li.find("time")
            iso_time = time_el.get("datetime") if time_el else ""
            a_el = li.find("a")
            headline = ""
            if a_el:
                span_hl = a_el.find("span", class_="headline")
                headline = span_hl.get_text(strip=True) if span_hl else a_el.get_text(strip=True)
            
            raw_url = a_el.get("href") if a_el else ""
            full_url = raw_url if raw_url.startswith("http") else (BASE_URL + raw_url)
            
            outlet_el = li.find("span", class_="outlet")
            outlet = outlet_el.get_text(strip=True) if outlet_el else "Media Daring"
            
            records.append({
                "report_id": rep_id,
                "hour_wib": int(hour_val) if hour_val.isdigit() else hour_val,
                "datetime_utc": iso_time,
                "published_at": iso_time[:10] if iso_time else "2026-11-07",
                "headline": headline,
                "outlet": outlet,
                "url": full_url,
                "entities": extract_entities_from_title(headline)
            })
            
    df_topic = pd.DataFrame(records)
    print(f"[+] Berhasil mengekstrak {len(df_topic)} artikel linimasa penyadapan.")
    return df_topic

def main():
    out_dir = "output/worlda"
    os.makedirs(out_dir, exist_ok=True)
    
    # Scrape Koran
    df_newspaper, title, desc = scrape_newspaper()
    newspaper_csv = os.path.join(out_dir, "newspaper_edisi_terkini.csv")
    newspaper_json = os.path.join(out_dir, "newspaper_edisi_terkini.json")
    df_newspaper.to_csv(newspaper_csv, index=False)
    with open(newspaper_json, "w", encoding="utf-8") as f:
        json.dump({
            "edisi": title,
            "deskripsi": desc,
            "tanggal_scrape": datetime.now().isoformat(),
            "total_berita": len(df_newspaper),
            "berita": df_newspaper.to_dict(orient="records")
        }, f, indent=2, ensure_ascii=False)
    print(f"[✓] Disimpan ke {newspaper_csv} dan {newspaper_json}")
    
    # Scrape Topik Penyadapan
    df_topic = scrape_penyadapan_topic()
    topic_csv = os.path.join(out_dir, "penyadapan_prabowo_114_berita.csv")
    topic_json = os.path.join(out_dir, "penyadapan_prabowo_114_berita.json")
    df_topic.to_csv(topic_csv, index=False)
    with open(topic_json, "w", encoding="utf-8") as f:
        json.dump({
            "topik": "Penyadapan Presiden Prabowo",
            "tanggal": "2026-11-07",
            "total_artikel": len(df_topic),
            "media_populer": df_topic["outlet"].value_counts().to_dict(),
            "sebaran_jam": df_topic["hour_wib"].value_counts().sort_index().to_dict(),
            "artikel": df_topic.to_dict(orient="records")
        }, f, indent=2, ensure_ascii=False)
    print(f"[✓] Disimpan ke {topic_csv} dan {topic_json}")
    
    # Buat file kompatibel pipeline intelligence: input/articles_worlda.csv
    # format: title,url,published_at,source,entities
    df_pipeline = pd.DataFrame({
        "title": df_topic["headline"],
        "url": df_topic["url"],
        "published_at": df_topic["published_at"],
        "source": df_topic["outlet"],
        "entities": df_topic["entities"]
    })
    os.makedirs("input", exist_ok=True)
    pipeline_csv = "input/articles_worlda.csv"
    df_pipeline.to_csv(pipeline_csv, index=False)
    print(f"[✓] Format pipeline disimpan ke {pipeline_csv} (siap diproses worlda-intelligence.sh)")
    
    print("\n--- RINGKASAN HASIL SCRAPING ---")
    print(f"Total Koran Harian: {len(df_newspaper)} berita")
    print(f"Total Kasus Penyadapan: {len(df_topic)} berita")
    print("\nDistribusi 5 Media Teratas Kasus Penyadapan:")
    print(df_topic["outlet"].value_counts().head(5).to_string())

if __name__ == "__main__":
    main()

