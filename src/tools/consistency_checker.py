"""Đối chiếu Consistency và ghi lại mục quan sát cùng reports/consistency.json.

Requirement nằm trong reports/consistency.md. Script không sửa requirement.
Khi mục Status còn Draft, các số là quan sát và official_result để null.
Khi mục Status là Frozen, script mới gán PASS, FAIL, UNDETERMINED, hoặc BLOCKED.
"""

from pathlib import Path
import itertools
import json
import re

LAB_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = LAB_ROOT / "src" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "consistency.md"
JSON_PATH = LAB_ROOT / "reports" / "consistency.json"

# Map tên thư mục sang mã taxonomy. yellow_leaf cố ý không có trong bảng này.
FOLDER_TO_TAXON = {
    "anthracnose_disease": "anthracnose_disease",
    "canker_disease": "phytophthora_canker",
    "fruit_rot": "phytophthora_fruit_rot",
    "mealybug_infestation": "mealybug_infestation",
    "pink_disease": "pink_disease",
    "sooty_mold": "sooty_mold",
    "stem_blight": "stem_blight_rhizoctonia",
    "stem_cracking_ gummosis": "stem_gummosis_severe",
    "thrips_disease": "thrips_damage",
}

FORBIDDEN_PAIRS = {
    frozenset({"yellow_leaf_nutrient", "yellow_leaf_root_rot"}),
}


def show(number):
    return f"{number:,}".replace(",", ".")


def specification_status(markdown):
    match = re.search(r"^## Status\n\n\*\*(Draft|Frozen)\.\*\*", markdown, re.M)
    if match is None:
        raise SystemExit(f"Missing Draft or Frozen status in {REPORT_PATH}")
    return match.group(1)


def classify_pair(label_a, label_b):
    if label_a not in FOLDER_TO_TAXON or label_b not in FOLDER_TO_TAXON:
        return "blocked_unmapped"
    mapped = frozenset({FOLDER_TO_TAXON[label_a], FOLDER_TO_TAXON[label_b]})
    if mapped in FORBIDDEN_PAIRS:
        return "forbidden"
    return "needs_evidence"


def label_sets(records):
    by_split = {"Test": set(), "Validation": set()}
    for record in records:
        split = record.get("source_split")
        if split in by_split:
            by_split[split].add(record.get("dataset_label"))
    return by_split["Test"], by_split["Validation"]


def pairs_by_hash(records):
    labels_of = {}
    for record in records:
        labels_of.setdefault(record.get("content_hash"), set()).add(record.get("dataset_label"))

    multi = []
    for digest, labels in labels_of.items():
        if len(labels) < 2:
            continue
        pair_rows = []
        for label_a, label_b in itertools.combinations(sorted(labels), 2):
            pair_rows.append(
                {
                    "labels": [label_a, label_b],
                    "class": classify_pair(label_a, label_b),
                }
            )
        multi.append({"content_hash": digest, "labels": sorted(labels), "pairs": pair_rows})
    return multi


def filename_collisions(records):
    grouped = {}
    for record in records:
        key = record.get("image_key") or ""
        filename = key.rsplit("/", 1)[-1]
        bucket = grouped.setdefault(filename, {"hashes": set(), "labels": set()})
        bucket["hashes"].add(record.get("content_hash"))
        bucket["labels"].add(record.get("dataset_label"))
    return sum(
        1
        for bucket in grouped.values()
        if len(bucket["hashes"]) > 1 and len(bucket["labels"]) > 1
    )


def official_results(status, strings_match, pair_counts):
    if status != "Frozen":
        return None
    requirement_1 = "PASS" if strings_match else "FAIL"
    if pair_counts["forbidden"] > 0:
        requirement_2 = "FAIL"
    elif pair_counts["blocked_unmapped"] > 0:
        requirement_2 = "BLOCKED"
    elif pair_counts["needs_evidence"] > 0:
        requirement_2 = "UNDETERMINED"
    else:
        requirement_2 = "PASS"
    return {"requirement_1": requirement_1, "requirement_2": requirement_2}


def measure(status):
    if not CATALOG_PATH.is_file():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    test_labels, validation_labels = label_sets(records)
    only_test = sorted(test_labels - validation_labels)
    only_validation = sorted(validation_labels - test_labels)
    multi = pairs_by_hash(records)
    pair_counts = {"forbidden": 0, "blocked_unmapped": 0, "needs_evidence": 0}
    for group in multi:
        for pair in group["pairs"]:
            pair_counts[pair["class"]] += 1

    strings_match = test_labels == validation_labels
    return {
        "criterion": "consistency",
        "dataset": "images-test/Cay-sau-rieng",
        "specification_status": status,
        "official_result": official_results(status, strings_match, pair_counts),
        "source": "images-test/src/tools/consistency_checker.py",
        "note": (
            "Status còn Draft. Các số này là quan sát, chưa phải PASS hay FAIL."
            if status != "Frozen"
            else "Status đã Frozen. official_result là kết quả của hai requirement."
        ),
        "requirement_1": {
            "rule": "Tập chuỗi dataset_label ở Test và Validation khớp từng ký tự",
            "strings_match": strings_match,
            "only_in_test": only_test,
            "only_in_validation": only_validation,
            "shared_label_count": len(test_labels & validation_labels),
        },
        "requirement_2": {
            "rule": "Cặp dataset_label trên cùng content_hash chỉ mâu thuẫn khi map sang cặp bị cấm",
            "hashes_with_two_or_more_labels": len(multi),
            "pairs": pair_counts,
            "examples": multi[:15],
        },
        "out_of_scope": {
            "filenames_with_different_bytes_and_labels": filename_collisions(records),
        },
    }


def observation_markdown(report):
    requirement_1 = report["requirement_1"]
    requirement_2 = report["requirement_2"]
    match_text = "khớp từng ký tự" if requirement_1["strings_match"] else "không khớp"
    lines = [
        f"Nguồn: `consistency_checker.py`. {report['note']}",
        "",
        "| Quan sát | Số |",
        "|---|---|",
        f"| Nội dung byte đứng trong hơn một thư mục bệnh | {show(requirement_2['hashes_with_two_or_more_labels'])} |",
        f"| Tên file trỏ tới nhiều nội dung và nhiều thư mục bệnh, ngoài requirement | {show(report['out_of_scope']['filenames_with_different_bytes_and_labels'])} |",
        f"| Chuỗi nhãn thư mục giữa `Test` và `Validation` | {match_text}. {show(requirement_1['shared_label_count'])} chuỗi dùng chung |",
        "",
        "| Requirement | Đối chiếu máy | Kết quả chính thức |",
        "|---|---|---|",
    ]
    official = report["official_result"]
    if official is None:
        lines.append("| 1. Chuỗi nhãn thư mục dùng chung | đã đếm | chưa chấm, Status còn Draft |")
        lines.append("| 2. Cặp nhãn trên cùng một nội dung byte | đã đếm | chưa chấm, Status còn Draft |")
    else:
        lines.append(f"| 1. Chuỗi nhãn thư mục dùng chung | đã đếm | {official['requirement_1']} |")
        lines.append(f"| 2. Cặp nhãn trên cùng một nội dung byte | đã đếm | {official['requirement_2']} |")
    lines.extend(
        [
            "",
            "Tên file không được chấm. Một hash chỉ có một `dataset_label` không tạo cặp.",
        ]
    )
    return "\n".join(lines)


def measurement_label(official):
    if official is None:
        return "chưa chấm"
    values = list(official.values())
    if "FAIL" in values:
        return "không đạt"
    if "BLOCKED" in values:
        return "blocked"
    if "UNDETERMINED" in values:
        return "chưa đủ để kết luận"
    return "đạt"


def replace_measurement_status(text, official):
    label = measurement_label(official)
    updated, count = re.subn(
        r"Trạng thái phép đo: \*\*.*?\*\*",
        f"Trạng thái phép đo: **{label}**",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"Missing measurement status in {REPORT_PATH}")
    return updated


def replace_section(text, heading, body, stop_heading):
    start = text.find(heading)
    stop = text.find(stop_heading)
    if start < 0 or stop < 0 or stop < start:
        raise SystemExit(f"Missing section boundaries in {REPORT_PATH}")
    return text[:start] + heading + "\n\n" + body.rstrip() + "\n\n" + text[stop:]


def write_reports(report):
    markdown = REPORT_PATH.read_text(encoding="utf-8")
    markdown = replace_measurement_status(markdown, report["official_result"])
    markdown = replace_section(
        markdown,
        "## Kết quả",
        observation_markdown(report),
        "## Status",
    )
    REPORT_PATH.write_text(markdown, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    markdown = REPORT_PATH.read_text(encoding="utf-8")
    report = measure(specification_status(markdown))
    write_reports(report)
    print(f"Consistency specification: {report['specification_status']}")
    print(f"Official result: {report['official_result']}")
    print(f"Wrote {REPORT_PATH.name} and {JSON_PATH.name}")


if __name__ == "__main__":
    main()
