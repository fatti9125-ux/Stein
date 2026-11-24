import csv,sys
from PIL import Image,ImageDraw,ImageFont
R=list(csv.DictReader(open('assets_raw/Asset_Index.csv',encoding='utf-8-sig')))
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14) if __import__('os').path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else ImageFont.load_default()
def sheet(pref,name,cols,cw,chh):
    rows=[r for r in R if r['ID'][0] in pref]
    n=len(rows);rr=(n+cols-1)//cols;S=Image.new('RGB',(cols*cw,rr*(chh+22)),(191,230,245));d=ImageDraw.Draw(S)
    for i,r in enumerate(rows):
        im=Image.open('assets_raw/'+r['File']).convert('RGBA');im.thumbnail((cw-8,chh-4))
        x=(i%cols)*cw;y=(i//cols)*(chh+22);S.paste(im,(x+(cw-im.width)//2,y+2),im);d.text((x+4,y+chh+2),r['ID'],fill=(0,0,0),font=f)
    S.save(name,quality=80)
sheet('C','sheet_chars.jpg',12,160,230)
sheet('FPE','sheet_props.jpg',14,140,140)
sheet('G','sheet_graphics.jpg',8,240,110)
sheet('B','sheet_bgs.jpg',5,384,216)
