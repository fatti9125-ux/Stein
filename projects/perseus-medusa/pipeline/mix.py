# mixes voiceover + sfx cues (read from render/index.html SFX list) -> render/mix.wav
import re,json,numpy as np,scipy.io.wavfile as wf
SR=44100
sr,vo=wf.read('render/vo.wav');vo=vo.astype(np.float32)/32768
if vo.ndim>1:vo=vo.mean(1)
assert sr==SR,sr
cues=json.loads(re.search(r"const SFX=(\[.*?\]);",open('render/index.html').read()).group(1).replace("'",'"'))
gain={'stamp':.32,'crack':.30,'swish':.22,'rewind':.20,'whoosh':.22,'splash':.28,'clang':.30}
fx=np.zeros_like(vo)
for n,t in cues:
    _,s=wf.read(f'sfx/{n}.wav');s=s.astype(np.float32)/32768;i=int(t*SR);L=min(len(s),len(fx)-i);fx[i:i+L]+=s[:L]*gain[n]
out=vo+fx;out=out/max(1,np.max(np.abs(out))/0.97)
wf.write('render/mix.wav',SR,(out*32767).astype(np.int16));print('cues',len(cues))
