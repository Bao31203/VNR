"""Original synthesized score and foley, aligned to the generated narration timeline."""
from pathlib import Path
import json
import wave
import numpy as np

root = Path(__file__).resolve().parents[1]
output = root / 'out' / 'history-1946'
timeline = json.loads((output / 'timeline.json').read_text(encoding='utf-8'))
sr = 48000
mix = np.zeros(round(timeline['duration'] * sr), dtype=np.float32)
rng = np.random.default_rng(19461219)
scenes = {scene['id']: scene for scene in timeline['scenes']}

def add(start, samples, gain=1.0):
    a = round(start * sr)
    b = min(len(mix), a + len(samples))
    if b > a:
        mix[a:b] += np.asarray(samples[:b-a] * gain, dtype=np.float32)

def drone(start, end, freqs, gain, fade=1.2):
    count = round((end-start) * sr)
    x = np.arange(count, dtype=np.float64) / sr
    env = np.minimum(1, x / fade) * np.minimum(1, np.maximum(0, end-start-x) / fade)
    # Soft harmonic bed, slow movement; no sampled or copyrighted music.
    signal = np.zeros(count)
    for i, f in enumerate(freqs):
        signal += np.sin(2*np.pi*f*x + i*.6) / len(freqs)
        signal += .16*np.sin(2*np.pi*(f*2.003)*x + i) / len(freqs)
    signal *= env * (.8 + .2*np.sin(2*np.pi*.13*x)) * gain
    add(start, signal)

def tick():
    x = np.arange(int(sr*.038)) / sr
    return (np.sin(2*np.pi*2200*x)*np.exp(-x*190) + rng.standard_normal(len(x))*.16*np.exp(-x*350))*.07

def boom(length=2.8):
    x = np.arange(round(sr*length)) / sr
    noise = np.convolve(rng.standard_normal(len(x)), np.ones(72)/72, mode='same')*3
    bass = np.sin(2*np.pi*(45*x-3*x*x))*.8
    return (noise*np.exp(-x*4.8)+bass*np.exp(-x*2.6))*np.minimum(1,x*700)

def heartbeat():
    x = np.arange(round(sr*.31)) / sr
    return np.sin(2*np.pi*55*x)*np.exp(-x*18)*np.minimum(1,x*250)*.085

for second in np.arange(.5, scenes['c01']['end']-.2, 1):
    add(second, tick(), .8)
drone(scenes['c02']['start'], scenes['c06']['end']-1.05, [55,82.41,110], .033, 2.0)
for offset in [0, 1.8, 3.7]:
    add(scenes['c03']['start']+offset, boom(1.7), .065)
countdown = scenes['c06']['end']-5
for second in np.arange(countdown, scenes['c06']['end']-.1, .5):
    add(second, tick(), 1.0 if second % 1 < .1 else .65)
# Silence before the artillery is deliberate; narration starts after the impact.
add(scenes['c07']['start']+.03, tick(), .4)
add(scenes['c07']['start']+1.0, boom(3), .28)
add(scenes['c07']['start']+1.65, boom(2), .09)
drone(scenes['c07']['start']+2, scenes['c08']['end'], [73.42,110,146.83,174.61], .036, 2.0)
for second in np.arange(scenes['c09']['start'], scenes['c10']['end']-2.0, .95):
    add(second, heartbeat())
    add(second+.22, heartbeat(), .6)
drone(scenes['c09']['start'], scenes['c10']['end']-1.8, [49,73.42,98], .020)
add(scenes['c11']['start']+.12, boom(2.4), .11)
drone(scenes['c11']['start'], timeline['duration'], [55,82.41,110,138.59], .040, 1.4)

mix = np.tanh(mix)
pcm = (np.stack([mix,mix],axis=1)*32767).astype(np.int16)
with wave.open(str(output/'soundtrack.wav'),'wb') as writer:
    writer.setnchannels(2)
    writer.setsampwidth(2)
    writer.setframerate(sr)
    writer.writeframes(pcm.tobytes())
print(f'Created original soundtrack: {timeline["duration"]:.2f}s')
