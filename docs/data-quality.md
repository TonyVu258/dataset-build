# Data quality — Cay-sau-rieng

Bản ghi này theo dõi bảy bài kiểm tra trước khi thư mục `images-test/Cay-sau-rieng` được gọi là một dataset.

Mỗi bài kiểm tra có ba phần:

1. **Điều kiện.** Thiếu điều kiện thì kết quả là *chưa kiểm được*, không phải đạt.
2. **Cách đo.**
3. **Quy tắc đạt.** Quy tắc phải được viết trước khi xem kết quả.

Code chỉ đo những gì có bằng chứng trong file và có quy tắc đã viết. Người, hoặc một nguồn bên ngoài, quyết định những gì file không chứa.

| # | Bài kiểm tra | Trạng thái |
|---|---|---|
| 1 | Accuracy | Chưa kiểm được |
| 2 | Completeness | Chưa làm |
| 3 | Consistency | Chưa làm |
| 4 | Timeliness | Chưa làm |
| 5 | Uniqueness | Chưa làm |
| 6 | Validity | Chưa làm |
| 7 | Split independence | Chưa làm |

## 1. Accuracy

Ảnh và nhãn có khớp với thực tế hay không.

Với bộ này, câu hỏi là: ảnh nằm trong một thư mục bệnh có đúng là bệnh đó hay không. Ảnh mở được không trả lời câu này.

### Điều kiện

Cần một nguồn sự thật nằm ngoài tên thư mục. Một trong hai nguồn sau là đủ để mở bài kiểm tra:

- Hồ sơ chẩn đoán gắn với từng ảnh, hoặc với từng đợt chụp.
- Một người biết bệnh cây gán lại nhãn trong khi không nhìn tên thư mục.

### Cách đo

1. Chọn sẵn số ảnh sẽ xem ở mỗi lớp, trước khi mở ảnh.
2. Người gán nhãn chỉ nhìn ảnh.
3. So nhãn đó với tên thư mục.
4. Tỷ lệ khớp là kết quả.

### Quy tắc đạt

Chưa đặt. Ngưỡng phải được viết trước khi xem ảnh. Ví dụ để thảo luận, chưa phải quy tắc đã chốt: khớp từ 95% số ảnh được xem trở lên.

### Kết quả

**Chưa kiểm được.** Chưa có hồ sơ chẩn đoán và chưa có lần gán nhãn độc lập.

### Cần bổ sung

- [ ] Nguồn sự thật là hồ sơ, là người, hay cả hai?
- [ ] Nếu là người: ai gán nhãn, và người đó có được nhìn tên thư mục hay không?
- [ ] Mỗi lớp sẽ xem bao nhiêu ảnh?
- [ ] Ngưỡng đạt là bao nhiêu phần trăm?

## 2. Completeness

Chưa làm.

## 3. Consistency

Chưa làm.

## 4. Timeliness

Chưa làm.

## 5. Uniqueness

Chưa làm.

## 6. Validity

Chưa làm.

## 7. Split independence

Chưa làm.
