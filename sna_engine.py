"""
SNA Engine: Modul Komputasi 4 Pilar Social Network Analysis
Standar Publikasi Jurnal Scopus Q1 & NodeXL / Gephi

1. Social Network Mapping
2. Community Detection (Louvain)
3. Analisis Influencer & Centrality Metrics
4. Global Network Characteristics & Topology Metrics
"""

import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
from networkx.algorithms.community import louvain_communities, modularity
import numpy as np
import pandas as pd

os.environ['MPLCONFIGDIR'] = '/tmp/mpl_cache'


def run_sna_analysis():
    print("=== [1/4] Memuat Data Relasi Media & Narasumber ===")
    df_edges = pd.read_csv('edges_media_source.csv')

    # Buat graf bipartit dan graf terbobot
    G = nx.Graph()

    for _, r in df_edges.iterrows():
        src = str(r['source_media']).strip()
        tgt = str(r['speaker']).strip()
        w = int(r['weight'])
        stype = str(r['speaker_type']).strip()

        G.add_node(src, node_type='Media', bipartite=0)
        G.add_node(tgt, node_type='Narasumber', bipartite=1, speaker_type=stype)
        G.add_edge(src, tgt, weight=w)

    N = G.number_of_nodes()
    E = G.number_of_edges()
    print(f"-> Graf berhasil dimuat: {N} simpul, {E} edge.")

    # ==========================================
    # PILAR 2: COMMUNITY DETECTION (LOUVAIN)
    # ==========================================
    print("\n=== [2/4] Melakukan Community Detection (Louvain Algorithm) ===")
    communities = list(louvain_communities(G, weight='weight', seed=42))
    mod_score = modularity(G, communities, weight='weight')
    print(f"-> Terdeteksi {len(communities)} komunitas/klaster dengan Modularity Q = {mod_score:.4f}")

    node_community = {}
    for c_id, comm in enumerate(communities, 1):
        for node in comm:
            node_community[node] = f"G{c_id}"
            G.nodes[node]['community'] = f"G{c_id}"

    # Simpan ringkasan komunitas
    comm_summary = []
    for c_id, comm in enumerate(communities, 1):
        media_in_c = [n for n in comm if G.nodes[n].get('node_type') == 'Media']
        actors_in_c = [n for n in comm if G.nodes[n].get('node_type') == 'Narasumber']
        comm_summary.append({
            'Komunitas': f"G{c_id}",
            'Total Anggota': len(comm),
            'Jumlah Media': len(media_in_c),
            'Jumlah Aktor': len(actors_in_c),
            'Aktor Utama': ", ".join(actors_in_c[:3]) if actors_in_c else "-"
        })

    df_comm = pd.DataFrame(comm_summary)
    df_comm.to_csv('sna_community_clusters.csv', index=False)
    print(df_comm.to_string(index=False))

    # ==========================================
    # PILAR 3: ANALISIS INFLUENCER & SENTRALITAS
    # ==========================================
    print("\n=== [3/4] Menghitung Metrik Sentralitas Influencer & Aktor Kunci ===")
    deg_centrality = nx.degree_centrality(G)
    bet_centrality = nx.betweenness_centrality(G, weight='weight')
    clo_centrality = nx.closeness_centrality(G)
    eig_centrality = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')
    pagerank_val = nx.pagerank(G, weight='weight')

    centrality_records = []
    for node in G.nodes():
        centrality_records.append({
            'Nama Simpul': node,
            'Tipe': G.nodes[node].get('node_type', ''),
            'Komunitas': node_community.get(node, ''),
            'Degree': G.degree(node, weight='weight'),
            'Degree Centrality': round(deg_centrality.get(node, 0), 4),
            'Betweenness Centrality (Broker)': round(bet_centrality.get(node, 0), 4),
            'Closeness Centrality': round(clo_centrality.get(node, 0), 4),
            'Eigenvector Centrality': round(eig_centrality.get(node, 0), 4),
            'PageRank': round(pagerank_val.get(node, 0), 4)
        })

    df_influencers = pd.DataFrame(centrality_records).sort_values(by='Betweenness Centrality (Broker)', ascending=False)
    df_influencers.to_csv('sna_influencer_centrality.csv', index=False)

    print("\n--- TOP 10 AKTOR PALING SENTRAL (BROKER NARASI / INFLUENCER) ---")
    top_speakers = df_influencers[df_influencers['Tipe'] == 'Narasumber'].head(10)
    print(top_speakers[['Nama Simpul', 'Komunitas', 'Degree', 'Betweenness Centrality (Broker)', 'Eigenvector Centrality', 'PageRank']].to_string(index=False))

    # ==========================================
    # PILAR 4: NETWORK TOPOLOGY METRICS
    # ==========================================
    print("\n=== [4/4] Menghitung Karakteristik Topologi Jaringan Global ===")
    density = nx.density(G)
    num_components = nx.number_connected_components(G)
    largest_cc = max(nx.connected_components(G), key=len)
    G_sub = G.subgraph(largest_cc)
    diameter = nx.diameter(G_sub)
    avg_path_len = nx.average_shortest_path_length(G_sub)
    # Graf G adalah bipartit (Media <-> Narasumber), sehingga gunakan Latapy bipartite clustering
    # serta one-mode actor projection clustering agar tidak bias ke 0.0
    avg_clustering_bipartite = bipartite.average_clustering(G)
    actor_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'Narasumber']
    G_actor_proj = bipartite.projected_graph(G, actor_nodes)
    avg_clustering_projected = nx.average_clustering(G_actor_proj)

    network_metrics = {
        'Total Nodes (Simpul)': N,
        'Total Edges (Relasi)': E,
        'Network Density (Kerapatan)': round(density, 4),
        'Modularity Score (Q)': round(mod_score, 4),
        'Connected Components': num_components,
        'Largest Component Size': len(largest_cc),
        'Diameter (Giant Component)': diameter,
        'Average Path Length (Geodesic Distance)': round(avg_path_len, 4),
        'Average Clustering Coefficient (Bipartite Latapy)': round(avg_clustering_bipartite, 4),
        'Average Clustering Coefficient (One-Mode Actor Projection)': round(avg_clustering_projected, 4)
    }

    with open('sna_network_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(network_metrics, f, indent=4)

    for k, v in network_metrics.items():
        print(f"  • {k:40}: {v}")

    # ==========================================
    # PILAR 1: SOCIAL NETWORK MAPPING (VISUALISASI)
    # ==========================================
    print("\n=== Menggambar Peta Jaringan (Social Network Map) ===")
    plt.figure(figsize=(14, 11))
    pos = nx.spring_layout(G, k=0.35, iterations=60, seed=42)

    # Warna per komunitas Louvain
    color_palette = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e']
    node_colors = []
    for node in G.nodes():
        c_str = node_community.get(node, 'G1')
        c_num = int(c_str.replace('G', '')) - 1
        node_colors.append(color_palette[c_num % len(color_palette)])

    # Ukuran node proporsional dengan Betweenness Centrality
    node_sizes = []
    for node in G.nodes():
        b_val = bet_centrality.get(node, 0.01)
        node_sizes.append(max(180, int(b_val * 4500) + 120))

    # Gambar edge
    nx.draw_networkx_edges(G, pos, alpha=0.35, edge_color='#94a3b8', width=1.2)

    # Gambar nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9, edgecolors='black', linewidths=1.2)

    # Label hanya untuk aktor dan media dengan derajat tinggi
    labels = {}
    for node in G.nodes():
        if G.nodes[node].get('node_type') == 'Narasumber' or bet_centrality.get(node, 0) > 0.03 or G.degree(node) >= 4:
            labels[node] = node

    nx.draw_networkx_labels(G, pos, labels, font_size=8.5, font_weight='bold', font_family='sans-serif')

    plt.title("Peta Jaringan Bipartit Liputan Media & Aktor Kasus Penyadapan Presiden\n(Layout Fruchterman-Reingold / Louvain Community Clustering)", fontsize=13, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('chart_sna_network_map.png', dpi=300)
    plt.close()
    print("-> Berhasil membuat visualisasi graf peta jaringan: 'chart_sna_network_map.png'")

    # Ekspor kembali GraphML dengan semua atribut lengkap
    for node in G.nodes():
        G.nodes[node]['betweenness'] = float(bet_centrality.get(node, 0))
        G.nodes[node]['degree_centrality'] = float(deg_centrality.get(node, 0))
        G.nodes[node]['closeness'] = float(clo_centrality.get(node, 0))
        G.nodes[node]['eigenvector'] = float(eig_centrality.get(node, 0))
        G.nodes[node]['pagerank'] = float(pagerank_val.get(node, 0))

    nx.write_graphml(G, 'network_media_narasumber.graphml')
    print("-> Berhasil memperbarui 'network_media_narasumber.graphml' dengan metrik 4 pilar lengkap.")

    return G, df_influencers, network_metrics


if __name__ == '__main__':
    run_sna_analysis()
