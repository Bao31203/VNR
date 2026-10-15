# Kế hoạch thiết kế và sản xuất video hook (bản mới)

**Mục tiêu:** làm một video mở đầu khiến cả lớp im lặng chú ý, rồi kết bằng câu hỏi **"Lấy gì để thắng?"** để dẫn vào phần thuyết trình về đường lối kháng chiến.

**Thông số video:**
- Khung hình 16:9, 1920×1080, 30 khung hình/giây.
- Có hai bản: **rút gọn khoảng 1 phút 25** và **đầy đủ khoảng 2 phút 05**.
- Phong cách: tranh vẽ minh họa, máy quay chuyển động chậm, chữ chạy kiểu đồ họa, lời dẫn tiếng Việt, nhạc phim tài liệu.

**Các file liên quan:**
- `kich-ban-loi-dan.md`: lời dẫn theo cảnh C1–C11.
- `thiet-ke-anh-minh-hoa.md`: thiết kế ảnh A01–A13, kèm prompt cho AI vẽ.
- `tu-lieu-lich-su.md`: nguồn của mọi chi tiết lịch sử.

---

## Tổng quan quy trình

| Bước | Việc | Người làm | Đầu ra | Thời gian ước tính |
|---|---|---|---|---|
| **0** | Chốt các quyết định | Bạn (mình đã có đề xuất sẵn) | Danh sách quyết định | 10 phút |
| **1** | Dựng **animatic**: video nháp dùng ảnh tạm, để chốt nhịp | Mình | `out/animatic.mp4` | 1 lượt làm việc |
| **2** | Tạo ảnh minh họa bằng AI | Bạn | `assets/A01…A13` | 2–4 giờ |
| **3** | Thu lời dẫn | Bạn hoặc thành viên nhóm | `audio/vo/VO-C01…C11` | 30–60 phút |
| **4** | Chọn nhạc nền và hiệu ứng âm thanh | Bạn chọn nhạc, mình làm hiệu ứng | `audio/music/`, `audio/sfx/` | 30 phút |
| **5** | Nâng cấp bộ dựng, dựng **bản v1** | Mình | `out/hook.mp4` | 1–2 lượt làm việc |
| **6** | Duyệt và sửa (tối đa 2 vòng) | Bạn góp ý, mình sửa | `hook-v2.mp4`, `hook-v3.mp4` | 30 phút mỗi vòng |
| **7** | Xuất bản cuối, thử trên máy chiếu | Bạn | File trình chiếu và bản dự phòng | 15 phút |

```
Bước 0 ─► Bước 1 (animatic) ─┬─► Bước 2 (ảnh)      ─┐
                             ├─► Bước 3 (lời dẫn)  ─┼─► Bước 5 (dựng v1) ─► Bước 6 (duyệt) ─► Bước 7 (trình chiếu)
                             └─► Bước 4 (nhạc)     ─┘
```

Sau khi có animatic, các bước 2, 3 và 4 **làm song song được**. Thiếu ảnh nào, bộ dựng tạm dùng hình vẽ bằng code của bản nháp cho ảnh đó, nên lúc nào cũng xuất được video để xem.

---

## Bước 0. Chốt các quyết định

| # | Quyết định | Lựa chọn | Đề xuất của mình |
|---|---|---|---|
| 1 | Độ dài | Rút gọn (~1:25) hoặc đầy đủ (~2:05) | **Rút gọn** nếu cả bài thuyết trình dưới 15 phút. Đầy đủ nếu dài hơn. |
| 2 | Giọng dẫn | Người trong nhóm tự thu, hoặc giọng AI | **Tự thu** nếu nhóm có người giọng trầm, đọc chắc, vì có cảm xúc hơn AI. Nếu không có thì dùng AI. |
| 3 | Giọng đọc Lời kêu gọi | Giọng thứ hai, hoặc chính người dẫn đọc chậm lại | **Giọng thứ hai** (nam, trang nghiêm). Không giả giọng Bác. |
| 4 | Câu trích Lời kêu gọi | Theo giáo trình, hoặc theo bản phổ biến | **Theo giáo trình** nếu giảng viên chấm sát giáo trình. |
| 5 | Ảnh A12 (quyết tử quân) | AI vẽ, hoặc ảnh tư liệu thật của TTXVN | **AI vẽ**, và đưa ảnh tư liệu thật vào slide ngay sau video. |
| 6 | Phụ đề lời dẫn | Không có, hoặc có | **Không có** phụ đề toàn bộ vì màn hình đã nhiều chữ. Mình vẫn xuất thêm một **bản có phụ đề** để dự phòng khi loa kém. |
| 7 | Nhạc | Tự chọn, hoặc để mình đề xuất | Lấy từ nguồn **miễn phí bản quyền** (xem bước 4). |

---

## Bước 1. Animatic: chốt nhịp trước khi vẽ ảnh

**Mục đích:** biết chính xác mỗi cảnh dài bao nhiêu giây và chữ hiện lúc nào, để khỏi vẽ ảnh rồi lại phải cắt.

**Mình làm:**
1. Dựng toàn bộ 11 cảnh theo **Phụ lục A**. Chỗ nào chưa có ảnh thì đặt một khung xám ghi mã ảnh và mô tả ngắn (ví dụ "A07 · Chiến lũy đêm"), kèm chuyển động máy quay thật.
2. Đưa đủ toàn bộ chữ và đồ họa (đường thời gian, tờ lịch, tối hậu thư, đồng hồ đếm ngược, trích dẫn, số liệu, tên đề tài) đúng kiểu dáng của bản cuối.
3. Cho **lời dẫn hiện thành phụ đề tạm** đúng thời điểm dự kiến, để bạn đọc to theo mà thử nhịp.
4. Đặt hiệu ứng âm thanh tạm và đổi mốc đồng hồ thành **20:03**.
5. Xuất hai file: `out/animatic-rut-gon.mp4` và `out/animatic-day-du.mp4`.

**Bạn làm:** xem animatic và đọc to lời dẫn theo phụ đề. Ghi chú theo mốc thời gian, ví dụ "0:42 chữ ra nhanh quá", "C5 thừa 2 giây".

**Xong bước này khi:** độ dài từng cảnh đã chốt, sai lệch không quá 1 giây.

---

## Bước 2. Tạo ảnh minh họa

Làm theo `thiet-ke-anh-minh-hoa.md`.

### 2.1. Thứ tự làm

1. **A02** (phố cổ) là ảnh chuẩn phong cách. Phải làm cho thật ưng rồi mới làm tiếp.
2. Các ảnh "rất cao": **A12, A09, A07**.
3. Các ảnh "cao": **A03, A04, A06, A10, A11a, A11b, A01**.
4. Các ảnh còn lại: **A08, A13**, rồi A05 (tùy chọn), rồi S1–S4 cho slide.

### 2.2. Quy trình cho mỗi ảnh

1. Dán **prompt** của ảnh, rồi **đuôi STYLE**, rồi **NEGATIVE** (nếu công cụ có ô đó). Gắn A02 làm ảnh tham chiếu phong cách.
2. Tạo 4 biến thể và chọn 1.
3. Kiểm tra theo **danh sách 2.3** bên dưới. Lỗi nhỏ thì sửa vùng (inpaint); lỗi lớn thì tạo lại.
4. Phóng to (upscale) lên tối thiểu **2560×1440**.
5. Với A02 và A07: tách lớp nếu làm được (không bắt buộc).
6. Đặt tên theo mã, ví dụ `A07-chien-luy.png`.
7. Tải lên GitHub vào thư mục `video-hook/assets/`, giống cách bạn đã tải giáo trình: mở thư mục trên web, bấm **Add file**, chọn **Upload files**, rồi chọn nhánh `claude/gifted-dirac-di6lc4`.

### 2.3. Kiểm tra từng ảnh

- [ ] Đúng thời kỳ: không có đồ vật hiện đại; xe, máy bay, tàu chiến đúng loại; cờ đúng (Pháp ba màu, Việt Nam cờ đỏ sao vàng)
- [ ] Không có chữ đọc được hoặc chữ bị lỗi
- [ ] Không vẽ rõ mặt nhân vật lịch sử có thật
- [ ] Không có cảnh máu me
- [ ] Chừa đúng vùng trống cho chữ (có ghi trong thiết kế từng ảnh)
- [ ] Cùng tông màu và nét vẽ với A02
- [ ] Tay, ngón tay, vũ khí không bị méo; bom ba càng có cán dài và ba ngạnh
- [ ] Đủ độ phân giải

### 2.4. Lỗi AI hay gặp và cách xử lý

| Lỗi | Cách xử lý |
|---|---|
| Bom ba càng bị vẽ sai | Dùng inpaint vẽ lại riêng vùng đó. Hoặc đặt cho xa, ngược sáng, ít chi tiết. |
| Cờ hoặc phù hiệu sai | Inpaint, hoặc che bằng khói, tối màu. |
| Có chữ lỗi trên giấy, biển hiệu | Làm mờ hoặc xóa bằng Canva, Photoshop. |
| Kiến trúc giống Trung Quốc | Thêm vào prompt: `French colonial Hanoi, Vietnamese tube houses, no pagoda`. |
| Mỗi ảnh một phong cách | Luôn gắn A02 làm tham chiếu, giữ nguyên đuôi STYLE. |

---

## Bước 3. Thu lời dẫn

### 3.1. Quy cách file

- **Mỗi cảnh một file**: `VO-C01.wav`, `VO-C02.wav`… `VO-C11.wav`. Lời kêu gọi đặt tên là `VO-C08.wav`.
- Định dạng WAV (hoặc M4A, MP3 320 kbps), mono, 44,1 hoặc 48 kHz.
- Đầu và cuối mỗi file để khoảng **0,5 giây im lặng**.
- Mỗi cảnh thu 2–3 lần và giữ lần tốt nhất. **Không cần chỉnh âm lượng**, mình sẽ chuẩn hóa.
- Thu cả các câu có dấu ✂︎, để sau này đổi qua lại giữa bản rút gọn và đầy đủ mà không phải thu lại.
- Tải lên thư mục `video-hook/audio/vo/`.

### 3.2. Cách đọc

- **Nhịp:** đọc theo animatic. Nếu dài hơn khung, cứ đọc tự nhiên; ở bước 5, độ dài cảnh sẽ tự giãn theo file thu.
- **Phát âm:**
  - "1946" đọc là "một nghìn chín trăm bốn mươi sáu".
  - "20 giờ 3 phút" đọc là "hai mươi giờ ba phút".
  - "Yên Ninh", "Hàng Bún", "Vạn Phúc" cần đọc rõ thanh điệu.
- **Cảm xúc từng đoạn:**
  - C1–C4: chậm, trầm, như kể chuyện.
  - C6: thì thầm, căng.
  - C7: dứt khoát.
  - C8: trang nghiêm, có lực ở chữ "Không!".
  - C10: chậm lại, ngừng thật lâu trước câu "lấy gì để thắng?".
- **Nếu dùng giọng AI:** chọn giọng nam miền Bắc, tốc độ khoảng 0,85–0,9. Nghe lại kỹ các địa danh vì AI hay đọc sai.

---

## Bước 4. Nhạc nền và hiệu ứng âm thanh

### 4.1. Nhạc

Cần **1 bản nhạc dài khoảng 2 phút có cao trào**, hoặc **2 bản** ghép lại: một bản căng thẳng cho C1–C6, một bản hùng tráng, bi tráng cho C8–C11.
- **Nguồn miễn phí bản quyền:** YouTube Audio Library, Pixabay Music.
- **Từ khóa tìm:** `cinematic documentary tension`, `epic orchestral sad`, `war drums dark`.
- Ghi lại tên bài và tác giả để ghi nguồn ở slide cuối.
- Tải lên thư mục `video-hook/audio/music/`.

### 4.2. Hiệu ứng âm thanh

Mình đã có bộ tự tạo, gồm tích tắc, pháo, tim đập, trống, và **bộ tiếng máy chữ** (6 tiếng phím, phím cách, gạt dòng, chuông) ở `audio/sfx/may-chu/`, kèm công cụ `audio/may_chu.py` để tạo tiếng gõ khớp từng dòng chữ. Nếu muốn thật hơn, bạn có thể lấy thêm từ Pixabay Sound Effects:
- tiếng đồng hồ quả lắc
- tiếng pháo hạm từ xa
- tiếng đại bác
- tiếng cầu dao điện
- tiếng xích xe tăng
- **tiếng máy chữ (bắt buộc):** 4–6 mẫu tiếng gõ phím, tiếng gạt dòng, tiếng chuông "ting". Mọi dòng chữ trong video đều hiện ra như đánh máy, kèm tiếng gõ
- tiếng dế kêu đêm
- tiếng tim đập
- tiếng trống lớn

### 4.3. Bảng âm thanh theo thời gian (bản đầy đủ)

| Thời điểm | Âm thanh |
|---|---|
| 0:00 | Tích tắc chậm, mỗi giây một tiếng |
| 0:05 | Nhạc 1 vào dần trong 2 giây, đặt thấp |
| 0:20, 0:23, 0:27 | Pháo hạm vọng từ xa (cùng lúc với chớp sáng trên hình) |
| 0:32 | Tiếng xích xe bọc thép từ xa |
| 0:40–0:45 | Tiếng máy chữ khi gõ các dòng tối hậu thư |
| 0:46 | Nhạc lắng xuống, tiếng dế đêm |
| 1:02–1:07 | Tích tắc nhanh dần, nhạc **tắt hẳn ở 1:06** |
| 1:07,0 | Tiếng "tách" của cầu dao, rồi **im lặng 1 giây** |
| 1:08,0 | **Đại bác nổ** và vang, màn hình rung |
| 1:15 | Nhạc 2 hùng tráng vào |
| 1:37 | Tiếng tim đập |
| 1:57 | Tim đập dừng, im lặng 0,5 giây, rồi câu hỏi |
| 1:59 | Tiếng trống lớn, nhạc ngân rồi tắt dần |

---

## Bước 5. Nâng cấp bộ dựng và dựng bản v1 (mình làm)

### 5.1. Nâng cấp bộ dựng

1. **File cấu hình `scenes.json`:** mô tả từng cảnh (ảnh, chuyển động máy quay, lớp chữ, file lời dẫn, hiệu ứng âm thanh và thời điểm). Sau này chỉnh nhịp chỉ cần sửa file này, không phải sửa code.
2. **Thời lượng tự khớp lời dẫn:** mỗi cảnh dài bằng file thu cộng phần đệm (tối thiểu bằng độ dài đã chốt ở animatic). Thu nhanh hay chậm hơn dự kiến video vẫn khớp.
3. **Lớp ảnh:**
   - Zoom và lia chậm (hiệu ứng Ken Burns).
   - Có chiều sâu (parallax) nếu ảnh được tách lớp.
   - Chớp sáng và rung khi có tiếng nổ.
   - Thiếu ảnh nào thì tự dùng hình vẽ bằng code của bản nháp cho ảnh đó.
4. **Lớp chữ và đồ họa:** giữ các hiệu ứng đã có (chữ đánh máy, đường thời gian, tờ lịch lật, đồng hồ), thêm số liệu đếm tăng dần ở C9. Toàn bộ theo **Phụ lục B**.
5. **Trộn âm thanh bằng ffmpeg:**
   - Chuẩn hóa âm lượng lời dẫn.
   - Nhạc tự hạ thấp khi có lời (ducking).
   - Ghép hiệu ứng âm thanh đúng mốc.
   - Giới hạn đỉnh tiếng để không bị rè trên loa lớp.
6. **Các file xuất ra:**
   - `hook.mp4` (1080p, bản trình chiếu)
   - `hook-720p.mp4` (bản xem trước, nhẹ)
   - `hook.srt` (phụ đề rời)
   - `hook-phude.mp4` (phụ đề in thẳng lên hình, bản dự phòng)

### 5.2. Dựng bản v1

1. Dựng bản v1 với những ảnh và lời dẫn đã có.
2. Tự kiểm tra trước khi gửi:
   - Xem ảnh chụp từng cảnh.
   - Đo âm lượng tổng.
   - Rà lại các mốc thời gian.
   - Đối chiếu mọi chữ trên màn hình với `tu-lieu-lich-su.md`.
3. Gửi cho bạn bản 720p xem trước. Bản 1080p được đẩy lên nhánh git.

---

## Bước 6. Duyệt và sửa

Mỗi vòng duyệt, xem video một lần không dừng để cảm nhận nhịp, rồi xem lại từng cảnh và ghi chú theo mốc thời gian.

**Danh sách kiểm tra:**
- [ ] **Nội dung:** mọi ngày tháng, số liệu, tên địa danh đúng với giáo trình và tư liệu
- [ ] **Nhịp:** không cảnh nào bị lê thê; khoảnh khắc 20 giờ 3 phút có đủ "sốc"
- [ ] **Chữ:** đọc kịp trước khi biến mất; đọc được từ **cuối lớp** (thử chiếu lên TV hoặc máy chiếu, đứng cách khoảng 5 m)
- [ ] **Âm thanh:** nghe rõ lời, nhạc không lấn lời, tiếng nổ không rè loa
- [ ] **Phát âm:** không đọc sai địa danh
- [ ] **Cảm xúc:** đến câu "Lấy gì để thắng?" người xem có muốn nghe tiếp không?

Tối đa **2 vòng sửa** (ra v2, v3) để không kéo dài.

---

## Bước 7. Xuất bản cuối và trình chiếu

1. **Lưu file ở 3 nơi:** laptop thuyết trình, USB, Google Drive. **Không** phụ thuộc mạng hay YouTube khi chiếu.
2. **Cách mở:**
   - **Cách 1:** chèn vào PowerPoint bằng *Insert*, *Video*, *This Device*. Trong tab *Playback*, chọn *Start: Automatically* và *Play Full Screen*.
   - **Cách 2:** mở bằng VLC ở chế độ toàn màn hình.
3. **Thử trước giờ thuyết trình ít nhất 15 phút:** kiểm tra âm thanh ra loa lớp, âm lượng, máy chiếu đúng tỉ lệ 16:9.
4. **Câu nối ngay sau video** (người thuyết trình nói):
   > "Câu trả lời nằm trong 12 chữ: *Toàn dân, toàn diện, lâu dài, dựa vào sức mình là chính.* Hôm nay nhóm mình sẽ cho các bạn thấy 12 chữ ấy đã biến thành chiến thắng Việt Bắc 1947 và Biên giới 1950 như thế nào."
5. **Phương án dự phòng nếu video không chạy:** chuẩn bị 3 slide ảnh tĩnh A07, A09, A12. Người thuyết trình đọc trực tiếp lời dẫn bản rút gọn trên nền 3 slide đó.

---

## Phụ lục A. Thiết kế chi tiết từng cảnh

> **Thông số chi tiết và mới nhất** nằm ở `style/thiet-ke-style-video.md`, `style/video-style.json` và `style/wireframes/`. Ở đó gồm cách chữ hiện ra như đánh máy kèm tiếng gõ phím, vị trí chữ, chuyển cảnh, màn đen và âm thanh. Nếu bảng dưới đây khác với các file đó, **theo thư mục `style/`**.

Thời gian ghi theo dạng **bản đầy đủ / bản rút gọn**. Mã ảnh xem trong `thiet-ke-anh-minh-hoa.md`, lời dẫn xem trong `kich-ban-loi-dan.md`.

| Cảnh | Thời gian | Hình và chuyển động máy quay | Chữ và đồ họa | Chuyển cảnh vào | Âm thanh |
|---|---|---|---|---|---|
| **C1** Mở đầu | 0:00–0:05 / 0:00–0:05 | A01. Zoom từ 100% lên 108% về phía mặt đồng hồ | *Hà Nội · Tháng 12 năm 1946*, chữ đánh máy, nửa trái màn hình | Hiện dần từ màn hình đen (0,8 giây) | Tích tắc. Lời dẫn vào ở giây 1,5 |
| **C2** Hòa bình mong manh | 0:05–0:20 / 0:05–0:13 | A02. Lia sang phải 10%, có chiều sâu nếu ảnh tách lớp | Đường thời gian ở 1/3 trên: *06.3.1946 Hiệp định Sơ bộ* (hiện ở 0:07), *14.9.1946 Tạm ước* (0:10) | Hòa tan 1 giây | Nhạc 1 vào dần |
| **C3** Hải Phòng | 0:20–0:32 / 0:13–0:21 | A03. Zoom từ 100% lên 112% về phía tàu chiến. Chớp sáng 3 lần | Mốc *11.1946* đỏ nhấp nháy. Chú thích *23.11.1946 · Pháp nã pháo vào Hải Phòng* | **Cắt thẳng**, đúng tiếng pháo đầu tiên | Pháo hạm từ xa ×3 |
| **C4** Hà Nội bị uy hiếp | 0:32–0:46 / 0:21–0:30 | A04 lia trái theo hướng xe chạy (7 giây). Sau đó chuyển sang đồ họa tờ lịch và tối hậu thư | *17.12 · Thảm sát phố Yên Ninh, Hàng Bún*. Lịch lật từ 17 sang 18. Tờ *TỐI HẬU THƯ* có 3 dòng đánh máy, cuối cùng là *Hạn chót: sáng 20.12.1946* | Hòa tan | Tiếng xích xe, tiếng máy chữ |
| **C5** Vạn Phúc | 0:46–0:55 / 0:30–0:39 | A06. Máy tiến chậm về khung cửa sáng, từ 100% lên 110% | Góc dưới trái: *18.12.1946 · Làng Vạn Phúc, Hà Đông*. Cuối cảnh hiện chữ lớn **PHÁT ĐỘNG TOÀN QUỐC KHÁNG CHIẾN** | Hòa tan chậm qua màn đen | Nhạc lắng, tiếng dế |
| **C6** Chờ hiệu lệnh | 0:55–1:07 / 0:39–0:47 | A07 lia nhẹ (6 giây), rồi A08 zoom vào cầu dao (6 giây) | *Tối 19.12.1946*. 5 giây cuối: đồng hồ số **20:02:55 → 20:03:00** ở giữa phía trên | Cắt thẳng | Tích tắc nhanh dần, nhạc tắt ở giây cuối |
| **C7** 20 giờ 3 phút | 1:07–1:15 / 0:47–0:55 | Đèn đường tắt, màn hình đen 1 giây, chớp trắng, rồi A09. Rung mạnh 0,8 giây, sau đó zoom ra từ 115% về 100% | **20 GIỜ 3 PHÚT · 19.12.1946**. Dòng nhỏ: *Pháo đài Láng nổ súng — Toàn quốc kháng chiến bùng nổ* | Tắt đèn chuyển sang đen | Tiếng "tách", im lặng, đại bác. Lời dẫn vào sau tiếng nổ |
| **C8** Lời kêu gọi | 1:15–1:37 / 0:55–1:05 | Nửa trái nền đỏ có ngôi sao mờ xoay chậm, nửa phải là A10 zoom chậm | Trích dẫn hiện từng dòng **khớp với giọng đọc**. Dòng cuối màu vàng, chữ lớn hơn. Ghi nguồn ở cuối | Hòa tan qua màu đỏ | Nhạc 2 vào, giọng thứ hai |
| **C9** Tương quan lực lượng | 1:37–1:50 / 1:05–1:10 | A11a và A11b trượt vào từ hai bên, ở giữa là vạch đỏ | Số liệu đếm tăng dần. Bên trái: *6.000+ quân · xe tăng · xe bọc thép · máy bay*. Bên phải: *2.500 vệ quốc quân · 8.000 tự vệ · ~2.000 khẩu súng* | Trượt ngang | Tiếng tim đập. Bản rút gọn không có lời |
| **C10** Câu hỏi | 1:50–1:59 / 1:10–1:19 | A12. Zoom rất chậm từ 100% lên 106%, nền tối dần | Hiện lần lượt *Thiếu vũ khí.* / *Kinh tế kiệt quệ.* / *Không một nước nào công nhận.* rồi mờ đi. Sau đó chữ lớn màu vàng **Lấy gì để thắng?** | Tối dần | Tim đập dừng, im lặng 0,5 giây, rồi câu hỏi |
| **C11** Tên đề tài | 1:59–2:05 / 1:19–1:24 | A13 gần như đứng yên | Vạch đỏ, rồi **ĐƯỜNG LỐI KHÁNG CHIẾN TOÀN QUỐC** / *và quá trình tổ chức thực hiện* / **1946 – 1950** | Hòa tan | Tiếng trống lớn, nhạc ngân rồi tắt |

---

## Phụ lục B. Quy chuẩn thiết kế

| Hạng mục | Quy chuẩn |
|---|---|
| Khung hình | 1920×1080, 30 khung hình/giây. Chữ cách mép tối thiểu 96 px |
| Phông chữ | **Tiêu đề:** Liberation Serif Bold. **Chữ thường:** Inter. **Ngày tháng, đồng hồ, chữ đánh máy:** DejaVu Sans Mono. Nếu muốn đẹp hơn, bạn có thể gửi file `.ttf` của Be Vietnam Pro, Noto Serif hoặc Lora (đều có dấu tiếng Việt) |
| Cỡ chữ | Chữ thường tối thiểu **40 px** để cuối lớp đọc được. Chú thích 44–50 px. Tiêu đề 84–140 px |
| Màu | Xanh than `#0D1626`, vàng `#F2C14E`, đỏ `#C8302A`, kem `#EFE6D2`, nâu `#3A2A17` |
| Chuyển động chữ | Hiện ra trong 0,4–0,8 giây, nhanh lúc đầu chậm dần lúc cuối. Mỗi dòng chữ ở trên màn hình tối thiểu bằng thời gian đọc hai lần |
| Chuyển động máy quay | Phóng to tối đa khoảng 1,5% mỗi giây. Mỗi cảnh chỉ một kiểu chuyển động máy quay |
| Chuyển cảnh | Chủ yếu hòa tan 0,6–1 giây. **Cắt thẳng** chỉ dùng ở các khoảnh khắc có tiếng nổ (C3, C7) để tạo cú sốc |
| Hiệu ứng nền | Nhiễu phim nhẹ, viền tối quanh khung hình. Dải tối ở đáy màn hình khi có chú thích |
| Âm thanh | Lời dẫn khoảng −16 LUFS. Khi có lời, nhạc thấp hơn lời khoảng 12 dB. Đỉnh tiếng không vượt −1 dBTP |

---

## Phụ lục C. Thư mục và tên file

```
video-hook/
├── assets/                 ← ảnh (bạn tải lên)
│   ├── A01-dong-ho.png
│   ├── A02-pho-ha-noi.png   (+ A02-layer1.png, A02-layer2.png… nếu tách lớp)
│   └── … A13-binh-minh.png
├── audio/
│   ├── vo/                 ← lời dẫn (bạn tải lên): VO-C01.wav … VO-C11.wav
│   ├── music/              ← nhạc nền
│   └── sfx/                ← hiệu ứng âm thanh
├── scenes.json             ← cấu hình cảnh (mình tạo ở bước 5)
├── index.html, render.cjs  ← bộ dựng
└── out/                    ← video xuất ra
```

---

## Phụ lục D. Rủi ro và phương án dự phòng

| Rủi ro | Phương án |
|---|---|
| AI vẽ sai chi tiết lịch sử | Kiểm tra theo danh sách 2.3. Dùng inpaint, hoặc che bằng khói, bóng tối |
| Thiếu ảnh khi gần hạn | Bộ dựng tự dùng hình vẽ bằng code của bản nháp. Ưu tiên làm xong 4 ảnh "rất cao" |
| Giọng AI đọc sai địa danh | Viết lại theo cách đọc (ví dụ thêm dấu phẩy để ngắt) hoặc thu riêng câu đó bằng giọng thật |
| Video dài quá thời gian cho phép | Chuyển sang bản rút gọn. Lời dẫn đã thu đủ nên không cần thu lại |
| Loa lớp kém, lời dẫn khó nghe | Dùng bản `hook-phude.mp4` |
| Máy chiếu hoặc laptop không phát được video | Dùng 3 slide ảnh tĩnh và đọc trực tiếp (xem bước 7) |
| Vấn đề bản quyền nhạc, ảnh | Chỉ dùng nguồn miễn phí bản quyền. Ảnh tư liệu TTXVN phải ghi nguồn ở slide cuối |

---

## Phụ lục E. Danh sách kiểm tra tổng

- [ ] Bước 0: đã chốt 7 quyết định
- [ ] Bước 1: đã duyệt animatic và chốt thời lượng từng cảnh
- [ ] Bước 2: A02 đã ưng ý → các ảnh "rất cao" → toàn bộ A01–A13 đã tải lên `assets/`
- [ ] Bước 3: VO-C01 đến VO-C11 đã tải lên `audio/vo/`
- [ ] Bước 4: đã có nhạc trong `audio/music/` và đã ghi tên bài, tác giả
- [ ] Bước 5: đã có bản v1
- [ ] Bước 6: đã có v2, v3 và qua toàn bộ danh sách kiểm tra
- [ ] Bước 7: file đã lưu ở 3 nơi, đã thử trên máy chiếu, đã chuẩn bị slide dự phòng
