"""
Automated Test Suite (pytest) untuk Verifikasi Integritas Data, SNA Bipartit,
Analisis Temporal/Granger, dan Deteksi Kontradiksi.
Standar Open Science & Reproducibility Jurnal Scopus Q1.
"""

import json
from pathlib import Path
import pandas as pd
import pytest

from sna_engine import run_sna_analysis
from temporal_analysis import run_temporal_analysis

ROOT = Path(__file__).resolve().parent.parent


def test_core_datasets_exist_and_schema():
    """Memastikan dataset utama tersedia dan memenuhi kontrak skema kolom."""
    articles_path = ROOT / "articles.csv"
    edges_path = ROOT / "edges_media_source.csv"
    quotes_path = ROOT / "quotes.csv"

    assert articles_path.exists(), "articles.csv wajib tersedia"
    assert edges_path.exists(), "edges_media_source.csv wajib tersedia"
    assert quotes_path.exists(), "quotes.csv wajib tersedia"

    df_art = pd.read_csv(articles_path)
    assert len(df_art) == 200, "Korpus utama wajib berisi 200 artikel terverifikasi"
    required_cols = {"article_id", "url", "source", "title", "published_at", "content_hash", "tahap_narasi"}
    assert required_cols.issubset(set(df_art.columns))
    assert df_art["content_hash"].str.len().eq(64).all(), "Setiap artikel wajib memiliki hash SHA-256 valid"


def test_sna_bipartite_metrics():
    """Memastikan SNA Engine menghitung metrik bipartit dengan benar (clustering > 0)."""
    G, df_infl, metrics = run_sna_analysis()

    assert metrics["Total Nodes (Simpul)"] == 59
    assert metrics["Total Edges (Relasi)"] == 85
    assert 0.30 <= metrics["Modularity Score (Q)"] <= 0.40
    assert metrics["Average Clustering Coefficient (Bipartite Latapy)"] > 0.40
    assert metrics["Average Clustering Coefficient (One-Mode Actor Projection)"] > 0.60
    assert not df_infl.empty


def test_temporal_ccf_and_regime_granger():
    """Memastikan konsistensi agregasi 15-menit ke 1-jam serta validitas uji CCF & Granger."""
    df_ccf, findings = run_temporal_analysis()

    # Lag 0 CCF harus signifikan (r = 0.896, p = 0.0005)
    lag0 = df_ccf[df_ccf["Lag (Jam)"] == 0].iloc[0]
    assert abs(lag0["Korelasi Pearson (r)"] - 0.896) < 0.001
    assert lag0["P-Value"] < 0.001
    assert lag0["Signifikan (p < 0.05)"] == "Ya"

    # Fase 1 (Public -> Media) harus signifikan secara statistik (p < 0.001) dan reverse tidak signifikan
    u1 = findings["Uji 1 (Fase 1 Pra-Konpers 15m: Public -> Media)"]
    assert u1["Signifikan_Statistik"] is True
    assert u1["P-value"] < 0.001
    assert u1["Reverse_Check_Media_to_Public"]["Signifikan_Statistik"] is False

    # Fase 2 (Media -> Public) harus signifikan secara statistik (p < 0.001) dan reverse tidak signifikan
    u2 = findings["Uji 2 (Fase 2 Pasca-Konpers 15m: Media -> Public)"]
    assert u2["Signifikan_Statistik"] is True
    assert u2["P-value"] < 0.001
    assert u2["Reverse_Check_Public_to_Media"]["Signifikan_Statistik"] is False

    # Pooled 10-hour test harus secara jujur menandai Signifikan = False karena p > 0.05
    u3 = findings["Uji 3 (Pooled Hourly 10-Jam Tanpa Pemisahan Rezim)"]
    assert u3["Public_to_Media_Signifikan"] is False
    assert u3["Media_to_Public_Signifikan"] is False


def test_contradiction_matrix_integrity():
    """Memastikan matriks kontradiksi narasi tersedia dan valid."""
    contra_path = ROOT / "reports" / "contradiction_matrix.json"
    assert contra_path.exists()
    with open(contra_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list) and len(data) >= 3
