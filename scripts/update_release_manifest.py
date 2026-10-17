"""Refresh release checksums for reviewed, Git-tracked working-tree files."""
from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_NAMES = {"MANIFEST.csv", "SHA256SUMS.txt"}


def main() -> int:
    tracked = subprocess.check_output(
        ["git", "ls-files", "--cached", "-z"], cwd=ROOT
    ).decode("utf-8").split("\0")
    names = sorted({name for name in tracked if name and name not in MANIFEST_NAMES})
    with (ROOT / "MANIFEST.csv").open(encoding="utf-8-sig", newline="") as stream:
        categories = {row["relative_path"]: row["category"] for row in csv.DictReader(stream)}
    rows = []
    for name in names:
        path = ROOT / name
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT):
            raise ValueError(f"Expected a regular tracked file: {name}")
        data = path.read_bytes()
        staged = subprocess.check_output(["git", "show", f":{name}"], cwd=ROOT)
        if data != staged:
            raise ValueError(
                f"Working file differs from staged bytes: {name}. "
                "Use LF for text files and stage the reviewed content first."
            )
        rows.append({"relative_path": name, "category": categories.get(name, "仓库说明"),
                     "byte_size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    with (ROOT / "MANIFEST.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["relative_path", "category", "byte_size", "sha256"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "SHA256SUMS.txt").write_text(
        "".join(f'{r["sha256"]}  {r["relative_path"]}\n' for r in rows),
        encoding="utf-8", newline="\n",
    )
    print(f"manifest=UPDATED\nfiles={len(rows)}")
    print("Run python scripts/verify_release.py before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
