# Animation quality gates

## Gate A — Skeleton integrity
PASS only if:
- expected rig/skeleton is actually used;
- no obvious scaling or transform corruption;
- no deformed body caused by bad binding/retargeting;
- weapon/hand roles are preserved.

## Gate B — Motion structure
PASS only if:
- anticipation is readable;
- acceleration is not robotic;
- motion is not a perfect mechanical loop unless required;
- body sequencing shows overlap;
- flexible object lags and extends progressively.

## Gate C — Reference similarity
Compare silhouettes and motion phases:
- stance
- anticipation
- load
- torso initiation
- shoulder/elbow acceleration
- release
- extension
- tension/impact
- follow-through
- recovery

Record mismatches. A textual description is insufficient.

## Gate D — Gameplay timing
Check visible animation against:
- input/start
- release event
- hit/tension event
- pull resolution
- cancel window
- recovery/control return

## Gate E — Skyrim
Only after the above:
- export HKX;
- wire OAR/BFCO/behavior;
- test in game.

A result can be `STATICALLY VALID` while still failing B/C/D.
