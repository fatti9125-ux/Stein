import wave,json
from pocketsphinx import Decoder
d=Decoder(samprate=16000)
w=wave.open("vo75.wav");data=w.readframes(w.getnframes())
d.start_utt();d.process_raw(data,full_utt=True);d.end_utt()
words=[dict(w=s.word,s=round(s.start_frame/100,2),e=round(s.end_frame/100,2)) for s in d.seg() if not s.word.startswith('<') and s.word not in('[NOISE]',)]
json.dump(words,open("ps_words.json","w"))
line=[];t0=0
for x in words:
    line.append(x['w'].split('(')[0])
    if len(line)>=12: print(f"{t0:6.2f} {' '.join(line)}");line=[];t0=x['e']
print(f"{t0:6.2f} {' '.join(line)}")
