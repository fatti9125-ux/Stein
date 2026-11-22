import wave,json
from pocketsphinx import Decoder
d=Decoder(samprate=16000)
w=wave.open("vo_full.wav");words=[];CH=16000*60;off=0
while True:
    data=w.readframes(CH)
    if not data:break
    d.start_utt();d.process_raw(data,full_utt=True);d.end_utt()
    words+=[dict(w=s.word.split('(')[0],s=round(off+s.start_frame/100,2),e=round(off+s.end_frame/100,2)) for s in d.seg() if not s.word.startswith('<') and not s.word.startswith('[')]
    off+=60;print('min',off//60,flush=True)
json.dump(words,open("full_words.json","w"))
