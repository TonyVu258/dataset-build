# Consistency

Dataset: `images-test/Cay-sau-rieng`

Trạng thái: **không đạt**

## Câu hỏi

Các bản ghi của cùng một sự vật có mâu thuẫn nhau hay không?

## Kiểm tra

### Một nội dung byte chỉ có một thư mục bệnh

Trạng thái: **đạt**

Quy tắc: không nội dung byte nào đứng trong hơn một thư mục bệnh.

Kết quả: 0

### Một tên file chỉ một ảnh

Trạng thái: **không đạt**

Quy tắc: một tên file không trỏ tới nhiều nội dung byte ở nhiều thư mục bệnh.

Kết quả: 97 tên file.

### Tên bệnh khớp giữa hai tập

Trạng thái: **đạt**

Quy tắc: tên thư mục bệnh ở `Test` và `Validation` khớp từng ký tự.

Kết quả: khớp. Cả hai phía đều có tên `stem_cracking_ gummosis`, với một dấu cách.

## Cần bổ sung

- [ ] Bảng từ đồng nghĩa, nếu `healthy` và `normal` được xem là cùng một nghĩa. Chưa có bảng này nên chưa kiểm.
