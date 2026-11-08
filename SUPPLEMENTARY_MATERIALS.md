# Supplementary Materials (Online Appendices)

**Title:** Network Topology of Political Scandals, Public Polarization, and Network Agenda-Setting in Hybrid Media Systems: The Case of the Indonesian Presidential Wiretapping Crisis  
**Target Journal:** *Journal of Communication* / *New Media & Society* (Scopus Q1)  
**Authors:** Computational Political Communication & Network Science Research Group  
**Permanent Open-Access Repository:** [https://github.com/25067020011-sudo/prabowo](https://github.com/25067020011-sudo/prabowo)  
**Live Interactive Intelligence Dashboard:** [https://prabowo-agendasetting.streamlit.app/](https://prabowo-agendasetting.streamlit.app/)

---

## TABLE OF CONTENTS

- **Section S1: Extended Methodological Protocols**
  - S1.1 Corpus Curation, Web Scraping Architecture, and Inclusion Criteria
  - S1.2 PRISMA 2020 Complete Audit Trail
  - S1.3 VOSviewer Bibliometric Mapping Configuration
- **Section S2: Social Network Analysis (SNA) Technical Specifications**
  - S2.1 NodeXL Pro Algorithmic Configuration
  - S2.2 Complete Centrality Metric Formulas & Definitions
  - S2.3 Full 59-Node Metric Table (Degree, Betweenness, Eigenvector, PageRank)
- **Section S3: Community Detection & Modularity Optimization**
  - S3.1 Louvain Modularity Partitioning ($Q = 0.3335$)
  - S3.2 Community Interaction Adjacency Matrix
- **Section S4: Temporal Analysis & Granger Causality Diagnostics**
  - S4.1 Hourly Publication & Public Comment Frequency Table
  - S4.2 Cross-Correlation Function (CCF) Diagnostic Table
  - S4.3 Vector Autoregressive (VAR) Model Output & Statistical Power Caveat
- **Section S5: Reportica Narrative Contradiction Matrix**
  - S5.1 Coding Methodology for Contradiction Detection
  - S5.2 Four Structural Contradiction Dimensions & Exemplar Quotes
- **Section S6: Complete Inventory of the Primary News Corpus ($N = 200$)**
- **Section S7: World A.LIVE Independent Replication Stream ($N = 114$)**

---

## SECTION S1: EXTENDED METHODOLOGICAL PROTOCOLS

### S1.1 Web Scraping & Ingestion Engine
Data collection was executed via a dedicated Python pipeline (`scrape_penyadapan.py` and `scrape_worlda.py`). The scraper features:
- Exponential backoff request throttler (default delay: 2.0 seconds).
- `robots.txt` compliance inspection with automatic fallback for CDN-protected news servers.
- Automated JSON-LD structured data extraction for publication datetime, author attribution, and headline canonicalization.
- SHA-256 cryptographic integrity hashing applied to title-URL pairs to eliminate duplicate syndicated wire reports.

### S1.2 PRISMA 2020 Complete Audit Trail
Corpus selection strictly adhered to the PRISMA 2020 statement:
1. **Identification:**
   - 342 candidate news items identified across 25 verified Indonesian news organizations.
   - 148 items harvested via World A.LIVE live aggregator.
   - 18,200 public comments harvested via YouTube Data API v3 and platform X interaction streams.
   - 78 duplicate articles removed via SHA-256 hash match; 46 verbatim wire syndications removed.
2. **Screening:**
   - 366 news items and 18,076 comments screened.
   - 68 off-topic or clickbait news items excluded; 44 items lacking verified hourly timestamps excluded.
   - 1,842 automated promotional spam comments removed; 814 unreadable comments (< 3 words) excluded.
3. **Eligibility:**
   - 254 full-text news reports sought for in-depth retrieval.
   - 18 paywalled or broken links excluded; 22 reports lacking direct source quotes excluded; 14 redundant aggregations excluded.
4. **Inclusion:**
   - Primary Verified News Corpus: $N = 200$ articles (Critical Hourly Sub-sample $n = 146$).
   - Independent Replication Stream: $N = 114$ articles.
   - Digital Public Response Corpus: $N = 15,420$ valid comments.

---

## SECTION S2: SOCIAL NETWORK ANALYSIS TECHNICAL SPECIFICATIONS

### S2.1 NodeXL Pro Algorithmic Configuration
- **Software:** NodeXL Pro (Version 1.0.1.534) & NetworkX 3.2.
- **Graph Type:** Undirected Bipartite Graph $G = (V_M, V_A, E)$.
- **Layout:** Harel-Koren Fast Multiscale Layout (500 iterations, edge tension = 1.0).
- **Node Size:** Proportional to Betweenness Centrality (5.0 to 35.0 pt).
- **Node Color:** Partitioned by Louvain modularity group assignment.

### S2.2 Centrality Metric Formulas
- **Degree Centrality:** $C_D(v) = \deg(v)$.
- **Betweenness Centrality:** $C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$.
- **Closeness Centrality:** $C_C(v) = \frac{N-1}{\sum_{u \neq v} d(v, u)}$.
- **Eigenvector Centrality:** $x_v = \frac{1}{\lambda} \sum_{u \in M(v)} x_u$.
- **PageRank:** $PR(v) = \frac{1-d}{N} + d \sum_{u \in M(v)} \frac{PR(u)}{L(u)}$ ($d = 0.85$).

---

## SECTION S3: COMMUNITY DETECTION & MODULARITY

### S3.1 Louvain Partitioning Summary ($Q = 0.3335$)
| Group ID | Label | Vertex Count | Edge Count | Group Density | Dominant Narrative Attribute |
|---|---|---|---|---|---|
| G1 | Executive Core (Presidency) | 14 | 26 | 0.2857 | Victim status, state stability, legal process |
| G2 | Suspect & Legal Accused (LSP) | 12 | 22 | 0.3333 | Individual accountability, telecommunications delict |
| G3 | Police Enforcement (Mabes Polri) | 9 | 15 | 0.4167 | Due process, evidence verification, rogue oknum |
| G4 | Parliamentary Oversight (DPR RI) | 7 | 10 | 0.4762 | Special Inquiry (Pansus), institutional audit |
| G5 | Constitutional Legal Experts | 6 | 8 | 0.5333 | Criminal code adherence, statutory boundaries |
| G6 | Civil Society & Human Rights NGOs | 5 | 6 | 0.6000 | Police reform, anti-impunity, surveillance audit |
| G7 | Cyber Defense & Technical Experts | 4 | 4 | 0.6667 | Cyber sovereignty, spyware vectors, BSSN review |
| G8 | International / Diplomatic Media | 2 | 2 | 1.0000 | Regional security, foreign intelligence intrigue |

---

## SECTION S4: TEMPORAL CROSS-CORRELATION & GRANGER DIAGNOSTICS

### S4.1 Hourly Publication & Public Commentary on November 3, 2026
| Hour (WIB) | News Articles ($M_t$) | Public Comments ($P_t$) | Cumulative News Share (%) | Primary Narrative Event |
|---|---|---|---|---|
| 14:00 | 5 | 1,240 | 3.4% | Niche portals break rumor of general arrests |
| 15:00 | 7 | 1,890 | 8.2% | Trending on platform X: #MakarJenderal |
| 16:00 | 12 | 2,450 | 16.4% | Initial Police response: 'we are checking' (16:23) |
| 17:00 | 6 | 1,670 | 20.5% | Social media speculation surges; palace silent |
| 18:00 | 5 | 1,420 | 24.0% | Broadcast news discusses cyber vulnerabilities |
| 19:00 | 4 | 1,150 | 26.7% | Mainstream pause awaiting Bareskrim briefing |
| 20:00 | 17 | 4,820 | 38.4% | Bareskrim press conference: LSP named suspect |
| 21:00 | 32 | 6,140 | 60.3% | Mainstream flood: 'purely rogue individual action' |
| 22:00 | 34 | 4,950 | 83.6% | Cabinet legal briefing by Coordinating Minister Yusril |
| 23:00 | 24 | 3,210 | 100.0% | Editorial consensus: judicial due process |

### S4.2 Cross-Correlation Function Coefficients
- $r_{-3} = 0.214$ ($p = 0.421$)
- $r_{-2} = 0.412$ ($p = 0.082$)
- $r_{-1} = 0.678$ ($p = 0.015$) &larr; **Statistically Significant Leading Public Effect**
- **$r_{0} = 0.896$ ($p = 0.0005$) &larr; Peak Contemporaneous Synchrony**
- $r_{+1} = 0.612$ ($p = 0.028$) &larr; **Statistically Significant Lagged Public Effect**
- $r_{+2} = 0.384$ ($p = 0.115$)
- $r_{+3} = 0.182$ ($p = 0.490$)

---

## SECTION S5: REPLICATION INSTRUCTIONS & FILE MANIFEST

### To Replicate in NodeXL Pro:
1. Open Microsoft Excel with NodeXL Pro installed.
2. Select **NodeXL > Import > From Open NodeXL Workbook**.
3. Choose `nodexl_penyadapan_prabowo.xlsx`.
4. Run **Show Graph** with *Harel-Koren Fast Multiscale* layout.

### To Run the Full Intelligence Pipeline:
```bash
git clone https://github.com/25067020011-sudo/prabowo.git
cd prabowo
pip install -r requirements.txt
bash worlda-intelligence.sh
```

### To Launch the Interactive Web Dashboard:
```bash
streamlit run app.py
```
Or access online directly at: [https://prabowo-agendasetting.streamlit.app/](https://prabowo-agendasetting.streamlit.app/)
