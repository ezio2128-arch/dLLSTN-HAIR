---
name: skyrim-modding-core
description: Specialist workflow for Skyrim SE/AE mod engineering. Use when creating, adapting, patching, packaging, or auditing Skyrim mods involving MO2-style layouts, OAR, SKSE, Papyrus, NIF/HKX assets, xEdit/Creation Kit data, or compatibility with a modern modlist.
---

# Skyrim Modding Core

Use this Skill as the default engineering discipline for Skyrim SE/AE work.

## Non-negotiable working rules

1. **Inspect before inventing.**
   - Search the repository for an existing implementation, mod dependency, animation, mesh, script, config, or proven subsystem before creating a replacement.
   - Prefer `existing working system -> adapt/patch -> validate` over rebuilding a complex Skyrim subsystem from zero.
   - Never assume a framework API, record layout, event name, OAR condition, node name, FormID, path, or behavior event. Verify from project files or authoritative documentation.

2. **Do not equate file creation with success.**
   Classify every claim using exactly one of:
   - `STATICALLY VALID`: files/configs parse, compile, or pass deterministic structural checks.
   - `VISUALLY VERIFIED`: screenshots/renders/video were inspected and compared against a reference.
   - `IN-GAME VERIFIED`: the behavior was actually observed in Skyrim.
   Never promote a lower level to a higher one without evidence.

3. **Work from a reversible copy.**
   - Preserve original/reference assets.
   - Keep generated files in a dedicated work tree or build tree.
   - Record changed files in `CHANGELOG.md`.
   - Do not overwrite a known-good baseline without a backup or version-control checkpoint.

4. **Use disk as project memory.**
   Maintain compact state:
   - `CHECKPOINT.md`
   - `CHANGELOG.md`
   - `SPEC_DIGEST.md`
   - `COMPAT_DIGEST.md`
   - `STATE/WORKER_LOCK.json`
   Read these first in a resumed session. Do not reread large PDFs or entire modlists unless their digest is missing/stale.

5. **One writer at a time.**
   - Assume only one active worker may modify a project.
   - If `STATE/WORKER_LOCK.json` indicates another active writer, stop and report the conflict.
   - Research-only work may continue without writing project outputs.

## Tool discovery

Before a task depends on Blender, hkx tools, ffmpeg, xEdit, Creation Kit, NifSkope, PyNifly, Papyrus compiler, SKSE headers, or game executables:
1. Detect whether the tool actually exists in the current environment.
2. Record its version/path when possible.
3. If unavailable in a cloud VM, continue all work that can be performed without it and clearly mark what remains unverified.
4. Never fabricate execution output from a tool that is not present.

## Skyrim project audit order

When entering an unfamiliar Skyrim mod repository:

1. Read top-level README/spec/checkpoint files.
2. Inventory:
   - plugins: `.esp`, `.esm`, `.esl`
   - scripts: `.psc`, `.pex`
   - native code: C/C++/CMake
   - animation: `.hkx`, OAR folders/config
   - meshes/textures: `.nif`, `.dds`
   - SKSE/INI/JSON/TOML configs
   - build/package scripts
3. Identify runtime dependencies and exact game/runtime target.
4. Identify which artifacts are source, generated, reference-only, and rejected.
5. Build a dependency/ownership map before edits.

## Compatibility strategy

Prefer modular integration:
- conditions/adapters over editing third-party files;
- OAR conditions over replacing global animation assets;
- SkyPatcher/KID/SPID only when they preserve progression and do not distribute content prematurely;
- SKSE hooks when Papyrus cannot reliably provide required state/timing;
- one authoritative reaction path for stagger/knockdown to avoid duplicated events.

## Completion report

For every substantial task, end with:
- `TASK`
- `STATUS`
- `INPUTS`
- `FILES CHANGED`
- `STATIC VALIDATION`
- `VISUAL VALIDATION`
- `IN-GAME VALIDATION`
- `KNOWN LIMITATIONS`
- `NEXT ACTION`

If visual or in-game evidence is absent, say so explicitly.
