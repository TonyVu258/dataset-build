"""Đối chiếu Completeness đã Frozen và ghi lại mục Kết quả.

Specification nằm trong reports/completeness.md. Script này không sửa các requirement.
Chỉ viết lại dòng trạng thái phép đo, mục Kết quả, và reports/completeness.json.
"""

from pathlib import Path
import json
import re

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
SPLITS = {"Test", "Validation"}
REQUIRED_FIELDS = ("image_key", "dataset_label", "source_split", "content_hash")

LAB_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = LAB_ROOT / "Cay-sau-rieng"
CATALOG_PATH = LAB_ROOT / "reports" / "json" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "completeness.md"
JSON_PATH = LAB_ROOT / "reports" / "completeness.json"


def show(number):
    return f"{number:,}".replace(",", ".")


def image_key_of(path):
    return path.relative_to(LAB_ROOT).as_posix()


def in_scope(path):
    relative = path.relative_to(DATA_ROOT)
    return len(relative.parts) >= 2 and relative.parts[0] in SPLITS


def blank(value):
    return value is None or (isinstance(value, str) and value.strip() == "")


def collect_files():
    in_scope_keys = []
    outside = []
    non_images = {}
    for path in DATA_ROOT.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in IMAGE_SUFFIXES:
            if in_scope(path):
                in_scope_keys.append(image_key_of(path))
            else:
                outside.append(image_key_of(path))
        elif path.name == ".DS_Store":
            non_images[".DS_Store"] = non_images.get(".DS_Store", 0) + 1
    return in_scope_keys, outside, non_images


def field_problems(records):
    problems = []
    accuracy_null = 0
    accuracy_absent = 0
    accuracy_other = 0
    for index, record in enumerate(records):
        if "accuracy" not in record:
            accuracy_absent += 1
        elif record["accuracy"] is None:
            accuracy_null += 1
        else:
            accuracy_other += 1
        for field in REQUIRED_FIELDS:
            if field not in record:
                problems.append({"index": index, "image_key": record.get("image_key"), "field": field, "problem": "absent"})
            elif blank(record[field]):
                problems.append({"index": index, "image_key": record.get("image_key"), "field": field, "problem": "null_or_blank"})
    return problems, accuracy_null, accuracy_absent, accuracy_other


def measure():
    if not DATA_ROOT.is_dir():
        raise SystemExit(f"Image folder not found: {DATA_ROOT}")
    if not CATALOG_PATH.is_file():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")

    file_keys, outside, non_images = collect_files()
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    keys = [record.get("image_key") for record in records]
    file_set = set(file_keys)
    key_counts = {}
    for key in keys:
        key_counts[key] = key_counts.get(key, 0) + 1

    files_without_record = sorted(file_set - set(keys))
    records_without_file = sorted(key for key in set(keys) if key not in file_set)
    duplicate_keys = sorted(key for key, count in key_counts.items() if count > 1)
    problems, accuracy_null, accuracy_absent, accuracy_other = field_problems(records)

    fields_pass = len(problems) == 0
    cases_pass = (
        len(files_without_record) == 0
        and len(records_without_file) == 0
        and len(duplicate_keys) == 0
    )
    missingness_pass = fields_pass
    overall = "PASS" if fields_pass and cases_pass and missingness_pass else "FAIL"

    return {
        "criterion": "completeness",
        "dataset": "images-test/Cay-sau-rieng",
        "specification_status": "Frozen",
        "measurement": overall,
        "source": "images-test/src/tools/completeness_checker.py",
        "counts": {
            "image_files_in_scope": len(file_keys),
            "catalog_records": len(records),
            "files_without_record": len(files_without_record),
            "records_without_file": len(records_without_file),
            "duplicate_image_keys": len(duplicate_keys),
            "required_fields_missing": len(problems),
            "accuracy_null": accuracy_null,
            "accuracy_key_absent": accuracy_absent,
            "accuracy_other": accuracy_other,
            "ds_store": non_images.get(".DS_Store", 0),
            "images_outside_scope": len(outside),
        },
        "results": {
            "required_record_fields": "PASS" if fields_pass else "FAIL",
            "required_dataset_cases": "PASS" if cases_pass else "FAIL",
            "quantity": "not_opened",
            "missingness": "PASS" if missingness_pass else "FAIL",
            "exclusions": "applied_not_scored",
            "measurement": overall,
        },
        "examples": {
            "files_without_record": files_without_record[:15],
            "records_without_file": records_without_file[:15],
            "duplicate_image_keys": duplicate_keys[:15],
            "required_field_problems": problems[:15],
        },
    }


def result_markdown(report):
    counts = report["counts"]
    results = report["results"]
    lines = [
        "Nguồn: `completeness_checker.py`, đối chiếu file `.jpg`, `.jpeg`, `.png` trong `Test` và `Validation` với `image_key` trong `images.json`.",
        "",
        "| Kiểm tra | Số | Kết quả |",
        "|---|---:|---|",
        f"| File ảnh trong phạm vi | {show(counts['image_files_in_scope'])} | — |",
        f"| Record trong catalog | {show(counts['catalog_records'])} | — |",
        f"| File không có record | {show(counts['files_without_record'])} | {results['required_dataset_cases'] if counts['files_without_record'] else 'PASS'} |",
        f"| Record không có file | {show(counts['records_without_file'])} | {results['required_dataset_cases'] if counts['records_without_file'] else 'PASS'} |",
        f"| `image_key` trùng nhau | {show(counts['duplicate_image_keys'])} | {'FAIL' if counts['duplicate_image_keys'] else 'PASS'} |",
        f"| Trường bắt buộc trống hoặc không có | {show(counts['required_fields_missing'])} | {results['required_record_fields']} |",
        f"| `accuracy: null` | {show(counts['accuracy_null'])} | được phép, không tính thiếu |",
        f"| `.DS_Store` | {show(counts['ds_store'])} | ngoài phạm vi |",
        f"| Ảnh nằm ngoài `Test` và `Validation` | {show(counts['images_outside_scope'])} | — |",
        "",
        "| Requirement | Kết quả |",
        "|---|---|",
        f"| 2. Required record fields | {results['required_record_fields']} |",
        f"| 3. Required dataset cases | {results['required_dataset_cases']} |",
        "| Quantity | không mở |",
        f"| 4. Missingness | {results['missingness']} |",
        "| 5. Exclusions | đã áp dụng, không chấm |",
        f"| Cả phép đo | {results['measurement']} |",
        "",
    ]
    if report["measurement"] == "PASS":
        lines.append("Không có requirement nào ra FAIL, UNDETERMINED, hoặc BLOCKED trong phạm vi đã đóng.")
    else:
        lines.append("Có requirement không đạt. Các ví dụ nằm trong `completeness.json`.")
    return "\n".join(lines)


def replace_section(text, heading, body):
    start = text.find(heading)
    if start < 0:
        raise SystemExit(f"Missing heading in {REPORT_PATH}: {heading}")
    return text[:start] + heading + "\n\n" + body.rstrip() + "\n"


def replace_measurement_status(text, measurement):
    label = "đạt" if measurement == "PASS" else "không đạt"
    updated, count = re.subn(
        r"Trạng thái phép đo: \*\*.*?\*\*",
        f"Trạng thái phép đo: **{label}**",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"Missing measurement status in {REPORT_PATH}")
    return updated


def write_reports(report):
    markdown = REPORT_PATH.read_text(encoding="utf-8")
    markdown = replace_measurement_status(markdown, report["measurement"])
    markdown = replace_section(markdown, "## Kết quả", result_markdown(report))
    REPORT_PATH.write_text(markdown, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    report = measure()
    write_reports(report)
    print(f"Completeness: {report['measurement']}")
    print(f"Wrote {REPORT_PATH.name} and {JSON_PATH.name}")


if __name__ == "__main__":
    main()
