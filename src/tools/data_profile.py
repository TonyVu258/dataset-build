"""Mô tả catalog và kích thước file"""

from pathlib import Path
import json

LAB_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = LAB_ROOT / "reports" / "json" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "data-profile.md"


def show(number):
    return f"{number:,}".replace(",", ".")


def show_bytes(number):
    return f"{number:,}".replace(",", ".")


def percentile(sorted_values, fraction):
    if not sorted_values:
        return 0
    index = int(round((len(sorted_values) - 1) * fraction))
    return sorted_values[index]


def measure():
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    by_split = {}
    by_label = {}
    by_label_split = {}
    by_suffix = {}
    sizes = []
    missing_files = 0
    name_has_224 = 0
    accuracy_null = 0
    accuracy_other = 0
    fields = ("image_key", "dataset_label", "source_split", "content_hash", "accuracy")
    field_absent = {field: 0 for field in fields}

    for record in records:
        for field in fields:
            if field not in record or record[field] is None or record[field] == "":
                if field == "accuracy" and field in record and record[field] is None:
                    accuracy_null += 1
                elif field not in record or record[field] == "":
                    field_absent[field] += 1
            elif field == "accuracy":
                accuracy_other += 1

        split = record.get("source_split")
        label = record.get("dataset_label")
        image_key = record.get("image_key") or ""
        by_split[split] = by_split.get(split, 0) + 1
        by_label[label] = by_label.get(label, 0) + 1
        by_label_split[(label, split)] = by_label_split.get((label, split), 0) + 1
        suffix = Path(image_key).suffix.lower() or "(không có đuôi)"
        by_suffix[suffix] = by_suffix.get(suffix, 0) + 1
        if "224x224" in Path(image_key).name:
            name_has_224 += 1
        path = LAB_ROOT / image_key if image_key else None
        if path is None or not path.is_file():
            missing_files += 1
        else:
            sizes.append(path.stat().st_size)

    sizes.sort()
    total_bytes = sum(sizes)
    return {
        "records": len(records),
        "files_found": len(sizes),
        "missing_files": missing_files,
        "total_bytes": total_bytes,
        "by_split": by_split,
        "by_label": by_label,
        "by_label_split": by_label_split,
        "by_suffix": by_suffix,
        "sizes": sizes,
        "name_has_224": name_has_224,
        "accuracy_null": accuracy_null,
        "accuracy_other": accuracy_other,
        "field_absent": field_absent,
    }


def markdown(profile):
    sizes = profile["sizes"]
    lines = [
        "# Data profile",
        "",
        "Dataset: `images-test/Cay-sau-rieng`",
        "",
        "Bản này mô tả catalog và dung lượng file. Không gán PASS, FAIL, hay BLOCKED.",
        "",
        "Nguồn: `images.json` và kích thước file trên đĩa, do `data_profile.py` ghi.",
        "",
        "## Số ảnh và split",
        "",
        "| Mục | Số |",
        "|---|---:|",
        f"| Record | {show(profile['records'])} |",
        f"| File còn trên đĩa | {show(profile['files_found'])} |",
        f"| `image_key` không còn file | {show(profile['missing_files'])} |",
        f"| Tổng dung lượng file | {show_bytes(profile['total_bytes'])} byte |",
        "",
        "| Split | Record |",
        "|---|---:|",
    ]
    for split, count in sorted(profile["by_split"].items(), key=lambda item: str(item[0])):
        lines.append(f"| `{split}` | {show(count)} |")
    lines.extend(
        [
            "",
            "Không có split tên `Train`.",
            "",
            "## Class",
            "",
            f"Số giá trị `dataset_label`: {show(len(profile['by_label']))}. Đây là tên thư mục, chưa phải bệnh đã xác nhận.",
            "",
            "| `dataset_label` | Test | Validation | Tổng |",
            "|---|---:|---:|---:|",
        ]
    )
    for label in sorted(profile["by_label"]):
        test = profile["by_label_split"].get((label, "Test"), 0)
        validation = profile["by_label_split"].get((label, "Validation"), 0)
        total = profile["by_label"][label]
        lines.append(f"| `{label}` | {show(test)} | {show(validation)} | {show(total)} |")
    lines.extend(
        [
            "",
            "Bảng này không đặt ngưỡng. Lệch số giữa các nhãn chưa được gọi là bất thường.",
            "",
            "## Format",
            "",
            "| Đuôi trong `image_key` | Record |",
            "|---|---:|",
        ]
    )
    for suffix, count in sorted(profile["by_suffix"].items()):
        lines.append(f"| `{suffix}` | {show(count)} |")
    lines.extend(
        [
            "",
            "Đuôi lệch chữ ký byte được ghi ở `validity.md`. Bản này không chấm lại.",
            "",
            "## Dung lượng file",
            "",
            "Đơn vị là byte. Đây không phải chiều rộng hay chiều cao của ảnh.",
            "",
            "| Mốc | Byte |",
            "|---|---:|",
            f"| Nhỏ nhất | {show_bytes(sizes[0]) if sizes else 0} |",
            f"| Mốc giữa | {show_bytes(percentile(sizes, 0.5))} |",
            f"| Lớn nhất | {show_bytes(sizes[-1]) if sizes else 0} |",
            "",
            f"Tên file có chuỗi `224x224`: {show(profile['name_has_224'])}. Chuỗi đó không phải kích thước pixel.",
            "",
            "## Metadata",
            "",
            "Trường có trong catalog: `image_key`, `dataset_label`, `source_split`, `content_hash`, `accuracy`.",
            "",
            "| Trường | Record trống hoặc không có |",
            "|---|---:|",
            f"| `image_key` | {show(profile['field_absent']['image_key'])} |",
            f"| `dataset_label` | {show(profile['field_absent']['dataset_label'])} |",
            f"| `source_split` | {show(profile['field_absent']['source_split'])} |",
            f"| `content_hash` | {show(profile['field_absent']['content_hash'])} |",
            f"| `accuracy` là `null` | {show(profile['accuracy_null'])} |",
            "",
            "`accuracy: null` là mô tả. Completeness không gọi trường này là thiếu.",
            "",
            "## Chưa có dữ liệu để mô tả",
            "",
            "- Chiều rộng và chiều cao pixel.",
            "- Số kênh và color mode.",
            "- Ngày chụp.",
            "- `tree_id`.",
            "",
            "Hash trùng, nhãn sai ký tự, và ảnh có ở cả hai split nằm ở `uniqueness.md`, `validity.md`, và `split_independence.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    profile = measure()
    REPORT_PATH.write_text(markdown(profile), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.name}")
    print(f"Records: {profile['records']}")
    print(f"Labels: {len(profile['by_label'])}")
    print(f"Splits: {profile['by_split']}")


if __name__ == "__main__":
    main()
