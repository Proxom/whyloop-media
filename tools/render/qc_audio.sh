#!/bin/bash
# usage: qc_audio.sh file  -> integrated loudness, true peak, and the 4 kHz high-pass loudness gap (must be >= 18 dB)
F=$1
A=$(ffmpeg -hide_banner -i "$F" -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary/,$p')
I=$(echo "$A" | grep "I:" | grep -o "\-\?[0-9.]* LUFS" | head -1 | grep -o "^-\?[0-9.]*"); TP=$(echo "$A" | grep "Peak:" | grep -o "\-\?[0-9.]* dBFS" | head -1 | grep -o "^-\?[0-9.]*")
H=$(ffmpeg -hide_banner -i "$F" -af highpass=f=4000,ebur128 -f null - 2>&1 | sed -n '/Summary/,$p' | grep "I:" | grep -o "\-\?[0-9.]* LUFS" | head -1 | grep -o "^-\?[0-9.]*")
echo "I=$I LUFS  TP=$TP dBTP  HP4k=$H LUFS  gap=$(python3 -c "print(round($I-($H),1))") dB"
