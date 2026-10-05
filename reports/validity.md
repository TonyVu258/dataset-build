# Validity

Dataset: `images-test/Cay-sau-rieng`

Trạng thái: **không đạt**

## Câu hỏi

File có tuân thủ quy tắc kỹ thuật đã viết hay không?

## Kiểm tra

### Đuôi file khớp chữ ký byte

Trạng thái: **không đạt**

Quy tắc: đuôi file khớp với byte đầu của nội dung.

17 file khai `.png` nhưng là JPEG:

- `Validation/fruit_rot/2000.png`
- `Validation/fruit_rot/2001.png`
- `Validation/fruit_rot/2003.png`
- `Validation/fruit_rot/2004.png`
- `Validation/fruit_rot/2005.png`
- `Validation/fruit_rot/2006.png`
- `Validation/fruit_rot/2007.png`
- `Validation/fruit_rot/2008.png`
- `Validation/fruit_rot/2009.png`
- `Validation/fruit_rot/2010.png`
- `Validation/fruit_rot/2011.png`
- `Validation/fruit_rot/2012.png`
- `Validation/fruit_rot/2013.png`
- `Validation/fruit_rot/2014.png`
- `Validation/fruit_rot/2015.png`
- `Validation/fruit_rot/2017.png`
- `Validation/fruit_rot/2018.png`

### Ảnh giải mã được

Trạng thái: **chưa chạy**

Quy tắc: mọi file ảnh giải mã được.

### Kích thước nằm trong khoảng cho phép

Trạng thái: **chưa kiểm được**

Chưa đặt khoảng kích thước cho phép.

### Nhãn thuộc danh sách cho phép

Trạng thái: **chưa kiểm được**

Nhãn nằm trong danh sách cho phép là validity. Nhãn đúng bệnh là accuracy. Danh sách cho phép chưa được chốt riêng khỏi tên thư mục hiện có.

## Cần bổ sung

- [ ] Khoảng kích thước ảnh được phép.
- [ ] Danh sách nhãn hợp lệ, nếu khác với mười tên thư mục hiện tại.
