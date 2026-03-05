import hashlib
import re
from pathlib import Path

MASTER_DOC = Path("GAIA-Master-Canonical-Document-v1.3.3.md")
START = "<!-- CANONICAL_INDEX_START -->"
END = "<!-- CANONICAL_INDEX_END -->"


def normalize_lf(data: bytes) -> bytes:
    data = data.replace(b"\r\n", b"\n")
    data = data.replace(b"\r", b"\n")
    return data


def sha256_lf(path: Path) -> str:
    return hashlib.sha256(normalize_lf(path.read_bytes())).hexdigest()


def extract_table(md: str) -> str:
    if START not in md or END not in md:
        raise SystemExit("Master doc missing canonical index markers")
    body = md.split(START, 1)[1].split(END, 1)[0]
    return body


def parse_rows(table_block: str) -> list[dict]:
    rows = []
    for line in table_block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("| Section") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 5:
            continue
        rows.append({
            "section": parts[0],
            "filename": parts[1],
            "version": parts[2],
            "sha": parts[3],
            "priority": parts[4],
        })
    return rows


def verify_all() -> int:
    if not MASTER_DOC.exists():
        raise SystemExit(f"Missing {MASTER_DOC}")

    md = MASTER_DOC.read_text(encoding="utf-8")
    table_block = extract_table(md)
    rows = parse_rows(table_block)

    if not rows:
        raise SystemExit("Canonical index table is empty. Run: python generate_canonical_index.py --write")

    failures = []
    for r in rows:
        path = Path(r["filename"])
        if not path.exists():
            failures.append(f"MISSING: {r['filename']}")
            continue
        actual = sha256_lf(path)
        if actual != r["sha"]:
            failures.append(f"HASH_MISMATCH: {r['filename']} expected {r['sha']} got {actual}")

    if failures:
        msg = "\n".join(failures)
        raise SystemExit(f"Canonical verification failed:\n{msg}")

    return 0


if __name__ == "__main__":
    raise SystemExit(verify_all())
