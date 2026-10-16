# V7: ảnh và phim tư liệu thật

V7 giữ nguyên **toàn bộ âm thanh, chữ, đồ họa và nhịp** của V6. Chỉ thay lớp hình nền:

- Cảnh có tư liệu thật: dùng ảnh Bảo tàng Lịch sử Quốc gia hoặc phim tư liệu cắt từ video tham khảo, tất cả đen trắng.
- Cảnh chưa có tư liệu thật: giữ tranh AI của V6 nhưng chuyển đen trắng, ghi rõ "Tranh minh họa (AI)".
- Mỗi hình có một dòng chú thích và nguồn, chữ nhỏ ở góc dưới phải. Không có màn "Tư liệu sử dụng" ở cuối.

Âm thanh V7 là **rãnh âm thanh của V6 chép nguyên** (`-c:a copy`), không giải mã lại.

## Từng cảnh

| Cảnh | Thời gian | Hình nền V7 | Loại |
|---|---|---|---|
| C1 | 0,0 – 5,9 | Nhà hát Lớn Hà Nội: toàn cảnh, rồi cận băng rôn "Hồ Chủ tịch muôn năm" (T1) | Phim |
| C2 | 5,9 – 10,9 | Bản tuyên bố Hiệp định Sơ bộ 6-3-1946 (BT1), khung ảnh in | Ảnh |
| C2 | 10,9 – 15,9 | Hồ Chí Minh và Jean Sainteny, 1946 (T2), khung ảnh in | Phim |
| C3 | 15,9 – 18,9 | Tàu chiến Pháp ở cảng Hải Phòng, 3-1946 (BT2), khung ảnh in | Ảnh |
| C3 | 18,9 – 22,9 | Tàu chiến Pháp trên biển (T4) | Phim |
| C3 | 22,9 – 27,9 | Khói lửa (T5) | Phim |
| C4 | 27,9 – 30,9 | Phố, nhìn qua vai lính đội mũ sắt (T6a, British Pathé) | Phim |
| C4 | 30,9 – 33,9 | Lính đi trong nhà đổ nát (T8a) | Phim |
| C4 | 33,9 – 41,9 | Tờ lịch, tối hậu thư | Đồ họa V6 |
| C5 | 42,2 – 51,2 | Ngôi nhà ở làng Vạn Phúc (BT3), khung ảnh in | Ảnh |
| C6 | 51,2 – 63,2 | Chiến lũy; nhà máy điện và đồng hồ | Tranh AI, đen trắng |
| C7 | 63,2 – 64,2 | Màn đen | V6 |
| C7 | 64,2 – 70,0 | Pháo đài Láng khai hỏa | Tranh AI, đen trắng |
| C7 | 70,0 – 77,0 | Đổi hình đúng 3 loạt súng: khẩu đội trong khói (T6b), bãi cháy (T7b), đống đổ nát bốc khói (T6c), British Pathé | Phim |
| C8 | 77,0 – 106,7 | Nền đỏ, ngôi sao, bản thảo Lời kêu gọi | Giữ nguyên V6 |
| C9 | 106,7 – 119,7 | Trái: lính Pháp trên phố đầy khói (T7a, British Pathé). Phải: quân dân Hà Nội | Phim / Tranh AI đen trắng |
| C10 | 119,7 – 128,7 | Quyết tử quân ôm bom ba càng | Tranh AI, đen trắng |
| C11 | 128,7 – 137,2 | Người dọn gạch vụn trên phố (T8b) | Phim |

Mã T và BT xem `assets/tu-lieu/nguon-tu-lieu.json`.

## Dựng lại V7

Cần Node 22, ffmpeg và Playwright (Chromium).

```bash
cd video-hook
node v7/dung-v7.mjs                      # timeline V6 dựng lại + hình nền V7 → out/history-1946-v7/build/variables-v7.json
node v7/xuat-hinh.cjs --template templates/history-v7/index.html \
  --vars out/history-1946-v7/build/variables-v7.json \
  --video out/history-1946-v7/build/video-silent.mp4 --workers 3 --crf 18
ffmpeg -i out/history-1946-v7/build/video-silent.mp4 -i out/history-1946-v6/hook.mp4 \
  -map 0:v:0 -map 1:a:0 -c copy -movflags +faststart out/history-1946-v7/hook.mp4
```

Muốn đổi hình của cảnh nào thì sửa `v7/canh-v7.json` rồi chạy lại ba lệnh trên. Ảnh mới đặt vào `assets/tu-lieu/anh/`, phim vào `assets/tu-lieu/phim/`.

## Các file

| File | Việc |
|---|---|
| `dung-lai-timeline-v6.mjs` | Dựng lại `timeline.json` và `variables.json` của V6 (repo thiếu hai file này). Chạy lại đúng logic của `scripts/render-history-v4.ts` và `render-history-v6.ts`; thời lượng cảnh đo từ `hook.mp4` của V6. Script tự kiểm tra 11 mốc đầu cảnh và tổng 4116 khung trùng V6. |
| `canh-v7.json` | Hình nền V7 cho từng cảnh. |
| `dung-v7.mjs` | Ghép timeline V6 với `canh-v7.json`, tách khung hình phim tư liệu ra JPG. |
| `xuat-hinh.cjs` | Xuất từng khung bằng Chromium rồi mã hóa H.264. |
| `phong-to-anh.py` | Phóng to ảnh nhỏ ×4 bằng Real-ESRGAN (chạy CPU). |
| `../templates/history-v7/index.html` | Trang dựng V7: sao từ V4, thêm lớp phim tư liệu, khung ảnh in, đen trắng và dòng nguồn. |

## Kiểm tra đã làm

- Dựng 19 khung bằng timeline dựng lại với trang V4 gốc, so với cùng khung trong `hook.mp4` V6: chữ đánh máy dừng đúng ký tự, số đếm trùng, PSNR 33–40 dB (phần lệch do lớp nhiễu hạt và nén).
- V7 cùng số khung (4116), cùng độ dài (137,2 s) với V6. Rãnh âm thanh V7 trùng từng byte với V6.
