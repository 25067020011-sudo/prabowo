"""
Modul Deteksi Kontradiksi Narasi (Reportica Intelligent & TinyFish Framework)
'Treats contradictions as the product, not the problem'

Mendeteksi perbedaan klaim, bantahan, dan diskrepansi narasi antar-media / aktor
dalam skandal penyadapan Presiden.
"""

import json
import re
import pandas as pd


CONTRADICTION_AXES = [
    {
        'id': 'CONT-01',
        'axis': 'Status Hukum Aktor: Penangkapan vs Penetapan Tersangka',
        'claim_a': {
            'stance': 'Penangkapan Fisik / Ditahan Mako Brimob',
            'pattern': r'ditangkap|penangkapan|diamankan|ditahan di mako brimob|bintang empat diamankan',
            'actors': 'Portal Berita Niche & Akun X Anonim',
            'fase': 'Fase Rumor (3 Nov 14.00 - 19.59 WIB)'
        },
        'claim_b': {
            'stance': 'Penetapan Tersangka Tanpa Penangkapan Fisik',
            'pattern': r'tersangka|ditetapkan|status|proses hukum',
            'actors': 'Mabes Polri (Bareskrim Resmi)',
            'fase': 'Fase Konfirmasi Resmi (3 Nov 20.00 WIB)'
        }
    },
    {
        'id': 'CONT-02',
        'axis': 'Klasifikasi Perbuatan: Dugaan Makar vs Delik Penyadapan Ilegal',
        'claim_a': {
            'stance': 'Tindakan Makar / Kudeta / Pengkhianatan Internal',
            'pattern': r'makar|kudeta|operasi senyap|pengkhianatan|guncang',
            'actors': 'Warganet Kritis / Oposisi / Akun Spekulatif',
            'fase': 'Fase Rumor & Respons Awal'
        },
        'claim_b': {
            'stance': 'Tindak Pidana Penyadapan Ilegal / Intersepsi Elektronik',
            'pattern': r'penyadapan ilegal|sadap ilegal|intersep|uu ite|pelanggaran hukum',
            'actors': 'Penyidik Bareskrim & Ahli Hukum',
            'fase': 'Fase Domestikasi Fakta (3-5 Nov)'
        }
    },
    {
        'id': 'CONT-03',
        'axis': 'Stabilitas Keamanan: Isu Gesekan Pasukan vs Bantahan Soliditas',
        'claim_a': {
            'stance': 'Isu Pengerahan Pasukan / Ketegangan Matra',
            'pattern': r'pengerahan tni|tni|pasukan|brimob siaga|gesekan',
            'actors': 'Rumor WAG / Media Sosial',
            'fase': 'Fase Rumor Lanjutan (3 Nov malam)'
        },
        'claim_b': {
            'stance': 'Bantahan Resmi & Soliditas TNI-Polri Terjaga',
            'pattern': r'bantah|klarifikasi|solid|tidak benar|hoaks|tenang',
            'actors': 'Mabes TNI & Divhumas Polri',
            'fase': 'Fase Bantahan / Klarifikasi (Tahap 5)'
        }
    },
    {
        'id': 'CONT-04',
        'axis': 'Kanal Informasi Kepala Negara: Spekulasi Liar vs Laporan Formal',
        'claim_a': {
            'stance': 'Presiden Tahu Melalui Saluran Non-Formal / Intelijen Luar',
            'pattern': r'bocor|isu liar|kabar burung|desas-desus|perang bintang',
            'actors': 'Spekulasi Publik / Media Independen',
            'fase': 'Fase Analisis Awal'
        },
        'claim_b': {
            'stance': 'Presiden Mengetahui dari Laporan Resmi Kapolri Jenderal Suyudi',
            'pattern': r'kapolri|suyudi|laporan resmi|menko yusril|istana',
            'actors': 'Menko Yusril Ihza Mahendra (Pemerintah)',
            'fase': 'Fase Resonansi Elite (Tahap 4)'
        }
    }
]


def detect_contradictions(df_articles):
    """Memetakan artikel berita ke dalam matriks kontradiksi narasi."""
    matrix_results = []

    for axis in CONTRADICTION_AXES:
        pat_a = axis['claim_a']['pattern']
        pat_b = axis['claim_b']['pattern']

        articles_a = []
        articles_b = []

        for idx, row in df_articles.iterrows():
            text = str(row.get('Judul / deskripsi', ''))
            media = str(row.get('Media / Akun', ''))
            url = str(row.get('URL', ''))

            if re.search(pat_a, text, re.IGNORECASE):
                articles_a.append({'media': media, 'title': text, 'url': url})
            if re.search(pat_b, text, re.IGNORECASE):
                articles_b.append({'media': media, 'title': text, 'url': url})

        matrix_results.append({
            'id': axis['id'],
            'axis': axis['axis'],
            'claim_a_title': axis['claim_a']['stance'],
            'claim_a_count': len(articles_a),
            'claim_a_actors': axis['claim_a']['actors'],
            'claim_a_samples': articles_a[:2],
            'claim_b_title': axis['claim_b']['stance'],
            'claim_b_count': len(articles_b),
            'claim_b_actors': axis['claim_b']['actors'],
            'claim_b_samples': articles_b[:2]
        })

    return matrix_results


def run_pipeline():
    df = pd.read_excel('data.xlsx', sheet_name='Data Link')
    contradictions = detect_contradictions(df)

    # Simpan ke JSON & CSV
    with open('reports/contradiction_matrix.json', 'w', encoding='utf-8') as f:
        json.dump(contradictions, f, indent=4)

    rows = []
    for c in contradictions:
        rows.append({
            'ID': c['id'],
            'Sumbu Kontradiksi': c['axis'],
            'Klaim A (Tesis/Rumor)': f"{c['claim_a_title']} ({c['claim_a_count']} berita)",
            'Aktor Klaim A': c['claim_a_actors'],
            'Klaim B (Antitesis/Resmi)': f"{c['claim_b_title']} ({c['claim_b_count']} berita)",
            'Aktor Klaim B': c['claim_b_actors']
        })

    df_res = pd.DataFrame(rows)
    df_res.to_csv('reports/contradiction_matrix.csv', index=False)
    print("✅ Berhasil mendeteksi kontradiksi narasi Reportica Intelligent!")
    print(df_res.to_string(index=False))

    return contradictions


if __name__ == '__main__':
    run_pipeline()
