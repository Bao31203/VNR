# Tiếng súng, giao tranh cho video hook, làm từ hai bản thu thật:
#   sfx/sung/goc/freesound_community-clean-machine-gun-burst-98224.mp3   (súng máy, 1 loạt 16 phát, 1,6 s)
#   sfx/sung/goc/dragon-studio-gunshots-firing-repeatedly-511326.mp3     (bắn liên tiếp dày đặc, 2,2 s)
#
#   python3 sung.py
# tạo ra trong sfx/sung/:
#   sung-may-loat.wav        loạt súng máy gần, nguyên gốc (đã căn đầu tiếng về 10 ms, chuẩn hóa)
#   sung-ban-lien-tiep.wav   bắn liên tiếp dày đặc, nguyên gốc
#   phat-sung-01..06.wav     phát súng lẻ (cắt từ loạt súng máy), có chút vang
#   giao-tranh-xa.wav        nền "giao tranh khắp thành phố" 10 s: nhiều loạt súng và phát lẻ ở xa gần,
#                            trái phải khác nhau, vang giữa các dãy nhà   → C7 từ 1,8 s, nhỏ dần sang C8
#   nghe-thu-sung.wav        nghe thử đúng như cảnh C7: tiếng đại bác rồi giao tranh nổ ran
import os
import numpy as np
from phao import SR, load, write, norm, filt, lp, hp, conv, pad, fade_out, street_ir, resample

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sfx', 'sung')
SUNG_MAY = os.path.join(OUT, 'goc', 'freesound_community-clean-machine-gun-burst-98224.mp3')
LIEN_TIEP = os.path.join(OUT, 'goc', 'dragon-studio-gunshots-firing-repeatedly-511326.mp3')
PHAO_VANG = os.path.join(HERE, 'sfx', 'phao', 'phao-gan-vang.wav')


def align(x, thr=0.05):
    """Cắt để đầu tiếng (vượt 5% đỉnh) nằm ở 10 ms."""
    on = np.argmax(np.abs(x).max(1) > thr * np.abs(x).max())
    return x[max(0, on - int(0.010 * SR)):]


def onsets(m, win=0.005, rise_db=8, gap=0.04):
    n = int(win * SR)
    env = np.array([np.sqrt((m[j:j + n] ** 2).mean()) for j in range(0, len(m) - n, n)])
    db = 20 * np.log10(env + 1e-9)
    out, last = [], -10**9
    for k in range(2, len(db)):
        if db[k] > db.max() - 20 and db[k] - db[k - 2] > rise_db and (k - last) * win > gap:
            out.append(k * win)
            last = k
    return out


def pan(x, p):
    """Đặt âm thanh sang trái (-1) / phải (+1)."""
    m = x.mean(1)
    a = (p + 1) * np.pi / 4
    return np.stack([m * np.cos(a), m * np.sin(a)], axis=1)


def place(bus, sig, at, gain_db=0.0, p=0.0, lp_fc=None, factor=1.0):
    if factor != 1.0:
        sig = resample(sig, factor)
    if lp_fc:
        sig = filt(sig, lp(lp_fc, 2))
    sig = pan(sig, p) * 10 ** (gain_db / 20)
    a = int(at * SR)
    b = min(len(bus), a + len(sig))
    if a < len(bus):
        bus[a:b] += sig[:b - a]


def main():
    may = align(load(SUNG_MAY))
    lien = align(load(LIEN_TIEP))
    write(os.path.join(OUT, 'sung-may-loat.wav'), fade_out(norm(may, -1.0), 0.15))
    write(os.path.join(OUT, 'sung-ban-lien-tiep.wav'), fade_out(norm(lien, -1.0), 0.3))

    # phát súng lẻ: cắt từng phát trong loạt súng máy, thêm chút vang cho có đuôi
    ons = onsets(may.mean(1))
    shots = []
    for i, t in enumerate(ons[:-1]):
        a = max(0, int((t - 0.005) * SR))
        b = int((ons[i + 1] - 0.004) * SR)
        s = may[a:b].copy()
        s[-int(0.015 * SR):] *= np.linspace(1, 0, int(0.015 * SR))[:, None]
        shots.append(align(s))
    ir_short = street_ir(21, 0.9, [(40, 0.4), (90, 0.3), (150, 0.2)], 3000)
    for i, s in enumerate(shots[:6], 1):
        wet = conv(pad(s, 0.8), ir_short)[:len(s) + int(0.8 * SR)]
        z = pad(s, 0.8) + 0.35 * wet / np.max(np.abs(wet))
        write(os.path.join(OUT, f'phat-sung-{i:02d}.wav'), fade_out(norm(z, -3.0), 0.3))

    # nền giao tranh khắp thành phố, 10 giây
    rng = np.random.default_rng(1946)
    dur = 10.0
    bus = np.zeros((int(dur * SR), 2))
    # những tràng bắn dày đặc ở xa
    for at, g, p, f, fac in ((0.6, -6, -0.4, 1600, 1.0), (4.8, -9, 0.5, 1400, 0.94), (7.6, -13, -0.1, 1300, 0.97)):
        place(bus, lien, at, g, p, f, fac)
    # các loạt súng máy ở khoảng cách vừa (có loạt chỉ lấy một nửa cho đỡ đều)
    half = may[:int(len(may) * 0.55)]
    for at, sig, g, p, f, fac in ((1.6, may, -4, 0.35, 2600, 1.0), (3.9, half, -7, -0.6, 2300, 0.97),
                                  (6.3, may, -9, 0.2, 2100, 1.02), (8.4, half, -12, -0.3, 1900, 0.95)):
        place(bus, sig, at, g, p, f, fac)
    # phát súng lẻ tẻ rải khắp nơi
    for _ in range(30):
        at = rng.uniform(0.2, 9.0)
        place(bus, shots[rng.integers(len(shots))], at, rng.uniform(-18, -6), rng.uniform(-0.9, 0.9),
              rng.uniform(1800, 3500), rng.uniform(0.9, 1.05))
    bus = filt(bus, hp(50, 2))
    ir = street_ir(31, 2.2, [(70, 0.45), (130, 0.38), (210, 0.3), (340, 0.22), (520, 0.15)], 2200)
    wet = conv(bus, ir)[:len(bus)]
    amb = 0.55 * bus + wet * (np.max(np.abs(bus)) / (np.max(np.abs(wet)) + 1e-9))
    n_in = int(0.15 * SR)
    amb[:n_in] *= np.linspace(0, 1, n_in)[:, None]
    amb = fade_out(norm(amb, -6.0), 2.5)
    write(os.path.join(OUT, 'giao-tranh-xa.wav'), amb)

    # nghe thử như cảnh C7: im lặng 1 s, đại bác nổ, rồi giao tranh nổ ran từ 1,8 s
    demo = np.zeros((int(11.5 * SR), 2))
    if os.path.exists(PHAO_VANG):
        from phao import load as load_any
        boom = load_any(PHAO_VANG)
        a = int(1.0 * SR)
        demo[a:a + len(boom)] += boom[:len(demo) - a]
    a = int(1.8 * SR)
    demo[a:a + len(amb)] += 1.4 * amb[:len(demo) - a]
    write(os.path.join(OUT, 'nghe-thu-sung.wav'), fade_out(norm(demo, -1.0), 0.5))
    print(f'Đã tạo tiếng súng trong {OUT} (cắt được {len(shots)} phát lẻ từ loạt súng máy)')


if __name__ == '__main__':
    main()
