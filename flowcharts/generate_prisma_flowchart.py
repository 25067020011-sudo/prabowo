#!/usr/bin/env python3
"""
Generator Diagram Alir PRISMA 2020 (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
Menghasilkan diagram alir seleksi korpus berita & data media sosial berstandar Scopus Q1.
Disimpan dalam format PNG 300 DPI: flowcharts/prisma_2020_flowchart.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_prisma_2020():
    fig, ax = plt.subplots(figsize=(15, 12), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 12)
    ax.axis('off')

    fig.patch.set_facecolor('#ffffff')

    # Color Scheme PRISMA 2020
    c_phase = {'bg': '#1e3a8a', 'text': '#ffffff'}
    c_main = {'bg': '#f8fafc', 'border': '#334155', 'text': '#0f172a'}
    c_exc = {'bg': '#fef2f2', 'border': '#ef4444', 'text': '#991b1b'}
    c_inc = {'bg': '#f0fdf4', 'border': '#16a34a', 'text': '#14532d'}

    def draw_phase_banner(y_bottom, height, label):
        # Vertical strip on the left
        rect = patches.FancyBboxPatch((0.5, y_bottom), 0.7, height, boxstyle="square,pad=0.0",
                                      facecolor=c_phase['bg'], edgecolor='#1e3a8a', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(0.85, y_bottom + height/2, label, fontsize=11, fontweight='bold', color=c_phase['text'],
                ha='center', va='center', rotation=90, family='sans-serif')

    def draw_box(x, y, w, h, text, style='main'):
        if style == 'main':
            fc, ec, tc = c_main['bg'], c_main['border'], c_main['text']
            lw = 1.4
        elif style == 'exc':
            fc, ec, tc = c_exc['bg'], c_exc['border'], c_exc['text']
            lw = 1.4
        elif style == 'inc':
            fc, ec, tc = c_inc['bg'], c_inc['border'], c_inc['text']
            lw = 1.8
        
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.1",
                                      facecolor=fc, edgecolor=ec, linewidth=lw)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, fontsize=8.5, color=tc,
                ha='center', va='center', family='sans-serif', wrap=True)

    def draw_arrow(x1, y1, x2, y2, color="#475569"):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.4, headwidth=6, headlength=6, shrink=0.04))

    # Title Banner
    ax.text(7.5, 11.6, "PRISMA 2020 Flow Diagram for Corpus Selection",
            fontsize=15, fontweight='bold', ha='center', color='#0f172a', family='sans-serif')
    ax.text(7.5, 11.3, "Proses Seleksi, Penyaringan, dan Penetapan Korpus Berita & Diskursus Publik Kasus Penyadapan Presiden",
            fontsize=10, ha='center', color='#64748b', family='sans-serif')

    # =========================================================================
    # 1. IDENTIFICATION (Top: y = 8.6 to 11.0)
    # =========================================================================
    draw_phase_banner(8.6, 2.4, "IDENTIFICATION")

    # Sources
    draw_box(1.5, 9.7, 4.4, 1.1,
             "Catatan diidentifikasi dari basis data\nportal berita nasional (25 portal):\n(n = 342)", 'main')
    draw_box(6.2, 9.7, 3.8, 1.1,
             "Catatan dari agregator berita\nWorld A.LIVE & Linimasa:\n(n = 148)", 'main')
    draw_box(10.3, 9.7, 4.2, 1.1,
             "Catatan dari API media sosial\n(YouTube comments & stream X):\n(n = 18,200)", 'main')

    # Duplicate / Pre-screening removal
    draw_box(3.5, 8.6, 5.0, 0.85,
             "Catatan duplikat dihapus via hash SHA-256 (n = 78)\nSindikasi pers tanpa atribusi baru dihapus (n = 46)", 'exc')

    draw_arrow(3.7, 9.7, 5.0, 9.45)
    draw_arrow(8.1, 9.7, 7.0, 9.45)
    draw_arrow(6.0, 9.45, 6.0, 9.45)

    # =========================================================================
    # 2. SCREENING (y = 5.9 to 8.4)
    # =========================================================================
    draw_phase_banner(5.9, 2.5, "SCREENING")

    # Screened Box
    draw_box(2.5, 7.2, 5.5, 1.0,
             "Catatan berita disaring berdasarkan judul,\nstempel waktu, dan metadata ringkasan:\n(n = 366)", 'main')
    
    # Excluded Box
    draw_box(8.8, 7.2, 5.7, 1.0,
             "Catatan berita dieksklusi (n = 112):\n• Konten clickbait / di luar konteks penyadapan (n = 68)\n• Tanpa stempel waktu jam yang terverifikasi (n = 44)", 'exc')

    draw_arrow(6.0, 8.6, 5.25, 8.2)
    draw_arrow(8.0, 7.7, 8.8, 7.7)

    # Social comments screening
    draw_box(2.5, 6.0, 5.5, 0.9,
             "Komentar publik disaring via pembersihan teks\n(penghapusan bot, spam, dan duplikasi akun):\n(n = 18,076)", 'main')
    draw_box(8.8, 6.0, 5.7, 0.9,
             "Komentar dieksklusi (n = 2,656):\n• Pesan spam promosi / bot otomatis (n = 1,842)\n• Teks tidak terbaca / < 3 kata (n = 814)", 'exc')

    draw_arrow(12.4, 9.7, 12.4, 7.0)
    draw_arrow(12.4, 7.0, 6.0, 7.0)
    draw_arrow(8.0, 6.45, 8.8, 6.45)

    # =========================================================================
    # 3. ELIGIBILITY (y = 3.3 to 5.7)
    # =========================================================================
    draw_phase_banner(3.3, 2.4, "ELIGIBILITY")

    draw_box(2.5, 4.5, 5.5, 0.95,
             "Artikel berita teks lengkap dicari untuk dinilai\nkelayakannya secara mendalam:\n(n = 254)", 'main')
    draw_box(8.8, 4.5, 5.7, 0.95,
             "Laporan tidak dapat diambil / dieksklusi:\n• Terhalang paywall / tautan rusak (n = 18)\n• Kurang atribusi kutipan narasumber primer (n = 22)\n• Agregasi ulang tanpa kutipan narasumber baru (n = 14)", 'exc')

    draw_arrow(5.25, 7.2, 5.25, 5.45)
    draw_arrow(8.0, 4.97, 8.8, 4.97)

    draw_box(2.5, 3.4, 5.5, 0.85,
             "Artikel berita memenuhi kriteria kelayakan metodologis:\n(n = 200)", 'main')
    draw_arrow(5.25, 4.5, 5.25, 4.25)

    # =========================================================================
    # 4. INCLUDED (y = 0.5 to 3.1)
    # =========================================================================
    draw_phase_banner(0.5, 2.6, "INCLUDED")

    draw_box(1.5, 0.7, 4.2, 2.1,
             "KORPUS BERITA PRIMER\n(n = 200 Artikel)\n\n• Sub-sampel Jam Kritis 3 Nov\n  (n = 146 Artikel)\n• Analisis 7 Tahap Narasi\n• Ekstraksi Bipartit Media-Aktor\n• Ekspor Buku Kerja NodeXL Pro", 'inc')

    draw_box(6.0, 0.7, 4.2, 2.1,
             "KORPUS REPLIKASI INDEPENDEN\n(n = 114 Artikel)\n\n• Sumber: World A.LIVE (7 Nov)\n• Sebaran 24 Jam Penuh\n• Validasi Stabilitas Sentralitas\n  dan Model Kausalitas Lag\n• Pengujian Difusi Lintas Portal", 'inc')

    draw_box(10.5, 0.7, 4.0, 2.1,
             "KORPUS DISKURSUS PUBLIK\n(n = 15,420 Interaksi)\n\n• Analisis Polarisasi Louvain\n  (Q = 0.3335, 4 Komunitas)\n• Uji Korelasi Silang (CCF Lag 0)\n• Validasi Two-Phase Reversal\n  Network Agenda-Setting", 'inc')

    draw_arrow(5.25, 3.4, 3.6, 2.8)
    draw_arrow(8.1, 9.7, 8.1, 2.8)
    draw_arrow(5.25, 6.0, 12.5, 2.8)

    plt.tight_layout()
    plt.savefig("flowcharts/prisma_2020_flowchart.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    print("[✓] Diagram alir PRISMA 2020 berhasil disimpan di flowcharts/prisma_2020_flowchart.png")

if __name__ == "__main__":
    draw_prisma_2020()
