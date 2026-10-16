# Video lịch sử V5 — bộ SFX thật từ repo

Cập nhật nhánh `claude/gifted-dirac-di6lc4` tới `1bc06b43f2a55d9788b980ca46bf1ff423f712d6`, chỉ fast-forward local, không commit/push sản phẩm. Thay âm thanh trên bản hình V4; giữ nguyên bản cũ.

## Âm thanh

- 12 mẫu phím và 2 mẫu phím cách từ `audio/sfx/may-chu/`; dùng ngẫu nhiên, cao độ ±3%, mức ±2 dB theo hướng dẫn repo. Căn tiếng cạch vào đúng khung hình từng ký tự, bù phần đầu mẫu khoảng 10 ms.
- Đại bác: dùng toàn bộ file gốc `universfield-powerful-cannon-shot-02-487887.mp3` tại ba lần chớp C3 và lúc 1 giây C7, gain nguồn 1×, đặt file sớm 85 ms.
- Súng C7: toàn bộ `dragon-studio-gunshots-firing-repeatedly-511326.mp3` tại 1,8/5,9 giây và `freesound_community-clean-machine-gun-burst-98224.mp3` tại 4,1 giây. Bù onset 23/25 ms; hạ 6 dB dưới lời dẫn.
- Không cắt, thêm vang, lọc, đổi tốc độ hay nén động tiếng pháo/súng. Chỉ giải mã, đổi sample rate khi cần và chỉnh mức khi trộn. Master dùng gain cố định −4,19 dB, không saturation/limiter; xuất đo được −17,65 LUFS, đỉnh −1,95 dBTP.
- Giữ yêu cầu trực tiếp của người dùng: không chuông/gạt dòng; C4 chỉ có SFX gõ chữ; không tiếng nổ/trống ở màn kết. Không sử dụng các file nghe thử đã ghép sẵn của repo.

Khoảng đen hình C7 vẫn đủ một giây. Cửa sổ im lặng âm thanh kết thúc sớm 85 ms để giữ nguyên toàn bộ phần đầu file đại bác, cho tiếng nổ chính trùng chớp ở giây 1,0. Lời dẫn, giọng đọc Bác, ảnh bản thảo, nhịp rút ngắn C2 và chữ bổ sung C9 giữ nguyên V4.

## Kiểm tra và dựng lại

Đầu ra tại `out/history-1946-v5/`, Full HD và 720p đều 3.966 khung hình, 132,2 giây. SHA-256 luồng hình của cả hai file trùng hoàn toàn với V4; `voice.wav` cũng trùng nguyên file. Đã giải mã MP4 cuối và kiểm tra bốn khoảng đen, đỉnh âm thanh, SHA-256 của 17 file SFX, đủ 1.067 tiếng gõ và 7 lần dùng nguyên bản thu pháo/súng. Báo cáo ở `qa/verification.json`, `qa/sfx-provenance.json`, `qa/recording-alignment.json` và `qa/mastering.json`.

Chạy từ `F:/VNR`:

```powershell
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v5.ts --prepare
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/create-history-v5-soundtrack.py
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v5.ts --finalize
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v5.ts --verify
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/verify-history-v5-audio.py
```
