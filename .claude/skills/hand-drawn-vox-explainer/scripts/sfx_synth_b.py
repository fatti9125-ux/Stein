import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf
SR=44100;rng=np.random.default_rng(7)
def t(d):return np.arange(int(SR*d))/SR
def env(d,a=0.005,dec=0.2):x=t(d);return np.minimum(x/a,1)*np.exp(-x/dec)
def bp(x,lo,hi,o=2):b,a=ss.butter(o,[lo/(SR/2),hi/(SR/2)],'band');return ss.lfilter(b,a,x)
def lp(x,f,o=2):b,a=ss.butter(o,f/(SR/2));return ss.lfilter(b,a,x)
def hp(x,f,o=2):b,a=ss.butter(o,f/(SR/2),'high');return ss.lfilter(b,a,x)
def norm(x,p=0.9):return x/np.max(np.abs(x))*p
def save(n,x):x=np.concatenate([x,np.zeros(int(SR*.05))]);wf.write(f'sfx_wav/{n}.wav',SR,(norm(x)*32767).astype(np.int16))
def bell(f,d,dec):x=t(d);return sum(np.sin(2*np.pi*f*m*x)*np.exp(-x/(dec/(1+i)))/(1+i*1.5) for i,m in enumerate([1,2.76,5.4]))
# cha-ching: drawer clack + two bright bells
d=1.2;x=t(d);clack=hp(rng.standard_normal(len(x)),1200)*env(d,.001,.02)
b1=bell(2093,d,.5);b2=np.zeros_like(x);s=int(.09*SR);b2[s:]=bell(2637,d,.6)[:len(x)-s]
save('ching',clack*0.8+b1*0.5+b2*0.6)
# crash: several wooden clatters + rumble
d=1.4;x=t(d);c=np.zeros_like(x)
for k in rng.uniform(0,.7,9):i=int(k*SR);L=int(SR*.15);c[i:i+L]+=bp(rng.standard_normal(L),300,2500)*np.exp(-np.arange(L)/(SR*.03))*rng.uniform(.4,1)
save('crash',c+lp(rng.standard_normal(len(x)),200)*env(d,.01,.3)*1.5)
# ding: single counter bell
save('ding',bell(1568,1.3,.7))
# pop: soft cork-like pop
d=.18;x=t(d);save('pop',np.sin(2*np.pi*(600-1800*x)*x)*env(d,.002,.03)+hp(rng.standard_normal(len(x)),2000)*env(d,.001,.004)*.3)
