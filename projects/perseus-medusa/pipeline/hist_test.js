const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..','editor');
const srv=http.createServer((q,r)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end()}
 const t=f.endsWith('.html')?'text/html; charset=utf-8':f.endsWith('.json')?'application/json':f.endsWith('.mp3')?'audio/mpeg':'image/webp';r.writeHead(200,{'Content-Type':t});r.end(d)})}).listen(0,async()=>{
 const port=srv.address().port;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:900}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{const S=window.__S={};
  const snap=(id,v)=>({id,exists:!!v,data:()=>v?JSON.parse(JSON.stringify(v)):undefined,metadata:{}});
  const docRef=path=>({get:async()=>snap(path.split('/').pop(),S[path]),set:async d=>{S[path]=JSON.parse(JSON.stringify(d))},collection:c=>coll(path+'/'+c)});
  const coll=(path,o={})=>({path,doc:id=>docRef(path+'/'+id),orderBy:(f,dir)=>coll(path,{...o,f,dir}),limit:n=>coll(path,{...o,n}),
   get:async()=>{let ks=Object.keys(S).filter(k=>k.startsWith(path+'/')&&k.split('/').length===path.split('/').length+1);let ds=ks.map(k=>snap(k.split('/').pop(),S[k]));
    if(o.f)ds.sort((a,b)=>(a.data()[o.f]>b.data()[o.f]?1:-1)*(o.dir==='desc'?-1:1));return{docs:ds,size:ds.length,empty:!ds.length}}});
  window.__dl=[];window.claude={use:async n=>n==='db'?{doc:docRef,collection:coll}:n==='downloads'?{save:async x=>window.__dl.push(x)}:null}});
 await p.goto(`http://127.0.0.1:${port}/index.html`);await p.waitForTimeout(2500);
 console.log('status0',await p.textContent('#status'));
 // edit 1: move an item via data, then save with note
 await p.evaluate(()=>{BOARD.scenes[0].items[0].x+=50;markDirty()});await p.fill('#saveNote','Moved Perseus right');await p.click('#btnSave');await p.waitForTimeout(500);
 console.log('status1',await p.textContent('#status'));
 await p.evaluate(()=>{BOARD.scenes[1].items.pop();markDirty()});await p.click('#btnSave');await p.waitForTimeout(500);
 await p.click('#btnHist');await p.waitForTimeout(500);
 console.log('hist',(await p.textContent('#histList')).replace(/\s+/g,' '));
 await p.screenshot({path:'hist_check.png'});
 await p.click('#histLog');await p.click('#histAll');await p.waitForTimeout(500);
 const dl=await p.evaluate(()=>window.__dl.map(x=>x.filename+' '+x.data.length));console.log('downloads',dl);
 // open older version
 await p.locator('.hrow').nth(1).getByText('Open').click();await p.waitForTimeout(300);
 console.log('status2',await p.textContent('#status'),await p.evaluate(()=>BOARD.scenes[1].items.length));
 // reload: should load latest saved
 const S=await p.evaluate(()=>window.__S);
 const p2=await b.newPage({viewport:{width:1400,height:900}});await p2.addInitScript(s=>{window.__seed=s},S);
 await p2.addInitScript(()=>{const S=window.__seed;const snap=(id,v)=>({id,exists:!!v,data:()=>v,metadata:{}});const docRef=path=>({get:async()=>snap(path,S[path]),set:async d=>{S[path]=d}});
  window.claude={use:async n=>n==='db'?{doc:docRef,collection:()=>({})}:null}});
 await p2.goto(`http://127.0.0.1:${port}/index.html`);await p2.waitForTimeout(2500);
 console.log('reload',await p2.textContent('#status'),await p2.evaluate(()=>[BOARD.scenes[1].items.length,BOARD.scenes[0].items[0].x]));
 console.log('errors',errs);await b.close();srv.close()});
