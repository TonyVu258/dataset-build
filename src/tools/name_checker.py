"""
Checklist for this raw folder.
Required items are the statistics we compute.
Optional items are checks, not separate reports.

1. Optional. How many image files are there?
2. Optional. How many filenames are repeated?
3. Optional. Among repeated names, how many groups share one file size?
4. Optional. Among those, how many are byte-identical?
5. Required. How many byte-identical images sit in more than one disease folder?
6. Required. How many distinct images exist by bytes, how many are stored
   more than once, and how many of those copies use different filenames?
7. Optional. For same-byte files with different names, what kind of
   name difference is it?
8. Required. How many distinct images appear in both Test and Validation?
9. Required. How many filenames point at different images and more than
   one disease folder?
10. Optional. How many files look like the same scene with different bytes?
11. Required note, no statistic. Bytes do not establish the true disease,
    the tree, the farm, or that Test and Validation were a deliberate split.
"""

from pathlib import Path
import hashlib

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
root = Path(__file__).resolve().parents[2] / "Cay-sau-rieng"

if not root.is_dir():
    raise SystemExit(f"Image folder not found: {root}")


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_name(path):
    # Cay-sau-rieng / Test|Validation / disease / file
    return path.parent.parent.name


def class_name(path):
    return path.parent.name


images = [
    path
    for path in root.rglob("*")
    if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
]

by_name = {}
by_hash = {}
hash_of = {}
for path in images:
    digest = file_hash(path)
    hash_of[path] = digest
    by_name.setdefault(path.name, []).append(path)
    by_hash.setdefault(digest, []).append(path)

# 1. Optional. File count, kept because criterion 6 is compared with it.
print(f"1. Image files: {len(images)}")

# 2. Optional. Same filename is not the same image.
repeated_names = {name: paths for name, paths in by_name.items() if len(paths) > 1}
print(f"2. Distinct filenames: {len(by_name)}")
print(f"2. Repeated filenames: {len(repeated_names)}")

# 3. Optional. Different sizes are already different files.
same_size = 0
different_size = 0
for paths in repeated_names.values():
    sizes = {path.stat().st_size for path in paths}
    if len(sizes) == 1:
        same_size += 1
    else:
        different_size += 1
print(f"3. Repeated names with one file size: {same_size}")
print(f"3. Repeated names with different file sizes: {different_size}")

# 4. Optional. Same size still needs a hash.
identical_names = 0
same_size_but_different = 0
for paths in repeated_names.values():
    sizes = {path.stat().st_size for path in paths}
    if len(sizes) != 1:
        continue
    hashes = {hash_of[path] for path in paths}
    if len(hashes) == 1:
        identical_names += 1
    else:
        same_size_but_different += 1
print(f"4. Same-size name groups that are byte-identical: {identical_names}")
print(f"4. Same-size name groups with different bytes: {same_size_but_different}")

# 5 and 6 and 8 share one grouping: the bytes themselves.
repeated_hashes = {digest: paths for digest, paths in by_hash.items() if len(paths) > 1}
different_names = 0
in_many_classes = 0
in_both_splits = 0
for paths in repeated_hashes.values():
    names = {path.name for path in paths}
    classes = {class_name(path) for path in paths}
    splits = {split_name(path) for path in paths}
    if len(names) > 1:
        different_names += 1
    if len(classes) > 1:
        in_many_classes += 1
    if "Test" in splits and "Validation" in splits:
        in_both_splits += 1

print(f"6. Distinct images by bytes: {len(by_hash)}")
print(f"6. Images stored more than once: {len(repeated_hashes)}")
print(f"6. Copies that use different filenames: {different_names}")
print(f"5. Byte-identical images in more than one disease folder: {in_many_classes}")
print(f"8. Distinct images in both Test and Validation: {in_both_splits}")

# 7. Optional. Not computed: name-difference kinds are a breakdown of criterion 6.
# 10. Optional. Not computed: a resized image is the same scene with different bytes.

# 9. Required. One filename used for different pictures and different disease folders.
names_across_classes = 0
for paths in repeated_names.values():
    hashes = {hash_of[path] for path in paths}
    classes = {class_name(path) for path in paths}
    if len(hashes) > 1 and len(classes) > 1:
        names_across_classes += 1
print(
    "9. Filenames that point at different images and more than one disease folder: "
    f"{names_across_classes}"
)

# 11. Required note. This script counts files and bytes, not diagnosed cases.
print(
    "11. Note: these counts do not establish the true disease, tree, farm, "
    "or that Test and Validation were a deliberate split."
)
