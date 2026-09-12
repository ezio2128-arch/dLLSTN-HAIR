#!/usr/bin/env python3
from pathlib import Path
import json, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
print(f"ROOT={root}")

patterns = {
    "plugins": ["*.esp", "*.esm", "*.esl"],
    "papyrus_source": ["*.psc"],
    "papyrus_compiled": ["*.pex"],
    "animations": ["*.hkx"],
    "meshes": ["*.nif"],
    "textures": ["*.dds"],
    "blender": ["*.blend"],
    "json": ["*.json"],
    "videos": ["*.mp4", "*.mkv", "*.webm", "*.mov"],
    "images": ["*.png", "*.jpg", "*.jpeg", "*.webp"],
    "pdfs": ["*.pdf"],
}

for label, pats in patterns.items():
    found = []
    for pat in pats:
        found.extend(root.rglob(pat))
    print(f"{label.upper()}={len(found)}")
    for p in sorted(found)[:10]:
        print(f"  {p.relative_to(root)}")
    if len(found) > 10:
        print(f"  ... +{len(found)-10} more")

# Static JSON parse check.
bad = []
for p in root.rglob("*.json"):
    try:
        json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as e:
        bad.append((p, str(e)))
print(f"JSON_PARSE_FAILURES={len(bad)}")
for p, e in bad[:20]:
    print(f"  FAIL {p.relative_to(root)}: {e}")

for name in ["CHECKPOINT.md", "SPEC_DIGEST.md", "COMPAT_DIGEST.md"]:
    print(f"{name}={'YES' if (root / name).exists() else 'NO'}")

print("NOTE: this preflight is structural only. It cannot prove visual or in-game correctness.")
