# Video mở đầu: "20 giờ, đêm 19/12/1946"

Video hook (78 giây, 1920x1080) cho phần thuyết trình *Đường lối kháng chiến toàn quốc và quá trình tổ chức thực hiện (1946–1950)*.

- `out/hook.mp4`: video hoàn chỉnh (có âm thanh nền).
- `index.html`: toàn bộ hoạt hình. Mở bằng trình duyệt để xem trước; bấm chuột để chạy lại từ đầu.
- `audio.py`: tạo âm thanh nền (`out/audio.wav`).
- `render.cjs`: xuất video bằng Playwright + ffmpeg.

## Sửa nội dung rồi xuất lại

1. Sửa chữ trong `index.html` (phụ đề nằm trong `CAPTIONS`, lời kêu gọi nằm trong `QUOTE`).
2. Xem nhanh vài khung hình: `node render.cjs --stills 10,42,68`
3. Xuất video: `python3 audio.py && node render.cjs`
