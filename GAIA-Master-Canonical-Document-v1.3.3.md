# GAIA Master Canonical Document — v1.3.3
**E5 Promotion & Auto-Generation Lock (Repository-backed)**

*Date: March 5, 2026*  
*Classification: P0-P1 Critical Foundations*

This repository is the single source of truth for canonical filenames and the canonical integrity index. Run the generator to rebuild 6.18 directly from the live tree.

## How to regenerate

```bash
python generate_canonical_index.py --write
python -m gaia_integrity.verify_all
```

## 6.18 Canonical Index & Integrity Controls

<!-- CANONICAL_INDEX_START -->

> This section is auto-generated. Do not edit by hand.
>
> To populate/update it, run:
>
> `python generate_canonical_index.py --write`

<!-- CANONICAL_INDEX_END -->
