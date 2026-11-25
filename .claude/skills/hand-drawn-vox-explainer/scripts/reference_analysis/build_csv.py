# merge numeric events + visual annotations into events.csv / frames.csv for one chapter range; update progress.json
import sys,json,csv,os
R='/home/user/Stein/reference_analysis/01'
evf,chap_id,a,b=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
S=json.load(open('full01.json'));E=[e for e in json.load(open(evf))['events'] if a<=e['first']<=b]
pts=json.load(open('pts01.json'));p0=pts[0]
ann={}
for l in open(f'{R}/annot/{chap_id}.tsv',encoding='utf-8').read().splitlines()[1:]:
    f,t,dsc,ev,cf=l.split('\t');ann.setdefault(int(f),[]).append((t,dsc,ev,cf))
strip_frames=set()
for f,L in ann.items():
    for t,dsc,ev,cf in L:
        if t.startswith('REFINED'):
            # refined spans were inspected frame by frame
            import re
            m=re.findall(r'F(\d+)',dsc)
            if m:lo,hi=min(map(int,m)),max(map(int,m));strip_frames.update(range(lo,hi+1))
rows=[];shot=0;shots={}
RESET=('hard_cut','layout_reset','partial_reset','camera_zoom')
for e in E:
    L=ann.get(e['first'],[])
    final=[x for x in L if x[0].startswith('REFINED')] or L
    t,dsc,evd,cf=(final[-1] if final else (e['kind'],'numeric only (not visually reviewed)','measured','low'))
    if t.startswith('REFINED'):t=t.replace('REFINED ','')
    if any(t.startswith(r) for r in RESET) or 'reset' in t:shot+=1
    eid=f'{chap_id}-E{e["first"]:06d}'
    rows.append(dict(event_id=eid,shot_id=f'{chap_id}-S{shot:02d}',track='scene',event_type=t,first_frame=e['first'],last_frame=e['last'],
        source_pts_in=f"{pts[e['first']]:.6f}",source_pts_out=f"{pts[min(e['last']+1,len(pts)-1)]:.6f}",from_state=f'state_before_F{e["first"]:06d}',to_state=f'state_after_F{e["last"]:06d}',
        measured_keys=json.dumps(dict(bbox_norm=e['bbox'],peak_frac=e['peak_frac'],frames=e['frames'],peak_frame=e['peak'],iframe=e.get('iframe',False)))+' | '+dsc,
        confidence=cf,evidence_path=f'reference_analysis/01/evidence/{chap_id}'))
    e['eid']=eid;e['shot']=f'{chap_id}-S{shot:02d}'
hdr=['event_id','shot_id','track','event_type','first_frame','last_frame','source_pts_in','source_pts_out','from_state','to_state','measured_keys','confidence','evidence_path']
ef=f'{R}/events.csv';new=not os.path.exists(ef)
old=[r for r in (csv.DictReader(open(ef,encoding='utf-8')) if not new else []) if not r['event_id'].startswith(chap_id+'-')]
with open(ef,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,hdr);w.writeheader();[w.writerow(r) for r in old+rows]
# frames
md5=S['md5'];frac=S['frac'];evat={};cur_shot=f'{chap_id}-S00';cur_state=0;fr_rows=[]
for e in E:
    for k in range(e['first'],e['last']+1):evat[k]=e
eidx={e['first']:e for e in E}
for k in range(a,b+1):
    if k in eidx:cur_shot=eidx[k]['shot'];cur_state+=1
    e=evat.get(k)
    if e is not None:
        st='visual_verified' if (k in (e['first'],e['last']) or k in strip_frames) and e['first'] in ann else ('measured_codec_refresh' if e['kind']=='codec_keyframe_refresh' else 'event_interior_measured')
    elif k>0 and md5[k]==md5[k-1]:st='identical_hold_verified'
    else:st='near_identical_hold_measured'
    fr_rows.append([f'F{k:06d}',f'{pts[k]:.6f}',f'{pts[k]-p0:.6f}',chap_id,cur_shot,f'{cur_shot}-st{cur_state:03d}',e['eid'] if e else '',st,f'reference_analysis/01/evidence/{chap_id}'])
ff=f'{R}/frames.csv';exist={}
if os.path.exists(ff):
    for r in csv.reader(open(ff,encoding='utf-8')):
        if r[0]!='frame_id':exist[r[0]]=r
for r in fr_rows:exist[r[0]]=r
with open(ff,'w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh);w.writerow(['frame_id','source_pts_s','video_elapsed_s','chapter_id','shot_id','state_id','active_event_ids','inspection_status','evidence_path'])
    for k in sorted(exist):w.writerow(exist[k])
from collections import Counter
print(chap_id,'events',len(rows),'shots',shot+1,'frames',len(fr_rows),Counter(r[7] for r in fr_rows))
