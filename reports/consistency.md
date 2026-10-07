# Consistency

Dataset: `images-test/Cay-sau-rieng`

Trạng thái phép đo: **đạt**

Specification: **Frozen**

Requirement đã đóng. Kết quả do `consistency_checker.py` ghi. Không sửa requirement sau kết quả này.

## Why

Một dataset có thể đủ trường, đúng định dạng, và vẫn dùng hai cách viết cho cùng một việc, hoặc gán hai nhãn mà rule cấm đứng cùng nhau.

Consistency trả lời:

> Các giá trị và mối quan hệ trong dataset có theo cùng một rule, và không mâu thuẫn với nhau, hay không?

Khác biệt vừa nhìn thấy chưa phải mâu thuẫn. Hai chuỗi khác nhau chỉ là mâu thuẫn khi rule nói chúng phải giống nhau. Hai nhãn trên cùng một nội dung chỉ là mâu thuẫn khi rule cấm cặp đó.

```text
Requirement / Rule
        ↓
Actual data
        ↓
Comparison
        ↓
Result
```

## Requirement

Requirement lấy từ hai loại consistency ở trên. Bản này đã Frozen.

| # | Requirement | Rule |
|---|---|---|
| 1 | Chuỗi nhãn thư mục dùng chung | Tập chuỗi `dataset_label` ở `Test` và tập ở `Validation` khớp từng ký tự |
| 2 | Cặp nhãn trên cùng một nội dung byte | Nếu một `content_hash` có từ hai `dataset_label`, map sang taxonomy rồi chỉ coi là mâu thuẫn khi cặp đó bị cấm |
| 3 | Ngoài phạm vi | Tên file, từ đồng nghĩa chưa có, và cùng nội dung ở hai split với cùng một nhãn không phải requirement của consistency |

### 1. Chuỗi nhãn thư mục dùng chung

| | |
|---|---|
| Rule | Tập chuỗi `dataset_label` ở `Test` và tập ở `Validation` khớp từng ký tự |
| Population | Mọi record trong `images.json` |
| Vi phạm | Một chuỗi có ở split này và không có ở split kia |
| Không vi phạm | Cả hai split cùng mang một chuỗi, kể cả `stem_cracking_ gummosis` |
| Dependency | Không. Dấu cách trong chuỗi thuộc validity |

### 2. Cặp nhãn trên cùng một nội dung byte

| | |
|---|---|
| Rule | Nếu một `content_hash` có từ hai `dataset_label`, cặp đó phải được phép cùng xuất hiện |
| Population | Các record trong `images.json` nhóm theo `content_hash` |
| Map | Tên thư mục sang mã taxonomy theo bảng map trong `taxonomy-agreement.md`, rồi xét theo bảng nhãn được cùng xuất hiện ở file đó |
| Vi phạm | Cặp map tới hai mã mà bảng cấm đứng cùng nhau |
| Không vi phạm | Cặp được bảng cho phép cùng gán. `sooty_mold` với `mealybug_infestation` là một cặp như vậy |
| Chưa đủ để FAIL | Hai tên thư mục cùng một hash mà bảng chỉ cho phép khi ảnh có đủ bằng chứng. Thư mục không ghi bằng chứng |
| Không xét bằng tên thư mục | Cặp có `yellow_leaf`, vì tên này không có map một-một. `yellow_leaf_nutrient` và `yellow_leaf_root_rot` không phải tên thư mục |
| Một hash, một `dataset_label` | Không tạo cặp. Thư mục im về các nhãn khác, và im lặng không có nghĩa ảnh chỉ có một bệnh |
| Dependency | Bảng map và bảng cùng xuất hiện trong `taxonomy-agreement.md` |

Cặp bị cấm trong bảng taxonomy là `yellow_leaf_nutrient` và `yellow_leaf_root_rot` cho cùng một kiểu vàng lá. Các cặp được ghi là có thể cùng gán: `sooty_mold` với `mealybug_infestation`, `sooty_mold` với `thrips_damage`, `phytophthora_canker` với `phytophthora_fruit_rot`, và `phytophthora_canker` với `stem_gummosis_severe` khi đủ hai kiểu bằng chứng.

### 3. Ngoài phạm vi

| Quan sát | Requirement |
|---|---|
| 97 tên file trỏ tới các nội dung byte khác nhau và nhiều thư mục bệnh | Không. Danh tính một ca là `image_key`. Tên file là tên cục bộ. Chỉ thành lỗi khi một specification nói tên file là định danh duy nhất |
| `healthy` và `normal` | Không mở. Bộ này không có hai chuỗi đó, và chưa có bảng đồng nghĩa |
| Cùng nội dung byte ở cả `Test` và `Validation` với cùng một nhãn | Không. Hai lời gán nhãn giống nhau. Cùng nội dung nằm ở hai split thuộc uniqueness và split independence |

## Kết quả

Nguồn: `consistency_checker.py`. Status đã Frozen. official_result là kết quả của hai requirement.

| Quan sát | Số |
|---|---|
| Nội dung byte đứng trong hơn một thư mục bệnh | 0 |
| Tên file trỏ tới nhiều nội dung và nhiều thư mục bệnh, ngoài requirement | 97 |
| Chuỗi nhãn thư mục giữa `Test` và `Validation` | khớp từng ký tự. 10 chuỗi dùng chung |

| Requirement | Đối chiếu máy | Kết quả chính thức |
|---|---|---|
| 1. Chuỗi nhãn thư mục dùng chung | đã đếm | PASS |
| 2. Cặp nhãn trên cùng một nội dung byte | đã đếm | PASS |

Tên file không được chấm. Một hash chỉ có một `dataset_label` không tạo cặp.

## Status

**Frozen.**

| Kết quả | Khi nào |
|---|---|
| PASS | Requirement đã đóng và không có vi phạm theo rule của requirement đó |
| FAIL | Requirement đã đóng và có một vi phạm |
| UNDETERMINED | Requirement đã đóng, dữ liệu hiện có không đủ để kết luận |
| BLOCKED | Requirement chưa được chấm vì bảng map hoặc bảng cùng xuất hiện chưa dùng được cho cặp đang xét |

Đã Frozen. Không sửa requirement sau khi checker ghi kết quả.
