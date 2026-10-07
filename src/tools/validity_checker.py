"""Đối chiếu Validity requirement 1 đến 4 và ghi lại mục Kết quả.

Không chấm kích thước, số kênh, hay tên file.
"""

from pathlib import Path
import json
import re

LAB_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = LAB_ROOT / "Cay-sau-rieng"
CATALOG_PATH = LAB_ROOT / "src" / "images.json"
REPORT_PATH = LAB_ROOT / "reports" / "validity.md"
JSON_PATH = LAB_ROOT / "reports" / "validity.json"

PNG_SIGNATURE = bytes.fromhex("89504E470D0A1A0A")
JPEG_SIGNATURE = bytes.fromhex("FFD8")
ALLOWED_LABELS = {
    "anthracnose_disease",
    "canker_disease",
    "fruit_rot",
    "mealybug_infestation",
    "pink_disease",
    "sooty_mold",
    "stem_blight",
    "thrips_disease",
    "yellow_leaf",
}
LABEL_PATTERN = re.compile(r"^[a-z0-9_]+$")


def show(number):
    return f"{number:,}".replace(",", ".")


def read_ends(path):
    with path.open("rb") as handle:
        head = handle.read(8)
        handle.seek(0, 2)
        size = handle.tell()
        handle.seek(max(0, size - 12))
        tail = handle.read(12)
    return head, tail


def detected_kind(head):
    if head.startswith(PNG_SIGNATURE):
        return "png"
    if head.startswith(JPEG_SIGNATURE):
        return "jpeg"
    return None


def ending_ok(kind, tail):
    if kind == "png":
        return tail[-8:-4] == b"IEND"
    if kind == "jpeg":
        return tail[-2:] == b"\xff\xd9"
    return False


def extension_matches(suffix, kind):
    if kind == "png":
        return suffix == ".png"
    if kind == "jpeg":
        return suffix in {".jpg", ".jpeg"}
    return False


def measure():
    if not CATALOG_PATH.is_file():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    signature_failures = []
    ending_failures = []
    unknown_kind = []
    missing_files = []
    charset_failures = []
    allowlist_failures = []

    for record in records:
        image_key = record.get("image_key")
        label = record.get("dataset_label")
        path = LAB_ROOT / image_key if image_key else None
        if path is None or not path.is_file():
            missing_files.append(image_key)
        else:
            head, tail = read_ends(path)
            kind = detected_kind(head)
            suffix = path.suffix.lower()
            if kind is None:
                unknown_kind.append(image_key)
            else:
                if not extension_matches(suffix, kind):
                    signature_failures.append(
                        {"image_key": image_key, "suffix": suffix, "detected": kind}
                    )
                if not ending_ok(kind, tail):
                    ending_failures.append({"image_key": image_key, "detected": kind})

        if not isinstance(label, str) or LABEL_PATTERN.fullmatch(label) is None:
            charset_failures.append({"image_key": image_key, "dataset_label": label})
        if label not in ALLOWED_LABELS:
            allowlist_failures.append({"image_key": image_key, "dataset_label": label})

    results = {
        "extension_matches_signature": "FAIL" if signature_failures or unknown_kind else "PASS",
        "label_charset": "FAIL" if charset_failures else "PASS",
        "container_ending": "FAIL" if ending_failures or unknown_kind else "PASS",
        "label_allowlist": "FAIL" if allowlist_failures else "PASS",
    }
    measurement = "PASS" if all(value == "PASS" for value in results.values()) and not missing_files else "FAIL"
    return {
        "criterion": "validity",
        "dataset": "images-test/Cay-sau-rieng",
        "specification_status": "Frozen",
        "measurement": measurement,
        "source": "images-test/src/tools/validity_checker.py",
        "counts": {
            "catalog_records": len(records),
            "missing_files": len(missing_files),
            "extension_signature_mismatches": len(signature_failures),
            "unknown_signatures": len(unknown_kind),
            "bad_endings": len(ending_failures),
            "label_charset_failures": len(charset_failures),
            "label_allowlist_failures": len(allowlist_failures),
        },
        "results": results,
        "not_scored": {
            "dimensions_and_channels": "Không mở. Chưa có model-input contract.",
            "filename_policy": "Không mở.",
            "pixel_decode": "Chưa phải requirement.",
        },
        "examples": {
            "extension_signature_mismatches": signature_failures[:20],
            "unknown_signatures": unknown_kind[:20],
            "bad_endings": ending_failures[:20],
            "label_charset_failures": charset_failures[:5],
            "label_allowlist_failures": allowlist_failures[:5],
            "missing_files": missing_files[:20],
        },
    }


def result_markdown(report):
    counts = report["counts"]
    results = report["results"]
    lines = [
        "Nguồn: `validity_checker.py`. Chấm requirement 1 đến 4. Kích thước, số kênh và tên file không mở.",
        "",
        "| Kiểm tra | Số | Kết quả |",
        "|---|---:|---|",
        f"| Record trong catalog | {show(counts['catalog_records'])} | — |",
        f"| File không còn trên đĩa | {show(counts['missing_files'])} | {'FAIL' if counts['missing_files'] else '—'} |",
        f"| Đuôi không khớp chữ ký | {show(counts['extension_signature_mismatches'])} | {results['extension_matches_signature']} |",
        f"| Không nhận ra chữ ký | {show(counts['unknown_signatures'])} | {results['extension_matches_signature'] if counts['unknown_signatures'] else 'PASS'} |",
        f"| Khung thiếu phần kết | {show(counts['bad_endings'])} | {results['container_ending']} |",
        f"| `dataset_label` sai ký tự | {show(counts['label_charset_failures'])} | {results['label_charset']} |",
        f"| `dataset_label` ngoài allow list | {show(counts['label_allowlist_failures'])} | {results['label_allowlist']} |",
        "",
        "| Requirement | Kết quả |",
        "|---|---|",
        f"| 1. Đuôi file khớp chữ ký | {results['extension_matches_signature']} |",
        f"| 2. Mã nhãn đúng ký tự | {results['label_charset']} |",
        f"| 3. Khung file có đủ phần kết | {results['container_ending']} |",
        f"| 4. Nhãn thuộc allow list | {results['label_allowlist']} |",
        "| 5. Kích thước và số kênh | không mở |",
        "| 6. Tên file | không mở |",
        "",
        f"Cả phép đo: {report['measurement']}.",
        "",
    ]
    if report["measurement"] == "PASS":
        lines.append("Requirement 1 đến 4 đều đạt.")
    else:
        lines.append("Có requirement không đạt. Các ví dụ nằm trong `validity.json`.")
    lines.append("Đủ phần kết không có nghĩa đuôi file đúng. Tên file và kích thước không được chấm.")
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
    print(f"Validity: {report['measurement']}")
    print(report["counts"])
    print(f"Wrote {REPORT_PATH.name} and {JSON_PATH.name}")


if __name__ == "__main__":
    main()
