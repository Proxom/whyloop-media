import json, numpy as np, wave
SR=48000; DUR=15.8; N=int(SR*DUR)
rng=np.random.default_rng(11)
kin=json.load(open('kin_240.json'))
L=np.zeros(N); R=np.zeros(N)
def put(sig, t, pan=0.0, gain=1.0):
    i0=int(round(t*SR)); idx=(np.arange(len(sig))+i0)%N   # circular -> seamless loop
    gl=np.cos((pan+1)*np.pi/4); gr=np.sin((pan+1)*np.pi/4)
    np.add.at(L, idx, sig*gain*gl); np.add.at(R, idx, sig*gain*gr)
def env(n, att, dec):
    t=np.arange(n)/SR; e=np.exp(-t/dec); a=np.clip(t/att,0,1); return e*a*a*(3-2*a)
def modal(freqs, amps, decs, dur=0.25, att=0.0015):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for f,a,d in zip(freqs,amps,decs):
        f=f*(1+rng.uniform(-0.02,0.02)); s+=a*np.sin(2*np.pi*f*t+rng.uniform(0,6.28))*np.exp(-t/d)
    return s*env(n,att,10)
def bandnoise(n, lo, hi):
    x=rng.standard_normal(n); X=np.fft.rfft(x); f=np.fft.rfftfreq(n,1/SR); X[(f<lo)|(f>hi)]=0; y=np.fft.irfft(X,n); return y/ (np.abs(y).max()+1e-9)
# pawl clicks: the nose lands in the next valley after riding over a tooth tip (|db| local max after a lift), plus the flip landing
db=np.array([k['db'] for k in kin]); ab=np.abs(db); evt=[]
for i in range(12,len(ab)-12):
    if ab[i]>=ab[i-12:i+13].max()-1e-6 and ab[i]>0.12 and ab[i]-ab[max(0,i-48):i].min()>0.03:
        prev=db[max(0,i-110):i]
        if prev.size and (np.abs(prev).min()<0.08 or (np.sign(prev)!=np.sign(db[i])).any()):
            if not evt or i/240-evt[-1]>0.15: evt.append(i/240)
json.dump(evt,open('clicks.json','w'))
for tc in evt:
    s=modal([620,1010,1490,240],[1.0,0.45,0.18,0.7],[0.030,0.020,0.012,0.045],dur=0.2)
    n=int(0.006*SR); s[:n]+=0.35*bandnoise(n,300,1800)*env(n,0.0008,0.0018)
    put(s, tc, pan=0.08, gain=0.5)
# lever flip: soft detent thunk when the lever moves (mid-flip)
lv=np.array([k['lever'] for k in kin]); dl=np.abs(np.diff(lv))
for i in range(1,len(dl)):
    if dl[i]>0 and dl[i-1]==0: put(modal([210,420,700],[1.0,0.4,0.15],[0.06,0.04,0.02],dur=0.25,att=0.003), i/240, pan=-0.1, gain=0.45)
# lock-in clunk at the start of each carry + socket turning rumble during drive
phi=np.array([k['phi'] for k in kin]); thg=np.array([k['thg'] for k in kin])
dth=np.diff(np.concatenate([thg,[thg[0]]]))*240  # gear speed rad/s
dph=np.diff(np.concatenate([phi,[phi[0]]]))*240
moving=np.abs(dth)>1e-3
starts=[i for i in range(len(moving)) if moving[i] and not moving[i-1]]
for i in starts:
    s=modal([150,330,560],[1.0,0.5,0.22],[0.07,0.05,0.03],dur=0.3,att=0.003)
    put(s, i/240, pan=0.0, gain=0.5)
tt=np.arange(N)/SR
gs=np.interp(tt, np.arange(len(dth))/240, np.abs(dth)); hs=np.interp(tt, np.arange(len(dph))/240, np.abs(dph))
rum=bandnoise(N,70,320)*gs/ (gs.max()+1e-9)
L+=0.10*rum; R+=0.10*rum
wh=bandnoise(N,120,900); whs=wh*(hs/(hs.max()+1e-9))**1.5
L+=0.07*whs*1.05; R+=0.07*whs*0.95
# music bed: soft pad D - Bm - G - A (3 s each) + low marimba on beats 1 and 3 (80 bpm), all < 1 kHz fundamentals
def note(m): return 440*2**((m-69)/12)
chords=[[50,57,62,66],[47,54,59,62],[43,50,55,59],[45,52,57,61]]
pad=np.zeros(N)
for ci,ch in enumerate(chords):
    t0=ci*3.95
    for m in ch:
        f=note(m); n=int(4.55*SR); t=np.arange(n)/SR
        w=np.sin(2*np.pi*f*t)+0.12*np.sin(2*np.pi*2*f*t+1.0)
        w*=0.5+0.5*np.sin(2*np.pi*0.23*t+m)
        e=np.clip(t/0.9,0,1)*np.clip((4.55-t)/0.9,0,1)
        idx=(np.arange(n)+int(t0*SR)-int(0.3*SR))%N; np.add.at(pad, idx, w*e*0.07)
mar=np.zeros(N)
bass=[38,35,31,33]
for ci in range(4):
    for b,gain in [(0,1.0),(1.975,0.6)]:
        f=note(bass[ci]+12); s=modal([f,f*3.9,f*9.2],[1.0,0.25,0.06],[0.5,0.12,0.04],dur=1.2,att=0.004)
        i0=int((ci*3.95+b)*SR); idx=(np.arange(len(s))+i0)%N; np.add.at(mar, idx, s*0.22*gain)
mus=pad+mar
M=np.fft.rfft(mus); fq=np.fft.rfftfreq(N,1/SR); M*=1/np.sqrt(1+(fq/1200)**4); mus=np.fft.irfft(M,N)
L+=0.55*mus; R+=0.55*mus
# circular convolution reverb (seamless)
def reverb(x, sec=0.7, wet=0.15):
    n=int(sec*SR); t=np.arange(n)/SR; ir=rng.standard_normal(n)*np.exp(-t/(sec/5.5)); ir/=np.sqrt((ir**2).sum())
    h=np.zeros(N); h[:n]=ir; y=np.real(np.fft.ifft(np.fft.fft(x)*np.fft.fft(h)))
    return (1-wet)*x+wet*y*1.6
L=reverb(L); R=reverb(R)
st=np.stack([L,R],1); st/=np.abs(st).max()*1.25
w=wave.open('mix_raw.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
print('ok', len(evt), 'clicks', [round(x,2) for x in evt], len(starts), 'lock starts', [round(x/240,2) for x in starts])
