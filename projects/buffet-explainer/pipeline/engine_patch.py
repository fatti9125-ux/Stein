import sys
p=sys.argv[1];h=open(p).read()
def rep(a,b,cnt=1):
    global h
    assert h.count(a)==cnt,(h.count(a),a[:70]);h=h.replace(a,b)

# ---- new renderers (counter, bars, icons, chapter) + sticker/stamp idle wobble
rep(" sfx(){return ''},", r""" sfx(){return ''},
 counter(it,t,p,boil,g){const dur=+it.dur||1.1,q=out3(p/dur),f=+it.from||0,to=+it.to||0,dec=+it.dec||0;const v=f+(to-f)*q;
  const fin=(it.pre||'')+fmtNum(to,dec)+(it.suf||''),txt=(it.pre||'')+fmtNum(v,dec)+(it.suf||''),fs=+it.size||120,w=Math.max(fin.length*fs*.5+70,fs*1.6);
  if(!g.d)g.d=blob(-w/2,-fs*.92,w,fs*1.2,10);const s=back(p/0.25)*0.3+0.7*clamp(p/0.06),col=it.color==='red'?'#E36A55':it.color==='green'?'#CFE3B4':YEL;
  return `<g transform="translate(${it.x},${it.y}) rotate(${(it.rot??-2)+[0,.4,-.3][boil]}) scale(${s})" opacity="${clamp(p/0.05)}"><g filter="url(#shadow)"><path d="${g.d}" fill="${col}" filter="url(#paint)"/></g><text x="0" y="${fs*.06}" text-anchor="middle" class="anton" font-size="${fs}" fill="${INK}" letter-spacing="1">${esc(txt)}</text>${it.cap?`<text x="0" y="${fs*.36+30}" text-anchor="middle" class="type" font-size="${Math.max(26,Math.round(fs*.25))}" fill="${INK}" opacity="${clamp((p-0.3)/0.3)}">${esc(it.cap)}</text>`:''}</g>`},
 bars(it,t,p,boil){const rows=parseRows(it.rows),x=+it.x,y=+it.y,W=+it.w||900,rh=+it.rh||80,lw=+it.lw||260,max=+it.max||Math.max(...rows.map(r=>r.v),1),stag=+it.stag||0.5;let s='';
  if(it.title)s+=`<text x="${x}" y="${y-36}" class="serif" font-size="${+it.ts||46}" fill="${INK}" opacity="${clamp(p/0.15)}">${esc(it.title)}</text>`;
  rows.forEach((r,i)=>{const st=i*stag;if(p<st)return;const q=out3((p-st)/0.9),yy=y+i*(rh+26),bw=Math.max(6,(W-lw)*(r.v/max)*q),col=r.c==='r'?'#E36A55':r.c==='g'?'#9CC47E':r.c==='b'?'#7FB6D6':YEL;
   s+=`<text x="${x+lw-18}" y="${yy+rh*.66}" text-anchor="end" class="hand" font-size="${Math.round(rh*.5)}" fill="${INK}" opacity="${clamp((p-st)/0.15)}">${esc(r.l)}</text>`;
   s+=`<g filter="url(#rough${boil})"><rect x="${x+lw}" y="${yy}" width="${bw}" height="${rh}" fill="${col}" stroke="${INK}" stroke-width="4"/></g>`;
   s+=`<text x="${x+lw+bw+16}" y="${yy+rh*.68}" class="anton" font-size="${Math.round(rh*.55)}" fill="${INK}" opacity="${clamp((p-st-0.3)/0.3)}">${esc(r.t!=null?r.t:fmtNum(r.v*q,0))}</text>`});
  return s},
 icons(it,t,p){const n=+it.n||20,cols=+it.cols||10,sz=+it.sz||84,gap=+it.gap||22,stag=+it.stag||0.05,hi=new Set(String(it.hi??'').split(',').filter(x=>x!=='').map(Number));let s='';
  const tw=cols*sz+(cols-1)*gap,x0=+it.x-tw/2+sz/2;
  for(let i=0;i<n;i++){const st=i*stag;if(p<st)continue;const q=back((p-st)/0.25),cx=x0+(i%cols)*(sz+gap),cy=+it.y+Math.floor(i/cols)*(sz*1.2+gap),isH=hi.has(i)&&p>=(+it.hiAt||0);
   s+=`<g transform="translate(${cx},${cy}) scale(${q*(isH?1.15:1)})"><image href="${src(isH?(it.b||'G02-03'):(it.a||'G02-02'))}" x="${-sz/2}" y="${-sz*.6}" width="${sz}" height="${sz*1.2}"/></g>`}
  return s},
 chapter(it,t,p,boil,g){const x=+it.x||960,y=+it.y||520,w=+it.w||1380,hh=+it.h||330;if(!g.d){g.d=torn(x-w/2,y-hh/2,w,hh,6);g.b=blob(x-w/2-40,y-hh/2-30,w+80,hh+60,14)}
  const s=back(p/0.3)*0.25+0.75,r=(1-out3(p/0.3))*3-1,op=clamp(p/0.06),title=String(it.t||''),n=Math.floor(clamp((p-0.25)/(title.length*0.025))*title.length);
  return `<g transform="translate(${x},${y}) rotate(${r}) scale(${s}) translate(${-x},${-y})" opacity="${op}"><path d="${g.b}" fill="${YEL}" filter="url(#paint)"/><g filter="url(#shadow)"><path d="${g.d}" fill="${PAPER}"/></g><text x="${x}" y="${y-60}" text-anchor="middle" class="type" font-size="34" fill="${INK}" letter-spacing="6">${esc(it.n?'CHAPTER '+it.n:'')}</text><text x="${x}" y="${y+40}" text-anchor="middle" class="serif" font-size="${+it.size||70}" fill="${INK}">${esc(title.slice(0,n))}</text></g>`},""")
rep("const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));","""const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const fmtNum=(v,d=0)=>Number(v).toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const inout=p=>{p=clamp(p);return p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2};
function parseRows(r){if(Array.isArray(r))return r;return String(r||'').split(';').map(x=>x.trim()).filter(Boolean).map(x=>{const [l,v,t,c]=x.split('|');return {l:l||'',v:+v||0,t:t||null,c:c||'y'}})}
function parseMv(m){if(Array.isArray(m))return m;return String(m||'').split(';').map(x=>x.trim()).filter(Boolean).map(x=>{const [t,dx,dy,s]=x.split(',').map(Number);return {t,dx:dx||0,dy:dy||0,s:isNaN(s)?1:s}})}""")
# idle wobble on stickers
rep(" return `<g transform=\"translate(${it.x},${it.y}) rotate(${it.rot??-3}) scale(${s})\" opacity=\"${clamp(p/0.05)}\"><g filter=\"url(#shadow)\">",
    " return `<g transform=\"translate(${it.x},${it.y}) rotate(${(it.rot??-3)+[0,.5,-.4][boil]}) scale(${s})\" opacity=\"${clamp(p/0.05)}\"><g filter=\"url(#shadow)\">")

# ---- frame composer: entrances, exits, make-room moves, camera push, transitions, chapter tab
a=h[h.index("function frameSVG(t,opts={}){"):h.index("/* ================= editor")]
b=r"""function anchorOf(it){if(it.k==='card'||it.k==='archive'){const L=LIB[it.a]||{w:4,h:3};const w=+it.w||400,hh=it.k==='card'?+it.h:w*L.h/L.w;return [+it.x+w/2,+it.y+hh/2]}
 if(it.k==='arrow')return [(+it.x+ +it.x2)/2,(+it.y+ +it.y2)/2];if(it.k==='bubble')return [+it.x+ +it.w/2,+it.y+ +it.h/2];if(it.k==='img'&&!it.center)return [+it.x,+it.y-(+it.h||300)/2];return [+it.x||960,+it.y||540]}
const IN_D=0.38;
function itemSVG(sc,it,i,tq,boil,opts){
 const outT=(it.out!=null&&it.out!=='')?+it.out:null,started=tq>=it.at-1e-6,gone=outT!=null&&tq>=outT+0.22;
 const forced=opts.sel===i&&(!started||gone)&&it.k!=='sfx';
 if(!(started&&!gone)&&!forced)return '';
 const p=forced?5:tq-it.at;seed=(it.uid||i)*977+13;
 let s='';try{s=R[it.k]?R[it.k](it,tq,p,boil,geo(it)):''}catch(e){s=''}
 if(!s)return '';
 const [ax,ay]=anchorOf(it);let tf='',op=1;
 if(!forced){
  if(it.in&&it.in!=='pop'&&p<IN_D){const q=1-out3(p/IN_D),d={left:[-1300,0],right:[1300,0],up:[0,-900],down:[0,900]}[it.in]||[0,0];tf+=`translate(${d[0]*q},${d[1]*q}) `}
  const mv=parseMv(it.mv);if(mv.length){let dx=0,dy=0,sc2=1;for(const m of mv){if(tq<m.t)break;const q=inout((tq-m.t)/0.5);dx+=(m.dx-dx)*q;dy+=(m.dy-dy)*q;sc2+=(m.s-sc2)*q}
   if(dx||dy||sc2!==1)tf+=`translate(${ax+dx},${ay+dy}) scale(${sc2}) translate(${-ax},${-ay}) `}
  if(outT!=null&&tq>=outT){const q=clamp((tq-outT)/0.22);op=1-q;tf+=`translate(${ax},${ay}) scale(${1-0.25*q}) translate(${-ax},${-ay}) `}
 }
 return `<g data-i="${i}" class="it"${forced?' opacity=".35"':op<1?` opacity="${op.toFixed(2)}"`:''}${tf?` transform="${tf}"`:''}>${s}</g>`}
function header(sc){const h=sc.h||{};return h.a?`<text x="960" y="62" text-anchor="middle" class="hand" font-size="44" fill="${INK}">${esc(h.a)}</text>${h.b?`<text x="960" y="104" text-anchor="middle" class="hand" font-size="34" fill="${INK}" opacity=".8">${esc(h.b)}</text>`:''}`:''}
function cam(sc,tq){if(sc.cam===0)return '';const d=Math.max(2,sc.e-sc.s),z=1+(+sc.cam||0.035)*clamp((tq-sc.s)/d);return `translate(960,560) scale(${z.toFixed(4)}) translate(-960,-560)`}
function sceneSVG(si,tq,boil,opts){const sc=BOARD.scenes[si];let b='';sc.items.forEach((it,i)=>{b+=itemSVG(sc,it,i,tq,boil,opts)});return `<g transform="${cam(sc,tq)}">${b}</g>${header(sc)}`}
function chapterTab(tq){const C=BOARD.chapters||[];let c=null;for(const x of C)if(tq>=x.s)c=x;if(!c||tq<c.s+(+c.d||3))return '';const op=clamp((tq-c.s-(+c.d||3))/0.3);
 return `<g opacity="${op}"><text x="40" y="1050" class="type" font-size="22" fill="${INK}" opacity=".7">${esc(c.n+' · '+c.t)}</text></g>`}
const TR=0.45;
function frameSVG(t,opts={}){
 const tq=Math.floor(t*15)/15,frame=Math.round(tq*15),boil=Math.floor(frame/3)%3;
 const si=sceneAt(tq),sc=BOARD.scenes[si],inT=tq-sc.s,tr=sc.tr||'slide';let body;
 if(si>0&&inT<TR&&tr!=='cut'&&opts.sel==null){const prev=sceneSVG(si-1,tq,boil,{}),cur=sceneSVG(si,tq,boil,opts),e=inout(inT/TR);
  if(tr==='wipe'){const bx=-2600+5200*e;body=(e<0.5?prev:cur)+`<g transform="translate(${bx},0) rotate(-4 960 540)"><rect x="-300" y="-200" width="2600" height="1500" fill="${YEL}" filter="url(#paint)"/></g>`}
  else if(tr==='up'){body=`<g transform="translate(0,${-1080*e})">${prev}</g><g transform="translate(0,${1080*(1-e)})">${cur}</g>`}
  else body=`<g transform="translate(${-1920*e},0)">${prev}</g><g transform="translate(${1920*(1-e)},0)">${cur}</g>`}
 else body=sceneSVG(si,tq,boil,opts);
 return `${defs(boil)}<rect width="1920" height="1080" fill="${SKY}"/><rect width="1920" height="1080" filter="url(#grain)" pointer-events="none"/>${body}${chapterTab(tq)}`;
}

"""
h=h.replace(a,b)
# editor: selection overlay should be in stage coords -> use getBBox of transformed element via getCTM; keep simple: ok
# ---- editor fields for new kinds
rep("hl:{x:860,y:560,w:300,h:32},xmark:{x:960,y:540,s:50},sfx:{a:'stamp',vol:0.6}};",
    "hl:{x:860,y:560,w:300,h:32},xmark:{x:960,y:540,s:50},sfx:{a:'stamp',vol:0.6},\n counter:{pre:'$',from:0,to:17,dec:0,suf:'',cap:'caption',x:960,y:460,size:130},bars:{title:'Title',rows:'Chicken|47|47M lb|y;Steak|6|6M lb|r',x:420,y:420,w:1100,rh:80,lw:260},\n icons:{n:20,cols:10,sz:84,hi:'19',x:960,y:420},chapter:{n:1,t:'Chapter title',x:960,y:520}};")
rep("arrow:['x','y','x2','y2','bend','color'],loop:['x','y','rx','ry','color','sw'],hl:['x','y','w','h','rot'],xmark:['x','y','s'],sfx:['a','vol']};",
    "arrow:['x','y','x2','y2','bend','color'],loop:['x','y','rx','ry','color','sw'],hl:['x','y','w','h','rot'],xmark:['x','y','s'],sfx:['a','vol'],\n counter:['pre','from','to','dec','suf','cap','x','y','size','rot','dur','color'],bars:['title','rows','x','y','w','rh','lw','max','stag'],icons:['n','cols','hi','hiAt','x','y','sz','gap','stag','a','b'],chapter:['n','t','x','y','size']};\nfor(const k in FIELDS)if(k!=='sfx'){FIELDS[k].push('in','mv')}")
rep("const NUM=new Set(['x','y','h','w','rot','size','x2','y2','bend','rx','ry','sw','s','tx','ty','vol']);",
    "const NUM=new Set(['x','y','h','w','rot','size','x2','y2','bend','rx','ry','sw','s','tx','ty','vol','from','to','dec','dur','rh','lw','max','stag','n','cols','sz','gap','hiAt']);")
rep("anchor:'Align'};","anchor:'Align',pre:'Prefix',suf:'Suffix',from:'Count from',to:'Count to',dec:'Decimals',dur:'Count time (s)',rows:'Rows (label|value|shown|colour; …)',rh:'Row height',lw:'Label width',max:'Scale max',stag:'Stagger (s)',n:'Count',cols:'Columns',hi:'Highlighted (0-based, comma)',hiAt:'Highlight at (s after appear)',sz:'Icon size',gap:'Gap',b:'Highlight icon',in:'Enters from',mv:'Make-room moves (t,dx,dy,scale; …)'};")
rep('<option value="hl">Highlighter</option><option value="xmark">Red X</option><option value="sfx">Sound effect</option>',
    '<option value="hl">Highlighter</option><option value="xmark">Red X</option><option value="counter">Counting number</option><option value="bars">Bar chart</option><option value="icons">Icon grid</option><option value="chapter">Chapter card</option><option value="sfx">Sound effect</option>')
# 'in' select + rows/mv wide text inputs in item panel
rep("  if(k==='t'||k==='cap')return `<label style=\"grid-column:1/-1\">",
    "  if(k==='in')return `<label>${NAMES[k]}<select data-f=\"in\">${['pop','left','right','up','down'].map(c=>`<option ${c===(v||'pop')?'selected':''}>${c}</option>`).join('')}</select></label>`;\n  if(k==='rows'||k==='mv'||k==='title')return `<label style=\"grid-column:1/-1\">${NAMES[k]||k}<input type=\"text\" data-f=\"${k}\" value=\"${esc(v??'')}\"></label>`;\n  if(k==='t'||k==='cap')return `<label style=\"grid-column:1/-1\">")
open(p,'w').write(h);print('patched')
