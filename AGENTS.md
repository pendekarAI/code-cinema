# Code Cinema: instruksi untuk agent

Repositori ini adalah library gaya film. Setiap gaya punya `styles/<slug>/STYLE.md` (apa gaya itu) dan satu film demo yang dibuat sepenuhnya dengan kode (`DEMO.md` dan `demo/`). User memilih gaya dan meminta film tentang topik **mereka sendiri**. Tugas Anda adalah menyutradarai dan memproduksi film itu.

| Permintaan | Buka |
|---|---|
| Permintaan apa pun: lihat dulu gaya milik user; belum ada permintaan: tawarkan pilihan jalur | **Mulai** di bawah |
| Film tentang topik user (kasus normal), 30 detik sampai 60 menit | **Gaya dan cerita**, **Alur kerja** di bawah (durasi, gaya naskah, dan voice over ditanyakan tepat setelah gaya jelas, lalu naskah ditulis sebelum produksi; film panjang: DIRECTOR.md §1 dan TECHNIQUE.md §13) |
| "Gaya apa saja yang ada?" / belum memilih gaya | **Mencari gaya** di bawah |
| Penyutradaraan: cerita, suara, ritme, kamera, peta, pemeriksaan, penyerahan | [`DIRECTOR.md`](DIRECTOR.md) |
| Pembangunan: instalasi, halaman, suara, musik, mix | [`TECHNIQUE.md`](TECHNIQUE.md) |
| Perintah dan flag alat | [`core/README.md`](core/README.md) |
| User ingin mengubah gaya dan menyimpannya sebagai miliknya, membuat gaya sendiri dari nol, atau menyebut gaya di `~/code-cinema-styles/` | [`MY-STYLES.md`](MY-STYLES.md) |

**Film di luar `styles/` adalah milik user: tanpa kredit Code Cinema, tanpa watermark.**

## Mulai

- **Gaya milik mereka didahulukan.** Jika `~/code-cinema-styles/README.md` ada, baca: file itu mencantumkan setiap gaya yang disimpan user, di mana pun disimpan, dan gaya milik mereka ([`MY-STYLES.md`](MY-STYLES.md)) diperlakukan sama seperti gaya library. Saat mereka menyebut sebuah gaya, cari di sana dulu, lalu di library.
- **Bahasa mereka.** Bicara dengan user dalam bahasa yang mereka pakai. Default: Bahasa Indonesia. Jika mereka memulai skill tanpa menulis apa pun, pertanyaan pertama Anda selalu soal bahasa, bahkan jika pengaturan, memori, atau pesan sebelumnya mengisyaratkan satu bahasa: gunakan tool `AskUserQuestion`, satu pertanyaan tersendiri berjudul "Bahasa / Language" dengan dua opsi, Bahasa Indonesia dan English (tool menambahkan Other, tempat mereka mengetik bahasa lain). Gunakan bahasa itu seterusnya, dan sebagai bahasa default film.
- **Belum ada permintaan** (mereka hanya memulai skill, atau menyapa): tawarkan pilihan jalur dengan satu pertanyaan, memakai tool `AskUserQuestion`, dalam bahasa mereka, dengan opsi pertama sebagai rekomendasi:
  1. film dengan gaya library (**Mencari gaya**);
  2. mengubah gaya library dan menyimpannya sebagai milik mereka ([`MY-STYLES.md`](MY-STYLES.md));
  3. membuat gaya sendiri dari nol ([`MY-STYLES.md`](MY-STYLES.md));
  4. film dengan salah satu gaya milik mereka, hanya jika mereka punya (sebutkan namanya).

  Jika permintaan mereka sudah menyebut yang mana, lewati pertanyaan ini.

## Gaya dan cerita

- **`STYLE.md` bersifat tetap**: invarian gaya (tampilan, warna, tipografi, gerak, tata bahasa kamera, palet suara, gerakan khas, jebakan). Pertahankan semuanya.
- **Selebihnya Anda yang menyutradarai** dari topik user: cerita, struktur, karakter, latar, shot, timing, rujukan, cara data digrafikkan. Jangan pernah membelokkan topik ke arah demo. Bahasa di layar juga milik film: baris Mandarin di atas baris Inggris di sebuah `STYLE.md` adalah dua bahasa demo kami (DIRECTOR.md §1).
- **Treatment dulu, demo belakangan.** Tulis `TREATMENT.md` Anda sendiri, dengan tiga kandidat struktur dan pilihan Anda (DIRECTOR.md §4), sebelum membuka `DEMO.md` atau kode demo. Lalu gunakan demo hanya untuk mempelajari teknik (mesin kuas, rig, shader, mix), jangan pernah cerita, alur, shot, properti, atau timeline-nya. Satu pengecualian: gaya yang dipotong dari materi nyata (Edit & Documentary) butuh materinya sebelum treatment, jadi alat yang disebut `STYLE.md`-nya di `demo/tools/` untuk mencari dan mencatat materi (`footage.py` dan sejenisnya) boleh dipakai lebih dulu, disalin ke folder proyek dan dijalankan di sana; tetap baca `DEMO.md` dan sisa demo hanya setelah treatment ditulis.
- **Gaya adegan** (panduan setup, penjelasan spesifikasi, pelat museum, panduan jalur) mencantumkan use case di `STYLE.md`-nya. Baca sebagai tata bahasa untuk urutan informasi muncul dan berapa lama setiap bagian butuh di layar, lalu bangun konten user dalam struktur Anda sendiri. Menukar teks ke `content.json` demo hanya pemeriksaan teknis, bukan cara menyerahkan hasil.
- Jangan pernah membangun di dalam `styles/`: salin yang Anda butuhkan ke folder proyek film.

## Mencari gaya

User menyebut gaya dengan namanya dalam bahasa Inggris atau Mandarin ("Impasto Oil Painting", "油画厚涂") atau dengan nama foldernya (`impasto`). Cari di [`styles/README.md`](styles/README.md). Jika tidak ada yang cocok dengan jelas, tunjukkan dua atau tiga yang paling dekat dan tanyakan.

Jika user belum memilih gaya:
- Sarankan dua atau tiga yang cocok dengan topik mereka.
- Jika mereka punya gaya sendiri, cantumkan lebih dulu, di bawah judul "Gaya saya" (dalam bahasa mereka).
- Tampilkan daftar lengkap di bawah ini di chat. Nama gaya tetap dalam bahasa Inggris; nama kategori dalam bahasa user. Jangan menghapus, menggabungkan, atau mengganti nama apa pun.
- Tautkan galeri, tempat setiap gaya punya gambar pratinjau: https://github.com/pendekarAI/code-cinema/blob/main/GALERI.md (contoh penggunaan setiap gaya juga ada di `styles/README.md`).
- Lalu minta mereka mengetik namanya. Daftar ditaruh di pesan Anda sendiri (output perintah tidak terlihat oleh mereka), dan pertanyaannya teks biasa, bukan `AskUserQuestion`: opsinya yang sedikit akan menyembunyikan sisa daftar.

Semua 99 gaya:

- **Edit & Dokumenter** (Edit & Documentary, 8): Caption News, 1920s Newsreel, Live Countdown Split-screen, City Symphony, Visual Investigation, Constructivist Montage, Sports Telestrator, Broadcast News Package
- **Lukisan & Ilustrasi** (Painting & Illustration, 5): Crayon Picture Book, Watercolor Brush, Impasto Oil Painting, Urban Sketch · Pen & Wash, Colored-Pencil Science Illustration
- **Sketsa & Papan** (Sketch & Board, 7): One-line Drawing, Whiteboard Explainer, Chalkboard, Sketchnote, Stick-figure Explainer, Tablet Sketch Explainer, Marker on Paper
- **Kerajinan Tradisional** (Traditional Crafts, 7): Chinese Ink Wash, Shadow Puppetry, Ukiyo-e, Red Paper-cut, Paper-cut Lightbox, Stained Glass, Gilded Illumination
- **Cetak & Seni Grafis** (Print & Printmaking, 8): Risograph Print, Halftone Dossier, Woodcut Print, Copperplate Engraving, Silkscreen Travel Poster, Scratchboard Long Take, Pop Art, Vintage Engraving Collage
- **Grafis & Tipografi** (Graphic & Type, 8): Swiss Motion Graphics, 60s Spy Title Sequence, Art Deco, Pictogram Motion, Bauhaus Shapes, Scale Zoom Explainer, Text Flash Cuts ✦, Silhouette Rhythm
- **Diagram Garis** (Line Diagrams, 8): Blueprint, Isometric Infographic, Exploded Teardown, Line-Art Cutaway, Color-Coded Mechanism, Instruction Manual Art, Pen Plotter, Assembly-Line Diagram
- **Kartun** (Cartoons, 6): 1930s Rubber Hose Cartoon, 80s Cel Anime, Sci-Fi Sitcom Toon, Mid-century Cartoon, Comic History Cartoon ✦, Manga Panels ✦
- **Game** (Games, 4): 16-bit Pixel RPG, 2.5D Pixel Art, Microgame Frenzy, Rhythm Game Show
- **Film & Pita** (Film & Tape, 5): CRT ASCII Terminal, 1920s Silent Film, Liminal Found Footage, Scratch Film, Double Exposure
- **Layar & Antarmuka** (Screens & Interfaces, 6): Dark Tech Keynote, Mascot Screencast, Sci-fi Hologram HUD, Tabletop App Flythrough, Spreadsheet Film, 1-bit Dither
- **Cahaya & Garis** (Light & Lines, 5): Circuit Board, Firefly Pointillism, Flow-field Wind Lines, Oscilloscope Math, Neon Tubes
- **3D & Miniatur** (3D & Miniature, 8): Brick Toy, Paper Pop-up Book, Tilt-Shift Miniature, Low-poly Isometric Island, Glass Product Render, Memphis Diorama, Isometric People Scene, Crayon World 3D
- **Instrumen & Bukti** (Instruments & Evidence, 8): Satellite Briefing, Engineering Briefing Board, LiDAR Survey, Under the Microscope, Archive Light Table, Security X-ray, Radar Sweep Documentary, Thermal Camera
- **Data & Peta** (Data & Maps, 6): Data Storytelling, Projection-Mapped Model, Data Physicalization, Transit Map, 3D Map Explainer, Blob Simulation

✦ menggambar dengan generator gambar: Codex CLI milik user, atau alat gambar lain yang mereka punya. Tanpa itu film tidak bisa dimulai (core/README.md, "Image generation"). Sebutkan hal ini saat menyarankan gaya tersebut.

Mascot Screencast tidak disertai demo: maskotnya harus karakter piksel orisinal (atau maskot produk milik user sendiri).

## Alur kerja

1. **Naskah dan voice over: tepat setelah gaya jelas, sebelum brief lain dan treatment.** Jawabannya menentukan bentuk film (narasi suara atau teks di layar), jadi jangan pernah memakai default diam-diam.
   1. **Satu `AskUserQuestion` dengan tiga pertanyaan** (lewati yang sudah disebut user di permintaannya):
      - **"Durasi"**: 30–60 detik (rekomendasi untuk promo dan teaser) · 1–5 menit · 5–20 menit (materi kelas, explainer panjang) · Layar Lebar: 20–60 menit (webinar atau modul kelas penuh, disusun dari 2–3 bagian). Maksimal 60 menit; kategori dan konsekuensinya di DIRECTOR.md §1 (**Durasi dan film panjang**). Jika user memilih di atas 3 menit, sebutkan dalam satu kalimat bahwa prosesnya jauh lebih lama dan render bisa berlanjut dalam beberapa putaran; untuk Layar Lebar, bahwa film dikerjakan per bagian dalam beberapa sesi dan setiap bagian dikirim sebagai pratinjau.
      - **"Gaya naskah"**: Edukatif (rekomendasi untuk materi belajar: jelas, runtut, ramah pemula) · Formal / profesional · Santai / gaul · Storytelling (bercerita dengan tokoh dan konflik). Tool menambahkan Other untuk gaya lain (humor, inspiratif, jualan, dan sebagainya).
      - **"Voice over"**: Rekam suara sendiri (rekomendasi: Anda menulis naskah, user merekam) · Suara AI perempuan atau laki-laki · Tanpa voice over (naskah tampil sebagai teks di layar + musik).
      - **Uji suara AI dulu** sebelum bertanya: pasang tingkat voice bila belum (`… setup.sh deps voice`), lalu `"$LIB/.venv/bin/python" -m edge_tts --text "uji suara" --voice id-ID-GadisNeural --write-media /tmp/vo_test.mp3`. Uji berhasil hanya jika file mp3 itu terbentuk dan tidak kosong. Untuk bahasa lain pakai suara bahasa itu (`python -m edge_tts --list-voices`). Tawarkan suara AI (`id-ID-GadisNeural` perempuan, `id-ID-ArdiNeural` laki-laki) hanya jika uji berhasil; jika gagal (mis. sesi cloud memblokir layanan suara), sebutkan dalam satu kalimat dan ganti opsinya dengan: **suara AI dibuat ulang lewat `build.sh` di komputer user**.
   2. **Tulis naskah** sesuai gaya naskah, topik, bahasa, dan durasi, lalu simpan sebagai `NASKAH.md`, `NASKAH.txt`, dan `vo/lines.json` di folder proyek:
      - kalimat pendek bernomor (v1, v2, …), satu gagasan per kalimat; hook di kalimat pertama; penutup yang menggema pembuka;
      - target jumlah kata ≈ durasi (detik) × 2,3 untuk bahasa Indonesia (2,1 untuk gaya santai atau storytelling; sisakan margin 5–8% untuk jeda dan keheningan musik); cantumkan perkiraan detik per kalimat dan totalnya;
      - di atas 60 detik, susun naskah per bab sesuai kategori durasi (DIRECTOR.md §1): `[Hook]`, `[Peta isi]`, `[Bab N — Judul]`, `[Ringkasan]`, `[Penutup]`; di atas 5 menit kelompokkan bab ke dalam bagian (`[Bagian 1 — Judul]`, …), dengan rekap mini di akhir tiap bagian (`[Rekap Bagian 1]`), dan beri ID kalimat per bab (`b01_v01`, …); untuk Layar Lebar, bagi dulu ke dalam bagian (≤ 20 menit, dipotong di titik alami), kelompokkan bab di dalam tiap bagian ke dalam segmen (`[Segmen 1 — Judul]`), dan beri ID dengan awalan bagian (`p1_b01_v01`, …); naskah bagian 2 dan seterusnya boleh ditulis lengkap setelah bagian 1 disetujui, tapi kerangka seluruh film disetujui di awal;
      - **pakai "bagian", jangan "babak"**: kata "babak" tidak lazim dalam bahasa Indonesia, jadi jangan pernah dipakai di naskah, label, tabel, kartu judul, subtitle, maupun `CHAPTERS.txt`. Di film Layar Lebar, satuan besarnya sudah bernama "Bagian", jadi kelompok bab di dalam tiap bagian disebut "Segmen" supaya satu kata tidak punya dua arti;
      - di `lines.json`, angka ditulis seperti diucapkan di field `say` ("empat puluh") dan sebagai digit di `text` (subtitle); tandai istilah asing beserta cara bacanya di `NASKAH.md`;
      - tulis juga **`NASKAH.txt`**, file teks polos untuk dibaca saat merekam atau ditempel ke teleprompter / aplikasi TTS, UTF-8, tanpa markdown:
        ```
        JUDUL FILM
        Gaya naskah: … · Target durasi: ± … · Total: … kata (± … detik)

        === NASKAH UTUH ===
        [Hook]
        <kalimat-kalimat bagian ini disambung menjadi satu paragraf>

        [Bab 1 — Judul]
        <paragraf>
        …

        === KALIMAT BERNOMOR (untuk rekaman per kalimat) ===
        v1  <kalimat>
        v2  <kalimat>
        …

        === CARA BACA ISTILAH ===
        data science: dé-ta sai-ens
        …

        === PANDUAN REKAM ===
        <panduan rekam langkah 1.3, ringkas>
        ```
        Teks naskah utuh memakai kalimat yang diucapkan (field `say`, angka ditulis dengan huruf), tanpa nomor dan tanpa perkiraan detik, supaya bisa langsung dibaca atau ditempel. Bagian kalimat bernomor hanya diisi jika user merekam sendiri atau film di atas 60 detik; bagian cara baca hanya jika ada istilah asing. Setiap kali naskah direvisi, perbarui `NASKAH.md`, `NASKAH.txt`, dan `vo/lines.json` bersama-sama;
   3. **Kirim naskah dalam satu pesan, bersama pertanyaan brief langkah 2** (supaya tidak menambah putaran):
      - naskah lengkap di chat sebagai tabel: no, kalimat, perkiraan detik; untuk film di atas 3 menit, di chat cukup tabel per bab (judul, jumlah kata, perkiraan detik) dan kirim `NASKAH.md` lengkap sebagai file;
      - **di bawah tabel, blok "Naskah siap salin"**: satu blok kode berisi naskah utuh yang sama dengan bagian NASKAH UTUH di `NASKAH.txt` (paragraf per bagian, label bagian di baris sendiri, tanpa nomor dan detik), supaya user tinggal menyalinnya dengan tombol copy. Untuk film di atas 3 menit, blok ini cukup berisi Hook dan Bab 1 sebagai contoh, dan naskah utuh ada di file;
      - **sertakan `NASKAH.txt` sebagai file yang bisa diunduh**: di sesi cloud kirim dengan `SendUserFile` (bersama `NASKAH.md` untuk film di atas 3 menit); di komputer user sebutkan path lengkapnya di folder proyek. Setelah revisi, kirim versi terbaru lagi;
      - jika user merekam sendiri, sertakan panduan rekam: satu file utuh dengan jeda ±1 detik antar kalimat, atau satu file per kalimat bernama `v1`, `v2`, …; format WAV, MP3, atau M4A; ruang hening, jarak mulut 15–20 cm, tanpa musik latar; boleh sedikit improvisasi karena timing film mengikuti rekaman; untuk film di atas 5 menit, satu file per bab bernomor dua digit (`bab01`, `bab02`, …), dengan ruangan dan jarak mikrofon yang sama untuk semua bab; untuk Layar Lebar dengan awalan bagian (`p1_bab01`, …, `p2_bab01`, …), dan rekaman bagian 1 boleh dikirim lebih dulu;
      - minta user menyetujui naskah atau menyebut revisinya.
   4. **Tunggu persetujuan naskah** dan revisi bila diminta. Lalu:
      - **Rekam sendiri:** jangan memproduksi suara dan animasi sebelum file rekaman diterima; treatment dan style frame boleh dikerjakan sambil menunggu. Setelah file tiba, potong per kalimat bila masih satu file (deteksi jeda dengan `ffmpeg silencedetect`), periksa dan ambil timing per kata dengan `core/tts/asr_check.py` (faster-whisper), lalu susun timeline, subtitle, dan potongan gambar dari rekaman itu (TECHNIQUE.md §4).
      - **Suara AI:** buat suaranya dari naskah yang disetujui (`core/tts/tts_zh.py … --voice <nama suara>`), lalu periksa dengan `asr_check.py`.
      - **Tanpa voice over:** naskah menjadi teks di layar; pastikan setiap baris tampil cukup lama (`readcheck.mjs`).
2. **Brief.** Pastikan gaya dan topik jelas, lalu tanyakan ke user sekali, dalam pesan yang sama dengan naskah (langkah 1.3; DIRECTOR.md §1):
   - apa pun tentang topik yang tidak bisa Anda putuskan sendiri (fakta; nama, logo, atau produk yang harus muncul);
   - apakah mereka punya materi sendiri: musik, foto, logo, font, dan untuk gaya yang dibangun dari materi nyata, data atau pindaian milik mereka;
   - bahasa film, jika belum jelas (default: bahasa yang mereka tulis atau pilih, untuk suara dan subtitle);
   - apakah mereka ingin melihat storyboard dulu (default: tidak);
   - apa pun yang belum ada di komputer mereka: sebelum bertanya, jalankan `sh plugin/skills/code-cinema-by-megabagus/scripts/setup.sh` dari root library (tanpa argumen: butuh beberapa detik dan menampilkan semua alat sistem yang belum ada sekaligus) dan sertakan laporannya. Jalankan `… setup.sh deps` (inti saja) di background, jika belum berjalan: pertama kali butuh beberapa menit. Tambahkan tingkat voice dan music belakangan, hanya jika film membutuhkannya (TECHNIQUE.md §1);
   - untuk gaya bertanda ✦, cara mereka membuat gambar, tapi hanya jika pemeriksaan gambar di bawah gagal.

   **Gaya bertanda ✦ menggambar dengan generator gambar** (`style.json`-nya memuat `"needs": ["image-generation"]`). Jalankan `python3 core/image/gen_image.py --check` dari root library sebelum menulis pertanyaan, bersama `setup.sh`. Jika gagal, sertakan alasannya dan pertanyaannya di pesan yang sama: dengan apa mereka akan membuat gambar (API atau aplikasi gambar lain, atau gambar mereka sendiri; Anda memberikan prompt dan nama file)? Tanpa generator gambar sama sekali, sampaikan dengan jelas bahwa film dengan gaya ini tidak bisa dimulai, dan tawarkan dua atau tiga gaya lain yang cocok dengan topik mereka. Jangan pernah menggambar karakter dengan kode sebagai pengganti.

   Lewati yang sudah dijawab permintaan mereka. Tunggu balasan, isi celah lain dengan default yang masuk akal, ringkas brief dalam beberapa baris, lalu mulai. Jangan kembali dengan pertanyaan lagi.
3. **Treatment.** Tulis `TREATMENT.md` di folder proyek (DIRECTOR.md §4), sebelum membuka demo (gaya Edit & Documentary mengumpulkan materinya dulu: **Treatment dulu** di atas).
4. **Tampilan.** Render style frame atau model sheet dengan kode gambar yang sebenarnya dan periksa terhadap `STYLE.md` (DIRECTOR.md §5).
5. **Storyboard, hanya jika user memintanya** (DIRECTOR.md §5). **Berhenti dan tunggu persetujuan.** Jika tidak, jangan berhenti.
6. **Produksi.** Suara → pemeriksaan → score (bisa paralel) → animasi → mix → render (TECHNIQUE.md).
7. **Periksa sendiri dan serahkan** (DIRECTOR.md §11).

Laporkan progres dalam bahasa user. Jika sebuah langkah gagal, baca error-nya, perbaiki penyebabnya, dan coba lagi; kembali ke user hanya untuk keputusan atau sesuatu yang hanya bisa mereka berikan.

## Di mana semuanya diletakkan

- Folder proyek film adalah `films/<nama>/` di dalam clone (diabaikan git), atau `<nama>/` di folder user dalam mode skill (lihat `SKILL.md` skill-nya). Setiap kali panduan menyebut `films/<nama>/`, baca sebagai "folder proyek". Bekerja hanya di sana, kecuali user meminta Anda bekerja di proyek mereka sendiri.
- Jalankan `node core/…` dan `sh tools/…` dari root library (`$LIB` dalam mode skill).
- `core/` berisi alat siap pakai (rendering, TTS, pemeriksaan suara, sampler, sfx, mux). Pakai alat itu atau stack Anda sendiri, tapi jangan mengedit `core/` atau `styles/` untuk film user.
- Jangan pernah mematikan proses yang tidak Anda mulai. Jangan tinggalkan proses background berjalan.
