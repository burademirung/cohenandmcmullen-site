#!/bin/bash
# Encodes the image-first (photoreal) Runway 4K masters into web films + posters.
# Usage: scripts/transcode-real.sh <folder with "Gen-4_5 - ... 4K.mp4" files>
set -e
SRC="$1"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"
V="$ROOT/site/assets/video"; P="$ROOT/site/assets/img/film"
map() { case "$1" in
 *"cracked steel part"*) echo forensic;; *"black metal card"*) echo card;; *"black king"*) echo chess;;
 *"conference table"*) echo evidence;; *"sword blade"*) echo sword;; *"courthouse columns"*) echo courthouse;;
 *"boardroom table"*) echo boardroom;; *"gold crest on the navy wall"*) echo crest;; *) echo "";; esac; }
for f in "$SRC"/Gen-4_5*4K.mp4; do
  b=$(basename "$f"); k=$(map "$b"); [ -z "$k" ] && continue
  ffmpeg -loglevel error -y -i "$f" -an -vf "scale=1920:-2,format=yuv420p" -c:v libx264 -preset slow -crf 27 -maxrate 2200k -bufsize 4400k -movflags +faststart -profile:v high "$V/$k.mp4"
  ffmpeg -loglevel error -y -i "$f" -an -vf "scale=960:-2,format=yuv420p" -c:v libx264 -preset slow -crf 29 -maxrate 520k -bufsize 1040k -movflags +faststart "$V/$k-sm.mp4"
  ffmpeg -loglevel error -y -ss 0.4 -i "$f" -frames:v 1 -vf "scale=1920:-2" "$P/$k.png"
  cwebp -quiet -q 80 "$P/$k.png" -o "$P/$k.webp"; cwebp -quiet -q 76 -resize 960 0 "$P/$k.png" -o "$P/$k-sm.webp"; rm "$P/$k.png"
  echo "done $k"
done
