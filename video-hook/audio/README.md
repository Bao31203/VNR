# Âm thanh cho video hook

## Tiếng máy chữ: `sfx/may-chu/`

Tất cả được **cắt từ bản thu máy chữ cơ thật** `sfx/may-chu/goc/sea-you-later-typewriter-301419.mp3`. Bản thu dài 91 giây, có khoảng 430 tiếng gõ, 3 tiếng chuông và 3 lần gạt dòng; đây là file người làm video cung cấp.

Các file cắt ra đều là WAV 48 kHz mono, đã chuẩn hóa âm lượng.

| File | Âm thanh | Dùng khi |
|---|---|---|
| `phim-01.wav` … `phim-12.wav` | 12 tiếng gõ phím khác nhau. Tiếng "cạch" chính nằm ở **10 ms đầu file** | **Mỗi ký tự** khi chữ hiện ra như đánh máy. Dùng luân phiên ngẫu nhiên |
| `phim-cach-01.wav`, `phim-cach-02.wav` | Hai tiếng gõ trầm nhất trong bản thu | Mỗi dấu cách |
| `gat-dong-01.wav`, `gat-dong-02.wav` | Gạt cần xuống dòng, bánh cóc chạy "rrrrt" (khoảng 1,3–1,5 s) | Cuối các dòng có `returnSound` trong `style/video-style.json` |
| `chuong-01.wav`, `chuong-02.wav` | Chuông "ting" của máy chữ, ngân khoảng 1,7 s | Gõ xong các dòng có `bell` (hạn chót tối hậu thư, năm 1946 – 1950) |
| `nghe-thu.wav` | Nghe thử 4 dòng chữ của video, gõ đúng tốc độ thiết kế | Để nghe trước |

## Tạo sẵn tiếng gõ cho một dòng chữ

```bash
python3 may_chu.py go "Hà Nội · Tháng 12 năm 1946" --cps 14 --return -o c1.wav
python3 may_chu.py go "Hạn chót: sáng 20.12.1946" --cps 24 --bell --jitter 0 -o han-chot.wav
```

- Mỗi ký tự có **đúng một tiếng gõ thật**. Dấu cách dùng tiếng phím cách.
- `--return` thêm tiếng gạt dòng ở cuối. `--bell` thêm tiếng chuông.
- Kèm theo là file `.json` ghi giây xuất hiện của từng ký tự, để căn với hình.
- `--jitter 0`: gõ đều tuyệt đối, khớp với hiệu ứng "Đánh máy" của CapCut. Mặc định là 0,2 (nhịp lệch ±20% cho giống người gõ thật).
- Thời lượng phần gõ bằng số ký tự chia cho `--cps`. Kéo dòng chữ trong công cụ dựng cho đúng bằng thời lượng này.

## Cắt lại từ bản thu

Chạy `python3 may_chu.py tach` để cắt lại toàn bộ bộ tiếng từ file gốc. Lệnh này cần `ffmpeg`.
- Tiếng phím được chọn tự động: chỉ lấy tiếng đứng riêng, không dính tiếng phím kế tiếp.
- Vị trí chuông và gạt dòng được ghi sẵn trong `may_chu.py` (`BELLS`, `RETURNS`). Các vị trí này chỉ đúng với file gốc này.

## Mức âm lượng khi trộn

Theo `style/thiet-ke-style-video.md`, mục 5.2:
- Tiếng gõ ở **−18 dB** khi không có lời dẫn.
- **−28 dB** khi lời dẫn đang nói.
- **−30 dB** ở cảnh Lời kêu gọi (C8).
