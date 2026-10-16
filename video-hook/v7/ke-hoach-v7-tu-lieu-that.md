# Kế hoạch V7: thay tranh vẽ của V6 bằng ảnh và phim tư liệu thật

**Mục tiêu:** giữ nguyên **toàn bộ âm thanh** của V6 (lời dẫn, tiếng máy chữ, đại bác, súng, nhạc), cùng nhịp, chữ, đồng hồ, đường thời gian và tờ tối hậu thư. Chỉ thay **lớp hình nền đang là tranh vẽ AI** bằng **ảnh tư liệu và phim tư liệu thật**, theo phong cách video tham khảo: đen trắng, ảnh và phim 4:3 đặt giữa khung, chân dung có chú thích tên và năm.

**File đi kèm trong thư mục này:**
- `v6-storyboard.jpg`: V6 cắt mỗi 2 giây, có ghi mốc thời gian.
- `tham-khao-danh-muc-1.jpg`, `tham-khao-danh-muc-2.jpg`: video tham khảo cắt mỗi 2,5 giây, có ghi mốc thời gian.

---

## 1. Hiện trạng

### 1.1. V6 (`video-hook/out/history-1946-v6/hook.mp4`, dài 137,2 s)

Mốc thời gian dưới đây đo từ chính video V6.

| Cảnh | Thời gian trong V6 | Hình nền hiện tại | Loại |
|---|---|---|---|
| C1 Mở đầu | 0,0 – 5,8 | Đồng hồ treo tường (A01) | Tranh AI |
| C2 Hòa bình mong manh | 5,8 – 15,8 | Phố cổ chập tối (A02), có đường thời gian | Tranh AI |
| C3 Hải Phòng | 15,8 – 27,8 | Tàu chiến nã pháo (A03); chớp sáng ở 15,8 / 18,8 / 22,8 | Tranh AI |
| C4 phần A | 27,8 – 34,2 | Xe bọc thép trên phố (A04) | Tranh AI |
| C4 phần B | 34,2 – 41,6 | Tờ lịch và tờ tối hậu thư | **Đồ họa, giữ nguyên** |
| C5 Vạn Phúc | 41,6 – 51,2 | Nhà làng ban đêm (A06) | Tranh AI |
| C6 phần A | 51,2 – 57,2 | Chiến lũy, tự vệ chờ (A07) | Tranh AI |
| C6 phần B | 57,2 – 63,2 | Nhà máy điện và đồng hồ đếm ngược (A08) | Tranh AI |
| C7 20 giờ 3 phút | 63,2 – 77,4 | Đen, sau đó pháo đài Láng khai hỏa (A09) từ 64,2; chuyển sang đỏ ở 76,8 | Tranh AI |
| C8 Lời kêu gọi | 77,4 – 106,8 | Nền đỏ, ngôi sao, **ảnh bản thảo Lời kêu gọi** | **Đã là ảnh thật, giữ nguyên** |
| C9 Tương quan lực lượng | 106,8 – 119,8 | Chia đôi (A11a, A11b) | Tranh AI |
| C10 Câu hỏi | 119,8 – 129,0 | Quyết tử quân (A12) | Tranh AI |
| C11 Tên đề tài | 129,0 – 134,8 (đen ở 134,8 – 137,2) | Mái phố lúc bình minh (A13) | Tranh AI |

### 1.2. Tư liệu thật đã có trong repo

| Mã | File | Kích thước | Nội dung | Lưu ý |
|---|---|---|---|---|
| BT1 | `assets/references/bao-tang-19-12-1946/images/01-hiep-dinh-so-bo.jpg` | 340×480 | Bản tuyên bố (DÉCLARATION) Hiệp định Sơ bộ, chữ ký Sainteny và Hồ Chí Minh | Ảnh nhỏ |
| BT2 | `.../02-tau-chien-hai-phong.jpg` | 480×316 | Tàu chiến Pháp ở Hải Phòng | **Bài bảo tàng ghi ảnh chụp ngày 5-3-1946**, không phải ngày 23-11. Trùng với `chinh-sua-video/tau-chien-phap-hai-phong.jpg` |
| BT3 | `.../03-nha-van-phuc.jpg` | 480×360 | Ngôi nhà ở Vạn Phúc | Cần ghi chú thích đúng theo bảo tàng |
| BT4 | `.../04-bac-bo-phu.jpg` | 480×327 | Bắc Bộ phủ | **Ảnh màu chụp ngày nay**, không phải ảnh năm 1946 |
| BT5 | `.../05-ban-thao-loi-keu-goi.jpg` | 480×373 | Bản viết tay Lời kêu gọi | V6 đã dùng ảnh bản thảo này |
| VT | `assets/references/chinh-sua-video/video-tham-khao.mp4` | 1280×720, 214 s, không có tiếng | Phim tài liệu: người dẫn ngồi bàn, xen phim thời sự đen trắng (nhiều đoạn có logo **British Pathé**) và ảnh chân dung | Xem danh mục ở mục 3 |

### 1.3. Các vấn đề phải xử lý trước

1. **Repo không có mã nguồn của V6.** Chỉ có video thành phẩm. Không có trang dựng, không có các ảnh A01–A13, không có file giọng đọc gốc. Xem cách xử lý ở mục 5.
2. **Môi trường của mình không tải được ảnh hay phim từ ngoài vào.** Đã thử và bị chặn với: baotanglichsu.vn, nhandan.vn, TTXVN (vnanet.vn), qdnd.vn, Bảo tàng Hồ Chí Minh, Wikimedia, British Pathé, ECPAD. Việc **tìm và tải tư liệu** (mục 4) phải do bạn làm, hoặc do agent bên máy kia (agent đó đã tải được từ trang Bảo tàng Lịch sử).
3. **Ảnh bảo tàng rất nhỏ** (340–480 px), không thể phóng toàn màn hình 1920×1080. Cách trình bày xem mục 2.3.
4. **Phim trong video tham khảo** là sản phẩm của người khác, phần lớn lấy từ British Pathé và có logo. Chỉ nên dùng cho buổi thuyết trình trên lớp, ghi nguồn đầy đủ, **không xóa logo**. Nếu muốn đăng công khai thì phải tải bản gốc từ British Pathé và xem điều khoản.

---

## 2. Định hướng hình ảnh V7

### 2.1. Nguyên tắc

1. **Thật thay cho vẽ.** Mỗi cảnh dùng ảnh hoặc phim tư liệu thật của đúng thời kỳ. Cảnh nào không tìm được tư liệu thì **dùng nền tối chỉ có chữ**, không quay lại dùng tranh AI. Trộn tranh vẽ với ảnh thật sẽ làm mất độ tin cậy.
2. **Giữ nguyên lớp chữ và đồ họa của V6:** chữ đánh máy, đường thời gian, tờ lịch và tối hậu thư, đồng hồ 20:02:55, khối chữ "20 GIỜ 3 PHÚT", trích dẫn, số liệu, câu hỏi, tên đề tài. Vị trí, cỡ chữ và mốc giữ như V6.
3. **Giữ nguyên âm thanh V6**, không cắt, không dịch. Thời lượng từng cảnh giữ như mục 1.1.
4. **Chú thích phải đúng sự thật của tấm ảnh hay đoạn phim.** Ghi đúng ngày và nơi chụp thật, kể cả khi khác sự kiện lời dẫn đang kể. Ví dụ ảnh BT2 phải ghi "Tàu chiến Pháp ở cảng Hải Phòng, 3-1946". Đoạn phim nào chưa rõ quay ở đâu thì **không ghi địa danh**, chỉ ghi nguồn.

### 2.2. Phong cách (theo video tham khảo)

- **Đen trắng** cho mọi ảnh và phim tư liệu. Không tô màu.
- Chỉnh tông đồng bộ: tương phản vừa, ngả nâu nhẹ khoảng 10%, cùng lớp nhiễu phim và viền tối như V6.
- **Phim 4:3** đặt giữa khung 16:9, hai bên là **viền đen** như video tham khảo. Không kéo giãn, không cắt bớt cho kín khung.
- **Ảnh chân dung** (Hồ Chí Minh, Sainteny...) đặt lệch một bên. Phía còn lại là nền đen, có **tên và năm sinh, năm mất**, chữ trắng nhỏ căn giữa, giống video tham khảo ở 00:27 và 01:05.
- **Dòng nguồn** chữ nhỏ ở góc dưới phải (30 px, màu kem, độ đậm 70%). Ví dụ: `Ảnh: Bảo tàng Lịch sử Quốc gia`, `Phim: British Pathé`.
- **Chuyển động:** ảnh tĩnh zoom và lia chậm như V6 (tối đa 1,5% mỗi giây). Phim chạy tốc độ thật, hoặc chậm còn 0,8 lần nếu đoạn quá ngắn. Không tua nhanh.
- **Chuyển cảnh và màn đen:** giữ đúng như V6. Ở C3 và C7, cắt sang ảnh hoặc phim mới **đúng khung hình chớp sáng và tiếng nổ** (15,8 / 18,8 / 22,8 / 64,2).

### 2.3. Cách xử lý ảnh nhỏ (dưới 1000 px)

Thứ tự ưu tiên:
1. **Tìm bản lớn hơn của cùng tấm ảnh.** Bảo tàng, TTXVN và báo Nhân Dân thường có bản lớn hơn bản trên trang bài viết.
2. **Phóng to bằng AI trên máy bạn**, ví dụ Upscayl (miễn phí) hoặc Real-ESRGAN, lên gấp 4 lần. Trên màn hình chỉ hiển thị tối đa khoảng 1,5 lần kích thước sau khi phóng.
3. **Trình bày kiểu "ảnh in đặt trên bàn"**, giống cách V6 đặt ảnh bản thảo ở C8:
   - Ảnh có viền trắng ngà, cao khoảng 55–65% khung.
   - Phía sau là chính tấm ảnh đó phóng to, làm mờ và tối đi, để lấp khung.
   - Ảnh zoom chậm.
   Cách này **không làm vỡ ảnh** và hợp với ảnh nhỏ.

---

## 3. Phim tư liệu có thể cắt từ video tham khảo

Mốc thời gian tính trong `video-tham-khao.mp4`. Đối chiếu với `tham-khao-danh-muc-1.jpg` và `-2.jpg`.

| Mã | Mốc | Nội dung | Địa điểm | Dùng cho |
|---|---|---|---|---|
| T1 | 00:31,5 – 00:34 | Nhà hát Lớn Hà Nội, có treo ảnh chân dung lớn | **Hà Nội** (nhận ra công trình) | C1 |
| T2 | 01:02 – 01:11 | Ảnh Hồ Chí Minh ngồi cạnh Jean Sainteny | — | C2 (mốc 6-3-1946) |
| T3 | 02:32 – 02:37 | Chiến hạm cập bến, lính Pháp và xe tải đổ bộ | Chưa xác định | C3 |
| T4 | 02:37 – 02:40 | Tuần dương hạm chạy trên biển | — | C3 |
| T5 | 02:40 – 02:44 | Khói nổ trong thành phố (mờ) | Chưa xác định | C3, C7 |
| T6 | 01:52 – 01:57 | Lính đội mũ sắt, khói trên phố (Pathé) | Chưa xác định | C7, C9 trái |
| T7 | 02:44 – 02:49 | Lính đi giữa phố đổ nát, đám cháy (Pathé) | Chưa xác định | C7, C9 trái |
| T8 | 00:12,5 – 00:19 | Phố ngổn ngang gạch vụn, người dọn dẹp | Chưa xác định | C11 |
| T9 | 00:20 – 00:26, 00:34 – 00:39, 01:12 – 01:20 | Phố xá đông người, xe đạp, chợ | **Có thể là Sài Gòn** | Chỉ dùng khi đã xác định được là Hà Nội |

**Không dùng:**
- Người dẫn chương trình (00:00–00:10 và từ 03:10 trở đi).
- Ảnh Bảo Đại; phù điêu rồng (00:45).
- Chợ có tháp đồng hồ ở 02:25, trông giống chợ Bến Thành (Sài Gòn).
- Đoạn đánh nhau trong rừng (02:55–03:08), thuộc giai đoạn sau 1946.
- Ảnh d'Argenlieu và Valluy (02:00–02:13). Lời dẫn V6 không nhắc tới hai người này; chỉ dùng nếu sau này thêm lời.

Khi cắt, phải **tắt tiếng** (file vốn không có tiếng) và chỉ lấy phần hình 4:3 bên trong viền đen. **Không xóa logo Pathé.**

---

## 4. Bảng thay thế từng cảnh

**Cách đọc cột "Thay bằng":**
- **BT** là ảnh bảo tàng đã có trong repo.
- **T** là phim cắt từ video tham khảo (mục 3).
- **P** là ảnh hoặc phim **cần tìm thêm** (danh sách ở mục 4.1).

| Cảnh (thời gian V6) | Thay bằng | Cách trình bày | Giữ nguyên từ V6 |
|---|---|---|---|
| **C1** (0,0–5,8) | T1 Nhà hát Lớn Hà Nội. Nếu tìm được: **P01** ảnh phố Hà Nội 1946 | Phim 4:3 có viền đen, tối đi 30% để dòng chữ đánh máy nổi rõ | Dòng gõ `Hà Nội · Tháng 12 năm 1946`, tiếng tích tắc |
| **C2** (5,8–15,8) | Khoảng 5,8–10,8: **BT1** bản tuyên bố Hiệp định Sơ bộ, kèm T2 ảnh Hồ Chí Minh và Sainteny. Khoảng 10,8–15,8: **P03** ảnh ký Tạm ước 14-9-1946 | Ảnh in đặt trên bàn (mục 2.3), đặt ở **2/3 dưới khung** vì đường thời gian nằm ở trên. Chú thích tên: `Hồ Chí Minh (1890–1969)`, `Jean Sainteny (1907–1978)` | Đường thời gian và các mốc |
| **C3** (15,8–27,8) | 15,8: **BT2** tàu chiến (chú thích *"Tàu chiến Pháp ở cảng Hải Phòng, 3-1946"*). 18,8: T3 hoặc T4. 22,8: T5 khói nổ, hoặc **P04** ảnh Hải Phòng bị phá hủy 11-1946 | **Cắt hình đúng 3 lần chớp sáng.** Phim có viền đen | Mốc đỏ 11.1946, dòng gõ `23.11.1946 · Pháp nã pháo vào Hải Phòng` |
| **C4A** (27,8–34,2) | **P05** lính hoặc xe bọc thép Pháp trên phố Hà Nội 12-1946 (dự phòng: T6). **P06** ảnh phố Hàng Bún sau vụ thảm sát (**không chọn ảnh có thi thể**) | Ảnh hoặc phim có viền đen | Dòng gõ `17.12.1946 · Thảm sát...` |
| **C4B** (34,2–41,6) | Không đổi | — | Tờ lịch và tối hậu thư |
| **C5** (41,6–51,2) | **BT3** ngôi nhà ở Vạn Phúc, ghi chú thích đúng theo bảo tàng | Ảnh in đặt trên bàn, zoom chậm về phía cửa | Ngày tháng góc trên trái, khẩu hiệu `PHÁT ĐỘNG TOÀN QUỐC KHÁNG CHIẾN` |
| **C6A** (51,2–57,2) | **P07** chiến lũy hoặc tự vệ trên phố Hà Nội 12-1946 | Ảnh có viền đen | Ngày tháng `TỐI 19.12.1946` |
| **C6B** (57,2–63,2) | **P08** nhà máy điện Yên Phụ. Nếu không có: **nền đen, chỉ còn đồng hồ** | Ảnh tối đi 50% để đồng hồ nổi rõ | Đồng hồ 20:02:55 → 20:03:00, hiệu ứng chập chờn |
| **C7** (63,2–77,4) | 64,2: **P09** khẩu pháo của pháo đài Láng (dự phòng: T5). Khoảng 68–76,8: T7, T6, **P10** giao tranh ở Bắc Bộ phủ hoặc Bưu điện Bờ Hồ 12-1946 | **Cắt hình đúng tiếng đại bác ở 64,2**, sau đó cắt theo nhịp tiếng súng. Phim tối đi để chữ dễ đọc | Màn đen 1 s, chớp trắng, rung, `20 GIỜ 3 PHÚT`, dòng phụ |
| **C8** (77,4–106,8) | Giữ **ảnh bản thảo** (BT5 hoặc ảnh V6 đang dùng). Thêm **P11** chân dung Hồ Chí Minh năm 1946 trong khoảng 1,5 s đầu | Như V6 | Nền đỏ, ngôi sao, chữ trích dẫn |
| **C9** (106,8–119,8) | Trái: **P12** lính Pháp ở Hà Nội 1946 (dự phòng: T7). Phải: **P13** vệ quốc quân hoặc tự vệ Hà Nội 1946 | Mỗi nửa một ảnh hoặc phim đen trắng, cắt cho vừa nửa khung | Nhãn, vạch đỏ, số liệu đếm |
| **C10** (119,8–129,0) | **P14** ảnh "Tự vệ thành Hoàng Diệu ôm bom ba càng" (23-12-1946) | Ảnh in đặt trên bàn hoặc toàn khung nếu ảnh đủ lớn, tối đi 60% | Ba dòng "Thiếu…", câu `Lấy gì để thắng?` |
| **C11** (129,0–134,8) | **P15** Hà Nội trong 60 ngày đêm, hoặc Trung đoàn Thủ đô (dự phòng: T8) | Ảnh tối đi 50% | Tên đề tài, vạch đỏ |
| **Mới: thêm sau C11** | Màn **"Tư liệu sử dụng"**, 4–5 s, liệt kê nguồn ảnh và phim | Chữ nhỏ trên nền đen | Âm thanh: thêm im lặng ở cuối, V6 không bị cắt |

### 4.1. Danh sách tư liệu cần tìm

Thứ tự theo mức ưu tiên.

| Mã | Cần tìm | Từ khóa gợi ý (Việt / Anh / Pháp) | Nơi nên tìm |
|---|---|---|---|
| **P14** | Tự vệ thành Hoàng Diệu ôm bom ba càng, 23-12-1946 | "tự vệ Hoàng Diệu bom ba càng 1946" | TTXVN, special.nhandan.vn, Bảo tàng Lịch sử Quân sự |
| **P07** | Chiến lũy, tự vệ trên phố Hà Nội 12-1946 | "chiến lũy Hà Nội 1946", "Hanoi barricade December 1946" | TTXVN, Nhân Dân, Bảo tàng Hà Nội |
| **P09** | Khẩu pháo ở pháo đài Láng | "pháo đài Láng 19-12-1946 khẩu pháo" | Bảo tàng Lịch sử Quân sự, báo QĐND |
| **P05** | Lính hoặc xe bọc thép Pháp trên phố Hà Nội 12-1946 | "Hanoi décembre 1946 troupes françaises automitrailleuse" | ECPAD (imagesdefense.gouv.fr), British Pathé |
| **P11** | Chân dung Chủ tịch Hồ Chí Minh năm 1946 | "Hồ Chí Minh 1946 chân dung" | Bảo tàng Hồ Chí Minh, TTXVN |
| **P03** | Ký Tạm ước 14-9-1946 (Hồ Chí Minh và Marius Moutet) | "Tạm ước 14-9-1946", "modus vivendi Moutet Ho Chi Minh 1946" | Bảo tàng Hồ Chí Minh, TTXVN |
| **P13** | Vệ quốc quân hoặc tự vệ Hà Nội 1946 | "vệ quốc quân 1946", "tự vệ thành Hoàng Diệu" | TTXVN, Nhân Dân |
| **P12** | Lính Pháp ở Hà Nội 1946 | "soldats français Hanoi 1946" | ECPAD, British Pathé |
| **P10** | Giao tranh ở Bắc Bộ phủ, Bưu điện Bờ Hồ, chợ Đồng Xuân 12-1946 | "Bắc Bộ phủ 1946", "Hà Nội 60 ngày đêm" | Nhân Dân (bài "Hà Nội 60 ngày đêm"), TTXVN |
| **P04** | Hải Phòng bị phá hủy 11-1946 | "Hải Phòng 23-11-1946", "Haiphong bombardment 1946" | ECPAD, Bảo tàng Hải Phòng |
| **P06** | Phố Hàng Bún sau ngày 17-12-1946 | "thảm sát phố Hàng Bún 1946" | Nhân Dân, TTXVN |
| **P15** | Hà Nội 60 ngày đêm, Trung đoàn Thủ đô | "Trung đoàn Thủ đô 1947" | Nhân Dân, Bảo tàng Hà Nội |
| **P01** | Phố Hà Nội năm 1946 | "Hà Nội 1946 phố" | British Pathé, ECPAD |
| **P08** | Nhà máy điện Yên Phụ thời Pháp | "nhà máy điện Yên Phụ xưa" | EVN, Bộ Công Thương |
| **Phim** | Đoạn phim thời sự Hà Nội 12-1946 | British Pathé: "Hanoi 1946", "Indo-China fighting 1946"; phim "Hà Nội 60 ngày đêm khói lửa" | britishpathe.com, Hãng phim Tài liệu và Khoa học Trung ương |

**Cách giao tư liệu:**
1. Đặt ảnh vào `video-hook/assets/tu-lieu/anh/`, phim vào `video-hook/assets/tu-lieu/phim/`. Tên file theo mã, ví dụ `P14-tu-ve-bom-ba-cang.jpg`.
2. Điền thông tin từng file vào `video-hook/assets/tu-lieu/nguon-tu-lieu.json`, gồm:

```json
{ "file": "anh/P14-tu-ve-bom-ba-cang.jpg", "maCanh": "C10",
  "moTa": "Tự vệ thành Hoàng Diệu ôm bom ba càng", "ngayChup": "23-12-1946", "noiChup": "Hà Nội",
  "nguon": "TTXVN", "url": "https://...", "ghiChuQuyen": "dùng cho thuyết trình trên lớp" }
```

- Ảnh nên có cạnh ngắn từ 1080 px trở lên. Ảnh nhỏ hơn thì xử lý theo mục 2.3.
- **Không** tải ảnh đã bị người khác tô màu hay dàn dựng lại. Không dùng ảnh có chữ chèn của báo.

---

## 5. Cách làm kỹ thuật

### Phương án A (nên chọn): có mã nguồn V6

1. Bạn hoặc agent bên máy kia đẩy **toàn bộ dự án đã dựng V6** lên repo, ví dụ vào `video-hook/v6-src/`. Gồm:
   - trang dựng hoặc file dự án;
   - ảnh A01–A13 và ảnh bản thảo;
   - file giọng đọc gốc;
   - các file âm thanh đã trộn;
   - lệnh xuất video.
2. Mình thêm vào bộ dựng **lớp "phim tư liệu"**: phát đoạn video có điểm vào và điểm ra, có tốc độ, đặt giữa khung kèm viền đen, chỉnh đen trắng. Thêm **khung "ảnh in đặt trên bàn"** và **chú thích tên, nguồn**.
3. Thay hình nền từng cảnh theo bảng ở mục 4. **Không động vào** lớp chữ, mốc thời gian và âm thanh.
4. Xuất V7, cùng độ dài với V6, cộng thêm màn "Tư liệu sử dụng".

### Phương án B (khi không lấy được mã nguồn V6)

1. **Lấy nguyên rãnh âm thanh từ `hook.mp4` của V6**, dùng làm âm thanh cho V7. Âm thanh vì thế giống V6 hoàn toàn.
2. **Dựng lại lớp chữ và đồ họa** bằng bộ dựng trong repo (`index.html` và `style/video-style.json`), theo mốc thời gian đo từ V6 (mục 1.1).
3. **Căn chữ đánh máy theo tiếng gõ có sẵn trong âm thanh V6.** Mình dò được thời điểm từng tiếng gõ (đã làm khi cắt bộ tiếng máy chữ), nên đặt được từng ký tự trùng đúng tiếng gõ.
4. Đặt hình nền mới theo mục 4, rồi xuất V7.
5. So khung hình V7 với `v6-storyboard.jpg` ở cùng mốc, để chắc chữ nằm đúng chỗ và đúng lúc.

Phương án B tốn công hơn, và chữ có thể lệch vài khung hình so với V6. Nên chỉ dùng khi không có mã nguồn.

---

## 6. Kiểm tra lịch sử và quyền sử dụng

| Điểm | Xử lý |
|---|---|
| Ảnh BT2 (tàu chiến) chụp ngày **5-3-1946**, không phải 23-11 | Chú thích ghi đúng "3-1946". Ảnh chỉ minh họa sự có mặt của tàu chiến Pháp ở Hải Phòng |
| Ảnh BT4 (Bắc Bộ phủ) là **ảnh màu chụp ngày nay** | Không dùng làm ảnh năm 1946. Nếu dùng phải ghi "Bắc Bộ phủ ngày nay". Nên tìm P10 thay thế |
| Bài bảo tàng ghi khai hỏa "**20 giờ**", V6 ghi "**20 giờ 3 phút**" | Giữ **20 giờ 3 phút** theo giáo trình (dòng 3139: "vào lúc 20 giờ 3 phút, pháo đài Láng bắn loạt đại bác đầu tiên"). "20 giờ" là mốc nổ súng chung trên toàn quốc |
| Bài bảo tàng có mốc **18-12-1964** | Lỗi gõ trong bài. V6 không dùng mốc này |
| Phim chưa rõ nơi quay (Hà Nội hay Sài Gòn) | Không ghi địa danh, chỉ ghi nguồn |
| Ảnh có cảnh chết chóc (Hàng Bún, Hải Phòng) | Không dùng ảnh có thi thể. Chọn ảnh đường phố đổ nát |
| Logo British Pathé | Giữ nguyên, ghi nguồn. Chỉ dùng cho buổi thuyết trình |
| Ảnh TTXVN, Bảo tàng | Ghi nguồn trên khung và ở màn "Tư liệu sử dụng" |

---

## 7. Các bước và phân công

| Bước | Việc | Ai làm | Ghi chú |
|---|---|---|---|
| 0 | Chốt các quyết định ở mục 8 | Bạn | |
| 1 | Đưa mã nguồn V6 lên repo (phương án A) | Bạn hoặc agent bên kia | Nếu không có thì làm phương án B |
| 2 | Tìm và tải tư liệu theo mục 4.1, điền `nguon-tu-lieu.json` | Bạn hoặc agent bên kia | Ưu tiên P14, P07, P09, P05, P11 |
| 3 | Cắt phim T1–T8 từ video tham khảo, chỉnh đen trắng, bỏ viền | Mình | **Làm được ngay**, vì file đã có trong repo |
| 4 | Xử lý ảnh: phóng to (nếu bạn đã chạy AI phóng to thì dùng bản đó), chỉnh tông, làm khung "ảnh in" | Mình | |
| 5 | Nâng cấp bộ dựng (lớp phim tư liệu, khung ảnh, chú thích tên và nguồn) rồi dựng V7 | Mình | Phương án A hoặc B |
| 6 | Kiểm tra: so storyboard V7 với V6, rà chú thích theo mục 6, xác nhận âm thanh giống V6 | Mình | Gửi bạn bản 720p xem trước |
| 7 | Bạn duyệt, sửa tối đa 2 vòng, xuất bản cuối và đẩy lên `out/history-1946-v7/` (dùng LFS) | Bạn và mình | |

---

## 8. Câu hỏi cần bạn trả lời

1. **Mã nguồn V6** đang nằm ở đâu? Bạn có thể nhờ agent bên kia đẩy lên repo được không? (Phương án A hay B)
2. Có được **dùng các đoạn phim cắt từ video tham khảo** (logo Pathé) cho buổi thuyết trình không?
3. Cảnh nào **không tìm được tư liệu thật** thì dùng **nền tối chỉ có chữ** (đề xuất của mình), hay giữ tạm tranh AI của V6 nhưng chuyển sang đen trắng?
4. Có thêm **màn "Tư liệu sử dụng"** khoảng 4–5 giây ở cuối không?
5. Bạn có máy chạy được **Upscayl hoặc Real-ESRGAN** để phóng to ảnh nhỏ không?

---

## 9. Đã chốt (cập nhật sau khi bạn trả lời)

| Câu hỏi | Trả lời | Cách làm |
|---|---|---|
| 1. Mã nguồn V6 | Đã đẩy lên repo | Repo vẫn thiếu `out/history-1946-v6/timeline.json` và `variables.json` (bị `.gitignore` bỏ qua). Đã **dựng lại hai file này** từ `scripts/render-history-v4.ts` + `render-history-v6.ts`, thời lượng cảnh đo từ `hook.mp4` V6. Kết quả trùng V6 đến từng khung hình, nên làm được theo **phương án A**. |
| 2. Dùng phim cắt từ video tham khảo | Có | Dùng T1, T2, T4, T5, T6a–c, T7a–b, T8a–b. Giữ logo Pathé. |
| 3. Cảnh không có tư liệu thật | Giữ tranh AI, chuyển đen trắng | C6 (cả hai phần), C7 lúc pháo đài Láng khai hỏa, C9 nửa phải, C10. Ghi "Tranh minh họa (AI)" ở góc. |
| 4. Màn "Tư liệu sử dụng" | Không | Nguồn ghi ngay trên từng hình, chữ nhỏ góc dưới phải. |
| 5. Phóng to ảnh | Mình chạy Real-ESRGAN ngay trong môi trường này | `v7/phong-to-anh.py`; kết quả trong `assets/tu-lieu/anh/`. |

Kết quả và cách dựng lại: xem `v7/README.md`.
