# Âm thanh cho video hook

## Bộ tiếng máy chữ: `sfx/may-chu/`

Tất cả là WAV 48 kHz mono, tự tổng hợp bằng `may_chu.py`, không dính bản quyền.

| File | Âm thanh | Dùng khi |
|---|---|---|
| `phim-01.wav` … `phim-06.wav` | Tiếng gõ phím máy chữ cơ "tạch", 6 biến thể | **Mỗi ký tự** khi chữ hiện ra như đánh máy. Dùng luân phiên ngẫu nhiên |
| `phim-cach-01.wav`, `phim-cach-02.wav` | Phím cách, trầm và nhẹ hơn | Mỗi dấu cách |
| `gat-dong.wav` | Gạt cần xuống dòng: "cạch, rắc rắc, xoẹt, cộp" (0,95 s) | Cuối các dòng có `returnSound` trong `style/video-style.json` |
| `chuong.wav` | Chuông "ting" của máy chữ (1,4 s) | Gõ xong các dòng có `bell` (hạn chót tối hậu thư, năm 1946 – 1950) |
| `nghe-thu.wav` | Nghe thử 4 dòng chữ của video, gõ đúng tốc độ thiết kế | Để nghe trước |

## Tạo sẵn tiếng gõ cho một dòng chữ

```bash
python3 may_chu.py go "Hà Nội · Tháng 12 năm 1946" --cps 14 --return -o c1.wav
python3 may_chu.py go "Hạn chót: sáng 20.12.1946" --cps 24 --bell --jitter 0 -o han-chot.wav
```

- Mỗi ký tự có **đúng một tiếng gõ**. Dấu cách dùng tiếng phím cách.
- `--return` thêm tiếng gạt dòng ở cuối. `--bell` thêm tiếng chuông.
- Kèm theo là file `.json` ghi giây xuất hiện của từng ký tự, để căn với hình.
- `--jitter 0`: gõ đều tuyệt đối, khớp với hiệu ứng "Đánh máy" của CapCut. Mặc định là 0,2 (nhịp lệch ±20% cho giống người gõ thật).
- Thời lượng phần gõ bằng số ký tự chia cho `--cps`. Kéo dòng chữ trong công cụ dựng cho đúng bằng thời lượng này.

Chạy `python3 may_chu.py tao` để tạo lại toàn bộ bộ tiếng.

## Mức âm lượng khi trộn

Theo `style/thiet-ke-style-video.md`, mục 5.2:
- Tiếng gõ ở **−18 dB** khi không có lời dẫn.
- **−28 dB** khi lời dẫn đang nói.
- **−30 dB** ở cảnh Lời kêu gọi (C8).
