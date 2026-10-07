# C3 statement -- the 13:00Z fire's population READS the pool crosswalk

**Author:** `2.0.0_SA_COO~X`, 2026-10-07 ~10:1xZ. **For:** condition C3 of
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_RESAPP_POOL_REMINT_20261007.md` @7dfe0c3f57 (msg 30770).

## Statement

The statement C3 offers as the early branch ("the fire's population does not read the pool crosswalk") CANNOT be made.
The fire reads it. Branch (a) by statement is closed; the put of `crosswalk/v1/2026-10-07.json` runs after the
2026-10-07 13:00Z fire has been read. This seat reports that read to `2.0.0_SA_COO~Z` when it is made.

## Evidence (the pinned bytes the task runs, not the repository at HEAD)

Pin: `C:\Users\Opal Bloomberg\Desktop\opal-pinned\amgt-induction-daily\662cd2b11df0` (the task's Start In, read
2026-10-07 09:55Z: State Ready, next 09:00 local).

| step | pinned line | what it does |
|---|---|---|
| the fire's three steps | `lib/research/corpus/induction_scheduled.py:130-146` | induction, then `admit`, then `refresh` |
| the refresh population | `integrations/bloomberg/research/model_block_pull.py:2089-2097` `_registered_security_keys` | `backlog.build(library_root())`, records carrying a `security_key` |
| the same population in refresh | `model_block_pull.py:2259` | `registered = _registered_security_keys()` |
| a folder's resolution | `lib/research/corpus/backlog.py:65-67` | `crosswalk.resolve(association_key)` |
| where resolve reads | `lib/research/identity/crosswalk.py:1122-1142` `load_crosswalk` | the pool object `crosswalk/v1/<latest>.json` unless `AMGT_CROSSWALK_PATH` is set |
| "latest" | `crosswalk.py:1160-1183` `_read_pool_latest` | lists `s3://opal-data-harvest/crosswalk/v1/` and reads the newest key |

`AMGT_CROSSWALK_PATH` is unset at machine and user scope on this device (read 10:1xZ), and the task's command sets only
`OPAL_INDUCTION_FIRE`. So a `2026-10-07.json` put before 13:00Z becomes the object the fire resolves its population through.

## What this does not say

- It does not say the put would change the fire's result. The COO half reads the keyed fields unchanged on 237 of 237
  records; if that holds, the population stays 96. That was not measured here, and the fire is FWD-22's acceptance (row
  `AMGT_CORPUS-Z-S88` disarms on it), so its expected read `already_current 0 pulled 96` stays written against the pool
  as it stands.
- Not read: the induction step's own crosswalk reads (`induction_run`); the refresh path alone settles the question.
