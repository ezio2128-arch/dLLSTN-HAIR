---
name: tn-chains
description: Project-specific engineering and animation Skill for True North TN Chains. Use whenever creating, repairing, auditing, animating, balancing, integrating, or packaging the TN Chains Skyrim mod, including the four chain variants, Pull Mastery-derived mechanics, target/mass rules, OAR/BFCO integration, NPC use, and visual reference matching.
---

# TN Chains

This is the project authority for TN Chains work.

Before implementation, also read the sibling Skills:
- `.claude/skills/skyrim-modding-core/SKILL.md`
- `.claude/skills/skyrim-animation-production/SKILL.md`
- `.claude/skills/skyrim-papyrus-skse/SKILL.md`
- `.claude/skills/skyrim-nif-textures/SKILL.md`
- `.claude/skills/skyrim-validation-qa/SKILL.md`
- `.claude/skills/youtube-video-animation-reference/SKILL.md` when URLs/video references are supplied

Read `references/latest-design-authority.md` first. It contains project decisions that override older documents when they conflict.

## Core objective

Create a Skyrim combat technique with a **physical chain in the left-hand/off-hand role**, while the main weapon remains in the right hand.

The intended feel is inspired by cinematic chain/whip techniques, but all implementation assets must be original or legitimately reusable from installed/openly licensed mod resources. Reference footage is for motion/design study, not asset extraction.

The chain must feel:
- physical,
- readable,
- weighty,
- tactically useful,
- integrated into Skyrim combat,
- visually credible before it is called finished.

## Current implementation strategy

Do **not** restart the mechanic from zero unless proven necessary.

Preferred direction:
1. preserve/reuse the already working projectile/impact/pull behavior derived from the project's Pull Mastery experiments;
2. replace staff/magic-like presentation with a physical left-hand chain presentation;
3. build the visible sequence:
   `equip -> idle -> precharge -> loop/spin -> release -> extension -> tension -> impact/pull -> recovery`
   plus a miss/fail recovery;
4. use OAR/BFCO/related project frameworks only where they solve a concrete problem;
5. keep the right-hand weapon available visually and return to melee quickly.

## Animation standard

The animation is not acceptable merely because it exports.

Use reference evidence and enforce:
- sword/main weapon remains right-hand identity;
- left arm begins from a compact guarded/preparation position;
- pelvis/torso contribute before the arm accelerates;
- shoulder follows torso;
- elbow leads a soft arm;
- wrist guides late;
- chain mass visibly lags;
- no robotic perfect circles;
- no tiny/proxy arm;
- no deformed body;
- no rigid-stick chain;
- no simultaneous release/extension/impact keyframe;
- pull recruits body/legs/back, not only shoulder;
- recovery is short enough to preserve combat flow.

Read:
- `references/animation-acceptance.md`
- `references/failure-archaeology.md`

## Vertical-slice rule

Do not implement all four variants simultaneously before one chain works.

First produce an **Iron Chain vertical slice**:
- physical left-hand chain identity;
- target validation;
- windup/telegraph;
- release;
- projectile/chain travel;
- real hit or miss;
- tension/pull aligned to animation;
- mass-aware reaction;
- cooldown;
- clean recovery;
- a preview that passes the visual gates.

Only then parameterize Steel, Nordic Heavy, and Domination.

## Four-chain design

Use `references/gameplay-matrix.md`.

The variants share the same mechanic and mass rules but differ in:
- animation tempo/commitment,
- direct damage,
- heavy-armor knockdown probability,
- cooldown,
- unique effects/costs.

Do not make four unrelated systems.

## NPC rules

NPCs may use chains against valid enemies without requiring the player's TDM lock.
NPC use must:
- obey range/LOS/state/cooldown;
- telegraph visibly;
- be dodgeable rather than auto-hit;
- avoid spam;
- respect faction/distribution rules and world-unlock progression.

## Target/mass rules

Do not use a generic "pull everything" force.

Resolve target categories explicitly:
- unarmored/light humanoid,
- heavy humanoid,
- large creature,
- giant,
- mammoth/equivalent huge actor,
- grounded dragon,
- flying/takeoff/landing dragon.

Read `references/gameplay-matrix.md`.

## Progression

The world distribution is gated by the tutorial/unlock state. Before unlock:
- no chain NPC distribution,
- no chain loot distribution,
- no crafting access,
- no accidental early system activation.

The Iron Chain tutorial encounter is the baseline entry point unless a newer project override says otherwise.

## Compatibility

Read `references/compatibility-targets.md`.
Do not patch every listed mod blindly. First identify which interface the current build actually uses.

## Work sequence

1. Read checkpoints/digests.
2. Inventory current working mod and rejected/prototype files.
3. Write `TN_CHAINS_UNDERSTANDING.md` before major implementation if the repository does not already contain an equivalent current document.
4. Identify what is already mechanically functional.
5. Build/fix Iron vertical slice first.
6. Render/capture animation evidence.
7. Compare to reference and correct.
8. Export/integrate only after visual blockout is acceptable.
9. Produce installable test build.
10. If Skyrim cannot run in the current environment, stop at `AWAITING IN-GAME VERIFICATION` and give exact test steps.

## No false completion

A successful build is not automatically a successful mod.
A compiled HKX is not automatically an acceptable animation.
A working pull with a bad visual presentation is not finished.
