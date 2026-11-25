import sys,subprocess,json,hashlib,numpy as np
src,out=sys.argv[1],sys.argv[2]
W,H=1280,720
p=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,bufsize=W*H*3*4)
prev=None;i=0
md5=[];frac=[];mx=[];bbox=[];grid=[];bg=[]
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3:break
    md5.append(hashlib.md5(b).hexdigest()[:12])
    f=np.frombuffer(b,np.uint8).reshape(H,W,3)
    s=f[::2,::2].astype(np.int16)                      # 640x360 working copy
    if i%15==0:
        top=s[50:70:2,::8].reshape(-1,3);u,c=np.unique(top,axis=0,return_counts=True);bg.append([i]+u[c.argmax()].tolist())
    if prev is None: frac.append(-1);mx.append(-1);bbox.append(None);grid.append(0)
    else:
        a=np.abs(s-prev).max(axis=2);m=a>24
        frac.append(round(float(m.mean()),5));mx.append(int(a.max()))
        if m.any():
            ys,xs=np.where(m);bbox.append([round(xs.min()/640,3),round(ys.min()/360,3),round((xs.max()+1)/640,3),round((ys.max()+1)/360,3)])
            g=m.reshape(4,90,8,80).mean(axis=(1,3))>0.002;grid.append(int(sum(1<<k for k,v in enumerate(g.flatten()) if v)))
        else: bbox.append(None);grid.append(0)
    prev=s;i+=1
    if i%5000==0:print(i,flush=True)
json.dump(dict(src=src,frames=i,md5=md5,frac=frac,maxdiff=mx,bbox=bbox,grid=grid,bg=bg),open(out,'w'))
print('done',i)
