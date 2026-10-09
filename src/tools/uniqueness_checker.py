"""Đối chiếu uniqueness ở mức byte và ghi lại mục Kết quả.

Rule: trong một split, một content_hash chỉ được xuất hiện một lần.
Cùng hash ở cả Test và Validation được phép, và không tính là vi phạm.
Scene và tree không được chấm.
"""

from pathlib import Path
import json
import re

LAB_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = LAB_ROOT / "reports" / "json" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "uniqueness.md"
JSON_PATH = LAB_ROOT / "reports" / "uniqueness.json"
SPLITS = ("Test", "Validation")


def show(number):
    return f"{number:,}".replace(",", ".")


def measure():
    if not CATALOG_PATH.is_file():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    grouped = {}
    splits_of_hash = {}
    for record in records:
        split = record.get("source_split")
        digest = record.get("content_hash")
        key = record.get("image_key")
        grouped.setdefault((split, digest), []).append(key)
        splits_of_hash.setdefault(digest, set()).add(split)

    violations = []
    per_split = {}
    for split in SPLITS:
        groups = [
            {"content_hash": digest, "image_keys": keys}
            for (group_split, digest), keys in grouped.items()
            if group_split == split and len(keys) > 1
        ]
        groups.sort(key=lambda item: item["content_hash"])
        per_split[split] = len(groups)
        for group in groups:
            violations.append({"split": split, **group})

    allowed_across_splits = sum(
        1
        for splits in splits_of_hash.values()
        if "Test" in splits and "Validation" in splits
    )
    byte_result = "PASS" if len(violations) == 0 else "FAIL"
    return {
        "criterion": "uniqueness",
        "level": "byte",
        "dataset": "images-test/Cay-sau-rieng",
        "specification_status": "Frozen",
        "measurement": byte_result,
        "source": "images-test/src/tools/uniqueness_checker.py",
        "rule": "Trong một split, một content_hash chỉ xuất hiện một lần. Trùng giữa Test và Validation được phép.",
        "counts": {
            "catalog_records": len(records),
            "hashes_in_both_splits_allowed": allowed_across_splits,
            "hashes_repeated_inside_test": per_split["Test"],
            "hashes_repeated_inside_validation": per_split["Validation"],
            "violations": len(violations),
        },
        "not_scored": {
            "scene": "Không mở. Chưa có policy scene identity.",
            "tree": "Không xét được. Không có tree_id.",
        },
        "examples": violations[:15],
    }


def result_markdown(report):
    counts = report["counts"]
    lines = [
        "Nguồn: `uniqueness_checker.py`. Chỉ chấm byte. Scene không mở. Tree không xét được.",
        "",
        "Rule: trong một split, một `content_hash` chỉ xuất hiện một lần. Cùng hash ở cả `Test` và `Validation` được phép.",
        "",
        "| Kiểm tra | Số | Kết quả |",
        "|---|---:|---|",
        f"| Record trong catalog | {show(counts['catalog_records'])} | — |",
        f"| Hash có ở cả `Test` và `Validation` | {show(counts['hashes_in_both_splits_allowed'])} | được phép, không tính vi phạm |",
        f"| Hash lặp trong `Test` | {show(counts['hashes_repeated_inside_test'])} | {report['measurement'] if counts['hashes_repeated_inside_test'] else 'PASS'} |",
        f"| Hash lặp trong `Validation` | {show(counts['hashes_repeated_inside_validation'])} | {report['measurement'] if counts['hashes_repeated_inside_validation'] else 'PASS'} |",
        "",
        "| Requirement | Kết quả |",
        "|---|---|",
        f"| 1. Byte | {report['measurement']} |",
        "| 2. Scene | không mở |",
        "| 3. Tree | không xét được |",
        "",
    ]
    if report["measurement"] == "PASS":
        lines.append("Không có `content_hash` nào đứng hơn một lần trong cùng một split.")
    else:
        lines.append("Có hash lặp trong một split. Các ví dụ nằm trong `uniqueness.json`.")
    return "\n".join(lines)


def replace_section(text, heading, body):
    start = text.find(heading)
    if start < 0:
        raise SystemExit(f"Missing heading in {REPORT_PATH}: {heading}")
    return text[:start] + heading + "\n\n" + body.rstrip() + "\n"


def replace_measurement_status(text, measurement):
    label = "đạt ở byte" if measurement == "PASS" else "không đạt ở byte"
    updated, count = re.subn(
        r"Trạng thái phép đo: \*\*.*?\*\*",
        f"Trạng thái phép đo: **{label}**",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"Missing measurement status in {REPORT_PATH}")
    return updated


def replace_byte_score(text, measurement):
    updated, count = re.subn(
        r"\| Cấm bản trùng trong một split \| Có \|\n\| Chấm \| .*? \|",
        f"| Cấm bản trùng trong một split | Có |\n| Chấm | {measurement} |",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"Missing byte score row in {REPORT_PATH}")
    return updated


def write_reports(report):
    markdown = REPORT_PATH.read_text(encoding="utf-8")
    markdown = replace_measurement_status(markdown, report["measurement"])
    markdown = replace_byte_score(markdown, report["measurement"])
    markdown = replace_section(markdown, "## Kết quả", result_markdown(report))
    REPORT_PATH.write_text(markdown, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    report = measure()
    write_reports(report)
    print(f"Uniqueness byte: {report['measurement']}")
    print(
        "Repeated inside Test: "
        f"{report['counts']['hashes_repeated_inside_test']}; "
        "Validation: "
        f"{report['counts']['hashes_repeated_inside_validation']}"
    )
    print(f"Wrote {REPORT_PATH.name} and {JSON_PATH.name}")


if __name__ == "__main__":
    main()
