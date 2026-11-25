# group per-frame changes into events; numeric pre-classification (visual review confirms/corrects)
import sys,json,numpy as np
S=json.load(open(sys.argv[1]));out=sys.argv[2];N=S['frames']
frac=np.array(S['frac']);bb=S['bbox'];md5=S['md5']
NOISE=float(sys.argv[3]) if len(sys.argv)>3 else 0.0004
ch=frac>NOISE;ch[0]=False
ev=[];i=1
while i<N:
    if ch[i]:
        j=i
        while j+1<N and (ch[j+1] or (j+2<N and ch[j+2])):j+=1   # allow 1-frame gaps
        span=list(range(i,j+1));fr=frac[i:j+1]
        boxes=[bb[k] for k in span if bb[k]]
        u=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
        area=(u[2]-u[0])*(u[3]-u[1]);pk=i+int(fr.argmax())
        n=j-i+1;mx=float(fr.max())
        if mx>0.35 and n<=2: kind='cut'
        elif mx>0.35: kind='full_frame_motion'           # grid/strip move, zoom, wipe, big entrance
        elif n<=2: kind='instant_change'                  # pop/swap/appear/disappear in 1-2 frames
        elif n<=8: kind='short_animation'
        else: kind='long_animation'
        ev.append(dict(first=i,last=j,frames=n,peak=pk,peak_frac=round(mx,4),bbox=[round(v,3) for v in u],area=round(area,3),kind=kind))
        i=j+1
    else:i+=1
# holds: identical-pixel runs and sub-noise runs
ident=sum(1 for k in range(1,N) if md5[k]==md5[k-1])
json.dump(dict(noise_thr=NOISE,frames=N,identical_to_prev=ident,below_noise=int((~ch).sum()),events=ev),open(out,'w'))
from collections import Counter
print('frames',N,'identical-to-previous',ident,'changed',int(ch.sum()),'events',len(ev),Counter(e['kind'] for e in ev))
