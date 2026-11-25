#!/bin/sh
# Join finished parts into one long film: join.sh out.mp4 part1.mp4 part2.mp4 … [--chapters CHAPTERS.txt]
# For films above 20 minutes (DIRECTOR.md §1, "Layar Lebar"): each part is a finished film of its own (≤ 20 min, made by mux.sh),
# and this joins them without re-encoding. It checks that every part has the same picture size, frame rate, codecs and audio
# format first, writes to a temporary file and renames it only when the joined film is complete, then reports the duration
# (against the sum of the parts) and the loudness of the whole film.
# --chapters: a text file with one chapter per line, "00:00 Title", "1:02:03 Title" (the same file the delivery hands over);
# the chapters are written into the mp4 so players show them. Times are for the whole film.
LC_ALL=C; export LC_ALL
die() { echo "join.sh: $*" >&2; exit 1; }
command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null || die "ffmpeg and ffprobe are needed and aren't on PATH"
O="$1"; [ -n "$O" ] || die "usage: sh core/render/join.sh out.mp4 part1.mp4 part2.mp4 … [--chapters CHAPTERS.txt]"; shift
CH=""; N=0; LIST=$(mktemp); TMP=""; META=""
trap 'rm -f "$LIST" "$META" ${TMP:+"$TMP"}' EXIT INT TERM
REF=""; SUM=0
while [ $# -gt 0 ]; do
  case "$1" in
    --chapters) CH="$2"; [ -f "$CH" ] || die "chapters file not found: $CH"; shift 2; continue;;
  esac
  P="$1"; [ -f "$P" ] || die "part not found: $P"
  AP=$(cd "$(dirname "$P")" && pwd)/$(basename "$P")
  F=$(ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels -of csv=p=0 "$AP" | sort | tr '\n' ' ')
  [ -n "$F" ] || die "cannot read $P"
  case "$F" in *video*) ;; *) die "$P has no video stream";; esac
  case "$F" in *audio*) ;; *) die "$P has no audio stream (join finished parts made by mux.sh)";; esac
  if [ -z "$REF" ]; then REF="$F"; RP="$P"; elif [ "$F" != "$REF" ]; then
    die "$P does not match $RP:
  $RP: $REF
  $P: $F
Render and mux every part with the same size, fps and settings."
  fi
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AP"); SUM=$(awk -v a="$SUM" -v b="$D" 'BEGIN{print a+b}')
  printf "file '%s'\n" "$(printf %s "$AP" | sed "s/'/'\\\\''/g")" >> "$LIST"; N=$((N + 1))
  shift
done
[ "$N" -ge 2 ] || die "give at least two parts"

# chapters → ffmetadata
if [ -n "$CH" ]; then
  META=$(mktemp)
  awk -v total="$SUM" '
    BEGIN { print ";FFMETADATA1"; n = 0 }
    /^[ \t]*$/ { next }
    match($0, /^[ \t]*[0-9]+(:[0-9]+){1,2}[ \t]+/) {
      t = substr($0, RSTART, RLENGTH); title = substr($0, RLENGTH + 1); gsub(/[ \t]/, "", t)
      k = split(t, p, ":"); s = 0; for (i = 1; i <= k; i++) s = s * 60 + p[i]
      n++; st[n] = s; ti[n] = title; next }
    { printf "join.sh: chapters line ignored (no time at the start): %s\n", $0 > "/dev/stderr" }
    END {
      for (i = 1; i <= n; i++) {
        e = (i < n) ? st[i + 1] : total
        if (e <= st[i]) { printf "join.sh: chapter %d (%s) does not start before the next one\n", i, ti[i] > "/dev/stderr"; exit 1 }
        gsub(/[=;#\\]/, "\\\\&", ti[i])
        printf "[CHAPTER]\nTIMEBASE=1/1000\nSTART=%d\nEND=%d\ntitle=%s\n", st[i] * 1000, e * 1000, ti[i] }
    }' "$CH" > "$META" || die "fix the chapters file: $CH"
fi

mkdir -p "$(dirname "$O")"
TMP="$(dirname "$O")/.join_$$.mp4"
if [ -n "$META" ]; then
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -i "$META" -map 0 -map_metadata 1 -map_chapters 1 -c copy -movflags +faststart "$TMP" || die "ffmpeg could not join the parts (its message is above)"
else
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -map 0 -c copy -movflags +faststart "$TMP" || die "ffmpeg could not join the parts (its message is above)"
fi
[ -s "$TMP" ] || die "the joined file is empty"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP")
OFF=$(awk -v a="$D" -v b="$SUM" -v n="$N" 'BEGIN{d=a-b; if (d<0) d=-d; print (d > 0.1*n) ? "bad" : "ok"}')
[ "$OFF" = ok ] || die "the joined film lasts ${D}s but the parts add up to ${SUM}s; the parts are untouched"
mv "$TMP" "$O"; TMP=""
L=$(ffmpeg -hide_banner -nostats -i "$O" -map 0:a:0 -af ebur128=peak=true -f null - 2>&1 | awk '/Integrated loudness:/{f=1} f&&/ I:/{i=$2} f&&/Peak:/{p=$2} END{print i, p}')
set -- $L
echo "joined $N parts → $O  $(awk -v d="$D" 'BEGIN{printf "%d:%02d:%02d", d/3600, (d%3600)/60, d%60}')  (parts add up to ${SUM}s)  loudness ${1} LUFS, true peak ${2} dBFS${META:+, chapters written}"
awk -v i="$1" 'BEGIN{ if (i+0 < -15 || i+0 > -13) print "join.sh: the whole film is outside −14 ±1 LUFS; mux every part with mux.sh so each one sits at −14" > "/dev/stderr" }'
