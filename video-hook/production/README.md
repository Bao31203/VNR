# Video lịch sử: 20 giờ 3 phút, đêm 19.12.1946

Video 11 cảnh, 1920×1080, 30 fps, dài 112,8 giây. Kịch bản dựa vào `../kich-ban-loi-dan.md`, `../tu-lieu-lich-su.md` và giáo trình trong repo; dùng câu trích Lời kêu gọi theo giáo trình. Nguồn được clone tại commit `3987c84`.

## Thiết kế

Template mới hoàn toàn ở `../templates/history/index.html`, được cài vào `F:/AI-auto-generate-video/templates/frame-vnr-history/` để gọi bộ render của công cụ. Không sử dụng thiết kế của các template có sẵn. Bố cục riêng cho mở đầu, đường thời gian, tối hậu thư, quyết định kháng chiến, đồng hồ, pháo đài, lời kêu gọi, tương quan lực lượng, câu hỏi và tiêu đề kết.

Tám tranh AI dạng gouache nằm trong `../assets/history-1946/`. Đây là minh họa, không phải ảnh tư liệu; video có nhãn phân biệt. Font Lora và Be Vietnam Pro lấy từ Google Fonts, kèm giấy phép OFL trong thư mục tài nguyên template.

Giọng dẫn dùng hồ sơ có sẵn `Giọng đọc bài giảng`; phần trích dẫn dùng `Giọng cổ phong - Nhân chi diện V2`. Hai hồ sơ đã có xác nhận sử dụng trong thư viện local. Không mô phỏng giọng Hồ Chí Minh. Phần nhạc nền trầm, tích tắc, tiếng pháo và nhịp tim được tổng hợp mới bằng mã nguồn, không dùng bản nhạc thương mại.

## Đầu ra

Tất cả nằm trong `../out/history-1946/`:

- `hook.mp4`: bản trình chiếu Full HD.
- `hook-720p.mp4`: bản xem trước nhẹ.
- `hook-phude.mp4`: bản Full HD có phụ đề in lên hình.
- `hook.srt`: phụ đề rời, chia theo câu/cụm; mốc nội câu ước lượng theo độ dài chữ, chưa căn chỉnh từng từ bằng nhận dạng giọng nói.
- `voice.mp3`, `script.txt`: lời dẫn riêng và văn bản để chỉnh sửa tiếp.
- `timeline.json`: thời gian thực tế theo từng cảnh sau TTS, làm tròn theo khung hình.
- `preview.html`: xem chuyển động hình trong trình duyệt, không kèm audio. Video MP4 là bản có âm thanh.
- `qa/`: ảnh kiểm tra và kết quả kiểm tra media.

## Dựng lại

Chạy từ `F:/VNR` sau khi OmniVoice ở `127.0.0.1:8123` đã sẵn sàng:

```powershell
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --tts-only
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --prepare
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/create-history-soundtrack.py
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --proof
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --extract-proof
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --render
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --finalize
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --extract-final
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history.ts --verify
```

Sửa chữ, lời đọc, ảnh và khoảng nghỉ trong `history-scenes.json`; sửa thiết kế trong template nguồn, rồi chạy lại từ `--prepare`. TTS có kiểm tra định danh nội dung và cấu hình trước khi dùng lại cache. Template chỉ nhận thời gian tuyệt đối từ renderer; trình xem trước có bộ chạy riêng, không đưa đồng hồ hệ thống vào render.

Các file dựng mới tách biệt với `video-hook/out/hook.mp4` và hoạt hình cũ trong repo. Đây là ghi chú của lần dựng đầu; các phiên bản sau được mô tả trong `history-v2-readme.md` đến `history-v6-readme.md`. Xem [hướng dẫn mã nguồn V6](../docs/source-v6.md) để biết phạm vi mã nguồn công bố và các phụ thuộc local.

## Prompt tạo tranh

Dùng công cụ imagegen tích hợp, không dùng CLI/API riêng. Prompt được lưu tại `image-prompts.md`. Các tranh dùng chung bảng màu xanh than, hổ phách, đỏ gạch và giấy cũ; toàn bộ chữ được dựng bằng HTML.
