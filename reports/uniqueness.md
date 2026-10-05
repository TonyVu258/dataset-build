# Uniqueness

Dataset: `images-test/Cay-sau-rieng`

Trạng thái: **không đạt**

## Câu hỏi

Một sự vật có bị ghi nhiều hơn một lần hay không?

## Kiểm tra

### Cùng từng byte

Trạng thái: **không đạt**

Quy tắc: mỗi nội dung byte chỉ xuất hiện một lần.

| Số đo | Giá trị |
|---|---|
| File ảnh | 1.297 |
| Nội dung byte khác nhau | 1.105 |
| Nội dung bị lưu nhiều lần | 166 |
| Trong đó khác tên file | 49 |

### Cùng một cảnh, khác byte

Trạng thái: **chưa kiểm được**

Quy tắc: mỗi cảnh chỉ xuất hiện một lần, kể cả khi byte đã đổi vì nén hoặc thu nhỏ.

Perceptual hash chỉ lập danh sách nghi ngờ. Người xác nhận các cặp gần ngưỡng. Chưa chạy.

### Cùng một cây

Trạng thái: **chưa kiểm được**

Quy tắc chưa đặt. Nhiều ảnh của cùng một cây là các mẫu không độc lập. Không có mã cây. Hash không thay được mã cây.

## Cần bổ sung

- [ ] Có chấp nhận bản trùng byte trong cùng một tập hay không? Bản nằm ở cả hai tập được ghi ở `split_independence.md`.
- [ ] Ngưỡng perceptual hash, khi nào kiểm tra cảnh.
- [ ] Mã cây cho mỗi ảnh, nếu uniqueness theo cây là bắt buộc.
