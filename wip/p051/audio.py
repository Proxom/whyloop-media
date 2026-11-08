# p051 audio stems. usage: python3 audio.py <vo dir with vo0..4.wav>  -> vo_stem.wav, bed_stem.wav (both 48 kHz stereo, LOOP s)
# SFX come from the same simulation as the picture (events.json, kin_240.json): pawl ticks, the lock-in clunk, hub rumble.
import json, sys, wave, numpy as np
SR=48000; DUR=18.5; N=int(SR*DUR); rng=np.random.default_rng(51)
VO_AT=[0.15, 2.6, 5.6, 10.4, 15.1]
def readwav(p):
    w=wave.open(p); sr=w.getframerate(); ch=w.getnchannels(); sw=w.getsampwidth(); x=np.frombuffer(w.readframes(w.getnframes()), dtype={2:np.int16,4:np.int32}[sw]).astype(float)
    x=x.reshape(-1,ch).mean(1)/ (32768 if sw==2 else 2**31); n=int(len(x)*SR/sr); return np.interp(np.arange(n)*sr/SR, np.arange(len(x)), x)
vo=np.zeros(N)
for i,t in enumerate(VO_AT):
    x=readwav(f'{sys.argv[1]}/vo{i}.wav'); i0=int(t*SR); vo[i0:i0+len(x)]+=x[:N-i0]
L=np.zeros(N); R=np.zeros(N)
def put(sig,t,pan=0.0,gain=1.0):
    i0=int(round(t*SR)); idx=(np.arange(len(sig))+i0)%N; gl=np.cos((pan+1)*np.pi/4); gr=np.sin((pan+1)*np.pi/4)
    np.add.at(L,idx,sig*gain*gl); np.add.at(R,idx,sig*gain*gr)
def env(n,att,dec): t=np.arange(n)/SR; a=np.clip(t/att,0,1); return np.exp(-t/dec)*a*a*(3-2*a)
def modal(fr,am,de,dur=0.25,att=0.0015):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for f,a,d in zip(fr,am,de): f*=1+rng.uniform(-0.03,0.03); s+=a*np.sin(2*np.pi*f*t+rng.uniform(0,6.28))*np.exp(-t/d)
    return s*env(n,att,10)
def bandnoise(n,lo,hi):
    X=np.fft.rfft(rng.standard_normal(n)); f=np.fft.rfftfreq(n,1/SR); X[(f<lo)|(f>hi)]=0; y=np.fft.irfft(X,n); return y/(np.abs(y).max()+1e-9)
ev=json.load(open('events.json')); clicks=[e['t'] for e in ev if e['type']=='click']; locks=[e['t'] for e in ev if e['type']=='lock']
for tc in clicks:   # soft wooden-ish tick, fundamentals < 1.3 kHz (no sharp metal clink)
    s=modal([560,880,1240,230],[1.0,0.42,0.14,0.6],[0.022,0.016,0.010,0.035],dur=0.16)
    n=int(0.005*SR); s[:n]+=0.3*bandnoise(n,250,1500)*env(n,0.0006,0.0015); put(s,tc,pan=0.05,gain=0.55)
for tl in locks: put(modal([140,310,520],[1.0,0.5,0.2],[0.08,0.05,0.03],dur=0.35,att=0.003),tl,gain=0.7)
kin=json.load(open('kin_240.json')); ar=np.array([k['ar'] for k in kin]); ad=np.array([k['ad'] for k in kin])
war=np.abs(np.gradient(ar))*240; wad=np.abs(np.gradient(ad))*240; tt=np.arange(N)/SR
gr=np.interp(tt,np.arange(len(war))/240,war); gd=np.interp(tt,np.arange(len(wad))/240,wad)
rum=bandnoise(N,60,260); L+=0.06*rum*gr/gr.max(); R+=0.06*rum*gr/gr.max()
whir=bandnoise(N,90,500)*(gd/(gd.max()+1e-9))**1.5; L+=0.08*whir; R+=0.08*whir
# music bed: soft pad + low marimba, 4 bars over the loop, fundamentals < 1 kHz
def note(m): return 440*2**((m-69)/12)
chords=[[52,59,64,67],[48,55,60,64],[43,50,55,59],[50,57,62,66]]; seg=DUR/4; mus=np.zeros(N)
for ci,ch in enumerate(chords):
    for m in ch:
        f=note(m); n=int((seg+0.9)*SR); t=np.arange(n)/SR; w=(np.sin(2*np.pi*f*t)+0.1*np.sin(4*np.pi*f*t+1))*(0.55+0.45*np.sin(2*np.pi*0.21*t+m))
        e=np.clip(t/0.9,0,1)*np.clip((seg+0.9-t)/0.9,0,1); idx=(np.arange(n)+int((ci*seg-0.45)*SR))%N; np.add.at(mus,idx,w*e*0.06)
bass=[40,36,31,38]
for ci in range(4):
    for b,g in [(0,1.0),(seg/2,0.6)]:
        f=note(bass[ci]+12); s=modal([f,f*3.9],[1.0,0.2],[0.5,0.1],dur=1.2,att=0.004); idx=(np.arange(len(s))+int((ci*seg+b)*SR))%N; np.add.at(mus,idx,s*0.2*g)
M=np.fft.rfft(mus); fq=np.fft.rfftfreq(N,1/SR); M*=1/np.sqrt(1+(fq/1100)**4); mus=np.fft.irfft(M,N); L+=0.5*mus; R+=0.5*mus
def reverb(x,sec=0.6,wet=0.14):
    n=int(sec*SR); t=np.arange(n)/SR; ir=rng.standard_normal(n)*np.exp(-t/(sec/5.5)); ir/=np.sqrt((ir**2).sum()); h=np.zeros(N); h[:n]=ir
    return (1-wet)*x+wet*np.real(np.fft.ifft(np.fft.fft(x)*np.fft.fft(h)))*1.6
L=reverb(L); R=reverb(R)
def w(p,st):
    st=st/ (np.abs(st).max()*1.25); f=wave.open(p,'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st*32767).astype(np.int16).tobytes()); f.close()
w('bed_stem.wav',np.stack([L,R],1)); w('vo_stem.wav',np.stack([vo,vo],1))
print('clicks',len(clicks),'locks',locks)
