# Data profile

Dataset: `images-test/Cay-sau-rieng`

Bản này mô tả catalog và dung lượng file. Không gán PASS, FAIL, hay BLOCKED.

Nguồn: `images.json` và kích thước file trên đĩa, do `data_profile.py` ghi.

## Số ảnh và split

| Mục | Số |
|---|---:|
| Record | 1.297 |
| File còn trên đĩa | 1.297 |
| `image_key` không còn file | 0 |
| Tổng dung lượng file | 1.244.672.914 byte |

| Split | Record |
|---|---:|
| `Test` | 648 |
| `Validation` | 649 |

Không có split tên `Train`.

## Class

Số giá trị `dataset_label`: 10. Đây là tên thư mục, chưa phải bệnh đã xác nhận.

| `dataset_label` | Test | Validation | Tổng |
|---|---:|---:|---:|
| `anthracnose_disease` | 63 | 62 | 125 |
| `canker_disease` | 65 | 65 | 130 |
| `fruit_rot` | 61 | 61 | 122 |
| `mealybug_infestation` | 65 | 65 | 130 |
| `pink_disease` | 68 | 65 | 133 |
| `sooty_mold` | 66 | 68 | 134 |
| `stem_blight` | 64 | 64 | 128 |
| `stem_cracking_ gummosis` | 68 | 68 | 136 |
| `thrips_disease` | 66 | 66 | 132 |
| `yellow_leaf` | 62 | 65 | 127 |

Bảng này không đặt ngưỡng. Lệch số giữa các nhãn chưa được gọi là bất thường.

## Format

| Đuôi trong `image_key` | Record |
|---|---:|
| `.jpg` | 36 |
| `.png` | 1.261 |

Đuôi lệch chữ ký byte được ghi ở `validity.md`. Bản này không chấm lại.

## Dung lượng file

Đơn vị là byte. Đây không phải chiều rộng hay chiều cao của ảnh.

| Mốc | Byte |
|---|---:|
| Nhỏ nhất | 8.160 |
| Mốc giữa | 786.048 |
| Lớn nhất | 3.826.049 |

Tên file có chuỗi `224x224`: 19. Chuỗi đó không phải kích thước pixel.

## Metadata

Trường có trong catalog: `image_key`, `dataset_label`, `source_split`, `content_hash`, `accuracy`.

| Trường | Record trống hoặc không có |
|---|---:|
| `image_key` | 0 |
| `dataset_label` | 0 |
| `source_split` | 0 |
| `content_hash` | 0 |
| `accuracy` là `null` | 1.297 |

`accuracy: null` là mô tả. Completeness không gọi trường này là thiếu.

## Chưa có dữ liệu để mô tả

- Chiều rộng và chiều cao pixel.
- Số kênh và color mode.
- Ngày chụp.
- `tree_id`.

Hash trùng, nhãn sai ký tự, và ảnh có ở cả hai split nằm ở `uniqueness.md`, `validity.md`, và `split_independence.md`.
