# Semantic Layer và Metadata Specification

**Dataset:** `Cay-sau-rieng`  
**Catalog:** `images-test/reports/json/images.json`  
**Ngày:** 2026-10-09

## Trạng thái

| Phần | Trạng thái |
|---|---|
| Quyết định metadata cốt lõi ở mục 1 | **Frozen** |
| Schema chi tiết của `plant_part` và `capture_time` | **Draft** |
| Khớp fingerprint đã lưu với file trên đĩa | **Đã xác minh.** 1.297 file khớp `content_hash` |
| `baseline_content_hash` trong catalog | **Đã ghi** bằng `content_hash` vì file hiện tại khớp |
| Migration `image_key` sang UUID | **Chưa thực hiện** |

Completeness đã Frozen ngày 2026-10-07 với `image_key` nghĩa là đường dẫn. Phép đo đó không bị viết lại bởi bản này.

## 1. Quyết định đã Frozen

| Hạng mục | Quyết định |
|---|---|
| `image_key` | UUID được cấp một lần, lưu trong registry; không tạo từ hash hoặc đường dẫn |
| Danh tính record | Hai file cùng byte ở hai split vẫn là hai record, mỗi record có ID riêng |
| Nội dung file thay đổi | Giữ nguyên `image_key`; ghi nhận fingerprint mới riêng |
| `relative_path` | Vị trí file. Phải bảo toàn đường dẫn hiện tại trước khi thay ID đang nhúng đường dẫn bằng UUID |
| `dataset_label` | Giữ nguyên nhãn nguồn, không sửa tại chỗ |
| `source_split` | Giữ nguyên split nguồn. Split mới phải được biểu diễn riêng |
| `content_hash` | Fingerprint SHA-256 được ghi tại thời điểm tạo catalog. Hash lần quét sau là quan sát mới |
| `accuracy` | Giữ field hiện tại. Assessment mới không ghi vào field này |
| Annotation | Một `image_key` có thể liên kết với nhiều annotation record. Record mới không ghi đè record cũ |
| Ground truth | Annotation không mặc nhiên là ground truth |
| `null` | Chỉ có nghĩa chưa ghi nhận giá trị. Không tự biểu thị lý do hoặc trạng thái quy trình |

### Registry

UUID được cấp một lần và lưu trong registry bền vững. Nơi dự kiến của registry: `images-test/reports/json/catalog-registry.json`. File này chưa được tạo.

Khi tạo lại catalog, phải tra registry để dùng lại ID cũ nếu xác định được record tương ứng. Ưu tiên phục hồi ID từ backup hoặc từ một nguồn ánh xạ đáng tin cậy. Mất registry không mặc định là mất ID vĩnh viễn. Chỉ cấp ID mới khi không thể khôi phục danh tính một cách đáng tin cậy, và lần cấp đó phải ghi nhận sự gián đoạn danh tính.

ID không được tạo bằng hash nội dung file và không được tạo bằng đường dẫn.

### Gốc của `relative_path`

Đường dẫn tương đối được tính từ thư mục lab `images-test/`, tức thư mục chứa `Cay-sau-rieng/`. Chuỗi không chứa ổ đĩa và không phải đường dẫn tuyệt đối của hệ điều hành. Dấu phân cách là `/`.

Ví dụ: `Cay-sau-rieng/Test/anthracnose_disease/00163.png`.

Cùng một chuỗi này luôn trỏ tới cùng vị trí trong lab, dù máy đang dùng ổ đĩa nào.

## 2. Ba điểm còn mở

`plant_part` và `capture_time` đang là `null` trên mọi record. `null` nghĩa là chưa có giá trị hoặc chưa triển khai. Đặt `null` không làm xong ý nghĩa của trường. `baseline_content_hash` đã được ghi sau khi file khớp `content_hash`.

| Trường | `null` đang nói gì | Ý nghĩa chưa chốt |
|---|---|---|
| `baseline_content_hash` | Đã ghi sau khi file hiện tại khớp `content_hash` | Không còn là `null`. Ý nghĩa “fingerprint lúc tạo catalog, đã đối chiếu” được xác nhận bởi lần tính lại này |
| `plant_part` | Chưa triển khai schema và chưa có giá trị | Bộ phận chính hay tập bộ phận trong ảnh |
| `capture_time` | Chưa triển khai schema và chưa có giá trị | Ngày hay timestamp có giờ, và nguồn nào được chấp nhận |

### A. Baseline của `content_hash`

`content_hash` đã Frozen với nghĩa fingerprint lúc tạo catalog. Bản sao các giá trị đó nằm ở `reports/json/content-hash-baseline-v1.json`, phiên bản 1.

Đã tính lại SHA-256 trên file hiện tại. 1.297 file khớp `content_hash`, 0 lệch, 0 thiếu file. Với mỗi record khớp, `baseline_content_hash` trong `images.json` được gán bằng `content_hash`. `content_hash` không bị ghi đè. Kết quả nằm ở `reports/json/content-hash-verification.json`.

Hash của một lần quét sau là quan sát mới, không ghi đè phiên bản 1. Đổi baseline chỉ được làm bằng một phiên bản baseline mới có lịch sử. Lệch hash, nếu xuất hiện sau này, chứng minh byte khác baseline và chưa tự kết luận là thay đổi trái phép.

### B. `plant_part`

Schema chưa Frozen. Không suy giá trị từ tên thư mục. Ví dụ cách đặt `null` khi schema chưa triển khai nằm trong `reports/json/images-test.json`, không nằm trong catalog thật.

### C. `capture_time`

Schema chưa Frozen. Không lấy thời điểm sửa file. Cùng file test ở trên.

## 3. Danh tính trước khi migration

Bước này không cấp UUID và không đổi `image_key`. Quan hệ và cách giữ dấu vết nằm ở `reports/conceptual-model.md`.

Cho đến khi migration chạy, `image_key` và `relative_path` cùng là đường dẫn từ gốc `images-test/`. Các phép đo đã Frozen vẫn nối được record với file bằng chuỗi đó.

## 4. Chưa thực hiện

- Chưa cấp UUID và chưa ghi registry.
- Chưa có annotation record.

## Kết quả

Nguồn: `catalog_schema_checker.py`. Không cấp UUID. Không tính lại SHA-256.

| Việc ghi catalog | Số record được thêm khóa |
|---|---:|
| `relative_path` chép từ `image_key` | 0 |
| `baseline_content_hash: null` | 0 |
| `plant_part: null` | 0 |
| `capture_time: null` | 0 |

| Kiểm tra phần Frozen | Số | Kết quả |
|---|---:|---|
| Record | 1.297 | — |
| `image_key` trùng | 0 | PASS |
| `relative_path` trùng đường dẫn hiện tại, gốc `images-test/` | 1.297 | PASS |
| `dataset_label` trùng tên thư mục | 1.297 | PASS |
| `source_split` trùng thư mục split | 1.297 | PASS |
| `content_hash` là SHA-256 hex | 1.297 | PASS |
| `accuracy` là `null` | 1.297 | PASS |
| `image_key` đã là UUID | 0 | chưa thực hiện |

| Baseline và field chưa triển khai | Số | Kết quả |
|---|---:|---|
| `baseline_content_hash` còn `null` | 0 | không có |
| `baseline_content_hash` đã khóa | 1.297 | bằng `content_hash` sau khi file khớp |
| `plant_part` | 1.297 | Draft. `null` là chưa triển khai, không phải đã chốt nghĩa |
| `capture_time` | 1.297 | Draft. `null` là chưa triển khai, không phải đã chốt nghĩa |

Phần Frozen kiểm được trên catalog hiện tại: PASS.

Migration UUID và registry chưa chạy. Đối chiếu SHA-256 nằm ở `content-hash-verification.json`.
