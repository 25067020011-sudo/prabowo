import os, sys, json
from pathlib import Path
import pandas as pd
import networkx as nx

# Hindari permission error matplotlib di macOS sandbox
os.environ['MPLCONFIGDIR'] = '/tmp/mpl_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root = Path(os.environ.get("WORLD_INTEL_HOME", Path.cwd())).resolve()
infile = root / "input" / "articles.csv"
out = root / "output"
if not infile.exists():
    sample = root / "input" / "articles.example.csv"
    print(f"No input/articles.csv found. Copy the example first:\n  cp '{sample}' '{infile}'\nThen add your permitted/public dataset.")
    sys.exit(2)

df = pd.read_csv(infile).fillna("")
required = {"title", "url", "published_at", "source", "entities"}
missing = required - set(df.columns)
if missing:
    raise SystemExit("Missing CSV columns: " + ", ".join(sorted(missing)))

G = nx.Graph()
for _, row in df.iterrows():
    ents = sorted({e.strip() for e in str(row["entities"]).split(";") if e.strip()})
    for entity in ents:
        G.add_node(entity, entity=entity)
    for i, a in enumerate(ents):
        for b in ents[i+1:]:
            if G.has_edge(a, b):
                G[a][b]["weight"] += 1
            else:
                G.add_edge(a, b, weight=1)

out_nx = out / "nodexl"
out_reports = out / "reports"
out_charts = out / "charts"
for p in (out_nx, out_reports, out_charts): p.mkdir(parents=True, exist_ok=True)

betweenness_dict = nx.betweenness_centrality(G)
nodes = pd.DataFrame([{"Vertex": n, "Degree": int(G.degree(n)), "Betweenness": betweenness_dict.get(n, 0)} for n in G.nodes()])
edges = pd.DataFrame([{"Vertex 1": a, "Vertex 2": b, "Edge Weight": d.get("weight", 1)} for a,b,d in G.edges(data=True)])
nodes.to_csv(out_nx / "nodes.csv", index=False)
edges.to_csv(out_nx / "edges.csv", index=False)

# GraphML is also convenient for Gephi, NodeXL, and other network tools.
nx.write_graphml(G, out_nx / "network.graphml")

n, m = G.number_of_nodes(), G.number_of_edges()
density = nx.density(G) if n > 1 else 0
components = nx.number_connected_components(G) if n else 0
central = sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]

report = [
    "# World Intelligence — Data Analysis Report",
    "",
    f"- Articles/records: {len(df)}",
    f"- Entity nodes: {n}",
    f"- Co-occurrence edges: {m}",
    f"- Network density: {density:.4f}",
    f"- Connected components: {components}",
    "",
    "## Top entities by degree",
    ""
]
report += [f"- **{name}**: {degree} koneksi" for name, degree in central]
report += [
    "",
    "## Data provenance",
    "Results are derived from the user-provided CSV. Validate source permissions, deduplication, timestamps, and interpretations before publication."
]
(out_reports / "analysis_report.md").write_text("\n".join(report), encoding="utf-8")

if n:
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, weight="weight")
    nx.draw_networkx(G, pos, node_size=600, font_size=9, font_weight="bold", with_labels=True, width=1.2, node_color="#38bdf8", edge_color="#94a3b8")
    plt.title("Entity Co-occurrence Network (World A.LIVE Intelligence Pipeline)", fontsize=13, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_charts / "entity_network.png", dpi=180)
    plt.close()

print(f"✅ Pipeline analisis selesai! Output tersedia di: {out}")
