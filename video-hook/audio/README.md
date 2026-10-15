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

## Tiếng pháo: `sfx/phao/`

Làm từ **bản thu pháo thật** `sfx/phao/goc/universfield-powerful-cannon-shot-02-487887.mp3` (1,07 giây, stereo), file do người làm video cung cấp. Chạy `python3 phao.py` để tạo lại.

| File | Âm thanh | Dùng ở |
|---|---|---|
| `phao-gan.wav` | Tiếng nổ gần, nguyên gốc (1 s) | Dự phòng |
| `phao-gan-vang.wav` | Tiếng nổ gần, có **vang dội giữa phố** khoảng 3 s | **C7**: pháo đài Láng khai hỏa, cùng khung hình với chớp trắng và rung |
| `phao-xa-01…03.wav` | **Pháo vọng từ xa**: trầm, tối màu, vang xa. Ba biến thể trầm bổng khác nhau | **C3**: pháo hạm nã vào Hải Phòng, mỗi lần chớp sáng một file |
| `nghe-thu-phao.wav` | Nghe thử: 3 tiếng pháo xa, rồi 1 tiếng pháo gần | Để nghe trước |

- Đầu tiếng nổ nằm ở **10 ms đầu file**. Khi dựng, đặt file sớm 10 ms so với khung hình chớp sáng.
- Tiếng pháo nặng về dải trầm: **thử trên loa của lớp học**. Nếu không rõ thì tăng âm lượng.

## Tiếng súng, giao tranh: `sfx/sung/`

Làm từ **2 bản thu thật** do người làm video cung cấp, nằm trong `sfx/sung/goc/`:
- `freesound_community-clean-machine-gun-burst-98224.mp3`: một loạt súng máy 16 phát.
- `dragon-studio-gunshots-firing-repeatedly-511326.mp3`: tràng bắn dày đặc.

Chạy `python3 sung.py` để tạo lại. Script này cần `phao.py` nằm cùng thư mục.

| File | Âm thanh | Dùng ở |
|---|---|---|
| `giao-tranh-xa.wav` | **Nền giao tranh khắp thành phố**, 10 s: tràng bắn dày, loạt súng máy, phát lẻ ở xa gần và trái phải khác nhau, vang giữa các dãy nhà, nhỏ dần ở cuối | **C7 từ 1,8 s** (ngay sau đại bác) đến hết cảnh, nhỏ dần trong 2 s đầu C8 |
| `sung-may-loat.wav` | Loạt súng máy gần, nguyên gốc | Dự phòng |
| `sung-ban-lien-tiep.wav` | Tràng bắn dày đặc, nguyên gốc | Dự phòng |
| `phat-sung-01…06.wav` | Phát súng lẻ (cắt từ loạt súng máy), có chút vang | Rải thêm nếu muốn dày hơn |
| `nghe-thu-sung.wav` | Nghe thử đúng như cảnh C7: im lặng, đại bác nổ, rồi giao tranh nổ ran | Để nghe trước |

Khi trộn, nền giao tranh **thấp hơn tiếng đại bác khoảng 12 dB**. Khi lời dẫn đang nói, hạ thêm 6 dB.

## Mức âm lượng khi trộn

Theo `style/thiet-ke-style-video.md`, mục 5.2:
- Tiếng gõ ở **−18 dB** khi không có lời dẫn.
- **−28 dB** khi lời dẫn đang nói.
- **−30 dB** ở cảnh Lời kêu gọi (C8).
