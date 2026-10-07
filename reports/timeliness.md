# Timeliness

Dataset: `images-test/Cay-sau-rieng`

Trạng thái phép đo: **blocked**

Specification: **Draft**

## Why

Một dataset có thể đủ record, đúng định dạng, và nhất quán, nhưng ảnh hoặc nhãn lại thuộc một thời điểm khác với lúc bộ này được dùng.

Timeliness trả lời:

> Dữ liệu có còn phù hợp với thời điểm mà dataset dự kiến được sử dụng hay không?

Bốn mốc thời gian dưới đây là bốn việc khác nhau. Không gộp chúng thành một ngày.

## Requirement

| # | Requirement | Câu hỏi | Trạng thái |
|---|---|---|---|
| 1 | Thời điểm chụp | Ảnh được chụp khi nào? | Chưa có trên file |
| 2 | Thời điểm nhãn | Nhãn bệnh phản ánh thời điểm nào? | Chưa có ngày gán nhãn |
| 3 | Kỳ sử dụng | Dataset được dùng cho thời kỳ nào? | Chưa viết |
| 4 | Giới hạn tuổi | Có giới hạn tuổi dữ liệu hay không? | Không mở |

### 1. Thời điểm chụp

Ngày máy ảnh ghi lúc chụp. Đây là ngày của ảnh, không phải ngày file được lưu trên đĩa.

Quan sát đã có, chưa phải kết quả: 36 file `.jpg` không có khối EXIF. 1.244 file PNG đúng chữ ký không chứa chuỗi ngày giờ dùng được. Catalog không có trường ngày chụp.

### 2. Thời điểm nhãn

Ngày lời nhãn bệnh được coi là đúng. Nhãn có thể được gán sau ngày chụp. `dataset_label` trong catalog là tên thư mục, không kèm ngày.

Thiếu ngày ở mục 1 và mục 2 không phải lỗi completeness. Completeness đã Frozen và để ngày chụp ngoài phạm vi.

### 3. Kỳ sử dụng

Thời kỳ mà bộ này được tuyên bố sẽ dùng. Kỳ này viết trong specification trước khi đo. Không suy ra từ số lượng ảnh hay từ ngày sửa file.

Chưa viết.

### 4. Giới hạn tuổi

Nếu có một tuổi tối đa, ngưỡng đó là requirement riêng. Nó phụ thuộc kỳ sử dụng ở mục 3. Chưa có kỳ sử dụng thì ngưỡng để trống.

Ví dụ "cũ hơn 12 tháng thì không dùng" không phải rule của bộ này.

## Khi nào được chấm

Phép đo chỉ chạy sau khi mục 3 đã viết, mục 4 đã quyết định có ngưỡng hay không mở, và specification chuyển thành Frozen.

Không có ngày ở mục 1 hoặc mục 2 thì requirement tương ứng là BLOCKED. Không phải FAIL, và không sửa completeness để gọi đây là thiếu trường.

## Kết quả

Chưa có. Status còn Draft.
