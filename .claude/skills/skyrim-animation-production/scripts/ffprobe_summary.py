#!/usr/bin/env python3
import json, shutil, subprocess, sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("usage: ffprobe_summary.py VIDEO")
        return 2
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        print("FFPROBE_NOT_FOUND")
        return 3
    p = Path(sys.argv[1])
    if not p.exists():
        print("VIDEO_NOT_FOUND")
        return 4
    cmd = [
        ffprobe, "-v", "error",
        "-show_entries", "format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames",
        "-of", "json", str(p)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr.strip())
        return r.returncode
    data = json.loads(r.stdout)
    print(json.dumps(data, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
