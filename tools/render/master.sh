#!/bin/bash
# Safe audio master (AGENT.md 5.5). usage: master.sh vo.wav bed.wav out.wav [voGainDb=0] [bedGainDb=-6] [targetLUFS=-15]
# vo: de-esser; bed: low-pass 7.5 kHz x2; mix: -4 dB high-shelf from 5 kHz, gentle compression, loudness to target, true peak <= -2 dBTP.
set -e
VO=$1; BED=$2; OUT=$3; VG=${4:-0}; BG=${5:--6}; TGT=${6:--15}
CH="[0:a]highpass=f=80,deesser=i=0.6:m=0.5:f=0.5,highshelf=f=3500:g=-8,lowpass=f=7000,lowpass=f=7000,volume=${VG}dB[v];[1:a]lowpass=f=7000,lowpass=f=7000,highshelf=f=3500:g=-6,volume=${BG}dB[b];[v][b]amix=inputs=2:normalize=0,highshelf=f=5000:g=-4,acompressor=threshold=-20dB:ratio=2.2:attack=8:release=120:makeup=1"
ffmpeg -loglevel error -y -i "$VO" -i "$BED" -filter_complex "$CH" -ar 48000 /tmp/_m1.wav
I=$(ffmpeg -hide_banner -i /tmp/_m1.wav -af ebur128=peak=true -f null - 2>&1 | grep -A1 "Integrated loudness" | grep -o "I: *-\?[0-9.]*" | grep -o "\-\?[0-9.]*$")
G=$(python3 -c "print(round($TGT - ($I), 2))")
ffmpeg -loglevel error -y -i /tmp/_m1.wav -af "volume=${G}dB,alimiter=limit=0.70:level=false:latency=true,aresample=48000" -c:a pcm_s16le "$OUT"
echo "pre $I LUFS, gain $G dB"
