# Video mở đầu: "20 giờ, đêm 19/12/1946"

Video hook (78 giây, 1920x1080) cho phần thuyết trình *Đường lối kháng chiến toàn quốc và quá trình tổ chức thực hiện (1946–1950)*.

- `out/hook.mp4`: video hoàn chỉnh (có âm thanh nền).
- `index.html`: toàn bộ hoạt hình. Mở bằng trình duyệt để xem trước; bấm chuột để chạy lại từ đầu.
- `audio.py`: tạo âm thanh nền (`out/audio.wav`).
- `render.cjs`: xuất video bằng Playwright + ffmpeg.

## Tài liệu đi kèm

- `tu-lieu-lich-su.md`: tư liệu lịch sử từ giáo trình và các nguồn trên mạng (bối cảnh 11-1946, tương quan lực lượng, trang bị hai bên, các điểm số liệu lệch nhau), có ghi nguồn.
- `kich-ban-loi-dan.md`: kịch bản lời dẫn theo từng cảnh, bản đầy đủ (~2 phút) và bản rút gọn (~1 phút 25).
- `thiet-ke-anh-minh-hoa.md`: thiết kế 13 ảnh minh họa (A01–A13) và 4 ảnh slide, kèm prompt tiếng Anh cho AI tạo ảnh.

## Sửa nội dung rồi xuất lại

1. Sửa chữ trong `index.html` (phụ đề nằm trong `CAPTIONS`, lời kêu gọi nằm trong `QUOTE`).
2. Xem nhanh vài khung hình: `node render.cjs --stills 10,42,68`
3. Xuất video: `python3 audio.py && node render.cjs`
