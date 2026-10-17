# V8: thêm ảnh do nhóm cung cấp

V8 là V7 thay thêm 5 hình bằng ảnh nhóm tải lên repo (commit `05e40fa`). Âm thanh, chữ, đồ họa, nhịp giữ nguyên V6/V7; rãnh âm thanh vẫn chép nguyên từ V6.

## Những chỗ đổi so với V7

| Cảnh | Thời gian | V7 | V8 | Ảnh |
|---|---|---|---|---|
| C2 | 5,9 – 10,9 | Bản tuyên bố (DÉCLARATION) về Hiệp định Sơ bộ, tiếng Pháp (BT1) | Văn bản Hiệp định Sơ bộ tiếng Việt, khung ảnh in | ND1 |
| C5 | 42,2 – 51,2 | Ảnh cũ ngôi nhà ở Vạn Phúc (BT3) | Ảnh chụp ngày nay ngôi nhà ở Vạn Phúc, khung ảnh in | ND2 |
| C7 | 64,2 – 70,0 | Tranh AI Pháo đài Láng | Ảnh khẩu đội pháo Pháo đài Láng, phủ kín khung, giữ hiệu ứng lóe sáng, rung và thu ống kính | ND3 |
| C9 trái | 106,7 – 119,7 | Phim lính Pháp trên phố (T7a) | Ảnh quân Pháp (ảnh minh họa) | ND4 |
| C9 phải | 106,7 – 119,7 | Tranh AI quân dân Hà Nội | Ảnh bộ đội Việt Nam (ảnh minh họa) | ND5 |

Các cảnh khác giống V7. Còn hai cảnh vẫn dùng tranh AI đen trắng vì chưa có ảnh thật: **C6** (chiến lũy; nhà máy điện và đồng hồ, 51,2 – 63,2) và **C10** (quyết tử quân, 119,7 – 128,7).

Ảnh gốc của nhóm vẫn để nguyên ở thư mục gốc repo. Bản đã xử lý nằm ở `assets/tu-lieu/anh/ND1…ND5`, cách xử lý ghi trong `assets/tu-lieu/nguon-tu-lieu.json`:

- ND1, ND2 đủ lớn nên chỉ chuyển đen trắng.
- ND3, ND4, ND5 nhỏ (rộng 474–568 px) nên phóng to ×4 bằng Real-ESRGAN rồi trộn 50% với bản phóng to thường. Ảnh chỉ qua Real-ESRGAN trông loang như tranh sơn dầu; trộn lại thì giữ được chất ảnh cũ.

## Dựng lại V8

Dùng chung script và trang dựng của V7, chỉ khác file cảnh và thư mục ra:

```bash
cd video-hook
node v7/dung-v7.mjs v8/canh-v8.json out/history-1946-v8
node v7/xuat-hinh.cjs --template templates/history-v7/index.html \
  --vars out/history-1946-v8/build/variables-v8.json \
  --video out/history-1946-v8/build/video-silent.mp4 --workers 3 --crf 18
```

Sau đó nén 2 lượt và ghép âm thanh V6 như V7 (lệnh ở `out/history-1946-v8/README.md`).

`canh-v8.json` có thêm trường `position` (phần ảnh giữ lại khi ảnh phủ kín khung, dùng cho hai nửa C9).
