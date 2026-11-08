"""
Modul Ekstraksi Narasumber & Kutipan (FR-5 & FR-9)
Sesuai PRD: Analisis Jaringan Narasi Kasus Penyadapan Presiden

Mengekstrak narasumber, pola kutipan, dan membangun jaringan relasi bipartit:
Media Massa <---> Narasumber (Speaker)
"""

import hashlib
import json
import re
import pandas as pd

# Kamus taksonomi tipe narasumber
SPEAKER_TAXONOMY = {
    'aparat': [
        r'kapolri', r'suyudi', r'bareskrim', r'divhumas', r'propam', r'divpropam',
        r'mabes polri', r'polri', r'brimob', r'polda', r'penyidik', r'irjen', r'komjen',
        r'jenderal', r'dittipidum', r'listyo', r'sigit', r'lsp'
    ],
    'pejabat': [
        r'presiden', r'prabowo', r'yusril', r'menko', r'mensesneg', r'istana',
        r'kantor komunikasi kepresidenan', r'pco', r'hasan nasbi', r'menteri', r'pemerintah'
    ],
    'politisi': [
        r'dpr', r'komisi iii', r'pansus', r'pdip', r'gerindra', r'demokrat', r'golkar',
        r'pks', r'nasdem', r'pkb', r'habiburokhman', r'hasto', r'puan', r'dasco', r'parpol'
    ],
    'pakar': [
        r'pakar', r'pengamat', r'akademisi', r'chairul huda', r'isess', r'bambang rukminto',
        r'ahli hukum', r'analis', r'peneliti', r'guru besar'
    ],
    'anonim': [
        r'sumber internal', r'informan', r'grup wa', r'pesan berantai', r'akun x',
        r'sumber terpercaya', r'dokumen bocor', r'kabar burung', r'lingkaran istana',
        r'sumber di mako brimob', r'anonim'
    ]
}

# Pola atribusi kutipan bahasa Indonesia
QUOTE_PATTERNS = [
    r'(?:kata|ujar|tutur|ungkap|tegas|jelas|beber|ucap|sebut|tandas|papar)\s+([A-Z][a-zA-Z\s\.\,]+?)(?:,|\.|\s+bahwa|\s+di|\s+pada|\s+saat|\s+dalam)',
    r'(?:menurut|berdasarkan|merujuk pada)\s+([A-Z][a-zA-Z\s\.\,]+?)(?:,|\.|\s+bahwa|\s+di|\s+pada)',
    r'([A-Z][a-zA-Z\s\.\,]+?)\s+(?:menegaskan|mengatakan|menyatakan|menjelaskan|mengungkapkan|membeberkan|membantah|mengonfirmasi)'
]


def classify_speaker(speaker_text):
    """Menentukan kategori narasumber berdasarkan taksonomi."""
    speaker_lower = speaker_text.lower()
    for cat, patterns in SPEAKER_TAXONOMY.items():
        for pat in patterns:
            if re.search(r'\b' + pat + r'\b', speaker_lower):
                return cat
    return 'lainnya'


def extract_quotes_from_text(text):
    """Mengekstrak narasumber potensial dari teks judul / ringkasan."""
    found_speakers = []
    for pat in QUOTE_PATTERNS:
        matches = re.finditer(pat, text)
        for m in matches:
            sp = m.group(1).strip().strip(',').strip('.')
            # Filter noise panjang nama
            if 3 <= len(sp) <= 45 and not re.match(r'^(Ini|Itu|Ada|Bila|Jika|Namun|Tetapi|Dan|Yang|Dalam|Pada)$', sp):
                found_speakers.append(sp)

    # Cek entitas kunci yang sering muncul sebagai subjek langsung
    direct_entities = [
        ('Kapolri Jenderal Suyudi Ario Seto', 'suyudi|kapolri jenderal suyudi'),
        ('Menko Yusril Ihza Mahendra', 'yusril|menko kumham|menko yusril'),
        ('Mabes Polri / Divhumas', 'mabes polri|divhumas|kadiv humas|bareskrim polri'),
        ('Presiden Prabowo Subianto', 'presiden prabowo|prabowo subianto|istana'),
        ('Komisi III DPR RI', 'komisi iii dpr|pansus dpr|dpr ri'),
        ('PDI Perjuangan', 'pdip|fraksi pdip|hasto'),
        ('Tersangka Jenderal (Purn) LSP', 'tersangka lsp|listyo sigit|eks kapolri'),
        ('Sumber Internal / Grup WA (Anonim)', 'grup wa|pesan berantai|sumber internal|internal polri'),
        ('Pakar Hukum / Pengamat Intelijen', 'chairul huda|isess|pakar hukum|pengamat')
    ]

    for label, pat in direct_entities:
        if re.search(pat, text, re.IGNORECASE):
            if label not in found_speakers:
                found_speakers.append(label)

    return found_speakers


def run_pipeline():
    print("=== [1/4] Membaca Korpus 200 Berita dari data.xlsx ===")
    df = pd.read_excel('data.xlsx', sheet_name='Data Link')

    articles_records = []
    quotes_records = []
    edges_records = []

    quote_id_counter = 1

    for idx, row in df.iterrows():
        url = str(row['URL'])
        title = str(row['Judul / deskripsi'])
        source_media = str(row['Media / Akun']).strip()
        pub_date = str(row.get('Tanggal publikasi', ''))

        # Buat content hash SHA-256 (FR-3)
        content_hash = hashlib.sha256((url + title).encode('utf-8')).hexdigest()
        article_id = f"ART-{idx+1:04d}"

        # Deteksi berita sindikasi kantor berita (FR-4)
        wire_origin = None
        if re.search(r'antara|antaranews', source_media, re.IGNORECASE) or re.search(r'antara', title, re.IGNORECASE):
            wire_origin = 'ANTARA'
        elif re.search(r'reuters', source_media, re.IGNORECASE) or re.search(r'reuters', title, re.IGNORECASE):
            wire_origin = 'Reuters'
        elif re.search(r'afp', source_media, re.IGNORECASE):
            wire_origin = 'AFP'

        articles_records.append({
            'article_id': article_id,
            'url': url,
            'source': source_media,
            'title': title,
            'published_at': pub_date,
            'content_hash': content_hash,
            'wire_origin': wire_origin,
            'tahap_narasi': row.get('Tahap narasi', '')
        })

        # Ekstrak narasumber / kutipan (FR-5)
        speakers = extract_quotes_from_text(title)
        for sp in speakers:
            sp_type = classify_speaker(sp)
            quotes_records.append({
                'quote_id': f"Q-{quote_id_counter:04d}",
                'article_id': article_id,
                'speaker': sp,
                'speaker_type': sp_type,
                'quote_snippet': title[:150],
                'extraction_confidence': 0.88,
                'manually_verified': False
            })
            quote_id_counter += 1

            # Hubungan edge bipartit: Media <---> Speaker (FR-9)
            edges_records.append({
                'source_media': source_media,
                'speaker': sp,
                'speaker_type': sp_type,
                'article_id': article_id
            })

    # Simpan articles.csv
    df_art = pd.DataFrame(articles_records)
    df_art.to_csv('articles.csv', index=False)
    print(f"-> Berhasil menyimpan {len(df_art)} artikel ke 'articles.csv'")

    # Simpan quotes.csv
    df_q = pd.DataFrame(quotes_records)
    df_q.to_csv('quotes.csv', index=False)
    print(f"-> Berhasil mengekstrak {len(df_q)} kutipan/narasumber ke 'quotes.csv'")

    # Agregasi Edge List Bipartit dengan Bobot (Weight)
    df_edges_raw = pd.DataFrame(edges_records)
    if not df_edges_raw.empty:
        df_edges = df_edges_raw.groupby(['source_media', 'speaker', 'speaker_type']).size().reset_index(name='weight')
        df_edges = df_edges.sort_values(by='weight', ascending=False)
        df_edges.to_csv('edges_media_source.csv', index=False)
        print(f"-> Berhasil membangun {len(df_edges)} relasi bipartit unik ke 'edges_media_source.csv'")

        print("\n=== TOP 10 RELASI MEDIA - NARASUMBER PALING KUAT ===")
        print(df_edges.head(10).to_string(index=False))

    return df_art, df_q, df_edges


if __name__ == '__main__':
    run_pipeline()
