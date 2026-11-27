import sys,re,glob
from PIL import Image,ImageDraw,ImageFont
d=sys.argv[1]; cols=6; tw,th=400,225
ts=[float(m) for m in re.findall(r'pts_time:([\d.]+)',open(f'{d}/info.txt').read())]
fs=sorted(glob.glob(f'{d}/0*.png'))
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
per=cols*6
for p in range(0,len(fs),per):
    ch=fs[p:p+per]; rows=(len(ch)+cols-1)//cols
    S=Image.new('RGB',(cols*tw,rows*th),'white')
    for i,f in enumerate(ch):
        im=Image.open(f).convert('RGB').resize((tw,th)); dr=ImageDraw.Draw(im); k=p+i
        dr.rectangle([0,0,118,20],fill='black'); dr.text((3,1),f'#{k+1} {ts[k]:.2f}s',fill='yellow',font=fnt)
        S.paste(im,((i%cols)*tw,(i//cols)*th))
    S.save(f'{d}_s{p//per}.jpg',quality=78)
print(d,len(fs))
