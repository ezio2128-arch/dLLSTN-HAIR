---
name: skyrim-papyrus-skse
description: Runtime logic and state-machine workflow for Skyrim Papyrus and SKSE-based mods. Use when implementing input/state handling, cooldowns, target selection, NPC logic, distribution gates, animation events, combat reactions, or native/Papyrus division of responsibility.
---

# Skyrim Papyrus / SKSE Runtime Logic

## Architecture rules

Use an explicit state machine for combat mechanics. Avoid scattered booleans that can produce impossible combinations.

Typical states:
- unavailable/locked,
- ready,
- windup,
- committed/released,
- hit/tension,
- miss,
- pull/reaction,
- recovery/cooldown,
- interrupted.

Every transition should define:
- entry condition,
- side effects,
- animation/event coupling,
- resource cost,
- cooldown behavior,
- cancellation behavior.

## Input

Do not hardcode a physical controller button if the project defines a logical action.
Integrate with the project's logical input/action layer and respect remapped controls.

## Player and NPC logic

Do not force player-specific targeting assumptions onto NPCs.
Separate:
- player target acquisition,
- NPC target selection,
- shared validation,
- shared impact resolution.

## Timing

Animation-visible events should be the timing authority whenever possible for:
- release,
- impact/tension,
- pull,
- recovery.

Do not fire physics early because a timer "approximately matches" the animation if an animation event can provide a stronger signal.

## Performance

- Avoid high-frequency Papyrus polling when an event, SKSE hook, cached state, or native query can provide the same information.
- Keep NPC distribution quest/progression-gated.
- Do not reset whole inventories to add one item.
- Clamp forces/displacements.
- Avoid multiple stagger/knockdown systems reacting to one hit.

## Debugging

For every gameplay branch, log enough to distinguish:
- blocked before start,
- interrupted during windup,
- released but missed,
- hit and resolved,
- cooldown rejected,
- invalid target state,
- missing dependency/event.

Logs are evidence of code paths, not proof that animation/physics looked correct.
