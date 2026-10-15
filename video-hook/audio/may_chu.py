# Bộ tiếng máy chữ cho video hook (tổng hợp bằng numpy, không cần file mẫu bên ngoài).
#
# Tạo bộ tiếng mẫu (6 tiếng phím, 2 tiếng phím cách, tiếng gạt dòng, tiếng chuông, file nghe thử):
#   python3 may_chu.py tao
#
# Tạo đoạn tiếng gõ khớp một dòng chữ (mỗi ký tự một tiếng gõ):
#   python3 may_chu.py go "Hạn chót: sáng 20.12.1946" --cps 24 --bell -o han-chot.wav
#   python3 may_chu.py go "Hà Nội · Tháng 12 năm 1946" --cps 14 --return --jitter 0 -o c1.wav
# Kèm theo là file .json ghi thời điểm từng ký tự hiện ra, để căn với hình.
# Dùng --jitter 0 nếu công cụ dựng gõ chữ đều nhau (ví dụ hiệu ứng "Đánh máy" của CapCut).
import argparse, json, os, unicodedata, wave
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.join(HERE, 'sfx', 'may-chu')


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def band_noise(n, fc, bw, rng):
    """Nhiễu trắng lọc dải quanh fc (Hz), bề rộng bw (Hz), lọc trong miền tần số."""
    x = rng.standard_normal(n)
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    spec *= np.exp(-0.5 * ((f - fc) / bw) ** 2)
    y = np.fft.irfft(spec, n)
    return y / (np.max(np.abs(y)) + 1e-9)


def damped(f, decay, dur, amp, phase=0.0):
    t = _t(dur)
    return amp * np.exp(-t / decay) * np.sin(2 * np.pi * f * t + phase)


def click(fc, bw, tau, amp, rng, dur=0.02):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return amp * band_noise(n, fc, bw, rng) * np.exp(-t / tau)


def put(buf, sig, at):
    a = int(at * SR)
    b = min(len(buf), a + len(sig))
    if a < len(buf):
        buf[a:b] += sig[:b - a]


def norm(x, peak):
    return x * (peak / (np.max(np.abs(x)) + 1e-9))


def key(seed):
    """Tiếng gõ một phím máy chữ cơ: cần chữ đập vào trục, thân máy rung, tiếng lách cách phụ, nhả phím."""
    r = np.random.default_rng(seed)
    buf = np.zeros(int(0.16 * SR))
    # cú đập của cần chữ vào trục giấy
    put(buf, click(r.uniform(2800, 4200), 1500, 0.0016, 1.0, r), 0)
    put(buf, click(r.uniform(1400, 2000), 700, 0.0025, 0.45, r), 0.0005)
    t = _t(0.004)
    put(buf, 0.6 * r.standard_normal(len(t)) * np.exp(-t / 0.0006), 0)
    # cộng hưởng thân máy và mặt bàn
    for f, d, a in ((r.uniform(170, 240), 0.014, 0.32), (r.uniform(850, 1250), 0.010, 0.35),
                    (r.uniform(2700, 3500), 0.006, 0.30), (r.uniform(5000, 6500), 0.003, 0.18)):
        put(buf, damped(f, d, 0.12, a, r.uniform(0, 2 * np.pi)), 0)
    # tiếng lách cách phụ của cần chữ bật lại
    put(buf, click(r.uniform(2000, 3000), 900, 0.0015, 0.35, r), r.uniform(0.007, 0.013))
    put(buf, damped(r.uniform(4200, 6800), 0.018, 0.06, 0.08), r.uniform(0.020, 0.035))
    # nhả phím
    d3 = r.uniform(0.060, 0.085)
    put(buf, click(r.uniform(1500, 2500), 800, 0.0015, 0.15, r), d3)
    put(buf, damped(300, 0.006, 0.03, 0.08), d3)
    return norm(buf, 0.7)


def space(seed):
    """Tiếng phím cách: thanh dài, trầm và nhẹ hơn phím chữ."""
    r = np.random.default_rng(seed)
    buf = np.zeros(int(0.16 * SR))
    put(buf, damped(r.uniform(120, 160), 0.035, 0.12, 0.8), 0)
    put(buf, damped(r.uniform(600, 800), 0.010, 0.06, 0.25), 0)
    put(buf, click(r.uniform(1800, 2600), 900, 0.0015, 0.4, r), 0)
    put(buf, click(r.uniform(1800, 2600), 900, 0.0015, 0.25, r), 0.004)
    put(buf, click(1600, 700, 0.0015, 0.12, r), r.uniform(0.065, 0.08))
    return norm(buf, 0.55)


def carriage_return(seed=7):
    """Tiếng gạt cần xuống dòng: 'cạch' + bánh cóc 'rắc rắc' + trục trượt 'xoẹt' + va chạm cuối hành trình."""
    r = np.random.default_rng(seed)
    buf = np.zeros(int(0.95 * SR))
    put(buf, norm(key(seed + 100), 0.6), 0)                      # tay nắm cần gạt
    for i in range(5):                                            # bánh cóc lên dòng
        put(buf, click(3500, 1200, 0.0012, 0.55 * (1 - i * 0.12), r), 0.03 + i * 0.018)
    # trục giấy trượt về: nhiễu dải cao + dải trầm, có độ "sạn" do ma sát
    n = int(0.48 * SR)
    t = np.arange(n) / SR
    env = np.minimum(1, t / 0.05) * np.minimum(1, (0.48 - t) / 0.12)
    grit = 0.7 + 0.3 * band_noise(n, 30, 25, r)
    slide = (band_noise(n, 2400, 1100, r) + 0.6 * band_noise(n, 420, 250, r)) * env * grit
    put(buf, 0.35 * slide / np.max(np.abs(slide)), 0.14)
    # va chạm cuối hành trình
    put(buf, damped(130, 0.05, 0.25, 0.9), 0.64)
    put(buf, damped(650, 0.015, 0.08, 0.4), 0.64)
    put(buf, click(3000, 1300, 0.0015, 0.8, r), 0.64)
    put(buf, click(2500, 1000, 0.0015, 0.25, r), 0.685)
    return norm(buf, 0.75)


def bell(seed=11):
    """Tiếng chuông 'ting' của máy chữ: chuông kim loại nhỏ, các họa âm không điều hòa, ngân khoảng 1 giây."""
    r = np.random.default_rng(seed)
    buf = np.zeros(int(1.4 * SR))
    put(buf, click(5000, 1500, 0.0008, 0.3, r), 0)
    f0 = 2480
    for ratio, amp, dec in ((1.0, 1.0, 0.7), (2.32, 0.45, 0.4), (4.25, 0.25, 0.25), (6.63, 0.12, 0.15)):
        for det, share in ((0.0, 0.85), (1.2, 0.15)):   # thành phần lệch nhỏ cho tiếng ngân hơi rung, không bị nhịp 'ù ù'
            put(buf, damped(f0 * ratio + det, dec, 1.39, amp * share, r.uniform(0, 2 * np.pi)), 0.001)
    fade = int(0.3 * SR)
    buf[-fade:] *= np.linspace(1, 0, fade) ** 2          # nhỏ dần ở cuối, tránh tiếng 'bụp'
    return norm(buf, 0.6)


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def pitch(x, factor):
    """Đổi cao độ nhẹ bằng cách co giãn mẫu (factor > 1 là cao hơn)."""
    idx = np.arange(0, len(x) - 1, factor)
    return np.interp(idx, np.arange(len(x)), x)


KEYS = [key(s) for s in range(1, 7)]
SPACES = [space(s) for s in (21, 22)]
RETURN = carriage_return()
BELL = bell()


def go(text, cps, start=0.0, jitter=0.2, seed=1946, ret=False, ring=False, gain_db=0.0):
    """Trả về (âm thanh, danh sách thời điểm ký tự) cho một dòng chữ được đánh máy."""
    rng = np.random.default_rng(seed)
    chars = list(unicodedata.normalize('NFC', text))
    base = 1.0 / cps
    if len(chars) > 1:
        iv = base * (1 + rng.uniform(-jitter, jitter, len(chars) - 1))
        iv *= (len(chars) - 1) * base / iv.sum()      # giữ đúng tổng thời gian theo cps
        times = start + np.concatenate([[0], np.cumsum(iv)])
    else:
        times = np.array([start])
    last = times[-1] if len(times) else start
    tail = (0.12 + len(RETURN) / SR) if ret else 0.0
    tail = max(tail, (0.08 + len(BELL) / SR) if ring else 0.0, 0.2)
    buf = np.zeros(int((last + tail) * SR) + 1)
    prev = -1
    for ch, tc in zip(chars, times):
        if ch == '\n':
            put(buf, RETURN, tc)
            continue
        if ch.isspace():
            s = SPACES[rng.integers(len(SPACES))]
        else:
            k = rng.integers(len(KEYS))
            if k == prev:
                k = (k + 1) % len(KEYS)
            prev = k
            s = KEYS[k]
        s = pitch(s, rng.uniform(0.95, 1.05)) * 10 ** (rng.uniform(-1.5, 1.5) / 20)
        put(buf, s, tc)
    if ring:
        put(buf, BELL, last + 0.08)
    if ret:
        put(buf, RETURN, last + (0.5 if ring else 0.12))
    buf *= 10 ** (gain_db / 20)
    return buf, [{'kyTu': c, 'giay': round(float(t), 4)} for c, t in zip(chars, times)]


def tao():
    os.makedirs(SFX_DIR, exist_ok=True)
    for i, k in enumerate(KEYS, 1):
        write_wav(os.path.join(SFX_DIR, f'phim-{i:02d}.wav'), k)
    for i, s in enumerate(SPACES, 1):
        write_wav(os.path.join(SFX_DIR, f'phim-cach-{i:02d}.wav'), s)
    write_wav(os.path.join(SFX_DIR, 'gat-dong.wav'), RETURN)
    write_wav(os.path.join(SFX_DIR, 'chuong.wav'), BELL)
    # File nghe thử: ba dòng chữ trong video, đúng tốc độ thiết kế
    demo = np.zeros(int(13 * SR))
    for text, cps, at, r_, b_ in (('Hà Nội · Tháng 12 năm 1946', 14, 0.3, True, False),
                                  ('— Giải tán lực lượng tự vệ', 30, 4.2, True, False),
                                  ('Hạn chót: sáng 20.12.1946', 24, 6.6, False, True),
                                  ('1946 – 1950', 12, 10.4, False, True)):
        x, _ = go(text, cps, 0, ret=r_, ring=b_)
        put(demo, x, at)
    write_wav(os.path.join(SFX_DIR, 'nghe-thu.wav'), norm(demo, 0.8))
    print('Đã tạo bộ tiếng trong', SFX_DIR)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Bộ tiếng máy chữ')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('tao', help='Tạo bộ tiếng mẫu vào sfx/may-chu/')
    g = sub.add_parser('go', help='Tạo đoạn tiếng gõ khớp một dòng chữ')
    g.add_argument('text')
    g.add_argument('--cps', type=float, default=26, help='Số ký tự mỗi giây (mặc định 26)')
    g.add_argument('--start', type=float, default=0.0, help='Giây bắt đầu gõ ký tự đầu tiên')
    g.add_argument('--jitter', type=float, default=0.2, help='Độ lệch nhịp gõ ±, 0 = đều tuyệt đối')
    g.add_argument('--seed', type=int, default=1946)
    g.add_argument('--return', dest='ret', action='store_true', help='Thêm tiếng gạt dòng cuối dòng')
    g.add_argument('--bell', action='store_true', help='Thêm tiếng chuông khi gõ xong')
    g.add_argument('--gain-db', type=float, default=0.0)
    g.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    if a.cmd == 'tao':
        tao()
    else:
        x, times = go(a.text, a.cps, a.start, a.jitter, a.seed, a.ret, a.bell, a.gain_db)
        write_wav(a.out, x)
        with open(os.path.splitext(a.out)[0] + '.json', 'w') as f:
            json.dump({'text': a.text, 'cps': a.cps, 'thoiDiemKyTu': times}, f, ensure_ascii=False, indent=1)
        print(f'Đã tạo {a.out} ({len(x) / SR:.2f}s, {len(times)} ký tự)')
