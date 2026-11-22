const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:Number(process.argv[2]||1),viewport:{width:1320,height:2300}});
await p.goto('file://'+__dirname+'/frames.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
for(const id of ['f1','f2','f3'])await (await p.$('#'+id)).screenshot({path:`${id}.png`});await b.close()})();
