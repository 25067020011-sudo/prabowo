#!/usr/bin/env bash
# World A.LIVE-inspired public-news intelligence pipeline (original implementation)
# macOS / zsh or bash. Uses permitted/public data supplied in input/articles.csv.
# NodeXL Pro and Reportica are integration-by-export/import unless you configure their APIs.

set -Eeuo pipefail
ROOT="${WORLD_INTEL_HOME:-$PWD}"
PYTHON="${PYTHON:-/Library/Frameworks/Python.framework/Versions/3.14/bin/python3}"
if [ ! -x "$PYTHON" ]; then
    PYTHON="$(which python3)"
fi

say(){ printf '\n[%s] %s\n' "$(date '+%H:%M:%S')" "$*"; }
fail(){ printf '\nERROR: %s\n' "$*" >&2; exit 1; }

say "Creating project workspace at $ROOT"
mkdir -p "$ROOT"/{input,output/{nodexl,reportica,charts,reports},src,dashboard,flowcharts,logs}

cat > "$ROOT/requirements.txt" <<'REQ'
pandas>=2.0
networkx>=3.0
matplotlib>=3.7
plotly>=5.15
streamlit>=1.35
openpyxl>=3.1
requests>=2.31
beautifulsoup4>=4.12
REQ

cat > "$ROOT/.env.example" <<'ENV'
# Optional only if your Reportica Intelligent deployment documents an API.
REPORTICA_API_URL=
REPORTICA_API_TOKEN=
ENV

cat > "$ROOT/input/articles.example.csv" <<'CSV'
title,url,published_at,source,entities
Example public policy announcement,https://example.org/article,2026-11-03,Example News,Ministry;Public Policy
Example public discussion,https://example.org/article2,2026-11-03,Example News,Public Policy;Community
CSV

# Jika input/articles.csv belum ada, tapi data.xlsx ada, otomatis ekstrak 200 artikel riil
if [ ! -f "$ROOT/input/articles.csv" ] && [ -f "$ROOT/data.xlsx" ]; then
    say "Memuat 200 data artikel riil dari data.xlsx ke input/articles.csv..."
    "$PYTHON" - <<'PYCONV'
import pandas as pd, re

df = pd.read_excel('data.xlsx', sheet_name='Data Link')

actors_dict = {
    'Presiden Prabowo': r'prabowo|presiden',
    'Eks Kapolri LSP': r'lsp|listyo|sigit|tersangka',
    'Mabes Polri': r'mabes polri|bareskrim|divhumas|propam',
    'Kapolri Jenderal Suyudi': r'suyudi|kapolri',
    'Menko Yusril': r'yusril',
    'DPR RI / Pansus': r'dpr|pansus|komisi iii',
    'PDI Perjuangan': r'pdip|hasto|puan',
    'Mabes TNI': r'tni|panglima',
    'Pakar Hukum / LSM': r'pakar|isess|kontras|icw|chairul huda',
    'Sumber Internal WAG': r'grup wa|pesan berantai|internal'
}

records = []
for idx, r in df.iterrows():
    title = str(r['Judul / deskripsi']).strip()
    url = str(r['URL']).strip()
    pub = str(r.get('Tanggal publikasi', '2026-11-03')).split()[0]
    source = str(r['Media / Akun']).strip()
    
    found_ents = []
    for label, pat in actors_dict.items():
        if re.search(pat, title, re.IGNORECASE):
            found_ents.append(label)
    
    if not found_ents:
        found_ents = ['Isu Penyadapan']
        
    records.append({
        'title': title,
        'url': url,
        'published_at': pub,
        'source': source,
        'entities': ';'.join(found_ents)
    })

pd.DataFrame(records).to_csv('input/articles.csv', index=False)
print("-> input/articles.csv berhasil dibuat dengan 200 artikel riil!")
PYCONV
elif [ ! -f "$ROOT/input/articles.csv" ]; then
    cp "$ROOT/input/articles.example.csv" "$ROOT/input/articles.csv"
fi

cat > "$ROOT/src/pipeline.py" <<'PY'
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
PY

say "Menjalankan pipeline analisis..."
"$PYTHON" "$ROOT/src/pipeline.py"

say "Pipeline berhasil dieksekusi!"
printf '\nOutput files created:\n'
printf '  • NodeXL Nodes:    %s/output/nodexl/nodes.csv\n' "$ROOT"
printf '  • NodeXL Edges:    %s/output/nodexl/edges.csv\n' "$ROOT"
printf '  • GraphML Network: %s/output/nodexl/network.graphml\n' "$ROOT"
printf '  • Intel Report:    %s/output/reports/analysis_report.md\n' "$ROOT"
printf '  • Network Chart:   %s/output/charts/entity_network.png\n\n' "$ROOT"
