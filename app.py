import datetime
import os
import json
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Dashboard Analisis Narasi: Kasus Penyadapan Presiden",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan modern & bersih
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-primary { background-color: #dbeafe; color: #1e40af; }
    .badge-warning { background-color: #fef3c7; color: #92400e; }
    .badge-success { background-color: #dcfce7; color: #166534; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_all_data():
    excel_path = "data.xlsx"
    df_link = pd.read_excel(excel_path, sheet_name="Data Link")
    df_dist = pd.read_excel(excel_path, sheet_name="Distribusi Jam")
    df_kandidat = pd.read_excel(excel_path, sheet_name="Kandidat Awal")
    df_unverified = pd.read_excel(excel_path, sheet_name="Belum Terverifikasi")
    df_meta = pd.read_excel(excel_path, sheet_name="Metodologi")

    # Format tanggal
    if "Tanggal publikasi" in df_link.columns:
        df_link["Tanggal_Clean"] = pd.to_datetime(df_link["Tanggal publikasi"]).dt.date

    return df_link, df_dist, df_kandidat, df_unverified, df_meta


df_link, df_dist, df_kandidat, df_unverified, df_meta = load_all_data()

# ==========================================
# SIDEBAR: FILTER & KONTROL
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/satellite-sending-signal.png", width=64)
    st.title("Filter & Parameter")
    st.markdown("Kajian SNA & Network Agenda-Setting Kasus Penyadapan Presiden.")

    # Search Box
    search_keyword = st.text_input("🔍 Cari kata kunci / judul:", placeholder="cth: makar, lsp, kapolri, yusril...")

    # Filter Tahap Narasi
    tahap_options = sorted(df_link["Tahap narasi"].dropna().unique().tolist())
    selected_tahap = st.multiselect("Pilih Tahap Narasi:", options=tahap_options, default=tahap_options)

    # Filter Jenis Sumber
    sumber_options = sorted(df_link["Jenis sumber"].dropna().unique().tolist())
    selected_sumber = st.multiselect("Pilih Jenis Sumber:", options=sumber_options, default=sumber_options)

    # Filter Media / Portal
    media_options = sorted(df_link["Media / Akun"].dropna().unique().tolist())
    selected_media = st.multiselect("Pilih Media Tertentu (Opsional):", options=media_options, default=[])

    st.markdown("---")
    st.caption("📌 **Target Penelitian:** Publikasi Jurnal Scopus Q1 / SINTA 1.")
    st.caption("🔬 **Kerangka Teori:** Network Agenda-Setting (Guo & McCombs) & Framing (Entman).")


# Filter DataFrame utama
filtered_df = df_link.copy()
if selected_tahap:
    filtered_df = filtered_df[filtered_df["Tahap narasi"].isin(selected_tahap)]
if selected_sumber:
    filtered_df = filtered_df[filtered_df["Jenis sumber"].isin(selected_sumber)]
if selected_media:
    filtered_df = filtered_df[filtered_df["Media / Akun"].isin(selected_media)]
if search_keyword:
    pat = re.escape(search_keyword)
    filtered_df = filtered_df[
        filtered_df["Judul / deskripsi"].str.contains(pat, case=False, na=False) |
        filtered_df["Media / Akun"].str.contains(pat, case=False, na=False)
    ]

# ==========================================
# HEADER UTAMA
# ==========================================
st.markdown('<div class="main-header">📡 Media Intelligence & Network Agenda-Setting Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analisis Jaringan Aktor, Respons Publik, dan Dinamika Pembingkaian Kasus Penyadapan Presiden Prabowo Subianto</div>', unsafe_allow_html=True)

# Metric KPI Baris 1
m1, m2, m3, m4 = st.columns(4)
total_news = len(filtered_df)
unique_media = filtered_df["Media / Akun"].nunique()
prabowo_mentions = filtered_df["Judul / deskripsi"].str.contains(r"prabowo|presiden", case=False, regex=True).sum()
lsp_mentions = filtered_df["Judul / deskripsi"].str.contains(r"lsp|listyo|sigit|tersangka", case=False, regex=True).sum()

m1.metric("Total Berita Terfilter", f"{total_news} / 200", delta="Korpus Terverifikasi")
m2.metric("Portal Media Aktif", f"{unique_media} Media", delta="Nasional & Global")
m3.metric("Sentralitas Presiden", f"{prabowo_mentions} ({prabowo_mentions/max(total_news,1)*100:.1f}%)", delta="Fokus Utama")
m4.metric("Keterkaitan Tersangka LSP", f"{lsp_mentions} ({lsp_mentions/max(total_news,1)*100:.1f}%)", delta="Kutub Legal")

st.markdown("---")

# ==========================================
# TABS UTAMA DASHBOARD
# ==========================================
tab_summary, tab_timeline, tab_rq1, tab_rq2, tab_rq3, tab_nodexl, tab_worlda, tab_data = st.tabs([
    "📊 Ringkasan Eksekutif",
    "⏱️ Timeline & Jam Kritis (3 Nov)",
    "🕸️ RQ1: Jaringan Aktor & Broker",
    "👥 RQ2: Komunitas & Framing Publik",
    "🔄 RQ3: Network Agenda-Setting",
    "🌐 4 Pilar SNA & NodeXL Pro",
    "🛰️ World A.LIVE & Kontradiksi",
    "📑 Penjelajah Data & Ekspor"
])

# -----------------------------------------------------------------------------
# TAB 1: RINGKASAN EKSEKUTIF
# -----------------------------------------------------------------------------
with tab_summary:
    st.subheader("Ringkasan Distribusi & Karakteristik Korpus Media")

    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        st.markdown("**Proporsi 7 Tahap Narasi Pemberitaan**")
        tahap_dist = filtered_df["Tahap narasi"].value_counts().reset_index()
        tahap_dist.columns = ["Tahap Narasi", "Jumlah Berita"]
        fig_tahap = px.pie(
            tahap_dist,
            names="Tahap Narasi",
            values="Jumlah Berita",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_tahap.update_traces(textposition='inside', textinfo='percent+label')
        fig_tahap.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=380, showlegend=False)
        st.plotly_chart(fig_tahap, width="stretch")

    with col_chart2:
        st.markdown("**Top 10 Media / Portal Peliput Terbanyak**")
        top_media = filtered_df["Media / Akun"].value_counts().head(10).reset_index()
        top_media.columns = ["Media / Akun", "Jumlah"]
        fig_media = px.bar(
            top_media,
            x="Jumlah",
            y="Media / Akun",
            orientation="h",
            color="Jumlah",
            color_continuous_scale="Blues",
            text="Jumlah"
        )
        fig_media.update_layout(yaxis=dict(autorange="reversed"), margin=dict(t=20, b=20, l=20, r=20), height=380)
        st.plotly_chart(fig_media, width="stretch")

    # Profil singkat kasus
    st.markdown("""
    > **Temuan Kunci Ringkasan:**
    > 1. Pemberitaan paling masif terpusat pada **Tahap 4 (Respons pemerintah/elite)** dengan 74 artikel (37.0%), diikuti oleh **Tahap 6 (Analisis/liputan lanjutan)** dengan 46 artikel (23.0%).
    > 2. JPNN, Jawa Pos, ANTARA, dan Okezone menjadi produsen berita utama yang menggerakkan volume informasi nasional.
    > 3. Sebanyak 19 artikel berasal dari media internasional / berbahasa Inggris (Kompas English, Jakarta Globe, TRT World, Tempo English) yang membingkai isu dalam koridor *national security vulnerability*.
    """)

# -----------------------------------------------------------------------------
# TAB 2: TIMELINE & TITIK BALIK HARI KRITIS
# -----------------------------------------------------------------------------
with tab_timeline:
    st.subheader("Rekonstruksi Temporal Hari Kritis (Selasa, 3 November 2026)")
    st.markdown("Perbandingan volume publikasi sebelum vs sesudah Konferensi Pers Resmi Mabes Polri (20.00 WIB).")

    # Bersihkan sheet Distribusi Jam: ambil hanya baris jam numerik (14.00 s.d. 23.00)
    num_jam = pd.to_numeric(df_dist["Jam (WIB), 3 Nov 2026"], errors="coerce")
    v_dist = df_dist[num_jam.notna()].copy()
    v_dist["Jam_Float"] = num_jam[num_jam.notna()]
    v_dist["Jam_Label"] = v_dist["Jam_Float"].apply(lambda x: f"{int(x):02d}.00 WIB")

    fig_jam = go.Figure()
    v_pra = v_dist[v_dist["Jam_Float"] < 20.0]
    v_post = v_dist[v_dist["Jam_Float"] >= 20.0]

    fig_jam.add_trace(go.Bar(
        x=v_pra["Jam_Label"],
        y=v_pra["Jumlah berita"],
        name="Fase Rumor & Pra-Konferensi (14.00 - 19.59)",
        marker_color="#ef4444",
        text=v_pra["Tahap narasi dominan"],
        hoverinfo="x+y+text"
    ))

    fig_jam.add_trace(go.Bar(
        x=v_post["Jam_Label"],
        y=v_post["Jumlah berita"],
        name="Fase Konfirmasi & Resonansi Resmi (20.00 - 23.59)",
        marker_color="#2563eb",
        text=v_post["Tahap narasi dominan"],
        hoverinfo="x+y+text"
    ))

    fig_jam.add_vline(
        x=5.5,
        line_width=2.5,
        line_dash="dash",
        line_color="#b91c1c",
        annotation_text="Konferensi Pers Bareskrim (20.00 WIB)",
        annotation_position="top left"
    )

    fig_jam.update_layout(
        title="Volume Publikasi Berita Per Jam pada 3 Nov 2026 (N = 146 Berita)",
        xaxis_title="Jam Penayangan (WIB)",
        yaxis_title="Jumlah Artikel",
        barmode="group",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_jam, width="stretch")

    c_box1, c_box2 = st.columns(2)
    with c_box1:
        st.info("""
        **Fase Pra-Konferensi Pers (14.00 - 19.59 WIB):**
        - Total berita: **39 artikel (26.7%)**.
        - Didominasi portal berita niche & media daerah (AFU.id, law-justice, RMOL Jateng, Optika.id).
        - Pembingkaian mengarah pada spekulasi penangkapan petinggi kepolisian dan operasi senyap.
        """)
    with c_box2:
        st.success("""
        **Fase Pasca-Konferensi Pers (20.00 - 23.59 WIB):**
        - Total berita: **107 artikel (73.3%)**.
        - Lonjakan drastis dalam kurun waktu 4 jam setelah penetapan status tersangka eks Kapolri LSP.
        - Terjadi *reframing* masif menjadi wacana hukum pidana "murni oknum, bukan kebijakan institusi".
        """)

# -----------------------------------------------------------------------------
# TAB 3: RQ1: JARINGAN AKTOR & BROKER NARASI
# -----------------------------------------------------------------------------
with tab_rq1:
    st.subheader("RQ1: Struktur Jaringan Aktor dan Narasumber dalam Liputan Media")

    actors_patterns = {
        "Presiden Prabowo Subianto": r"prabowo|presiden",
        "Eks Kapolri LSP / Tersangka": r"lsp|listyo|sigit|tersangka",
        "Mabes Polri / Bareskrim": r"bareskrim|mabes polri|propam|divpropam",
        "DPR RI / Parpol (Pansus)": r"dpr|pansus|pdip|gerindra|parpol",
        "Kapolri Jenderal Suyudi": r"suyudi|kapolri",
        "Menko Yusril Ihza Mahendra": r"yusril",
        "Isu Makar / Kudeta": r"makar|kudeta|operasi senyap",
        "Pakar Hukum & LSM Sipil": r"pakar|pengamat|kontras|icw|isess|huda"
    }

    actor_counts = {}
    for act, pat in actors_patterns.items():
        actor_counts[act] = filtered_df["Judul / deskripsi"].str.contains(pat, case=False, regex=True).sum()

    df_actors = pd.DataFrame(list(actor_counts.items()), columns=["Entitas / Aktor", "Frekuensi"])
    df_actors["Persentase"] = (df_actors["Frekuensi"] / len(filtered_df) * 100).round(1)
    df_actors = df_actors.sort_values(by="Frekuensi", ascending=True)

    fig_actors = px.bar(
        df_actors,
        x="Frekuensi",
        y="Entitas / Aktor",
        orientation="h",
        color="Frekuensi",
        color_continuous_scale="Teal",
        text=df_actors.apply(lambda r: f"{r['Frekuensi']} ({r['Persentase']}%)", axis=1)
    )
    fig_actors.update_layout(height=420, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_actors, width="stretch")

    st.markdown("### Analisis Peran Pialang Narasi (*Narrative Brokerage*)")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("""
        #### 🏛️ Yusril Ihza Mahendra
        **Peran:** *Political Reconciler Broker*
        - Menjembatani Istana dan Kepolisian.
        - Memastikan narasi *"Presiden tahu disadap dari laporan resmi Kapolri Jenderal Suyudi"* masuk ke media.
        - Mencegah persepsi keretakan antara Presiden dan pimpinan Polri.
        """)
    with b2:
        st.markdown("""
        #### 🛡️ Mabes Polri (Bareskrim)
        **Peran:** *Defensive Institutional Buffer*
        - Membatasi krisis dengan frame *"tindakan murni oknum personal"*.
        - Mensterilkan institusi kepolisian dari tuduhan makar institusional.
        - Menjadi penyuplai kutipan terbesar pasca jam 20.00 WIB.
        """)
    with b3:
        st.markdown("""
        #### ⚖️ DPR RI (Komisi III & PDIP)
        **Peran:** *Accountability & Policy Broker*
        - Menghubungkan keresahan publik ke arena legislatif.
        - Mengusulkan pembentukan **Pansus Angket Penyadapan**.
        - Menuntut audit komprehensif perangkat intersepsi intelijen.
        """)

# -----------------------------------------------------------------------------
# TAB 4: RQ2: KOMUNITAS & FRAMING PUBLIK
# -----------------------------------------------------------------------------
with tab_rq2:
    st.subheader("RQ2: Komunitas Publik, Pembingkaian Dominan, dan Pemantik Pertama")

    st.markdown("#### 1. Kronologi Pemantik Pertama ke Ruang Publik")
    st.markdown("""
    - **Fase 0 (2 Nov malam):** Beredar pesan berantai di grup WhatsApp politik/keamanan dan cuitan akun X anonim.
    - **Fase 1 (3 Nov 14.00 WIB):** Diberitakan oleh portal niche (*Kaki News, Inilah.com, law-justice, Wartakotalive, Kabar24, Aktual.com*).
    - **Fase 2 (3 Nov 15.00 WIB):** *AFU.id* menerbitkan rincian operasi senyap Divpropam di Mako Brimob.
    - **Fase 3 (3 Nov 16.23 WIB):** *CNN Indonesia* mempublikasikan tanggapan awal Mabes Polri yang menyatakan *"sedang mengecek informasi"*.
    """)

    st.markdown("#### 2. Tabel 20 Kandidat Berita Awal (Sheet Kandidat Awal)")
    st.dataframe(
        df_kandidat[["Jam bucket indeks (WIB)", "Media", "Judul menurut indeks", "Status"]],
        width="stretch",
        hide_index=True
    )

    st.markdown("#### 3. Klaster Komunitas Publik (Berdasarkan Pemodelan NodeXL)")
    k1, k2 = st.columns(2)
    with k1:
        st.info("""
        **Komunitas G1: Loyalis Pro-Pemerintah**
        - **Frame:** *Victimization & Law Enforcement*
        - **Stance:** Pro-Prabowo, mengutuk pelaku, mendukung pembersihan Polri.
        - **Kata Kunci:** `#KawalPrabowo`, `TindakTegas`, `OknumPengkhianat`, `KapolriHebat`.
        """)
        st.warning("""
        **Komunitas G3: Warganet Spekulatif & WAG**
        - **Frame:** *Factional Coup / "Perang Bintang"*
        - **Stance:** Sensasionalis, mempercayai adanya perang faksi antar-jenderal.
        - **Kata Kunci:** `PerangBintang`, `Makar`, `Kudeta`, `FaksiJenderal`.
        """)
    with k2:
        st.error("""
        **Komunitas G2: Oposisi & Aktivis Sipil (X)**
        - **Frame:** *Systemic Abuse of Power & Failed Reform*
        - **Stance:** Menolak narasi "hanya oknum", menuntut akuntabilitas negara & Pansus DPR.
        - **Kata Kunci:** `#PansusPenyadapan`, `BukanSekadarOknum`, `ReformasiPolri`.
        """)
        st.success("""
        **Komunitas G4: Pakar Hukum & Media Asing**
        - **Frame:** *Cyber Security Breach & National Threat*
        - **Stance:** Objektif, menyoroti kelemahan sandi negara dan dampak diplomasi.
        - **Kata Kunci:** `StateSurveillance`, `Wiretapping`, `NationalSecurity`.
        """)

# -----------------------------------------------------------------------------
# TAB 5: RQ3: NETWORK AGENDA-SETTING
# -----------------------------------------------------------------------------
with tab_rq3:
    st.subheader("RQ3: Pengujian Model Network Agenda-Setting (Media vs. Publik)")

    st.markdown("""
    Dalam kerangka **Network Agenda-Setting (NAS)** (Guo & McCombs, 2011), transfer atribut antara media dan publik pada kasus ini terbukti mengikuti pola **Two-Phase Reversal Flow**:
    """)

    fase_c1, fase_c2 = st.columns(2)
    with fase_c1:
        st.markdown("""
        ### 🔄 Fase 1: Bottom-Up Agenda Flow
        *(2 Nov malam – 3 Nov 16.00 WIB)*
        - **Agenda publik mendahului media.**
        - Rumor meledak di X dan WAG dengan atribut *"kudeta, penangkapan jenderal, makar"*.
        - Media arus utama menahan diri menunggu verifikasi resmi.
        - Tekanan publik yang masif memaksa Mabes Polri merespons pada pukul 16.23 WIB.
        """)
    with fase_c2:
        st.markdown("""
        ### 🎯 Fase 2: Top-Down Domestication
        *(3 Nov 20.00 WIB – 8 Nov 2026)*
        - **Agenda media merebut kendali publik.**
        - Konferensi pers Bareskrim membanjiri ruang wacana dengan **107 artikel berita dalam 4 jam**.
        - Media arus utama sukses melakukan *reframing*: mengganti kata *"makar/kudeta"* menjadi *"tersangka penyadapan ilegal oleh oknum personal"*.
        - Publik terdisiplinkan mengikuti koridor wacana hukum formal.
        """)

    # Tabel Leksikon
    st.markdown("#### Proporsi Atribut Framing Kata Kunci Per Tahap Narasi (%)")
    lexicon_data = {
        "Tahap Narasi": ["1 Rumor", "2 Respons Polri Pra-Konpers", "3 Konfirmasi Resmi", "4 Respons Pemerintah/Elite", "5 Bantahan/Klarifikasi", "6 Analisis/Liputan Lanjutan", "7 Internasional"],
        "Negatif/Krisis": [62.5, 42.9, 82.4, 50.0, 28.6, 50.0, 0.0],
        "Penegakan Hukum Resmi": [18.8, 21.4, 41.2, 29.7, 57.1, 28.3, 5.3],
        "Bantahan / Oknum": [87.5, 78.6, 0.0, 18.9, 78.6, 6.5, 0.0],
        "Pengawasan Parlemen / Politik": [25.0, 0.0, 70.6, 73.0, 7.1, 47.8, 57.9]
    }
    df_lex = pd.DataFrame(lexicon_data)
    fig_lex = px.bar(
        df_lex,
        x="Tahap Narasi",
        y=["Negatif/Krisis", "Penegakan Hukum Resmi", "Bantahan / Oknum", "Pengawasan Parlemen / Politik"],
        title="Dinamika Leksikon Framing Sepanjang 7 Tahap Narasi",
        barmode="stack",
        height=450
    )
    st.plotly_chart(fig_lex, width="stretch")

# -----------------------------------------------------------------------------
# TAB 6: 8 DIMENSI ANALISIS NODEXL & SOCIAL NETWORK ANALYSIS
# -----------------------------------------------------------------------------
with tab_nodexl:
    st.subheader("🌐 8 Dimensi Analisis NodeXL Pro & Social Network Analysis (SNA)")
    st.markdown("Implementasi terpadu metode Social Network Analysis sesuai standar NodeXL Pro, Max Planck Institute, dan jurnal terindeks Scopus Q1.")

    # Tombol Unduh NodeXL Workbook
    try:
        with open("nodexl_penyadapan_prabowo.xlsx", "rb") as f_nodexl:
            nodexl_bytes = f_nodexl.read()
        st.download_button(
            label="📥 Unduh Workbook Resmi NodeXL Pro (nodexl_penyadapan_prabowo.xlsx)",
            data=nodexl_bytes,
            file_name="nodexl_penyadapan_prabowo.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Buka file ini langsung di NodeXL Pro / NodeXL Cloud untuk visualisasi graf otomatis.",
            width="stretch"
        )
    except Exception as e:
        st.caption(f"Workbook NodeXL dapat dibuat via export_to_nodexl.py")

    st.markdown("---")

    # Matriks 8 Dimensi Analisis
    dim1, dim2 = st.columns(2)

    with dim1:
        st.markdown("### 1. 🗺️ Pemetaan Jaringan (Network Graph)")
        st.markdown("""
        - **Simpul (Nodes):** 59 entitas (Media Massa & Narasumber/Aktor Kunci).
        - **Sisi (Edges):** 85 relasi penyiaran berita terbobot (*weighted bipartite edges*).
        - **Layout:** *Fruchterman-Reingold / ForceAtlas2* memisahkan kutub hukum dan politik.
        """)
        try:
            if os.path.exists("chart_sna_network_map.png"):
                st.image("chart_sna_network_map.png", caption="Peta Jaringan Bipartit (NodeXL & Louvain Clusters)", width="stretch")
            elif os.path.exists("output/charts/entity_network.png"):
                st.image("output/charts/entity_network.png", caption="Peta Jaringan Bipartit (NodeXL & Louvain Clusters)", width="stretch")
        except Exception:
            pass

        st.markdown("### 2. 🏘️ Analisis Komunitas (Louvain Groups)")
        st.markdown("""
        - **Kualitas Partisi Modularity (Q):** `0.3335` (Klasterisasi signifikan).
        - **Jumlah Komunitas:** 8 Klaster terdeteksi.
        """)
        try:
            df_nodexl_grp = pd.read_excel("nodexl_penyadapan_prabowo.xlsx", sheet_name="Groups")
            st.dataframe(df_nodexl_grp[["Group", "Label", "Vertex Count", "Edge Count"]], width="stretch", hide_index=True)
        except Exception:
            pass

        st.markdown("### 3. ⭐ Analisis Influencer & Centrality Metrics")
        st.markdown("Identifikasi simpul paling berpengaruh berdasarkan 5 metrik sentralitas:")
        try:
            df_infl = pd.read_csv("sna_influencer_centrality.csv")
            top_infl = df_infl[df_infl["Tipe"] == "Narasumber"].head(6)
            st.dataframe(top_infl[["Nama Simpul", "Degree", "Betweenness Centrality (Broker)", "Eigenvector Centrality", "PageRank"]], width="stretch", hide_index=True)
        except Exception:
            pass

        st.markdown("### 4. 🏷️ Analisis Hashtag & Kata Kunci Dominan")
        st.markdown("""
        - `#KawalPrabowo` (Sentimen Dukungan & Kedaulatan Negara)
        - `#PansusPenyadapan` (Wacana Akuntabilitas DPR RI & PDIP)
        - `#PerangBintang` (Wacana Spekulatif Persaingan Antar-Jenderal)
        - `#WiretappingScandal` (Sorotan Komunitas Diplomatik & Asing)
        - `#ReformasiPolri` (Tuntutan Evaluasi Institusi Pasca-Kasus)
        """)

    with dim2:
        st.markdown("### 5. 🎭 Analisis Sentimen Publik & Media")
        sentimen_data = {
            "Valensi Sentimen": ["Negatif / Krisis", "Netral / Klarifikasi", "Positif / Penegakan Hukum"],
            "Proporsi (%)": [52.5, 27.5, 20.0]
        }
        fig_sent = px.pie(
            pd.DataFrame(sentimen_data),
            names="Valensi Sentimen",
            values="Proporsi (%)",
            color="Valensi Sentimen",
            color_discrete_map={"Negatif / Krisis": "#ef4444", "Netral / Klarifikasi": "#94a3b8", "Positif / Penegakan Hukum": "#10b981"},
            hole=0.45
        )
        fig_sent.update_layout(height=260, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_sent, width="stretch")

        st.markdown("### 6. ⏱️ Analisis Temporal (Dinamika Waktu)")
        st.markdown("""
        - **3 Nov, 14.00 - 19.59 WIB:** Ledakan rumor awal di media niche & media sosial.
        - **3 Nov, 20.00 WIB:** Konferensi pers penetapan tersangka LSP (Titik balik agenda).
        - **3 Nov, 20.00 - 23.59 WIB:** 107 artikel resmi diterbitkan dalam tempo 4 jam.
        - **4 - 8 Nov 2026:** Respons politik DPR, Menko Yusril, dan liputan internasional.
        """)

        st.markdown("### 7. 🏛️ Analisis Jaringan Kebijakan (Policy Network)")
        st.markdown("""
        Pemetaan relasi kelembagaan publik:
        - **Kutub Eksekutif:** Presiden Prabowo ↔ Menko Yusril Ihza Mahendra.
        - **Kutub Aparat Hukum:** Mabes Polri / Bareskrim ↔ Kapolri Jenderal Suyudi.
        - **Kutub Legislatif:** Komisi III DPR RI ↔ Fraksi Oposisi (PDIP) & Koalisi.
        - **Kutub Pengawas Eksternal:** Pakar Hukum Pidana (Chairul Huda) & LSM (ISESS/KontraS).
        """)

        st.markdown("### 8. 🚨 Analisis Disinformasi & Pola Difusi")
        st.markdown("""
        **Rantai Penyebaran Informasi (*Information Diffusion Cascade*):**
        1. **Fase Inisiasi (Dark Social):** Pesan berantai WAG politik/keamanan (2 Nov malam).
        2. **Fase Amplifikasi (Portal Niche):** Kaki News, Inilah.com, law-justice (3 Nov 14.00 WIB).
        3. **Fase Penetrasi Mainstream:** CNN Indonesia memuat respons awal Polri (3 Nov 16.23 WIB).
        4. **Fase Domestikasi Fakta:** Konferensi pers Bareskrim mematikan rumor makar menjadi delik pidana oknum (3 Nov 20.00 WIB).
        """)

# -----------------------------------------------------------------------------
# TAB 7: WORLD A.LIVE & KONTRADIKSI
# -----------------------------------------------------------------------------
with tab_worlda:
    st.subheader("🛰️ Integrasi World A.LIVE & Deteksi Kontradiksi Narasi (Reportica)")
    st.markdown("""
    Tab ini mengintegrasikan feed berita publik dari **[World A.LIVE](https://worlda.live/indonesia/newspaper)**
    dan mesin analisis **Reportica Intelligent** untuk memetakan pertentangan klaim naratif serta linimasa publikasi berita secara real-time.
    """)

    # 1. Headline Koran Harian World A.LIVE
    worlda_news_path = "output/worlda/newspaper_edisi_terkini.json"
    if os.path.exists(worlda_news_path):
        try:
            with open(worlda_news_path, "r", encoding="utf-8") as f:
                news_meta = json.load(f)
            
            st.info(f"📰 **Edisi Koran Terkini:** {news_meta.get('edisi', 'Koran Harian')} — *{news_meta.get('deskripsi', '')}* (Total: {news_meta.get('total_berita', 0)} tajuk topik)")
        except Exception:
            pass

    # 2. Dataset Linimasa 114 Berita Penyadapan Prabowo
    topic_csv_path = "output/worlda/penyadapan_prabowo_114_berita.csv"
    topic_json_path = "output/worlda/penyadapan_prabowo_114_berita.json"
    df_worlda = None
    if os.path.exists(topic_csv_path):
        df_worlda = pd.read_csv(topic_csv_path)
    elif os.path.exists(topic_json_path):
        with open(topic_json_path, "r", encoding="utf-8") as f:
            worlda_json = json.load(f)
        df_worlda = pd.DataFrame(worlda_json.get("artikel", []))

    if df_worlda is not None and not df_worlda.empty:
        
        st.markdown("### 1. ⏱️ Linimasa & Sebaran 114 Berita Penyadapan (World A.LIVE)")
        st.markdown("Sebaran 114 liputan berita pada edisi Sabtu, 7 November 2026 berdasarkan jam tayang dan outlet media.")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Total Berita Terkumpul", f"{len(df_worlda)}")
        m_col2.metric("Jumlah Media Portal", f"{df_worlda['outlet'].nunique()} Outlet")
        m_col3.metric("Puncak Pemberitaan", f"{df_worlda['hour_wib'].value_counts().index[0]}:00 WIB ({df_worlda['hour_wib'].value_counts().iloc[0]} Berita)")
        
        # Chart Distribusi Jam & Media
        w_chart1, w_chart2 = st.columns(2)
        with w_chart1:
            hourly_counts = df_worlda.groupby("hour_wib").size().reset_index(name="Jumlah Berita")
            hourly_counts["Jam"] = hourly_counts["hour_wib"].apply(lambda h: f"{int(h):02d}:00")
            fig_w_hour = px.bar(
                hourly_counts,
                x="Jam",
                y="Jumlah Berita",
                title="Distribusi Frekuensi Berita per Jam (WIB)",
                color="Jumlah Berita",
                color_continuous_scale="Teal"
            )
            fig_w_hour.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_w_hour, width="stretch")
            
        with w_chart2:
            top_outlets = df_worlda["outlet"].value_counts().head(8).reset_index()
            top_outlets.columns = ["Media", "Jumlah Berita"]
            fig_w_media = px.bar(
                top_outlets,
                x="Jumlah Berita",
                y="Media",
                orientation="h",
                title="Top 8 Media Portal Paling Aktif",
                color="Jumlah Berita",
                color_continuous_scale="Blues"
            )
            fig_w_media.update_layout(height=350, yaxis=dict(autorange="reversed"), margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_w_media, width="stretch")

        # Tabel Berita Interaktif
        with st.expander("🔍 Buka Penjelajah 114 Artikel Berita Lengkap (Tautan & Waktu)", expanded=False):
            st.dataframe(
                df_worlda[["hour_wib", "outlet", "headline", "url"]].rename(columns={
                    "hour_wib": "Jam (WIB)",
                    "outlet": "Media Outlet",
                    "headline": "Judul Berita",
                    "url": "Tautan"
                }),
                width="stretch",
                hide_index=True
            )

    # 3. Matriks Deteksi Kontradiksi (Reportica Engine)
    contra_path = "reports/contradiction_matrix.json"
    if os.path.exists(contra_path):
        st.markdown("---")
        st.markdown("### 2. ⚖️ Matriks Deteksi Kontradiksi Narasi (Reportica Intelligent Engine)")
        st.markdown("""
        Berdasarkan metodologi investigasi kontradiksi *(TinyFish / Reportica Intelligent)*,
        perkembangan narasi dianalisis bukan dari mencari satu klaim yang benar,
        melainkan **memetakan friksi antar-klaim berlawanan** (*contradictions as the signal*):
        """)
        
        with open(contra_path, "r", encoding="utf-8") as f:
            contra_data = json.load(f)
            
        for c in contra_data:
            with st.container():
                st.markdown(f"#### 📍 {c.get('axis', '')}")
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    st.error(f"**Klaim A:** {c.get('claim_a_title', '')}")
                    st.caption(f"Volume Liputan: **{c.get('claim_a_count', 0)} artikel** | Aktor Pengusung: *{c.get('claim_a_actors', '')}*")
                with c_col2:
                    st.success(f"**Klaim B:** {c.get('claim_b_title', '')}")
                    st.caption(f"Volume Liputan: **{c.get('claim_b_count', 0)} artikel** | Aktor Pengusung: *{c.get('claim_b_actors', '')}*")
                st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

    # 4. Diagram Alir Arsitektur Pipeline
    st.markdown("---")
    st.markdown("### 3. 🗺️ Diagram Alir Arsitektur Sistem Terpadu")
    st.markdown("""
    Alur kerja integrasi dari pengumpulan data (*World A.LIVE / News Scrapers / Social API*),
    validasi deduplikasi, pemrosesan analitik (*Reportica, NodeXL, Temporal Granger*), hingga diseminasi laporan riset Scopus Q1.
    """)
    flowchart_img_path = "flowcharts/pipeline_flowchart.png"
    if os.path.exists(flowchart_img_path):
        st.image(flowchart_img_path, caption="Diagram Alir Pipeline Sistem Terpadu (World A.LIVE + NodeXL + Reportica)", width="stretch")

    # 5. Diagram Alir PRISMA 2020
    st.markdown("---")
    st.markdown("### 4. 📋 Diagram Alir Seleksi Korpus Berstandar PRISMA 2020")
    st.markdown("""
    Transparansi seleksi korpus berita dan respons publik digital mengikuti protokol baku **PRISMA 2020** (*Preferred Reporting Items for Systematic Reviews and Meta-Analyses*), memetakan 4 fase: **Identifikasi**, **Penyaringan**, **Kelayakan**, dan **Inklusi Final**.
    """)
    prisma_img_path = "flowcharts/prisma_2020_flowchart.png"
    if os.path.exists(prisma_img_path):
        st.image(prisma_img_path, caption="Diagram Alir PRISMA 2020 untuk Seleksi Korpus Berita & Diskursus Publik", width="stretch")

    # 6. Peta Bibliometrik VOSviewer
    st.markdown("---")
    st.markdown("### 5. 🔬 Peta Bibliometrik Literatur VOSviewer (Co-Occurrence & Klaster Tematik)")
    st.markdown("""
    Pemetaan bibliometrik literatur global komunikasi politik dan krisis menggunakan **VOSviewer** membagi 40 kata kunci seminal ke dalam 4 klaster utama:
    - **Klaster 1 (Merah):** *Third-Level Network Agenda-Setting & Cognitive Networks* (Guo & McCombs, Vargo).
    - **Klaster 2 (Hijau):** *Crisis Communication, Political Scandals & Narrative Framing* (Entman, Coombs).
    - **Klaster 3 (Biru):** *Social Network Analysis, Betweenness Centrality & Structural Holes* (Freeman, Burt).
    - **Klaster 4 (Kuning):** *Hybrid Media Systems, Disinformation & Dark Social* (Chadwick, Bennett).
    """)
    vos_img_path = "vosviewer/vosviewer_bibliometric_map.png"
    if os.path.exists(vos_img_path):
        st.image(vos_img_path, caption="Peta Bibliometrik VOSviewer: Analisis Co-Occurrence Kata Kunci Seminal (4 Klaster Tematik)", width="stretch")

    st.markdown("""
    ```mermaid
    graph TD
        subgraph S1["1. DATA INGESTION LAYER"]
            A1["World A.LIVE Topic Feed"] --> B1["Collector Module (worlda_collector.py)"]
            A2["Direct Portal Scrapers (Antara, JawaPos, JPNN, Viva, dll.)"] --> B1
            A3["Social Media Streams (X, WAG, YouTube API)"] --> B1
        end

        subgraph S2["2. PROCESSING & VALIDATION"]
            B1 --> C1["Deduplication & Wire Origin Filter (ANTARA/Reuters)"]
            C1 --> C2["Integrity Hashing (SHA-256) & Metadata Extraction"]
            C2 --> C3[("Data Repository: data.xlsx / articles.csv")]
        end

        subgraph S3["3. ANALYTICS & INTELLIGENCE ENGINES"]
            C3 --> D1["Reportica Engine (Contradiction & Framing Matrix)"]
            C3 --> D2["SNA Engine (NodeXL Pro Bipartite & Community Detection)"]
            C3 --> D3["Temporal Engine (Time-Series & Granger Causality)"]
        end

        subgraph S4["4. REPORTING & DISSEMINATION LAYER"]
            D1 --> E1["Reportica Intelligence Brief (Executive Markdown)"]
            D2 --> E2["NodeXL Pro Workbook (.xlsx) & GraphML"]
            D3 --> E3["Scopus Q1 Academic Manuscript (IMRaD)"]
            D1 & D2 & D3 --> E4["World A.LIVE Live Clone Dashboard (Streamlit Cloud)"]
            E4 --> E5["Terminal Bash CLI Tool (worlda-intelligence.sh)"]
        end
    ```
    """)

# -----------------------------------------------------------------------------
# TAB 8: PENJELAJAH DATA & EKSPOR
# -----------------------------------------------------------------------------
with tab_data:
    st.subheader("Penjelajah Data Korpus Berita")
    st.markdown(f"Menampilkan **{len(filtered_df)}** dari total **200** artikel berita terverifikasi.")

    show_cols = ["No", "Media / Akun", "Judul / deskripsi", "Tanggal publikasi", "Tahap narasi", "Jenis sumber", "URL"]
    valid_cols = [c for c in show_cols if c in filtered_df.columns]

    st.dataframe(
        filtered_df[valid_cols],
        width="stretch",
        hide_index=True
    )

    # Download Buttons
    st.markdown("### 📥 Unduh Manuskrip Riset (26 Halaman), Buku Kerja NodeXL, & Data")
    st.markdown("Seluruh berkas riset dapat diunduh langsung ke komputer/laptop Anda:")

    pdf_path = "MANUSCRIPT_SCOPUS_Q1_26_PAGES.pdf"
    docx_path = "MANUSCRIPT_SCOPUS_Q1_26_PAGES.docx"
    nodexl_path = "nodexl_penyadapan_prabowo.xlsx"

    dl_col1, dl_col2, dl_col3, dl_col4 = st.columns(4)

    with dl_col1:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📄 Unduh Naskah 26 Hal (PDF)",
                data=pdf_bytes,
                file_name="MANUSCRIPT_SCOPUS_Q1_26_PAGES.pdf",
                mime="application/pdf",
                width="stretch"
            )

    with dl_col2:
        if os.path.exists(docx_path):
            with open(docx_path, "rb") as f:
                docx_bytes = f.read()
            st.download_button(
                label="📝 Unduh Naskah Word (DOCX)",
                data=docx_bytes,
                file_name="MANUSCRIPT_SCOPUS_Q1_26_PAGES.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                width="stretch"
            )

    with dl_col3:
        if os.path.exists(nodexl_path):
            with open(nodexl_path, "rb") as f:
                xlsx_bytes = f.read()
            st.download_button(
                label="📊 Unduh NodeXL Pro (.xlsx)",
                data=xlsx_bytes,
                file_name="nodexl_penyadapan_prabowo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch"
            )

    with dl_col4:
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📑 Unduh Korpus CSV",
            data=csv_data,
            file_name="data_penyadapan_prabowo_filtered.csv",
            mime="text/csv",
            width="stretch"
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        f'<a href="https://github.com/25067020011-sudo/prabowo" target="_blank">'
        f'<button style="width:100%; height:42px; background-color:#1e3a8a; color:white; border:none; border-radius:8px; font-weight:600; cursor:pointer;">'
        f'🌐 Buka Repositori GitHub & Berkas VOSviewer</button></a>',
        unsafe_allow_html=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem;">
    Dashboard Analisis Jaringan Narasi Kasus Penyadapan Presiden &copy; 2026 | Berbasis Teori Network Agenda-Setting & Social Network Analysis
</div>
""", unsafe_allow_html=True)
