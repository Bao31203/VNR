# Video lịch sử — bản V9 (không còn tranh AI)

[Video Full HD](hook.mp4) · [Bản nhẹ 720p](hook-720p.mp4) · [Storyboard mỗi 2 giây](storyboard.jpg)

Dài 137,2 giây, 1920 × 1080, 30 hình/giây, 4116 khung, giống hệt V6, V7 và V8.

- **Âm thanh chép nguyên từ V6** (không giải mã lại): rãnh âm thanh của V9 và V6 trùng mã SHA-256 `036510782575fc11d99a56a345fefc78e70245bdafa65386ed961bfa811c017c`.
- So với V8, thay nốt 3 tranh AI cuối cùng bằng ảnh tư liệu nhóm gửi: chiến đấu trên đường phố (ảnh TTXVN) và nhà máy điện Yên Phụ (C6), chiến sĩ quyết tử với bom ba càng (C10). Video không còn tranh AI.
- Chữ, đồ họa, số liệu, nhịp: giữ nguyên V6. Mỗi hình có dòng chú thích ở góc dưới phải.

Bảng thay đổi và cách dựng lại: [`v9/README.md`](../../v9/README.md).

Nén và ghép âm thanh (giống V7, V8):

```bash
cd video-hook/out/history-1946-v9
ffmpeg -i build/video-silent.mp4 -c:v libx264 -preset slow -b:v 4600k -pass 1 -passlogfile build/x264pass -an -f null /dev/null
ffmpeg -i build/video-silent.mp4 -i ../history-1946-v6/hook.mp4 -map 0:v:0 -map 1:a:0 -c:v libx264 -preset slow -b:v 4600k \
  -maxrate 9000k -bufsize 12000k -pass 2 -passlogfile build/x264pass -pix_fmt yuv420p -c:a copy -movflags +faststart hook.mp4
ffmpeg -i hook.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -preset slow -crf 23 -c:a copy -movflags +faststart hook-720p.mp4
```

Hai video lưu thẳng trong Git (không qua LFS), bản Full HD dưới 100 MB.

| Tệp | SHA-256 |
| --- | --- |
| `hook.mp4` | `f793e0cc36ae276cbd424062f9378d9d13e2b46963b4a91fc1f08a6a43884886` |
| `hook-720p.mp4` | `190a3dce162cb3701e54334e55a48274e5fbde0d46f06c18daae1ab6ff6263ca` |
