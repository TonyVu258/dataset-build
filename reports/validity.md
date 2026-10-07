# Validity

Dataset: `images-test/Cay-sau-rieng`

Trạng thái phép đo: **không đạt**

Specification: **Frozen**

Requirement 1 đến 4 đã đóng. Kết quả do `validity_checker.py` ghi. Không sửa requirement sau kết quả này.

## Why

Một giá trị có thể có mặt, và vẫn sai quy tắc định dạng đã viết. Validity trả lời giá trị đó có theo rule kỹ thuật hay không. Nó không trả lời giá trị có đúng với bệnh ngoài vườn hay không. Câu đó thuộc accuracy.

> File và mã nhãn có thuộc allow list, và có đúng dạng trong allow list, hay không?

## Requirement

| # | Requirement | Rule |
|---|---|---|
| 1 | Đuôi file khớp chữ ký | Đuôi file nằm trong allow list đuôi, và byte đầu khớp chữ ký của đuôi đó |
| 2 | Mã nhãn đúng ký tự | `dataset_label` chỉ gồm chữ thường, chữ số và `_` |
| 3 | Khung file có đủ phần kết | PNG kết thúc bằng `IEND`. JPEG kết thúc bằng `FF D9` |
| 4 | Nhãn thuộc allow list | `dataset_label` là một chuỗi trong allow list nhãn |
| 5 | Kích thước và số kênh | Không mở |
| 6 | Tên file | Không mở |

Giải mã từng điểm ảnh chưa phải requirement. Policy tên file tạm thời không mở.

Không mở requirement về kích thước và số kênh. Dataset chưa có model-input contract quy định các giá trị này. `width >= 224`, `height >= 224`, hay `channels = 3` chỉ trở thành requirement khi contract đó được viết và Frozen. Tên file chứa `224x224` không phải contract, và không được dùng để suy ra requirement.

Requirement 4 dùng allow list nhãn ở dưới. Danh sách đó là tên thư mục được phép lưu trong `dataset_label`. Mười một mã taxonomy trong `taxonomy-agreement.md` không phải allow list này. Catalog vẫn giữ tên thư mục. Map từ tên thư mục sang mã taxonomy là việc của taxonomy agreement.

## Allow list

### Đuôi file và chữ ký

| Đuôi | Chữ ký byte đầu |
|---|---|
| `.png` | `89 50 4E 47 0D 0A 1A 0A` |
| `.jpg` | `FF D8` |
| `.jpeg` | `FF D8` |

Đuôi không có trong bảng thì không được phép. Đuôi có trong bảng nhưng byte đầu khác chữ ký của dòng đó thì không đạt requirement 1.

### Ký tự của `dataset_label`

Được phép: `a-z`, `0-9`, `_`.

Không được phép: dấu cách, chữ hoa, và ký tự khác.

### Giá trị `dataset_label`

| Được phép |
|---|
| `anthracnose_disease` |
| `canker_disease` |
| `fruit_rot` |
| `mealybug_infestation` |
| `pink_disease` |
| `sooty_mold` |
| `stem_blight` |
| `thrips_disease` |
| `yellow_leaf` |

`stem_cracking_ gummosis` không có trong allow list. Chuỗi đó có dấu cách, nên cũng không đạt requirement 2.

Các mã sau không thuộc allow list của `dataset_label`. Chúng là mã taxonomy, không phải tên thư mục đang lưu: `phytophthora_canker`, `phytophthora_fruit_rot`, `stem_blight_rhizoctonia`, `stem_gummosis_severe`, `thrips_damage`, `yellow_leaf_nutrient`, `yellow_leaf_root_rot`.

## Quan sát đã có, chưa phải kết quả

17 file trong `Validation/fruit_rot` khai `.png` nhưng là JPEG, từ `2000.png` đến `2018.png`, trừ `2002.png` và `2016.png`.

Một nhãn không có trong allow list, trên 136 ảnh: `stem_cracking_ gummosis`. `Test` và `Validation` cùng chuỗi này. Hai phía khớp nhau, nên đây không phải lỗi consistency. Ảnh không vì dấu cách mà sai bệnh.

1.297 file đều đủ phần kết, kể cả 17 file đuôi không khớp chữ ký. Đủ khung không có nghĩa đuôi file đúng.

## Kết quả

Nguồn: `validity_checker.py`. Chấm requirement 1 đến 4. Kích thước, số kênh và tên file không mở.

| Kiểm tra | Số | Kết quả |
|---|---:|---|
| Record trong catalog | 1.297 | — |
| File không còn trên đĩa | 0 | — |
| Đuôi không khớp chữ ký | 17 | FAIL |
| Không nhận ra chữ ký | 0 | PASS |
| Khung thiếu phần kết | 0 | PASS |
| `dataset_label` sai ký tự | 136 | FAIL |
| `dataset_label` ngoài allow list | 136 | FAIL |

| Requirement | Kết quả |
|---|---|
| 1. Đuôi file khớp chữ ký | FAIL |
| 2. Mã nhãn đúng ký tự | FAIL |
| 3. Khung file có đủ phần kết | PASS |
| 4. Nhãn thuộc allow list | FAIL |
| 5. Kích thước và số kênh | không mở |
| 6. Tên file | không mở |

Cả phép đo: FAIL.

Có requirement không đạt. Các ví dụ nằm trong `validity.json`.
Đủ phần kết không có nghĩa đuôi file đúng. Tên file và kích thước không được chấm.
