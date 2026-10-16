# Video lịch sử V3 — chỉnh nhịp và âm thanh

Bản dựng sửa từ V2 theo phản hồi của người dùng, vẫn dùng template lịch sử tự thiết kế, không dùng mẫu có sẵn của tool. Thiết kế nền tảng lấy từ commit `ba8b2e2`; template mới tại `../templates/history-v3/index.html`, cài vào `F:/AI-auto-generate-video/templates/frame-vnr-history-v3/`.

## Thay đổi

- Loại bỏ toàn bộ tiếng gạt dòng và chuông ở cuối dòng/câu. Giữ tiếng gõ từng ký tự.
- Bỏ âm nhấn trống/nổ ở màn tiêu đề kết (mốc 02:09,3 của V2, tương ứng 02:04,3 sau khi cắt 5 giây). Cảnh kết chỉ giữ lời dẫn, nhạc nền và tiếng gõ chữ.
- Cảnh C4 (tối hậu thư) chỉ còn hiệu ứng gõ chữ; bỏ tiếng lật lịch, trượt giấy và các âm nhấn cuối dòng. Lời dẫn và nhạc nền giữ nguyên.
- Rút C2 từ 15 xuống 10 giây: bỏ 5 giây chờ giữa mốc 14.9.1946 và cảnh 11.1946, không cắt hay tăng tốc lời dẫn. Tất cả cảnh sau dịch sớm 5 giây, vẫn đồng bộ hình/tiếng.
- C8 dùng nguyên ảnh `C:/Users/pgb31/Downloads/OIP (2).webp`, sao lưu tại `../assets/history-1946-v3/loi-keu-goi-ban-thao.webp`. Trình bày đủ hai trang ở bên phải, giữ tỷ lệ gốc, không cắt, chỉnh nét chữ hay tạo lại bằng AI. Phần trích lời và bản thu do người dùng cung cấp giữ nguyên nhịp và cao độ như V2.

## Đầu ra và kiểm tra

Đầu ra riêng tại `../out/history-1946-v3/`: `hook.mp4` (1080p/30 fps), `hook-720p.mp4`, `timeline.json`, `sfx-events.json`, `mix.wav`, `preview.html` và `qa/`. Thời lượng **132,2 giây / 3.966 khung hình**. Các bản V1, V2 được giữ nguyên.

MP4 Full HD đã giải mã toàn bộ thành công: H.264/AAC, 30 fps, −16,01 LUFS, đỉnh −1,39 dBTP; đủ bốn khoảng đen, riêng khoảng trước tiếng pháo ở cảnh khai hỏa vẫn dài đúng một giây. Bản 720p có cùng thời lượng và số khung hình.

`qa/recording-alignment.json` kiểm tra: không còn sự kiện chuông/gạt dòng, C4 chỉ có tiếng gõ, bớt đúng 5 giây, không cắt lời dẫn C2, ảnh trùng SHA-256 với file người dùng gửi, bản thu trích 26,42 giây phát tốc độ 1× và tương quan PCM 1,0. `qa/verification.json` lưu kết quả giải mã toàn bộ MP4, số khung hình, âm lượng và bốn khoảng đen; ảnh kiểm tra từng cảnh tại `qa/c01.png`–`qa/c11.png`.

## Dựng lại

Chạy từ `F:/VNR`. Hai file lời C10 đã có cache trong `out/history-1946-v3/voice/`; không cần tổng hợp lại khi chỉ sửa hình và hiệu ứng.

```powershell
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v3.ts --prepare
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/create-history-v3-soundtrack.py
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v3.ts --render
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v3.ts --finalize
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v3.ts --extract-final
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v3.ts --verify
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/verify-history-v3-audio.py
```

Không commit/push các sản phẩm lên GitHub.
