#!/usr/bin/env python3
"""
Membuat representasi grafis pipeline flowchart arsitektur sistem
dari teks Mermaid menjadi gambar PNG menggunakan matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_pipeline_flowchart():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#f8fafc')

    # Colors
    c_s1 = {'bg': '#eff6ff', 'border': '#3b82f6', 'hdr': '#1d4ed8'}
    c_s2 = {'bg': '#f0fdf4', 'border': '#22c55e', 'hdr': '#15803d'}
    c_s3 = {'bg': '#fefce8', 'border': '#eab308', 'hdr': '#a16207'}
    c_s4 = {'bg': '#faf5ff', 'border': '#a855f7', 'hdr': '#7e22ce'}
    box_c = {'bg': '#ffffff', 'border': '#94a3b8', 'text': '#0f172a'}

    def draw_subgraph(x, y, w, h, title, scheme):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                      facecolor=scheme['bg'], edgecolor=scheme['border'], linewidth=2)
        ax.add_patch(rect)
        ax.text(x + 0.3, y + h - 0.45, title, fontsize=11, fontweight='bold', color=scheme['hdr'], family='sans-serif')

    def draw_node(x, y, w, h, text, shape="rect"):
        if shape == "cylinder":
            rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                                          facecolor='#dcfce7', edgecolor='#16a34a', linewidth=1.5)
        else:
            rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.1",
                                          facecolor=box_c['bg'], edgecolor=box_c['border'], linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, fontsize=9, fontweight='500', color=box_c['text'],
                ha='center', va='center', family='sans-serif', wrap=True)

    def draw_arrow(x1, y1, x2, y2, color="#64748b"):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=7, headlength=7, shrink=0.05))

    # Title
    ax.text(7, 9.6, "Sistem Intelijen Berita & Analisis Jaringan Terpadu (World A.LIVE + NodeXL)",
            fontsize=15, fontweight='bold', ha='center', color='#0f172a', family='sans-serif')
    ax.text(7, 9.25, "Arsitektur Pipeline: Data Ingestion → Preprocessing → Multi-Engine Analytics → Dissemination",
            fontsize=10, ha='center', color='#64748b', family='sans-serif')

    # 1. DATA INGESTION (Top)
    draw_subgraph(0.8, 6.8, 12.4, 2.1, "1. DATA INGESTION LAYER", c_s1)
    draw_node(1.2, 7.3, 3.2, 0.9, "World A.LIVE Feed\n(Topic 51140 / Newspaper)")
    draw_node(4.8, 7.3, 3.2, 0.9, "Portal Scrapers\n(Antara, CNN, Detik, Viva)")
    draw_node(8.4, 7.3, 3.2, 0.9, "Social Media Streams\n(X, WAG, YouTube API)")
    draw_node(11.8, 7.1, 1.2, 1.3, "Collector\nEngine\n(CLI)")

    draw_arrow(4.4, 7.75, 4.8, 7.75)
    draw_arrow(8.0, 7.75, 8.4, 7.75)
    draw_arrow(11.6, 7.75, 11.8, 7.75)

    # Arrow down to S2
    draw_arrow(7.0, 6.8, 7.0, 6.2, color="#3b82f6")

    # 2. PROCESSING & VALIDATION
    draw_subgraph(0.8, 4.3, 12.4, 1.9, "2. PROCESSING & VALIDATION LAYER", c_s2)
    draw_node(1.2, 4.8, 3.4, 0.8, "Deduplikasi & Filter Kantor Berita\n(ANTARA / Reuters / AFP)")
    draw_node(5.0, 4.8, 3.4, 0.8, "Integrity Hash (SHA-256) &\nMetadata Extraction (JSON-LD)")
    draw_node(9.0, 4.6, 3.8, 1.1, "Data Repositories\ndata.xlsx / articles.csv\n(200 Portal + 114 World A.LIVE)", shape="cylinder")

    draw_arrow(4.6, 5.2, 5.0, 5.2)
    draw_arrow(8.4, 5.2, 9.0, 5.2)

    # Arrow down to S3
    draw_arrow(7.0, 4.3, 7.0, 3.8, color="#22c55e")

    # 3. ANALYTICS & INTELLIGENCE ENGINES
    draw_subgraph(0.8, 2.0, 12.4, 1.8, "3. ANALYTICS & INTELLIGENCE ENGINES", c_s3)
    draw_node(1.2, 2.4, 3.6, 0.9, "Reportica Intelligent Engine\n(4 Matriks Kontradiksi Narasi)")
    draw_node(5.2, 2.4, 3.6, 0.9, "SNA Engine & NodeXL Pro\n(Louvain Q=0.33, Centrality Broker)")
    draw_node(9.2, 2.4, 3.6, 0.9, "Temporal & Granger Engine\n(CCF Time-Lag & Network Agenda)")

    # Arrow down to S4
    draw_arrow(3.0, 2.0, 3.0, 1.5, color="#eab308")
    draw_arrow(7.0, 2.0, 7.0, 1.5, color="#eab308")
    draw_arrow(11.0, 2.0, 11.0, 1.5, color="#eab308")

    # 4. REPORTING & DISSEMINATION
    draw_subgraph(0.8, 0.2, 12.4, 1.3, "4. REPORTING & DISSEMINATION LAYER", c_s4)
    draw_node(1.1, 0.4, 2.6, 0.7, "Reportica Brief\n(analysis_report.md)")
    draw_node(3.9, 0.4, 2.6, 0.7, "NodeXL Workbook\n(.xlsx & GraphML)")
    draw_node(6.7, 0.4, 2.6, 0.7, "Naskah Scopus Q1\n(DRAF_ARTIKEL.md)")
    draw_node(9.5, 0.4, 3.4, 0.7, "Streamlit Cloud Live App\n(worlda-intelligence.sh CLI)")

    plt.tight_layout()
    plt.savefig("flowcharts/pipeline_flowchart.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    print("[✓] Gambar flowchart tersimpan di flowcharts/pipeline_flowchart.png")

if __name__ == "__main__":
    draw_pipeline_flowchart()

