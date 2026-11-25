import sys,json,numpy as np
sys.path.insert(0,'.')
from framegrab import grab
from PIL import Image,ImageDraw
src,ptsf,md5f,out=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
pairs=[tuple(map(int,s.split(':'))) for s in sys.argv[5].split(',')]   # a:b means compare frame a-1 vs b (b defaults a)
pts=json.load(open(ptsf));need=[]
for a,b in pairs:need+= [a-1,b]
fr=grab(src,pts,need,md5file=md5f)
rows=[]
for a,b in pairs:
    A=np.asarray(fr[a-1]).astype(int);B=np.asarray(fr[b]).astype(int);m=np.abs(A-B).max(axis=2)>24
    if not m.any():rows.append((a,b,None,None,None));continue
    ys,xs=np.where(m);x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    # largest dense cluster: use 64px grid density
    pad=24;box=(max(0,x0-pad),max(0,y0-pad),min(1280,x1+pad),min(720,y1+pad))
    rows.append((a,b,box,int(m.sum()),(round(x0/1280,3),round(y0/720,3),round(x1/1280,3),round(y1/720,3))))
M=Image.new('RGB',(3*330,len(rows)*260),'white');d=ImageDraw.Draw(M)
for r,(a,b,box,npx,nb) in enumerate(rows):
    y=r*260;d.text((2,y+2),f'F{a-1:06d} vs F{b:06d}  changed px={npx} bbox={nb}',fill='black')
    if box is None:d.text((2,y+20),'no pixel > 24 differs',fill='red');continue
    for c,img in enumerate([fr[a-1],fr[b]]):
        cr=img.crop(box);cr=cr.resize((min(320,cr.width*3),min(220,cr.height*3)),Image.NEAREST) if cr.width<110 and cr.height<75 else cr;cr.thumbnail((320,225));M.paste(cr,(c*330,y+18))
    A=np.asarray(fr[a-1].crop(box)).astype(int);B=np.asarray(fr[b].crop(box)).astype(int);D=Image.fromarray((np.abs(A-B).max(axis=2)>24).astype(np.uint8)*255).convert('RGB');D.thumbnail((320,225));M.paste(D,(660,y+18))
M.save(out,quality=85);print('ok')
