# Generic combat mechanic state machine

```text
LOCKED
  -> READY when progression + equipment valid

READY
  -> WINDUP when logical input + target + stance valid
  -> READY when input rejected (no cooldown)

WINDUP
  -> INTERRUPTED if struck/cancelled
  -> RELEASED on release event

INTERRUPTED
  -> COOLDOWN if design says commitment already consumed

RELEASED
  -> MISS if trajectory invalidated
  -> HIT on confirmed contact

MISS
  -> COOLDOWN

HIT
  -> TENSION/PULL or special mass response
  -> COOLDOWN after recovery

COOLDOWN
  -> READY when cooldown completes and equipment remains valid
  -> LOCKED if progression/equipment invalid
```
