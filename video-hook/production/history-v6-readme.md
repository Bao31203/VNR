# Video lịch sử V6 — gõ chữ rõ hơn, kết thúc tiếng súng trước Lời kêu gọi

Sửa từ V5 theo ba yêu cầu liên tiếp của người dùng. Giữ riêng V6, không ghi đè các bản cũ.

## Thay đổi

- Tăng toàn bộ tiếng gõ phím/phím cách tổng cộng **13 dB so với V5** (thêm **3 dB so với V6 đã giao**); cập nhật trực tiếp các MP4 V6 theo yêu cầu, không tạo V7. Không thay mẫu thu thật, cao độ ngẫu nhiên, nhịp hay mốc ký tự. Master vẫn dùng gain cố định −4,19 dB của V5, nên không tự hạ lại tiếng gõ hoặc tăng âm lượng toàn video.
- Người dùng xác nhận chỉ dời **các loạt súng**, không dời đại bác. Ba loạt ở C7 được dời muộn **5 giây**, giảm thêm **3 dB** so với V5; dùng đầy đủ file gốc và giữ onset chính xác.
- Kéo dài C7 thêm đúng **5 giây / 150 khung hình** để tiếng súng kết thúc hẳn trước khi chuyển sang C8. Lời dẫn không kéo giãn hay phát chậm; chỉ thêm khoảng im tiếng lời giữa hai cảnh.
- Tiếng súng cuối kết thúc ở **76,2757 giây**, chuyển đỏ bắt đầu **76,6 giây**, cảnh Lời kêu gọi bắt đầu **77 giây**. Không có súng dưới bản thu của Bác.
- Giữ nguyên các yêu cầu trước: tắt chuông/gạt dòng, tối hậu thư chỉ có SFX gõ chữ, không tiếng nổ màn kết, ảnh bản thảo, chữ quân số C9 và rút 5 giây chờ ở C2.

## Đầu ra và kiểm tra

Đầu ra `out/history-1946-v6/`: `hook.mp4` Full HD, `hook-720p.mp4`, clip cảnh Pháo đài Láng `fort-review.mp4`. Thời lượng **137,2 giây**, **4.116 khung hình / 30 fps**.

`qa/recording-alignment.json` xác nhận: mỗi sự kiện gõ tăng đúng 13 dB so với V5 và 3 dB so với V6 cũ; sai khác của bản phối chỉ là phần tiếng gõ tăng thêm; mỗi loạt súng muộn 5 giây và giảm đúng 3 dB; đại bác và nguồn SFX không đổi; tiếng súng hết trước cả chuyển cảnh; toàn bộ mẫu lời dẫn trước/sau phần chèn 5 giây trùng V5, không đổi tốc độ; chữ C9 vẫn khớp lời đọc. `qa/verification.json` lưu kết quả kiểm tra MP4 cuối, thời lượng, số khung hình, độ lớn và đỉnh âm thanh. Dữ liệu đối chiếu trước khi tăng thêm 3 dB lưu ở `qa/typing-plus3/`.

## Dựng lại

Từ `F:/VNR`, chạy `render-history-v6.ts --prepare`, `create-history-v6-soundtrack.py`, `render-history-v6.ts --render-fort`, `--assemble-fort`, `--finalize`, `--verify`, rồi `verify-history-v6-audio.py`. Các script dùng Node/tsx và Python tại `F:/AI-auto-generate-video/`. Bộ dựng chỉ dựng lại C7 kéo dài và một giây đầu C8 bằng template lịch sử tự thiết kế `frame-vnr-history-v4`; các phần còn lại lấy hình từ V5, căn theo đúng khung hình.

Để chỉ cập nhật mức gõ trên V6 có sẵn: chạy `--update-typing-metadata`, `create-history-v6-soundtrack.py`, `--remux-existing`, `--verify` và `verify-history-v6-audio.py`. Chế độ remux thay âm thanh trực tiếp trong Full HD, 720p và clip xem thử, không mã hóa lại luồng hình; kiểm tra file ứng viên trước khi thay file đang dùng.
