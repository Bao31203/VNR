"""Check recording playback rate/alignment and sample-level quiet windows."""
from pathlib import Path
import json
import wave
import numpy as np

output=Path(__file__).resolve().parents[1]/'out/history-1946-v2'
plan=json.loads((output/'timeline.json').read_text(encoding='utf-8'))
def read(path):
    with wave.open(str(path),'rb') as w:
        sr=w.getframerate();channels=w.getnchannels()
        signal=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
    return sr,signal.reshape(-1,channels).mean(axis=1)
sr,original=read(output/'voice/c08-recording.wav')
_,padded=read(output/'voice/c08-padded.wav')
lead=round(plan['scenes'][7]['voStart']*sr)
margin=round(.05*sr)
reference=original[margin:-margin]
aligned=padded[lead+margin:lead+len(original)-margin]
correlation=float(np.corrcoef(reference,aligned)[0,1])
assert correlation>.99999,correlation
assert abs(len(original)/sr-26.42)<1/sr
mix_sr,mix=read(output/'mix.wav')
quiet=[]
for interval in [*plan['quietWindows'],plan['blackouts'][-1]]:
    signal=mix[round(interval['start']*mix_sr):round(interval['end']*mix_sr)]
    peak=float(np.max(np.abs(signal)))
    quiet.append({**interval,'peak':peak,'peakDbFS':float(20*np.log10(max(peak,1e-12)))})
    assert peak<1e-4,(interval,peak)
report={'passed':True,'sourceClipDuration':len(original)/sr,'playbackRate':1.0,'recordingToPaddedCorrelation':correlation,'quietWindows':quiet}
(output/'qa/recording-alignment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report))
