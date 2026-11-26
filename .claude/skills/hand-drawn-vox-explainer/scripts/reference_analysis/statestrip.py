# full-frame state after every event inside [a,b], labelled; shows how a composition builds
import sys,json
sys.path.insert(0,'.')
from framegrab import grab
from PIL import Image,ImageDraw
src,ptsf,md5f,evf,out=sys.argv[1:6];spans=[tuple(map(int,s.split('-'))) for s in sys.argv[6].split(',')]
pts=json.load(open(ptsf));E=json.load(open(evf))['events']
rows=[]
for a,b in spans:
    fr=[a]+[e['last']+1 for e in E if a<e['first']<=b and e['kind']!='codec_keyframe_refresh']
    rows.append(fr)
G=grab(src,pts,[f for r in rows for f in r],md5file=md5f)
tw,th,cols=320,180,8;lines=sum((len(r)+cols-1)//cols for r in rows)
M=Image.new('RGB',(cols*tw,lines*(th+14)),'white');d=ImageDraw.Draw(M);y=0
for r in rows:
    for k,f in enumerate(r):
        if k and k%cols==0:y+=th+14
        x=(k%cols)*tw
        if f in G:im=G[f].copy();im.thumbnail((tw-3,th));M.paste(im,(x,y+14))
        d.text((x+2,y+1),f'F{f} {(pts[f]):.1f}s',fill='black')
    y+=th+14
M.save(out,quality=82);print(out,[len(r) for r in rows])
