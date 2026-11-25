# every frame of a span (plus 1 before/after) as a labelled filmstrip, full frame
import sys,json
sys.path.insert(0,'.')
from framegrab import grab
from PIL import Image,ImageDraw
src,ptsf,md5f,out=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
spans=[tuple(map(int,s.split('-'))) for s in sys.argv[5].split(',')]
pts=json.load(open(ptsf));tw,th,cols=240,135,8
rows=[]
for a,b in spans:
    idx=list(range(a-1,b+2))
    if len(idx)>cols*3: idx=[a-1]+list(range(a,b+1,max(1,(b-a)//(cols*3-3))))+[b,b+1]
    rows.append(idx)
fr=grab(src,pts,[i for r in rows for i in r],md5file=md5f)
lines=sum((len(r)+cols-1)//cols for r in rows)
M=Image.new('RGB',(cols*tw,lines*(th+14)),'white');d=ImageDraw.Draw(M);y=0
for r in rows:
    for k,i in enumerate(r):
        x=(k%cols)*tw
        if k and k%cols==0:y+=th+14
        if i in fr:im=fr[i].copy();im.thumbnail((tw-2,th));M.paste(im,(x,y+14))
        d.text((x+2,y+1),f'F{i:06d}',fill='black')
    y+=th+14
M.save(out,quality=82);print('ok')
