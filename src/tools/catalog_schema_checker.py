"""Ghi các field còn mở bằng null, rồi kiểm quyết định metadata đã Frozen.

Script này không cấp UUID, không tính lại SHA-256, và không sửa ảnh.
relative_path được chép từ image_key khi chưa có, để giữ đường dẫn trước migration.
baseline_content_hash, plant_part và capture_time chỉ được thêm khi chưa có khóa.
"""

from pathlib import Path
import json
import re

LAB_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = LAB_ROOT / "reports" / "json" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "catalog-schema.md"
JSON_PATH = LAB_ROOT / "reports" / "json" / "catalog-schema.json"
PATH_ROOT_PREFIX = "Cay-sau-rieng/"
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
FIELD_ORDER = (
    "image_key",
    "relative_path",
    "dataset_label",
    "source_split",
    "content_hash",
    "baseline_content_hash",
    "accuracy",
    "plant_part",
    "capture_time",
)


def show(number):
    return f"{number:,}".replace(",", ".")


def is_lab_relative(value):
    if not isinstance(value, str) or value.strip() == "":
        return False
    if value.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", value):
        return False
    return value.startswith(PATH_ROOT_PREFIX) and "\\" not in value


def apply_open_fields(records):
    added = {"relative_path": 0, "baseline_content_hash": 0, "plant_part": 0, "capture_time": 0}
    updated = []
    for record in records:
        row = dict(record)
        if "relative_path" not in row:
            row["relative_path"] = row.get("image_key")
            added["relative_path"] += 1
        for field in ("baseline_content_hash", "plant_part", "capture_time"):
            if field not in row:
                row[field] = None
                added[field] += 1
        ordered = {field: row[field] for field in FIELD_ORDER if field in row}
        for field, value in row.items():
            if field not in ordered:
                ordered[field] = value
        updated.append(ordered)
    return updated, added


def measure(records):
    problems = []
    counts = {
        "records": len(records),
        "duplicate_image_keys": 0,
        "relative_path_matches_image_key": 0,
        "dataset_label_matches_directory": 0,
        "source_split_matches_directory": 0,
        "content_hash_hex": 0,
        "baseline_content_hash_null": 0,
        "baseline_content_hash_locked": 0,
        "accuracy_null": 0,
        "plant_part_null": 0,
        "capture_time_null": 0,
        "uuid_image_keys": 0,
    }
    seen = {}
    for index, record in enumerate(records):
        image_key = record.get("image_key")
        seen[image_key] = seen.get(image_key, 0) + 1
        parts = image_key.split("/") if isinstance(image_key, str) else []
        directory_label = parts[2] if len(parts) >= 4 else None
        directory_split = parts[1] if len(parts) >= 2 else None

        if not is_lab_relative(image_key):
            problems.append({"index": index, "image_key": image_key, "problem": "image_key_not_lab_relative"})
        if re.fullmatch(r"[0-9a-fA-F-]{36}", image_key or ""):
            counts["uuid_image_keys"] += 1
        if record.get("relative_path") == image_key and is_lab_relative(record.get("relative_path")):
            counts["relative_path_matches_image_key"] += 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "relative_path"})
        if record.get("dataset_label") == directory_label:
            counts["dataset_label_matches_directory"] += 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "dataset_label"})
        if record.get("source_split") == directory_split and directory_split in {"Test", "Validation"}:
            counts["source_split_matches_directory"] += 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "source_split"})
        if isinstance(record.get("content_hash"), str) and HEX_64.fullmatch(record["content_hash"]):
            counts["content_hash_hex"] += 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "content_hash"})
        baseline_hash = record.get("baseline_content_hash")
        if baseline_hash is None:
            counts["baseline_content_hash_null"] += 1
        elif baseline_hash == record.get("content_hash"):
            counts["baseline_content_hash_locked"] = counts.get("baseline_content_hash_locked", 0) + 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "baseline_content_hash_differs"})
        if "accuracy" in record and record.get("accuracy") is None:
            counts["accuracy_null"] += 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "accuracy"})
        if record.get("plant_part") is None:
            counts["plant_part_null"] += 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "plant_part"})
        if record.get("capture_time") is None:
            counts["capture_time_null"] += 1
        else:
            problems.append({"index": index, "image_key": image_key, "problem": "capture_time"})

    counts["duplicate_image_keys"] = sum(1 for count in seen.values() if count > 1)
    for key, count in seen.items():
        if count > 1:
            problems.append({"image_key": key, "problem": "duplicate_image_key", "count": count})

    total = counts["records"]
    frozen_pass = (
        total > 0
        and counts["duplicate_image_keys"] == 0
        and counts["relative_path_matches_image_key"] == total
        and counts["dataset_label_matches_directory"] == total
        and counts["source_split_matches_directory"] == total
        and counts["content_hash_hex"] == total
        and counts["accuracy_null"] == total
        and counts["uuid_image_keys"] == 0
    )
    return {
        "criterion": "catalog_schema",
        "dataset": "images-test/Cay-sau-rieng",
        "specification_status": {
            "core_metadata": "Frozen",
            "plant_part_schema": "Draft",
            "capture_time_schema": "Draft",
            "baseline": "verified" if counts["baseline_content_hash_locked"] == total and counts["baseline_content_hash_null"] == 0 else "partial_or_unverified",
            "uuid_migration": "not_done",
            "integrity_recompute": "see content-hash-verification.json",
        },
        "measurement": "PASS" if frozen_pass else "FAIL",
        "source": "images-test/src/tools/catalog_schema_checker.py",
        "path_root": "images-test/",
        "counts": counts,
        "open_as_null": {
            "baseline_content_hash": counts["baseline_content_hash_null"] == total,
            "plant_part": counts["plant_part_null"] == total,
            "capture_time": counts["capture_time_null"] == total,
        },
        "examples": problems[:20],
    }


def result_markdown(report, added):
    counts = report["counts"]
    total = counts["records"]
    lines = [
        "Nguồn: `catalog_schema_checker.py`. Không cấp UUID. Không tính lại SHA-256.",
        "",
        "| Việc ghi catalog | Số record được thêm khóa |",
        "|---|---:|",
        f"| `relative_path` chép từ `image_key` | {show(added['relative_path'])} |",
        f"| `baseline_content_hash: null` | {show(added['baseline_content_hash'])} |",
        f"| `plant_part: null` | {show(added['plant_part'])} |",
        f"| `capture_time: null` | {show(added['capture_time'])} |",
        "",
        "| Kiểm tra phần Frozen | Số | Kết quả |",
        "|---|---:|---|",
        f"| Record | {show(total)} | — |",
        f"| `image_key` trùng | {show(counts['duplicate_image_keys'])} | {'PASS' if counts['duplicate_image_keys'] == 0 else 'FAIL'} |",
        f"| `relative_path` trùng đường dẫn hiện tại, gốc `images-test/` | {show(counts['relative_path_matches_image_key'])} | {'PASS' if counts['relative_path_matches_image_key'] == total else 'FAIL'} |",
        f"| `dataset_label` trùng tên thư mục | {show(counts['dataset_label_matches_directory'])} | {'PASS' if counts['dataset_label_matches_directory'] == total else 'FAIL'} |",
        f"| `source_split` trùng thư mục split | {show(counts['source_split_matches_directory'])} | {'PASS' if counts['source_split_matches_directory'] == total else 'FAIL'} |",
        f"| `content_hash` là SHA-256 hex | {show(counts['content_hash_hex'])} | {'PASS' if counts['content_hash_hex'] == total else 'FAIL'} |",
        f"| `accuracy` là `null` | {show(counts['accuracy_null'])} | {'PASS' if counts['accuracy_null'] == total else 'FAIL'} |",
        f"| `image_key` đã là UUID | {show(counts['uuid_image_keys'])} | chưa thực hiện |",
        "",
        "| Baseline và field chưa triển khai | Số | Kết quả |",
        "|---|---:|---|",
        f"| `baseline_content_hash` còn `null` | {show(counts['baseline_content_hash_null'])} | {'không có' if counts['baseline_content_hash_null'] == 0 else 'chưa khóa vì file không khớp hoặc chưa có file'} |",
        f"| `baseline_content_hash` đã khóa | {show(counts['baseline_content_hash_locked'])} | bằng `content_hash` sau khi file khớp |",
        f"| `plant_part` | {show(counts['plant_part_null'])} | Draft. `null` là chưa triển khai, không phải đã chốt nghĩa |",
        f"| `capture_time` | {show(counts['capture_time_null'])} | Draft. `null` là chưa triển khai, không phải đã chốt nghĩa |",
        "",
        f"Phần Frozen kiểm được trên catalog hiện tại: {report['measurement']}.",
        "",
        "Migration UUID và registry chưa chạy. Đối chiếu SHA-256 nằm ở `content-hash-verification.json`.",
    ]
    return "\n".join(lines)


def replace_section(text, heading, body):
    start = text.find(heading)
    if start < 0:
        raise SystemExit(f"Missing heading in {REPORT_PATH}: {heading}")
    return text[:start] + heading + "\n\n" + body.rstrip() + "\n"


def main():
    if not CATALOG_PATH.is_file():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    updated, added = apply_open_fields(records)
    CATALOG_PATH.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = measure(updated)
    report["fields_added"] = added
    markdown = REPORT_PATH.read_text(encoding="utf-8")
    REPORT_PATH.write_text(replace_section(markdown, "## Kết quả", result_markdown(report, added)), encoding="utf-8")
    JSON_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catalog schema: {report['measurement']}")
    print(f"Added: {added}")
    print(f"Wrote {REPORT_PATH.name} and {JSON_PATH.name}")


if __name__ == "__main__":
    main()
