#!/usr/bin/env python3
"""
Prepare a YouTube video as an animation-reference dataset.

Dependencies:
  - yt-dlp command or Python module
  - ffmpeg
  - ffprobe

This script does not bypass login, DRM, age gates, regional restrictions,
or platform access controls.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

def which_or_none(name: str):
    return shutil.which(name)

def run(cmd, check=True):
    print("+", " ".join(str(x) for x in cmd))
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.stdout.strip():
        print(p.stdout.strip())
    if p.stderr.strip():
        print(p.stderr.strip(), file=sys.stderr)
    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(map(str, cmd))}")
    return p

def safe_name(s: str) -> str:
    out = "".join(c if c.isalnum() or c in "-_" else "_" for c in s.strip())
    return out.strip("_") or "reference"

def timestamp_to_seconds(s: str) -> float:
    parts = s.strip().split(":")
    vals = [float(x) for x in parts]
    if len(vals) == 3:
        return vals[0] * 3600 + vals[1] * 60 + vals[2]
    if len(vals) == 2:
        return vals[0] * 60 + vals[1]
    if len(vals) == 1:
        return vals[0]
    raise ValueError(f"Invalid timestamp: {s}")

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--start", help="HH:MM:SS.mmm / MM:SS.mmm")
    ap.add_argument("--end", help="HH:MM:SS.mmm / MM:SS.mmm")
    ap.add_argument("--name", default="youtube_reference")
    ap.add_argument("--out", default="01_REFERENCES")
    ap.add_argument("--fps", type=float, default=None,
                    help="Override frame extraction FPS. Default: source-ish dense extraction from clip.")
    ap.add_argument("--contact-every", type=float, default=0.5,
                    help="Seconds between contact-sheet thumbnails.")
    return ap.parse_args()

def main():
    a = parse_args()
    name = safe_name(a.name)
    out = Path(a.out).resolve()
    raw_dir = out / "RAW_REFERENCES"
    clip_dir = out / "CLIPS"
    frame_dir = out / "FRAMES" / name
    contact_dir = out / "CONTACT_SHEETS"
    meta_dir = out / "METADATA"
    for d in [raw_dir, clip_dir, frame_dir, contact_dir, meta_dir]:
        d.mkdir(parents=True, exist_ok=True)

    ffmpeg = which_or_none("ffmpeg")
    ffprobe = which_or_none("ffprobe")
    ytdlp = which_or_none("yt-dlp")

    if not ffmpeg or not ffprobe:
        print(json.dumps({
            "status": "BLOCKED",
            "reason": "ffmpeg_or_ffprobe_missing",
            "ffmpeg": ffmpeg,
            "ffprobe": ffprobe
        }, indent=2))
        return 3

    if not ytdlp:
        # Try Python module without modifying environment.
        probe = subprocess.run([sys.executable, "-m", "yt_dlp", "--version"],
                               capture_output=True, text=True)
        if probe.returncode == 0:
            ytdlp_cmd = [sys.executable, "-m", "yt_dlp"]
        else:
            print(json.dumps({
                "status": "BLOCKED",
                "reason": "yt_dlp_missing",
                "install_hint": f"{sys.executable} -m pip install -U yt-dlp"
            }, indent=2))
            return 4
    else:
        ytdlp_cmd = [ytdlp]

    metadata_json = meta_dir / f"{name}.youtube.json"
    meta = run(ytdlp_cmd + ["--dump-single-json", "--no-playlist", a.url], check=False)
    if meta.returncode != 0:
        failure = {
            "status": "BLOCKED",
            "url": a.url,
            "start": a.start,
            "end": a.end,
            "reason": "youtube_metadata_or_access_failed",
            "stderr": meta.stderr[-4000:],
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
        metadata_json.write_text(json.dumps(failure, indent=2), encoding="utf-8")
        print(json.dumps(failure, indent=2))
        return 5

    try:
        ytmeta = json.loads(meta.stdout)
    except Exception:
        ytmeta = {"raw": meta.stdout}
    metadata_json.write_text(json.dumps(ytmeta, indent=2, ensure_ascii=False), encoding="utf-8")

    source_template = raw_dir / f"{name}.%(ext)s"
    download = run(ytdlp_cmd + [
        "--no-playlist",
        "-f", "bv*[height<=1080]+ba/b[height<=1080]/best",
        "--merge-output-format", "mp4",
        "-o", str(source_template),
        a.url
    ], check=False)

    if download.returncode != 0:
        failure = {
            "status": "BLOCKED",
            "url": a.url,
            "start": a.start,
            "end": a.end,
            "reason": "youtube_download_failed",
            "stderr": download.stderr[-4000:],
            "fallback": "Provide the shortest MP4 clip covering the requested range.",
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
        (meta_dir / f"{name}.failure.json").write_text(
            json.dumps(failure, indent=2), encoding="utf-8")
        print(json.dumps(failure, indent=2))
        return 6

    candidates = sorted(raw_dir.glob(f"{name}.*"))
    candidates = [p for p in candidates if p.suffix.lower() in {".mp4",".mkv",".webm",".mov"}]
    if not candidates:
        print("Downloaded file not found.", file=sys.stderr)
        return 7
    src = candidates[0]

    clip = clip_dir / f"{name}.mp4"
    ff = [ffmpeg, "-y"]
    start_sec = timestamp_to_seconds(a.start) if a.start else None
    end_sec = timestamp_to_seconds(a.end) if a.end else None
    if start_sec is not None:
        ff += ["-ss", f"{start_sec:.6f}"]
    ff += ["-i", str(src)]
    if end_sec is not None:
        if start_sec is not None:
            if end_sec <= start_sec:
                raise RuntimeError("--end must be after --start")
            ff += ["-t", f"{(end_sec - start_sec):.6f}"]
        else:
            ff += ["-t", f"{end_sec:.6f}"]
    ff += ["-c:v", "libx264", "-crf", "18", "-preset", "fast",
           "-c:a", "aac", "-b:a", "160k", str(clip)]
    # If both start/end given and ffmpeg rejects semantics, fallback to full source copy for later manual clip.
    clip_run = run(ff, check=False)
    if clip_run.returncode != 0:
        print("Clip extraction failed; copying full source as working clip.", file=sys.stderr)
        shutil.copy2(src, clip)

    # Probe
    probe_cmd = [
        ffprobe, "-v", "error",
        "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames",
        "-of", "json", str(clip)
    ]
    pr = run(probe_cmd, check=False)
    probe_data = {}
    if pr.returncode == 0:
        try:
            probe_data = json.loads(pr.stdout)
        except Exception:
            pass
    (meta_dir / f"{name}.probe.json").write_text(
        json.dumps(probe_data, indent=2), encoding="utf-8")

    # Dense frames: source fps by default, optional reduced/forced fps.
    vf = []
    if a.fps:
        vf.append(f"fps={a.fps}")
    frame_pattern = frame_dir / "frame_%06d.jpg"
    frame_cmd = [ffmpeg, "-y", "-i", str(clip)]
    if vf:
        frame_cmd += ["-vf", ",".join(vf)]
    frame_cmd += ["-q:v", "2", str(frame_pattern)]
    run(frame_cmd)

    # Contact sheet: sample every N seconds, tile.
    contact = contact_dir / f"{name}_contact.jpg"
    sample_fps = 1.0 / max(a.contact_every, 0.05)
    contact_filter = (
        f"fps={sample_fps},scale=320:-1,"
        "drawtext=text='%{pts\\:hms}':x=8:y=h-th-8:"
        "fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,"
        "tile=5x4:padding=4:margin=4"
    )
    contact_run = run([
        ffmpeg, "-y", "-i", str(clip),
        "-vf", contact_filter,
        "-frames:v", "1", str(contact)
    ], check=False)

    result = {
        "status": "READY",
        "url": a.url,
        "name": name,
        "source": str(src),
        "clip": str(clip),
        "frames": str(frame_dir),
        "contact_sheet": str(contact) if contact.exists() else None,
        "metadata": str(metadata_json),
        "probe": str(meta_dir / f"{name}.probe.json"),
        "start": a.start,
        "end": a.end
    }
    (meta_dir / f"{name}.prepared.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
