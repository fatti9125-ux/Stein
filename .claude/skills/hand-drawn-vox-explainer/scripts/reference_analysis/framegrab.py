# exact frame grabber: seeks, then ALIGNS decoded frames to the global index by matching per-frame md5 sequences
import json,subprocess,hashlib
from PIL import Image
_MD5={}
def grab(src,pts,idxs,W=1280,H=720,md5file=None):
    md5=_MD5.get(md5file)
    if md5 is None and md5file:md5=_MD5[md5file]=json.load(open(md5file))['md5']
    idxs=sorted(set(i for i in idxs if 0<=i<len(pts)));out={}
    groups=[];cur=[]
    for i in idxs:
        if cur and i-cur[-1]>90:groups.append(cur);cur=[]
        cur.append(i)
    if cur:groups.append(cur)
    for g in groups:
        t0=max(0,pts[g[0]]-3.0)
        p=subprocess.Popen(['ffmpeg','-v','error','-ss',f'{t0:.4f}','-i',src,'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
        buf=[]
        est=next(i for i,t in enumerate(pts) if t>=t0-1e-4)
        need_n=g[-1]-est+60
        for _ in range(need_n+60):
            b=p.stdout.read(W*H*3)
            if len(b)<W*H*3:break
            buf.append(b)
        p.kill()
        h=[hashlib.md5(b).hexdigest()[:12] for b in buf]
        # find offset k0 such that h[m]==md5[k0+m] for the longest run near est
        best=None
        for k0 in range(max(0,est-90),est+91):
            if k0+len(h)>len(md5):continue
            ok=sum(1 for m in range(0,min(len(h),200)) if h[m]==md5[k0+m])
            if best is None or ok>best[1]:best=(k0,ok)
        k0=best[0]
        if best[1]<min(len(h),200)*0.98:print('WARN weak alignment',g[0],best)
        for i in g:
            m=i-k0
            if 0<=m<len(buf):out[i]=Image.frombytes('RGB',(W,H),buf[m])
    return out
