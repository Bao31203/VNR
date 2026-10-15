# Tiếng pháo cho video hook, làm từ bản thu thật:
#   sfx/phao/goc/universfield-powerful-cannon-shot-02-487887.mp3  (1,07 giây, stereo)
#
#   python3 phao.py
# tạo ra trong sfx/phao/:
#   phao-gan.wav        tiếng nổ gần, nguyên gốc (đã căn đầu tiếng nổ về 10 ms, chuẩn hóa)
#   phao-gan-vang.wav   tiếng nổ gần + vang dội giữa phố (~3,5 s)   → C7, pháo đài Láng khai hỏa
#   phao-xa-01..03.wav  pháo vọng từ xa, 3 biến thể trầm bổng          → C3, pháo hạm nã vào Hải Phòng
#   nghe-thu-phao.wav   nghe thử: 3 tiếng pháo xa rồi 1 tiếng pháo gần
import os, subprocess, wave
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sfx', 'phao')
GOC = os.path.join(OUT, 'goc', 'universfield-powerful-cannon-shot-02-487887.mp3')


def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).reshape(-1, 2).astype(float) / 32767


def write(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def norm(x, peak_db):
    return x * (10 ** (peak_db / 20) / (np.max(np.abs(x)) + 1e-9))


def filt(x, gain_fn):
    n = len(x)
    f = np.maximum(np.fft.rfftfreq(n, 1 / SR), 1e-3)
    return np.fft.irfft(np.fft.rfft(x, axis=0) * gain_fn(f)[:, None], n, axis=0)


lp = lambda fc, o=2: (lambda f: 1 / np.sqrt(1 + (f / fc) ** (2 * o)))
hp = lambda fc, o=2: (lambda f: 1 / np.sqrt(1 + (fc / f) ** (2 * o)))


def conv(x, ir):
    n = len(x) + len(ir)
    return np.fft.irfft(np.fft.rfft(x, n, axis=0) * np.fft.rfft(ir, n, axis=0), n, axis=0)


def pad(x, sec):
    return np.vstack([x, np.zeros((int(sec * SR), 2))])


def fade_out(x, sec):
    n = min(len(x), int(sec * SR))
    x = x.copy()
    x[-n:] *= (np.linspace(1, 0, n) ** 2)[:, None]
    return x


def street_ir(seed, rt60, echoes, bright):
    """Vang ngoài trời giữa các dãy nhà: vài tiếng dội rõ từ tường nhà + đuôi vang tối màu. Stereo (hai kênh khác nhau)."""
    r = np.random.default_rng(seed)
    n = int((rt60 + 0.3) * SR)
    t = np.arange(n) / SR
    ir = np.zeros((n, 2))
    ir[0] = 1.0
    for ms, g in echoes:
        for c in range(2):
            ir[int((ms + r.uniform(-6, 6)) * SR / 1000), c] += g * r.uniform(0.8, 1.0)
    tail = r.standard_normal((n, 2)) * np.exp(-t / (rt60 / 6.91))[:, None] * np.clip((t - 0.05) / 0.08, 0, 1)[:, None]
    tail = filt(tail, lambda f: lp(bright, 2)(f) * hp(60, 1)(f))
    return ir + 0.5 * tail / np.max(np.abs(tail))


def resample(x, factor):
    """Đổi cao độ và tốc độ cùng lúc (factor < 1: trầm và dài hơn)."""
    idx = np.arange(0, len(x) - 1, factor)
    return np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in range(2)], axis=1)


def main():
    x = load(GOC)
    # căn: điểm bắt đầu tiếng nổ (vượt 5% đỉnh) nằm ở 10 ms
    on = np.argmax(np.abs(x).max(1) > 0.05 * np.abs(x).max())
    x = x[max(0, on - int(0.010 * SR)):]
    x = fade_out(x, 0.25)

    gan = norm(x, -1.0)
    write(os.path.join(OUT, 'phao-gan.wav'), gan)

    # pháo gần + vang dội giữa phố
    ir = street_ir(1, 2.6, [(85, 0.45), (140, 0.38), (230, 0.30), (370, 0.22), (560, 0.15), (820, 0.10)], 1800)
    wet = conv(pad(x, 3.0), ir)[:len(x) + int(3.0 * SR)]
    vang = pad(x, 3.0) + 0.55 * wet / np.max(np.abs(wet))
    write(os.path.join(OUT, 'phao-gan-vang.wav'), fade_out(norm(vang, -1.0), 0.6))

    # pháo vọng từ xa: cắt dải cao, làm mềm tiếng nổ, vang xa nhiều hơn tiếng gốc
    xa_list = []
    for i, factor in enumerate((0.92, 0.85, 0.98), 1):
        y = resample(x, factor)
        y = filt(y, lambda f: lp(1300, 2)(f) * hp(35, 2)(f))   # vẫn giữ dải trung để loa nhỏ ở lớp học phát được
        k = int(0.030 * SR)                               # làm mềm tiếng nổ: âm lượng tăng dần trong 30 ms đầu
        y[:k] *= np.linspace(0.15, 1, k)[:, None]
        ir = street_ir(10 + i, 3.0, [(180, 0.5), (320, 0.4), (520, 0.3), (800, 0.2), (1150, 0.12)], 1500)
        wet = conv(pad(y, 3.2), ir)[:len(y) + int(3.2 * SR)]
        z = 0.6 * pad(y, 3.2) + 0.9 * wet / np.max(np.abs(wet))
        z = fade_out(norm(z, -6.0), 0.8)
        xa_list.append(z)
        write(os.path.join(OUT, f'phao-xa-{i:02d}.wav'), z)

    # nghe thử: 3 tiếng pháo xa (như C3) rồi 1 giây im lặng, tiếng pháo gần có vang (như C7)
    demo = np.zeros((int(13.5 * SR), 2))
    for at, z in zip((0.2, 2.7, 5.2), xa_list):
        a = int(at * SR)
        demo[a:a + len(z)] += z[:len(demo) - a]
    v = norm(vang, -1.0)
    a = int(9.0 * SR)
    demo[a:a + len(v)] += v[:len(demo) - a]
    write(os.path.join(OUT, 'nghe-thu-phao.wav'), fade_out(norm(demo, -1.0), 0.5))
    print('Đã tạo tiếng pháo trong', OUT)


if __name__ == '__main__':
    main()
