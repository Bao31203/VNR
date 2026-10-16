"""Repo's recorded SFX at exact frame onsets; full original firearm recordings."""
from pathlib import Path
import json
import wave
import subprocess
import hashlib
import numpy as np

root = Path(__file__).resolve().parents[1]
output = root/'out/history-1946-v6'
plan = json.loads((output/'timeline.json').read_text(encoding='utf-8'))
events = json.loads((output/'sfx-events.json').read_text(encoding='utf-8'))
assert not any(e['type'] in ('type-return','type-bell') for e in events)
assert all(e['type'] in ('type-key','type-space') for e in events if e['scene']=='C4')
assert all(e['type'] in ('type-key','type-space') for e in events if e['scene']=='C11')
sr = 48000
length = round(plan['duration']*sr)
mix = np.zeros((length,2), dtype=np.float32)
typing = np.zeros(length, dtype=np.float32)
typing_boost_db = 13.0
music = np.zeros(length, dtype=np.float32)
rng = np.random.default_rng(19461219)
key_rng = np.random.default_rng(1946)
scenes = {s['id']:s for s in plan['scenes']}
audit={'sourceCommit':plan['sourceCommit'],'assets':{},'recordedPlacements':[],'typingPlacements':[],'noReturnOrBell':True,'noClosingExplosion':True,'firearmProcessing':'full decoded source, format resampling only, volume only'}

def add(t, data, gain=1.0, destination=None):
    target = mix if destination is None else destination
    a = round(t*sr)
    b = min(len(target), a+len(data))
    if a>=0 and b>a:
        signal=np.asarray(data[:b-a]*gain,dtype=np.float32)
        if target.ndim==2 and signal.ndim==1:signal=signal[:,None]
        target[a:b] += signal

def timebase(duration):
    return np.arange(round(duration*sr))/sr

def normalize(a):
    return a/max(.000001,float(np.max(np.abs(a))))

def load_source(relative,channels):
    path=root/relative
    # Decode the complete asset, preserving stereo. 44.1 -> 48 kHz is only the
    # format conversion needed by this project's audio bus, not a sound effect.
    raw=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-ar',str(sr),'-f','f32le','pipe:1'],check=True,capture_output=True).stdout
    signal=np.frombuffer(raw,dtype=np.float32).copy()
    if channels>1:signal=signal.reshape(-1,channels)
    audit['assets'][relative]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'decodedSha256':hashlib.sha256(raw).hexdigest(),'samples':len(signal),'duration':len(signal)/sr,'channels':channels}
    return signal

key_paths=[f'audio/sfx/may-chu/phim-{i:02d}.wav' for i in range(1,13)]
space_paths=[f'audio/sfx/may-chu/phim-cach-{i:02d}.wav' for i in range(1,3)]
keys=[load_source(path,1) for path in key_paths]
spaces=[load_source(path,1) for path in space_paths]
cannon_path='audio/sfx/phao/universfield-powerful-cannon-shot-02-487887.mp3'
burst_path='audio/sfx/sung/dragon-studio-gunshots-firing-repeatedly-511326.mp3'
machine_path='audio/sfx/sung/freesound_community-clean-machine-gun-burst-98224.mp3'
cannon=load_source(cannon_path,2)
burst=load_source(burst_path,2)
machine=load_source(machine_path,1)

def recorded(event,path,signal,onset,gain):
    target=event['frame']/30
    start=target-onset
    assert round(start*sr)>=0 and round(start*sr)+len(signal)<=length
    add(start,signal,gain)
    audit['recordedPlacements'].append({'scene':event['scene'],'type':event['type'],'source':path,'start':start,'targetOnset':target,'sourceOnsetSeconds':onset,'gain':gain,'samplesPlaced':len(signal),'fullOriginal':True})

def tick():
    x=timebase(.035)
    return normalize(np.sin(2*np.pi*2300*x)*np.exp(-x*180)+rng.standard_normal(len(x))*.35*np.exp(-x*300))

def hit():
    x=timebase(.4)
    return normalize(np.sin(2*np.pi*(58*x-15*x*x))*np.exp(-x*13)*np.minimum(1,x*300))

def drone(start,end,freqs,gain):
    x=timebase(end-start)
    env=np.minimum(1,x/1.7)*np.minimum(1,np.maximum(0,end-start-x)/1.4)
    signal=sum(np.sin(2*np.pi*f*x+i*.8) for i,f in enumerate(freqs))/len(freqs)
    signal*=env*(.85+.15*np.sin(2*np.pi*.13*x))*gain
    add(start,signal,destination=music)

def vo_active(scene,local):
    return any(a<=local<=b for a,b in scene['voiceWindows'])

previous_key=-1
for event in events:
    kind=event['type']; t=event['frame']/30
    scene=scenes[event['scene']]
    speaking=vo_active(scene,event['local'])
    if kind in ('type-key','type-space'):
        db=-30 if scene['id']=='C8' else (-28 if speaking else -18)
        if kind=='type-space':
            index=int(key_rng.integers(len(spaces)));sample=spaces[index];source=space_paths[index]
        else:
            index=int(key_rng.integers(len(keys)))
            if index==previous_key:index=(index+1)%len(keys)
            previous_key=index;sample=keys[index];source=key_paths[index]
        if kind=='type-space':db-=4
        pitch=float(key_rng.uniform(.97,1.03))
        db+=float(key_rng.uniform(-2,2))+typing_boost_db
        pitched=np.interp(np.arange(0,len(sample),pitch),np.arange(len(sample)),sample)
        start=t-.010/pitch
        add(start,pitched,10**(db/20))
        add(start,pitched,10**(db/20),destination=typing)
        audit['typingPlacements'].append({'scene':event['scene'],'element':event.get('element'),'frame':event['frame'],'source':source,'start':start,'onset':t,'pitch':pitch,'gainDb':db})
    elif kind in ('type-return','type-bell','paper-flip','paper-slide','drum'):raise AssertionError(f'Forbidden SFX: {kind}')
    elif kind=='node-pop':add(t,keys[0],.065)
    elif kind=='counter':
        for offset in np.arange(0,1.2,.065):add(t+offset,keys[2],.042)
        add(t+1.2,keys[0],.09)
    elif kind=='hit':add(t,hit(),.20*event.get('gain',1))
    elif kind=='tick':add(t,tick(),.075*event.get('gain',1))
    elif kind in ('naval','cannon'):recorded(event,cannon_path,cannon,.085,1.0)
    elif kind=='gunfire':recorded(event,burst_path,burst,.023,event.get('gainOverride',10**(-6/20) if speaking else 1.0))
    elif kind=='machine-gun':recorded(event,machine_path,machine,.025,event.get('gainOverride',10**(-6/20) if speaking else 1.0))
    elif kind=='switch':add(t,keys[0][:round(.018*sr)],.22)
    elif kind=='buzz':
        x=timebase(.8);add(t,np.sin(2*np.pi*100*x)*rng.standard_normal(len(x))*.035)

drone(scenes['C2']['start'],scenes['C6']['end']-1,[55,82.41,110],.065)
drone(scenes['C7']['start']+2,scenes['C8']['end'],[73.42,110,146.83,174.61],.045)
drone(scenes['C9']['start'],scenes['C10']['start']+5.4,[49,73.42,98],.032)
drone(scenes['C11']['start'],plan['duration']-1,[55,82.41,110,138.59],.06)

# Music ducking envelope: 0.2s attack, 0.6s release; quote gets extra headroom.
duck=np.ones(length,dtype=np.float32)
for scene in plan['scenes']:
    for left,right in scene['voiceWindows']:
        a=round((scene['start']+left)*sr);b=min(length,round((scene['start']+right)*sr))
        attack=round(.2*sr);release=round(.6*sr);level=.16 if scene['id']=='C8' else .25
        start=max(0,a-attack);end=min(length,b+release)
        envelope=np.ones(end-start,dtype=np.float32)
        envelope[:a-start]=np.linspace(1,level,a-start,endpoint=False)
        envelope[a-start:b-start]=level
        envelope[b-start:]=np.linspace(level,1,end-b,endpoint=False)
        duck[start:end]=np.minimum(duck[start:end],envelope)
mix+=(music*duck)[:,None]
for t in np.arange(scenes['C9']['start'],scenes['C10']['start']+5.4,.86):
    add(t,hit(),.10);add(t+.21,hit(),.055)
# Quiet windows are explicit, including the full one-second blackout after
# the switch's initial 18ms and the half-second before the closing question.
for interval in plan['quietWindows']:
    mix[round(interval['start']*sr):round(interval['end']*sr)]=0
    typing[round(interval['start']*sr):round(interval['end']*sr)]=0
mix[round((plan['duration']-1)*sr):]=0
typing[round((plan['duration']-1)*sr):]=0
def float_wav(path,signal):
    subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-c:a','pcm_f32le',str(path)],input=np.asarray(signal,dtype=np.float32).tobytes(),check=True)
float_wav(output/'soundtrack.wav',mix)
float_wav(output/'typing-stem.wav',np.repeat(typing[:,None],2,axis=1))
with wave.open(str(output/'voice.wav'),'rb') as w:
    assert w.getframerate()==sr and w.getnchannels()==1 and w.getsampwidth()==2
    voice=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
assert len(voice)==length
mixed=mix+voice[:,None]
for interval in [*plan['quietWindows'],plan['blackouts'][-1]]:
    mixed[round(interval['start']*sr):round(interval['end']*sr)]=0
float_wav(output/'mix-unmastered.wav',mixed)
audit['typingCount']=len(audit['typingPlacements'])
audit['firearmCount']=len(audit['recordedPlacements'])
audit['unmasteredPeak']=float(np.max(np.abs(mixed)))
audit['noNonlinearProcessing']=True
audit['typingBoostDb']=typing_boost_db
(output/'qa/sfx-provenance.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'events':len(events),'typingCount':audit['typingCount'],'firearmCount':audit['firearmCount'],'sourceAssets':len(audit['assets']),'unmasteredPeak':audit['unmasteredPeak']}))
