# TN Chains gameplay matrix

## Damage reference

Provisional tuning reference:
`D_ref = 7 + (0.50 * attacker level)`

The exact formula may be tuned, but the hierarchy is fixed:
`Steel < Iron < Nordic Heavy < Domination`

## Four chains

| Chain | Role | Relative speed | Direct damage | Heavy humanoid KD | Cooldown | Cost / special |
|---|---|---|---|---:|---:|---|
| Iron | tutorial / balanced | normal | 1.00 x D_ref | 70% | 7 s | none |
| Steel | fast / agile | faster than Iron | 0.90 x D_ref | 80% | 6 s | lower damage, faster recovery |
| Nordic Heavy | power / commitment | slow, long telegraph | 1.10 x D_ref | 100% | 8 s | if knockdown, ground impact ~0.25 x D_ref provisional |
| Domination | unique Daedric / maximum | fastest | 1.25 x D_ref + Daedric progressive effect | 100% | 7 s | 15 Stamina + 5 Magicka; spikes/Daedric effect; temporary soul-capture theme |

Domination:
- associated with Molag Bal;
- unique artifact/reward path;
- not a normal craftable chain;
- if user has <15 Stamina OR <5 Magicka: do not start animation, do not pay cost, do not start cooldown;
- once launch begins, resource cost is paid even if the action later misses or is interrupted.

## Target resolution

| Target | Valid impact behavior |
|---|---|
| Unarmored/light humanoid | pull toward user + knockdown; creates attack window |
| Heavy humanoid | do not absurdly drag; knockdown probability depends on chain, otherwise stagger/stun |
| Large creature | strong reaction/stagger, little or no displacement |
| Giant | stagger only; never normal pull; never normal knockdown |
| Mammoth / equivalent huge | extreme resistance; limited reaction; never normal pull |
| Grounded dragon | do not pull dragon; pull USER toward dragon while user remains standing if possible |
| Flying / takeoff / landing dragon | dragon overpowers user; user is knocked down/dragged; do not force dragon to ground |

Domination does not override the dragon mass rule.

## Start/cancel logic

Before launch:
- invalid/no target -> no action, no cooldown;
- invalid LOS/range -> no action, no cooldown;
- incompatible stance -> no action, no cooldown.

After commitment:
- interruption during windup -> full cooldown;
- released but misses -> full cooldown + short miss recovery;
- active cooldown -> reject without stacking another cooldown.

Use the current project input design from `latest-design-authority.md`, not the older hardcoded R1 wording.

## NPC distribution intent after world unlock

High:
- bandits
- Forsworn
- Silver Hand

Medium:
- mercenaries
- deserters
- some vampires
- selected Dark Brotherhood / Thieves Guild style users where appropriate

Low:
- some irregular/veteran Stormcloak-type users

Extremely rare:
- thematic draugr / ancient guardians, potentially Nordic variant, with reduced physiological recovery because they are undead

Normally never:
- ordinary guards
- regular Imperial soldiers
- civilians
- animals

Optional if another mod adds them:
- pirates/corsairs/smugglers

Do not distribute anything before the world-unlock/tutorial gate.
