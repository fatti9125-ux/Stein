# voiceover + every sfx element in the storyboard -> mix_full.wav
import json,sys,numpy as np,scipy.io.wavfile as wf,subprocess
board=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'editor/storyboard.json'))
subprocess.run(['ffmpeg','-v','error','-y','-i','/root/.claude/uploads/00440a20-9369-5308-8642-4b0451bc0d58/e194e43d-Buffet_voiceover___Casper.mp3','-ac','1','-ar','44100','vo_full44.wav'],check=True)
SR,vo=wf.read('vo_full44.wav');vo=vo.astype(np.float32)/32768
fx=np.zeros_like(vo);n=0
for sc in board['scenes']:
    for it in sc['items']:
        if it.get('k')!='sfx':continue
        _,s=wf.read(f"sfx_wav/{it['a']}.wav");s=s.astype(np.float32)/32768;i=int(float(it['at'])*SR);L=min(len(s),len(fx)-i)
        if L>0:fx[i:i+L]+=s[:L]*0.5*float(it.get('vol',0.6));n+=1
out=vo+fx;out/=max(1,np.max(np.abs(out))/0.97)
wf.write('mix_full.wav',SR,(out*32767).astype(np.int16));print('sfx cues',n)
