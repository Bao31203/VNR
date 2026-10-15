# Tạo âm thanh nền cho video (tích tắc, nền trầm, tiếng pháo, nhịp tim) -> out/audio.wav
# Mốc thời gian khớp với seek() trong index.html.
import os, wave
import numpy as np

SR = 44100
DUR = 78
t = np.arange(int(SR * DUR)) / SR
mix = np.zeros_like(t)
rng = np.random.default_rng(1946)


def at(sec):
    return int(sec * SR)


def add(start, sig, gain=1.0):
    a = at(start)
    b = min(len(mix), a + len(sig))
    mix[a:b] += sig[: b - a] * gain


def tick(level=1.0):
    n = int(.03 * SR)
    x = np.arange(n) / SR
    s = np.sin(2 * np.pi * 2400 * x) * np.exp(-x * 220) + rng.standard_normal(n) * np.exp(-x * 400) * .3
    return s * level


def boom(length=3.0):
    n = int(length * SR)
    x = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # lọc thông thấp đơn giản
    k = 60
    noise = np.convolve(noise, np.ones(k) / k, mode='same') * 4
    low = np.sin(2 * np.pi * 42 * x * (1 - x * .08)) * 1.2
    return (noise * np.exp(-x * 3.5) + low * np.exp(-x * 1.6)) * np.minimum(1, x * 400)


def thump():
    n = int(.35 * SR)
    x = np.arange(n) / SR
    return np.sin(2 * np.pi * 58 * x) * np.exp(-x * 14) * np.minimum(1, x * 300)


def drone(a, b, freqs, gain, fade=2.0):
    seg = (t >= a) & (t < b)
    x = t[seg] - a
    env = np.minimum(1, x / fade) * np.minimum(1, (b - a - x) / fade)
    s = sum(np.sin(2 * np.pi * f * t[seg] + i) for i, f in enumerate(freqs)) / len(freqs)
    s *= 1 + .25 * np.sin(2 * np.pi * .2 * t[seg])
    mix[seg] += s * env * gain


# Cảnh 1: tích tắc chậm
for s in np.arange(0.5, 5, 1.0):
    add(s, tick(.35))
# Cảnh 2–3: nền trầm căng dần
drone(4.5, 30.5, [55, 82.4, 110], .18, fade=3)
# Cảnh 4: tích tắc theo từng giây 19:59:50 → 20:00
drone(30, 40, [49, 73.4, 98, 146.8], .22, fade=1.5)
for i, s in enumerate(np.arange(30.0, 40.0, 1.0)):
    add(s, tick(.45 + i * .05))
for s in np.arange(30.5, 40.0, 1.0):
    add(s, tick(.25))
# Cảnh 5: im lặng rồi tiếng pháo
add(40.85, boom(3.5), .9)
add(41.6, boom(2.5), .35)
# Cảnh 6: nền trầm hùng tráng cho Lời kêu gọi
drone(44.2, 59.6, [55, 82.4, 110, 164.8], .2, fade=2.5)
# Cảnh 7: nhịp tim
for s in np.arange(59.8, 67.6, .85):
    add(s, thump(), .6)
    add(s + .22, thump(), .35)
add(67.8, boom(2.5), .5)
# Cảnh 8: tên đề tài
add(70.8, boom(3.0), .45)
drone(70.6, 78, [55, 82.4, 110, 138.6], .2, fade=1.2)

mix = np.tanh(mix * 1.2) * .85
pcm = (np.stack([mix, mix], axis=1) * 32767).astype(np.int16)
os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
with wave.open(os.path.join(os.path.dirname(__file__), 'out', 'audio.wav'), 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('ok')
