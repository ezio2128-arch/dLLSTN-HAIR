#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil, subprocess
from pathlib import Path

def to_seconds(s: str) -> float:
    parts = s.strip().split(":")
    nums = [float(x) for x in parts]
    if len(nums) == 3:
        return nums[0]*3600 + nums[1]*60 + nums[2]
    if len(nums) == 2:
        return nums[0]*60 + nums[1]
    if len(nums) == 1:
        return nums[0]
    raise ValueError(s)

ap = argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("output")
ap.add_argument("--start", required=True)
ap.add_argument("--end", required=True)
a = ap.parse_args()

ffmpeg = shutil.which("ffmpeg")
if not ffmpeg:
    raise SystemExit("ffmpeg not found")

start = to_seconds(a.start)
end = to_seconds(a.end)
if end <= start:
    raise SystemExit("--end must be after --start")
duration = end - start

out = Path(a.output)
out.parent.mkdir(parents=True, exist_ok=True)
cmd = [
    ffmpeg, "-y", "-ss", f"{start:.6f}", "-i", a.input,
    "-t", f"{duration:.6f}",
    "-c:v", "libx264", "-crf", "18", "-preset", "fast",
    "-c:a", "aac", "-b:a", "160k", str(out)
]
print("+", " ".join(cmd))
raise SystemExit(subprocess.call(cmd))
