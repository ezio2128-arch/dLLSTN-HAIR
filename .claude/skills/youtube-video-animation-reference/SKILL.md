---
name: youtube-video-animation-reference
description: YouTube-URL-driven visual reference workflow for Claude Code. Use when a Skyrim animation should be reconstructed or evaluated from one or more YouTube videos. Downloads reference media when allowed, creates timestamped clips and frame sequences, analyzes motion phases, drives Blender animation iteration, and compares generated previews against the original reference before export.
---

# YouTube Video -> Skyrim Animation Reference Loop

This Skill turns a public YouTube URL into **visual evidence** for an animation workflow.

It is not enough to read the title, transcript, description, subtitles, or comments. For animation work, the model must inspect actual video frames.

## Input contract

Accept any of:

1. A YouTube URL alone.
2. A YouTube URL plus one or more timestamp ranges.
3. Multiple YouTube URLs where each reference has a declared purpose.
4. A local video/clip as fallback if YouTube access is unavailable.

Preferred user syntax:

```text
REFERENCE 1
URL: https://www.youtube.com/watch?v=...
RANGE: 00:41.200-00:46.800
PURPOSE: left-arm windup, release, chain lag

REFERENCE 2
URL: https://youtu.be/...
RANGE: 01:12.000-01:15.500
PURPOSE: recovery and body-weight transfer
```

If the user provides only a URL, inspect metadata and create a coarse contact sheet first. Narrow the useful time range before dense frame extraction.

## Legal / asset rule

Reference footage is used for **motion study and visual comparison only**.

Do not:
- redistribute downloaded reference video;
- extract proprietary game meshes, textures, audio, animation files, or other copyrighted assets from the reference;
- claim that an original TN Chains animation is an extracted Witcher animation.

Create an original animation informed by visible motion.

Prefer short working clips and frame extracts over keeping full videos in the repository.

## Required tools

Attempt discovery in this order:
- `yt-dlp`
- `ffmpeg`
- `ffprobe`

If `yt-dlp` is not installed, install it only if the environment/project policy permits it:

```bash
python -m pip install -U yt-dlp
```

If FFmpeg is absent, inspect the repository/setup mechanism. Do not claim visual video analysis if frames cannot be obtained.

## YouTube access workflow

Use `scripts/youtube_reference.py`.

Example:

```bash
python .claude/skills/youtube-video-animation-reference/scripts/youtube_reference.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --start 00:41.200 \
  --end 00:46.800 \
  --name witcher_release \
  --out 01_REFERENCES
```

The script should create a structure similar to:

```text
01_REFERENCES/
  RAW_REFERENCES/
  CLIPS/
    witcher_release.mp4
  FRAMES/
    witcher_release/
      frame_000001.jpg
      ...
  CONTACT_SHEETS/
    witcher_release_contact.jpg
  METADATA/
    witcher_release.json
```

## Network / YouTube failure behavior

YouTube access is **not guaranteed** in a cloud VM.

If the download fails because of:
- HTTP 403/429,
- bot verification,
- age restriction,
- login/cookies,
- regional restriction,
- network policy,
- unavailable/private video,

then:

1. Preserve the URL, requested range, and purpose in `REFERENCE_MANIFEST.md`.
2. Record the exact failure.
3. Do not invent visual observations.
4. Ask only for the smallest missing artifact:
   - preferably the short MP4 clip for the requested timestamp range;
   - otherwise the source MP4.
5. Resume at frame extraction; do not restart project analysis.

Do not bypass access controls, DRM, login requirements, or platform restrictions.

## Frame extraction strategy

### Coarse pass
For an unknown long video:
- create a contact sheet at low temporal density;
- identify candidate action windows.

### Dense pass
For the selected action:
- preserve source FPS when practical;
- otherwise extract enough consecutive frames to understand temporal ordering;
- never use only one screenshot to infer a dynamic motion.

For fast flexible-weapon motion, use dense frames around:
- anticipation;
- reversal;
- elbow acceleration;
- wrist acceleration;
- release;
- maximum extension;
- tension;
- impact/pull;
- recovery.

## Motion analysis output

Create `REFERENCE_ANALYSIS.md` with:

```text
SOURCE
URL:
CLIP:
FPS:
RESOLUTION:
RANGE:

MOTION PHASES
1. STANCE
2. ANTICIPATION
3. LOAD
4. PELVIS REVERSAL
5. TORSO INITIATION
6. SHOULDER INITIATION
7. ELBOW LEAD
8. WRIST ACCELERATION
9. RELEASE
10. CHAIN EXTENSION
11. TENSION
12. IMPACT/PULL
13. FOLLOW-THROUGH
14. RECOVERY
```

For each phase describe only what is supported by visible evidence:
- approximate timestamp/frame;
- pelvis orientation/change;
- torso rotation/flexion;
- shoulder elevation/protraction/retraction;
- elbow path;
- wrist/hand path;
- stance/foot loading;
- right-hand weapon behavior;
- visible chain state;
- center-of-mass tendency;
- occlusions/uncertainty.

Do not invent invisible joint motion. Mark uncertain observations.

## Reference -> Blender loop

After reference analysis:

1. Build or modify the animation on the **actual intended XP32/XPMSE-compatible rig**, not a proxy stick figure.
2. Produce a blockout first.
3. Render a preview from readable cameras.
4. Extract preview frames.
5. Phase-align generated preview to reference.
6. Compare.
7. Correct failed phases.
8. Repeat.

Do not export a final HKX before the visual loop reaches the project's acceptance threshold.

## Self-comparison loop

Create/update `REFERENCE_COMPARISON.md`.

Evaluate at minimum:

| Criterion | Status | Evidence |
|---|---|---|
| stance silhouette | PASS/PARTIAL/FAIL | |
| anticipation/readability | | |
| pelvis timing | | |
| torso timing | | |
| shoulder path | | |
| elbow lead | | |
| wrist plane | | |
| right-hand weapon preservation | | |
| chain lag | | |
| release timing | | |
| extension timing | | |
| tension timing | | |
| follow-through | | |
| recovery | | |
| absence of robotic circular motion | | |
| absence of rig deformation | | |

Use a numeric score only as an iteration aid, never as scientific ground truth.

Recommended gate:
- no critical FAIL;
- no automatic rejection condition from `skyrim-animation-production`;
- overall visual assessment >= 8.5/10 if a score is used.

## Phase alignment

Do not compare frames only by equal frame number.

Reference and generated animation may have different FPS/duration.

Align them by semantic phase:
- stance vs stance,
- release vs release,
- max extension vs max extension,
- tension vs tension,
- recovery vs recovery.

Timing differences should be measured separately from pose differences.

## Comparison artifacts

When tooling permits, generate:
- side-by-side reference/generated frame pairs;
- 50% alpha overlays;
- difference images;
- contact sheets.

These artifacts are aids for visual inspection. Pixel difference alone must never decide animation quality because camera, rig, lighting, proportions and rendering differ.

## TN Chains integration

When invoked for TN Chains:
- also load the `tn-chains` Skill;
- use Witcher footage as motion-language reference, not a source asset;
- compare against project failure archaeology to ensure a new version does not repeat rejected patterns;
- preserve the right-hand weapon identity;
- preserve physical left-hand chain presentation;
- enforce chain lag, release-before-extension, and extension-before-tension;
- reject spell/staff/gun presentation.

## Evidence levels

Downloaded/extracted frames alone: not validation of the generated animation.

Generated Blender preview inspected against reference:
`VISUALLY VERIFIED` only if it passes the comparison gate.

HKX generated:
still only `STATICALLY VALID` unless preview/in-game evidence exists.

Observed inside Skyrim:
`IN-GAME VERIFIED`.
