# V9: không còn tranh AI

V9 là V8 thay nốt 3 tranh AI cuối cùng bằng ảnh tư liệu nhóm gửi. Toàn bộ hình nền giờ là ảnh hoặc phim tư liệu thật (đen trắng), trừ màn đen, nền đỏ của Lời kêu gọi và tờ lịch/tối hậu thư vẽ bằng đồ họa. Âm thanh, chữ, đồ họa, nhịp giữ nguyên V6.

## Những chỗ đổi so với V8

| Cảnh | Thời gian | V8 (tranh AI) | V9 | Ảnh |
|---|---|---|---|---|
| C6 | 51,2 – 57,2 | Chiến lũy đêm 19-12 | Bộ đội chiến đấu dọc dãy nhà mái vòm, ảnh TTXVN | ND6 |
| C6 | 57,2 – 63,2 | Nhà máy điện và đồng hồ | Nhà máy điện Yên Phụ, giảm sáng cho hợp cảnh tối; đồng hồ 20:02:55 → 20:03:00 và lúc đèn chớp tắt giữ nguyên | ND7 |
| C10 | 119,7 – 128,7 | Quyết tử quân ôm bom ba càng | Chiến sĩ quyết tử cầm bom ba càng bên đống gạch đổ | ND8 |

Ảnh gốc lưu ở `assets/tu-lieu/anh/goc/`. Cách xử lý và ghi chú nguồn ở `assets/tu-lieu/nguon-tu-lieu.json`. ND6 có dấu TTXVN ở góc dưới phải; khi dựng phần đó bị cắt khỏi khung nên nguồn TTXVN được ghi ở dòng chú thích.

## Dựng lại V9

```bash
cd video-hook
node v7/dung-v7.mjs v9/canh-v9.json out/history-1946-v9
node v7/xuat-hinh.cjs --template templates/history-v7/index.html \
  --vars out/history-1946-v9/build/variables-v9.json \
  --video out/history-1946-v9/build/video-silent.mp4 --workers 3 --crf 18
```

Sau đó nén 2 lượt và ghép âm thanh V6 như V8 (lệnh ở `out/history-1946-v9/README.md`).
