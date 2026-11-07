#!/bin/bash
# HARD GATE technical + look QC. usage: qc_video.sh reel.mp4 outdir
# Prints stream facts, black first/last frame check, exports 6 stills (0/20/40/60/80/100 %) + 0.5 s frame with safe zones drawn, and a contact sheet.
set -e; F=$1; O=$2; mkdir -p "$O"
ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels -show_entries format=duration -of compact "$F"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
for p in 0 20 40 60 80 100; do T=$(python3 -c "print(max(0,min($D-0.04,$D*$p/100)))"); ffmpeg -loglevel error -y -ss $T -i "$F" -frames:v 1 "$O/still_$p.png"; done
ffmpeg -loglevel error -y -ss 0.5 -i "$F" -frames:v 1 -vf "drawbox=x=0:y=0:w=1080:h=320:color=magenta@0.35:t=fill,drawbox=x=0:y=1440:w=1080:h=480:color=magenta@0.35:t=fill,drawbox=x=930:y=0:w=150:h=1920:color=magenta@0.35:t=fill,drawbox=x=0:y=0:w=60:h=1920:color=magenta@0.35:t=fill" "$O/safe_0.5s.png"
for p in 0 100; do python3 - "$O/still_$p.png" <<'PY'
import sys, struct, zlib, subprocess
out = subprocess.run(['ffmpeg','-loglevel','error','-i',sys.argv[1],'-vf','scale=54:96','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
m = sum(out)/len(out); print(sys.argv[1].split('/')[-1], 'mean luma', round(m,1), 'BLACK!' if m < 8 else 'ok')
PY
done
ffmpeg -loglevel error -y $(for p in 0 20 40 60 80 100; do echo -i $O/still_$p.png; done) -filter_complex "[0][1][2][3][4][5]hstack=6,scale=2160:-1" "$O/sheet.jpg"
echo "stills in $O"
