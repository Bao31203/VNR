"""Check recording playback rate/alignment and sample-level quiet windows."""
from pathlib import Path
import json
import wave
import hashlib
import numpy as np

output=Path(__file__).resolve().parents[1]/'out/history-1946-v4'
plan=json.loads((output/'timeline.json').read_text(encoding='utf-8'))
previous=json.loads((output.parent/'history-1946-v2/timeline.json').read_text(encoding='utf-8'))
events=json.loads((output/'sfx-events.json').read_text(encoding='utf-8'))
assert not any(e['type'] in ('type-return','type-bell') for e in events)
ultimatum=[e for e in events if e['scene']=='C4']
assert ultimatum and all(e['type'] in ('type-key','type-space') for e in ultimatum)
assert all(e['type'] in ('type-key','type-space') for e in events if e['scene']=='C11')
comparison=plan['scenes'][8]
elements={e['id']:e for e in comparison['elements']}
readiness=[]
for element_id,spoken_at in [('c9-viet-quoc-quan',5.92),('c9-tu-ve',8.48)]:
    element=elements[element_id]
    complete=element['charFrames'][-1]/30
    assert complete<=spoken_at,(element_id,complete,spoken_at)
    readiness.append({'element':element_id,'text':element['text'],'fullyVisible':complete,'spokenAt':spoken_at,'globalFullyVisible':comparison['start']+complete})
assert elements['c9-num-r']['runtimeIn']+1.2<=10.32
v3=json.loads((output.parent/'history-1946-v3/timeline.json').read_text(encoding='utf-8'))
assert [(s['start'],s['end']) for s in plan['scenes']]==[(s['start'],s['end']) for s in v3['scenes']]
assert hashlib.sha256((output/'voice.wav').read_bytes()).digest()==hashlib.sha256((output.parent/'history-1946-v3/voice.wav').read_bytes()).digest()
assert abs(previous['duration']-plan['duration']-5)<1e-6
assert plan['scenes'][1]['voiceDuration']==previous['scenes'][1]['voiceDuration']
assert plan['scenes'][1]['voStart']+plan['scenes'][1]['voiceDuration']<plan['scenes'][1]['duration']
for new,old in zip(plan['scenes'][2:],previous['scenes'][2:]):
    assert abs(old['start']-new['start']-5)<1e-6
image_source=Path('C:/Users/pgb31/Downloads/OIP (2).webp')
image_asset=output.parents[1]/'templates/history-v4/assets/a10.webp'
image_hash=hashlib.sha256(image_source.read_bytes()).hexdigest()
assert hashlib.sha256(image_asset.read_bytes()).hexdigest()==image_hash
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
report={'passed':True,'sourceClipDuration':len(original)/sr,'playbackRate':1.0,'recordingToPaddedCorrelation':correlation,'quietWindows':quiet,'lineEndAccentEvents':0,'ultimatumOnlyTyping':True,'ultimatumTypingEvents':len(ultimatum),'closingExplosiveSfxEvents':0,'timelineIdleSecondsRemoved':5,'manuscriptSha256':image_hash}
report['comparisonTextReadyBeforeNarration']=readiness
report['narrationUnchangedFromV3']=True
(output/'qa/recording-alignment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report))
