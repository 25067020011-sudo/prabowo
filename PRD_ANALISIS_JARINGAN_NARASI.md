# PRD: Analisis Jaringan Narasi Kasus Penyadapan Presiden
**Draf v0.1, 8 November 2026**  
*Dokumen kerja untuk penelitian SNA (Social Network Analysis) dengan target publikasi jurnal Scopus Q1.*  
*Angka target dan jadwal adalah usulan dan perlu disesuaikan.*

---

## 1. Ringkasan
Proyek ini membangun korpus dan pipeline analisis untuk memetakan bagaimana kasus dugaan penyadapan ilegal terhadap Presiden Prabowo Subianto diberitakan dan direspons publik sejak 3 November 2026. Fokusnya ada pada struktur jaringan aktor dan narasumber di media, komunitas dan frame di respons publik, serta hubungan waktu antara keduanya.

Proyek ini tidak menilai benar atau salahnya perkara hukum. Seluruh klaim tentang kasus mengikuti pemberitaan dan harus diberi atribusi sumber. Status hukumnya masih berjalan.

---

## 2. Tujuan dan Non-Tujuan

### Tujuan
- Menghasilkan dataset yang sah, terdokumentasi, dan bisa direplikasi.
- Menjawab tiga pertanyaan riset berbasis teori (bagian 3).

### Non-tujuan
- Membuktikan siapa pelaku atau pengunggah pertama informasi.
- Melabeli akun sebagai buzzer atau bot tanpa bukti kuat.
- Membagikan ulang teks artikel utuh atau data pribadi akun.

---

## 3. Pertanyaan Riset (Research Questions)
- **RQ1:** Bagaimana struktur jaringan aktor dan narasumber dalam liputan media, dan siapa yang berperan sebagai broker narasi?
- **RQ2:** Komunitas apa yang terbentuk dalam respons publik, dan frame atau stance apa yang dominan di tiap komunitas?
- **RQ3:** Apakah frame media mendahului frame publik, atau sebaliknya (*network agenda-setting*)?

*Kerangka teori yang diusulkan:* Network Agenda-Setting, Framing, dan Sistem Media Hibrida. Hipotesis dirumuskan setelah studi pustaka dan sebelum analisis (disarankan pra-registrasi di OSF).

---

## 4. Ruang Lingkup

### Dalam Lingkup
- **Jendela waktu:** 3 sampai sekitar 17 November 2026 (dapat diperpanjang).
- **Lapisan utama:** portal berita (*JawaPos, Antara, JPNN, Viva, detikcom, CNN Indonesia, Tirto, Liputan6, Okezone*, dan lain-lain).
- **Lapisan respons publik:** komentar YouTube lewat API resmi.
- **Korpus tiga lapis:**
  1. Berita langsung soal penyadapan.
  2. Berita terkait (penetapan tersangka, reaksi DPR dan partai, evaluasi pemerintah).
  3. Respons publik.

### Opsional atau Terbatas
- **X (Twitter):** hanya jika tersedia anggaran dan akses API yang sah.
- **Threads dan TikTok:** sampel kualitatif untuk ilustrasi, tidak masuk jaringan utama.

### Di Luar Lingkup
- Isi atau rekaman hasil penyadapan, dan data pribadi non-publik.
- Prediksi hasil proses hukum.

---

## 5. Pemangku Kepentingan
- Peneliti utama (pemilik proyek).
- Pembimbing dan ko-penulis.
- Komite etik kampus dan bagian hukum.
- Reviewer dan editor jurnal (pengguna akhir standar metodologi).

---

## 6. Kebutuhan Fungsional

| ID | Kebutuhan | Prioritas | Status Proyek Saat Ini |
| :--- | :--- | :---: | :--- |
| **FR-1** | Menyusun seed set (~100 URL terverifikasi) dan daftar kata kunci (*sadap, penyadapan, disadap, intersep*, nama aktor). | **Tinggi** | **Selesai** (200 data terverifikasi di [data.xlsx](file:///Users/jevin/Downloads/prabowo/prabowo/data.xlsx)). |
| **FR-2** | Scraper berita per portal: judul, tanggal terbit, sumber, URL, deskripsi singkat (maks. 300 char), hyperlink keluar. Patuhi robots.txt dan jeda request. | **Tinggi** | **Selesai** ([scrape_penyadapan.py](file:///Users/jevin/Downloads/prabowo/prabowo/scrape_penyadapan.py)). |
| **FR-3** | Arsip pengambilan: waktu pengambilan, hash isi (SHA-256), dan salinan di arsip web bila memungkinkan. | **Tinggi** | *Sedang diintegrasikan*. |
| **FR-4** | Deteksi duplikat dan berita kantor berita yang dimuat ulang (*near-duplicate* / sindikasi). | **Tinggi** | *Sedang diintegrasikan*. |
| **FR-5** | Ekstraksi kutipan dan narasumber (pola *kata X, ujar X, menurut X*), kategori khusus sumber anonim. | **Tinggi** | *Modul `extract_quotes.py`*. |
| **FR-6** | Pengambilan komentar YouTube lewat API resmi, dengan ID pengguna di-hash (SHA-256). | **Sedang** | *Modul `youtube_harvester.py`*. |
| **FR-7** | Coding manual stance dan frame pada sampel oleh dua koder, perhitungan *Krippendorff's alpha* $\ge 0.7$. | **Tinggi** | *Buku Kode [CODEBOOK_STANCE_FRAME.md](file:///Users/jevin/Downloads/prabowo/prabowo/CODEBOOK_STANCE_FRAME.md)*. |
| **FR-8** | Klasifikasi otomatis stance dan frame (IndoBERT) yang divalidasi pada sampel koding manual. | **Sedang** | *Skrip klasifikasi baseline*. |
| **FR-9** | Pembangunan jaringan: media dan narasumber (bipartit), serta jaringan respons publik (reply, mention, ko-sitasi). | **Tinggi** | *Modul `build_network.py`*. |
| **FR-10**| Analisis temporal untuk RQ3 (time series, uji Granger causality atau setara). | **Sedang** | *Modul `temporal_analysis.py`*. |
| **FR-11**| Repositori kode dan data (ID dan metadata saja) di OSF atau GitHub. | **Tinggi** | **Selesai** ([github.com/25067020011-sudo/prabowo](https://github.com/25067020011-sudo/prabowo)). |

---

## 7. Skema Data (Data Schema)

- **`articles`:** `article_id`, `url`, `source`, `title`, `published_at`, `retrieved_at`, `content_hash`, `description` (maks. 300 karakter), `is_duplicate_of`, `wire_origin`.
- **`quotes`:** `quote_id`, `article_id`, `speaker`, `speaker_type` (*pejabat, aparat, politisi, pakar, anonim, lainnya*), `quote_snippet` (pendek), `extraction_confidence`, `manually_verified`.
- **`edges_media_source`:** `source_media`, `speaker`, `weight`, `first_seen_at`.
- **`comments`:** `comment_id`, `platform`, `parent_id`, `video_or_post_id`, `user_hash`, `published_at`, `text_snippet`, `stance`, `frame`, `coded_by`.
- **`codebook`:** definisi 4 sampai 6 kategori stance dan frame, aturan koding, contoh, dan hasil uji reliabilitas.

---

## 8. Metode Analisis
- **Jaringan:** Centrality (*betweenness, eigenvector*), deteksi komunitas (*Louvain* atau *Leiden*), modularity, dan ukuran polarisasi. Untuk jaringan bipartit gunakan ukuran bipartit sebelum proyeksi ke satu mode.
- **Teks:** Stance dan frame dengan koding manual terlebih dahulu, lalu klasifikasi otomatis yang divalidasi. *Topic modelling* (misalnya BERTopic) sebagai pelengkap.
- **Kekokohan:** Bandingkan beberapa algoritma komunitas, gunakan model null jaringan, dan lakukan analisis sensitivitas terhadap kata kunci serta jendela waktu.
- **Pembanding:** Tambahkan pembanding (platform lain atau kasus skandal politik lain) atau hipotesis yang diuji agar tidak berhenti pada studi kasus tunggal.

---

## 9. Kebutuhan Non-Fungsional
- **Hukum:** Pasal 44 UU Hak Cipta memberi ruang untuk penelitian dan karya ilmiah dengan pencantuman sumber dan tanpa merugikan kepentingan wajar pencipta. Simpan metadata dan kutipan pendek, cantumkan sumber, dan konsultasikan dengan bagian hukum kampus.
- **Etika:** *Ethical clearance* sebelum menyimpan data akun. Hash ID pengguna, kecuali akun pejabat atau institusi. Simpan data di penyimpanan aman.
- **Reproduktifitas:** Dokumentasikan versi skrip, tanggal dan metode pengambilan, serta parameter analisis. Bagikan ID dan kode, bukan teks mentah.
- **Netralitas:** Bahasa laporan netral dan berbasis atribusi. Hindari klaim tentang benar atau salahnya perkara.

---

## 10. Metrik Keberhasilan (Usulan)
- Korpus minimal 300 artikel dari sedikitnya 8 portal dan sekitar 3.000 komentar.
- Reliabilitas koding: *Krippendorff's alpha* sebesar 0,7 atau lebih.
- Presisi ekstraksi kutipan sebesar 0,85 atau lebih pada sampel validasi.
- Seluruh hasil utama dapat direproduksi dari repositori.
- Naskah siap kirim ke jurnal target sebelum akhir kuartal pertama 2027.

---

## 11. Risiko dan Mitigasi

| Risiko | Mitigasi |
| :--- | :--- |
| Artikel diedit atau dihapus | Arsipkan sejak awal dengan hash dan waktu pengambilan |
| Portal memblokir bot atau memuat konten lewat JS | Parser per situs, jeda request, fallback header realistis |
| Kuantitas data terlalu kecil untuk jaringan bermakna | Snowball dari seed, perluas kata kunci dan jendela waktu |
| Berita kantor berita menggembungkan edge | Deteksi duplikat dan simpul khusus untuk wire (sindikasi) |
| Risiko hukum atau etika | Ethical clearance, anonimisasi ID (hashing), konsultasi bagian hukum |
| Kasus berkembang cepat (penentuan jendela waktu) | Tetapkan jendela utama di awal, laporkan analisis sensitivitas |
| Kebaruan dinilai kurang | Rumuskan hipotesis teoritis dan tambahkan pembanding komparatif |
