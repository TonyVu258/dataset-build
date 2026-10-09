"""Ghi kết quả Integrity theo trạng thái requirement.

Requirement 1 chưa Frozen, nên không gán PASS hay FAIL.
Requirement 2 tính lại SHA-256 và so với baseline_content_hash.
Requirement 3 vẫn BLOCKED vì chưa chọn source of truth.
Requirement 4 không mở.
"""

from pathlib import Path
import hashlib
import json
import re

LAB_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = LAB_ROOT / "reports" / "json" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "integrity.md"
JSON_PATH = LAB_ROOT / "reports" / "integrity.json"


def show(number):
    return f"{number:,}".replace(",", ".")


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def measure():
    if not CATALOG_PATH.is_file():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    missing = []
    baseline_null = 0
    baseline_match = 0
    baseline_mismatch = []
    for record in records:
        relative = record.get("relative_path") or record.get("image_key")
        path = LAB_ROOT / relative if relative else None
        if path is None or not path.is_file():
            missing.append(relative)
            continue
        if record.get("baseline_content_hash") is None:
            baseline_null += 1
            continue
        observed = sha256_file(path)
        if observed == record.get("baseline_content_hash") == record.get("content_hash"):
            baseline_match += 1
        else:
            baseline_mismatch.append(relative)
    content_result = "PASS" if records and baseline_match == len(records) and not missing and baseline_null == 0 else "FAIL"
    return {
        "criterion": "integrity",
        "dataset": "images-test/Cay-sau-rieng",
        "specification_status": "Draft",
        "measurement": "BLOCKED",
        "content_integrity": content_result,
        "source": "images-test/src/tools/integrity_checker.py",
        "results": {
            "identity_reference": "not_scored",
            "content_integrity": content_result,
            "catalog_file": "BLOCKED",
            "provenance": "not_opened",
        },
        "reasons": {
            "identity_reference": "Requirement chưa Frozen.",
            "content_integrity": "SHA-256 của file hiện tại so với baseline_content_hash và content_hash.",
            "catalog_file": "Chưa chọn source of truth.",
            "provenance": "Requirement không mở.",
        },
        "observation": {
            "catalog_records": len(records),
            "image_key_missing_file": len(missing),
            "baseline_content_hash_null": baseline_null,
            "baseline_match": baseline_match,
            "baseline_mismatch": len(baseline_mismatch),
            "note": "Số file còn trỏ được không phải kết quả PASS của requirement 1.",
        },
        "examples": {"image_key_missing_file": missing[:20], "baseline_mismatch": baseline_mismatch[:20]},
    }


def result_markdown(report):
    observation = report["observation"]
    lines = [
        "Nguồn: `integrity_checker.py`. Requirement 2 tính lại SHA-256. Requirement chưa Frozen hoặc còn BLOCKED không được gán là kết quả của cả phép đo.",
        "",
        "| Requirement | Kết quả | Lý do |",
        "|---|---|---|",
        "| 1. Identity / reference | chưa chấm | Requirement chưa Frozen |",
        f"| 2. Content integrity | {report['results']['content_integrity']} | SHA-256 file hiện tại so với `baseline_content_hash` |",
        "| 3. Catalog ↔ file | BLOCKED | Chưa chọn source of truth |",
        "| 4. Provenance | không mở | Chưa có lịch sử thay đổi |",
        "",
        "| Quan sát | Số |",
        "|---|---:|",
        f"| Record trong catalog | {show(observation['catalog_records'])} |",
        f"| File không còn theo `relative_path` | {show(observation['image_key_missing_file'])} |",
        f"| `baseline_content_hash` là `null` | {show(observation['baseline_content_hash_null'])} |",
        f"| File khớp baseline và `content_hash` | {show(observation['baseline_match'])} |",
        f"| File lệch baseline | {show(observation['baseline_mismatch'])} |",
        "",
        "Số file còn trỏ được không phải PASS của requirement 1. Lệch hash chứng minh byte khác baseline, chưa kết luận thay đổi trái phép.",
        "",
        "Cả phép đo: BLOCKED, vì requirement 1 và 3 chưa chấm.",
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
