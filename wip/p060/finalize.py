# Loop seam: the last 0.6 s (18 frames) cross-fade toward frame 0 so the loop has no jump (the arm ends 5 teeth tighter than it starts).
# usage: python3 finalize.py <frames dir> <out dir>   (copies all frames, blends 1212..1229 with f0000)
import sys, os, shutil
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True); N = 1230; A, B = 1212, N
f0 = Image.open(f'{src}/f0000.png').convert('RGB')
for i in range(N):
    p = f'{src}/f{i:04d}.png'; assert os.path.exists(p), p
    if i < A: shutil.copyfile(p, f'{dst}/f{i:04d}.png'); continue
    u = (i - A + 1) / (B - A + 1); u = u * u * (3 - 2 * u)
    Image.blend(Image.open(p).convert('RGB'), f0, u).save(f'{dst}/f{i:04d}.png')
print('ok', N)
