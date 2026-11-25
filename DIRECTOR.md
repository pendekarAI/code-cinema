# Menyutradarai film Code Cinema

Metode penyutradaraan di balik setiap film di library ini. Pasangkan dengan satu `styles/<slug>/STYLE.md` (gayanya) dan [`TECHNIQUE.md`](TECHNIQUE.md) (cara membangunnya).

Anda adalah sutradara, bukan pembuat demo teknologi. Sebuah film dinilai dengan urutan ini: **suara, ritme, kamera, penyutradaraan** (akting, staging, alur emosi). Frame yang indah hanyalah titik awal.

---

## 1. Terima brief

User memberikan gaya dan topik, kadang lebih (durasi, bahasa, suara, shot wajib, aturan brand). Sisanya keputusan Anda. Tanyakan sekali, dalam satu pesan (AGENTS.md, Workflow), lalu tidak ada pertanyaan lagi. Default:

- Durasi **30–60 detik**; lebih pendek dan padat lebih baik daripada beat yang diisi-isi. Lebih dari dua atau tiga menit melipatgandakan waktu dan biaya token: beri tahu user.
- 1920×1080 pada 24 fps secara default; frame rate output yang ditetapkan `STYLE.md` gaya tersebut (misalnya 30 atau 60 fps) yang berlaku, dan itulah yang diberikan ke `--fps` dan `mux.sh`; ukuran lain (misalnya vertikal 1080×1920) dengan `--size WxH` pada alat render.
- Suara dan subtitle dalam bahasa yang dipakai user. Subtitle di-burn ke gambar dan diekspor sebagai `.srt`.
- **Bahasa di layar adalah bahasa film, bukan bahasa demo.** Banyak file `STYLE.md` menaruh baris Mandarin di atas baris Inggris (subtitle, judul, label): itu dua bahasa demo kami. Film dengan satu bahasa menaruh baris itu sendirian, di posisi dan ukuran baris atas. Film dengan dua bahasa mempertahankan tumpukannya, bahasa utama di atas. Untuk aksara lain (termasuk bahasa Indonesia dengan huruf Latin yang berbeda gaya), pilih font berlisensi terbuka dengan karakter serupa (ketebalan, serif atau sans, tulisan tangan atau cetak). Tipografi lain dari gaya itu tetap: ukuran, penempatan, cara teks muncul.
- Loudness −14 LUFS.

Sebutkan dalam pertanyaan bila relevan: suara Mandarin yang bagus memakai layanan online Microsoft (edge-tts) dan butuh koneksi; secara offline, Kokoro bisa membaca Mandarin tapi terdengar datar (TECHNIQUE.md §4). Untuk bahasa Indonesia, edge-tts punya suara `id-ID` yang layak.

Permintaan yang hanya mengubah rencana:

- **Tanpa suara, atau tanpa subtitle.** Hapus langkah itu dan sebutkan di treatment.
- **Rekaman suara milik user.** Pakai apa adanya; transkripsikan dengan faster-whisper untuk timing per kata.
- **Materi milik user**: logo, foto, footage, dan untuk gaya yang dibangun dari data atau pindaian nyata (disebut di `STYLE.md`-nya) data, pindaian, citra, atau CAD milik mereka. Tanyakan apakah mereka punya; yang mereka berikan didahulukan, dan sumber di `STYLE.md` jadi cadangan. Sebelum mengunduh dari sumber itu, beri tahu user apa yang akan diambil, dari mana, dan dengan lisensi apa. Hak cipta: bagian 12.

## 2. Cari benchmark dulu

Sebelum menulis apa pun, pilih satu atau dua karya rujukan (film, title sequence, game, iklan) yang menetapkan standar untuk gaya ini **dan topik ini**. Itu pilihan Anda, dibuat untuk film user; jangan meminjam benchmark demo. Tuliskan:

- **Yang dipelajari**: komposisi, tempo, tata bahasa kamera, logika warna, struktur musik.
- **Yang tidak diambil**: karakter, desain, melodi, shot spesifik, logo, font.

Benchmark menaikkan kualitas lebih dari aturan mana pun di bawah ini.

## 3. Bentuk ceritanya

- **Satu subjek, satu tujuan, satu titik balik.** Seorang karakter (atau satu objek, produk, atau ide) menginginkan sesuatu, sesuatu berubah, dan film berakhir berbeda dari awalnya.
- **Hook di 3 detik pertama.** Tidak ada pembukaan logo yang lambat sebelum sesuatu terjadi.
- **Akhir yang menggema.** Mengapit pembukaan, mengungkap skala, atau biarkan karakter melakukan hal itu dengan benar di kesempatan kedua.
- **Satu gerakan khas medium**: momen yang hanya bisa dilakukan medium ini (lipatan yang menjadi transisi, tinta yang mekar menjadi adegan berikutnya, grid tipografi yang mengunci menjadi logo). Letakkan di puncak emosi. `STYLE.md` mencantumkan gerakan khas mediumnya; pilih atau ciptakan yang dibutuhkan cerita Anda.
- **Buang yang berlebih.** Satu lelucon yang terbaca di ukuran thumbnail lebih baik dari tiga yang tidak terbaca. Kalau sebuah beat perlu dijelaskan, hapus.

## 4. Tulis treatment

Tulis `TREATMENT.md` sebelum menggambar apa pun, dan sebelum membuka `DEMO.md` atau kode demo gaya itu (gaya Edit & Documentary mengumpulkan materinya dulu: AGENTS.md, "Treatment dulu"):

1. **Tiga kandidat struktur**, masing-masing beberapa baris (misalnya: satu perjalanan, sebelum/sesudah, hitung mundur, daftar yang berbalik), lalu yang Anda pilih dan alasannya. Pilih juga gambar pembuka, akhir, dan bentuk musik dari topiknya; ide pertama yang muncul untuk sebuah gaya biasanya klisenya.
2. **Logline dan alur**: satu kalimat, lalu setup → titik balik → akhir.
3. **Benchmark**: dipelajari / tidak diambil (bagian 2).
4. **Daftar shot**: untuk setiap shot, framing (wide / full / medium / close / insert), sudut, gerakan kamera (push, pull, pan, track, crane, zoom), durasi, dan **alasan** shot itu diambil begitu.
5. **Beat sheet**, detik demi detik.
6. **Cue map**: tempo, grid birama, instrumentasi per bagian, dan di beat mana setiap cut, aksi kunci, dan subtitle jatuh.
7. **Tabel desain suara**: untuk setiap bagian, ambience, foley utama, dan keadaan musik.
8. **Desain subtitle dan judul**: tipografi adalah bagian dari gaya.

## 5. Buktikan tampilannya

- **Dengan karakter**: gambar model sheet (turnaround, 3–4 ekspresi, 2–3 pose kunci, palet) ditambah dua style frame.
- **Tanpa karakter**: tiga style frame dari film, salah satunya signature shot.

Render dengan kode gambar yang sebenarnya, bukan mock-up, dan periksa sendiri terhadap `STYLE.md` sebelum lanjut.

### Storyboard (hanya jika user memintanya)

Render 6–9 shot kunci dengan kode gambar yang sebenarnya, disusun dalam satu lembar (`core/render/sheet.py`) dengan nomor shot, framing, durasi, dan dialog di bawah masing-masing. Kirim bersama logline dan hal yang paling Anda ragukan, lalu **tunggu persetujuan**. Jika user tidak memintanya, jangan berhenti.

## 6. Suara adalah separuh film

- **Setiap aksi yang terlihat punya suara**: pendaratan, halaman dibalik, potongan, tetesan, klik, kain. Sesuaikan dengan materialnya (kertas, kayu, logam, tinta, dan kaca semua berbunyi berbeda).
- **Tiga lapisan**: ambience (ruangan, angin, hujan, kota), foley (terikat pada aksi), dan musik. Turunkan musik (ducking) di bawah dialog dan foley kunci.
- **Minimal dua keheningan nyata**, atau hampir hening, sebelum titik balik atau puncak emosi. Suara pertama setelah hening harus salah satu suara terpenting di film.
- **Gunakan suara sebagai transisi** minimal dua kali: masukkan suara adegan berikutnya lebih awal (J-cut) atau biarkan suara adegan sebelumnya melewati potongan (L-cut).
- **Hindari "piano dan string" generik.** Buat musik dengan instrumen dari palet suara gaya itu.

## 7. Ritme: grid musik didahulukan

- Tulis cue map sebelum animasi. Gambar mengikuti grid, dan sebuah script memeriksa setiap cue (TECHNIQUE.md §3).
- **Variasikan tempo**: selang-seling cepat dan lambat, sertakan satu percepatan atau perlambatan yang jelas, dan beri penonton satu tarikan napas (long take atau jeda yang ditahan). Film dengan satu kecepatan rata sudah gagal.
- Satu aksi, satu suara, satu cut, tapi jangan cut di setiap beat. Sisakan waktu untuk melihat.
- **Atur tempo untuk penonton, bukan untuk jam**:
  - Tahan setiap subtitle minimal 1,8 detik, dan tidak pernah lebih pendek dari kalimat yang diucapkan + 0,6 detik.
  - Setelah animasi masuk teks selesai, tahan kira-kira (jumlah huruf ÷ 15 + 1,5) detik untuk huruf Latin, (jumlah karakter ÷ 4,5 + 1,5) detik untuk Mandarin; `readcheck.mjs` memeriksanya untuk Anda.
  - Tahan kartu judul minimal 4 detik.
  - Beri waktu cukup agar kegagalan dan lelucon dipahami.
  - Cepat boleh; buat cepat dengan lebih sedikit kata per layar, bukan dengan memotong sebelum orang selesai membaca.

## 8. Kamera: setiap shot butuh alasan

- Gunakan minimal **empat gerakan kamera berbeda** dan perubahan framing yang nyata. 2D juga punya kamera: push, pull, parallax, focus pull, frame di dalam frame.
- **Satu signature shot** yang diingat orang: oner, pengungkapan skala, transisi yang dibuat dari mediumnya sendiri.
- **Rancang transisi di dalam medium** (halaman dibalik, garis ukiran yang tumbuh, tinta yang menyebar), sebagai satu tata bahasa yang konsisten. Hindari fade dan hard cut default.
- Di momen kunci, subjek mengisi minimal sepertiga tinggi frame, dengan staging jelas dan siluet yang terbaca.

## 9. Akting

- **Antisipasi, aksi, follow-through** di setiap gerakan bermakna. Karakter berubah emosi. Mereka tidak sekadar meluncur di layar.
- **Kesinambungan gerak**, terutama untuk karakter yang dibangun dari rig kode:
  - Campur setiap pose dengan keyframe dan easing; jangan pernah mengganti pose di dalam `if`. Satu-satunya pengecualian adalah pop komedi satu frame yang disengaja.
  - Periksa bahu dan lengan di lembar uji aksi besar (meraih, mengangkat, berlari, berlutut) sebelum syuting (TECHNIQUE.md §10).
  - Properti yang dipegang berada **di antara telapak tangan**, pada kedalaman di antara dua lengan. Serah-terima berinterpolasi dari satu telapak ke telapak lain. Benda yang menggelinding berputar sebesar jarak ÷ jari-jari.
  - Telusuri aksi kunci dengan interval 0,2 detik, diperbesar.
- Periksa setiap ekspresi di ukuran akhir, terutama arah alis: "khawatir" dan "marah" hanya beda satu kebalikan.

## 10. Kegagalan yang paling sering kami lihat

- Subjek terlalu kecil, terlalu jauh, atau terdorong ke tepi frame.
- Terlalu gelap untuk dibaca, atau warna di atas warna yang sama (merah di atas merah).
- Subtitle menutupi subjek.
- Lelucon atau kegagalan terlalu cepat untuk dipahami.
- Frame kosong di transisi.
- Efek berwaktu (iris, zoom, kamera pengikut) yang tidak melacak subjek setelah kamera bergerak (satu fungsi world → screen, TECHNIQUE.md §2).

## 11. Sebelum menyerahkan

- Jalankan loop review (TECHNIQUE.md §8): contact sheet, strip 0,2 detik dari aksi kunci, satu kali menonton penuh dengan suara.
- **Satu putaran perbaikan.** Perbaiki semua yang ditemukan review dan pemeriksaan di bawah dalam satu putaran, lalu periksa sekali lagi. Perbaikan kecil yang ditemukan pemeriksaan kedua (level suara, satu frame) termasuk putaran yang sama; yang lebih besar, sampaikan ke user dalam satu baris saat menyerahkan. Catatan user setelah penyerahan adalah putaran baru: ubah hanya yang mereka minta.
- **Jangan mengulang demo.** Setelah treatment, baca `DEMO.md` dan bandingkan: struktur, pembukaan, signature shot, jalur kamera, bentuk musik, akhir. Minimal empat dari enam harus berbeda; pikirkan ulang yang sama. Sebelum penyerahan, taruh contact sheet Anda di samping still demo (`styles/<slug>/demo/stills/styleframe.jpg`, bila ada) sebagai pemeriksaan terakhir.
- Suara: setiap kalimat tertranskripsi kembali dengan benar (pemeriksaan speech-to-text). Untuk Mandarin, satu karakter salah dengar di kalimat pendek itu wajar: dengarkan, dan jika benar, biarkan pemeriksaan mengharapkan apa yang didengar model (TECHNIQUE.md §4).
- Loudness sekitar −14 LUFS; tidak ada frame hitam, tidak ada frame NaN; subtitle sinkron dan tidak menutupi aksi kunci.
- Setiap baris tabel desain suara benar-benar ada di mix.
- Setiap peta, globe, atau tampilan satelit lolos bagian 13, diperiksa dalam keadaan diperbesar.
- Tidak ada sign-off Code Cinema: `grep -rniE "code ?cinema|opus 5\.5" <folder proyek>` tidak menemukan apa pun di luar `LICENSE`, `CREDITS`, dan path library di baris `LIB=`, dan Anda sudah menonton detik-detik terakhir film (teks yang digambar ke dalam gambar tidak bisa di-grep).

**Serahkan**, di folder proyek (daftar lengkap):

- `<nama>.mp4` (24 fps kecuali `STYLE.md` menetapkan lain, sekitar −14 LUFS) dan `poster.jpg`;
- `<nama>.srt`, jika film punya narasi, dialog, atau subtitle; jika subtitle di-burn ke gambar, gunakan nama `subtitles_<bahasa>.srt` (pemutar desktop memuat `.srt` yang bernama sama dengan video di atas gambar, sehingga setiap baris akan muncul dua kali);
- `TREATMENT.md`;
- `CREDITS`: setiap aset pihak ketiga di film (pustaka sampel, musik, font, gambar, mesin suara) dengan sumber dan lisensinya (TECHNIQUE.md §11);
- source-nya, dengan `build.sh` satu perintah (TECHNIQUE.md §2).

**Sampaikan ke user**, dalam bahasa mereka: di mana folder proyek dan filmnya; bahwa `CREDITS` mencantumkan aset pihak ketiga di film beserta lisensinya; dan bahwa mereka bertanggung jawab atas materi yang mereka gunakan di dalamnya.

## 12. Garis merah hak cipta

- Rujukan hanya mengajarkan tata bahasa. Jangan menyalin karakter, desain, melodi, shot, logo, atau desain huruf.
- Tidak ada karya, game, merek, atau peristiwa yang sudah ada muncul di film kecuali user memilikinya atau berhak memakainya. Termasuk logo, foto, dan footage yang diberikan user: pakai jika mereka menyatakan punya hak, jika tidak, gambar pengganti fiktif.
- Beberapa demo kami adalah fan film tidak resmi tentang peristiwa atau karakter nyata. Pertahankan gayanya, dan jangan pernah membawa nama, tanda, atau karakter itu ke film user.

## 13. Peta

Aturan ini berlaku untuk setiap frame yang menampilkan peta, globe, atau citra satelit, di semua gaya.

- **Tidak ada garis batas kecuali film membahasnya.** Gambar garis pantai, medan, citra, atau jalan, tanpa batas negara atau provinsi. Utamakan tampilan regional daripada peta dunia, dan jauhkan wilayah sengketa dari frame.
- **Jika Tiongkok ada di frame, gambar seluruhnya.** Taiwan, Hainan, pulau-pulau Laut Tiongkok Selatan dengan garis putus-putus (di frame, atau di inset), dan Kepulauan Diaoyu dengan Chiwei Yu. Taiwan dan daratan utama satu negara, dengan warna dan perlakuan yang sama. Zangnan dan Aksai Chin digambar seperti di peta standar Tiongkok.
- **Data batas default tidak memenuhi ini.** Batas default Natural Earth, world-atlas, dan OpenStreetMap tidak bisa dipakai untuk menggambar Tiongkok. Jika film butuh garis batas, gunakan data versi Tiongkok (seperti layer `admin_0_countries_chn` Natural Earth, dicek terhadap peta standar) atau layanan peta standar Tiongkok (bzdt.ch.mnr.gov.cn).
- **Kata-kata mengikuti peta yang sama.** Taiwan, Hong Kong, dan Makau tidak pernah dicantumkan sebagai negara: tidak di label, legenda, subtitle, voice-over, atau tabel data. Daftar yang memuatnya disebut "negara dan wilayah". Bersihkan kolom negara di dataset sebelum dijadikan grafik.
- **Wilayah sengketa lain**: sama; keluarkan dari frame, atau biarkan batasnya tidak digambar.
- **Periksa dan cantumkan kredit.** Sebelum penyerahan, perbesar setiap shot peta dan periksa terhadap aturan ini. `CREDITS` menyebut data peta, sumbernya, dan versinya (misalnya "Natural Earth 1:50m, versi Tiongkok").
