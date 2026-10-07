# Taxonomy Agreement

Dataset: `images-test/Cay-sau-rieng`

Trạng thái: **quy tắc đã đóng, chưa review**

Tên phép đo: **Independent Label Agreement**. Không gọi kết quả này là accuracy của dataset. Một người xem làm theo taxonomy này chỉ cho biết nhãn thư mục có khớp cách người đó đọc bảng hay không. Phép đo không chứng minh nhãn đúng với bệnh ngoài vườn.

Accuracy theo nghĩa đúng với thực tế nằm ở `accuracy.md` và chưa làm được.

## 1. Chính sách nhãn

Một ảnh được phép mang nhiều nhãn.

Thư mục cũ chỉ khẳng định một nhãn và im lặng về các nhãn khác. Người xem có thể gán thêm nhãn mà thư mục không ghi. Nhãn thêm không biến lời thư mục thành `MISMATCH`.

`UNDETERMINED` không phải một nhãn. Đó là lựa chọn của người xem khi ảnh không đủ bằng chứng để gán nhãn đang xét.

`UNSCORED` không phải một nhãn. Đó là kết quả của hệ thống khi tên thư mục cũ không có map một-một sang taxonomy này.

## 2. Taxonomy

| Mã nhãn | Vùng | Gán khi ảnh cho thấy | Không gán khi |
|---|---|---|---|
| `anthracnose_disease` | Lá hoặc quả | Đốm hoại tử đồng tâm, có quầng vàng. | Chỉ thấy vàng lá hoặc lớp muội, không có đốm hoại tử. |
| `phytophthora_canker` | Thân hoặc cành lớn | Vỏ gốc tối, sũng nước, hoặc gỗ mạch nâu khi vỏ bị cạo. | Chỉ có quả thối, không có thân trong khung hình. |
| `phytophthora_fruit_rot` | Quả | Vết thối úng nước, có thể có tơ trắng. | Chỉ có vết trên thân, không có quả. |
| `mealybug_infestation` | Quả, cuống hoặc lá | Cụm bông trắng trong khe gai hoặc nách lá. | Chỉ có lớp muội đen, không thấy cụm bông. |
| `pink_disease` | Cành hoặc nhánh | Lớp váng hồng, hoặc bột phấn hồng trên vỏ cành. | Chỉ có mủ hổ phách, không có bột hồng. |
| `sooty_mold` | Bề mặt lá hoặc quả | Màng đen như bồ hóng, bám bề mặt. | Vết đen nằm trong mô, không phải lớp phủ bề mặt. |
| `stem_blight_rhizoctonia` | Cành non hoặc lá | Lá táp và dính nhau bằng sợi tơ, hoặc cành non khô mục. | Chỉ có một đốm nhỏ trên lá già, không có tơ hoặc chết cành non. |
| `stem_gummosis_severe` | Thân hoặc vỏ gỗ | Nứt dọc sâu kèm mủ đặc màu hổ phách hoặc đỏ. | Chỉ có vỏ sũng nước mà không có nứt dọc và mủ đặc. |
| `thrips_damage` | Lá non hoặc đọt | Lá non quăn, mép cong, hoặc vệt mất màu vạn hoa ở mặt dưới. | Chỉ có đốm hoại tử trên lá già. |
| `yellow_leaf_nutrient` | Tán lá | Vàng theo quy luật: gân xanh lá vàng, hoặc vàng từ mép. | Vàng xỉn kèm héo rũ và rụng loạt. |
| `yellow_leaf_root_rot` | Tán lá, và cần dấu hiệu rễ hoặc suy cả cây | Lá vàng xỉn, héo rũ, rụng loạt, cây suy kiệt. | Chỉ có vàng theo quy luật dinh dưỡng, không có héo rũ hoặc rụng loạt. |

`yellow_leaf_root_rot` không được gán chỉ vì tán lá vàng. Ảnh không có dấu hiệu héo rũ, rụng loạt hoặc tổn thương rễ thì người xem chọn `UNDETERMINED` cho nhãn này, không chọn nhãn.

## 3. Nhãn nào được cùng xuất hiện

Mặc định, hai nhãn được cùng gán khi ảnh có đủ bằng chứng của cả hai.

Các cặp sau được ghi rõ vì dễ bị gán nhầm:

| Cặp | Quy tắc |
|---|---|
| `sooty_mold` và `mealybug_infestation` | Được cùng gán. Muội đen không thay cho cụm bông trắng. |
| `sooty_mold` và `thrips_damage` | Được cùng gán. |
| `phytophthora_canker` và `phytophthora_fruit_rot` | Được cùng gán khi khung hình có cả thân và quả, và mỗi vùng đủ bằng chứng của nhãn đó. |
| `phytophthora_canker` và `stem_gummosis_severe` | Không phải hai tên của cùng một vết. Cùng gán chỉ khi ảnh vừa có vỏ sũng nước hoặc gỗ mạch nâu, vừa có nứt dọc sâu và mủ đặc. Chỉ thấy mủ mà không tách được hai kiểu bằng chứng thì `UNDETERMINED`, không đoán một trong hai. |
| `yellow_leaf_nutrient` và `yellow_leaf_root_rot` | Không gán cả hai cho cùng một kiểu vàng lá. Vàng theo quy luật dinh dưỡng là nhãn dinh dưỡng. Vàng xỉn, héo rũ, rụng loạt là nhãn rễ. Vàng chung chung, không đủ một trong hai kiểu, là `UNDETERMINED`. |

## 4. Mã quan sát

Người xem chỉ được dùng các mã dưới đây. Không tạo mã mới trong lúc review.

Vùng: `leaf`, `fruit`, `stem`, `bark`, `branch`, `shoot`, `flower`, `root`, `canopy`, `leaf_axil`, `fruit_spine`.

Triệu chứng:

| Mã | Nhìn thấy gì |
|---|---|
| `concentric_necrotic_spot` | Đốm hoại tử đồng tâm |
| `yellow_halo` | Quầng vàng quanh vết |
| `darkened_wet_bark` | Vỏ tối, sũng nước |
| `brown_vascular_wood` | Gỗ mạch nâu |
| `water_soaked_lesion` | Vết úng nước |
| `white_mycelium` | Tơ trắng |
| `white_cottony_cluster` | Cụm bông trắng |
| `pink_powdery_crust` | Bột hoặc váng hồng trên vỏ |
| `removable_black_coating` | Màng đen trên bề mặt |
| `leaves_bound_by_mycelium` | Lá dính nhau bằng tơ |
| `young_branch_dieback` | Cành non khô mục |
| `deep_vertical_crack` | Nứt dọc sâu |
| `amber_or_red_gum` | Mủ đặc màu hổ phách hoặc đỏ |
| `curled_young_leaf` | Lá non quăn, mép cong |
| `iridescent_scar` | Vệt mất màu vạn hoa |
| `patterned_chlorosis` | Vàng theo quy luật, gân xanh hoặc từ mép |
| `dull_yellow_wilt` | Vàng xỉn và héo |
| `mass_leaf_drop` | Rụng lá loạt |

Thiếu mã cho một đặc điểm dùng để phân biệt nhãn thì chưa được review. Danh sách này phủ các đặc điểm trong mục 2.

## 5. Map từ thư mục cũ

`dataset_label` giữ nguyên tên thư mục. Phép so dùng bảng này. Bảng không được sửa sau khi mở ảnh.

| Tên thư mục | Nhãn taxonomy tương ứng | So được không |
|---|---|---|
| `anthracnose_disease` | `anthracnose_disease` | Có |
| `canker_disease` | `phytophthora_canker` | Có |
| `fruit_rot` | `phytophthora_fruit_rot` | Có |
| `mealybug_infestation` | `mealybug_infestation` | Có |
| `pink_disease` | `pink_disease` | Có |
| `sooty_mold` | `sooty_mold` | Có |
| `stem_blight` | `stem_blight_rhizoctonia` | Có |
| `stem_cracking_ gummosis` | `stem_gummosis_severe` | Có |
| `thrips_disease` | `thrips_damage` | Có |
| `yellow_leaf` | Không có | Không. Kết quả là `UNSCORED` |

Tên thư mục `stem_cracking_ gummosis` có một dấu cách. Map này trỏ dấu cách đó tới `stem_gummosis_severe`.

## 6. Khóa và bản ghi

`image_key` là đường dẫn đầy đủ tính từ `Cay-sau-rieng/`.

```text
Cay-sau-rieng/Test/canker_disease/00163.png
Cay-sau-rieng/Validation/canker_disease/00163.png
```

Hai dòng trên là hai lời gán nhãn, kể cả khi cùng nội dung byte. `content_hash` là một cột để tìm bản trùng, không phải khóa nối.

Người xem không thấy đường dẫn, tên thư mục, nhãn thư mục, và kết quả so. Màn hình dùng một mã ngẫu nhiên. Hệ thống giữ map từ mã đó sang `image_key`.

Bản ghi người xem gửi:

```json
{
  "review_item_id": "R-000183",
  "assigned_labels": ["phytophthora_canker"],
  "observed_regions": ["stem", "bark"],
  "observed_symptoms": ["darkened_wet_bark", "brown_vascular_wood"],
  "undetermined": false,
  "confidence": "high"
}
```

Nếu không đủ bằng chứng, `undetermined` là `true` và `assigned_labels` để trống. `confidence` không tham gia phép so.

Bản ghi thư mục, lưu riêng:

```json
{
  "image_key": "Cay-sau-rieng/Test/canker_disease/00163.png",
  "dataset_label": "canker_disease",
  "content_hash": "",
  "source_split": "Test"
}
```

## 7. Mẫu

Chọn mẫu trước khi xem ảnh.

- Chia theo tên thư mục cũ.
- Không đưa hai đường dẫn cùng `content_hash` và cùng `dataset_label` vào mẫu. Một nội dung chỉ là một ca thị giác.
- Cùng hash mà khác `dataset_label` thì không gộp. Đó là lỗi consistency của cả bộ, không phải một ca trong mẫu.
- Không chọn ảnh vì nó trông dễ hoặc trông đúng nhãn.

## 8. Phép so

Sau khi mọi ảnh trong mẫu đã được gửi, hệ thống mới nối bằng `image_key` và áp bảng map.

| Điều kiện | Kết quả |
|---|---|
| Tên thư mục nằm ở dòng “không so được” | `UNSCORED` |
| Người xem chọn không đủ bằng chứng | `UNDETERMINED` |
| Nhãn đã map có trong `assigned_labels` | `MATCH` |
| Người xem đã gán nhãn khác, và nhãn đã map không có trong danh sách | `MISMATCH` |

Nhãn người xem gán thêm, ngoài nhãn đã map, được ghi vào `additional_labels`. Chúng không đổi `MATCH` thành `MISMATCH`.

`82 / (82 + 12)` là độ khớp trên các ca quyết định được. Không gọi đó là tỷ lệ của mọi ảnh đã xem. `UNDETERMINED / số ảnh đã xem` là tỷ lệ không đủ bằng chứng. `UNSCORED` không vào mẫu số của hai tỷ lệ này.

Ngưỡng đạt chưa đặt. Trước khi mở ảnh phải chốt cả ngưỡng độ khớp và trần tỷ lệ `UNDETERMINED`. Không sửa ngưỡng sau khi thấy kết quả.

## 9. Chưa làm

- [ ] Đặt ngưỡng độ khớp và trần `UNDETERMINED`.
- [ ] Tính `content_hash` và lập mẫu, mỗi nội dung một lần.
- [ ] Review. Người xem chỉ nhận ảnh, taxonomy này, và danh sách mã.
- [ ] Nối bản ghi và tính `MATCH`, `MISMATCH`, `UNDETERMINED`, `UNSCORED`.
- [ ] Ghi tên người xem trong kết quả. Một người xem là độ khớp với người đó.

Kết quả hiện tại: **chưa review**.
