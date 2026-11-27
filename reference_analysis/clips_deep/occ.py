import sys,glob,numpy as np
from PIL import Image
from scipy import ndimage
def stats(f):
    a=np.asarray(Image.open(f).convert('RGB').resize((320,180)),int)
    bg=np.median(a[2:8,:,:].reshape(-1,3),axis=0)
    m=(np.abs(a-bg).sum(2)>40)
    m[:22,:]=False  # ignore header strip (top 12%)
    occ=m.mean()
    lab,n=ndimage.label(ndimage.binary_dilation(m,iterations=1))
    sizes=ndimage.sum(m,lab,range(1,n+1)); big=(sizes>40).sum()
    # gap metric: dilate by k px until #big comps merges to 1 -> how far apart clusters are
    k=0;mm=m.copy()
    while True:
        l,nn=ndimage.label(mm); s=ndimage.sum(m,l,range(1,nn+1))
        if (s>40).sum()<=1 or k>40: break
        mm=ndimage.binary_dilation(mm); k+=1
    xs=np.nonzero(m.any(0))[0]; ys=np.nonzero(m.any(1))[0]
    return occ,big,k*2*1080/180/ 2  # k px at 320 -> px at 1920 approx (x6)
for g in sys.argv[1:]:
    fs=sorted(glob.glob(g)); r=np.array([stats(f) for f in fs])
    print(g, 'n',len(fs),'occ med %.3f p75 %.3f'%(np.median(r[:,0]),np.percentile(r[:,0],75)),'comps med',np.median(r[:,1]),'merge-dist(px@1080) med',np.median(r[:,2]))
