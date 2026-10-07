"""Ghi kết quả Integrity theo trạng thái requirement.

Requirement 1 chưa Frozen, nên không gán PASS hay FAIL.
Requirement 2 và 3 là BLOCKED. Không tính lại SHA-256 để chấm.
Requirement 4 không mở.
Quan sát duy nhất: image_key còn trỏ tới một file trên đĩa hay không.
"""

from pathlib import Path
import json
import re

LAB_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = LAB_ROOT / "src" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "integrity.md"
JSON_PATH = LAB_ROOT / "reports" / "integrity.json"


def show(number):
    return f"{number:,}".replace(",", ".")


def measure():
    if not CATALOG_PATH.is_file():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    missing = []
    for record in records:
        image_key = record.get("image_key")
        path = LAB_ROOT / image_key if image_key else None
        if path is None or not path.is_file():
            missing.append(image_key)
    return {
        "criterion": "integrity",
        "dataset": "images-test/Cay-sau-rieng",
        "specification_status": "Draft",
        "measurement": "BLOCKED",
        "source": "images-test/src/tools/integrity_checker.py",
        "results": {
            "identity_reference": "not_scored",
            "content_integrity": "BLOCKED",
            "catalog_file": "BLOCKED",
            "provenance": "not_opened",
        },
        "reasons": {
            "identity_reference": "Requirement chưa Frozen.",
            "content_integrity": "Chưa có baseline fingerprint đã khóa.",
            "catalog_file": "Chưa chọn source of truth.",
            "provenance": "Requirement không mở.",
        },
        "observation": {
            "catalog_records": len(records),
            "image_key_missing_file": len(missing),
            "note": "Số file còn trỏ được không phải kết quả PASS của requirement 1.",
        },
        "examples": {"image_key_missing_file": missing[:20]},
    }


def result_markdown(report):
    observation = report["observation"]
    lines = [
        "Nguồn: `integrity_checker.py`. Không tính lại SHA-256. Không gán PASS hay FAIL cho requirement chưa Frozen hoặc BLOCKED.",
        "",
        "| Requirement | Kết quả | Lý do |",
        "|---|---|---|",
        "| 1. Identity / reference | chưa chấm | Requirement chưa Frozen |",
        "| 2. Content integrity | BLOCKED | Chưa có baseline fingerprint đã khóa |",
        "| 3. Catalog ↔ file | BLOCKED | Chưa chọn source of truth |",
        "| 4. Provenance | không mở | Chưa có lịch sử thay đổi |",
        "",
        "| Quan sát | Số |",
        "|---|---:|",
        f"| Record trong catalog | {show(observation['catalog_records'])} |",
        f"| `image_key` không còn file | {show(observation['image_key_missing_file'])} |",
        "",
        "Số file còn trỏ được không phải PASS của requirement 1.",
        "",
        "Cả phép đo: BLOCKED.",
    ]
    return "\n".join(lines)


def replace_section(text, heading, body):
    start = text.find(heading)
    if start < 0:
        raise SystemExit(f"Missing heading in {REPORT_PATH}: {heading}")
    return text[:start] + heading + "\n\n" + body.rstrip() + "\n"


def replace_measurement_status(text):
    updated, count = re.subn(
        r"Trạng thái phép đo: \*\*.*?\*\*",
        "Trạng thái phép đo: **blocked**",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"Missing measurement status in {REPORT_PATH}")
    return updated


def write_reports(report):
    markdown = REPORT_PATH.read_text(encoding="utf-8")
    markdown = replace_measurement_status(markdown)
    markdown = replace_section(markdown, "## Kết quả", result_markdown(report))
    REPORT_PATH.write_text(markdown, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    report = measure()
    write_reports(report)
    print(f"Integrity: {report['measurement']}")
    print(f"Missing files: {report['observation']['image_key_missing_file']}")
    print(f"Wrote {REPORT_PATH.name} and {JSON_PATH.name}")


if __name__ == "__main__":
    main()
