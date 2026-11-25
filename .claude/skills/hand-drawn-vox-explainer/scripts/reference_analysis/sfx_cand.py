# SFX candidates: broadband transients whose HF/flux stands out from local speech envelope AND that sit in a VO gap (pause list)
import sys,json,numpy as np,scipy.io.wavfile as wf,scipy.signal as ss
wav,afeat,out=sys.argv[1:4]
A=json.load(open(afeat));P=[(p['s'],p['e']) for p in A['pauses']]
SR,x=wf.read(wav);x=x.astype(np.float32);x=(x.mean(axis=1) if x.ndim>1 else x)/32768
hop=int(SR*0.01);win=int(SR*0.04)
f,t,Z=ss.stft(x,SR,nperseg=win,noverlap=win-hop,boundary=None);P2=np.abs(Z)**2+1e-12
hf=10*np.log10(P2[f>4000].sum(axis=0));lo=10*np.log10(P2[(f>80)&(f<4000)].sum(axis=0))
flux=np.concatenate([[0],np.maximum(0,np.diff(np.log(P2),axis=1)).sum(axis=0)])
inp=np.zeros(len(t),bool)
for s,e in P:inp[(t>=s)&(t<=e)]=True
med=ss.medfilt(flux,201);z=(flux-med)/(np.median(np.abs(flux-med))+1e-9)
pk,_=ss.find_peaks(z,height=6,distance=20)
c=[dict(t=round(float(t[k]),2),z=round(float(z[k]),1),hf_db=round(float(hf[k]),1),lo_db=round(float(lo[k]),1)) for k in pk if inp[k]]
json.dump(c,open(out,'w'));print('peaks',len(pk),'in pauses',len(c))
