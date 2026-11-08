# OSF Pre-Registration Protocol: Network Agenda-Setting and Narrative Brokerage in Presidential Crisis Communication

**Repository:** Open Science Framework (OSF) Standard Pre-Registration Template  
**Date of Registration:** November 8, 2026  
**Status:** Pre-registered Prior to Final Inferential Hypotheses Testing  
**Project Identifier:** `osf.io/prabowo-wiretapping-sna-2026` (Hypothetical OSF DOI identifier)  
**Permanent Public Code & Data Repository:** [https://github.com/25067020011-sudo/prabowo](https://github.com/25067020011-sudo/prabowo)

---

## 1. STUDY INFORMATION

### 1.1 Title
Network Topology of Political Scandals, Public Polarization, and Network Agenda-Setting in Hybrid Media Systems: The Case of the Indonesian Presidential Wiretapping Crisis.

### 1.2 Description & Background
On November 2–3, 2026, allegations emerged regarding the illegal wiretapping and electronic surveillance targeting Indonesian President Prabowo Subianto, allegedly involving former National Police Chief General (Ret.) Listyo Sigit Prabowo (LSP). This study investigates the informational diffusion from encrypted messaging (*dark social*) into news media and social platform discourses, testing the Third-Level Network Agenda-Setting (NAS) model, information brokerage, and community polarization.

### 1.3 Theoretical Framework
1. **Third-Level Network Agenda-Setting (NAS) Theory** (Guo & McCombs, 2011; Vargo et al., 2014): Mental representations of issues exist as networked associative attribute bundles transferred between media and public domains.
2. **Structural Holes & Narrative Brokerage** (Burt, 2004; Freeman, 1978): Elite actors occupying high betweenness centrality positions act as gatekeepers who de-escalate or reframe institutional conflict.
3. **Hybrid Media System Theory** (Chadwick, 2017): Non-linear interactions between broadcast journalism verification logics and real-time digital network virality logics.

---

## 2. FORMAL RESEARCH QUESTIONS & HYPOTHESES

### 2.1 Research Question 1 (RQ1: Media Structure & Narrative Brokerage)
- **RQ1:** What is the topological structure of the actor-source network in media coverage of the presidential wiretapping scandal, and which institutional actors occupy central positions as narrative brokers?
- **Hypothesis 1 (H1):** Media coverage of the scandal will exhibit a **bipolar core-periphery structure**, separated between executive and law enforcement poles, with legal-constitutional ministers (e.g., Coordinating Minister Yusril Ihza Mahendra) exhibiting significantly higher betweenness centrality than partisan spokespersons.

### 2.2 Research Question 2 (RQ2: Public Community Polarization & Framing)
- **RQ2:** What distinct sub-communities emerge within digital public responses, what dominant frames characterize each cluster, and through which channels did the issue first penetrate the public sphere?
- **Hypothesis 2 (H2):** Public response interaction graphs will demonstrate significant structural modularity ($Q > 0.30$), dividing into distinct political stance clusters (Pro-Government institutionalist vs. Critical Opposition accountability vs. Speculative Factionalists).

### 2.3 Research Question 3 (RQ3: Network Agenda-Setting Directionality)
- **RQ3:** Does the mainstream media’s attribute network precede the public attribute network, or does the public agenda precede and force the media agenda across critical crisis phases?
- **Hypothesis 3 (H3 - Two-Phase Reversal Flow):** 
  - *Phase 3a (Pre-Press Conference):* Public discourse volume and "treason/coup" attribute bundles will temporally precede mainstream media coverage (bottom-up agenda-pushing).
  - *Phase 3b (Post-Press Conference 20:00 WIB):* Mainstream media "individual criminal act" attribute bundles will precede and restructure public cognitive framing (top-down domestication).

---

## 3. DESIGN PLAN & DATA COLLECTION

### 3.1 Data Collection & Inclusion Protocols (PRISMA 2020)
- **Primary News Corpus ($N = 200$):** Articles collected from 25 national online news portals, news agencies (ANTARA), broadcast sites (CNN Indonesia, Kompas TV), and verified newspapers (Jawa Pos, Detik, Tempo) covering November 3–8, 2026.
- **Hourly Critical Window ($N = 146$):** Hourly timestamped sub-corpus tracking November 3, 2026, 14:00–23:59 WIB.
- **Independent Replication Stream ($N = 114$):** Real-time aggregation stream extracted from World A.LIVE on November 7, 2026.
- **Digital Public Discourse Corpus ($N = 15,420$):** Public interactions and comments extracted via YouTube Data API v3 and social streams on platform X using verified query sets (`#PenyadapanPrabowo`, `#MakarJenderal`, `#ListyoSigit`, `#PansusPenyadapan`).

### 3.2 Exclusion Criteria
1. Articles with missing publication timestamps.
2. Syndicated press releases duplicated verbatim without journalistic value-add (deduplicated via SHA-256 hash).
3. Social media automated spam, promotional bots, or unreadable strings (< 3 words).

---

## 4. SAMPLING & ANALYSIS PLAN

### 4.1 Variables & Operationalization
1. **Network Centrality Metrics:**
   - Degree Centrality ($C_D$): Sum of direct media-source citation ties.
   - Betweenness Centrality ($C_B$): Proportion of all shortest paths passing through a given actor.
   - Eigenvector Centrality & PageRank: Influence scores weighting ties to other highly connected nodes.
2. **Community Detection:**
   - Louvain modularity algorithm ($Q$) with resolution parameter = 1.0.
3. **Cross-Correlation Function (CCF):**
   - Pearson cross-correlation $r_k$ computed for lags $k \in \{-3, -2, -1, 0, +1, +2, +3\}$ between hourly media publishing rate ($M_t$) and public comment volume ($P_t$).
4. **Framing Lexicon & Attribute Coding:**
   - Double-blind coding of 7 Narrative Stages (Rumor, Preliminary Police Reaction, Official Confirmation, Government Reaction, Factional Clarification, Deep Analysis, International).
   - Inter-coder reliability target: Krippendorff's alpha $\alpha \ge 0.80$.

---

## 5. RESEARCH INTEGRITY & ETHICAL COMMITMENTS
- **No Private Data Storage:** All user IDs from digital platforms are one-way cryptographic hashed (SHA-256).
- **Attribution Preservation:** No full copyrighted text is redistributed; metadata, quotes, and character-limited snippets ($\le 300$ chars) only.
- **Strict Analytical Neutrality:** No legal guilt or innocence is adjudicated; analysis strictly maps the dynamics of communicative interaction and public attribution.

