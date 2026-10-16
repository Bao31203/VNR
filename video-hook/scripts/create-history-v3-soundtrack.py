"""Original mechanical typewriter foley and documentary score, driven by exact frame events."""
from pathlib import Path
import json
import wave
import numpy as np

root = Path(__file__).resolve().parents[1]
output = root/'out/history-1946-v3'
plan = json.loads((output/'timeline.json').read_text(encoding='utf-8'))
events = json.loads((output/'sfx-events.json').read_text(encoding='utf-8'))
assert not any(e['type'] in ('type-return','type-bell') for e in events)
assert all(e['type'] in ('type-key','type-space') for e in events if e['scene']=='C4')
assert all(e['type'] in ('type-key','type-space') for e in events if e['scene']=='C11')
sr = 48000
length = round(plan['duration']*sr)
mix = np.zeros(length, dtype=np.float32)
music = np.zeros(length, dtype=np.float32)
rng = np.random.default_rng(19461219)
scenes = {s['id']:s for s in plan['scenes']}

def add(t, data, gain=1.0, destination=None):
    target = mix if destination is None else destination
    a = round(t*sr)
    b = min(len(target), a+len(data))
    if a>=0 and b>a:
        target[a:b] += np.asarray(data[:b-a]*gain,dtype=np.float32)

def timebase(duration):
    return np.arange(round(duration*sr))/sr

def normalize(a):
    return a/max(.000001,float(np.max(np.abs(a))))

# Six dry, metallic 1940s-style key mechanisms: impact, resonant typebar,
# short platen thump and spring return. No computer-keyboard sample is used.
keys=[]
for i in range(6):
    x=timebase(.046)
    noise=rng.standard_normal(len(x))
    impact=noise*np.exp(-x*(480+30*i))
    typebar=np.sin(2*np.pi*(1700+160*i)*x)*np.exp(-x*155)
    platen=np.sin(2*np.pi*(190+13*i)*x)*np.exp(-x*100)
    spring=np.sin(2*np.pi*(3200-105*i)*x)*np.exp(-x*230)
    keys.append(normalize(impact*.9+typebar*.7+platen*.65+spring*.22))
x=timebase(.055)
space=normalize(rng.standard_normal(len(x))*np.exp(-x*220)*.6+np.sin(2*np.pi*170*x)*np.exp(-x*90))
x=timebase(.32)
carriage=normalize(rng.standard_normal(len(x))*np.exp(-x*10)*(.15+.75*np.sin(2*np.pi*47*x)**12)+np.sin(2*np.pi*(650*x-370*x*x))*np.exp(-x*9)*.5)
x=timebase(.75)
bell=normalize((np.sin(2*np.pi*2670*x)+.35*np.sin(2*np.pi*4217*x))*np.exp(-x*9))

def tick():
    x=timebase(.035)
    return normalize(np.sin(2*np.pi*2300*x)*np.exp(-x*180)+rng.standard_normal(len(x))*.35*np.exp(-x*300))

def boom(duration=3):
    x=timebase(duration)
    noise=np.convolve(rng.standard_normal(len(x)),np.ones(65)/65,mode='same')*3
    return normalize((noise*np.exp(-x*4.2)+np.sin(2*np.pi*(44*x-2*x*x))*np.exp(-x*2.1))*np.minimum(1,x*900))

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

for event in events:
    kind=event['type']; t=event['frame']/30
    scene=scenes[event['scene']]
    speaking=vo_active(scene,event['local'])
    if kind in ('type-key','type-space'):
        db=-30 if scene['id']=='C8' else (-28 if speaking else -18)
        sample=space if kind=='type-space' else keys[event['variant']]
        if kind=='type-space':db-=4
        pitch=event['pitch']
        pitched=np.interp(np.arange(0,len(sample),pitch),np.arange(len(sample)),sample)
        add(t,pitched,10**(db/20))
    elif kind=='type-return': add(t,carriage,.075 if speaking else .12)
    elif kind=='type-bell': add(t,bell,.13)
    elif kind=='node-pop':add(t,keys[0],.065)
    elif kind=='paper-flip':add(t,carriage[:round(sr*.13)],.1)
    elif kind=='paper-slide':add(t,carriage,.055)
    elif kind=='counter':
        for offset in np.arange(0,1.2,.065):add(t+offset,keys[2],.042)
        add(t+1.2,keys[0],.09)
    elif kind=='hit':add(t,hit(),.20*event.get('gain',1))
    elif kind=='drum':add(t,boom(2.5),.25)
    elif kind=='tick':add(t,tick(),.075*event.get('gain',1))
    elif kind=='naval':add(t,boom(2),.20)
    elif kind=='cannon':add(t,boom(3.2),.64)
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
mix+=music*duck
for t in np.arange(scenes['C9']['start'],scenes['C10']['start']+5.4,.86):
    add(t,hit(),.10);add(t+.21,hit(),.055)
# Quiet windows are explicit, including the full one-second blackout after
# the switch's initial 18ms and the half-second before the closing question.
for interval in plan['quietWindows']:
    mix[round(interval['start']*sr):round(interval['end']*sr)]=0
mix[round((plan['duration']-1)*sr):]=0
pcm=(np.stack([np.tanh(mix),np.tanh(mix)],axis=1)*32767).astype(np.int16)
with wave.open(str(output/'soundtrack.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
print(f'Created {len(events)} frame-synchronized foley events; {plan["duration"]:.3f}s')
