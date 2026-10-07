# Uniqueness

Dataset: `images-test/Cay-sau-rieng`

Trạng thái phép đo: **không đạt ở byte**

Specification: **Frozen**

Bốn requirement dưới đây là bộ đã đóng. Không thêm requirement. Không sửa bộ này sau khi đã thấy số đếm để làm phép đo thành đạt. Không làm checker. Không có kết quả chính thức. Trạng thái **không đạt** ở bản trước được gỡ.

Scope của byte đã chọn: từng split. Trong lúc test, cùng một byte được phép đứng ở cả `Test` và `Validation`. Bản trùng đó không tính là vi phạm uniqueness. `split_independence.md` vẫn ghi việc một hình nằm ở cả hai sample. Scene chưa mở vì chưa có policy về scene identity. Data không có `tree_id`, nên uniqueness theo cây không xét được. Hiện chỉ byte kiểm được.

## Why

Một dataset có thể đủ record và nhất quán, nhưng cùng một sự vật vẫn bị ghi nhiều lần. Lần ghi thừa làm bộ đếm nhiều ca hơn số sự vật thực có.

Uniqueness trả lời:

> Một sự vật có bị ghi nhiều hơn một lần trong scope đã chọn hay không?

Sự vật có thể là một nội dung byte, một cảnh, hoặc một cây. Ba lớp này không thay cho nhau.

Bản trùng nằm ở cả `Test` và `Validation` là scope toàn dataset. Byte đang cho phép trường hợp đó để test rule trong từng split trước. Uniqueness không chấm nó. `split_independence.md` vẫn là nơi ghi một hình có đứng trong cả hai sample hay không.

## Requirement

| # | Requirement | Rule đã đóng |
|---|---|---|
| 1 | Byte | Cùng một nội dung byte có bị ghi nhiều hơn một lần trong scope của rule này hay không |
| 2 | Scene | Chưa mở. Chưa có policy nói hai ảnh nào là cùng một cảnh |
| 3 | Tree | Cùng một cây có bị ghi nhiều hơn một lần trong scope của rule này hay không |
| 4 | Scope trong từng rule | Rule 1, 2 và 3 mỗi rule ghi scope của chính nó: toàn dataset, hoặc từng split |

Requirement 4 là điều kiện của rule 1–3. Không có dòng Scope thì rule đó chưa đủ để chấm.

### 1. Byte

Một nội dung byte là một giá trị `content_hash`. Completeness đã lấy một ca là một file, nên hai file cùng hash vẫn là hai record. Rule này hỏi hai record đó có phải một sự vật bị ghi thừa hay không.

| | |
|---|---|
| Scope | Từng split |
| Trùng giữa `Test` và `Validation` | Được phép trong lúc test. Không phải vi phạm uniqueness |
| Cấm bản trùng trong một split | Có |
| Chấm | FAIL |

Số 166 ở mục quan sát đếm trên cả dataset. Số vi phạm trong một split nằm ở mục Kết quả.

### 2. Scene

Scene identity là policy. pHash và visual embedding không quyết định hai ảnh có cùng cảnh hay không. Chúng chỉ được dùng sau khi policy đã viết, và chỉ để lập cặp nghi ngờ.

Ví dụ một policy có thể nói: hai ảnh là cùng scene khi chúng mô tả cùng một bố cục thực tế, và thay đổi không làm mất identity của cảnh, như resize, nén lại, hoặc crop nhỏ. Crop sang một vùng hoàn toàn khác là scene mới. Ví dụ này chưa phải policy của bộ này.

Requirement scene chưa mở. Chưa trả lời được các câu sau:

- Scene là gì?
- Thay đổi nào vẫn là cùng scene?
- Thay đổi nào tạo scene mới?
- Dùng pHash hay embedding để tạo candidate?
- Threshold bao nhiêu?
- Human reviewer quyết định theo rule nào?

Flow sau chỉ là thứ tự làm việc khi các câu trên đã có lời. Hiện chưa chạy.

```text
                ┌── SHA-256
                │
Images ─────────┼── pHash
                │
                └── Visual embedding
                         ↓
                  Candidate pairs
                         ↓
                  Human verification
                         ↓
              Confirmed scene groups
```

| | |
|---|---|
| Scope | Chưa mở. Nếu mở, scope đã bàn là từng split, và trùng giữa hai split được phép trong lúc test |
| Áp dụng | Không. Chưa có policy scene identity |
| Chấm | Không mở |

### 3. Tree

Nếu rule là một cây chỉ xuất hiện một lần trong dataset, scope là `Test` và `Validation` cùng nhau. `Tree-001` có ảnh ở cả hai split thì FAIL. Bộ này không dùng rule đó.

Một ca đã khóa ở completeness là một file. Nhiều ảnh của một cây, như lá, quả và thân, là nhiều ca. Cùng một cây ở cả hai split là câu của `split_independence.md`: mọi ảnh của cây phải nằm trong một tập. Câu đó vẫn chưa kiểm được vì không có `tree_id`.

Nếu bộ này dùng để train một vision model nhận diện bệnh, nhiều ảnh của cùng một cây không nhất thiết là bản trùng. Chúng chỉ thành vấn đề khi sample phải độc lập ở mức cây.

```text
Tree A
  ├── leaf 1
  ├── leaf 2
  └── leaf 3
```

Ba ảnh này có thể là ba quan sát khác nhau. Nếu muốn đánh giá model trên cây chưa từng xuất hiện lúc train, danh tính cây trở thành việc của split design, tức group split: mọi ảnh của một cây nằm trong một tập. Đó không phải uniqueness.

Data không có `tree_id`. Không có mã cây thì không biết hai ảnh có cùng một cây hay không, dù scope là từng split hay toàn dataset. Uniqueness theo cây không xét được.

| | |
|---|---|
| Scope | Không xét được. Mọi scope đều cần `tree_id` |
| Áp dụng | Không xét được |
| Chấm | Không xét được |

### 4. Scope trong từng rule

Mỗi rule 1–3 phải ghi một trong hai scope: toàn dataset, hoặc từng split. Scope của rule này không suy ra từ rule kia.

| | |
|---|---|
| Byte | Từng split |
| Scene | Chưa mở. Chưa có policy scene identity |
| Tree | Không xét được. Không có `tree_id` |
| Chấm | Byte đã có scope. Scene chưa mở nên không có scope để chấm |

## Quan sát đã có, chưa phải kết quả

| Quan sát | Số |
|---|---|
| File ảnh | 1.297 |
| Nội dung byte khác nhau | 1.105 |
| Nội dung bị lưu nhiều hơn một lần | 166 |
| Trong đó khác tên file | 49 |

## Kết quả

Nguồn: `uniqueness_checker.py`. Chỉ chấm byte. Scene không mở. Tree không xét được.

Rule: trong một split, một `content_hash` chỉ xuất hiện một lần. Cùng hash ở cả `Test` và `Validation` được phép.

| Kiểm tra | Số | Kết quả |
|---|---:|---|
| Record trong catalog | 1.297 | — |
| Hash có ở cả `Test` và `Validation` | 158 | được phép, không tính vi phạm |
| Hash lặp trong `Test` | 15 | FAIL |
| Hash lặp trong `Validation` | 15 | FAIL |

| Requirement | Kết quả |
|---|---|
| 1. Byte | FAIL |
| 2. Scene | không mở |
| 3. Tree | không xét được |

Có hash lặp trong một split. Các ví dụ nằm trong `uniqueness.json`.
