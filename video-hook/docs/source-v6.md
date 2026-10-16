# Mã nguồn dựng video lịch sử V6

## Tổng quan

Đây là mã nguồn của quá trình dựng V1–V6 bằng công cụ local `F:/AI-auto-generate-video`, không phải mã nguồn của công cụ đó. Template lịch sử được thiết kế riêng; không dùng mẫu thiết kế có sẵn của công cụ. Bản V6 đã xuất dài 137,2 giây, 30 fps; xem [thư mục video](../out/history-1946-v6/README.md).

## Các thành phần

- [scripts](../scripts/): TypeScript dựng hình, Python phối âm, nhận dạng và kiểm tra âm thanh. Điểm vào V6 là [render-history-v6.ts](../scripts/render-history-v6.ts), [create-history-v6-soundtrack.py](../scripts/create-history-v6-soundtrack.py) và [verify-history-v6-audio.py](../scripts/verify-history-v6-audio.py).
- [templates/history-v4](../templates/history-v4/): template hình V6 sử dụng; `history`, `history-v2`, `history-v3` giữ các phiên bản trước. Font và giấy phép đi cùng từng template.
- [production](../production/): kịch bản, mốc lời đọc, cấu hình bản thu, prompt minh họa và ghi chú từng phiên bản. [Ghi chú V6](../production/history-v6-readme.md) mô tả các chỉnh sửa cuối.
- [style](../style/): thiết kế từng cảnh và cấu hình style gốc của repo.
- [assets](../assets/): minh họa, ảnh bản thảo và bản thu Lời kêu gọi do người dùng cung cấp. Tranh tạo bằng AI là minh họa, không phải ảnh tư liệu.
- [audio](../audio/): các file SFX gốc được dùng ở V5/V6.

## Điều kiện dựng lại

1. Git LFS để tải đủ các file media được quản lý bằng LFS (`git lfs pull`).
2. Windows, Node.js có hỗ trợ `import.meta.dirname`, FFmpeg và ffprobe trên `PATH`. Máy dựng gốc sử dụng Node.js 26 và FFmpeg 8.1.1.
3. Công cụ `F:/AI-auto-generate-video` cùng dependencies của nó: `tsx`, `src/render/template-composer.ts`, `src/assets/audio-tools.ts`, `src/tts/omnivoice-client.ts`. Các đường dẫn tool đang cố định trong script; nếu đổi máy/ổ đĩa cần sửa tương ứng. `video-hook/package.json` chỉ khai báo module, không cài toàn bộ bộ dựng bằng `npm install` tại đây.
4. Python có NumPy; máy dựng gốc dùng `F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe`.
5. Nếu cần tạo lại lời dẫn: OmniVoice tại `127.0.0.1:8123` và hồ sơ giọng đọc đã được cho phép sử dụng, lưu trong tool local. Không kèm hồ sơ, mẫu giọng riêng tư, model hay môi trường ảo trong repo. Phần Lời kêu gọi ở V2 trở đi dùng trực tiếp bản thu người dùng cung cấp, không clone giọng.
6. Script nhận dạng tùy chọn cần `faster-whisper` và model local; các đường dẫn model/Downloads trong script kiểm tra là đường dẫn của máy dựng gốc, cần điều chỉnh khi chuyển máy.

## Luồng dựng và giới hạn hiện tại

Các phiên bản được dựng nối tiếp, không phải một lệnh độc lập chạy từ clone sạch:

- V1 tạo cache lời dẫn trong `out/history-1946/voice/`.
- V2–V4 dùng lại cache lời dẫn V1; từng bước `--prepare` tạo timeline, variables, audio trung gian và cài template riêng vào thư mục templates của tool.
- V5 dùng timeline/voice/hình của V4 và phối lại SFX.
- V6 dùng timeline, SFX, voice và video V5; dựng lại đoạn Pháo đài Láng bằng template V4, chèn thêm 5 giây rồi ghép các đoạn còn lại.

Cache lời dẫn, WAV, timeline/variables và video trung gian trong `out/history-1946*` không nằm trong lần công bố mã nguồn này. Clone repo và tải MP4 V6 **chưa đủ** để chạy ngay `--prepare` của V6: phải có các bước/đầu ra trước đó và tool local. Tạo lại TTS có thể thay đổi thời lượng, nên cần kiểm tra lại mốc chữ và âm thanh. Không bảo đảm tái tạo đúng từng byte MP4 trên máy khác.

## Lệnh V6 trên máy đã có đầu vào V1–V5

Các lệnh dưới đây ghi lại output V6; chỉ chạy khi muốn dựng lại, không cần chạy để xem mã nguồn hoặc video đã xuất. Chạy từ thư mục gốc repo:

```powershell
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v6.ts --prepare
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/create-history-v6-soundtrack.py
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v6.ts --render-fort
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v6.ts --assemble-fort
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v6.ts --finalize
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v6.ts --verify
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/verify-history-v6-audio.py
```

V6 giữ mức gõ chữ +13 dB so với V5 (bao gồm lần tăng thêm 3 dB cuối), chỉ dời các loạt súng +5 giây/giảm 3 dB, giữ đại bác, và chờ hết súng trước khi chuyển sang Lời kêu gọi. Không bật lại chuông/gạt dòng hay tiếng nổ ở màn kết.

## Tham khảo

- [Quy trình ban đầu](../production/README.md) và các ghi chú `history-v2-readme.md` đến `history-v6-readme.md` trong cùng thư mục.
- [Nguồn âm thanh và mốc câu](../production/history-v2-audio.json).
- [Tài liệu tham khảo người dùng cung cấp](../assets/references/chinh-sua-video/README.md).

Giữ nguyên các giấy phép font đi kèm. Việc đưa tư liệu vào repo không có nghĩa mọi tư liệu đều có cùng giấy phép tái sử dụng.
