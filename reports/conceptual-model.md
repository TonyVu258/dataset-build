# Conceptual Data Model

**Dataset:** `Cay-sau-rieng`  
**Ngày:** 2026-10-09  
**Trạng thái:** Draft

Mô hình này nói các khái niệm của dataset là gì và chúng quan hệ với nhau thế nào. Nó không cấp UUID, không đổi `images.json`, và không thiết kế bảng vật lý.

## Thực thể

| Thực thể | Là gì | Danh tính | Không phải |
|---|---|---|---|
| Image artifact | Một file đã được đưa vào catalog | Một ID ổn định, cấp một lần. Hai file cùng byte là hai artifact | Đường dẫn, hash, một cảnh, một cây, một mẫu bệnh |
| Locator | Chỗ đang tìm thấy byte của artifact | Đường dẫn tương đối từ gốc lab `images-test/` | Danh tính của artifact |
| Source label | Nhãn gốc từ tên thư mục lúc lập catalog | Giá trị chuỗi gốc, gắn với một artifact | Taxonomy code, nhãn đã chuẩn hóa, chẩn đoán |
| Source split | Phân vùng gốc `Test` hoặc `Validation` | Giá trị gốc gắn với một artifact | Split dùng để huấn luyện sau này |
| Content fingerprint | SHA-256 của byte tại một thời điểm | Giá trị hash của một phiên bản nội dung | Danh tính artifact. Cùng hash vẫn có thể là hai artifact |
| Baseline version | Một fingerprint đã được chọn làm mốc, có phiên bản và lý do | Số phiên bản của mốc đó | Một lần quét tùy ý |
| Hash observation | Kết quả một lần quét byte sau mốc | Một lần quét | Bản ghi đè lên baseline |
| Annotation | Một lần đánh giá độc lập | ID của lần đánh giá | Ground truth. Nhãn thư mục |
| Plant-part description | Bộ phận cây mà ảnh thể hiện | Chưa chọn: một bộ phận chính, hay một tập bộ phận | Suy ra từ tên thư mục bệnh |
| Capture time | Thời điểm máy ảnh ghi lúc chụp | Chưa chọn độ chính xác và nguồn | Thời điểm tạo hoặc sửa file |

`plant-part description` và `capture time` có mặt trong mô hình vì đó là khái niệm của dataset. Cách biểu diễn chưa được chọn. Chưa có giá trị không có nghĩa là khái niệm đã được định nghĩa xong.

## Quan hệ

| Từ | Quan hệ | Đến | Số lượng |
|---|---|---|---|
| Image artifact | đang nằm ở | Locator hiện tại | 1 hiện tại, nhiều locator trong lịch sử |
| Image artifact | mang | Source label | đúng 1, không ghi đè |
| Image artifact | thuộc | Source split | đúng 1 split gốc |
| Image artifact | có fingerprint lúc tạo catalog | Content fingerprint | đúng 1 |
| Image artifact | được khóa bởi | Baseline version | nhiều phiên bản theo thời gian; phiên bản mới không sửa phiên bản cũ |
| Image artifact | được quét thành | Hash observation | 0 hoặc nhiều |
| Image artifact | được đánh giá bởi | Annotation | 0 hoặc nhiều |
| Annotation | đưa ra | Nhãn người đánh giá | 1 lần đánh giá có thể có nhiều nhãn |
| Source label | có thể được ánh xạ sang | Taxonomy code | quan hệ riêng, không thay nhãn gốc |
| Annotation | có thể được chấp nhận làm | Ground truth cho một mục đích | chỉ khi mục đích đó đã có quy trình, bằng chứng và tiêu chí |

Hai image artifact được phép cùng một content fingerprint. Đó vẫn là hai thực thể, hai ID.

Một image artifact được phép đổi byte. ID không đổi. Fingerprint của phiên bản mới là một hash observation hoặc một baseline version mới.

## Danh tính và truy nguyên

ID của image artifact không được tạo từ hash và không được tạo từ đường dẫn. Cấp một lần. Tạo lại catalog phải tìm lại ID cũ. Chỉ cấp ID mới khi không còn cách khôi phục đáng tin cậy, và lần đó phải ghi rằng danh tính bị gián đoạn.

Đường dẫn mà các phép đo hiện tại đang dùng là locator, đồng thời là giá trị ID đang lưu tạm. Khi ID ổn định được cấp, locator đó phải còn lại như locator lịch sử. Phép đo cũ nối với artifact bằng locator đã lưu, không bằng cách suy ID từ tên file hoặc từ hash.

Source label và source split là lời của dataset nguồn. Chuẩn hóa, taxonomy và split huấn luyện là khái niệm khác, đứng cạnh lời gốc.

## Ngoài mô hình này

`reports/json/images-test.json` là dữ liệu ví dụ để thử cách ghi. Nó không phải một thực thể của dataset.

File JSON, registry và script migration là cách lưu sau này. Chúng không thêm khái niệm mới vào mô hình.
