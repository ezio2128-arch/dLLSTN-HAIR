---
name: skyrim-smp-hair
description: Diagnostic and tuning workflow for Skyrim SMP/FSMP hair and flexible physics assets. Use when fixing hair motion, clipping, collisions, unstable bones, floating decorations, jump response, wind response, or comparing physics configs against a known-good reference.
---

# Skyrim SMP / Hair Physics

Treat SMP work as a visual/physics tuning problem, not as an XML-editing problem.

## Required test set

Keep repeatable short captures for:
- idle,
- run,
- sudden stop,
- left/right direction change,
- jump,
- wind or exposed outdoor motion.

When comparing versions, use the same character, hair, camera, action, and approximate environment.

## Diagnostic categories

Classify visible problems before editing:
- too stiff,
- too loose,
- excessive lateral sway,
- high-frequency shaking,
- slow settling,
- over-damped/dead,
- body clipping,
- neck/back penetration,
- jump opening missing,
- bun/short-section static,
- rings/decorations detached or floating,
- collision instability/explosion,
- inconsistent behavior by hair length.

Do not change many unrelated parameters at once.

## Tuning discipline

1. Capture baseline.
2. Identify one visible failure.
3. Identify the minimum parameters/bones/colliders likely responsible.
4. Modify only those.
5. Re-run the same test.
6. Compare.
7. Keep the change only if the evidence improves.

## Bone/constraint principles

- Long hair needs enough articulated sections to bend progressively; a single rigid section will not reproduce natural lag.
- Short hair can still show weight response, but should not behave like long cloth.
- Buns should react slightly with the parent mass, not remain world-static and not swing like a ponytail.
- Decorations should follow intended hair bones and not use an unrelated transform.
- More bones are not automatically better; each extra degree of freedom can increase instability.
- Confirm collision shapes and bone ownership before compensating with extreme damping.

## Collision principles

- Verify the actual body/skeleton/collision setup used by the project.
- Separate "no collider exists" from "collider exists but constraint permits penetration".
- Diagnose clipping at the exact motion phase where it occurs.
- Do not hide clipping by simply making the hair rigid unless the design calls for rigid hair.

## Evidence levels

XML parses -> `STATICALLY VALID`.
Captured motion visibly improves -> `VISUALLY VERIFIED`.
Observed in actual Skyrim under the intended setup -> `IN-GAME VERIFIED`.
