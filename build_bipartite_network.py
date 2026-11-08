"""
Modul Pembangunan Jaringan Bipartit & Proyeksi Satu-Mode (FR-9)
Sesuai PRD: Analisis Jaringan Narasi Kasus Penyadapan Presiden

Membangun graf jaringan bipartit: Media <---> Narasumber
Menghitung Betweenness Centrality, Degree, dan mengekspor file GraphML
untuk NodeXL dan Gephi.
"""

import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite


def build_and_analyze_network():
    print("=== [1/3] Membaca Edge List Bipartit dari edges_media_source.csv ===")
    df_edges = pd.read_csv('edges_media_source.csv')

    # Buat graf bipartit
    B = nx.Graph()

    media_nodes = set(df_edges['source_media'].unique())
    speaker_nodes = set(df_edges['speaker'].unique())

    # Tambahkan node dengan atribut tipe
    B.add_nodes_from(media_nodes, bipartite=0, node_type='Media')
    B.add_nodes_from(speaker_nodes, bipartite=1, node_type='Narasumber')

    # Tambahkan edge dengan bobot
    for _, row in df_edges.iterrows():
        B.add_edge(row['source_media'], row['speaker'], weight=int(row['weight']), speaker_type=str(row['speaker_type']))

    print(f"-> Graf Bipartit terbentuk: {B.number_of_nodes()} simpul ({len(media_nodes)} media, {len(speaker_nodes)} narasumber), {B.number_of_edges()} edge.")

    # ==========================================
    # METRIK SENTRALITAS (RQ1)
    # ==========================================
    print("\n=== [2/3] Menghitung Metrik Sentralitas Aktor (Betweenness & Degree) ===")
    betweenness = nx.betweenness_centrality(B, weight='weight')
    degree = dict(B.degree(weight='weight'))

    metrics_records = []
    for sp in speaker_nodes:
        metrics_records.append({
            'Aktor / Narasumber': sp,
            'Degree (Koneksi Media)': degree.get(sp, 0),
            'Betweenness Centrality (Broker)': round(betweenness.get(sp, 0), 4)
        })

    df_metrics = pd.DataFrame(metrics_records).sort_values(by='Betweenness Centrality (Broker)', ascending=False)
    df_metrics.to_csv('metrics_actor_centrality.csv', index=False)

    print(df_metrics.to_string(index=False))

    # ==========================================
    # EKSPOR KE FORMAT GRAPHML UNTUK NODEXL / GEPHI
    # ==========================================
    print("\n=== [3/3] Mengekspor Jaringan ke GraphML (NodeXL / Gephi Ready) ===")
    graphml_filename = 'network_media_narasumber.graphml'
    # Tambahkan nilai metrik ke dalam atribut node
    for node in B.nodes():
        B.nodes[node]['betweenness'] = float(betweenness.get(node, 0))
        B.nodes[node]['degree_weighted'] = int(degree.get(node, 0))

    nx.write_graphml(B, graphml_filename)
    print(f"-> Berhasil menyimpan file graf ke '{graphml_filename}' (dapat langsung dibuka di NodeXL Pro / Gephi).")

    return B, df_metrics


if __name__ == '__main__':
    build_and_analyze_network()
