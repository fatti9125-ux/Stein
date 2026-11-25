# audio pass helper: envelope, pauses, spectral-flux onsets, residual (music/ambience) check in pauses
import sys,json,numpy as np,scipy.io.wavfile as wf,scipy.signal as ss
src,out=sys.argv[1],sys.argv[2]
SR,x=wf.read(src);x=x.astype(np.float32)/32768
if x.ndim>1:x=x.mean(axis=1)
hop=int(SR*0.01);win=int(SR*0.04)
f,t,Z=ss.stft(x,SR,nperseg=win,noverlap=win-hop,boundary=None)
P=np.abs(Z)**2+1e-12
rms=10*np.log10(P.sum(axis=0)/P.shape[0])
speech=10*np.log10(P[(f>300)&(f<3400)].sum(axis=0)+1e-12)
hf=10*np.log10(P[f>5000].sum(axis=0)+1e-12)
flat=np.exp(np.log(P).mean(axis=0))/P.mean(axis=0)
flux=np.maximum(0,np.diff(np.log(P),axis=1)).sum(axis=0);flux=np.concatenate([[0],flux])
# VO activity: speech-band energy above adaptive threshold
thr=np.percentile(speech,30)+10;act=speech>thr
# pauses >= 0.25 s
pauses=[];i=0;n=len(act)
while i<n:
    if not act[i]:
        j=i
        while j<n and not act[j]:j+=1
        if (j-i)*0.01>=0.25:
            seg=slice(i,j);pauses.append(dict(s=round(t[i],2),e=round(t[j-1],2),dur=round((j-i)*0.01,2),floor_db=round(float(np.median(rms[seg])),1),flat=round(float(np.median(flat[seg])),3)))
        i=j
    else:i+=1
# onset candidates: flux peaks well above local median
med=ss.medfilt(flux,101);pk,_=ss.find_peaks(flux-med,height=np.percentile(flux-med,99.3),distance=15)
ons=[dict(t=round(float(t[k]),2),strength=round(float(flux[k]-med[k]),1),rms_db=round(float(rms[k]),1),hf_db=round(float(hf[k]),1),in_pause=bool(not act[k])) for k in pk]
json.dump(dict(sr=SR,hop_s=0.01,global_rms_median_db=round(float(np.median(rms)),1),speech_thr_db=round(float(thr),1),pauses=pauses,onsets=ons),open(out,'w'))
print('pauses',len(pauses),'onsets',len(ons),'pause floor median dB',np.median([p['floor_db'] for p in pauses]),'speech median',np.median(rms[act]))
