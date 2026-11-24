import json,wave,re,numpy as np
from pocketsphinx import Decoder
T=json.load(open('script_words.json'))
SP={'350':['three hundred and fifty','three hundred fifty'],'2008':'two thousand eight','2012':'two thousand twelve','2016':'two thousand sixteen','2021':'twenty twenty one',
'38':'thirty eight','$7.40':'seven dollars and forty cents','$4.70':'four dollars and seventy cents','$16.90':'sixteen dollars and ninety cents','2018':'twenty eighteen',
'30-year-old':'thirty year old','€15.90':'fifteen euros ninety','20':'twenty','6-foot-6':'six foot six','350-pound':'three hundred fifty pound','$2.25':'two dollars and twenty five cents',
'29th':'twenty ninth','2022':'twenty twenty two','40':'forty','47':'forty seven','6':'six','$2.50':'two dollars fifty','2006':'two thousand six','74':'seventy four','92':'ninety two',
'$175':'one hundred seventy five','5':'five','25':'twenty five','2020':'twenty twenty','1980s':'nineteen eighties','2000':'two thousand','35':'thirty five','$7.5':'seven point five',
'$12':'twelve','200':'two hundred','70':'seventy','2025':'twenty twenty five','348':'three hundred forty eight'}
seen={}
def spoken(i):
    w=T[i]['w'].replace('’',"'")
    if w in SP:
        v=SP[w]
        if isinstance(v,list):k=seen.get(w,0);seen[w]=k+1;v=v[min(k,len(v)-1)]
        out=v.split()
        if w.startswith('$') and i+1<len(T) and T[i+1]['w'].lower().startswith('million'):pass
        return out
    out=[]
    for p in w.split('-'):
        p=re.sub(r"[^a-z']","",p.lower()).strip("'")
        if p:out.append(p)
    return out
SPW=[spoken(i) for i in range(len(T))]
# "$12 million" / "$175 million" / "$7.5 million" are read "... million dollars": add 'dollars' after million
for i in range(len(T)-1):
    if T[i]['w'].startswith('$') and T[i+1]['w'].lower().startswith('million'):SPW[i+1]=['million','dollars']
d=Decoder(samprate=16000,loglevel='ERROR')
PH={'jaroslav':'Y AA R AH S L AA V','landshut':'L AE N D Z HH UW T','thiensville':'TH IY N Z V IH L','wisth':'W IH S TH','souplantation':'S UW P L AE N T EY SH AH N',
'triathlete':'T R AY AE TH L IY T','triathletes':'T R AY AE TH L IY T S','sirloin':'S ER L OY N','bodybuilder':'B AA D IY B IH L D ER','corrals':'K ER AE L Z',
'bensalem':'B EH N S EY L AH M','bobrowski':'B AH B R AO F S K IY','hometown':'HH OW M T AW N','meatloaf':'M IY T L OW F','sushi':'S UW SH IY','modeled':'M AA D AH L D',
'skimping':'S K IH M P IH NG','nuggets':'N AH G AH T S','fifty':'F IH F T IY',"chuck's":'CH AH K S','golden':'G OW L D AH N','corral':'K ER AE L',"hustle's":'HH AH S AH L Z'}
for wd in sorted({x for s in SPW for x in s}):
    if d.lookup_word(wd) is None:
        if wd in PH:d.add_word(wd,PH[wd],False)
        elif wd.endswith("'s") and (d.lookup_word(wd[:-2]) or PH.get(wd[:-2])):d.add_word(wd,(d.lookup_word(wd[:-2]) or PH[wd[:-2]])+' Z',False)
        else:print('OOV no phones:',wd)
w=wave.open('vo_full.wav');SR=16000;audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16);DUR=len(audio)/SR
sents=[];cur=[]
for i,t in enumerate(T):
    cur.append(i)
    if t.get('end') or i==len(T)-1:sents.append(cur);cur=[]
def align(idx,a,b):
    words=[x for i in idx for x in SPW[i]]
    seg=audio[int(a*SR):int(b*SR)].tobytes()
    d.set_align_text(' '.join(words));d.start_utt();d.process_raw(seg,full_utt=True);d.end_utt()
    out=[(re.sub(r'\(\d+\)','',s.word),a+s.start_frame/100,a+(s.end_frame+1)/100) for s in d.seg() if not s.word.startswith(('<','['))]
    if [o[0] for o in out]!=words:return None
    return out
new={};a=0.0;fails=0
for k,s in enumerate(sents):
    nxt=sents[k+1] if k+1<len(sents) else []
    idx=s+nxt;b=min(DUR,max(T[idx[-1]]['e'],a+1)+1.5)
    r=align(idx,max(0,a-0.1),b)
    if r is None and nxt:r=align(s,max(0,a-0.1),min(DUR,T[s[-1]]['e']+1.2))
    if r is None:
        fails+=1
        for i in s:new[i]=(T[i]['s'],T[i]['e'],0)
        a=T[s[-1]]['e'];continue
    j=0
    for i in s:
        n=len(SPW[i])
        if n==0:new[i]=(new[i-1][1],new[i-1][1],1);continue
        new[i]=(round(r[j][1],2),round(r[j+n-1][2],2),1);j+=n
    a=new[s[-1]][1]
diff=[new[i][0]-T[i]['s'] for i in new if new[i][2]]
print('sentences',len(sents),'failed',fails,'aligned words',sum(v[2] for v in new.values()),'/',len(T))
print('old-vs-new: mean',round(float(np.mean(diff)),2),'median abs',round(float(np.median(np.abs(diff))),2),'p90 abs',round(float(np.percentile(np.abs(diff),90)),2),'max',round(float(max(diff,key=abs)),2))
for i,t in enumerate(T):t['s'],t['e'],t['fa']=new[i]
json.dump(T,open('script_words_fa.json','w'))
