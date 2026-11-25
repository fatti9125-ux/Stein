# compact review sheet: every event as [before | after] crops of its changed region, 5 per row
import sys,json
sys.path.insert(0,'.')
from framegrab import grab
from PIL import Image,ImageDraw
src,evf,ptsf,md5f,cid,a,b=sys.argv[1:8];a,b=int(a),int(b)
pts=json.load(open(ptsf))
E=[e for e in json.load(open(evf))['events'] if a<=e['first']<=b and e['kind']!='codec_keyframe_refresh']
fr=grab(src,pts,[k for e in E for k in (e['first']-1,e['last']+1)],md5file=md5f)
W,H=1280,720;CW,CH,cols=190,150,5;per=40
out=[]
for s in range(0,len(E),per):
    sub=E[s:s+per];rows=(len(sub)+cols-1)//cols
    M=Image.new('RGB',(cols*(2*CW+8),rows*(CH+16)),'white');d=ImageDraw.Draw(M)
    for i,e in enumerate(sub):
        x=(i%cols)*(2*CW+8);y=(i//cols)*(CH+16)
        x0,y0,x1,y1=e['bbox'];full=(x1-x0)*(y1-y0)>0.5
        box=(0,0,W,H) if full else (int(max(0,x0-.02)*W),int(max(0,y0-.02)*H),int(min(1,x1+.02)*W),int(min(1,y1+.02)*H))
        for j,k in enumerate((e['first']-1,e['last']+1)):
            if k in fr:
                c=fr[k].crop(box);c.thumbnail((CW-2,CH));M.paste(c,(x+j*CW,y+16))
        d.text((x+2,y+2),f"F{e['first']}" + (f"-{e['last']}" if e['last']>e['first'] else '') + f" {e['kind'][:10]} {'FULL' if full else ''}",fill='black')
        d.rectangle([x+CW-1,y+16,x+CW,y+16+CH],fill='red')
    p=f'cmp_{cid}_{s//per}.jpg';M.save(p,quality=82);out.append(p)
json.dump(dict(events=E),open(f'_ev_{cid}.json','w'))
print(cid,len(E),'events',out)
