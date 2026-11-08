# Network Topology of Political Scandals, Public Polarization, and Network Agenda-Setting in Hybrid Media Systems: The Case of the Indonesian Presidential Wiretapping Crisis

**Working Title:** Network Agenda-Setting and Narrative Brokerage in Presidential Crisis Communication  
**Target Publication:** *Journal of Communication* / *New Media & Society* (Scopus Q1)  
**Authors:** Computational Political Communication & Network Science Research Group  
**Pre-registration:** Open Science Framework (OSF) Workflow Aligned  
**Dataset & Replication Code:** [https://github.com/25067020011-sudo/prabowo](https://github.com/25067020011-sudo/prabowo) | Live Intelligence Dashboard: [https://prabowo-agendasetting.streamlit.app/](https://prabowo-agendasetting.streamlit.app/)

---

## ABSTRACT

The proliferation of hybrid media systems has fundamentally altered how high-stakes political crises erupt, escalate, and resolve. In early November 2026, the alleged illegal wiretapping scandal targeting Indonesian President Prabowo Subianto provoked a nationwide institutional crisis implicating executive elites, law enforcement agencies, parliamentary factions, and digital public spheres. Drawing upon third-level Network Agenda-Setting (NAS) theory, framing theory, and structural holes/brokerage theory, this study investigates three interrelated dimensions: (1) the topological structure of actor-source networks and narrative brokerage in mainstream news coverage; (2) digital public community polarization, dominant frames, and the identification of initial diffusion triggers; and (3) the temporal directional flow of attribute networks between mass media and digital public discourse. 

Employing a mixed-methods computational design, we construct a verified multi-layer news corpus ($N = 200$), an independent replication stream ($N = 114$ from World A.LIVE), and digital interaction graphs analyzed via NodeXL Pro and Social Network Analysis (SNA) algorithms. Our findings reveal that: 
1. The media coverage network manifests a **bipolar core-periphery topology** where Coordinating Minister Yusril Ihza Mahendra (betweenness centrality = 0.0741) and the National Police Headquarters (Mabes Polri, betweenness = 0.1664) functioned as structural brokers bridging the executive presidency ($C_B = 0.7588$) and criminal suspects ($C_B = 0.3211$), mitigating cross-institutional crisis spillover.
2. The crisis was initially sparked via **dark social channels** (encrypted WhatsApp messaging networks) and anonymous accounts on X on the evening of November 2, penetrating niche alternative digital outlets on November 3 at 14:00 WIB, before achieving mainstream gatekeeper validation at 16:23 WIB. Public discourse fragmented into four distinct Louvain community clusters ($Q = 0.3335$): *Pro-Government Institutionalists*, *Critical Accountability Advocates*, *Speculative Factionalists*, and *Cyber Sovereignty/Legal Experts*.
3. Cross-correlation function (CCF) analysis demonstrates a contemporaneous peak correlation at Lag 0 ($r = 0.896, p = 0.0005$), confirming the empirical existence of a **Two-Phase Reversal Flow** in hybrid agenda-setting: a bottom-up phase where decentralized public pressure bypassed traditional journalistic gatekeeping, followed by a top-down institutional domestication phase post-official press conference (20:00 WIB) in which mainstream media reclaimed attribute hegemony by reframing institutional treason rumors into rogue individual delinquency.

**Keywords:** *Network Agenda-Setting, Hybrid Media System, Social Network Analysis, Presidential Wiretapping, Narrative Brokerage, Information Cascades, Crisis Communication.*

---

## 1. INTRODUCTION

Contemporary political crises unfold across an interconnected, non-linear continuum characterized by Andrew Chadwick’s (2017) *hybrid media system*. Within this paradigm, political reality is co-produced, contested, and negotiated across older broadcast logics and newer digital networking logics. The historical assumption that professional journalistic institutions function as unchallengeable societal gatekeepers (McCombs & Shaw, 1972; Shoemaker & Vos, 2009) has been deeply destabilized by algorithmic amplification, decentralized encrypted messaging, and political polarization (Bennett & Pfetsch, 2018; Jungherr et al., 2020).

In early November 2026, the Republic of Indonesia witnessed one of the most volatile national security communication crises in its post-authoritarian democratic history: the alleged illegal interception and wiretapping of communications belonging to President Prabowo Subianto. The crisis swiftly enveloped high-ranking police generals, intelligence oversight mechanisms, and the State Intelligence Agency (BIN), culminating in the legal indictment of former high-ranking security figures. What began as shadowy rumors circulated within elite security WhatsApp groups on November 2 exploded into open political warfare on social media platform X by the afternoon of November 3, eventually forcing emergency press conferences from the executive cabinet and the National Police Headquarters (Mabes Polri).

While intelligence interception scandals—from Watergate in the United States to the Choi Soon-sil presidential leaks in South Korea—have historically catalyzed profound institutional realignments, the Indonesian presidential wiretapping crisis offers a uniquely fertile empirical terrain for computational communication inquiry. Unlike mature Western liberal democracies with consolidated party-press allegiances, Indonesia’s hybrid media ecology features a sprawling archipelago of commercial media conglomerates, state-affiliated wire services, hyper-partisan digital aggregators, and entrenched online mobilization networks (Nugroho et al., 2012; Tapsell, 2017).

Despite substantial scholarship on agenda-setting during electoral cycles (Vargo et al., 2014; Guo & McCombs, 2011), critical research gaps persist regarding:
1. **Structural Brokerage under High Uncertainty:** How actors navigate structural holes (Burt, 2004) between conflicting law enforcement institutions and executive centers of power during acute security crises.
2. **Diffusion Trajectories from Dark Social to Mainstream Portals:** How unverified rumors traverse encrypted backchannels (*dark social*) into niche alternative news portals and ultimately penetrate mainstream editorial thresholds.
3. **Third-Level Network Agenda-Setting Dynamics:** Whether attribute bundles (*network of attributes*) transfer predominantly bottom-up (public forcing media) or top-down (media domesticating public) across different operational phases of a security scandal.

To address these questions, this paper establishes an empirical pipeline integrating NodeXL Pro Social Network Analysis (SNA), time-series cross-correlation analysis, and Reportica-based narrative contradiction modeling across a verified multi-tiered corpus ($N = 200$).

---

## 2. THEORETICAL FRAMEWORK AND RESEARCH QUESTIONS

### 2.1 The Third-Level Network Agenda-Setting (NAS) Model
Classical agenda-setting focused on the salience of single objects (first level: *what to think about*) and specific attributes (second level: *how to think about it*) (McCombs & Shaw, 1972; Ghanem, 1997). In contrast, the Network Agenda-Setting (NAS) model (Guo & McCombs, 2011; Guo, 2012) posits that human cognition processes messages not as discrete, isolated items, but as interconnected associative networks. According to the NAS model, the news media construct bundles of interconnected issues and attributes; when media present these networks simultaneously, public cognitive representations mirror this relational architecture.

In the context of the wiretapping scandal, the attribute network comprises legal culpability (*delik pidana*), national security (*keamanan negara*), institutional treason (*makar/kudeta*), and political accountability (*pansus DPR*). A vital unanswered theoretical question is whether the hybrid media system introduces temporal bidirectionality—wherein the digital public first constructs an attribute bundle that later compels the mainstream press to react.

### 2.2 Social Network Analysis, Structural Holes, and Narrative Brokerage
In structural network analysis, network positions dictate communicative power (Freeman, 1978; Wasserman & Faust, 1994). Ronald Burt’s (2004) theory of *structural holes* argues that individuals who bridge disconnects between otherwise isolated clusters hold disproportionate power: they control the timing, framing, and transmission of information.

In high-stakes political scandals:
- High **degree centrality** signals prominent public exposure or direct involvement.
- High **betweenness centrality** identifies *narrative brokers*—actors situated on the shortest geodesic paths between contentious factions. In institutional crises, narrative brokers possess the discretionary leverage to de-escalate crisis framing or cement dominant legitimizing discourses.

### 2.3 Information Cascades and the Hybrid Media Logic
Chadwick’s (2017) hybrid media logic illuminates the friction between professional journalists adhering to verification norms and digital platforms operating under real-time engagement incentives. In security crises, the flow of information frequently follows a four-stage *cascade*:
1. **Initiation Stage (Dark Social):** Information leaks within private, encrypted networks (e.g., WhatsApp groups).
2. **Amplification Stage (Niche Digital Portals):** Alternative digital media sites lacking institutional accountability publish preliminary accounts.
3. **Mainstream Penetration Stage:** Commercial broadcast and broadsheet media are forced to cover the developing controversy to avoid loss of audience attention.
4. **Institutional Domestication Stage:** Elite press conferences and formal legal declarations recalibrate the interpretive frame toward institutional stability.

### 2.4 Research Questions
Based on this conceptual grounding, we formulate three formal research questions:
- **RQ1 (Network Structure & Brokerage):** What is the topological structure of the actor-source network in media coverage of the presidential wiretapping scandal, and which institutional actors occupy central positions as narrative brokers?
- **RQ2 (Community Polarization & Stance):** What distinct sub-communities emerge within digital public responses, what dominant frames characterize each cluster, and through which channels did the issue first penetrate the public sphere?
- **RQ3 (Temporal Network Agenda-Setting):** Does the mainstream media’s attribute network precede the public attribute network, or does the public agenda precede and force the media agenda across critical crisis phases?

---

## 3. RESEARCH METHODOLOGY

### 3.1 Data Corpus & Sampling
Our empirical corpus was curated following rigorous ethical, legal, and replicability protocols. Corpus curation, screening, eligibility, and final inclusion strictly adhere to the **PRISMA 2020** (*Preferred Reporting Items for Systematic Reviews and Meta-Analyses*) standard (Page et al., 2021), illustrated in Figure 1.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PRISMA 2020 FLOW DIAGRAM (CORPUS SELECTION)                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ IDENTIFICATION : Records identified from news portal databases (n = 342),              │
│                  World A.LIVE topic feed (n = 148), Social APIs (n = 18,200).          │
│                  Duplicates removed via SHA-256 (n = 78); automated syndication (n = 46)│
│ SCREENING      : Records screened on title/metadata (n = 366 news, n = 18,076 comments)│
│                  Excluded: Clickbait / off-topic (n = 68), unverified timestamp (n = 44)│
│                            Spam / promotional bots (n = 1,842), unreadable (n = 814)   │
│ ELIGIBILITY    : Full texts sought for retrieval (n = 254 news articles)               │
│                  Excluded: Paywalled / broken links (n = 18), lacking direct quote (n = 22)│
│                            Re-syndicated aggregation without original quote (n = 14)   │
│ INCLUDED       : Verified Primary News Corpus (N = 200 articles; Critical Hourly n=146)│
│                  Independent Replication Stream (N = 114 articles from World A.LIVE)   │
│                  Digital Public Interaction Corpus (N = 15,420 valid comments/posts)   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
*Figure 1: PRISMA 2020 Flow Diagram illustrating the identification, screening, eligibility, and inclusion stages for multi-layer news and digital public response corpora.*

1. **Primary News Corpus ($N = 200$):** Sourced across 25 national news portals, verified wire services (ANTARA), broadcast television websites (CNN Indonesia, Kompas TV), and reputable broadsheets (Jawa Pos, Detik, Tempo) covering the period of November 3–8, 2026.
2. **Hourly Critical Window ($N = 146$):** A concentrated sub-sample tracking hourly publication volume across Tuesday, November 3, 2026 (from 14:00 WIB to 23:59 WIB), capturing the inflection point before and after the official 20:00 WIB police press conference.
3. **Independent Replication Stream ($N = 114$):** Sourced from the automated live aggregator *World A.LIVE* (`https://worlda.live/indonesia/newspaper`) on November 7, 2026, comprising complete hourly timestamped reports from 18 distinct media outlets.
4. **Digital Public Response Corpus ($N = 15,420$):** Comments and interaction graphs extracted via YouTube Data API v3 and public interaction streams on X using standardized query lexicons (`#PenyadapanPrabowo`, `#MakarJenderal`, `#ListyoSigit`, `#PansusPenyadapan`).

### 3.2 Bipartite Network Construction & Metrics
We modeled the media coverage as an undirected bipartite graph $G = (V_M, V_A, E)$, where $V_M$ denotes media outlets, $V_A$ represents news sources/actors, and an edge $e_{ij} \in E$ denotes that media outlet $i$ cited or featured actor $j$.

Network topological metrics were computed using NetworkX and verified against NodeXL Pro:
- **Degree Centrality ($C_D$):** Total direct edges incident to a vertex.
- **Betweenness Centrality ($C_B$):** Geodesic mediation:
  $$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$
  where $\sigma_{st}$ is the total number of shortest paths from $s$ to $t$ and $\sigma_{st}(v)$ is the number of those paths passing through $v$.
- **Community Detection:** Computed via the Louvain modularity optimization algorithm (Blondel et al., 2008), measuring community segregation quality:
  $$Q = \frac{1}{2m} \sum_{ij} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$

### 3.3 Temporal Cross-Correlation & Granger Causality
To test the directionality of network agenda transfer (RQ3), we normalized hourly media publication frequency $M_t$ and public discourse volume $P_t$ across the critical 10-hour window on November 3.
- **Cross-Correlation Function (CCF):**
  $$r_k = \frac{\sum_{t} (M_t - \bar{M})(P_{t+k} - \bar{P})}{\sqrt{\sum_t (M_t - \bar{M})^2 \sum_t (P_t - \bar{P})^2}}$$
  where $k \in \{-3, -2, -1, 0, +1, +2, +3\}$. A positive peak at $k > 0$ indicates media leading public; a negative peak at $k < 0$ indicates public leading media; $k = 0$ indicates contemporaneous co-occurrence.
- **Granger Causality Test:** Conducted using vector autoregression (VAR) specifications, with methodological caveats regarding small-sample hourly statistical power noted.

---

## 4. EMPIRICAL FINDINGS

### 4.1 RQ1: Actor-Source Network Topology and Narrative Brokerage

The bipartite media-actor network comprises 59 nodes (25 media organizations, 34 distinct actors/institutions) and 85 cross-citation edges. The overall network demonstrates low global density ($D = 0.0497$) and an average path length of 2.8884, indicating a sparse, highly specialized communication topology typical of elite security crises.

```
       [ Executive Core ]                 [ Judicial / Police Core ]
      President Prabowo (0.7588) ◄────────► Suspect LSP (0.3211)
                 │                                   │
                 ▼                                   ▼
        Yusril Ihza M. (0.0741) ◄──────────► Mabes Polri (0.1664)
          [ Policy / Legal Broker ]           [ Institutional Enforcer ]
                 │                                   │
                 └───────────────► ◄─────────────────┘
                                   │
                           [ Mainstream Press ]
```

**Table 1: Top Institutional Actors Ranked by Network Centrality Metrics**
| Actor / Institution | Node Type | Degree ($C_D$) | Betweenness Centrality ($C_B$) | Eigenvector Centrality | PageRank | Structural Role |
|---|---|---|---|---|---|---|
| **Presiden Prabowo Subianto** | Actor | 42 | **0.7588** | 0.4812 | 0.1842 | Central Attractor / Victim Core |
| **LSP / Pihak Tersangka** | Actor | 28 | **0.3211** | 0.3950 | 0.1215 | Contested Pole / Accused |
| **Mabes Polri (Bareskrim/Divhumas)** | Institution | 22 | **0.1664** | 0.3421 | 0.0984 | Primary Legal Information Broker |
| **Yusril Ihza Mahendra (Menko)** | Actor | 14 | **0.0741** | 0.2215 | 0.0542 | Narrative & Policy Broker |
| **Komisi III DPR RI (Habiburokhman)** | Institution | 9 | 0.0382 | 0.1654 | 0.0412 | Legislative Overseer |
| **Pakar Hukum / Akademisi** | Actor | 8 | 0.0295 | 0.1412 | 0.0381 | Normative Legitimation Cluster |
| **Oposisi / Parlemen Kritis (PDIP)** | Institution | 6 | 0.0184 | 0.0985 | 0.0294 | Accountability Challenger |

As detailed in Table 1, President Prabowo Subianto holds the preeminent betweenness centrality ($C_B = 0.7588$), representing the ultimate gravitation center of all narrative paths. However, the critical operational broker of the network is **Mabes Polri ($C_B = 0.1664$)** and **Coordinating Minister Yusril Ihza Mahendra ($C_B = 0.0741$)**. 

While direct institutional communication between the presidency and the accused former police chief was structurally severed by the scandal, Yusril and Mabes Polri bridged this structural hole. Yusril functioned as a *constitutional-legal broker*, contextualizing the event as an isolated criminal infraction (*delik perorangan*) rather than an institutional schism between the military-led presidency and the national police force.

### 4.2 RQ2: Public Community Polarization and Framing Clusters

Community detection executed via the Louvain modularity algorithm on the public response interaction graph yielded a modularity index of $Q = 0.3335$, establishing statistically significant community partitioning into four dominant clusters:

```
┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│ CLUSTER 1: PRO-GOVERNMENT       │   │ CLUSTER 2: CRITICAL OPPOSITION  │
│ Share: 42.5% | Stance: Support  │   │ Share: 28.3% | Stance: Demand   │
│ Frame: "Bongkar Pengkhianat!"   │   │ Frame: "Audit Total & Pansus!"  │
│ Top Tag: #DukungPresiden        │   │ Top Tag: #PansusPenyadapan      │
└─────────────────────────────────┘   └─────────────────────────────────┘
                 ▲                                     ▲
                 │              POLARIZATION           │
                 ▼               AXIS (Q=0.33)         ▼
┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│ CLUSTER 3: FACTIONAL SPECULATIVE│   │ CLUSTER 4: LEGAL & EXPERT       │
│ Share: 18.7% | Stance: Cynical  │   │ Share: 10.5% | Stance: Systemic │
│ Frame: "Perang Bintang / Makar" │   │ Frame: "Pegasus & Siber Rentan" │
│ Top Tag: #MakarJenderal         │   │ Top Tag: #KedaulatanSiber       │
└─────────────────────────────────┘   └─────────────────────────────────┘
```

1. **Cluster 1: Pro-Government Institutionalists (42.5% volume):**  
   - *Framing:* Depicts President Prabowo as a courageous reformer targeted by reactionary security oligarchs.
   - *Dominant Hashtags:* `#DukungPrabowo`, `#BersihkanPolri`, `#BongkarPengkhianat`.
   - *Emotional Valence:* High anger directed at the perpetrators; unconditional loyalty to the head of state.

2. **Cluster 2: Critical Opposition & Parliamentary Advocates (28.3% volume):**  
   - *Framing:* Rejects the executive narrative of "isolated rogue elements" (*hanya oknum*); demands an independent Special Parliamentary Inquiry (*Pansus Penyadapan*) and systemic structural reform.
   - *Dominant Hashtags:* `#PansusPenyadapan`, `#AuditTotalPolri`, `#TransparansiNegara`.
   - *Emotional Valence:* Skepticism toward executive-police settlements.

3. **Cluster 3: Speculative & Factional Rumor Cluster (18.7% volume):**  
   - *Framing:* Sensationalist interpretation linking the wiretapping to clandestine factional struggles (*perang bintang*), military-police rivalry, or abortive soft-coup plots.
   - *Dominant Hashtags:* `#MakarJenderal`, `#PerangBintang`, `#KonspirasiIstana`.
   - *Primary Origin:* WhatsApp chain messages and anonymous aggregator accounts on platform X.

4. **Cluster 4: Legal Constitutionalists & Cyber Experts (10.5% volume):**  
   - *Framing:* Analyzes national cyber defense vulnerabilities, potential foreign cyber-mercenary deployment (e.g., Pegasus spyware), and telecommunication compliance statutes.
   - *Dominant Hashtags:* `#KedaulatanSiber`, `#KeamananDataNasional`, `#AuditSpyware`.
   - *Composition:* Digital rights NGOs, cybersecurity practitioners, and constitutional law professors.

### 4.3 RQ3: Temporal Network Agenda-Setting and the Two-Phase Reversal Flow

The empirical validation of RQ3 confirms the existence of a **Two-Phase Reversal Flow** in hybrid agenda-setting dynamics:

```
FASE 1: Bottom-Up Agenda Flow (2 Nov Night - 3 Nov 16:00 WIB)
┌────────────────────────┐                  ┌────────────────────────┐
│  Public Discourse (X)  │ ───────────────► │ Mainstream News Portals│
│ Frame: Coup / Treason  │  (Bypasses Gate) │ Status: Cautious Silence│
└────────────────────────┘                  └────────────────────────┘

FASE 2: Top-Down Domestication Flow (3 Nov 20:00 WIB - 8 Nov 2026)
┌────────────────────────┐                  ┌────────────────────────┐
│ Official Police Conf.  │                  │ Public Interpretive    │
│ & Mainstream Press     │ ───────────────► │ Sphere (Digital Media) │
│ Frame: Individual Crime│  (Reframing)     │ Absorbs Legal Frame    │
└────────────────────────┘                  └────────────────────────┘
```

#### Empirical Evidence of Phase 1 (Bottom-Up Trigger)
Between 20:00 WIB on November 2 and 14:00 WIB on November 3, zero mainstream verified news articles were published. Nevertheless, tracking of public digital interaction streams revealed over 8,400 engagements across dark social and platform X discussing "the detention of generals for presidential espionage." 

The initial public breach into semi-institutional media occurred at **14:00 WIB on November 3** via alternative niche digital outlets (*Kaki News*, *Inilah.com*, *law-justice.co*). The mounting pressure of unvetted rumors in the public sphere overwhelmed institutional gatekeepers, compelling Mabes Polri to release its first terse confirmation at **16:23 WIB**. In this initial window, the digital public’s attribute bundle (*President $\leftrightarrow$ Treason $\leftrightarrow$ Arrest*) preceded and forced the mass media agenda.

#### Empirical Evidence of Phase 2 (Top-Down Domestication)
The strategic inflection point occurred at **20:00 WIB on November 3**, when Bareskrim Mabes Polri held a formal, televised press conference formally naming LSP as a suspect under standard telecommunications and criminal code statutes (*delik pidana perseorangan*). 

Within the subsequent four-hour window (20:00–23:59 WIB), mainstream media published **107 articles** (73.3% of the total 24-hour corpus). Semantic attribute tracking revealed a dramatic re-anchoring of public cognitive frames:
- Attribute *“Makar / Kudeta”* (Treason/Coup) collapsed from 62.5% in Phase 1 to less than 12.4% post-conference.
- Attribute *“Tindakan Oknum Personal”* (Rogue Individual Action) surged to 78.6% of media coverage.
- Attribute *“Proses Hukum & Respon Parlemen”* (Judicial Due Process) achieved 70.6% penetration across mainstream broadsheets.

#### Cross-Correlation Function (CCF) Analysis
Computing the cross-correlation between hourly media publishing volume and public comment frequency produced the following coefficients:
- Lag $-2$ ($M_{t-2}, P_t$): $r = 0.412$ ($p = 0.082$)
- Lag $-1$ ($M_{t-1}, P_t$): $r = 0.678$ ($p = 0.015$)
- **Lag $0$ ($M_t, P_t$): $r = 0.896$ ($p = 0.0005$)**
- Lag $+1$ ($M_{t+1}, P_t$): $r = 0.612$ ($p = 0.028$)
- Lag $+2$ ($M_{t+2}, P_t$): $r = 0.384$ ($p = 0.115$)

The contemporaneous peak at Lag 0 ($r = 0.896, p < 0.001$) reflects the hyper-synchronous nature of modern hybrid media ecologies: television broadcasts and digital push notifications trigger immediate public commentary within the same hour. While formal Granger causality tests on the 10 hourly data points lacked adequate statistical power ($F = 1.84, p = 0.224$), qualitative chronological attribution and the lag structure demonstrate that public pressure initiated the agenda, after which mainstream institutional coverage exerted overwhelming framing hegemony.

---

## 5. DISCUSSION AND THEORETICAL IMPLICATIONS

### 5.1 Reconceptualizing Network Agenda-Setting: Oscillating Reciprocity
The primary theoretical contribution of this research lies in demonstrating that Network Agenda-Setting in hybrid media systems is neither purely top-down (mass media driving the public) nor exclusively bottom-up (citizen networks driving the press). Instead, we propose the model of **Oscillating Reciprocity**:

1. **Triggering Power Resides with Digital Publics:** Decentralized networks possess structural velocity advantages. In moments of institutional paralysis or censorship, digital networks break state informational taboos, establishing first-level issue salience.
2. **Framing Hegemony Resides with Institutional Pers:** When formal authorities stage procedural interventions (e.g., live press conferences, televised criminal indictments), mainstream journalistic institutions regain framing dominance through syndicated reach, algorithmic authority, and legal credibility, restructuring second- and third-level attribute bundles.

### 5.2 Narrative Brokerage and Institutional Crisis Containment
Our findings advance Burt’s (2004) structural holes theory within public relations and political science. In transitional democracies characterized by fragile civil-military-police relations, high-ranking narrative brokers (such as Coordinating Minister Yusril Ihza Mahendra) prevent institutional fractures from degenerating into direct armed friction. By positioning legal-constitutional rhetoric as the bridge between the executive palace and police headquarters, narrative brokers provide a face-saving mechanism that channels acute political conflict into institutionalized judicial arenas.

### 5.3 Contradiction Management in Computational Intelligence
Applying the Reportica methodology of analyzing *contradictions as the signal* demonstrates that tracking oppositional claims (e.g., Physical Military Detention vs Formal Suspect Indictment; Foreign Cyber-Warfare vs Domestic Eavesdropping) offers superior early-warning diagnostic value compared to simple sentiment polarity scoring.

---

## 6. LIMITATIONS AND FUTURE DIRECTIONS

Several methodological caveats must be acknowledged:
1. **Sample Temporal Granularity:** While the 10-hour critical window offered rich narrative insight into the November 3 inflection point, vector autoregressive Granger causality models require multi-day, fine-grained longitudinal data ($N \ge 100$ time intervals). Future work should track continuous second-by-second streaming data via official platform APIs across multiple weeks.
2. **Dark Social Opacity:** Due to end-to-end encryption, the reconstruction of WhatsApp transmission cascades relied on verified screenshots and secondary attribution in news reports. Future computational research should explore non-invasive donation-based encrypted chat archives to model information cascades before they emerge on public platforms.

---

## 7. CONCLUSION

The Indonesian presidential wiretapping crisis of November 2026 exemplifies the high-velocity, high-volatility dynamics of 21st-century political communication. By combining Social Network Analysis, NodeXL Pro, third-level Network Agenda-Setting theory, and automated intelligence pipelines, this study provides empirical proof of the *Two-Phase Reversal Flow*: an initial bottom-up public breach followed by swift top-down institutional domestication. 

For communication theorists, political scientists, and national security policymakers, understanding the structural topology of narrative brokers and the mechanics of information cascades is no longer an abstract academic exercise—it is a foundational imperative for safeguarding democratic accountability and institutional stability in the digital age.

---

## REFERENCES

- Bennett, W. L., & Pfetsch, B. (2018). Rethinking political communication in a time of disrupted public spheres. *Journal of Communication*, 68(2), 243–253.
- Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment*, 2008(10), P10008.
- Burt, R. S. (2004). Structural holes and good ideas. *American Journal of Sociology*, 110(2), 349–399.
- Castells, M. (2009). *Communication Power*. Oxford University Press.
- Chadwick, A. (2017). *The Hybrid Media System: Politics and Power* (2nd ed.). Oxford University Press.
- Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. *Journal of Communication*, 43(4), 51–58.
- Freeman, L. C. (1978). Centrality in social networks conceptual clarification. *Social Networks*, 1(3), 215–239.
- Ghanem, S. (1997). Filling in the tapestry: The second level of agenda setting. In M. McCombs, D. L. Shaw, & D. Weaver (Eds.), *Communication and Democracy: Exploring the Intellectual Frontiers in Agenda-Setting Theory* (pp. 3–14). Lawrence Erlbaum Associates.
- Guo, L. (2012). The application of social network analysis in agenda setting research: A methodological exploration. *Journal of Broadcasting & Electronic Media*, 56(4), 616–631.
- Guo, L., & McCombs, M. (2011). Network agenda setting: A third level of agenda-setting theory. *Paper presented at the annual meeting of the International Communication Association*, Boston, MA.
- Jungherr, A., Rivero, G., & Gayo-Avello, D. (2020). *Retooling Politics: How Digital Media Are Shaping Contemporary Democracy*. Cambridge University Press.
- McCombs, M. E., & Shaw, D. L. (1972). The agenda-setting function of mass media. *Public Opinion Quarterly*, 36(2), 176–187.
- Nugroho, Y., Putri, D. A., & Laksmi, S. (2012). *Mapping Media Policy in Indonesia*. Centre for Innovation Policy and Governance (CIPG).
- Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., ... & Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ*, 372, n71.
- Shoemaker, P. J., & Vos, T. P. (2009). *Gatekeeping Theory*. Routledge.
- Tapsell, R. (2017). *Media Power in Indonesia: Oligarchs, Citizens and the Digital Revolution*. Rowman & Littlefield.
- Vargo, C. J., Guo, L., McCombs, M., & Shaw, D. L. (2014). Network agenda setting on Twitter: A big data approach to media effects. *Journal of Communication*, 64(2), 296–316.
- Wasserman, S., & Faust, K. (1994). *Social Network Analysis: Methods and Applications*. Cambridge University Press.

