import wave,json,sys
from pocketsphinx import Decoder
a,b=int(sys.argv[1]),int(sys.argv[2])  # minutes
d=Decoder(samprate=16000);w=wave.open("vo_full.wav");words=[]
for m in range(a,b):
    w.setpos(m*16000*60);data=w.readframes(16000*60)
    if not data:break
    d.start_utt();d.process_raw(data,full_utt=True);d.end_utt()
    words+=[dict(w=s.word.split('(')[0],s=round(m*60+s.start_frame/100,2),e=round(m*60+s.end_frame/100,2)) for s in d.seg() if not s.word.startswith('<') and not s.word.startswith('[')]
json.dump(words,open(f"part_{a:02d}.json","w"))
