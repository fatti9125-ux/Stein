import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf
SR=44100;rng=np.random.default_rng(3)
def t(d):return np.arange(int(SR*d))/SR
def env(d,a=0.005,dec=0.2):x=t(d);return np.minimum(x/a,1)*np.exp(-x/dec)
def bp(x,lo,hi,o=2):b,a=ss.butter(o,[lo/(SR/2),hi/(SR/2)],'band');return ss.lfilter(b,a,x)
def lp(x,f,o=2):b,a=ss.butter(o,f/(SR/2));return ss.lfilter(b,a,x)
def hp(x,f,o=2):b,a=ss.butter(o,f/(SR/2),'high');return ss.lfilter(b,a,x)
def norm(x,peak=0.9):return x/np.max(np.abs(x))*peak
def save(n,x):
    x=np.concatenate([x,np.zeros(int(SR*.05))]);wf.write(f'source/sfx_wav/{n}.wav',SR,(norm(x)*32767).astype(np.int16))
# rubber stamp: dull thud + short paper slap
d=.35;x=t(d);thud=np.sin(2*np.pi*(95-40*x)*x)*env(d,.002,.06);slap=hp(rng.standard_normal(len(x)),900)*env(d,.001,.012)
save('stamp',thud*1.0+slap*0.35)
# sword swish: band noise sweeping up, bell-shaped envelope
d=.42;x=t(d);n=rng.standard_normal(len(x));out=np.zeros_like(n)
for i,(lo,hi) in enumerate(np.linspace([500,1500],[2500,6000],12)):
    s=slice(i*len(x)//12,(i+1)*len(x)//12);out[s]=bp(n,lo,hi)[s]
save('swish',out*np.sin(np.pi*x/d)**2)
# stone crack: random sharp clicks + low grind
d=.8;x=t(d);c=np.zeros_like(x)
for k in rng.uniform(0,.45,18):i=int(k*SR);L=int(SR*.012);c[i:i+L]+=hp(rng.standard_normal(L),1500)*np.exp(-np.arange(L)/(SR*.003))*rng.uniform(.4,1)
grind=lp(rng.standard_normal(len(x)),300)*env(d,.01,.25)
save('crack',c*1.0+grind*2.5)
# bronze door clang: inharmonic partials + impact
d=1.8;x=t(d);fs=[196,523,887,1310,1784,2410];cl=sum(np.sin(2*np.pi*f*x+rng.uniform(0,6))*np.exp(-x/(0.9/(1+i*.6)))/(1+i*.5) for i,f in enumerate(fs))
imp=lp(rng.standard_normal(len(x)),2000)*env(d,.001,.03)
save('clang',cl*0.6+imp*0.8)
# wave splash: swelling filtered noise
d=1.6;x=t(d);n=rng.standard_normal(len(x));w=bp(n,200,3500)*(np.minimum(x/.25,1)*np.exp(-np.maximum(x-.25,0)/.45))
save('splash',w+lp(n,400)*0.6*np.exp(-x/.5))
# throw whoosh (lower, airy)
d=.5;x=t(d);n=rng.standard_normal(len(x));save('whoosh',bp(n,250,1400)*np.sin(np.pi*x/d)**3)
# rewind: fast descending warble
d=.7;x=t(d);f=900*np.exp(-x*2.2)+180;ph=2*np.pi*np.cumsum(f)/SR;r=np.sign(np.sin(ph*6))*0.25+np.sin(ph)
save('rewind',lp(r,3000)*np.sin(np.pi*x/d)**1.5*0.7+bp(rng.standard_normal(len(x)),800,4000)*0.15*np.sin(np.pi*x/d))
print('ok')
