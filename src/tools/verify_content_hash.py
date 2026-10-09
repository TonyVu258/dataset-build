"""Tính lại SHA-256 của file hiện tại và khóa baseline khi khớp.

baseline_content_hash được gán bằng content_hash chỉ khi hash file bằng content_hash.
Record lệch hoặc không còn file giữ baseline_content_hash là null.
content_hash không bị ghi đè.
"""

from pathlib import Path
import hashlib
import json

LAB_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = LAB_ROOT / "reports" / "json" / "images.json"
BASELINE_PATH = LAB_ROOT / "reports" / "json" / "content-hash-baseline-v1.json"
REPORT_PATH = LAB_ROOT / "reports" / "json" / "content-hash-verification.json"


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    records = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    matched = 0
    mismatched = []
    missing = []
    for record in records:
        relative = record.get("relative_path")
        path = LAB_ROOT / relative if relative else None
        if path is None or not path.is_file():
            record["baseline_content_hash"] = None
            missing.append(relative)
            continue
        observed = sha256_file(path)
        if observed == record.get("content_hash"):
            record["baseline_content_hash"] = record["content_hash"]
            matched += 1
        else:
            record["baseline_content_hash"] = None
            mismatched.append({
                "relative_path": relative,
                "content_hash": record.get("content_hash"),
                "file_sha256": observed,
            })
    CATALOG_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    baseline["verification_against_current_files"] = "done"
    baseline["verified_on"] = "2026-10-09"
    baseline["matched"] = matched
    baseline["mismatched"] = len(mismatched)
    baseline["missing"] = len(missing)
    baseline["catalog_baseline_content_hash"] = (
        "set to content_hash where the current file matches; null where it does not"
    )
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = {
        "dataset": "images-test/Cay-sau-rieng",
        "verified_on": "2026-10-09",
        "records": len(records),
        "matched": matched,
        "mismatched": len(mismatched),
        "missing": len(missing),
        "rule": "baseline_content_hash equals content_hash only when the current file SHA-256 equals content_hash",
        "examples": {"mismatched": mismatched[:20], "missing": missing[:20]},
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"matched={matched} mismatched={len(mismatched)} missing={len(missing)}")


if __name__ == "__main__":
    main()
