const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..','editor');const types={'.html':'text/html','.json':'application/json','.webp':'image/webp','.mp3':'audio/mpeg'};
const srv=http.createServer((q,r)=>{let f=path.join(root,decodeURIComponent(q.url.split('?')[0]));if(f.endsWith('/'))f+='index.html';fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end()}r.writeHead(200,{'Content-Type':types[path.extname(f)]||'application/octet-stream'});r.end(d)})}).listen(0,async()=>{
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:960}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto(`http://127.0.0.1:${srv.address().port}/index.html`);await p.waitForTimeout(2500);
 await p.evaluate(()=>{document.querySelector('#scrub').value=21.5;document.querySelector('#scrub').dispatchEvent(new Event('input'))});await p.waitForTimeout(400);
 await p.click('#items div:nth-child(6)');await p.waitForTimeout(600);
 await p.screenshot({path:'editor_check.png'});
 const m=await b.newPage({viewport:{width:400,height:860}});await m.goto(`http://127.0.0.1:${srv.address().port}/index.html`);await m.waitForTimeout(2000);await m.screenshot({path:'editor_phone.png'});
 const ow=await m.evaluate(()=>document.documentElement.scrollWidth);console.log('phone scrollWidth',ow,'errors',errs);await b.close();srv.close()});
