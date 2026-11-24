import sys
p=sys.argv[1];h=open(p).read()
def rep(a,b):
    global h
    assert h.count(a)==1,(h.count(a),a[:70]);h=h.replace(a,b)
# quick "cut-in" pop like the reference clips (things just appear, with a tiny settle)
rep("const s=it.noPop?1:back(p/0.28)*0.35+0.65*clamp(p/0.08),op=it.noPop?1:clamp(p/0.06),fl=flipFor(it)?-1:1;",
    "const s=it.noPop?1:back(p/0.16)*0.12+0.88*clamp(p/0.03),op=it.noPop?1:clamp(p/0.03),fl=flipFor(it)?-1:1;")
# feathered photo (archive / scene plate) + thought bubble + plain counter + label-above support
rep(" sfx(){return ''},", r""" sfx(){return ''},
 photo(it,t,p,boil){const L=LIB[it.a]||{w:16,h:9};const w=+it.w||520,hh=w*L.h/L.w,x=+it.x-w/2,y=+it.y-hh/2,f=+it.f||Math.min(w,hh)*0.09,id='ph'+(it.uid||0);
  const op=clamp(p/0.08),gray=it.gray?'filter="url(#bw)"':'';
  return `<g opacity="${op}"><mask id="${id}"><rect x="${x+f}" y="${y+f}" width="${w-2*f}" height="${hh-2*f}" rx="${it.oval?w/2:f}" ry="${it.oval?hh/2:f}" fill="#fff" filter="url(#feather)"/></mask><image href="${src(it.a)}" x="${x}" y="${y}" width="${w}" height="${hh}" preserveAspectRatio="xMidYMid slice" mask="url(#${id})" ${gray}/>${it.cap?`<text x="${+it.x}" y="${y-14}" text-anchor="middle" class="hand" font-size="${+it.cs||34}" fill="${INK}">${esc(it.cap)}</text>`:''}</g>`},
 think(it,t,p,boil,g){const x=+it.x,y=+it.y,w=+it.w||420,hh=+it.h||150,fs=+it.size||34,tx=+it.tx,ty=+it.ty;if(!g.d){let d='';const n=Math.max(8,Math.round((w+hh)/55));for(let i=0;i<n;i++){const a=i/n*Math.PI*2,cx=x+w/2+Math.cos(a)*w/2*0.92,cy=y+hh/2+Math.sin(a)*hh/2*0.88,r=Math.min(w,hh)*0.22;d+=`M${cx-r},${cy}a${r},${r} 0 1,0 ${2*r},0a${r},${r} 0 1,0 ${-2*r},0`}g.d=d}
  const s=back(p/0.2),mx=x+w/2,my=y+hh;const dots=[0.35,0.65].map((q,i)=>`<circle cx="${mx+(tx-mx)*q}" cy="${my+(ty-my)*q}" r="${14-i*5}" fill="#fff" stroke="${INK}" stroke-width="4"/>`).join('');
  return `<g transform="translate(${tx},${ty}) scale(${s}) translate(${-tx},${-ty})" opacity="${clamp(p/0.05)}"><g filter="url(#rough${boil})"><path d="${g.d}" fill="#fff" stroke="${INK}" stroke-width="5"/><ellipse cx="${x+w/2}" cy="${y+hh/2}" rx="${w/2*0.95}" ry="${hh/2*0.9}" fill="#fff"/>${dots}</g>${it.a?`<image href="${src(it.a)}" x="${x+w/2-hh*0.4}" y="${y+hh*0.1}" width="${hh*0.8}" height="${hh*0.8}"/>`:''}${it.t?`<text x="${x+w/2}" y="${y+hh/2+fs*.35}" text-anchor="middle" class="hand" font-size="${fs}" fill="${INK}">${esc(it.t)}</text>`:''}</g>`},""")
rep("<filter id=\"shadow\" x=\"-10%\"","<filter id=\"feather\" x=\"-20%\" y=\"-20%\" width=\"140%\" height=\"140%\"><feGaussianBlur stdDeviation=\"16\"/></filter><filter id=\"bw\"><feColorMatrix type=\"saturate\" values=\"0\"/><feComponentTransfer><feFuncR type=\"linear\" slope=\"1.1\" intercept=\"-0.04\"/><feFuncG type=\"linear\" slope=\"1.1\" intercept=\"-0.04\"/><feFuncB type=\"linear\" slope=\"1.1\" intercept=\"-0.04\"/></feComponentTransfer></filter>\n<filter id=\"shadow\" x=\"-10%\"")
# counter: plain hand-lettered style (no paint block) when it.plain, caption ABOVE like the clips' labels
a="  if(!g.d)g.d=blob(-w/2,-fs*.92,w,fs*1.2,10);const s=back(p/0.25)*0.3+0.7*clamp(p/0.06),col=it.color==='red'?'#E36A55':it.color==='green'?'#CFE3B4':YEL;"
b="""  if(it.plain){const s=back(p/0.16)*0.12+0.88*clamp(p/0.03),col=it.color==='red'?RED:it.color==='green'?'#2E7D32':INK;
   return `<g transform="translate(${it.x},${it.y}) scale(${s})" opacity="${clamp(p/0.03)}">${it.cap?`<text x="0" y="${-fs*.85}" text-anchor="middle" class="hand" font-size="${Math.max(28,Math.round(fs*.3))}" fill="${INK}">${esc(it.cap)}</text>`:''}<text x="0" y="0" text-anchor="middle" class="hand" font-size="${fs}" fill="${col}" stroke="${col}" stroke-width="${fs*0.025}">${esc(txt)}</text></g>`}
  if(!g.d)g.d=blob(-w/2,-fs*.92,w,fs*1.2,10);const s=back(p/0.25)*0.3+0.7*clamp(p/0.06),col=it.color==='red'?'#E36A55':it.color==='green'?'#CFE3B4':YEL;"""
rep(a,b)
# img label above (clip style): it.lab drawn above the sprite top
rep(" return `<g transform=\"translate(${it.x},${it.y}) rotate(${it.rot||0}) scale(${s*fl},${s*breath})\" opacity=\"${op}\"><image href=\"${src(it.a)}\" x=\"${-w/2}\" y=\"${-ax}\" width=\"${w}\" height=\"${h}\" ${it.stone?'filter=\"url(#stone)\"':''}/></g>`},",
    " return `<g transform=\"translate(${it.x},${it.y}) rotate(${it.rot||0}) scale(${s*fl},${s*breath})\" opacity=\"${op}\"><image href=\"${src(it.a)}\" x=\"${-w/2}\" y=\"${-ax}\" width=\"${w}\" height=\"${h}\" ${it.stone?'filter=\"url(#stone)\"':''}/></g>${it.lab?`<text x=\"${it.x}\" y=\"${+it.y-ax+(it.center?0:0)-18}\" text-anchor=\"middle\" class=\"hand\" font-size=\"${+it.ls||32}\" fill=\"${INK}\" opacity=\"${op}\">${esc(it.lab)}</text>`:''}`},")
# header: small stacked lines like the clips (name / date / context)
a=h[h.index("function header(sc){"):h.index("function cam(sc,tq)")]
rep(a,"""function header(sc){const h=sc.h||{};let s='',y=48;for(const [k,fs] of [['a',36],['b',30],['c',30]]){if(h[k]){s+=`<text x="960" y="${y}" text-anchor="middle" class="hand" font-size="${fs}" fill="${INK}">${esc(h[k])}</text>`;y+=fs+4}}return s}
""")
# camera: static by default; zoom punches from sc.z = "t,scale,x,y; ..."
a=h[h.index("function cam(sc,tq)"):h.index("function sceneSVG")]
rep(a,"""function cam(sc,tq){let z=1,cx=960,cy=540;const Z=String(sc.z||'').split(';').map(x=>x.trim()).filter(Boolean).map(x=>x.split(',').map(Number));
 for(const [t,s,x,y] of Z){if(tq<t)break;const q=inout((tq-t)/0.45);z+=(s-z)*q;cx+=((x||960)-cx)*q;cy+=((y||540)-cy)*q}
 if(sc.cam)z*=1+(+sc.cam)*clamp((tq-sc.s)/Math.max(2,sc.e-sc.s));
 if(z===1)return '';return `translate(${960-(cx-960)*(z-1)/z*0},0) translate(${cx},${cy}) scale(${z.toFixed(4)}) translate(${-cx},${-cy})`}
""")
rep("tr=sc.tr||'slide';let body;","tr=sc.tr||'cut';let body;")
rep("const IN_D=0.38;","const IN_D=0.3;")
# editor fields
rep("chapter:['n','t','x','y','size']};","chapter:['n','t','x','y','size'],photo:['a','cap','x','y','w','gray','oval','f'],think:['t','a','x','y','w','h','tx','ty','size']};")
rep("<option value=\"chapter\">Chapter card</option>","<option value=\"chapter\">Chapter card</option><option value=\"photo\">Feathered photo</option><option value=\"think\">Thought bubble</option>")
rep("chapter:{n:1,t:'Chapter title',x:960,y:520}};","chapter:{n:1,t:'Chapter title',x:960,y:520},photo:{a:'B01-01',x:1200,y:480,w:620},think:{t:'…',x:900,y:200,w:380,h:150,tx:700,ty:420}};")
rep("const BOOL=new Set(['flip','center','still','stone','noPop','yellow','italic','typeOn']);","const BOOL=new Set(['flip','center','still','stone','noPop','yellow','italic','typeOn','gray','oval','plain']);")
open(p,'w').write(h);print('ok')
