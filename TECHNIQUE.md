# Teknik: cara film-film ini dibangun

Setiap film di sini dibuat dari kode: tanpa video generation, tanpa stock footage. Halaman ini menjelaskan pipeline-nya, untuk direproduksi dengan alat kami di `core/` atau dengan stack Anda sendiri. Pasangkan dengan [`DIRECTOR.md`](DIRECTOR.md) dan satu `styles/<slug>/STYLE.md`. Semua perintah dan flag ada di [`core/README.md`](core/README.md).

```
timeline (satu sumber kebenaran)
   ├─► gambar:   halaman web dengan render(t) ──► headless Chrome, frame demi frame ──► video.mp4
   ├─► suara:    TTS per kalimat ──► pemeriksaan speech-to-text ──► timing per kata
   ├─► musik:    score dari timeline yang sama (sampel + sintesis) ──► stem
   ├─► efek:     foley prosedural di waktu event
   └─► subtitle: .srt + caption yang di-burn
mix (ducking, kompresi, keseimbangan) ──► mux dengan ffmpeg, loudnorm dua tahap −14 LUFS ──► film.mp4
```

## 1. Kebutuhan dan instalasi

Alat sistem, yang dipasang user: **Node 20+**, **ffmpeg 7+** (versi 6.x melaporkan durasi audio terlalu pendek lewat `loudnorm`, lalu `mux.sh` menolak file karena dianggap terpotong), dan **Python 3.11+** atau [uv](https://docs.astral.sh/uv/). Dikembangkan di macOS (Apple silicon); Linux seharusnya jalan. Di Windows, Git Bash (bagian dari Git for Windows) bisa dipakai: jalankan perintah `sh` yang sama di sana; WSL juga bisa. Gaya 3D dan yang berat shader sebaiknya pakai GPU.

Selebihnya dipasang bertingkat, dari root library (`$LIB` dalam mode skill). Pasang satu tingkat hanya saat film membutuhkannya:

| Perintah | Menambahkan | Ukuran |
|---|---|---|
| `sh plugin/skills/code-cinema-by-megabagus/scripts/setup.sh deps` | inti: paket npm, headless browser, Python `.venv` (numpy, scipy, soundfile, soxr, pillow): render, sintesis suara, mux | ~350 MB |
| `… setup.sh deps voice` | Kokoro + model (Inggris, offline), edge-tts (Mandarin, Indonesia, dan bahasa lain, online), faster-whisper (pemeriksaan suara) | ~0,55 GB + model Whisper saat pemeriksaan pertama (~145 MB untuk Inggris, ~480 MB untuk bahasa lain) |
| `… setup.sh deps music` | numba, untuk senar petik (`pluck.py`); sampler sendiri hanya butuh inti | ~140 MB |
| `sh tools/fetch.sh instruments <lib>` | satu pustaka sampel: `freepats`, `karoryfer`, `salamander`, `vcsl`, `vsco2ce`, atau `all` | 70–400 MB masing-masing |
| `sh tools/fetch.sh hdri` | HDRI untuk gaya 3D | 12 MB |

Beberapa gaya butuh paket sendiri (pembaca LiDAR, decoder slide-scan, importer CAD); `STYLE.md` gaya itu mencantumkannya. Itu paket, bukan alat sistem: pasang sendiri ke venv privat atau `node_modules` di folder proyek, jangan pernah ke `$LIB/.venv`.

Gaya bertanda ✦ juga menggambar dengan generator gambar, yang tidak disertakan library dan tidak Anda pasang: Codex CLI milik user yang sudah login (`core/image/gen_image.py`), atau alat gambar lain yang mereka punya. Prompt dikirim ke layanan itu (core/README.md, "Image generation").

Score hasil sintesis tidak butuh unduhan besar. Score bersampel butuh pustaka tempat instrumennya berada: `sampler.py` mengunduh yang belum ada sendiri, sekaligus, saat score di-render (`CC_FETCH=0` mematikannya dan menampilkan perintah `fetch.sh` sebagai gantinya). Taruh `"$LIB/.venv/bin/python" core/audio/sampler.py --need <mix.py Anda>` di awal `build.sh`, supaya pustaka tiba sebelum render gambar yang lama, bukan sesudahnya. Satu paket butuh ruang kosong sekitar dua kali ukurannya saat dibongkar. Unduhan berasal dari npm, PyPI, GitHub Releases repo ini, dan Hugging Face (`HF_ENDPOINT` mengatur mirror).

## 2. Gambar adalah fungsi waktu

Setiap film adalah folder dengan `index.html` (`<demo>` di perintah-perintah) yang menyediakan:

```js
window.DUR = 54.2;                 // detik
window.render = (t) => { ... };    // gambar frame pada waktu t, deterministik
window.READY = true;               // diset setelah font dan gambar termuat
window.EV = [{t, type, ...}];      // opsional: event suara / cue untuk mixer
window.TEXTS = (t) => [{id, text, x0, y0, x1, y1}];   // opsional: semua teks yang terlihat pada t, untuk readcheck (pass: true = tidak dimaksudkan dibaca penuh: papan yang lewat, kredit huruf kecil)
```

**Path:** halaman mengakses file library dengan URL absolut (`/core/lib.js`, `/node_modules/three/build/three.module.js`); script dan `build.sh` memakai `$LIB`. Jangan pernah `../..`.

`build.sh` yang bekerja di kedua mode (dalam mode skill, taruh `LIB=<path yang dicetak setup.sh>` di baris atas):

```sh
#!/bin/sh
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-$(cd "$HERE/../.." && pwd)}          # mode clone: <repo>/films/<nama>/
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
cd "$LIB"
node core/render/events.mjs "$HERE"
node core/render/video.mjs "$HERE" --fps 24 --out "$HERE/out/video.mp4"
"$LIB/.venv/bin/python" "$HERE/mix.py"                               # score, foley, suara → out/mix.wav
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/<nama>.mp4" 24
```

Aturan yang membuatnya andal:

- **Deterministik.** Tanpa `Date.now()`, tanpa `Math.random()` tanpa seed (`core/lib.js` punya `mulberry` dan `hash`), tanpa state yang terbawa dari frame sebelumnya. Frame mana pun bisa di-render sendiri, dalam urutan apa pun, oleh worker mana pun.
- **Canvas 2D** untuk sebagian besar gaya 2D; **three.js** untuk 3D (§9); shader **WebGL2** untuk post pass (kerusakan film, CRT, gambar ulang tinta).
- **Animasi "on twos" bila gayanya menghendaki** (langkah 12 fps untuk tampilan stop-motion, piksel, atau cel), tapi kamera dan cahaya tetap halus di setiap frame. Kamera yang patah-patah terbaca sebagai lag.
- **Satu fungsi world → screen.** Setiap efek yang mengikuti subjek (iris, zoom, spotlight) melewati fungsi ini. Jangan pernah mengetik koordinat layar secara manual.
- **Gambar untuk frame yang Anda render.** Default 1920×1080; untuk ukuran lain berikan `--size WxH` (mis. `1080x1920`) ke setiap alat render dan susun halaman dari `innerWidth` × `innerHeight`.

Capture (`core/render/`; film di atas 60 detik dirender per chunk dengan `chunks.mjs`, §13):

```sh
node core/render/still.mjs <demo> 1.5 12 --range 0:50:2   # still untuk review; berhenti jika ada error halaman
node core/render/video.mjs <demo> --fps 24 --workers 3     # semua frame → <demo>/out/video.mp4
node core/render/events.mjs <demo>                         # ekspor DUR + EV → events.json
node core/render/readcheck.mjs <demo>                      # setiap teks di layar tampil cukup lama untuk dibaca
```

Untuk me-render versi kedua dengan konten lain, berikan ke halaman dan beri output sendiri: `--q 'content=content_alt.json' --out …/alt.mp4` (sama untuk `events.mjs`).

Capture cepat karena **screenshot JPEG**, **satu browser per worker**, dan **grain ditambahkan di ffmpeg**: grain yang digambar di halaman membuat setiap frame tidak bisa dikompres dan lambat.

## 3. Satu timeline menggerakkan semuanya

Simpan bagian, tempo, beat, dan titik hit dalam satu file (`timeline.js`). Ekspor ke JSON dan biarkan score, mixer, subtitle, dan pemeriksaan membaca angka yang sama:

```js
export const SECS = [{ id: 'chase', t: 12.0, bpm: 144, beats: 12 }, ...];
export const HIT  = { pratfall: ['chase', 6], ... };   // bagian + beat
```

Script kecil (`cuecheck.py`, di `styles/<slug>/demo/tools/` beberapa demo) membandingkan setiap hit visual dengan cue musik tempat ia seharusnya jatuh. Targetkan 0 ms.

## 4. Suara

- **TTS hanya default.** Jika user membawa rekaman atau menyebut suara tertentu, pakai itu. Jika tidak:
  - **Inggris**: [Kokoro](https://github.com/thewh1teagle/kokoro-onnx), lokal, banyak suara (nama `voice` yang tidak dikenal membuat `tts.py` menampilkan daftar lengkap; `af_` / `am_` Amerika, `bf_` / `bm_` Inggris; pilih narator untuk film ini, bukan narator demo). `core/tts/tts.py lines.json out/` menulis satu WAV per kalimat dan file durasi. Suara Mandarinnya (`"lang": "cmn"`) bekerja offline tapi terdengar datar.
  - **Mandarin**: `core/tts/tts_zh.py lines.json out/` memakai [edge-tts](https://github.com/rany2/edge-tts) dengan suara neural Microsoft (`zh-CN-XiaoxiaoNeural`, `zh-CN-YunxiNeural`…), dengan output yang sama seperti `tts.py`, kecepatan per kalimat, dan hening yang dipangkas. **Butuh koneksi internet.**
  - **Bahasa Indonesia dan bahasa lain**: script yang sama membaca bahasa lain juga. Untuk Indonesia: `core/tts/tts_zh.py lines.json out/ --voice id-ID-GadisNeural` (perempuan) atau `id-ID-ArdiNeural` (laki-laki), atau isi field `"voice"` per kalimat. Daftar suara: `python -m edge_tts --list-voices`. **Butuh koneksi internet**; cek sendiri ketentuan Microsoft sebelum memakai suaranya untuk keperluan komersial. Untuk pemeriksaan, `asr_check.py --lang id`.
- Tulis angka dengan huruf di teks TTS dan dengan digit di subtitle.
- **Periksa setiap kalimat**: `core/tts/asr_check.py` mentranskripsi setiap WAV dengan faster-whisper dan membandingkannya dengan naskah (`--lang zh`: angka dibandingkan berdasarkan nilai, jadi 十九 cocok dengan 19, sisanya karakter per karakter); generate ulang sampai keluar dengan kode 0. Satu karakter salah dengar di kalimat Mandarin pendek itu wajar: dengarkan, dan jika benar, isi field `asr` kalimat itu dengan yang didengar model. Script ini juga menulis timestamp per kata untuk menempatkan kalimat dan subtitle.
- **Sebelum mixing**: TTS punya rasio puncak-ke-rata-rata yang tinggi. Kompres suaranya dulu, lalu seimbangkan dengan RMS: suara sekitar 10 dB di atas musik.

## 5. Musik

Tulis score orisinal dari cue map, dengan instrumen dari palet suara gaya itu; tanpa piano dan string generik.

- **Sampel**: `core/audio/sampler.py` memainkan instrumen nyata dari pustaka gratis (VSCO 2 CE, VCSL, FreePats, Karoryfer, Salamander Grand Piano; daftar dan lisensi di `core/audio/INSTRUMENTS.md`). Tulis score sebagai event `(waktu, instrumen, nada, durasi, velocity, pan)`. Nada panjang diperpanjang tanpa sambungan, dan round-robin menghindari efek senapan mesin.
- **Senar petik dan senar tradisional** (guqin, pipa, shamisen, banjo, juga cocok untuk kecapi atau sasando): `core/audio/pluck.py`, pemodelan fisik (Karplus–Strong) dengan bend dan vibrato.
- **Sintesis** dengan numpy untuk chip tune, drone, dan efek; tidak perlu unduhan.
- **Seimbangkan frekuensi rendah.** Score sintetis cepat menjadi terlalu berat di bass. Ukur energi per band setelah mixing; jaga 20–120 Hz sekitar −3 dB relatif terhadap sisanya, hindari nada pad di bawah MIDI 48, dan beri bass sedikit harmonik ke-2 dan ke-3 supaya terdengar di speaker kecil.

## 6. Efek suara dan mix

- `core/audio/sfx.py` menyintesis foley secara prosedural (klik, whoosh, dentum, ding, kertas, lapisan noise…) dengan filter, envelope, dan `add(buffer, sound, at, gain, pan)`. Gerakkan dari `window.EV`, supaya setiap suara jatuh tepat di frame-nya.
- **Master**: `sh core/render/mux.sh video.mp4 mix.wav out.mp4 24 [grain]` menggabungkan (mux), menjalankan loudnorm dua tahap ke −14 LUFS dengan batas true-peak, menambahkan grain di ffmpeg, dan menampilkan loudness terukur; keluar dengan kode bukan nol jika ada kegagalan. Di latar terang pakai grain lebih sedikit; untuk gaya piksel dan vektor, tanpa grain.
- Film dengan grain yang tertanam di gambar terkompres buruk; encode ulang dengan `-tune grain` dan CRF lebih tinggi.

## 7. Subtitle

- Ekspor `.srt` dengan `core/render/srt.py cues.json out.srt` (cues = `[{t0, t1, text}]`), dan burn caption bergaya ke halaman itu sendiri: desain caption adalah bagian dari gaya.
- Aturan timing ada di DIRECTOR.md §7.

## 8. Loop review

1. Contact sheet: satu frame setiap 1–2 detik dengan `still.mjs --range`, disusun dengan `core/render/sheet.py`. Minimal dua kali penuh.
2. Strip frame per 0,2 detik untuk setiap aksi kunci: serah-terima, jatuh, pukulan.
3. Pada file akhir: `ffmpeg -af ebur128` (loudness), `blackdetect` (frame kosong), whisper lagi pada mix akhir jika ada suara.
4. Tonton sekali, dengan kecepatan penuh, dengan suara.

## 9. Catatan 3D

- three.js r170 di-render headless lewat WebGL2 di GPU; depth of field fisik dan GTAO dari `core/three/post.js`, di-render 2× lalu diperkecil.
- Pencahayaan: area light lembut ditambah HDRI Poly Haven berintensitas rendah terbaca lebih "nyata" daripada ambient light yang terang.
- `core/three/post.js` ditulis untuk kamera perspektif. Untuk kamera ortografis, ganti `perspectiveDepthToViewZ` dengan `orthographicDepthToViewZ` di depth pass-nya, atau depth of field rusak tanpa peringatan.

## 10. Karakter yang digambar dengan kode

- Rig 2.5D (torso, kepala, anggota badan dihitung per frame) cukup untuk pantomim.
- Urutkan rotasi bahu sebagai abduksi, lalu fleksi; urutan terbalik membuat lengan yang terangkat bersilang menjadi X.
- Biarkan bahu naik dan maju saat lengan terangkat, dan jangan memberi outline pada bagian lengan yang menumpuk dengan torso: garis itulah yang membuat sendi terlihat seperti sambungan boneka.

## 11. Aset, kredit, dan font

Hanya materi CC0, CC BY, atau OFL, masing-masing dicantumkan di `CREDITS` film dengan sumber dan lisensinya; `core/audio/sampler.py credits(names)` menulis baris untuk instrumen yang Anda pakai. Karya domain publik dihitung sebagai CC0; "no known restrictions" tidak. Data atau gambar dengan lisensi terbuka lain (ODbL, CC BY-SA, lisensi open-hardware) hanya setelah Anda menyebut lisensi dan syaratnya (atribusi, share-alike) ke user dan mereka setuju. Materi milik user boleh dipakai apa adanya. Gambar dari generator gambar (gaya ✦) juga dicantumkan: alat dan model yang membuatnya, bahwa gambar itu hasil generate, dan di mana prompt-nya disimpan; gambar yang dibuat user dikreditkan kepada mereka.

Film yang menyatakan fakta (gaya yang dibangun dari data atau pindaian nyata: disebut di `STYLE.md`-nya) menyimpan `FACTS.md` di folder proyek: setiap klaim dengan URL sumber dan kutipan kalimatnya, atau pengukuran yang menghasilkannya.

Font: Google Fonts (OFL), di-host sendiri di proyek. Typeface yang disebut `STYLE.md` tidak ada di library; unduh (`https://github.com/google/fonts/tree/main/ofl/<family>`) ke folder `fonts/` proyek. `core/fonts/` berisi beberapa font display Latin dan satu font display Mandarin dengan hanya sekitar 200 glyph, tidak cukup untuk teks Mandarin panjang. Untuk Mandarin, subset font CJK ke karakter yang Anda pakai: Google Fonts CSS API dengan `&text=` hanya mengembalikan glyph itu (`https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@700&text=<karakter yang di-URL-encode>`). Unduh file font yang ditunjuknya ke `fonts/` proyek dan muat dengan `@font-face`; jangan menautkan Google Fonts saat render.

## 13. Film panjang (sampai 20 menit)

Kategori durasi dan strukturnya ada di DIRECTOR.md §1. Di sini cara membangunnya supaya film 20 menit tetap rapi, deterministik, dan bisa dirender tanpa takut terputus.

**Susunan kode.** Satu folder proyek, satu halaman, satu `render(t)`, tapi kodenya dipecah:

```
<proyek>/
  timeline.js          # menggabungkan bab: SECS, SUBS, EV global; DUR dari rekaman
  timeline/bab01.js …  # satu file per bab (film > 5 menit: per babak, berisi bab-babnya)
  scenes/              # pustaka adegan: fungsi (ctx, t_lokal, data) untuk tiap jenis adegan
  vo/bab01/ …          # lines.json dan WAV per bab
```

- `render(t)` mencari bab aktif dari `t` (pencarian biner pada waktu mulai bab), lalu memanggil adegan bab itu dengan waktu lokal. Tetap deterministik: tanpa state antar frame, angka acak dari seed ID elemen.
- Setiap bab bisa diuji sendiri: `still.mjs <proyek> --range <awal>:<akhir>:2` untuk rentang bab itu, sebelum bab berikutnya ditulis. Film > 5 menit dibangun dan diuji **per babak**: selesaikan babak 1 (gambar, suara, subtitle) sebelum menulis babak 2.
- Aset besar (font, tekstur, HDR) dimuat sekali sebelum `READY`, dan tingkat skala gambar besar di-cache sekali, bukan per frame.

**Suara per bab.** Naskah di `NASKAH.md` dikelompokkan per bab; kalimat diberi ID bab (`b01_v01`, `b01_v02`, …). Rekaman user untuk film > 5 menit datang satu file per bab (`bab01.wav`, `bab02.wav`, …): periksa tiap file dengan `asr_check.py`, sambung dengan jeda ±0,7 detik, dan jadikan offset tiap file sebagai waktu mulai bab di timeline. TTS dibuat per bab dengan suara dan pengaturan yang sama persis; jangan membuat ulang satu bab dengan pengaturan lain.

**Musik.** Satu cue per bab atau per babak, dari palet instrumen yang sama, dengan transisi di pergantian bab (crossfade 1–2 detik atau satu hening musik). Tulis score per babak ke stem terpisah (`music/babak1.wav`, …) lalu sambung; satu array numpy untuk 20 menit stereo 48 kHz float64 makan ±0,9 GB memori. Musik di-duck di bawah suara sepanjang film. Untuk film > 5 menit boleh 2–3 tema yang bergantian per babak.

**Render: `core/render/chunks.mjs`.** Film di atas 60 detik dirender per chunk, bukan dengan `video.mjs` sekali jalan:

```sh
# render uji: chunk pertama dan satu di tengah, periksa, lalu perkirakan waktu dari frames/s yang dicetak
node core/render/chunks.mjs "$HERE" --fps 24 --only 1,20 --out "$HERE/out/video.mp4"
# render penuh: chunk yang sudah jadi dilewati, lalu semuanya disambung tanpa re-encode dan jumlah frame dicek
node core/render/chunks.mjs "$HERE" --fps 24 --out "$HERE/out/video.mp4"
# setelah mengubah adegan bab 3 (mis. chunk 7–9): render ulang chunk itu saja
node core/render/chunks.mjs "$HERE" --fps 24 --redo 7,8,9 --out "$HERE/out/video.mp4"
```

- Chunk default 30 detik (`--chunk`), disimpan di `out/video.chunks/`. Jika proses berhenti (sesi berakhir, komputer tidur, error halaman), jalankan perintah yang sama lagi: render lanjut dari chunk yang belum ada. Pengaturan yang berubah (durasi, fps, ukuran) ditolak dengan pesan, supaya chunk lama tidak tercampur; mulai ulang dengan `--fresh`.
- **Di sesi cloud**, proses background biasanya dihentikan beberapa menit setelah balasan selesai. Jalankan render di foreground dalam putaran berulang, `timeout 580 node core/render/chunks.mjs …`, sampai mencetak `done`; setiap putaran menyimpan chunk yang selesai. Laporkan progres per putaran ke user (chunk ke berapa dari berapa, perkiraan sisa waktu).
- Di komputer user, `build.sh` film panjang memanggil `chunks.mjs` alih-alih `video.mjs`; sisanya sama (mix → `mux.sh`).
- Jangan menurunkan resolusi, menaikkan CRF, atau menyederhanakan animasi di bab akhir demi mengejar waktu render. Jika waktu atau disk tidak cukup (sediakan ±2 GB untuk film 20 menit pada 1080p), laporkan dan minta keputusan.
- Jangan menyerahkan film setengah jadi sebagai film final. Hapus `out/video.chunks/` setelah film final diperiksa.

**Pemeriksaan.** `chunks.mjs` sudah mencocokkan jumlah frame setiap chunk dan film gabungannya. Selebihnya ada di DIRECTOR.md §11: loudness per bab (`ffmpeg -af ebur128` pada potongan per bab), sinkron di setiap awal bab, contact sheet per babak, `blackdetect` dan `freezedetect`.

## 12. Di mana mencari di demo kami

| Jika Anda butuh… | Lihat |
|---|---|
| animasi karakter 2D dan lip sync | `styles/scifi-toon/`, `styles/cel-anime-80s/` |
| score berbasis timeline dengan pemeriksaan cue | `styles/microgame/`, `styles/silent-film/` |
| gambar ulang gambar-ke-tinta dan post pass kerusakan film | `styles/silent-film/demo/engine/` |
| mesin kuas atau goresan | `styles/watercolor/`, `styles/ink-wash/`, `styles/impasto/` |
| 3D dengan depth of field dan material nyata | `styles/brick-toy/`, `styles/paper-popup/` |
| tampilan CRT atau VHS | `core/post/crt.js`, `styles/ascii-crt/`, `styles/backrooms/` |

`DEMO.md` setiap gaya menjelaskan cara demonya dibangun. Buka file itu dan kodenya hanya setelah treatment Anda ada, untuk mempelajari teknik, jangan pernah untuk membangun ulang film kami (alat materi gaya Edit & Documentary di `demo/tools/` didahulukan: AGENTS.md, "Treatment dulu"). Dalam mode skill, ambil source-nya dengan `sh <folder skill>/scripts/setup.sh demo <slug>`. Kode demo yang disalin sering mengakses library dengan `../..`: ganti dengan `$LIB` atau URL absolut.
