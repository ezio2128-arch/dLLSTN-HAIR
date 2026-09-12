---
name: skyrim-animation-production
description: Reference-driven Skyrim animation workflow for XP32/XPMSE, Blender, HKX, OAR, BFCO and related combat animation systems. Use when creating, retargeting, repairing, reviewing, or exporting character animations where visual quality and biomechanical plausibility matter.
---

# Skyrim Animation Production

This Skill exists to prevent technically valid but visually poor animations.

## Mandatory pipeline

Never jump from text description directly to final HKX.

Use:
`REFERENCE -> CAPTURE -> ANALYSIS -> BLOCKOUT -> PREVIEW -> COMPARISON -> CORRECTION -> EXPORT -> IN-GAME TEST`

If reference video exists:
1. Probe FPS/duration with `ffprobe` if available.
2. Extract or use consecutive frames around the relevant motion.
3. Identify phase boundaries and body sequencing.
4. Build the animation from the reference evidence, not from memory.
5. Render comparable previews before HKX export.
6. Compare reference and result at matching motion phases, not merely matching absolute frame numbers.

## Visual evidence rules

- A valid `.blend` is not proof of a good animation.
- A valid `.hkx` is not proof of a good animation.
- Correct XP32 bone names are not proof of a good animation.
- A written claim such as "biomechanically correct" is not proof.
- The character must be inspected in motion.

Use `references/animation-quality-gates.md`.

## Flexible-chain / whip-like motion

For flexible weapons:
- Do not animate the chain as rigid cylinders or a stiff rod.
- Treat the distal mass as delayed relative to the hand.
- Preserve distinct states: slack -> trailing arc -> progressive extension -> tension -> impact/pull.
- Release must precede maximum extension.
- Tension must occur after extension, not on the same keyframe as release.
- Avoid a perfect mechanical circle unless a reference clearly shows one.
- Avoid wrist-only spinning. Power should propagate through lower body/pelvis/torso/shoulder/elbow, with wrist guidance late in the sequence.

## Human sequencing baseline

Unless contradicted by a stronger reference:
1. load/reversal begins in pelvis,
2. torso follows,
3. shoulder follows torso,
4. elbow leads the accelerating hand,
5. wrist shapes the plane late,
6. follow-through overlaps rather than stopping every body part together,
7. recovery recenters body before the flexible object fully settles.

Maintain asymmetry. Do not peak pelvis, torso, shoulder, elbow, wrist, and chain on one frame.

## XP32 / Skyrim constraints

- Confirm the actual skeleton used by the project.
- Preserve transforms and naming expected by the export pipeline.
- Do not create a proxy skeleton and assume equivalence.
- If using Blender automation, save a `.blend` and render previews before export.
- If retargeting an existing animation, document source rig, destination rig, mapping, scaling, root treatment, and any hand/weapon constraints.
- If OAR/BFCO controls activation, animation QA includes checking that the clip is selected only in the intended state.

## Combat readability

An animation must communicate:
- anticipation / telegraph,
- commitment,
- release,
- impact/tension,
- recovery.

The right timing matters for gameplay. Events such as projectile release, hit confirmation, tension, pull, and recovery should align with visible motion. Do not place all gameplay events at the same timestamp.

## Failure correction

If a preview looks wrong:
1. identify one or two visible causes,
2. modify only those causes,
3. re-render the same viewpoints,
4. compare again.

Do not rebuild the entire animation blindly after each failure.
