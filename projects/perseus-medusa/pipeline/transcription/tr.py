from faster_whisper import WhisperModel
m=WhisperModel("small.en",device="cpu",compute_type="int8")
segs,_=m.transcribe("vo75.wav",word_timestamps=True)
import json;out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
    out+= [dict(w=w.word.strip(),s=round(w.start,2),e=round(w.end,2)) for w in s.words]
json.dump(out,open("words.json","w"))
