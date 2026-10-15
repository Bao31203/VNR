# Thiết kế ảnh minh họa cho video hook

File này dùng để gửi cho người vẽ hoặc dán vào AI tạo ảnh (Midjourney, DALL·E / ChatGPT, Gemini, Leonardo, Ideogram...). Mã ảnh **A01–A13** khớp với các cảnh C1–C11 trong `kich-ban-loi-dan.md`.

## Danh sách ảnh

| Mã | Cảnh | Nội dung | Ưu tiên |
|---|---|---|---|
| A01 | C1 | Đồng hồ treo tường trong nhà phố cổ, ánh đèn dầu | Cao |
| A02 | C2 | Phố cổ Hà Nội chập tối tháng 12-1946 | **Rất cao** (ảnh chuẩn phong cách cho cả bộ) |
| A03 | C3 | Tàu chiến Pháp nã pháo vào Hải Phòng | Cao |
| A04 | C4 | Xe bọc thép Pháp trên phố Hà Nội | Cao |
| A05 | C4 | Bàn giấy có tờ tối hậu thư | Thấp (có thể giữ bản đồ họa của bản nháp) |
| A06 | C5 | Làng Vạn Phúc ban đêm, cuộc họp quyết định kháng chiến | Cao |
| A07 | C6 | Chiến lũy trên phố đêm 19-12, tự vệ chờ hiệu lệnh | **Rất cao** |
| A08 | C6 | Phòng máy nhà máy điện Yên Phụ | Vừa |
| A09 | C7 | Pháo đài Láng khai hỏa | **Rất cao** |
| A10 | C8 | Gia đình đọc Lời kêu gọi dưới đèn dầu | Cao |
| A11a / A11b | C9 | Quân Pháp và quân dân Hà Nội (hai nửa màn hình) | Cao |
| A12 | C10 | Quyết tử quân ôm bom ba càng trước xe tăng | **Rất cao** (ảnh "chốt" của video) |
| A13 | C11 | Bình minh trên mái phố, nền cho tên đề tài | Vừa |
| S1–S4 | Slide | Ảnh bổ sung cho phần thuyết trình (không bắt buộc) | Tùy chọn |

---

## 1. Quy tắc chung (áp dụng cho mọi ảnh)

### 1.1. Phong cách

**Tranh minh họa lịch sử kiểu điện ảnh, vẽ tay kỹ thuật số với chất màu bột (gouache), thấy được nét cọ.**
- Không vẽ kiểu ảnh chụp, không 3D, không anime.
- Không khí trầm, căng thẳng, có chiều sâu không gian (sương, khói).
- Ánh sáng tương phản mạnh: đêm xanh thẫm đối lập với ánh đèn vàng ấm và ánh lửa cam đỏ.

**Bảng màu** (giữ khớp với phần đồ họa chữ trong video):

| Vai trò | Màu | Mã |
|---|---|---|
| Đêm, nền | Xanh than | `#0D1626` – `#1D2A40` |
| Đèn, ánh ấm | Vàng hổ phách | `#F2C14E` / `#FFD27A` |
| Lửa, nhấn mạnh | Đỏ gạch | `#C8302A` |
| Giấy, chữ | Kem | `#EFE6D2` |
| Đất, gỗ, áo nâu | Nâu sẫm | `#3A2A17` |

### 1.2. Kích thước và cách giao ảnh

- **Tỉ lệ 16:9, tối thiểu 2560×1440 px.** Ảnh cần lớn hơn khung 1920×1080 để video còn zoom và lia chậm được.
- Riêng **A11a, A11b** dùng tỉ lệ **8:9** (hoặc 1:1 rồi cắt) vì mỗi ảnh chỉ chiếm nửa màn hình.
- Lưu PNG hoặc JPG chất lượng cao, đặt tên theo mã, ví dụ `A02-pho-ha-noi.png`, rồi bỏ vào thư mục `video-hook/assets/`.
- Với ảnh có ghi chú **"Tách lớp"**, nếu tách được nền trời, nhà xa và tiền cảnh thành các file PNG nền trong suốt (`A02-layer1.png`, `A02-layer2.png`...) thì video sẽ có hiệu ứng chiều sâu khi máy quay lia (parallax). Không tách được cũng không sao.

### 1.3. Tuyệt đối tránh

- **Chữ trong ảnh.** AI thường viết sai chữ, nên mọi chữ sẽ được thêm khi dựng video. Giấy tờ, biển hiệu trong tranh phải mờ, không đọc được.
- **Vẽ khuôn mặt nhân vật lịch sử có thật** (Hồ Chí Minh, Võ Nguyên Giáp, Trường Chinh...). Nếu cần hình Bác, hãy dùng **ảnh tư liệu thật** (TTXVN, Bảo tàng Hồ Chí Minh) và ghi nguồn. Ở cảnh Vạn Phúc chỉ vẽ bóng người, không thấy rõ mặt.
- **Máu me, xác người, cảnh tàn bạo cận cảnh.** Sự khốc liệt thể hiện qua khói lửa và nét mặt.
- **Sai bối cảnh:** nhà cao tầng, xe máy, ô tô hiện đại, cột điện hiện đại, kiến trúc kiểu Trung Quốc hay Nhật Bản, cờ Nhật, chữ thập ngoặc, biểu tượng quân Đức trên máy bay Ju 52 (phải là phù hiệu tròn xanh–trắng–đỏ của Pháp), búa liềm Liên Xô.

### 1.4. Cách giữ cả bộ ảnh đồng nhất

1. Làm **A02 trước** cho đến khi thật ưng, rồi dùng A02 làm **ảnh tham chiếu phong cách** cho mọi ảnh khác: `--sref` trong Midjourney, "style reference" trong Leonardo, hoặc đính kèm ảnh và ghi "same style as this image" với ChatGPT hay Gemini.
2. Mọi prompt đều kết thúc bằng cùng **đuôi phong cách** và **prompt loại trừ** dưới đây.
3. Tạo cả bộ trong cùng một phiên, cùng một model.

**Đuôi phong cách (STYLE), dán vào cuối mỗi prompt:**

```
cinematic historical illustration, painterly digital gouache with visible brush strokes, Vietnam 1946, muted desaturated palette of deep navy blue night and warm amber lamplight with brick-red accents, soft film grain, dramatic chiaroscuro lighting, atmospheric haze, wide 16:9 composition, no text
```

**Prompt loại trừ (NEGATIVE)**, dán vào ô negative prompt nếu công cụ có, hoặc thêm "avoid: ..." vào cuối:

```
text, letters, words, captions, signage text, watermark, signature, logo, modern buildings, skyscrapers, motorbikes, modern cars, smartphones, anime, cartoon, chibi, 3D render, plastic look, oversaturated colors, gore, blood, corpses, swastika, nazi symbols, german iron cross, japanese rising sun flag, chinese pagoda, hammer and sickle, deformed hands, extra fingers
```

Với Midjourney, thêm tham số: `--ar 16:9 --style raw`. Với A11a và A11b thì dùng `--ar 8:9`.

---

### 1.5. Vùng chừa chỗ cho chữ (khớp với wireframe trong `style/wireframes/`)

Mỗi ảnh phải chừa sẵn một vùng **tối, ít chi tiết** để đặt chữ. Vị trí chính xác xem ở ảnh wireframe cùng số cảnh.

| Ảnh | Vùng phải chừa trống | Trọng tâm ảnh đặt ở |
|---|---|---|
| A01 | Nửa trái | Đồng hồ ở 1/3 bên phải |
| A02 | 1/3 phía trên (bầu trời), dành cho đường thời gian | Con phố ở giữa và dưới |
| A03 | Dải trên (y < 340) và dải đáy (y > 860) | Con tàu ở giữa phải |
| A04 | Dải đáy (chú thích) | Xe bọc thép ở giữa |
| A06 | Góc trên trái (ngày tháng) và dải đáy (khẩu hiệu) | Khung cửa sáng ở giữa |
| A07 | Góc trên trái | Chiến lũy và người ở nửa dưới |
| A08 | 1/3 phía trên (đồng hồ đếm ngược) | Bảng điện và bàn tay ở giữa dưới |
| A09 | **Nửa trên** là trời đêm tối (tiêu đề "20 GIỜ 3 PHÚT") | Khẩu pháo và chớp lửa ở nửa dưới bên trái |
| A10 | **Nửa trái** tối (trích dẫn) | Gia đình ở nửa phải |
| A11a / A11b | 15% trên (nhãn) và 30% dưới (con số) ít chi tiết | Người và xe ở giữa |
| A12 | 1/3 phía trên (câu hỏi) | Người chiến sĩ ở giữa dưới |
| A13 | Khoảng trời giữa khung (tên đề tài) | Mái nhà và lá cờ ở dải đáy |

## 2. Tư liệu hình ảnh cho người vẽ

### 2.1. Hà Nội cuối năm 1946

- **Phố cổ:** nhà ống hẹp, 1–3 tầng, mái ngói ta đỏ sẫm hoặc nâu đen, cửa gỗ lùa, cửa chớp, ban công sắt nhỏ. Xen kẽ là nhà kiểu Pháp tường vàng đất, cửa chớp xanh lá.
- **Đường phố:** đường ray tàu điện chạy giữa phố, cột đèn đường bằng gang, xe kéo, xe đạp, quang gánh.
- **Công trình tiêu biểu:** cầu Long Biên (cầu Doumer, dầm thép), hồ Hoàn Kiếm, Bắc Bộ phủ (dinh thự kiểu Pháp), Bưu điện Bờ Hồ, chợ Đồng Xuân (mái vòm sắt).
- **Thời tiết tháng 12:** lạnh, mưa phùn, sương mù. Người dân mặc áo bông, khoác áo len, quàng khăn.
- **Người dân:** áo nâu, áo cánh, quần đen hoặc trắng, nón lá; phụ nữ thành thị mặc áo dài, chít khăn mỏ quạ. Đàn ông tóc ngắn.

### 2.2. Lực lượng Việt Nam

- **Vệ quốc quân (bộ đội chính quy), năm 1946:** *chưa có quân phục thống nhất*. Phần lớn mặc kaki bạc màu hoặc quần áo nâu, đội mũ ca-lô, mũ cát hoặc mũ sắt thu được của địch. Súng trường đủ loại (Pháp, Nhật), lựu đạn, kiếm, mã tấu. Chi tiết quân phục là theo hiểu biết chung, nên đối chiếu ảnh tư liệu.
- **Tự vệ chiến đấu (thành Hoàng Diệu):** thanh niên nam nữ, mặc áo nâu hoặc áo cánh. Vũ khí chủ yếu là gậy tầm vông vạt nhọn, mã tấu, lựu đạn, **chai cháy** (chai xăng) và **bom ba càng**.
- **Bom ba càng:** khối thuốc nổ hình phễu hoặc trụ, gắn ở đầu **một cán gỗ dài khoảng 1,5–2 m**. Mặt trước có **ba ngạnh sắt nhọn ngắn**, khi chọc vào thành xe tăng thì ba ngạnh tì vào làm kích nổ. Người lính cầm bằng hai tay như cầm giáo, lao thẳng vào xe. Đây là cách đánh **cảm tử**.
- **Chiến lũy:** dựng từ tủ, giường, bàn ghế, xe cộ, toa tàu điện lật ngang, bao cát, gạch đá. Giữa các nhà có lối "đục tường thông nhà" để di chuyển.
- **Năm 1950** (chỉ dùng cho ảnh slide S4): bộ đội đã có **mũ nan** (mũ đan bằng tre, bọc vải) cài lá ngụy trang, quân phục màu xanh, dép cao su hoặc giày vải.

### 2.3. Quân Pháp

- **Lính:** quân viễn chinh gồm lính Âu, lính lê dương và lính thuộc địa. Họ đội mũ sắt kiểu Mỹ M1, mũ bê-rê hoặc mũ ca-lô, mặc quân phục kaki hoặc xanh ô liu, mang tiểu liên Thompson, carbine M1 và súng trường MAS 36.
- **Xe:** xe tăng hạng nhẹ **M5 Stuart**, xe bọc thép bánh lốp **M8 Greyhound**, xe bọc thép Coventry, xe nửa xích. Vẽ cờ ba màu hoặc phù hiệu Pháp nhỏ trên thân xe.
- **Máy bay:** máy bay vận tải ba động cơ **Junkers Ju 52** (Pháp gọi là AAC.1 Toucan), vỏ tôn nhăn đặc trưng. **Phù hiệu tròn xanh–trắng–đỏ của Pháp.**
- **Tàu chiến:** tuần dương hạm **Suffren**, tàu chiến xám thời Thế chiến II, nhiều tháp pháo, ống khói cao, treo cờ ba màu. Trên sông có ca nô và tàu đổ bộ nhỏ.

---

## 3. Thiết kế từng ảnh

Mỗi ảnh gồm phần mô tả bằng tiếng Việt và **prompt tiếng Anh**. Hầu hết AI tạo ảnh hiểu tiếng Anh tốt hơn. Khi dùng, dán prompt, rồi dán **đuôi STYLE**, rồi thêm **NEGATIVE** nếu công cụ có ô đó.

### A01. Đồng hồ (C1, 0:00–0:05)

- **Ý đồ:** mở bằng cảm giác thời gian đang chạy.
- **Bố cục:** đồng hồ quả lắc gỗ kiểu Pháp nằm lệch phải 1/3 khung hình. Bên trái là tường vôi trống, tối dần, để đặt chữ *Hà Nội · Tháng 12 năm 1946*.
- **Ánh sáng:** đèn dầu chiếu từ dưới lên bên trái, bụi lơ lửng trong luồng sáng.
- **Chuyển động:** zoom rất chậm từ 100% vào 108% về phía mặt đồng hồ.

```
Close-up of an old French colonial-era wooden pendulum wall clock hanging on a whitewashed plaster wall inside a 1940s Hanoi tube house at night, the clock placed on the right third of the frame, warm oil lamp light from below left, dust floating in the light beam, deep shadows, empty dark wall on the left side, quiet and tense mood
```

### A02. Phố cổ Hà Nội chập tối (C2, 0:05–0:20). Ảnh chuẩn phong cách. Tách lớp.

- **Ý đồ:** Hà Nội vẫn đang sống bình thường nhưng đã căng thẳng. Đây là "hòa bình mong manh".
- **Bố cục:** góc nhìn ngang tầm mắt dọc một con phố cổ. **35% phía trên là bầu trời gần như trống** để đặt đường thời gian. Dãy nhà ống hai bên dẫn mắt vào sâu, đèn đường vừa bật.
- **Chi tiết:** đường ray tàu điện, một chiếc xe kéo, vài người áo nâu đội nón lá vội về nhà, cửa chớp khép hờ. Xa xa có một xe jeep quân sự với hai lính Pháp, nhỏ và mờ.
- **Tách lớp:** (1) bầu trời; (2) dãy nhà xa; (3) dãy nhà gần, cột đèn, người.
- **Chuyển động:** lia ngang chậm sang phải khoảng 10% chiều rộng ảnh.

```
Wide eye-level view down a street in Hanoi Old Quarter at dusk in December 1946, rows of narrow two- and three-storey tube houses with dark clay tile roofs and wooden shutters, a few faded ochre French colonial facades, cast-iron street lamps just turned on with warm glow, an empty tram track running down the middle of the street, a rickshaw, a few people in brown peasant clothes and conical hats hurrying home, a small blurred French military jeep far in the background, cold blue sky with thin winter mist occupying the top third of the image, quiet but tense atmosphere
```

### A03. Hải Phòng bị nã pháo, 23-11-1946 (C3, 0:20–0:32)

- **Ý đồ:** khoảnh khắc Pháp lật mặt. Dùng sức mạnh hải quân để đánh một thành phố.
- **Bố cục:** từ phía cảng nhìn ra. Tiền cảnh là mái nhà, nhà kho và cần cẩu cảng đang bốc khói. Trung cảnh là mặt nước sông Cấm. Hậu cảnh là tàu tuần dương xám khai hỏa, chớp lửa ở đầu nòng. Trời buổi sáng xám đục.
- **Chi tiết:** cột khói đen, đạn rơi giữa phố, bóng người dân rất nhỏ chạy dọc bờ. **Không vẽ xác người.**
- **Chuyển động:** zoom chậm về phía con tàu. Chớp sáng tiếng pháo sẽ được thêm khi dựng.

```
View from the docks of Haiphong port city on a grey overcast morning in November 1946, a grey WWII-era French navy heavy cruiser with tall funnels and gun turrets anchored offshore firing its main guns with bright muzzle flashes, shells exploding among colonial warehouses, cranes and tile-roofed houses along the river, thick black smoke columns rising over the city, tiny distant silhouettes of civilians fleeing along the quay, dramatic and tragic mood, no gore
```

### A04. Xe bọc thép Pháp trên phố Hà Nội (C4, 0:32–0:40)

- **Ý đồ:** Hà Nội bị uy hiếp ngay trên đường phố, chừng một tuần trước 19-12.
- **Bố cục:** xe bọc thép M8 chạy chéo khung hình từ phải sang trái. Lính Pháp đội mũ sắt đi bộ bên cạnh. Bên trái là người dân nép vào hiên nhà, nhìn qua khe cửa chớp. Góc phố có chiến lũy dựng dở.
- **Ánh sáng:** ban ngày u ám, lạnh, tông xanh xám.
- **Chuyển động:** lia chậm theo hướng xe chạy.

```
A French WWII-era M8 Greyhound six-wheeled armored car with a small French tricolor roundel driving slowly down a narrow Hanoi street in December 1946, French colonial soldiers in M1 steel helmets and khaki uniforms with rifles and Thompson submachine guns walking beside it, Vietnamese residents in brown clothes pressing into doorways and peeking through half-closed wooden shutters, a half-built barricade of furniture and sandbags at the street corner, cold overcast grey-blue light, oppressive mood
```

### A05. Tờ tối hậu thư (C4, tùy chọn)

Có thể **giữ phần đồ họa tờ lịch và tờ "TỐI HẬU THƯ"** của bản nháp, vì phần đó cần chữ rõ ràng. Nếu vẫn muốn có ảnh làm nền:

```
Top-down still life on an old wooden desk at night: a typed military letter on yellowed paper with completely blurred illegible text, a fountain pen, a French army kepi cap, part of an old city map, a brass desk lamp casting a pool of warm light, cold blue moonlight from a window, tense and ominous mood
```

### A06. Làng Vạn Phúc, đêm 18-12-1946 (C5, 0:46–0:55)

- **Ý đồ:** khoảnh khắc Đảng ra quyết định lịch sử. Không khí giản dị, bí mật, kiên quyết.
- **Bố cục:** nhìn từ sân vào một ngôi nhà ngói ba gian của làng Bắc Bộ. Cửa gỗ mở hé, ánh đèn dầu hắt ra. Bên trong thấy **bóng** vài người mặc đồ giản dị cúi quanh bàn có bản đồ, giấy tờ, **không thấy rõ mặt**. Ngoài sân có lũy tre, cây cau và một chiến sĩ gác trong bóng tối.
- **Chi tiết:** Vạn Phúc là làng dệt lụa, có thể thấp thoáng một khung cửi dưới hiên.
- **Chuyển động:** dolly chậm tiến về phía khung cửa sáng.

```
Night exterior of a traditional northern Vietnamese village house with a low clay tile roof in Van Phuc silk-weaving village near Hanoi, 1946, wooden doors half open with warm oil lamp light spilling into the dark courtyard, inside the doorway the silhouettes of several men in simple clothes leaning over a table covered with papers and a map, faces not visible, a wooden silk loom under the eaves, bamboo grove and areca palms around, a lone sentry with a rifle standing in the shadows near the gate, dark empty areas in the top-left corner and along the bottom of the frame, deep blue night, secret and decisive mood
```

### A07. Chiến lũy đêm 19-12-1946 (C6, 0:55–1:01). Tách lớp.

- **Ý đồ:** những giây phút chờ trước giờ nổ súng: im lặng, căng thẳng, quyết tâm.
- **Bố cục:** tiền cảnh là chiến lũy chắn ngang phố (tủ, giường, bàn ghế, toa tàu điện lật, bao cát). Phía sau chiến lũy, 4–5 tự vệ và vệ quốc quân, cả nam lẫn nữ, nép mình chờ. Một người cầm **bom ba càng**, một người cầm chai cháy, một người cầm súng trường cũ. **Đèn đường vẫn sáng** ở hậu cảnh (sắp tắt). **Phía trên giữa khung để trống** cho đồng hồ đếm ngược.
- **Chi tiết:** hơi thở thành khói vì lạnh, khăn quàng cổ, ánh mắt nhìn về phía cuối phố.
- **Tách lớp:** (1) phố và đèn ở hậu cảnh; (2) người; (3) chiến lũy tiền cảnh.

```
Night street in Hanoi on 19 December 1946, a barricade across the street built from wardrobes, beds, tables, an overturned tram car and sandbags in the foreground, behind it four or five young Vietnamese militia men and women in brown and dark clothes with scarves crouching silently and waiting, one holding a long wooden pole with a three-pronged explosive charge at its tip, one holding a glass bottle firebomb, one holding an old rifle, their breath visible in the cold air, street lamps still glowing in the background, empty dark sky at the top center, tense silent anticipation
```

### A08. Nhà máy điện Yên Phụ (C6, 1:01–1:07)

- **Ý đồ:** người thợ điện sẽ phát tín hiệu cho cả thành phố.
- **Bố cục:** phòng máy kiểu Pháp những năm 1940, có máy phát hơi nước lớn, bảng điện với đồng hồ đo bằng đồng và **cầu dao lớn**. Hai công nhân áo quần lấm dầu máy đứng cạnh bảng điện, một người nhìn đồng hồ quả quýt, tay đặt gần cần gạt.
- **Ánh sáng:** đèn vàng yếu, hơi nước, bóng đổ dài.
- **Chuyển động:** zoom chậm vào bàn tay và cầu dao.

```
Interior of a 1940s French colonial coal-fired power station in Hanoi at night, large old steam-driven generators, a marble switchboard with brass gauges and big knife switches, dim yellow work lamps, steam and long shadows, two Vietnamese workers in grease-stained work clothes standing by the switchboard, one checking a pocket watch, the other with his hand near a large lever, tense focused expressions, the upper third of the frame dark and empty, the moment just before a signal
```

### A09. Pháo đài Láng khai hỏa, 20 giờ 03 (C7, 1:08–1:15)

- **Ý đồ:** cao trào của video, tức khoảnh khắc kháng chiến toàn quốc bùng nổ.
- **Bố cục:** góc thấp. Khẩu pháo dã chiến cũ đặt trong công sự đất, **chớp lửa đầu nòng rực sáng** soi gương mặt 3–4 pháo thủ từ phía dưới. Hậu cảnh xa là bóng thành phố tối đen, **mất điện hoàn toàn**, chỉ còn vài đốm lửa.
- **Chi tiết:** khói súng, tia lửa. Pháo thủ mặc đồ đơn giản, đội mũ ca-lô hoặc mũ cát.
- **Chuyển động:** rung mạnh khung hình đúng nhịp tiếng pháo, sau đó zoom ra chậm.

```
Night, an old earthwork artillery fortification on the western edge of Hanoi in December 1946, low angle shot, Vietnamese artillerymen in simple uniforms and caps firing an old field gun, an enormous bright muzzle flash lighting their determined faces from below, smoke and sparks, in the far background the dark silhouette of the city with every light out, only a few distant fires, the gun and the crew placed in the lower half of the frame, the upper half kept as empty dark night sky for title text, explosive and historic moment
```

### A10. Lời kêu gọi (C8, 1:15–1:37)

- **Ý đồ:** Lời kêu gọi đến với từng gia đình. Cả dân tộc cùng đứng lên.
- **Bố cục:** trong căn nhà phố tối, một ngọn đèn dầu. Ba thế hệ (ông, mẹ, chàng trai trẻ) chụm đầu bên **tờ truyền đơn chữ mờ không đọc được**. Gương mặt kiên quyết. Khẩu súng trường dựng ở góc tường. Bàn thờ phía sau có tấm vải đỏ. **Nửa trái khung hình tối** để đặt chữ trích dẫn.
- **Chuyển động:** zoom rất chậm.

```
Inside a dim Hanoi house at night lit by a single oil lamp, three generations of a Vietnamese family, an old grandfather, a mother and a young man, gathered closely around a printed leaflet with illegible blurred text held in the young man's hands, solemn and resolute faces, an old rifle leaning against the wall, a family altar with red cloth in the background, the people placed on the right half of the frame and the left half in deep shadow, warm chiaroscuro, emotional and determined mood
```

### A11a và A11b. Tương quan lực lượng (C9, 1:37–1:50). Tỉ lệ 8:9.

Hai ảnh đặt cạnh nhau, **cùng góc máy thấp, cùng cỡ người** để dễ so sánh.
- **A11a (bên trái):** tông lạnh xanh xám. Toát lên vẻ máy móc, đông và nặng nề.
- **A11b (bên phải):** tông ấm nâu vàng. Toát lên vẻ ít người, vũ khí thô sơ nhưng kiên cường.

```
A11a: French Far East Expeditionary Corps in Hanoi 1946, low angle, a column of soldiers in M1 steel helmets and khaki uniforms with Thompson submachine guns and carbines, an M5 Stuart light tank and an M8 armored car behind them, a three-engine Junkers Ju 52 transport plane with French blue-white-red roundels flying overhead, cold grey-blue lighting, heavy mechanical menacing mood, vertical 8:9 composition
```

```
A11b: Vietnamese defenders of Hanoi in December 1946, low angle, two regular soldiers in faded khaki with simple caps and old mismatched rifles, beside young militia men and women in brown peasant clothes holding sharpened bamboo staffs, a machete, glass bottle firebombs, and one holding a long wooden pole with a three-pronged explosive charge at its tip, standing behind a barricade of furniture, warm amber light, few in number but determined, vertical 8:9 composition
```

### A12. Quyết tử quân (C10, 1:50–1:59). Ảnh chốt của video.

- **Ý đồ:** trả lời bằng hình ảnh cho câu "Lấy gì để thắng?": bằng con người và ý chí. Đây là ảnh mạnh nhất của cả video.
- **Bố cục:** một chiến sĩ trẻ quay lưng hoặc nhìn nghiêng ba phần tư, đứng giữa phố mù khói, hai tay cầm **bom ba càng** chĩa về phía trước như cầm giáo. Phía trước, **bóng xe tăng** lờ mờ hiện ra trong khói. Ngược sáng, tàn lửa bay. **Phần trên giữa khung để trống** cho chữ "Lấy gì để thắng?".
- **Chuyển động:** zoom rất chậm vào người chiến sĩ.
- **Thay thế:** có thể dùng ảnh tư liệu thật *Tự vệ thành Hoàng Diệu ôm bom ba càng* (23-12-1946, TTXVN), rồi tô màu lại hoặc đặt trên nền tranh. Nhớ ghi nguồn.

```
A lone young Vietnamese militia fighter seen from behind at a three-quarter angle, wearing simple dark clothes and a scarf, standing in a smoke-filled Hanoi street at night, gripping with both hands a long wooden pole with a three-pronged explosive charge at its tip and aiming it forward like a spear, ahead of him the dark silhouette of a tank emerging from the smoke, floating embers, strong backlight from fires, empty smoky space in the upper center, heroic yet somber mood, no gore
```

### A13. Bình minh trên mái phố (C11, 1:59–2:05)

- **Ý đồ:** sau đêm khói lửa, cuộc kháng chiến trường kỳ bắt đầu, để lại cảm giác hy vọng.
- **Bố cục:** toàn cảnh mái ngói phố cổ lúc rạng đông, vài cột khói mảnh bốc lên. Tiền cảnh là một **lá cờ đỏ sao vàng nhỏ** trên chiến lũy, bay trong gió. **Khoảng trời giữa khung để trống** cho tên đề tài.

```
Dawn over the clay tile rooftops of Hanoi Old Quarter after a night of fighting, thin columns of smoke rising, soft pink and gold light breaking through winter clouds, in the lower foreground a small red flag with a single yellow five-pointed star fluttering on top of a street barricade, birds in the sky, large calm empty sky in the center of the frame, hopeful and solemn mood
```

---

## 4. Ảnh bổ sung cho slide thuyết trình (tùy chọn)

| Mã | Nội dung | Prompt |
|---|---|---|
| S1 | Trung đoàn Thủ đô rút khỏi Hà Nội qua gầm cầu Long Biên, đêm 17-2-1947 | `Night, a long line of Vietnamese soldiers moving silently along the sandy riverbank beneath the huge steel truss Long Bien bridge over the Red River in Hanoi, small wooden boats waiting in the mist, the silhouette of a French sentry on the bridge above, cold blue moonlight, secret and tense mood` |
| S2 | Pháp nhảy dù xuống Bắc Kạn, 7-10-1947 (chiến dịch Việt Bắc) | `Autumn morning 1947, dozens of white parachutes descending over a small mountain town in a valley surrounded by limestone mountains in northern Vietnam, three-engine Junkers Ju 52 transport planes with French roundels flying low, morning mist over green jungle` |
| S3 | Phục kích trên sông Lô, 10-1947 | `Vietnamese soldiers hidden in dense jungle on the steep bank of a river in northern Vietnam in 1947 ambushing French river gunboats and small landing craft, water splashes from explosions, one boat burning, misty mountains` |
| S4 | Chiến dịch Biên giới 1950: Đông Khê, đường số 4 | `Dawn 1950, Vietnamese People's Army soldiers in green uniforms and woven bamboo helmets covered with leaf camouflage advancing over limestone hills toward a French fortified hilltop post along a mountain road in northern Vietnam near the Chinese border, smoke over the post, determined and victorious mood` |

Với hình **Chủ tịch Hồ Chí Minh quan sát mặt trận Đông Khê (1950)**, hãy dùng **ảnh tư liệu thật của TTXVN**, không dùng AI vẽ.

---

## 5. Gửi ảnh lại để dựng video

Khi có ảnh, chỉ cần bỏ vào `video-hook/assets/` đúng tên theo mã (`A01-...png` đến `A13-...png`). Bản nháp hiện tại đang dùng hình vẽ đơn giản bằng code. Sau khi thay bằng ảnh thật và ghép lời dẫn, video sẽ giữ nguyên nhịp, chữ chạy và hiệu ứng âm thanh, chỉ thay phần hình nền.
