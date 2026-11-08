import os
import sys

# Jika file ini dieksekusi sebagai Main File oleh Streamlit Cloud,
# jalankan dashboard interaktif utama di app.py setiap kali rerun
try:
    import streamlit as st
    _HAS_STREAMLIT_RUNTIME = bool(st.runtime.exists())
except Exception:
    _HAS_STREAMLIT_RUNTIME = False

if _HAS_STREAMLIT_RUNTIME:
    import runpy
    runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py"), run_name="__main__")
    st.stop()

import re
import pandas as pd
import numpy as np

# Atur cache matplotlib agar tidak ada permission error
os.environ['MPLCONFIGDIR'] = '/tmp/mpl_cache'

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    print("[Info] Matplotlib belum terinstal, pembuatan gambar dilewati.")
    plt = None

if plt is not None:
    # 1. Baca Data
    df = pd.read_excel('data.xlsx', sheet_name='Data Link')
    df_jam = pd.read_excel('data.xlsx', sheet_name='Distribusi Jam')

    # ==========================================
    # CHART 1: Distribusi Jam Kritis (3 Nov 2026)
    # ==========================================
    plt.figure(figsize=(10, 5))
    valid_jam = df_jam.dropna(subset=['Jumlah berita']).copy()
    valid_jam = valid_jam[valid_jam['Jam (WIB), 3 Nov 2026'] != 'Total']
    jam_labels = valid_jam['Jam (WIB), 3 Nov 2026'].astype(str)
    jumlah = valid_jam['Jumlah berita'].astype(int)

    colors = ['#e74c3c' if float(j.split()[0]) < 20 else '#2980b9' for j in jam_labels if j.replace('.', '').isdigit()]
    if len(colors) < len(jam_labels):
        colors = ['#e74c3c' if idx < 6 else '#2980b9' for idx in range(len(jam_labels))]

    plt.bar(jam_labels, jumlah, color=colors, edgecolor='black', alpha=0.85)
    plt.axvline(x=5.5, color='darkred', linestyle='--', linewidth=2, label='Konferensi Pers Resmi (20.00 WIB)')
    plt.title('Dinamika Pemberitaan Per Jam pada Hari Kritis (3 Nov 2026)\nFase Rumor vs. Fase Domestikasi Media Resmi', fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Jam Penayangan (WIB)', fontsize=10, fontweight='bold')
    plt.ylabel('Jumlah Artikel Berita', fontsize=10, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.legend(frameon=True, facecolor='white', loc='upper left')
    plt.tight_layout()
    plt.savefig('chart_distribusi_jam_3nov.png', dpi=300)
    plt.close()
    print('Chart 1 created: chart_distribusi_jam_3nov.png')

    # ==========================================
    # CHART 2: Frekuensi Kemunculan Aktor Utama
    # ==========================================
    actors = {
        'Prabowo (Presiden)': r'prabowo|presiden',
        'LSP (Eks Kapolri / Tersangka)': r'lsp|listyo|sigit|tersangka',
        'Mabes Polri / Bareskrim': r'bareskrim|mabes polri|propam|polri',
        'DPR / Parpol (Pansus)': r'dpr|pansus|pdip|gerindra|parpol',
        'Jenderal Suyudi (Kapolri)': r'suyudi|kapolri',
        'Yusril (Menko Kumham)': r'yusril',
        'Isu Makar / Kudeta': r'makar|kudeta|operasi senyap',
        'Pakar / LSM / Hukum': r'pakar|pengamat|kontras|icw|isess'
    }

    counts = {}
    for act, pat in actors.items():
        cnt = df['Judul / deskripsi'].str.contains(pat, case=False, regex=True).sum()
        counts[act] = cnt

    actors_df = pd.Series(counts).sort_values(ascending=True)

    plt.figure(figsize=(10, 5.5))
    bars = plt.barh(actors_df.index, actors_df.values, color='#16a085', edgecolor='black', alpha=0.85)
    plt.title('Frekuensi Kemunculan Entitas & Aktor Kunci dalam 200 Berita\n(Identifikasi Node Sentral & Broker Narasi)', fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Jumlah Berita yang Menyebutkan Entitas', fontsize=10, fontweight='bold')
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 1.5, bar.get_y() + bar.get_height()/2, f'{int(w)} ({w/200*100:.1f}%)', va='center', fontsize=9, fontweight='bold')
    plt.xlim(0, max(actors_df.values) + 20)
    plt.grid(axis='x', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('chart_frekuensi_aktor.png', dpi=300)
    plt.close()
    print('Chart 2 created: chart_frekuensi_aktor.png')

    # ==========================================
    # CHART 3: Proporsi Tahap Narasi
    # ==========================================
    tahap_counts = df['Tahap narasi'].value_counts()
    plt.figure(figsize=(8, 8))
    palette = ['#3498db', '#9b59b6', '#e67e22', '#1abc9c', '#e74c3c', '#f1c40f', '#34495e']
    plt.pie(tahap_counts.values, labels=tahap_counts.index, autopct='%1.1f%%', startangle=140, colors=palette,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    plt.title('Proporsi 7 Tahap Narasi Kasus Penyadapan\n(Total N = 200 Artikel)', fontsize=12, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('chart_proporsi_tahap_narasi.png', dpi=300)
    plt.close()
    print('Chart 3 created: chart_proporsi_tahap_narasi.png')
