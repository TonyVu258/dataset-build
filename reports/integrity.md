# Integrity

Dataset: `images-test/Cay-sau-rieng`

Trạng thái phép đo: **blocked**

Specification: **Draft**

Kết quả do `integrity_checker.py` ghi. Requirement chưa Frozen hoặc BLOCKED không được gán PASS hay FAIL.

## Why

Integrity hỏi dữ liệu có còn nguyên vẹn, và có còn là dữ liệu mà hệ thống tuyên bố đã lưu, hay không.

Validity hỏi file có phải PNG hoặc JPEG đúng quy tắc hay không. Accuracy hỏi ảnh có đúng bệnh hay không. Uniqueness hỏi một sự vật có bị ghi nhiều lần hay không. Hash trong uniqueness dùng để tìm bản trùng. Hash trong integrity dùng để hỏi nội dung còn đúng phiên bản đã xác nhận hay không.

Một file có thể vẫn là PNG hợp lệ sau khi nội dung đã đổi. Validity khi đó vẫn có thể đạt. Integrity fail khi fingerprint đã xác nhận không còn khớp.

## Requirement

| # | Requirement | Rule | Trạng thái |
|---|---|---|---|
| 1 | Identity / reference | `image_key` phải resolve đúng tới artifact được định danh. Mọi thay đổi identity/reference phải nằm trong quy trình được cho phép | Chưa Frozen |
| 2 | Content integrity | SHA-256 hiện tại của artifact phải bằng baseline fingerprint đã được khóa | BLOCKED. Chưa có baseline đã khóa |
| 3 | Catalog ↔ file | Các metadata được catalog tuyên bố phải khớp với artifact theo source-of-truth đã xác định | BLOCKED. Chưa chọn source of truth |
| 4 | Provenance | Thay đổi quan trọng phải truy được: đổi gì, khi nào, từ phiên bản nào, bởi quy trình nào, vì sao | Không mở |

Frozen là cổng để được chấm. Không phải requirement thứ năm.

### 1. Identity / reference

`image_key` phải trỏ tới file mà record tuyên bố.

```text
image_key
    ↓
file thực tế
```

Mọi thay đổi identity hoặc reference phải nằm trong quy trình được cho phép. Completeness đã kiểm file còn trên đĩa. Việc file bị thay nội dung mà đường dẫn vẫn giữ nguyên thuộc requirement 2. Requirement 1 chưa Frozen.

### 2. Content integrity

Nếu một file đã có fingerprint được tin cậy:

```text
image → SHA-256 → ABC123
```

Kiểm lại vẫn ra `ABC123` thì nội dung không đổi. Ra `XYZ999` thì có bằng chứng nội dung đã đổi.

Baseline phải là fingerprint đã khóa, không phải hash vừa tính lại rồi ghi đè cùng lúc với file. `content_hash` hiện trong catalog được tính từ file lúc lập catalog. Chưa có baseline đã khóa, nên requirement 2 là BLOCKED.

### 3. Catalog ↔ file

Catalog có thể ghi một `content_hash`, trong khi file trên đĩa đã thành hash khác. Catalog của bộ này không có `width` và `height`.

Phải chọn source of truth trước khi gọi một bên là sai. Nếu không biết catalog đúng hay file đúng, lệch nhau chỉ có nghĩa hai bên không còn khớp. Chưa chọn source of truth, nên requirement 3 là BLOCKED.

### 4. Provenance

Đường đi như raw, làm sạch, đổi tên, đổi kích thước, sửa nhãn nên truy được đổi gì, khi nào, từ phiên bản nào, bởi quy trình nào, và vì sao. Bộ học này chưa cần một hệ versioning đầy đủ. Chưa có lịch sử đó, nên requirement không mở.

## Kết quả

Nguồn: `integrity_checker.py`. Không tính lại SHA-256. Không gán PASS hay FAIL cho requirement chưa Frozen hoặc BLOCKED.

| Requirement | Kết quả | Lý do |
|---|---|---|
| 1. Identity / reference | chưa chấm | Requirement chưa Frozen |
| 2. Content integrity | BLOCKED | Chưa có baseline fingerprint đã khóa |
| 3. Catalog ↔ file | BLOCKED | Chưa chọn source of truth |
| 4. Provenance | không mở | Chưa có lịch sử thay đổi |

| Quan sát | Số |
|---|---:|
| Record trong catalog | 1.297 |
| `image_key` không còn file | 0 |

Số file còn trỏ được không phải PASS của requirement 1.

Cả phép đo: BLOCKED.
