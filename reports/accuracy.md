# Accuracy

Dataset: `images-test/Cay-sau-rieng`

Trạng thái: **chưa kiểm được**

## Câu hỏi

Ảnh nằm trong một thư mục bệnh có đúng là bệnh đó hay không?

## Label taxonomy

Mười nhãn dưới đây là tên thư mục hiện có. Accuracy so sánh ảnh với cột ground truth, không so với tên tiếng Anh. Một ảnh trong thư mục này chỉ đứng ở một nhãn. Nếu một ảnh được phép mang hai bệnh, taxonomy này chưa ghi điều đó.

| Nhãn | Tên thư mục, giữ nguyên ký tự | Ground truth: ảnh được gán nhãn này khi nào | Không gán nhãn này khi |
|---|---|---|---|
| `anthracnose_disease` | `anthracnose_disease` | | |
| `canker_disease` | `canker_disease` | | |
| `fruit_rot` | `fruit_rot` | | |
| `mealybug_infestation` | `mealybug_infestation` | | |
| `pink_disease` | `pink_disease` | | |
| `sooty_mold` | `sooty_mold` | | |
| `stem_blight` | `stem_blight` | | |
| `stem_cracking_gummosis` | `stem_cracking_ gummosis` | | |
| `thrips_disease` | `thrips_disease` | | |
| `yellow_leaf` | `yellow_leaf` | | |

`stem_cracking_gummosis` là mã nhãn đề xuất, không có dấu cách. Tên thư mục thật có một dấu cách sau dấu gạch dưới. Hai chuỗi này chưa được coi là một cho đến khi ground truth nói chúng là cùng một nhãn.

## Điều kiện

- [ ] Có nguồn sự thật nằm ngoài tên thư mục.

Cần hồ sơ chẩn đoán gắn với ảnh, hoặc một người biết bệnh cây gán lại nhãn khi không nhìn tên thư mục.

## Cách đo

1. Chọn số ảnh sẽ xem ở mỗi lớp trước khi mở ảnh.
2. Người gán nhãn chỉ nhìn ảnh.
3. So nhãn đó với tên thư mục.
4. Tỷ lệ khớp là kết quả.

## Quy tắc đạt

Chưa đặt. Ngưỡng phải được chốt trước khi xem ảnh.

## Kết quả

Chưa có.

## Cần bổ sung

- [ ] Điền hai cột ground truth trong label taxonomy cho đủ mười nhãn.
- [ ] Một ảnh có được mang hai nhãn hay không?
- [ ] Nguồn sự thật là hồ sơ, là người, hay cả hai?
- [ ] Nếu là người: ai gán nhãn, và người đó có được nhìn tên thư mục hay không?
- [ ] Mỗi lớp sẽ xem bao nhiêu ảnh?
- [ ] Ngưỡng đạt là bao nhiêu phần trăm?
