# Bộ tiếng máy chữ cho video hook, cắt từ bản thu máy chữ cơ thật:
#   sfx/may-chu/goc/sea-you-later-typewriter-301419.mp3  (91 giây, 432 tiếng gõ, 3 tiếng chuông, 3 lần gạt dòng)
#
# Cắt bộ tiếng mẫu từ bản thu (12 tiếng phím, 2 tiếng phím cách, 2 tiếng gạt dòng, 2 tiếng chuông, file nghe thử):
#   python3 may_chu.py tach
#
# Tạo đoạn tiếng gõ khớp một dòng chữ (mỗi ký tự một tiếng gõ thật):
#   python3 may_chu.py go "Hạn chót: sáng 20.12.1946" --cps 24 --bell -o han-chot.wav
#   python3 may_chu.py go "Hà Nội · Tháng 12 năm 1946" --cps 14 --return --jitter 0 -o c1.wav
# Kèm theo là file .json ghi thời điểm từng ký tự hiện ra, để căn với hình.
# Dùng --jitter 0 nếu công cụ dựng gõ chữ đều nhau (ví dụ hiệu ứng "Đánh máy" của CapCut).
import argparse, glob, json, os, subprocess, unicodedata, wave
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.join(HERE, 'sfx', 'may-chu')
GOC = os.path.join(SFX_DIR, 'goc', 'sea-you-later-typewriter-301419.mp3')

# Vị trí chuông và gạt dòng trong bản thu gốc (đo bằng phổ tần; chỉ đúng với file này)
BELLS = [(33.50, 1.75), (58.34, 1.75)]                 # (giây bắt đầu, độ dài)
RETURNS = [(36.00, 1.35), (87.65, 1.45)]
# Các vùng không lấy tiếng phím: đoạn đầu lặt vặt, quanh chuông và gạt dòng
EXCLUDE = [(0, 14.0), (33.3, 37.6), (57.9, 63.2), (84.9, 89.5)]


def load_mp3(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(float) / 32767


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def read_wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32767


def put(buf, sig, at):
    a = int(round(at * SR))
    b = min(len(buf), a + len(sig))
    if 0 <= a < len(buf):
        buf[a:b] += sig[:b - a]


def norm(x, peak):
    return x * (peak / (np.max(np.abs(x)) + 1e-9))


def fades(x, fin=0.002, fout=0.04):
    x = x.copy()
    a, b = int(fin * SR), min(len(x), int(fout * SR))
    x[:a] *= np.linspace(0, 1, a)
    x[-b:] *= np.linspace(1, 0, b) ** 2
    return x


def onsets(x):
    hop = int(0.002 * SR)
    env = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))[::hop]
    thr = max(np.percentile(env, 20) * 6, np.percentile(env, 90) * 0.35)
    out, last = [], -10**9
    for i in range(5, len(env)):
        if env[i] > thr and env[i] > 3 * env[i - 5] and (i - last) * 0.002 > 0.05:
            out.append(i * 0.002)
            last = i
    return np.array(out)


def centroid(seg):
    X = np.abs(np.fft.rfft(seg)) ** 2
    f = np.fft.rfftfreq(len(seg), 1 / SR)
    return (f * X).sum() / (X.sum() + 1e-12)


def tach():
    x = load_mp3(GOC)
    ons = onsets(x)
    # tiếng phím đứng riêng: cách tiếng trước >= 0.09s và tiếng sau >= 0.20s, ngoài các vùng loại trừ
    cands = []
    for i in range(1, len(ons) - 1):
        t = ons[i]
        if any(a <= t <= b for a, b in EXCLUDE):
            continue
        if t - ons[i - 1] < 0.09 or ons[i + 1] - t < 0.20:
            continue
        # căn để tiếng "cạch" chính (đỉnh lớn nhất) luôn nằm ở 10 ms đầu file, khớp lúc chữ hiện ra
        a0 = int((t - 0.003) * SR)
        pk = a0 + int(np.argmax(np.abs(x[a0:a0 + int(0.08 * SR)])))
        start = pk / SR - 0.010
        dur = min(0.22, ons[i + 1] - 0.01 - start)
        seg = x[int(start * SR):int((start + dur) * SR)]
        cands.append((t, seg, np.max(np.abs(seg)), centroid(seg[:int(0.05 * SR)])))
    peaks = np.array([c[2] for c in cands])
    lo, hi = np.percentile(peaks, 35), np.percentile(peaks, 92)
    good = sorted([c for c in cands if lo <= c[2] <= hi], key=lambda c: c[3])
    # phím cách: 2 tiếng trầm nhất; phím chữ: 12 tiếng trải đều theo độ sáng tiếng
    spaces, keys = good[:2], good[2:]
    keys = [keys[int(i)] for i in np.linspace(0, len(keys) - 1, 12)]
    for f in glob.glob(os.path.join(SFX_DIR, '*.wav')):
        os.remove(f)
    for i, (t, seg, _, _) in enumerate(keys, 1):
        write_wav(os.path.join(SFX_DIR, f'phim-{i:02d}.wav'), fades(norm(seg, 0.7)))
    for i, (t, seg, _, _) in enumerate(spaces, 1):
        write_wav(os.path.join(SFX_DIR, f'phim-cach-{i:02d}.wav'), fades(norm(seg, 0.55)))
    for i, (t, d) in enumerate(BELLS, 1):
        seg = x[int((t - 0.005) * SR):int((t + d) * SR)]
        write_wav(os.path.join(SFX_DIR, f'chuong-{i:02d}.wav'), fades(norm(seg, 0.7), fout=0.4))
    for i, (t, d) in enumerate(RETURNS, 1):
        seg = x[int(t * SR):int((t + d) * SR)]
        write_wav(os.path.join(SFX_DIR, f'gat-dong-{i:02d}.wav'), fades(norm(seg, 0.7), fin=0.02, fout=0.15))
    print(f'Đã cắt {len(keys)} tiếng phím, {len(spaces)} phím cách, {len(BELLS)} chuông, {len(RETURNS)} gạt dòng '
          f'(từ {len(ons)} tiếng gõ trong bản thu) vào {SFX_DIR}')
    nghe_thu()


def load_set():
    ld = lambda pat: [read_wav(p) for p in sorted(glob.glob(os.path.join(SFX_DIR, pat)))]
    return ld('phim-[0-9]*.wav'), ld('phim-cach-*.wav'), ld('gat-dong-*.wav'), ld('chuong-*.wav')


def pitch(x, factor):
    idx = np.arange(0, len(x) - 1, factor)
    return np.interp(idx, np.arange(len(x)), x)


def go(text, cps, start=0.0, jitter=0.2, seed=1946, ret=False, ring=False, gain_db=0.0):
    """Trả về (âm thanh, danh sách thời điểm ký tự) cho một dòng chữ được đánh máy."""
    keys, spaces, returns, bells = load_set()
    rng = np.random.default_rng(seed)
    chars = list(unicodedata.normalize('NFC', text))
    base = 1.0 / cps
    if len(chars) > 1:
        iv = base * (1 + rng.uniform(-jitter, jitter, len(chars) - 1))
        iv *= (len(chars) - 1) * base / iv.sum()      # giữ đúng tổng thời gian theo cps
        times = start + np.concatenate([[0], np.cumsum(iv)])
    else:
        times = np.array([start])
    last = times[-1]
    bell = bells[rng.integers(len(bells))] if ring else None
    rtn = returns[rng.integers(len(returns))] if ret else None
    t_bell = last + 0.06
    t_ret = (t_bell + 0.6) if ring else (last + 0.15)
    end = last + 0.3
    if ring:
        end = max(end, t_bell + len(bell) / SR)
    if ret:
        end = max(end, t_ret + len(rtn) / SR)
    buf = np.zeros(int(end * SR) + 1)
    prev = -1
    for ch, tc in zip(chars, times):
        if ch.isspace():
            s = spaces[rng.integers(len(spaces))]
        else:
            k = rng.integers(len(keys))
            if k == prev:
                k = (k + 1) % len(keys)
            prev = k
            s = keys[k]
        s = pitch(s, rng.uniform(0.97, 1.03)) * 10 ** (rng.uniform(-2.0, 2.0) / 20)
        put(buf, s, tc)
    if ring:
        put(buf, bell * 0.8, t_bell)
    if ret:
        put(buf, rtn, t_ret)
    buf = norm(buf, 0.8) * 10 ** (gain_db / 20)
    return buf, [{'kyTu': c, 'giay': round(float(t), 4)} for c, t in zip(chars, times)]


def nghe_thu():
    demo = np.zeros(int(15 * SR))
    for text, cps, at, r_, b_ in (('Hà Nội · Tháng 12 năm 1946', 14, 0.3, True, False),
                                  ('— Giải tán lực lượng tự vệ', 30, 5.0, True, False),
                                  ('Hạn chót: sáng 20.12.1946', 24, 7.9, False, True),
                                  ('1946 – 1950', 12, 11.6, False, True)):
        x, _ = go(text, cps, 0, ret=r_, ring=b_)
        put(demo, x, at)
    write_wav(os.path.join(SFX_DIR, 'nghe-thu.wav'), fades(norm(demo, 0.8), fout=0.3))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Bộ tiếng máy chữ (cắt từ bản thu thật)')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('tach', help='Cắt bộ tiếng mẫu từ bản thu gốc vào sfx/may-chu/')
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
    if a.cmd == 'tach':
        tach()
    else:
        x, times = go(a.text, a.cps, a.start, a.jitter, a.seed, a.ret, a.bell, a.gain_db)
        write_wav(a.out, x)
        with open(os.path.splitext(a.out)[0] + '.json', 'w') as f:
            json.dump({'text': a.text, 'cps': a.cps, 'thoiDiemKyTu': times}, f, ensure_ascii=False, indent=1)
        print(f'Đã tạo {a.out} ({len(x) / SR:.2f}s, {len(times)} ký tự)')
