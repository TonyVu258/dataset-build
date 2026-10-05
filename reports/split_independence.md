# Split independence

Dataset: `images-test/Cay-sau-rieng`

Trạng thái: **không đạt**

## Câu hỏi

Ảnh dùng để chấm điểm đã xuất hiện trong tập còn lại hay chưa?

Một bản trùng trong cùng một tập là dư thừa. Cùng bản đó nằm ở cả `Test` và `Validation` làm cho tập giữ lại không còn là ảnh chưa thấy. Uniqueness không ghi chỗ bản trùng đang nằm.

## Kiểm tra

### Không dùng chung nội dung byte

Trạng thái: **không đạt**

Quy tắc: số nội dung byte có mặt ở cả `Test` và `Validation` bằng 0.

Kết quả: 158

### Không dùng chung một cảnh

Trạng thái: **chưa kiểm được**

Cần danh sách nghi ngờ từ uniqueness theo cảnh, rồi người xác nhận.

### Không dùng chung một cây

Trạng thái: **chưa kiểm được**

Cần mã cây. Mọi ảnh của cùng một cây phải nằm trong một tập.
