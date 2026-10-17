# Video lịch sử — bản V8 (thêm ảnh do nhóm cung cấp)

[Video Full HD](hook.mp4) · [Bản nhẹ 720p](hook-720p.mp4) · [Storyboard mỗi 2 giây](storyboard.jpg)

Dài 137,2 giây, 1920 × 1080, 30 hình/giây, 4116 khung, giống hệt V6 và V7.

- **Âm thanh chép nguyên từ V6** (không giải mã lại): rãnh âm thanh của V8, V7 và V6 trùng mã SHA-256 `036510782575fc11d99a56a345fefc78e70245bdafa65386ed961bfa811c017c`.
- So với V7, thay 5 hình bằng ảnh nhóm tải lên: văn bản Hiệp định Sơ bộ (C2), ngôi nhà ở Vạn Phúc (C5), Pháo đài Láng (C7), quân Pháp và quân ta (C9). Còn C6 và C10 vẫn là tranh AI đen trắng.
- Chữ, đồ họa, số liệu, nhịp: giữ nguyên V6. Mỗi hình có dòng chú thích ở góc dưới phải.

Bảng thay đổi và cách dựng lại: [`v8/README.md`](../../v8/README.md).

Nén và ghép âm thanh (giống V7):

```bash
cd video-hook/out/history-1946-v8
ffmpeg -i build/video-silent.mp4 -c:v libx264 -preset slow -b:v 4600k -pass 1 -passlogfile build/x264pass -an -f null /dev/null
ffmpeg -i build/video-silent.mp4 -i ../history-1946-v6/hook.mp4 -map 0:v:0 -map 1:a:0 -c:v libx264 -preset slow -b:v 4600k \
  -maxrate 9000k -bufsize 12000k -pass 2 -passlogfile build/x264pass -pix_fmt yuv420p -c:a copy -movflags +faststart hook.mp4
ffmpeg -i hook.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -preset slow -crf 23 -c:a copy -movflags +faststart hook-720p.mp4
```

Hai video lưu thẳng trong Git (không qua LFS), bản Full HD dưới 100 MB.

| Tệp | SHA-256 |
| --- | --- |
| `hook.mp4` | `c4cde34e282bf8b3b9c33a74d91d4addf5e8a0d4817ed615d3f1dc89274e27d6` |
| `hook-720p.mp4` | `7f7c5fda1def2ed18a1091ebfa758a8a12dbfc6da93cb313013e8c263cc242ee` |
