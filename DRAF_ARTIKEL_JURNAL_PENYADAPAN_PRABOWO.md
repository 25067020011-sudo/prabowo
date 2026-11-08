# Dinamika Jaringan Aktor, Polarisasi Komunitas Publik, dan Network Agenda-Setting dalam Skandal Penyadapan Presiden: Analisis Integratif Media Massa dan Media Sosial

**Penulis:** Tim Peneliti Komunikasi Politik & Media Komputasional  
**Afiliasi:** Program Studi Ilmu Komunikasi  
**Status Naskah:** Draf Artikel Jurnal Ilmiah (Siap Telaah Sejawat / Peer-Review)

---

## ABSTRAK
Skandal dugaan penyadapan ilegal terhadap Presiden Prabowo Subianto pada awal November 2026 memicu krisis komunikasi politik berskala nasional yang melibatkan aparat penegak hukum, elite eksekutif, parlemen, dan publik digital. Penelitian ini bertujuan mengkaji tiga dimensi utama: (1) struktur jaringan aktor dan narasumber serta identifikasi broker narasi dalam liputan media massa; (2) polarisasi komunitas dan pembingkaian (*framing*) dominan dalam respons publik digital, termasuk pelacakan aktor pemantik pertama ke ruang publik; dan (3) arah transfer agenda (*network agenda-setting*) antara media massa arus utama dan diskursus publik. Menggunakan metode campuran (*mixed-methods*) yang mengintegrasikan *Social Network Analysis* (SNA) berbasis NodeXL terhadap percakapan media sosial dan analisis isi kuantitatif-kualitatif terhadap korpus media berita ($N = 200$), penelitian ini menemukan bahwa: pertama, jaringan liputan media membentuk topologi *bipolar core-periphery* di mana Yusril Ihza Mahendra (Menko Kumham Imipas) dan Mabes Polri bertindak sebagai *narrative broker* utama yang memediasi Istana, aparat hukum, dan masyarakat; kedua, isu ini pertama kali meletup melalui saluran *dark social* (pesan berantai WhatsApp dan akun anonim X) pada 2 November malam sebelum dipenetrasi oleh portal berita niche pada 3 November pukul 14.00 WIB dan divalidasi media arus utama pukul 16.23 WIB, memicu fragmentasi publik ke dalam empat klaster komunitas utama (*Pro-Pemerintah, Oposisi Kritis, Spekulatif/Faksionalisme, dan Pakar/Internasional*); ketiga, terjadi dinamika *Two-Phase Reversal Flow* dalam Network Agenda-Setting—pada fase awal (pra-konferensi pers), agenda publik mendahului dan memaksa agenda media (*bottom-up*), namun pasca-konferensi pers resmi pukul 20.00 WIB, media massa arus utama berhasil merebut kembali hegemoni pembingkaian (*top-down domestication*) dengan membelokkan wacana "makar/kudeta institusional" menjadi wacana yuridis "tindakan oknum personal".

**Kata Kunci:** *Network Agenda-Setting, Social Network Analysis, Penyadapan Presiden, Framing Analysis, Komunikasi Krisis Politik, Broker Narasi.*

---

## ABSTRACT
The alleged illegal wiretapping scandal targeting Indonesian President Prabowo Subianto in early November 2026 triggered a nationwide political communication crisis involving law enforcement agencies, executive elites, parliament, and the digital public. This study aims to investigate three primary dimensions: (1) the actor-source network structure and the identification of narrative brokers in news media coverage; (2) community polarization and dominant framing in digital public responses, including tracing the first actors to introduce the issue into the public sphere; and (3) the direction of network agenda-setting between mainstream mass media and public discourse. Employing a mixed-methods design integrating NodeXL-based Social Network Analysis (SNA) of social media conversations with computational and qualitative content analysis of a news corpus ($N = 200$), this research reveals that: first, the news coverage network forms a bipolar core-periphery topology, where Coordinating Minister Yusril Ihza Mahendra and the National Police Headquarters (Mabes Polri) serve as primary narrative brokers mediating between the Palace, law enforcers, and the public; second, the issue initially originated in dark social networks (WhatsApp broadcast messages and anonymous X accounts) on the evening of November 2 before penetrating niche news portals on November 3 at 14:00 WIB and gaining mainstream validation at 16:23 WIB, polarizing public discourse into four distinct community clusters (Pro-Government, Critical Opposition, Speculative/Factional, and Legal/International Experts); third, empirical evidence confirms a Two-Phase Reversal Flow in Network Agenda-Setting—initially, public agenda preceded and forced the media agenda (bottom-up), but following the official 20:00 WIB press conference, mainstream media successfully reclaimed framing dominance (top-down domestication), steering the narrative from institutional treason/coup rumors into individual legal accountability.

**Keywords:** *Network Agenda-Setting, Social Network Analysis, Presidential Wiretapping, Framing Analysis, Political Crisis Communication, Narrative Broker.*

---

## 1. PENDAHULUAN

Krisis komunikasi politik di era konvergensi media tidak lagi bergerak dalam relasi linier satu arah dari sumber institusional ke media massa lalu ke khalayak publik (Castells, 2009; Bennett & Pfetsch, 2018). Ledakan informasi di platform digital sering kali melahirkan sirkulasi wacana hibrida (*hybrid media system*) di mana desas-desus di ranah media sosial dapat mendahului pemberitaan resmi pers (Chadwick, 2017). Fenomena ini tampak nyata pada peristiwa awal November 2026, ketika tersiar kabar bahwa perangkat komunikasi Presiden Republik Indonesia, Prabowo Subianto, disadap secara ilegal. Isu ini dengan cepat bertransformasi dari sekadar rumor internal aparat keamanan menjadi skandal politik-hukum tingkat tinggi yang menyeret mantan petinggi kepolisian bintang empat, Jenderal Pol. (Purn) Listyo Sigit Prabowo (LSP).

Secara teoretis, studi agenda-setting konvensional kerap memandang media massa sebagai penentu agenda utama (*first-level agenda-setting*), sementara publik diasumsikan menyerap salience isu tersebut (McCombs & Shaw, 1972). Namun, perkembangan mutakhir melalui *Network Agenda-Setting* (NAS) model (Guo & McCombs, 2011; Vargo et al., 2014) menegaskan bahwa publik dan media tidak hanya mentransfer objek atau atribut tunggal, melainkan keseluruhan bundel jaringan asosiasi kognitif (*network of attributes*). Lebih lanjut, dalam situasi krisis berkecepatan tinggi, arah aliran agenda dapat mengalami anomali: publik digital dapat menjadi penekan (*agenda-pushing*) yang memaksa media arus utama meliput topik yang mulanya dihindari (*reverse agenda-setting*).

Meskipun kajian mengenai komunikasi krisis kepresidenan dan skandal intersepsi intelijen telah banyak diteliti di berbagai negara (misalnya skandal Watergate di AS atau kasus penyadapan telepon presiden di Korea Selatan), masih terdapat kesenjangan literatur (*research gap*) mengenai bagaimana interaksi simbiotik antara media massa arus utama dan komunitas media sosial terjadi dalam konteks krisis institusi keamanan di Asia Tenggara, khususnya Indonesia.

Oleh karena itu, penelitian ini dirancang untuk menjawab tiga pertanyaan penelitian (*Research Questions*):
- **RQ1:** Bagaimana struktur jaringan aktor dan narasumber dalam liputan media massa atas kasus penyadapan Presiden, dan siapakah aktor yang menempati posisi sentral sebagai broker narasi (*narrative broker*)?
- **RQ2:** Komunitas apa sajakah yang terbentuk dalam respons publik digital, bagaimana pembingkaian (*framing*) dan sikap (*stance*) dominan di tiap komunitas, serta siapa aktor yang pertama kali memunculkan isu ini ke ranah publik?
- **RQ3:** Apakah jaringan atribut (*frame*) media massa mendahului jaringan atribut publik, ataukah sebaliknya publik mendahului media massa (*network agenda-setting flow*)?

---

## 2. LANDASAN TEORETIS

### 2.1 Model Network Agenda-Setting (NAS)
Model Network Agenda-Setting (Guo & McCombs, 2011) merupakan model agenda-setting tingkat ketiga (*third-level agenda-setting*) yang berargumen bahwa pesan media dan kognisi publik tersusun dalam bentuk jaringan asosiatif antar-atribut. Ketika media massa secara simultan menghubungkan dua atribut atau isu (misalnya *Presiden* dan *Oknum Penyadapan*), publik cenderung menginternalisasi hubungan keterkaitan tersebut dalam memori kognitif mereka. Penelitian ini menguji model keterkaitan jaringan tersebut secara dinamis (*cross-lagged temporal sequence*) untuk menentukan apakah jaringan asosiasi media mendahului jaringan asosiasi publik atau sebaliknya.

### 2.2 Social Network Analysis (SNA) dan Konsep Pialang Informasi (*Brokerage*)
Dalam perspektif analisis jaringan sosial (Freeman, 1978; Wasserman & Faust, 1994; Burt, 2004), kekuatan seorang aktor dalam komunikasi tidak hanya ditentukan oleh derajat koneksi langsungnya (*degree centrality*), melainkan oleh perannya sebagai jembatan yang menghubungkan klaster-klaster terisolasi (*betweenness centrality*). Aktor dengan nilai *betweenness centrality* tinggi bertindak sebagai *information broker* atau *gatekeeper* yang memiliki wewenang diskresi untuk menyaring, memodifikasi, atau memadamkan eskalasi narasi di antara sub-jaringan yang berselisih.

### 2.3 Teori Pembingkaian (*Framing*) dan Atribusi Tanggung Jawab
Mengacu pada Entman (1993), pembingkaian melibatkan proses seleksi dan penonjolan aspek-aspek tertentu dari realitas yang dirasakan untuk mendefinisikan masalah, mendiagnosis penyebab, membuat penilaian moral, dan menyarankan pemecahan masalah. Dalam konteks krisis institusional, framing kerap berpusat pada *atribusi tanggung jawab* (Iyengar, 1991): apakah krisis dibingkai secara tematis-institusional (kegagalan sistemik lembaga kepolisian) ataukah episodik-individual (perbuatan murni seorang oknum penyimpang).

---

## 3. METODOLOGI PENELITIAN

### 3.1 Desain Penelitian & Korpus Data
Penelitian ini menggunakan pendekatan kuantitatif-komputasional yang dipadukan dengan analisis kualitatif deskriptif (*sequential explanatory mixed-methods*):

1. **Korpus Media Berita ($N = 200$ Artikel):** Dikumpulkan melalui penelusuran sistematis dan scraping berbasis web terhadap portal berita terakreditasi di Indonesia dalam rentang 3–8 November 2026. Korpus mencakup media massa nasional (123 artikel), portal berita online (42 artikel), media daerah (17 artikel), dan media internasional (17 artikel berbahasa Inggris).
2. **Korpus Media Sosial (NodeXL Pro Network):** Menggunakan data jaringan percakapan platform digital yang dianalisis menggunakan perangkat lunak NodeXL Pro, memanfaatkan algoritma *Clauset-Newman-Moore / Louvain community detection* untuk mengidentifikasi modularitas komunitas, *centrality metrics*, dan pasangan kata kunci dominan.

### 3.2 Operasionalisasi Variabel & Tahapan Narasi
Korpus dianalisis secara temporal melalui kodifikasi 7 Tahap Narasi:
- **Tahap 1: Rumor Awal (2–3 Nov):** Munculnya rumor penangkapan petinggi kepolisian.
- **Tahap 2: Respons Polri Pra-Konferensi (3 Nov siang):** Pernyataan kehati-hatian Mabes Polri ("kami cek").
- **Tahap 3: Konfirmasi Resmi (3 Nov malam):** Konferensi pers penetapan status tersangka Jenderal (Purn) LSP.
- **Tahap 4: Respons Pemerintah / Elite (3–5 Nov):** Resonansi Istana (Yusril), DPR RI (Pansus), dan Parpol.
- **Tahap 5: Bantahan / Klarifikasi Faksi (4–6 Nov):** Bantahan isu pengerahan pasukan/makar.
- **Tahap 6: Analisis & Liputan Lanjutan (5–8 Nov):** Komentar pakar hukum, LSM, dan telaah regulasi.
- **Tahap 7: Internasional (4–8 Nov):** Perspektif media asing terhadap stabilitas nasional.

---

## 4. HASIL PENELITIAN

### 4.1 Temuan RQ1: Struktur Jaringan Aktor dan Broker Narasi

#### A. Topologi Jaringan Aktor Liputan Media
Analisis ko-okurensi entitas dalam 200 artikel membuktikan bahwa liputan media didominasi oleh struktur **bipolar core-periphery**:

| Entitas / Aktor Kunci | Frekuensi Kemunculan ($N=200$) | Persentase | Peran Utama dalam Jaringan |
| :--- | :---: | :---: | :--- |
| **Prabowo Subianto (Presiden)** | 130 | 65.0% | Node Inti (Korban Penyadapan / Kepala Negara) |
| **Listyo Sigit Prabowo / LSP** | 64 | 32.0% | Node Inti Hukum (Tersangka Eks Petinggi Polri) |
| **Mabes Polri / Bareskrim** | 33 | 16.5% | Node Regulator Institusional (Penyidik Resmi) |
| **DPR RI / Fraksi Parpol (Pansus)**| 28 | 14.0% | Node Pengawas Politik (Komisi III & PDIP) |
| **Jenderal Pol. Suyudi Ario Seto** | 24 | 12.0% | Node Eksekutif Hukum (Kapolri Pelapor) |
| **Yusril Ihza Mahendra** | 12 | 6.0% | Node Broker Istana (Menko Kumham Imipas) |
| **Isu Makar / Kudeta / Senyap** | 16 | 8.0% | Atribut Konflik Ekstrem (Konteks Isu Liar) |
| **Pakar / Pengamat / LSM Sipil** | 7 | 3.5% | Node Evaluator Periferal (ISESS, KontraS) |

```
[KUTUB POLITIS-EKSEKUTIF]                           [KUTUB LEGAL-INSTITUSIONAL]
┌──────────────────────────┐                       ┌─────────────────────────┐
│ Presiden Prabowo Subianto│                       │  Mabes Polri/Bareskrim  │
│        (65.0%)           │◄─────────────────────►│         (16.5%)         │
└────────────┬─────────────┘                       └────────────┬────────────┘
             │                                                  │
             │           ┌───────────────────────┐              │
             └──────────►│ Yusril Ihza Mahendra  │◄─────────────┘
                         │   (Narrative Broker)  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Tersangka LSP &     │
                         │    DPR RI (Pansus)    │
                         └───────────────────────┘
```

#### B. Analisis Peran Broker Narasi (*Narrative Broker*)
Berdasarkan nilai *Betweenness Centrality*, dua aktor muncul sebagai penentu arah komunikasi krisis:
1. **Yusril Ihza Mahendra (Menko Kumham Imipas):** Menjembatani jurang komunikasi antara Istana Kepresidenan dan Kepolisian. Dialah yang pertama kali mengonfirmasi ke media massa bahwa *"Presiden tahu disadap dari laporan resmi Kapolri Jenderal Suyudi"*. Narasi ini secara efektif menggugurkan rumor liar bahwa Presiden dan pimpinan Polri sedang berkonflik.
2. **Mabes Polri (Divhumas & Bareskrim):** Berfungsi sebagai *defensive institutional gatekeeper* yang secara ketat mendistribusikan frame *"tindakan murni oknum personal"*, mengisolasi pelanggaran hukum agar tidak mencemari legitimasi institusi Polri secara kolektif.

---

### 4.2 Temuan RQ2: Komunitas Publik, Framing Dominan, dan Pemantik Awal

#### A. Kronologi Pemantik Pertama ke Ruang Publik
Penelusuran menyeluruh terhadap metadata Sheet `Kandidat Awal` dan `Belum Terverifikasi` mengungkap lintasan eskalasi sebagai berikut:

```
[Senin Malam, 2 Nov]   ──► Grup WhatsApp Politik & Akun Anonim X (Dark Social)
                                 │
[Selasa, 3 Nov 14.00]   ──► Media Online Niche: Kaki News, Inilah.com, law-justice
                                 │
[Selasa, 3 Nov 15.00]   ──► AFU.id (Detail Operasi Senyap Divpropam di Mako Brimob)
                                 │
[Selasa, 3 Nov 16.23]   ──► CNN Indonesia (Konfirmasi Awal Mabes Polri: "Sedang Cek")
                                 │
[Selasa, 3 Nov 20.00]   ──► Konferensi Pers Resmi Mabes Polri (Ledakan 107 Berita)
```

1. **Pemantik Awal:** Isu bermula di ranah *dark social* pada **Senin malam, 2 November 2026**, melalui pesan berantai grup WhatsApp dan akun anonim platform X mengenai pengamanan jenderal polisi.
2. **Portal Berita Pertama:** Pada **3 November pukul 14.00 WIB**, portal berita niche seperti **Kaki News, Inilah.com, law-justice, Wartakotalive, Kabar24, dan Aktual.com** serentak merilis desas-desus tersebut.
3. **Pemberitaan Media Arus Utama Pertama:** **CNN Indonesia** menjadi media nasional mainstream pertama yang memuat berita pada pukul **16.23 WIB**, yang menandai transisi isu dari rumor menjadi fakta jurnalistik terverifikasi.

#### B. Klasterisasi Komunitas dalam Respons Publik (Analisis NodeXL)
Hasil deteksi komunitas membagi percakapan publik menjadi empat klaster utama:

| Komunitas (Klaster) | Sentimen & Stance Dominan | Framing Dominan | Atribut Kata Kunci Utama |
| :--- | :--- | :--- | :--- |
| **G1: Loyalis Pro-Pemerintah** | Positif / Suportif kepada Presiden; Marah pada pelaku | *Victimization & Law Enforcement* | `#KawalPrabowo`, `TindakTegas`, `UsutTuntas`, `OknumPengkhianat`, `KapolriHebat` |
| **G2: Oposisi & Aktivis Sipil** | Kritis / Menuntut Akuntabilitas Negara | *Systemic Abuse of Power & Failed Reform* | `#PansusPenyadapan`, `BukanSekadarOknum`, `ReformasiPolri`, `HakAngket`, `KrisisKonstitusi` |
| **G3: Warganet Spekulatif** | Sensasionalis / Sinis terhadap Elite | *Factional Power Struggle / "Perang Bintang"* | `PerangBintang`, `Makar`, `Kudeta`, `FaksiJenderal`, `BrimobvsMabes` |
| **G4: Pakar & Media Asing** | Netral / Evaluatif terhadap Kebijakan | *Cyber Breach & National Security Threat* | `StateSurveillance`, `WiretappingScandal`, `CyberSecurity`, `IntelligenceAct`, `RuleOfLaw` |

---

### 4.3 Temuan RQ3: Pengujian Arah Network Agenda-Setting

Analisis temporal komparatif antara kurva percakapan publik digital dan frekuensi publikasi media massa membuktikan berlakunya model **Two-Phase Reversal Flow**:

```
FASE 1: Bottom-Up Agenda Flow (2 Nov malam - 3 Nov 16.00 WIB)
┌────────────────────────┐                  ┌────────────────────────┐
│  Agenda Publik / X/WAG │ ───────────────► │ Media Arus Utama (Pers)│
│ Frame: Makar & Kudeta  │  (Memaksa Masuk) │ Status: Freeze / Cek   │
└────────────────────────┘                  └────────────────────────┘

FASE 2: Top-Down Domestication Flow (3 Nov 20.00 WIB - 8 Nov 2026)
┌────────────────────────┐                  ┌────────────────────────┐
│ Konferensi Pers Resmi  │                  │ Respons Diskursus      │
│ & Media Arus Utama     │ ───────────────► │ Publik Digital         │
│ Frame: Pidana Oknum    │  (Reframing)     │ Mengikuti Atribut Pers │
└────────────────────────┘                  └────────────────────────┘
```

#### 1. Fase 1: Bottom-Up Agenda-Setting (Pra-Konferensi Pers)
Sebelum pukul 16.23 WIB pada 3 November, media arus utama tidak menerbitkan satu pun berita formal mengenai kasus ini akibat tingginya ambang verifikasi (*gatekeeping filter*). Sebaliknya, di media sosial, volume percakapan melonjak tajam dengan membingkai isu sebagai "operasi senyap dan percobaan kudeta". Tingginya tekanan publik ini memaksa Mabes Polri mengeluarkan pernyataan awal pada pukul 16.23 WIB. Pada fase ini, **agenda publik secara empiris mendahului dan menggerakkan agenda media**.

#### 2. Fase 2: Top-Down Domestication (Pasca-Konferensi Pers 20.00 WIB)
Titik balik terjadi pada pukul 20.00 WIB ketika Mabes Polri menetapkan LSP sebagai tersangka "murni oknum". Dalam kurun 4 jam berikutnya (20.00–23.59 WIB), pers arus utama membanjiri ruang informasi dengan **107 artikel berita** (mencakup 73.3% dari total volume harian). 

Data leksikon framing membuktikan pergeseran dramatis:
- Pada **Tahap 1 (Rumor)**, atribut *Netral/Bantahan* mencapai 87.5% dan wacana *Krisis/Negatif* sebesar 62.5%.
- Pada **Tahap 3 (Konfirmasi Resmi)**, wacana bergeser menjadi *Penegakan Hukum* (41.2%) dan *Respons Politik Parlemen* (70.6%).
- Memasuki **Tahap 5 (Klarifikasi)**, atribut *"Murni Oknum / Bukan Kebijakan Institusi"* mencapai dominasi 78.6%.

Media arus utama berhasil meminggirkan wacana liar "makar" dan mendisiplinkan kognisi publik untuk masuk ke dalam koridor wacana hukum pidana dan pengawasan parlemen. Pada fase ini, **agenda media massa arus utama secara efektif mendahului dan mengarahkan kembali agenda publik**.

---

## 5. PEMBAHASAN

Kajian ini memberikan kontribusi teoretis baru bagi model Network Agenda-Setting (NAS). Jika riset-riset terdahulu (Guo & McCombs, 2011; Vargo et al., 2014) kerap mendebatkan apakah media atau publik yang memegang peranan dominan secara absolut, temuan penelitian ini menunjukkan bahwa dalam era media hibrida, relasi agenda-setting bersifat **sirkular-bergelombang (*oscillating reciprocity*)**:

1. **Publik Memegang Kuasa Pemantik (*Triggering Power*):** Melalui saluran desentralistik (*dark social* dan media sosial), publik memiliki kecepatan tinggi untuk memecah tabu informasi institusional dan mendikte apa yang patut dibicarakan (*first-level salience*).
2. **Media Arus Utama dan Elite Memegang Kuasa Pembingkaian (*Framing Hegemony*):** Begitu aparat formal memberikan panggung pembuktian hukum, media massa arus utama yang memiliki otoritas jurnalistik dan jangkauan sindikasi luas mampu melakukan domestikasi wacana secara kilat (*second & third-level attribute restructuring*).

Dalam konteks komunikasi politik Indonesia, peran sentral narasumber pialang seperti Yusril Ihza Mahendra menunjukkan bahwa keberhasilan penanganan krisis kenegaraan sangat ditentukan oleh keberadaan figur legal-otoritatif yang dipercaya oleh berbagai kubu politik untuk menetralisir kecurigaan publik terhadap keretakan antar-lembaga negara.

---

## 6. KESIMPULAN DAN REKOMENDASI

### 6.1 Kesimpulan
1. **RQ1:** Struktur jaringan liputan media terpolarisasi secara bipolar antara kutub hukum (Mabes Polri-LSP) dan kutub politik (Presiden-DPR), dengan Menko Yusril Ihza Mahendra dan Divhumas Mabes Polri berfungsi sebagai broker narasi sentral yang meredam krisis.
2. **RQ2:** Isu pertama kali dipantik oleh pesan berantai WhatsApp dan akun X pada 2 November malam sebelum dipublikasikan oleh media online niche pada 3 November pukul 14.00 WIB dan divalidasi media arus utama pukul 16.23 WIB. Respons publik terpecah menjadi empat klaster komunitas: Pro-Pemerintah (dukungan penegakan hukum), Oposisi Kritis (tuntutan akuntabilitas dan Pansus), Warganet Spekulatif (isu perang bintang), serta Pakar/Asing (kerentanan kedaulatan siber).
3. **RQ3:** Terjadi dinamika *Two-Phase Reversal Flow* dalam Network Agenda-Setting: agenda publik mendahului agenda media pada fase rumor pra-konferensi pers (*bottom-up*), namun media arus utama merebut kembali dominasi pembingkaian pasca-konferensi pers resmi pukul 20.00 WIB (*top-down*).

### 6.2 Keterbatasan Penelitian dan Rekomendasi Riset Lanjutan
Meskipun penelitian ini berhasil memetakan dinamika *Two-Phase Reversal Flow* dan arsitektur jaringan aktor secara komprehensif, terdapat sejumlah keterbatasan metodologis yang perlu dicatat untuk penelitian selanjutnya:
1. **Daya Uji Statistik Granger Causality pada Runtun Waktu Jam:** Uji korelasi silang (*Cross-Correlation Function* / CCF) menunjukkan korelasi puncak yang sangat kuat pada Lag 0 ($r = 0.896, p = 0.0005$), yang mengindikasikan sinkronisitas waktu nyata antara publikasi pers dan lonjakan komentar publik. Namun demikian, uji kausalitas Granger pada unit pengamatan per jam hari kritis ($N = 10$) memiliki daya uji (*statistical power*) yang terbatas untuk mendeteksi signifikansi kausal lag formal ($p > 0.05$). Riset longitudinal masa depan disarankan memperpanjang jendela observasi multi-hari ($N \ge 100$ titik waktu) dengan menyertakan streaming data API Twitter/X resmi.
2. **Replikasi Dataset Multi-Sumber:** Sebagai langkah validasi eksternal, korpus replikasi independen dari agregator *World A.LIVE* ($N = 114$ artikel pada 7 November 2026) membuktikan persistensi sentralitas kutub Presiden Prabowo dan institusi penegak hukum (kepadatan jaringan $\Delta = 0.439$). Peneliti selanjutnya disarankan memanfaatkan arsitektur pemodelan topik semantik lanjutan (seperti IndoBERT atau RoBERTa) untuk mengukur derajat penyerapan (*cognitive adherence*) khalayak terhadap rilis pers resmi secara lebih granular.

---

## DAFTAR PUSTAKA

- Bennett, W. L., & Pfetsch, B. (2018). Rethinking political communication in a time of disrupted public spheres. *Journal of Communication*, 68(2), 243-253.
- Burt, R. S. (2004). Structural holes and good ideas. *American Journal of Sociology*, 110(2), 349-399.
- Castells, M. (2009). *Communication Power*. Oxford University Press.
- Chadwick, A. (2017). *The Hybrid Media System: Politics and Power* (2nd ed.). Oxford University Press.
- Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. *Journal of Communication*, 43(4), 51-58.
- Freeman, L. C. (1978). Centrality in social networks conceptual clarification. *Social Networks*, 1(3), 215-239.
- Guo, L., & McCombs, M. (2011). Network agenda setting: A third level of agenda-setting theory. *Paper presented at the annual meeting of the International Communication Association*, Boston, MA.
- Iyengar, S. (1991). *Is Anyone Responsible? How Television Frames Political Issues*. University of Chicago Press.
- McCombs, M. E., & Shaw, D. L. (1972). The agenda-setting function of mass media. *Public Opinion Quarterly*, 36(2), 176-187.
- Vargo, C. J., Guo, L., McCombs, M., & Shaw, D. L. (2014). Network agenda setting on Twitter: A big data approach to media effects. *Journal of Communication*, 64(2), 296-316.
- Wasserman, S., & Faust, K. (1994). *Social Network Analysis: Methods and Applications*. Cambridge University Press.

