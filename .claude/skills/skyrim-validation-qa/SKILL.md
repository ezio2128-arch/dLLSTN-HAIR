---
name: skyrim-validation-qa
description: Evidence-based QA for Skyrim mods. Use when reviewing builds, claiming fixes, packaging test versions, comparing animation/physics results, or deciding whether a mod is ready for user testing or release.
---

# Skyrim Validation QA

## Evidence ladder

Use these exact labels.

### STATICALLY VALID
Examples:
- JSON parses.
- Papyrus compiles.
- C++ builds.
- expected files exist.
- FormID/path references are structurally consistent.
- HKX was produced by the export pipeline.

This does **not** prove the result looks good or works in Skyrim.

### VISUALLY VERIFIED
Requires direct inspection of:
- render,
- screenshots,
- ordered animation frames,
- or gameplay video.

For motion, inspect temporal sequence rather than one still image.

### IN-GAME VERIFIED
Requires observation in Skyrim under the intended modlist/runtime.

If the user must perform the final test, write a concise test build and exact test protocol. Mark the result `AWAITING IN-GAME VERIFICATION`.

## Required failure behavior

Never:
- say "fixed" because a file was edited;
- say "animation works" because HKX exists;
- say "compatible" because two mods load;
- say "tested" if no actual execution occurred.

If a tool/environment is unavailable, state the highest evidence level achieved.

## Visual comparison protocol

For animation/SMP:
1. keep the same camera/test action where possible;
2. compare reference and result side by side or phase by phase;
3. list visible improvements and regressions;
4. reject a version if it introduces body deformation, rigid/mechanical motion, obvious clipping, or reference divergence that matters to the requested feel.

## Packaging gate

A user-test build should include:
- version/name,
- files changed,
- installation path,
- requirements,
- known conflicts,
- expected behavior,
- exact test steps,
- rollback/removal instructions,
- current evidence level.
