# Project-state template

## CHECKPOINT.md
- Current objective:
- Last known-good build:
- Last completed task:
- Current blocker:
- Next action:
- Evidence available:
- Evidence missing:

## SPEC_DIGEST.md
Keep only current, authoritative rules. Mark superseded rules explicitly.

## COMPAT_DIGEST.md
For every relevant mod/framework:
- version if known
- interface relied on
- conflict risk
- patch method
- validation status

## STATE/WORKER_LOCK.json
```json
{
  "worker": null,
  "status": "idle",
  "started_at": null,
  "scope": null
}
```
