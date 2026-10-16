# Video mở đầu: "20 giờ, đêm 19/12/1946"

Video hook (78 giây, 1920x1080) cho phần thuyết trình *Đường lối kháng chiến toàn quốc và quá trình tổ chức thực hiện (1946–1950)*.

- `out/hook.mp4`: video hoàn chỉnh (có âm thanh nền).
- `index.html`: toàn bộ hoạt hình. Mở bằng trình duyệt để xem trước; bấm chuột để chạy lại từ đầu.
- `audio.py`: tạo âm thanh nền (`out/audio.wav`).
- `render.cjs`: xuất video bằng Playwright + ffmpeg.

## Tài liệu đi kèm

- [Mã nguồn dựng video V6](docs/source-v6.md): script, template lịch sử tự thiết kế, tài nguyên và các phụ thuộc cần để dựng lại. [Video V6 đã xuất](out/history-1946-v6/README.md) nằm riêng với mã nguồn.
- `v7/ke-hoach-v7-tu-lieu-that.md`: **kế hoạch V7**, thay tranh vẽ AI của V6 bằng ảnh và phim tư liệu thật. Kèm `v7/v6-storyboard.jpg` và `v7/tham-khao-danh-muc-*.jpg` (ảnh tổng quan có mốc thời gian).
- `style/thiet-ke-style-video.md`, `style/video-style.json`, `style/wireframes/`: **thiết kế style video**, gồm chữ đánh máy kèm tiếng gõ phím, vị trí chữ, chuyển cảnh, màn đen, âm thanh, bố cục từng cảnh. Có sẵn lời nhắn mẫu để giao việc cho AI agent dựng video.
- `ke-hoach-san-xuat.md`: kế hoạch sản xuất video mới, gồm 8 bước, thiết kế chi tiết từng cảnh, quy chuẩn thiết kế và các danh sách kiểm tra.
- `tu-lieu-lich-su.md`: tư liệu lịch sử từ giáo trình và các nguồn trên mạng (bối cảnh 11-1946, tương quan lực lượng, trang bị hai bên, các điểm số liệu lệch nhau), có ghi nguồn.
- `kich-ban-loi-dan.md`: kịch bản lời dẫn theo từng cảnh, bản đầy đủ (~2 phút) và bản rút gọn (~1 phút 25).
- `thiet-ke-anh-minh-hoa.md`: thiết kế 13 ảnh minh họa (A01–A13) và 4 ảnh slide, kèm prompt tiếng Anh cho AI tạo ảnh.

## Sửa nội dung rồi xuất lại

1. Sửa chữ trong `index.html` (phụ đề nằm trong `CAPTIONS`, lời kêu gọi nằm trong `QUOTE`).
2. Xem nhanh vài khung hình: `node render.cjs --stills 10,42,68`
3. Xuất video: `python3 audio.py && node render.cjs`
