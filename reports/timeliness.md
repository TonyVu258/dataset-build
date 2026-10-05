# Timeliness

Dataset: `images-test/Cay-sau-rieng`

Trạng thái: **chưa kiểm được**

## Câu hỏi

Ảnh còn đúng với thời điểm sẽ dùng bộ dữ liệu hay không?

## Điều kiện

- [ ] File còn ngày chụp. 36 file `.jpg` không có khối EXIF. 1.244 file PNG có chữ ký PNG thì không chứa chuỗi ngày giờ.
- [ ] Đã đặt ngưỡng. Ví dụ: ảnh cũ hơn 12 tháng thì không dùng.

## Cách đo

1. Đọc ngày chụp trong file.
2. So với ngày sẽ dùng bộ dữ liệu và với ngưỡng đã đặt.
3. Đếm ảnh vượt ngưỡng và ảnh không có ngày.

## Quy tắc đạt

Không ảnh nào vượt ngưỡng. Ảnh thiếu ngày là lỗi completeness, và làm bài kiểm tra này không chạy được.

## Kết quả

Chưa có.

## Cần bổ sung

- [ ] Ngày chụp đáng tin cho mỗi ảnh.
- [ ] Ngưỡng bao lâu thì ảnh còn được dùng.
