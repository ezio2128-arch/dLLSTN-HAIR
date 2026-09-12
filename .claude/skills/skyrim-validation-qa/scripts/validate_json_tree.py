#!/usr/bin/env python3
import json, sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
files = sorted(root.rglob("*.json"))
bad = 0
for p in files:
    try:
        json.loads(p.read_text(encoding="utf-8-sig"))
        print(f"PASS {p}")
    except Exception as e:
        bad += 1
        print(f"FAIL {p}: {e}")
print(f"JSON_FILES={len(files)} FAILURES={bad}")
raise SystemExit(1 if bad else 0)
