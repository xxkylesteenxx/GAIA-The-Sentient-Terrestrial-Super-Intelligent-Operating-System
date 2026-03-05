#!/usr/bin/env python3

import argparse
import hashlib
import os
import re
from pathlib import Path

MASTER_DOC = Path("GAIA-Master-Canonical-Document-v1.3.3.md")
START = "<!-- CANONICAL_INDEX_START -->"
END = "<!-- CANONICAL_INDEX_END -->"

CANONICAL_GLOB = "**/GAIA-*-v1.0.md"  # Changed: now searches subdirectories

# Explicitly excluded / deprecated artifacts (kept for history, not canonical)
EXCLUDE = {
    "GAIA-Performance-Benchmarking-Protocols-v1.0.md",
}


def normalize_lf(data: bytes) -> bytes:
    data = data.replace(b"\r\n", b"\n")
    data = data.replace(b"\r", b"\n")
    return data


def sha256_lf(path: Path) -> str:
    raw = path.read_bytes()
    norm = normalize_lf(raw)
    return hashlib.sha256(norm).hexdigest()


def iter_canonical_files(root: Path) -> list[Path]:
    files = []
    # Changed: use rglob for recursive search
    for p in root.rglob("GAIA-*-v1.0.md"):
        if p.name in EXCLUDE:
            continue
        if p.is_file():
            files.append(p)
    files.sort(key=lambda x: x.name)
    return files


def make_table(files: list[Path]) -> str:
    header = "| Section | Exact Filename (Repository) | Version | SHA-256 | Priority |\n|---|---|---|---|---|\n"

    # Section numbers are assigned in sorted filename order unless overridden.
    # This keeps generation deterministic.
    rows = []
    base_section = 611
    for i, f in enumerate(files):
        sec = f"6.{base_section + i}"
        ver = "v1.0"
        sha = sha256_lf(f)
        # Enhanced priority detection for new P0 docs
        prio = "P0" if any(keyword in f.name for keyword in [
            "Economic", "Security", "Environmental", "Performance", 
            "P0-Blockers", "Inter-Core", "Consciousness", "Actuation"
        ]) else "P0-P1"
        # Use relative path from repo root to show subdirectories
        rel_path = str(f).replace("\\", "/")  # Normalize path separators
        rows.append(f"| {sec} | {rel_path} | {ver} | {sha} | {prio} |\n")

    return header + "".join(rows)


def update_master_doc(master_path: Path, table_md: str) -> str:
    text = master_path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"Master doc missing markers {START}/{END}")

    pre, rest = text.split(START, 1)
    middle, post = rest.split(END, 1)

    new_middle = "\n\n> This section is auto-generated. Do not edit by hand.\n\n" + table_md + "\n"
    return pre + START + new_middle + END + post


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Overwrite 6.18 table in the master doc")
    ap.add_argument("--root", default=".", help="Repository root")
    args = ap.parse_args()

    root = Path(args.root)
    files = iter_canonical_files(root)

    if not MASTER_DOC.exists():
        raise SystemExit(f"Missing {MASTER_DOC}")

    table = make_table(files)
    updated = update_master_doc(MASTER_DOC, table)

    if args.write:
        MASTER_DOC.write_text(updated, encoding="utf-8", newline="\n")
    else:
        print(updated)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
