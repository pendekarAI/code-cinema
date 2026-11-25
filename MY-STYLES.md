# Jadikan sebuah gaya milik Anda

User membuat gaya miliknya sendiri, dengan salah satu dari dua cara: **mengubah gaya library**, atau **mulai dari halaman kosong**. Anda merencanakannya bersama mereka, satu pertanyaan per pesan atau dalam percakapan bebas, membuktikan tampilannya dengan satu style frame, dan membuat film demo pendek. Setelah mereka mengonfirmasi, Anda menyimpannya di folder milik mereka dengan bentuk yang sama seperti gaya library. Sejak itu mereka menyebutnya seperti gaya library mana pun saat meminta film. Gaya itu tinggal di luar library dan tidak pernah mengubahnya.

Gunakan panduan ini saat user ingin mengubah gaya atau membuat gaya sendiri ("saya mau ubah gaya ini", "buat versi saya sendiri", "mulai dari nol", "I want to change this style", "make my own version"), atau saat mereka menyebut gaya yang ada di folder milik mereka. Hal lain dalam sebuah film mengikuti [`AGENTS.md`](AGENTS.md) seperti biasa, dengan pengecualian yang diberikan panduan ini.

Bicara dengan user dalam bahasa mereka. Tulis file dalam bahasa Inggris, seperti library, dengan nama gaya dalam bahasa Inggris dan bahasa user.

## Di mana disimpan

Sampai user mengonfirmasinya (§6), sebuah gaya adalah draf di folder proyek film demonya. Gaya yang sudah dikonfirmasi tinggal di **`~/code-cinema-styles/`**, di luar library, sehingga update library dan uninstall tidak pernah menyentuhnya. `~/code-cinema-styles/README.md` mencantumkan setiap gaya, satu baris per gaya (nama Inggris dan nama dalam bahasa user, slug, base, satu baris tentang apa gaya itu, dan foldernya jika tidak di `~/code-cinema-styles/`): inilah cara sesi berikutnya menemukan gaya berdasarkan nama. Jika user ingin gaya disimpan di folder lain, simpan di sana dan tetap tambahkan barisnya, dengan path lengkap, ke `~/code-cinema-styles/README.md`.

Setiap gaya punya foldernya sendiri, `~/code-cinema-styles/<slug>/`, dengan bentuk seperti gaya library:

| File | Isinya |
|---|---|
| `style.json` | `slug`, `en` (nama Inggris), `local` (nama dalam bahasa user, mis. Indonesia), `based_on` (slug base; dari halaman kosong, base tekniknya), `borrows` (slug tempat gerakan diambil, boleh kosong), `size` (hanya jika default bukan 1920×1080, mis. `"1080x1440"`), `needs` (disalin dari base, mis. `["image-generation"]` untuk base ✦; hilangkan jika base tidak punya), `library_version` (`git -C "$LIB" rev-parse --short HEAD`, atau versi plugin jika `$LIB` bukan clone git), `created`, `line` (satu kalimat bahasa Inggris), `line_local` (satu kalimat bahasa user) |
| `STYLE.md` | hanya invarian gaya, dalam bagian-bagian `STYLE.md` library (11 di sebagian besar gaya; gaya yang diubah mempertahankan bagian base-nya): tanpa cerita, tabel beat, durasi, atau end card |
| `CHANGES.md` | satu baris per keputusan: bagian, base, sekarang, alasan. Dari halaman kosong, "base" adalah nilai dari base teknik, atau "—" untuk hal baru. Inilah yang disetujui user dan yang Anda periksa di film demo |
| `DEMO.md` | cara film demo dibuat, seperti `DEMO.md` library: dibuka dengan "One example among many. Don't reuse its story, arc, shots, props or timings.", lalu cerita, shot, palet, score, catatan build, dan file mana menggambar apa. File ini menggantikan `TREATMENT.md` film, yang tidak disimpan |
| `demo/` | source film demo dengan `build.sh` satu perintah dan `CREDITS`: kode dan aset kecil yang dibutuhkan untuk build ulang (font, data), bukan hasil render, frame, `node_modules`, virtual environment, atau cache. `CREDITS` menyebut setiap aset agar bisa dicari lagi, dan `build.sh` mengambil font lebih dulu, sehingga clone baru bisa build |
| `styleframe.jpg` | style frame yang disetujui |
| `styleframe-vs-base.jpg` | hanya untuk mengubah gaya library: frame yang sama, base di kiri, milik mereka di kanan |
| `test.mp4`, `test.jpg` | film demo dan posternya |

Jangan pernah menulis ke `styles/` atau mengedit panduan library untuk ini. Nama dan slug tidak boleh sama dengan gaya library atau baris di `~/code-cinema-styles/README.md`.

## 1. Dari mana mulai

- **Mengubah gaya library.** User menyebut satu gaya (lihat **Mencari gaya** di `AGENTS.md`). Jika belum, lakukan seperti **Mencari gaya** untuk film: daftar lengkap gaya library di pesan Anda, dua atau tiga saran di atasnya jika Anda tahu untuk apa gaya itu akan dipakai, lalu pertanyaan teks biasa yang meminta mereka mengetik namanya (bukan `AskUserQuestion`). Hanya satu base. Jika mereka ingin mencampur dua, ambil yang *Essence* §1-nya paling dekat sebagai base dan ambil hanya yang mereka mau dari yang lain, sebagai perubahan (cantumkan di `borrows`).
- **Mulai dari halaman kosong.** User menggambarkan tampilan dengan kata-kata mereka sendiri, atau membawa gambar atau film yang mereka suka. Pilih satu gaya library sebagai **base teknik** (material dan mesin terdekat: dasar yang akan dibangun kode) dan paling banyak dua untuk dipinjam gerakannya. Jadikan itu pertanyaan pertama: pilihan Anda dan alasannya masing-masing satu baris, dengan yang terdekat berikutnya sebagai opsi lain.

Bagaimanapun caranya, baca `STYLE.md` base secara penuh sebelum pertanyaan pertama. Dalam alur ini Anda boleh membaca `DEMO.md` base (dan, dalam mode skill, mengambil source-nya dengan `setup.sh demo <slug>`) sebelum treatment apa pun: style frame membutuhkan tekniknya. Cerita film demo tetap harus berbeda dari demo base (DIRECTOR.md §11, *Jangan mengulang demo*, dibandingkan dengan base).

## 2. Rencanakan bersama

Wawancarai user sampai setiap bagian `STYLE.md` mereka diputuskan dan mereka tahu konsekuensi tiap pilihan.

**Cara bertanya**

- **Satu pertanyaan per pesan.** Gunakan tool `AskUserQuestion`: 2–3 opsi, yang Anda rekomendasikan di urutan pertama dan ditandai (Rekomendasi), masing-masing dengan satu baris tentang efeknya pada film, dan **Percakapan bebas** sebagai opsi terakhir. Tanpa tool itu, daftar bernomor singkat dengan rekomendasi Anda, dan percakapan bebas sebagai baris terakhir.
- **Percakapan bebas.** Jika mereka memilihnya, berhenti bertanya satu per satu. Tampilkan checklist di chat: apa yang sudah diputuskan, dan setiap hal yang masih terbuka dengan rekomendasi Anda (saat mengubah gaya library, juga kelompoknya dari tabel di bawah). Mereka menjawab dengan kata-kata sendiri, dalam urutan apa pun, beberapa sekaligus, atau balik bertanya. Jika mereka ragu tentang suatu hal, beri dua atau tiga arah konkret. Perbarui checklist setiap putaran; jika semua sudah diputuskan, atau mereka bilang "terserah kamu", lanjut ke ringkasan.
- Setiap pertanyaan punya rekomendasi dan alasan Anda, diambil dari `STYLE.md` base dan yang dikatakan user, dengan contoh konkret dari gaya ini, bukan kata-kata umum.
- Jangan menanyakan yang bisa Anda cari sendiri (`STYLE.md` base, library, file mereka).
- **Paling banyak sekitar sepuluh pertanyaan**, termasuk base teknik. Jika bagian yang terlibat lebih banyak, tanyakan yang berkaitan bersamaan (gerak dengan suara, kamera dengan gerakan khas). Jika mereka bilang "terserah kamu" ("ikut rekomendasi semua"), ambil rekomendasi Anda untuk sisanya, cantumkan dalam satu pesan, lalu lanjut.

**Urutannya** (lewati yang sudah mereka sebutkan):

1. **Kegunaan.** Film apa yang akan mereka buat dengannya, untuk siapa, di mana akan diunggah, dan karena itu ukuran frame (feed vertikal butuh 1080×1920 atau 1080×1440). Brand atau IP mereka: warna, logo, font, karakter. File-nya mereka berikan belakangan.
2. **Apa yang berubah.**
   - *Mengubah gaya library*: tunjukkan dulu tiga kelompok dalam pesan singkat, memakai bagian dan contoh dari gaya ini sendiri. Lalu tanyakan bagian mana yang ingin mereka sentuh (boleh pilih beberapa).

     Nomor bagian di bawah adalah yang umum; beberapa gaya (terutama Edit & Documentary) menomori atau memecahnya berbeda, jadi ikuti pokok bahasan bagian di `STYLE.md` base.

     | Kelompok | Bagian `STYLE.md` | Yang disampaikan ke user |
     |---|---|---|
     | **Aman diubah** | §3 warna (palet dalam logikanya), §4 tipografi, §5 gerak (tempo, seberapa banyak yang bergerak), §7 palet suara (instrumen, kepadatan), §8 gerakan khas (tambah atau tukar satu) | gaya tetap menjadi dirinya; beri 2–3 ide untuk masing-masing |
     | **Mengubah karakternya** | §2 material dan rendering, logika warna itu sendiri di §3, §6 tata bahasa kamera | bisa; sebutkan apa yang hilang dari gaya dengan setiap perubahan |
     | **Tidak bisa diubah** | §1 esensi (dan "apa yang bukan"), §10 mesin | itu gaya yang berbeda, bukan versi dari gaya ini. Sampaikan dan sarankan base yang lebih dekat |

     Jika perubahan yang aman mempersempit sebuah frasa di §1 (tiga tinta menjadi dua), sesuaikan frasa itu; esensinya tetap.
   - *Dari halaman kosong*: esensinya dulu, satu kalimat tentang apa gaya itu dan satu tentang apa yang bukan. Lalu materialnya.
3. **Bagian demi bagian**, hanya bagian yang terlibat, mengikuti urutan `STYLE.md`: material dan rendering, warna, tipografi, gerak, kamera, suara, gerakan khas. Beri 2–3 arah konkret untuk masing-masing.
4. **Namanya**: Inggris, bahasa user, atau keduanya, dan slug-nya.

**Bantu mereka mengubahnya dengan baik.** Sebagian besar user tahu rasa yang mereka inginkan, bukan bagiannya. Sambil bertanya:

- Mulai dari kegunaan. Perubahan mengikuti untuk apa film-filmnya: buletin brand mingguan butuh tipografi yang terbaca dan pembuka yang tetap, channel anak-anak butuh bentuk lebih besar dan waktu baca lebih lambat.
- Ubah keinginan yang samar menjadi opsi, jangan pernah edit diam-diam:

  | Mereka bilang | Biasanya berarti |
  |---|---|
  | lebih premium, lebih mewah | warna lebih sedikit, kontras terang-gelap lebih kuat, gerak lebih lambat, ruang kosong lebih banyak, tipografi lebih ringan |
  | lebih muda, lebih hidup, ceria | aksen lebih cerah, cut di beat, easing lebih memantul, lebih banyak perkusi |
  | lebih tenang, kalem | tempo lebih lambat, tahan lebih lama, lebih sedikit yang bergerak, instrumen lebih jarang |
  | seperti brand kami | warna brand sebagai aksen, bukan latar; font brand untuk judul; logo di pembuka dan penutup |

- **Brand.** Pertahankan struktur terang-gelap base agar teks tetap terbaca, dan masukkan warna brand sebagai aksen dulu. Font brand harus mencakup bahasa film (glyph Mandarin untuk film berbahasa Mandarin) dan mengizinkan penggunaan di video. Logo dan font berasal dari user.
- **Rujukan.** Sebutkan dua atau tiga hal di dalamnya yang membuatnya berhasil, petakan masing-masing ke satu bagian, dan sebutkan mana yang akan menyentuh esensi §1.
- **Pertahankan ciri khasnya.** Gerakan khas adalah yang membuat gaya dikenali: tukar paling banyak satu.
- **Perubahan yang berjalan bersama.** Gerak lebih cepat butuh suara lebih padat. Palet lebih gelap butuh kontras tipografi dicek. Material baru membawa jebakannya sendiri ke §9.
- **Paling banyak lima perubahan** per putaran saat mengubah gaya library; lebih dari itu sulit dinilai. Perubahan yang dipaksa bahasa film (font Mandarin saat base tidak punya) tidak dihitung.
- **Gambar dengan cara base menggambar.** Kode menggambar semuanya kecuali base bertanda ✦: maka gambar tetap berasal dari generator gambar yang disediakan user (AGENTS.md, Alur kerja, Brief), dan kode tidak pernah menggambar pengganti. Jangan menambahkan image atau video generation ke base yang tidak memakainya: user mungkin tidak punya. Apa pun yang bukan kode (gambar, font, data goresan atau peta, sampel) adalah milik user atau berlisensi terbuka, seperti TECHNIQUE.md §11, dan disebut di `CREDITS`. Lisensi yang harus disetujui user ditanyakan sekali, dan jawabannya ditulis ke `STYLE.md` agar film berikutnya tidak bertanya lagi. Jika sesuatu tidak bisa jalan, sampaikan dan tawarkan perubahan terdekat yang bisa digambar kode.
- **Yang tidak butuh gaya.** Cerita, struktur, pembuka, penutup, pemeran, latar, tempo, dan suara (§11 *Variation space*) bebas di setiap film. Jika hanya itu yang mereka mau, mereka tidak butuh gaya sendiri: cukup sebutkan saat meminta film.

Jika rencana sudah lengkap, tunjukkan ringkasan singkat dalam bahasa mereka: setiap keputusan, sebelum dan sesudah, dan konsekuensinya. **Tunggu persetujuan mereka**, lalu tuliskan.

## 3. Tuliskan

Buat folder proyek film demo sekarang (`films/<slug>-test/` di dalam clone, `<slug>-test/` di folder user dalam mode skill) dan bekerja hanya di sana sampai §6. Draf gaya masuk ke folder `style/`-nya, dengan file-file dari tabel di atas.

- **`STYLE.md`**:
  - *Mengubah gaya library*: salinan penuh `STYLE.md` base dengan perubahan ditulis ke bagian-bagiannya, sehingga terbaca seperti style prompt mana pun (tanpa celah "lihat base"). Ganti judul dengan nama baru dan tambahkan satu baris di bawahnya: `Based on <nama base> (<slug base>) from Code Cinema.`
  - *Dari halaman kosong*: semua 11 bagian ditulis dari rencana, dengan §10 *Engine* dari base teknik untuk sementara (langkah 5 di bawah mengarahkannya ke kode gaya itu sendiri). Di bawah judul: `Made from a blank page; techniques from <nama base> (<slug base>) in Code Cinema.`
  - Jika ukuran default bukan 1920×1080, satu baris lagi di bawah judul: `Default size: 1080×1440.`
  - Tautan: `DEMO.md` dan `demo/` milik gaya itu sendiri (ada setelah §5) tetap relatif; tautan ke base menjadi `$LIB/styles/<slug base>/…`. Pertahankan setiap jebakan di §9 yang masih berlaku, dan tambahkan yang dibawa oleh perubahan.
- **`CHANGES.md`** dan **`style.json`** seperti tabel di atas.

## 4. Buktikan tampilannya

Render satu style frame dengan kode gambar yang sebenarnya, mulai dari teknik gaya base (salin kode ke proyek, jangan pernah mengedit library). Periksa terhadap `STYLE.md` yang baru dan perbaiki yang meleset, sekali.

- *Mengubah gaya library*: render frame yang sama kedua kalinya dengan pengaturan base (warna, material, dan tipografinya; font pengganti jika font base tidak punya glyph untuk bahasa film), dan letakkan berdampingan, base di kiri, sehingga hanya perubahannya yang berbeda: `style/styleframe-vs-base.jpg` (`core/render/sheet.py` menyusun still).
- *Dari halaman kosong*: tidak ada pembanding. Tunjukkan frame sendirian, di samping rujukan user jika mereka memberikannya.

Simpan frame sebagai `style/styleframe.jpg`. **Tunjukkan ke user dan tunggu.** Jika mereka ingin lebih, perbarui `STYLE.md` dan `CHANGES.md` lalu render lagi. Jika masih belum pas setelah dua putaran catatan mereka, sampaikan dan sarankan base yang lebih dekat.

## 5. Film demo (15–30 detik)

Film pendek yang tugasnya menunjukkan gaya itu bekerja, bukan produksi penuh:

- **Topik**: milik user jika mereka memberikannya; jika tidak, sesuatu yang sederhana dengan gerakan dan sedikit cahaya (layang-layang di pantai berangin, kereta pertama di pagi hari). Bukan cerita demo base.
- **Setiap baris `CHANGES.md` terlihat jelas di layar** minimal sekali, dan gerakan khas muncul sekali.
- Musik dan efek suara, tanpa suara narasi dan tanpa subtitle kecuali user meminta (suara narasi adalah uji terpisah).
- Treatment: satu struktur cukup (tanpa tiga kandidat). Tanpa storyboard. Hitungan di DIRECTOR.md ditulis untuk film yang lebih panjang: di durasi ini satu keheningan nyata dan tiga jenis gerakan kamera sudah cukup.
- **Pemeriksaan**, seperti film mana pun: DIRECTOR.md §11, dengan satu putaran perbaikannya (tanpa sign-off Code Cinema di film).

Lalu simpan ke `style/`:

- film dan posternya sebagai `test.mp4` dan `test.jpg`;
- source sebagai `demo/`, dengan `CREDITS` dan `build.sh` yang berjalan dari sana: `LIB=<path>` di baris atas, file library sebagai `$LIB/…` (jangan pernah `../..`, termasuk di kode yang disalin dari base), dan semua yang ditulisnya diarahkan ke `${OUT:-<folder di luar demo/>}`. Jalankan sekali dari folder yang disimpan dengan `OUT` diset ke folder sementara, dan periksa bahwa `demo/` berisi file yang sama setelahnya. Kode yang disalin dari library mempertahankan notice MIT-nya di `demo/CREDITS`; itu lisensi, bukan kredit di film;
- `DEMO.md`;
- Dari halaman kosong, arahkan §10 *Engine* di `STYLE.md` ke file di `demo/` yang menggambar gaya itu, lalu ke base teknik.

## 6. Simpan

Tunjukkan film demo ke user: di mana lokasinya, dan setiap perubahan dengan detik di mana ia terlihat. Lalu tanyakan dengan `AskUserQuestion`:

1. **Simpan sebagai gaya saya** (Rekomendasi): periksa bahwa nama dan slug masih tersedia, salin `style/` ke `~/code-cinema-styles/<slug>/` (atau folder yang mereka inginkan), tambahkan barisnya ke `~/code-cinema-styles/README.md` (buat jika belum ada: judul dan tabel dengan satu baris per gaya), dan beri tahu di mana lokasinya dan cara memakainya ("Buat film dengan gaya <nama> saya tentang…").
2. **Satu putaran lagi**: ubah yang mereka minta (§7), lalu tanyakan lagi.
3. **Nanti saja**: biarkan di folder proyek. Beri tahu path-nya, dan bahwa mengatakan "simpan gaya di <path> sebagai gaya saya" nanti akan menyimpannya saat itu.

Hanya gaya yang disimpan yang menjadi milik mereka: dicantumkan saat skill dimulai, dan ditemukan berdasarkan nama.

## 7. Revisi atau pakai

- **Belum pas**: ubah `STYLE.md` dan `CHANGES.md`, lalu render style frame dan film demo lagi dan ganti `demo/` dan `DEMO.md`. Ubah hanya yang diminta user.
- **Memakainya**: temukan lewat `~/code-cinema-styles/README.md`. Baca `STYLE.md`-nya sebagai pengganti `STYLE.md` library dan ikuti alur kerja normal di `AGENTS.md`, treatment dulu, pada ukuran default gaya itu kecuali user meminta lain. Untuk teknik, baca `DEMO.md` dan `demo/` milik gaya itu dulu, lalu milik base (`$LIB/styles/<based_on>/DEMO.md`). Film demo adalah satu contoh: jangan pernah memakai ulang cerita, shot, atau timeline-nya. Film-filmnya milik user: tanpa kredit Code Cinema, tanpa watermark.
- **Setelah update library**: jika `STYLE.md` base berubah sejak `library_version`, sebutkan sekali dan tawarkan untuk membawa perbaikan yang berguna ke salinan mereka. Jangan mengubah gaya mereka tanpa bertanya.
