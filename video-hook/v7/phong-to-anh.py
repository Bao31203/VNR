# Phóng to ảnh tư liệu nhỏ ×4 bằng Real-ESRGAN (model realesrgan-x4plus, chạy CPU qua thư viện ncnn).
#
# Cài đặt một lần:
#   pip install ncnn pillow numpy
#   tải realesrgan-ncnn-vulkan-20220424-ubuntu.zip (hoặc bản windows) từ
#   https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.2.5.0 rồi giải nén, lấy thư mục models/
#
# Dùng:
#   python3 phong-to-anh.py --models <thư mục models> anh-vao.jpg anh-ra.png
#
# Ảnh được chia thành ô nhỏ có chồng mép để không tốn RAM; ảnh đen trắng vẫn giữ đen trắng.
import argparse
import numpy as np
import ncnn
from PIL import Image

SCALE = 4


def upscale(path_in, path_out, models, tile=128, pad=12, threads=4):
    net = ncnn.Net()
    net.opt.use_vulkan_compute = False
    net.opt.num_threads = threads
    net.load_param(f'{models}/realesrgan-x4plus.param')
    net.load_model(f'{models}/realesrgan-x4plus.bin')

    img = Image.open(path_in)
    gray = img.mode in ('L', 'LA') or (img.mode == 'RGB' and _is_gray(img))
    rgb = np.asarray(img.convert('RGB'), dtype=np.float32) / 255.0
    h, w, _ = rgb.shape
    out = np.zeros((h * SCALE, w * SCALE, 3), dtype=np.float32)
    for y0 in range(0, h, tile):
        for x0 in range(0, w, tile):
            y1, x1 = min(h, y0 + tile), min(w, x0 + tile)
            ya, xa = max(0, y0 - pad), max(0, x0 - pad)
            yb, xb = min(h, y1 + pad), min(w, x1 + pad)
            patch = np.ascontiguousarray(rgb[ya:yb, xa:xb].transpose(2, 0, 1))
            ex = net.create_extractor()
            ex.input('data', ncnn.Mat(patch))
            _, res = ex.extract('output')
            res = np.array(res).transpose(1, 2, 0)
            oy, ox = (y0 - ya) * SCALE, (x0 - xa) * SCALE
            out[y0 * SCALE:y1 * SCALE, x0 * SCALE:x1 * SCALE] = res[oy:oy + (y1 - y0) * SCALE, ox:ox + (x1 - x0) * SCALE]
    result = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    if gray:
        result = result.convert('L')
    result.save(path_out)
    return result.size


def _is_gray(img):
    a = np.asarray(img.convert('RGB'), dtype=np.int16)
    return np.abs(a[..., 0] - a[..., 1]).mean() < 2 and np.abs(a[..., 1] - a[..., 2]).mean() < 2


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Phóng to ảnh ×4 bằng Real-ESRGAN (CPU)')
    ap.add_argument('--models', required=True)
    ap.add_argument('src')
    ap.add_argument('dst')
    a = ap.parse_args()
    print('Kích thước mới:', upscale(a.src, a.dst, a.models))
