# TN Chains — latest design authority

This file intentionally resolves conflicts between older design documents and the latest project direction.

## Precedence

When information conflicts, use:
1. this file / explicit newer project override;
2. current project checkpoint/spec digest;
3. gameplay PDF for rules not superseded;
4. current implementation as evidence of what works, not as design authority;
5. rejected prototypes only as negative examples.

## Current override: left-hand physical tool

Older TN Chains documentation described a "third tool" that did not occupy either hand and was triggered by a dedicated R1 action.

**That presentation is superseded.**

Current direction:
- TN Chain is a physical **left-hand/off-hand weapon/tool role**.
- The player chooses TN Chain instead of shield, left-hand spell, or second weapon while using it.
- The primary/right-hand weapon remains the main weapon.
- Input must follow the game's **logical left-hand action**, not a hardcoded physical controller button.
- Do not recreate the rejected "invisible third hand" behavior.
- Do not make it feel like a spell or staff.
- Chain should be visibly present around/in the left hand/forearm before release.

## Current reuse strategy

Previous experiments established that Pull Mastery-style behavior already provides a promising working base:
`visible projectile/chain -> impact -> pull`.

Preserve working mechanics where possible and replace the presentation/animation layer rather than recreating projectile/pull from scratch.

Relevant prior experiments:
- whip-style direct reuse conflicted with BFCO/MVC behavior;
- a Pull Mastery prototype achieved ranged impact/pull but looked like a gun/artifact;
- spell-left-hand conversion was rejected because it felt magical and lacked physical spinning/windup;
- current target is a physical left-hand object with a full equip/idle/precharge/loop/release sequence.

## Visual identity

Essential sequence:
`visible chain at hand/forearm -> physical windup/spin -> release -> chain exits toward target -> tension -> target/user reaction -> recovery`

The reference target is a *feel and movement language*, not copied proprietary assets.
