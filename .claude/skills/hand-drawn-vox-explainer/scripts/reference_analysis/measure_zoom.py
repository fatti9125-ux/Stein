# measure grid->tile zoom: similarity transform from reference grid frame to each frame (ORB + RANSAC), chained frame-to-frame
import sys,json,numpy as np,cv2
sys.path.insert(0,'.')
from framegrab import grab
src,ptsf,md5f,a,b=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
pts=json.load(open(ptsf));fr=grab(src,pts,list(range(a-1,b+2)),md5file=md5f)
orb=cv2.ORB_create(4000);bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
def feat(k):
    g=cv2.cvtColor(np.asarray(fr[k]),cv2.COLOR_RGB2GRAY);return orb.detectAndCompute(g,None)
M=np.eye(3);rows=[]
prev=feat(a-1)
for k in range(a,b+2):
    cur=feat(k);m=bf.match(prev[1],cur[1])
    p1=np.float32([prev[0][x.queryIdx].pt for x in m]);p2=np.float32([cur[0][x.trainIdx].pt for x in m])
    A,inl=cv2.estimateAffinePartial2D(p1,p2,method=cv2.RANSAC,ransacReprojThreshold=3)
    if A is None:rows.append((k,None));prev=cur;continue
    M=np.vstack([A,[0,0,1]])@M;s=float(np.sqrt(M[0,0]**2+M[1,0]**2))
    # grid point that maps to frame centre
    inv=np.linalg.inv(M);c=inv@np.array([640,360,1])
    rows.append((k,round(s,3),round(c[0]/1280,3),round(c[1]/720,3),int(inl.sum())))
    prev=cur
for r in rows:print(r)
