import sys,re,glob,os
from PIL import Image,ImageDraw,ImageFont
d=sys.argv[1]; cols=int(sys.argv[2]) if len(sys.argv)>2 else 4; tw=480
ts=[float(m) for m in re.findall(r'pts_time:([\d.]+)',open(f'{d}/info.txt').read())]
fs=sorted(glob.glob(f'{d}/0*.png'))
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
per=cols*5
for p in range(0,len(fs),per):
    chunk=fs[p:p+per]; rows=(len(chunk)+cols-1)//cols
    S=Image.new('RGB',(cols*tw,rows*270),'white')
    for i,f in enumerate(chunk):
        im=Image.open(f).convert('RGB').resize((tw,270))
        dr=ImageDraw.Draw(im); idx=p+i
        dr.rectangle([0,0,150,26],fill='black'); dr.text((4,2),f'#{idx+1} {ts[idx]:.2f}s',fill='yellow',font=fnt)
        S.paste(im,((i%cols)*tw,(i//cols)*270))
    S.save(f'{d}_sheet{p//per}.jpg',quality=80)
print(len(fs),len(ts))
