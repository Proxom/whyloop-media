# p052 audio (track B, wordless): webbing whirr from the spool speed, lever swing tick, lock clunk, release tick, soft pad + marimba.
# Everything is placed circularly (seamless loop) and kept below ~1.5 kHz fundamentals; tools/render/master.sh does the safe chain.
import json, numpy as np, wave
SR=48000; DUR=13.0; N=int(SR*DUR)
rng=np.random.default_rng(52)
kin=json.load(open('kin_240.json')); ev=json.load(open('events.json'))
L=np.zeros(N); R=np.zeros(N)
def put(sig, t, pan=0.0, gain=1.0):
    i0=int(round(t*SR)); idx=(np.arange(len(sig))+i0)%N
    gl=np.cos((pan+1)*np.pi/4); gr=np.sin((pan+1)*np.pi/4)
    np.add.at(L, idx, sig*gain*gl); np.add.at(R, idx, sig*gain*gr)
def env(n, att, dec):
    t=np.arange(n)/SR; e=np.exp(-t/dec); a=np.clip(t/att,0,1); return e*a*a*(3-2*a)
def modal(freqs, amps, decs, dur=0.25, att=0.0015):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for f,a,d in zip(freqs,amps,decs): s+=a*np.sin(2*np.pi*f*(1+rng.uniform(-0.02,0.02))*t+rng.uniform(0,6.28))*np.exp(-t/d)
    return s*env(n,att,10)
def bandnoise(n, lo, hi):
    x=rng.standard_normal(n); X=np.fft.rfft(x); f=np.fft.rfftfreq(n,1/SR); X[(f<lo)|(f>hi)]=0; y=np.fft.irfft(X,n); return y/(np.abs(y).max()+1e-9)
w=np.array([k['w'] for k in kin]); db=np.array([k['db'] for k in kin]); tt=np.arange(N)/SR
ws=np.interp(tt, np.arange(len(w))/240, np.abs(w))
# webbing sliding out/in: soft fabric whoosh scaled by speed (plus a low spool rumble)
fab=bandnoise(N,150,1100); rum=bandnoise(N,60,260)
wn=ws/ (ws.max()+1e-9)
L+=0.22*fab*wn**0.8*1.03 + 0.10*rum*wn; R+=0.22*fab*wn**0.8*0.97 + 0.10*rum*wn
# lock: firm metal clunk (low modes) at the lock event
tl=[e['t'] for e in ev if e['type']=='lock'][0]
s=modal([140,310,520,880],[1.0,0.55,0.25,0.08],[0.09,0.06,0.035,0.02],dur=0.45,att=0.002); n=int(0.01*SR); s[:n]+=0.4*bandnoise(n,200,1500)*env(n,0.0006,0.003)
put(s, tl, pan=-0.1, gain=0.9)
# lever swing-out tick (when it starts moving fast) and release tick (lever back to rest)
ddb=np.diff(db)*240
i_out=int(np.argmax(ddb>1.0)); put(modal([600,980,1350],[0.6,0.25,0.08],[0.02,0.012,0.008],dur=0.12), i_out/240, pan=-0.15, gain=0.35)
i_in=int(np.argmax(ddb<-1.0)); put(modal([560,900],[0.6,0.2],[0.02,0.012],dur=0.12), i_in/240, pan=-0.15, gain=0.35)
# music: D - Bm - G - A pad (3.25 s each) + low marimba, LP 1.2 kHz
def note(m): return 440*2**((m-69)/12)
chords=[[50,57,62,66],[47,54,59,62],[43,50,55,59],[45,52,57,61]]; CH=DUR/4
pad=np.zeros(N)
for ci,ch in enumerate(chords):
    for m in ch:
        f=note(m); n=int((CH+0.6)*SR); t=np.arange(n)/SR
        wv=np.sin(2*np.pi*f*t)+0.12*np.sin(2*np.pi*2*f*t+1.0); wv*=0.5+0.5*np.sin(2*np.pi*0.23*t+m)
        e=np.clip(t/0.8,0,1)*np.clip((CH+0.6-t)/0.8,0,1)
        idx=(np.arange(n)+int(ci*CH*SR)-int(0.3*SR))%N; np.add.at(pad, idx, wv*e*0.07)
mar=np.zeros(N); bass=[38,35,31,33]
for ci in range(4):
    for b,gain in [(0,1.0),(CH/2,0.6)]:
        f=note(bass[ci]+12); s=modal([f,f*3.9,f*9.2],[1.0,0.25,0.06],[0.5,0.12,0.04],dur=1.2,att=0.004)
        idx=(np.arange(len(s))+int((ci*CH+b)*SR))%N; np.add.at(mar, idx, s*0.22*gain)
mus=pad+mar; M=np.fft.rfft(mus); fq=np.fft.rfftfreq(N,1/SR); M*=1/np.sqrt(1+(fq/1200)**4); mus=np.fft.irfft(M,N)
L+=0.5*mus; R+=0.5*mus
def reverb(x, sec=0.7, wet=0.15):
    n=int(sec*SR); t=np.arange(n)/SR; ir=rng.standard_normal(n)*np.exp(-t/(sec/5.5)); ir/=np.sqrt((ir**2).sum())
    h=np.zeros(N); h[:n]=ir; y=np.real(np.fft.ifft(np.fft.fft(x)*np.fft.fft(h))); return (1-wet)*x+wet*y*1.6
L=reverb(L); R=reverb(R)
st=np.stack([L,R],1); st/=np.abs(st).max()*1.25
wf=wave.open('mix_raw.wav','wb'); wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((st*32767).astype(np.int16).tobytes()); wf.close()
print('ok lock', round(tl,3), 'swing out', round(i_out/240,3), 'release', round(i_in/240,3))
