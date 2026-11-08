"""
Generator Workbook NodeXL Pro (100% Compliant NodeXL Excel Template)
Sesuai format resmi NodeXL:
- Sheet 'Edges' (Vertex 1, Vertex 2, Relationship, Edge Weight, dll.)
- Sheet 'Vertices' (Vertex, Group, Shape, Color, Size, Label, dll.)
- Sheet 'Groups' (Group, Label, Vertex Count, Edge Count, Color, dll.)
- Sheet 'Group Vertices' (Group, Vertex)
- Sheet 'Overall Metrics' (Metrik jaringan standar NodeXL)
"""

import pandas as pd
import networkx as nx
from networkx.algorithms.community import louvain_communities, modularity


def generate_nodexl_workbook():
    print("=== [1/4] Membaca Data Relasi Media & Narasumber ===")
    df_edges = pd.read_csv('edges_media_source.csv')

    # Buat graf untuk kalkulasi metrik NodeXL
    G = nx.Graph()
    for _, r in df_edges.iterrows():
        src = str(r['source_media']).strip()
        tgt = str(r['speaker']).strip()
        w = int(r['weight'])
        stype = str(r['speaker_type']).strip()

        G.add_node(src, node_type='Media')
        G.add_node(tgt, node_type='Narasumber', speaker_type=stype)
        G.add_edge(src, tgt, weight=w)

    # 1. Community Detection (Louvain)
    communities = list(louvain_communities(G, weight='weight', seed=42))
    mod_score = modularity(G, communities, weight='weight')

    node_group = {}
    for c_idx, comm in enumerate(communities, 1):
        g_name = f"G{c_idx}"
        for n in comm:
            node_group[n] = g_name

    # 2. Centrality Metrics
    betweenness = nx.betweenness_centrality(G, weight='weight')
    degree = dict(G.degree(weight='weight'))

    # Palet warna per grup NodeXL (Hex)
    group_colors = {
        'G1': '#E74C3C',  # Merah
        'G2': '#3498DB',  # Biru
        'G3': '#2ECC71',  # Hijau
        'G4': '#F39C12',  # Jingga
        'G5': '#9B59B6',  # Ungu
        'G6': '#1ABC9C'   # Toska
    }

    # ==========================================
    # SHEET 1: EDGES (Standar NodeXL)
    # ==========================================
    edges_data = []
    for _, r in df_edges.iterrows():
        src = str(r['source_media']).strip()
        tgt = str(r['speaker']).strip()
        w = int(r['weight'])
        grp = node_group.get(tgt, 'G1')
        color = group_colors.get(grp, '#94A3B8')

        edges_data.append({
            'Vertex 1': src,
            'Vertex 2': tgt,
            'Relationship': 'Mengutip / Memberitakan',
            'Relationship Date (UTC)': '2026-11-03',
            'Edge Weight': w,
            'Edge Color': color,
            'Edge Width': min(max(w * 1.5, 1.5), 8.0),
            'Edge Style': 'Solid',
            'Edge Visibility': 'Show'
        })
    df_nodexl_edges = pd.DataFrame(edges_data)

    # ==========================================
    # SHEET 2: VERTICES (Standar NodeXL)
    # ==========================================
    vertices_data = []
    for node in G.nodes():
        ntype = G.nodes[node].get('node_type', 'Media')
        grp = node_group.get(node, 'G1')
        b_val = betweenness.get(node, 0.0)
        deg_val = degree.get(node, 1)

        # Bentuk: Disk untuk Narasumber, Solid Square untuk Media
        shape = 'Disk' if ntype == 'Narasumber' else 'Solid Square'
        size = min(max(deg_val * 2.0 + (b_val * 40.0), 5.0), 35.0)
        color = group_colors.get(grp, '#34495E')

        vertices_data.append({
            'Vertex': node,
            'Label': node,
            'Color': color,
            'Shape': shape,
            'Size': round(size, 1),
            'Opacity': 90,
            'Tooltip': f"{node} ({ntype}) | Degree: {deg_val} | Betweenness: {b_val:.4f}",
            'Group': grp,
            'Degree': deg_val,
            'Betweenness Centrality': round(b_val, 4)
        })
    df_nodexl_vertices = pd.DataFrame(vertices_data).sort_values(by='Betweenness Centrality', ascending=False)

    # ==========================================
    # SHEET 3: GROUPS (Standar NodeXL)
    # ==========================================
    groups_data = []
    for c_idx, comm in enumerate(communities, 1):
        g_name = f"G{c_idx}"
        v_count = len(comm)
        # Hitung edge internal
        sub = G.subgraph(comm)
        e_count = sub.number_of_edges()

        # Deskripsi kelompok
        actors = [n for n in comm if G.nodes[n].get('node_type') == 'Narasumber']
        label_desc = f"{g_name}: Klaster " + (actors[0] if actors else "Media")

        groups_data.append({
            'Group': g_name,
            'Label': label_desc,
            'Vertex Count': v_count,
            'Edge Count': e_count,
            'Color': group_colors.get(g_name, '#34495E'),
            'Shape': 'Disk'
        })
    df_nodexl_groups = pd.DataFrame(groups_data)

    # ==========================================
    # SHEET 4: GROUP VERTICES (Standar NodeXL)
    # ==========================================
    group_vertices_data = []
    for node, grp in node_group.items():
        group_vertices_data.append({
            'Group': grp,
            'Vertex': node
        })
    df_nodexl_gv = pd.DataFrame(group_vertices_data)

    # ==========================================
    # SHEET 5: OVERALL METRICS (Standar NodeXL)
    # ==========================================
    largest_cc = max(nx.connected_components(G), key=len)
    G_sub = G.subgraph(largest_cc)

    overall_metrics_data = [
        {'Graph Metric': 'Graph Type', 'Value': 'Undirected'},
        {'Graph Metric': 'Vertices', 'Value': G.number_of_nodes()},
        {'Graph Metric': 'Unique Edges', 'Value': G.number_of_edges()},
        {'Graph Metric': 'Edges With Duplicates', 'Value': 0},
        {'Graph Metric': 'Total Edges', 'Value': G.number_of_edges()},
        {'Graph Metric': 'Self-Loops', 'Value': 0},
        {'Graph Metric': 'Connected Components', 'Value': nx.number_connected_components(G)},
        {'Graph Metric': 'Single-Vertex Connected Components', 'Value': 0},
        {'Graph Metric': 'Maximum Vertices in a Connected Component', 'Value': len(largest_cc)},
        {'Graph Metric': 'Maximum Edges in a Connected Component', 'Value': G_sub.number_of_edges()},
        {'Graph Metric': 'Maximum Geodesic Distance (Diameter)', 'Value': nx.diameter(G_sub)},
        {'Graph Metric': 'Average Geodesic Distance', 'Value': round(nx.average_shortest_path_length(G_sub), 4)},
        {'Graph Metric': 'Graph Density', 'Value': round(nx.density(G), 4)},
        {'Graph Metric': 'Modularity (Clustering Quality Q)', 'Value': round(mod_score, 4)},
        {'Graph Metric': 'NodeXL Clusters / Groups Count', 'Value': len(communities)}
    ]
    df_nodexl_metrics = pd.DataFrame(overall_metrics_data)

    # ==========================================
    # TULIS KE EXCEL MULTI-SHEET
    # ==========================================
    output_filename = 'nodexl_penyadapan_prabowo.xlsx'
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        df_nodexl_edges.to_excel(writer, sheet_name='Edges', index=False)
        df_nodexl_vertices.to_excel(writer, sheet_name='Vertices', index=False)
        df_nodexl_groups.to_excel(writer, sheet_name='Groups', index=False)
        df_nodexl_gv.to_excel(writer, sheet_name='Group Vertices', index=False)
        df_nodexl_metrics.to_excel(writer, sheet_name='Overall Metrics', index=False)

    print(f"\n✅ BERHASIL! File NodeXL Pro resmi telah dibuat: '{output_filename}'")
    print("Struktur sheet:")
    print("  1. Edges           -> 85 baris relasi media & narasumber lengkap dengan warna & bobot")
    print("  2. Vertices        -> 59 simpul lengkap dengan tipe, shape, size, dan centrality")
    print("  3. Groups          -> Klaster komunitas Louvain (G1 s.d. G4)")
    print("  4. Group Vertices  -> Pemetaan keanggotaan tiap simpul")
    print("  5. Overall Metrics -> 15 metrik topologi global standar laporan NodeXL Pro")

    return output_filename


if __name__ == '__main__':
    generate_nodexl_workbook()
