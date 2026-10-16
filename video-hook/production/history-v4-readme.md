# Video lịch sử V4 — đồng bộ chữ phần quân ta

Sửa từ V3, giữ nguyên toàn bộ lời dẫn, thời lượng 132,2 giây, ảnh bản thảo và các yêu cầu loại bỏ SFX trước đó. Bản cũ không bị ghi đè.

## Thay đổi và kiểm tra

C9 trước đây chỉ có nhãn “Ta” rồi đợi tới giây 8,8 mới hiện số khẩu súng, chưa có chữ riêng cho quân số dù lời dẫn đã chuyển sang “Phía ta” ở giây 5,92. Bản V4 bổ sung hai dòng theo nội dung lời dẫn, tách quân số khỏi số súng:

- “2.500 vệ quốc quân” gõ từ giây 5,6; đầy đủ ở 5,833, trước câu “Phía ta” ở 5,92.
- “8.000 tự vệ” gõ từ giây 8,1; đầy đủ ở 8,3, trước cụm “tám nghìn tự vệ” ở 8,48.
- “~2.000 khẩu súng” vẫn hiện riêng theo lời về vũ khí, không dùng làm số quân.

Mốc cục bộ tính từ đầu C9 tại giây 101,7. Nhận dạng mốc local tại `../out/history-1946-v4/qa/comparison-transcript.json`; đây là dữ liệu căn tiếng, không phải nguồn tư liệu lịch sử. File lời dẫn PCM trùng SHA-256 với V3; các mốc đầu/cuối của mọi cảnh giữ nguyên. Kiểm tra tại `qa/recording-alignment.json`, `qa/verification.json`, ảnh `qa/final-phia-ta.png` và `qa/c09.png`.

## Dựng lại

Chạy từ `F:/VNR` bằng Node/tsx của tool `F:/AI-auto-generate-video`. Script `video-hook/scripts/render-history-v4.ts` hỗ trợ `--prepare`, `--render-comparison`, `--assemble-comparison`, `--finalize`, `--verify`, `--extract-final`. `--assemble-comparison` dùng hình V3 cho các cảnh không đổi, thay đúng 420 khung hình gồm C9 và một giây hòa cảnh sang C10. Có thể dùng `--render` để dựng toàn bộ trực tiếp từ template tự thiết kế `frame-vnr-history-v4`.

Âm thanh dựng bằng `create-history-v4-soundtrack.py`; kiểm tra đồng bộ và các yêu cầu trước bằng `verify-history-v4-audio.py`. Đầu ra gồm Full HD `hook.mp4`, `hook-720p.mp4` và clip xem nhanh cảnh đã sửa `comparison-review.mp4` trong `out/history-1946-v4/`.
