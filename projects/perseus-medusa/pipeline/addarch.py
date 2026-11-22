import json,os
from PIL import Image
A=json.load(open('render/assets.json'))
want={'medusa_caravaggio':(1,1),'pelike_met':(3159,4000),'cast_out_met':(16,10),'tower_brass':(348,685)}
for k,ar in want.items():
    f=f'archive_dl/{k}.jpg'
    if os.path.exists(f):
        im=Image.open(f).convert('RGB');im.thumbnail((1400,1400))
        if k=='medusa_caravaggio':  # crop to the shield
            w,h=im.size;c=int(min(w,h)*0.9);im=im.crop(((w-c)//2,(h-c)//2,(w+c)//2,(h+c)//2))
        if k=='pelike_met':
            w,h=im.size;im=im.crop((int(w*.16),int(h*.24),int(w*.86),int(h*.78)))
        im.save(f'render/assets/{k}.png');print('real',k,im.size)
    else:
        im=Image.new('RGB',(ar[0]*100//max(ar),ar[1]*100//max(ar)),(150,150,150));im.save(f'render/assets/{k}.png');print('placeholder',k)
    A[k]=list(im.size)
json.dump(A,open('render/assets.json','w'))
