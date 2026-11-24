import json,sys,os
from PIL import Image,ImageDraw
B=json.load(open('editor/storyboard.json'));S=B['scenes'];a,b=int(sys.argv[1]),int(sys.argv[2])
W,H=640,360;cols=4;sub=S[a:b];rows=(len(sub)+cols-1)//cols
M=Image.new('RGB',(cols*W,rows*(H+24)),'white');d=ImageDraw.Draw(M)
for i,s in enumerate(sub):
    t=round(s['e']-0.25,2);f=f'chk/t_{t}.jpg'
    if not os.path.exists(f):f=f'chk/t_{int(t)}.jpg' if os.path.exists(f'chk/t_{int(t)}.jpg') else None
    x,y=(i%cols)*W,(i//cols)*(H+24)
    if f:M.paste(Image.open(f).resize((W,H)),(x,y+24))
    d.text((x+4,y+5),f"#{a+i+1} {s['s']:.0f}-{s['e']:.0f}s {s['h']['a'][:40]}",fill='black')
M.save(sys.argv[3],quality=82)
