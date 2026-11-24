import json,re,difflib
W=[];[W.extend(json.load(open(f))) for f in ['part_00.json','part_04.json','part_08.json','part_11.json']]
W.sort(key=lambda w:w['s']);json.dump(W,open('words_raw.json','w'))
txt=open('script.md',encoding='utf-8').read()
body=txt.split('## SCRIPT')[1].split('## Fact-check')[0]
lines=[l for l in body.split('\n') if l.strip() and not l.strip().startswith('[') and not l.startswith('*[') and not l.startswith('---')]
toks=[];chap=[]
for l in lines:
    if l.startswith('### '):chap.append((len(toks),l[4:].strip()));continue
    for t in re.findall(r"[\w$€¢'’.,%\-]+",l):
        n=re.sub(r"[^a-z0-9]","",t.lower().replace('’',"'"))
        if n:toks.append(dict(w=t.strip('.,'),n=n))
norm=lambda w:re.sub(r"[^a-z0-9]","",w.lower())
R=[norm(w['w']) for w in W]
sm=difflib.SequenceMatcher(None,[t['n'] for t in toks],R,autojunk=False)
m=0
for a,b,n in sm.get_matching_blocks():
    for k in range(n):toks[a+k]['s']=W[b+k]['s'];toks[a+k]['e']=W[b+k]['e'];m+=1
# interpolate
idx=[i for i,t in enumerate(toks) if 's' in t]
for i,t in enumerate(toks):
    if 's' in t:continue
    p=max([j for j in idx if j<i],default=None);q=min([j for j in idx if j>i],default=None)
    if p is None:t['s']=toks[q]['s'];
    elif q is None:t['s']=toks[p]['e']
    else:t['s']=round(toks[p]['e']+(toks[q]['s']-toks[p]['e'])*(i-p)/(q-p),2)
    t['e']=t['s']+.2;t['interp']=1
print('script words',len(toks),'matched',m,'recognized',len(W),'last',toks[-1]['s'])
for i,c in chap:print(round(toks[i]['s'],1),c)
json.dump(toks,open('script_words.json','w'))
# transcript for editor (script words with times)
json.dump([dict(w=t['w'],s=t['s'],e=t['e']) for t in toks],open('transcript.json','w'))
