---
name: code-cinema-by-megabagus
description: Menyutradarai dan memproduksi film 30 detik sampai 60 menit yang dibuat sepenuhnya dengan kode (tanpa video model), dalam salah satu dari 99 gaya film Code Cinema (mis. Impasto Oil Painting, Watercolor Brush, Ukiyo-e, Satellite Briefing, Exploded Teardown). Gunakan saat user meminta video, film pendek, promo, explainer, atau animasi sinematik dengan gaya tertentu, termasuk explainer dari materi nyata (citra satelit, pemindaian laser, file CAD, arsip) dan film yang disusun dari rekaman dan dokumen arsip; saat user ingin film tentang topiknya tapi belum memilih gaya (bantu pilih); saat user ingin mengubah gaya menjadi miliknya, membuat gaya sendiri dari nol, atau memakai gaya yang sudah ia simpan; saat skill dipanggil tanpa permintaan; atau saat user bertanya gaya film apa saja yang ada. Bukan untuk sekadar mengedit, memotong, atau mengonversi video milik user. Berbahasa Indonesia.
---

# Code Cinema by Megabagus

Gaya, panduan, dan alat produksi ada di library Code Cinema (github.com/pendekarAI/code-cinema). Skill ini mengambil library tersebut dan menyerahkan alur kerjanya ke panduan di dalamnya. Komunikasi dengan user dalam Bahasa Indonesia, kecuali user memilih bahasa lain.

1. **Siapkan library.** Jalankan `sh "<folder dasar skill>/scripts/setup.sh"`. Perintah ini meng-clone atau memperbarui library (default `~/code-cinema`; clone yang sedang ditempati user dipakai apa adanya), menampilkan alat sistem yang belum ada (Node, ffmpeg, Python), dan mencetak `LIB=<path>` di baris terakhir.
2. **Pasang alat inti sejak awal.** Segera jalankan `sh "<folder dasar skill>/scripts/setup.sh" deps`, di background jika bisa: pertama kali butuh beberapa menit. Tambahkan `deps voice` atau `deps music` belakangan, hanya jika film membutuhkannya (`$LIB/TECHNIQUE.md` §1). Laporkan alat sistem yang belum ada (Node 20+, ffmpeg 7+, Python 3.11+ atau uv) dalam satu putaran pertanyaan; jangan memasang software sistem sendiri. Gaya bertanda ✦ juga butuh generator gambar yang disediakan user (`$LIB/AGENTS.md`, Alur kerja, Brief). Paket yang dibutuhkan sebuah gaya (tercantum di `STYLE.md`-nya) dipasang sendiri, ke folder proyek.
3. **Ikuti panduan library.** Baca `$LIB/AGENTS.md` dan kerjakan sesuai isinya, mulai dari bagian **Mulai** (gaya milik user di `~/code-cinema-styles/`; jika skill dipanggil tanpa permintaan, tanyakan bahasa dulu, lalu pilihan jalurnya): mencari gaya atau membuat gaya sendiri, satu putaran pertanyaan, treatment, produksi, dan penyerahan hasil.

4. **Naskah dulu, baru voice over.** Tepat setelah gaya jelas, tanyakan dalam satu `AskUserQuestion`: **durasi** (30–60 detik, 1–5 menit, 5–20 menit, atau Layar Lebar 20–60 menit), **gaya naskah** (Edukatif, Formal / profesional, Santai / gaul, Storytelling, atau lainnya) dan **voice over** (rekam suara sendiri, suara AI hanya jika uji edge-tts di sesi ini berhasil, atau tanpa voice over). Lalu tulis naskahnya (`NASKAH.md`, `NASKAH.txt`, dan `vo/lines.json`), kirim ke user sebagai tabel per kalimat, diikuti blok **Naskah siap salin** (naskah utuh dalam satu blok kode) dan file `NASKAH.txt` yang bisa diunduh, beserta panduan rekam dan pertanyaan brief, tunggu persetujuan dan file rekamannya, dan susun timing film dari rekaman itu. Detail: `$LIB/AGENTS.md`, Alur kerja langkah 1.
5. **Film panjang (di atas 60 detik, maksimal 20 menit).** Ikuti kategori durasi di `$LIB/DIRECTOR.md` §1: naskah per bab (di atas 5 menit per babak dengan rekap mini), rekaman per bab, kode per bab dengan pustaka adegan, dan render per chunk yang bisa dilanjutkan dengan `node core/render/chunks.mjs` (`$LIB/TECHNIQUE.md` §13). Sampaikan sejak awal bahwa film di atas 3 menit butuh waktu jauh lebih lama dan bisa berlanjut dalam beberapa putaran; di sesi cloud, jalankan render di foreground dalam putaran `timeout 580` berulang sampai selesai.
6. **Layar Lebar (di atas 20 menit, maksimal 60 menit).** Bagi film menjadi 2–3 bagian (≤ 20 menit, dipotong di titik alami), masing-masing diproduksi seperti film Sangat panjang di subfolder `bagian1/`, `bagian2/`, … dengan gaya bersama di `shared/`. Selesaikan dan kirim satu bagian sebagai pratinjau sebelum membangun bagian berikutnya, catat status di `PROGRES.md` agar bisa dilanjutkan di sesi lain, lalu sambung dengan `sh core/render/join.sh <nama>.mp4 bagian1/bagian1.mp4 … --chapters CHAPTERS.txt`. Di atas 60 menit, tawarkan seri video terpisah. Detail: `$LIB/DIRECTOR.md` §1 dan `$LIB/TECHNIQUE.md` §13.

Yang berbeda dalam mode skill:

| | |
|---|---|
| Folder proyek | `<nama>/` di folder tempat user memulai (huruf kecil, angka, tanda hubung; hindari `#` dan `?` di path). Setiap kali panduan menyebut `films/<nama>/`, artinya folder ini |
| Menjalankan alat | dari `$LIB`, dengan path absolut proyek: `cd "$LIB" && node core/render/still.mjs "<proyek>" 1.5 3` |
| File library di halaman | URL absolut: `/core/lib.js`, `/node_modules/three/…` (proyek disajikan di `/@film/`) |
| File library di script dan `build.sh` | `$LIB/…`, dengan `LIB=<path>` di baris atas `build.sh`; jangan pernah `../..` |
| Source demo | tidak diunduh. `sh "<folder dasar skill>/scripts/setup.sh" demo <slug>`, hanya setelah `TREATMENT.md` ditulis, untuk mempelajari tekniknya; bukan untuk dirender. Pengecualian: gaya Edit & Documentary, ambil sebelum treatment untuk memakai alat materi yang disebut `STYLE.md`-nya di `demo/tools/` (`$LIB/AGENTS.md`, "Treatment dulu") |

Serahkan semua yang tercantum di `$LIB/DIRECTOR.md` §11 di folder proyek, lalu beri tahu user lokasinya.
