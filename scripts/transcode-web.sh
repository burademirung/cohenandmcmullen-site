#!/bin/bash
set -e
V=../site/assets/video; P=../site/assets/img/film; mkdir -p $V $P
map() { case "$1" in
 *"empty grand American courtroom"*) echo courtroom;; *"federal courth"*) echo courthouse;; *"walnut boardroom"*) echo boardroom;;
 *"fountain pen"*) echo pen;; *"soft rain streaming"*) echo lily;; *"emergency lights"*) echo lights;; *"forensic"*) echo forensic;;
 *"antique steel sword"*) echo sword;; *"law library"*) echo library;; *"Fort Lauderdale"*) echo fort-lauderdale;;
 *"Fifth Avenue"*) echo new-york;; *"Los Angeles"*) echo los-angeles;; *"private corner law office"*) echo office;;
 *"credit card"*) echo card;; *"chess king"*) echo chess;; *"legal evidence"*) echo evidence;; *"heraldic crest"*) echo crest;; *) echo "";; esac; }
for f in Gen-4_5*4K.mp4; do
  k=$(map "$f"); [ -z "$k" ] && { echo "UNMAPPED: $f"; continue; }
  
  ffmpeg -loglevel error -y -i "$f" -an -vf "scale='min(1920,iw)':-2,format=yuv420p" -c:v libx264 -preset slow -crf 27 -maxrate 2200k -bufsize 4400k -movflags +faststart -profile:v high "$V/$k.mp4"
  ffmpeg -loglevel error -y -i "$f" -an -vf "scale=960:-2,format=yuv420p" -c:v libx264 -preset slow -crf 29 -maxrate 520k -bufsize 1040k -movflags +faststart "$V/$k-sm.mp4"
  ffmpeg -loglevel error -y -ss 0.5 -i "$f" -frames:v 1 -vf "scale='min(1920,iw)':-2" "$P/$k.png"
  cwebp -quiet -q 78 "$P/$k.png" -o "$P/$k.webp"; cwebp -quiet -q 75 -resize 960 0 "$P/$k.png" -o "$P/$k-sm.webp"; rm "$P/$k.png"
  echo "done $k"
done
