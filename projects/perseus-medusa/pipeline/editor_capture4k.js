// node editor_capture.js <outdir> <fps|list> [start] [end]
const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..','editor'),out=process.argv[2],mode=process.argv[3],t0=+(process.argv[4]||0),t1=+(process.argv[5]||0);
const types={'.html':'text/html','.json':'application/json','.webp':'image/webp','.mp3':'audio/mpeg'};
const srv=http.createServer((q,r)=>{let f=path.join(root,decodeURIComponent(q.url.split('?')[0]));if(f.endsWith('/'))f+='index.html';fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end()}r.writeHead(200,{'Content-Type':types[path.extname(f)]||'application/octet-stream'});r.end(d)})}).listen(0,async()=>{
 const port=srv.address().port;fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:2});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.addInitScript(()=>{window.__RENDER__=true});
 await p.goto(`http://127.0.0.1:${port}/index.html`);await p.waitForFunction(()=>window.boardReady,null,{timeout:120000});await p.waitForTimeout(300);
 const stage=await p.$('.stagebox');
 let times;if(mode.includes(','))times=mode.split(',').map(Number);else{const fps=+mode;times=[];for(let f=Math.round(t0*fps);f<Math.round(t1*fps);f++)times.push(f/fps)}
 let i=0;for(const t of times){await p.evaluate(t=>window.renderAt(t),t);
  await stage.screenshot({path:path.join(out,mode.includes(',')?`t_${t}.jpg`:String(Math.round(t*+mode)).padStart(6,'0')+'.jpg'),type:'jpeg',quality:90});
  if(++i%300==0)console.log(out,i,'/',times.length)}
 await b.close();srv.close();});
