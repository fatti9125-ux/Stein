import csv,json
from PIL import Image
R=list(csv.DictReader(open('assets_raw/Asset_Index.csv',encoding='utf-8-sig')))
FACE={'C01-06':'R','C01-12':'R','C02-02':'R','C02-05':'R','C02-07':'R','C02-11':'R','C02-12':'L','C03-04':'R','C03-06':'R',
 'C04-01':'R','C04-03':'R','C04-04':'R','C04-09':'R','C04-10':'R','C04-11':'R'}
K={'C':'char','F':'prop','P':'prop','E':'fx','B':'bg','G':'gfx'}
lib={}
for r in R:
    i=r['ID'];im=Image.open('assets_raw/'+r['File']).convert('RGBA' if r['Transparent']=='Yes' else 'RGB')
    im.save(f'editor/assets/{i}.webp','WEBP',quality=88,method=5)
    e=dict(d=r['Asset'].replace('_',' '),w=im.width,h=im.height,k=K[i[0]])
    if i[0]=='C':e['f']=FACE.get(i,'F')
    lib[i]=e
json.dump(lib,open('editor/library.json','w'));print(len(lib))
