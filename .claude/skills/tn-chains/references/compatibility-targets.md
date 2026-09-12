# TN Chains compatibility targets

These are integration targets from the True North design. Verify installed/current versions before patching.

## High/required areas

- True Directional Movement / target-lock integration:
  player targeting only; NPCs choose valid enemies independently.
- Open Animation Replacer:
  activate TN Chains clips only in the intended equipment/state.
- BFCO + MVC BFCO:
  avoid launching during incompatible attack states and return cleanly to melee.
- Payload Interpreter:
  useful for precise animation-timed events if the current setup uses it.
- Animation Motion Revolution:
  use only when controlled movement/root motion is actually required.
- XP32/XPMSE:
  actual skeleton/attachment validation is mandatory.
- Dodge frameworks / NPC dodge:
  telegraphed launches must be genuinely dodgeable.
- Precision / creature precision:
  avoid duplicate hit registration and incompatible collision behavior.
- Modern Stagger Lock:
  avoid stacked/duplicate reactions.

## Other compatibility areas

- Valhalla Combat / block systems:
  read actual defensive state and define one reaction path.
- IED:
  if used for visual display, prevent duplicate chain display.
- SPID/SkyPatcher/KID:
  may support distribution/keywords, but must not bypass the world-unlock gate.
- dragon combat mods:
  distinguish grounded vs flight/transition states and never accidentally trigger a dragon-fall subsystem.

## Patch policy

Do not edit third-party mod files unless unavoidable.
Prefer:
- runtime detection,
- OAR conditions,
- adapters,
- project-owned configs,
- project-owned patches.
