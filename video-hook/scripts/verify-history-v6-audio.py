"""Check recording playback rate/alignment and sample-level quiet windows."""
from pathlib import Path
import json
import wave
import hashlib
import subprocess
import numpy as np

output=Path(__file__).resolve().parents[1]/'out/history-1946-v6'
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
for i,(new,old) in enumerate(zip(plan['scenes'],v3['scenes'])):
    assert abs(new['start']-old['start']-(5 if i>=7 else 0))<1e-6
    assert abs(new['end']-old['end']-(5 if i>=6 else 0))<1e-6
assert abs(previous['duration']-plan['duration'])<1e-6
assert previous['scenes'][1]['duration']-plan['scenes'][1]['duration']==5
assert plan['scenes'][1]['voiceDuration']==previous['scenes'][1]['voiceDuration']
assert plan['scenes'][1]['voStart']+plan['scenes'][1]['voiceDuration']<plan['scenes'][1]['duration']
for i,(new,old) in enumerate(zip(plan['scenes'],previous['scenes'])):
    assert abs(old['start']-new['start']-(5 if 2<=i<=6 else 0))<1e-6
image_source=Path('C:/Users/pgb31/Downloads/OIP (2).webp')
image_asset=output.parents[1]/'templates/history-v4/assets/a10.webp'
image_hash=hashlib.sha256(image_source.read_bytes()).hexdigest()
assert hashlib.sha256(image_asset.read_bytes()).hexdigest()==image_hash
def read(path):
    with wave.open(str(path),'rb') as w:
        sr=w.getframerate();channels=w.getnchannels()
        signal=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
    return sr,signal.reshape(-1,channels).mean(axis=1)
sr,original=read(output.parent/'history-1946-v4/voice/c08-recording.wav')
_,padded=read(output.parent/'history-1946-v4/voice/c08-padded.wav')
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
_,v5_voice=read(output.parent/'history-1946-v5/voice.wav')
_,new_voice=read(output/'voice.wav')
cut=round(72*sr);hold=round(5*sr)
assert np.array_equal(v5_voice[:cut],new_voice[:cut])
assert np.array_equal(v5_voice[cut:],new_voice[cut+hold:])
assert np.all(new_voice[cut:cut+hold]==0)
report['narrationSamplesUnchangedWithFiveSecondHold']=True
provenance=json.loads((output/'qa/sfx-provenance.json').read_text(encoding='utf-8'))
firearms=provenance['recordedPlacements']
assert len(firearms)==7
assert [e['scene'] for e in firearms].count('C3')==3
assert [e['scene'] for e in firearms].count('C7')==4
assert all(e['fullOriginal'] and e['samplesPlaced']==provenance['assets'][e['source']]['samples'] for e in firearms)
assert all(e['gain']==1.0 for e in firearms if e['type'] in ('naval','cannon'))
assert all(abs(e['start']+e['sourceOnsetSeconds']-e['targetOnset'])<1e-7 for e in firearms)
for relative,asset in provenance['assets'].items():
    assert hashlib.sha256((output.parents[1]/relative).read_bytes()).hexdigest()==asset['sha256']
assert len({e['source'] for e in provenance['typingPlacements'] if '/phim-0' in e['source'] or '/phim-1' in e['source']})==12
assert all(abs(e['start']+.010/e['pitch']-e['onset'])<1e-7 for e in provenance['typingPlacements'])
assert not any('chuong' in p or 'gat-dong' in p or 'nghe-thu' in p for p in provenance['assets'])
assert provenance['noNonlinearProcessing']
mastering=json.loads((output/'qa/mastering.json').read_text(encoding='utf-8'))
assert mastering['noDynamicCompression']
report['recordedSfx']={'sourceAssets':len(provenance['assets']),'typingCount':provenance['typingCount'],'fullOriginalFirearmPlacements':len(firearms),'allSourceChecksumsMatch':True,'staticMasterGainDb':mastering['gainDb']}
v5=output.parent/'history-1946-v5'
old_provenance=json.loads((v5/'qa/sfx-provenance.json').read_text(encoding='utf-8'))
old_mastering=json.loads((v5/'qa/mastering.json').read_text(encoding='utf-8'))
for new,old in zip(firearms,old_provenance['recordedPlacements']):
    if new['type'] in ('naval','cannon'):assert new==old
    else:
        assert abs(new['start']-old['start']-5)<1e-7
        assert abs(new['targetOnset']-old['targetOnset']-5)<1e-7
        assert abs(20*np.log10(new['gain']/old['gain'])+3)<1e-7
        assert new['source']==old['source'] and new['samplesPlaced']==old['samplesPlaced']
assert provenance['assets']==old_provenance['assets']
assert mastering['gainDb']==old_mastering['gainDb']
assert provenance['typingBoostDb']==13.0
assert len(provenance['typingPlacements'])==len(old_provenance['typingPlacements'])
for new,old in zip(provenance['typingPlacements'],old_provenance['typingPlacements']):
    assert all(new[k]==old[k] for k in ['source','scene','element','pitch'])
    offset=5 if new['scene'] in ('C8','C9','C10','C11') else 0
    assert new['frame']-old['frame']==offset*30
    assert abs(new['start']-old['start']-offset)<1e-7
    assert abs(new['onset']-old['onset']-offset)<1e-7
    assert abs(new['gainDb']-old['gainDb']-13.0)<1e-9
gun_end=max(e['start']+e['samplesPlaced']/sr for e in firearms if e['type'] in ('gunfire','machine-gun'))
red_start=plan['scenes'][7]['start']-.4
assert gun_end<red_start
report['typingBoost']={'db':13,'sameV5MasterGainDb':mastering['gainDb']}
baseline_dir=output/'qa/typing-plus3'
if (baseline_dir/'before-sfx-provenance.json').exists():
    baseline=json.loads((baseline_dir/'before-sfx-provenance.json').read_text(encoding='utf-8'))
    assert baseline['recordedPlacements']==firearms
    for new,old in zip(provenance['typingPlacements'],baseline['typingPlacements']):
        assert all(new[k]==old[k] for k in ['source','scene','element','pitch','frame','start','onset'])
        assert abs(new['gainDb']-old['gainDb']-3)<1e-9
    def read_float(path):
        raw=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','f32le','pipe:1'],check=True,capture_output=True).stdout
        return np.frombuffer(raw,dtype=np.float32).reshape(-1,2)
    delta=read_float(output/'mix-unmastered.wav')-read_float(baseline_dir/'before-mix-unmastered.wav')
    expected=read_float(output/'typing-stem.wav')*(1-10**(-3/20))
    error=float(np.max(np.abs(delta-expected)))
    assert error<1e-6,error
    report['typingBoost'].update({'addedDbOverPriorV6':3,'onlyTypingChangedMaxError':error})
report['gunfireAdjustment']={'delaySeconds':5,'gainDb':-3,'cannonUnchanged':True,'lastGunfireEnds':gun_end,'transitionToC8Starts':red_start,'quoteSceneStarts':plan['scenes'][7]['start'],'gunfireFinishesBeforeTransition':True}
(output/'qa/recording-alignment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report))
