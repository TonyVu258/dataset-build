# Completeness

Dataset: `images-test/Cay-sau-rieng`

Trạng thái phép đo: **đạt**

Phép đo này chỉ nói mỗi file ảnh trong phạm vi đã có một record đủ trường bắt buộc. Nó không nói bộ ảnh đã phủ đủ bệnh, đủ cây, hay đủ để huấn luyện.

Specification đóng ngày 2026-10-07, trước lần đối chiếu ở mục Kết quả. Không sửa các bảng requirement sau kết quả này.

## Requirement đã chốt

| # | Requirement | Câu hỏi |
|---|---|---|
| 1 | Dataset purpose | Bộ này dùng để quyết định việc gì? Một ca được đếm bằng gì? Completeness này tuyên bố phủ việc gì? |
| 2 | Required record fields | Một ca, theo đơn vị ở mục 1, phải có thông tin gì? |
| 3 | Required dataset cases | Bộ phải chứa những loại ca nào? |
| 4 | Missingness và allowed missing | Trạng thái nào bị tính là thiếu? Trong phạm vi, trạng thái đó được phép ở đâu? |
| 5 | Exclusions | Việc nào bộ không tuyên bố, nên sự vắng mặt không phải là thiếu? |
| 6 | Status | Specification đã Frozen chưa? Requirement nào đã đóng thì được chấm PASS, FAIL hoặc UNDETERMINED? Requirement nào còn BLOCKED? |

## Specification

Trạng thái: **Frozen**

### 1. Dataset purpose

- Quyết định bộ này dùng để làm gì: mỗi file ảnh trong `Cay-sau-rieng` đã có một record để các phép đo sau dùng được hay chưa. Record phải chỉ đúng một file, một nhãn thư mục, một split, và một nội dung byte.
- Đơn vị một ca: một file ảnh. Danh tính là `image_key`, đường dẫn đầy đủ từ `Cay-sau-rieng/`. Hai file cùng nội dung byte ở `Test` và `Validation` là hai ca.
- Phạm vi completeness tuyên bố phủ: mọi file `.jpg`, `.jpeg`, `.png` nằm trong `Test` hoặc `Validation`. Completeness trả lời record có đủ chỗ để giữ lời của thư mục hay không.

### 2. Required record fields

| Field | Required | Condition | Reason |
|---|---|---|---|
| `image_key` | có | mọi ca | Không có đường dẫn đầy đủ thì không biết ca là file nào |
| `dataset_label` | có | mọi ca | Nhãn thư mục là lời mà record đang giữ |
| `source_split` | có | mọi ca | `Test` và `Validation` là hai ca khác nhau khi cùng nội dung |
| `content_hash` | có | mọi ca | Các phép đo sau cần biết hai file có cùng nội dung byte hay không |
| `accuracy` | không | — | Chưa có hồ sơ chẩn đoán, xét nghiệm, hoặc người chẩn đoán độc lập |

### 3. Required dataset cases

| Case | Required | Condition | Reason |
|---|---|---|---|
| Một file ảnh trên đĩa có đúng một record trong `images.json` | có | file `.jpg`, `.jpeg`, `.png` trong `Test` hoặc `Validation` | Ca là file. File không có record là ca bị thiếu |
| Một record trỏ tới một file ảnh còn trên đĩa | có | mọi record | Record không có file là ca không tồn tại |

### Quantity

| Requirement | Threshold | Dependency |
|---|---:|---|
| | | |

Không mở. Chưa có quyết định nào buộc một số lượng tối thiểu. Bảng trống không bị chấm.

### 4. Missingness và allowed missing

| Value/state | Considered missing? | Allowed where | Reason |
|---|---|---|---|
| Trường bắt buộc không có trong record | có | không được phép | Record không giữ được ca |
| Trường bắt buộc là `null` hoặc chuỗi rỗng | có | không được phép | Có chìa khóa mà không có giá trị |
| `accuracy: null` | không | mọi record | Trường này không bắt buộc |
| `dataset_label` có dấu cách | không | nhãn thư mục đang mang dấu cách | Giá trị có mặt. Sai định dạng thuộc validity |
| Đuôi file không khớp chữ ký byte | không | file vẫn có record | File có mặt. Sai định dạng thuộc validity |

### 5. Exclusions

Những việc sau không bị gọi là thiếu:

- Bệnh ngoài vườn đúng hay sai.
- Mỗi mã trong taxonomy 11 nhãn đã có ảnh hay chưa. `yellow_leaf` chưa có map một-một sang hai nhãn con.
- Ảnh cây khỏe, ảnh rễ, ngày chụp, mã cây, mã vườn.
- Một split tên `Train`.
- `.DS_Store` và file không phải ảnh.
- Hai file cùng nội dung byte. Việc đó thuộc uniqueness và split independence.

### 6. Status

**Frozen.**

| Kết quả | Khi nào |
|---|---|
| PASS | Requirement đã đóng và đạt rule của requirement đó |
| FAIL | Requirement đã đóng và bị vi phạm |
| UNDETERMINED | Requirement đã đóng, dữ liệu hiện có không đủ để kết luận |
| BLOCKED | Requirement chưa được chấm vì còn phụ thuộc một quyết định chưa đóng |

## Kết quả

Nguồn: `completeness_checker.py`, đối chiếu file `.jpg`, `.jpeg`, `.png` trong `Test` và `Validation` với `image_key` trong `images.json`.

| Kiểm tra | Số | Kết quả |
|---|---:|---|
| File ảnh trong phạm vi | 1.297 | — |
| Record trong catalog | 1.297 | — |
| File không có record | 0 | PASS |
| Record không có file | 0 | PASS |
| `image_key` trùng nhau | 0 | PASS |
| Trường bắt buộc trống hoặc không có | 0 | PASS |
| `accuracy: null` | 1.297 | được phép, không tính thiếu |
| `.DS_Store` | 21 | ngoài phạm vi |
| Ảnh nằm ngoài `Test` và `Validation` | 0 | — |

| Requirement | Kết quả |
|---|---|
| 2. Required record fields | PASS |
| 3. Required dataset cases | PASS |
| Quantity | không mở |
| 4. Missingness | PASS |
| 5. Exclusions | đã áp dụng, không chấm |
| Cả phép đo | PASS |

Không có requirement nào ra FAIL, UNDETERMINED, hoặc BLOCKED trong phạm vi đã đóng.
