// usage: node capture.js <outdir> <fps> [t1,t2,...]   (times list = stills only)
const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname,out=process.argv[2],fps=Number(process.argv[3]||15),list=process.argv[4];
const srv=http.createServer((q,r)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end()}
 r.writeHead(200,{'Content-Type':f.endsWith('.html')?'text/html':f.endsWith('.json')?'application/json':'image/png'});r.end(d)})}).listen(0,async()=>{
 const port=srv.address().port;fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto(`http://127.0.0.1:${port}/index.html`);await p.evaluate(()=>window.ready);await p.waitForTimeout(500);
 const times=list?list.split(',').map(Number):Array.from({length:Math.ceil(74.2*fps)},(_,i)=>i/fps);
 let i=0;for(const t of times){await p.evaluate(t=>window.renderAt(t),t);
  await p.screenshot({path:path.join(out,list?`t_${t}.jpg`:String(i).padStart(5,'0')+'.jpg'),type:'jpeg',quality:92});i++;
  if(!list&&i%150==0)console.log('frame',i,'/',times.length)}
 await b.close();srv.close();});
