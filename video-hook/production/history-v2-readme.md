# Video lịch sử V2 theo thiết kế mới của repo

Bản dựng lấy thiết kế tại commit `ba8b2e2` của nhánh `claude/gifted-dirac-di6lc4`. Chữ, kiểu chữ, tọa độ, bố cục và hiệu ứng lấy từ `../style/video-style.json`; template mới nằm tại `../templates/history-v2/index.html` và được cài riêng vào `F:/AI-auto-generate-video/templates/frame-vnr-history-v2/`.

## Bản thu Lời kêu gọi

Nguồn do người dùng cung cấp: `C:/Users/pgb31/Downloads/Loikeugoitoanquockhangchien.mp3`. Bản sao nguyên file được giữ tại `../assets/audio/loi-keu-goi-user-recording.mp3`.

Phân đoạn C8 sử dụng trực tiếp khoảng **00:00.30–00:26.72**, từ “Hỡi đồng bào toàn quốc!” đến “…nhất định không chịu làm nô lệ.” Giữ tốc độ và cao độ gốc; chỉ cắt trích đoạn, làm mềm biên 8 ms, chuẩn hóa âm lượng và ghép vào bản dựng. Không dùng file này làm mẫu tổng hợp hoặc clone giọng.

Các mốc câu được nhận dạng local để căn hình; chữ hiển thị vẫn lấy nguyên văn JSON thiết kế. File nhận dạng thô có thể sai chính tả và không phải tài liệu lịch sử. Mốc hiệu ứng chữ `Không!` theo câu nói ở giây 18,12 của file nguồn. Chi tiết nằm trong `history-v2-audio.json`; checksum nguồn được ghi vào timeline và báo cáo kiểm tra.

## Những thay đổi trên hình và tiếng

- Dùng ba bộ chữ Noto Serif, Be Vietnam Pro và Noto Sans Mono, kèm giấy phép OFL trong thư mục template.
- Chữ thông tin hiện từng ký tự, có con trỏ vàng. Lịch và tiêu đề in sẵn trên giấy giữ cách xuất hiện theo JSON. Tiêu đề giờ nổ súng, chữ `Không!`, câu hỏi và các số liệu giữ các hiệu ứng riêng của thiết kế.
- Lịch 17→18, tối hậu thư, đường thời gian xuyên C2–C3, đồng hồ neo cuối C6, tắt đèn/đen 1 giây, chớp sáng và pháo cùng mốc, nền đỏ và sao mờ ở C8, màn so sánh chia đôi ở C9.
- Mỗi ký tự có một sự kiện âm thanh theo đúng khung hình; có phím cách, gạt dòng và chuông. Foley máy chữ được tổng hợp mới từ sáu biến thể tiếng cơ khí ngắn, không dùng tiếng bàn phím máy tính hoặc bản nhạc thương mại.
- Sáu tranh bổ sung ở `../assets/history-1946-v2/`; các tranh còn lại dùng từ bộ đã tạo. A11b tái sử dụng tranh chiến lũy và lấy bố cục phần người tự vệ cho nửa phải. Không có lớp ảnh tách rời, nên chuyển động máy quay dùng một lớp thay cho parallax nhiều lớp.
- Nền nhạc hạ khi có lời. Có cửa sổ im lặng trước tiếng pháo và nửa giây trước câu hỏi kết.

## Thời lượng và khác biệt với mốc mẫu

Bản Full HD có **4.116 khung hình, 137,2 giây**. C8 dài **29,7 giây** để giữ nguyên nhịp bản thu và đọc đủ dòng nguồn. C1, C7 kéo dài theo độ dài lời dẫn thực tế; C4→C5 có 0,3 giây giữ đen. Các khác biệt thời lượng này thực hiện quy tắc `audioRules.sceneStretch` và căn lại C8 theo file đọc thật. Lời ở C10 tách thành phần bối cảnh và câu hỏi, để câu hỏi vào đúng giây 5,9 sau khoảng im lặng 0,5 giây.

Đầu ra lưu riêng tại `../out/history-1946-v2/`, gồm `hook.mp4`, `hook-720p.mp4`, `voice.wav`, `mix.wav`, `timeline.json`, `sfx-events.json`, bản xem hình `preview.html` và thư mục `qa/`. Bản trước ở `out/history-1946/` được giữ nguyên. Trang preview chỉ phát hình; MP4 là bản có đầy đủ tiếng.

## Kết quả kiểm tra

Bản MP4 cuối đã giải mã toàn bộ thành công, đủ 4.116 khung hình H.264 1080p/30 fps và âm thanh AAC. Đo được −16,29 LUFS, đỉnh −1,49 dBTP; phát hiện đủ bốn khoảng đen, riêng khoảng trước tiếng pháo dài đúng một giây. Bản trích 26,42 giây khi chèn vào rãnh lời có tương quan mẫu PCM bằng 1,0 với bản trích nguồn. Các cửa sổ im lặng của bản phối PCM có biên độ bằng 0 sau chuẩn hóa. Báo cáo máy đọc được ở `qa/verification.json` và `qa/recording-alignment.json`; 11 ảnh kiểm tra ở `qa/c01.png`–`qa/c11.png`.

## Dựng lại

Chạy từ `F:/VNR`:

```powershell
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v2.ts --prepare
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/create-history-v2-soundtrack.py
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v2.ts --proof
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v2.ts --extract-proof
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v2.ts --render
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v2.ts --finalize
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v2.ts --extract-final
node F:/AI-auto-generate-video/node_modules/tsx/dist/cli.mjs video-hook/scripts/render-history-v2.ts --verify
F:/AI-auto-generate-video/.venv-omnivoice/Scripts/python.exe video-hook/scripts/verify-history-v2-audio.py
```

OmniVoice cần chạy khi tạo lại hai đoạn lời C10 chưa có cache. Môi trường nhận dạng tiếng nói local tại `.venv-asr/` chỉ dùng để căn mốc, không phải dependency của bộ render. Chưa commit hoặc push sản phẩm lên GitHub.

## Tranh bổ sung và prompt

Công cụ tạo tranh: imagegen tích hợp. Sáu prompt dưới đây đều dùng tranh gouache 1946, chất giấy và nét cọ, bảng màu xanh than, hổ phách, nâu trầm, đỏ gạch. Không chữ, logo, watermark, đồ vật hiện đại hoặc nhân vật lịch sử có thật.

| File | Prompt cảnh và bố cục |
|---|---|
| `a01-dong-ho.png` | Old Hanoi shophouse interior at night. Antique wooden pendulum wall clock on the right third, oil lamp and old wooden sideboard, warm amber light, left half dark empty wall for a single line of typography. Ordinary analog dial without readable numbers, hands near eight o'clock. Wide 16:9. |
| `a04-thiet-giap.png` | French colonial armored vehicles on a Hanoi street, December 1946. A period M8 Greyhound armored car and M5A1 Stuart light tank, a few soldiers in khaki, distant civilians retreating to doorways, no violence. Main vehicle in lower center, upper third quiet and lower edge clear for caption. Wide 16:9. |
| `a08-nha-may-dien.png` | Yen Phu colonial power-station interior. Steam-driven generators, marble switchboard, brass circular gauges and large knife switches, two anonymous Vietnamese workers seen from behind at a large lever. Workers and controls in lower central portion, upper third empty dark shadow for countdown. Wide 16:9. |
| `a09-phao-khai-hoa.png` | Lang artillery fort at night. Entire old field gun and three anonymous militia artillerymen in lower-left half, bright amber muzzle flash kept below midline, large empty dark navy upper half for white title. Low earthen fort, distant city with lights out. Wide 16:9. |
| `a11a-quan-phap.png` | Low-angle French expeditionary soldiers and period armored vehicles, old Hanoi shophouse backdrop. Figures in middle, upper 20 percent dark sky for label, lower 25 percent quiet street for number. Cold slate blue, muted amber rim light. Portrait 8:9. |
| `a12-cau-hoi.png` | Anonymous young Vietnamese militia fighter seen from behind, in dark cotton clothes and scarf, behind low street barricade in lower center, distant 1940s light tank silhouette in smoke. A vague period pole-charge silhouette held at his side. Top 40 percent empty low-detail dark-blue smoke for question. Wide 16:9. |
