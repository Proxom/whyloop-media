#!/bin/bash
# Final encode (AGENT.md 5.1): PNG frames + mastered audio -> 1080x1920 H.264 High yuv420p CRF 18 + AAC 48 kHz, faststart.
# usage: encode.sh <frames dir with f%04d.png> <audio.wav> <out.mp4> <duration s> [fps=30]
set -e; D=$1; A=$2; O=$3; T=$4; FPS=${5:-30}
ffmpeg -loglevel error -y -framerate $FPS -i "$D/f%04d.png" -i "$A" -map 0:v -map 1:a -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high \
  -movflags +faststart -c:a aac -b:a 192k -ar 48000 -t "$T" "$O"
ls -la "$O"
