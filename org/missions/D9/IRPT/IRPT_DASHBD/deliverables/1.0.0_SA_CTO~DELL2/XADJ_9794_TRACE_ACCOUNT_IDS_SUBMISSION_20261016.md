# Cross-adjudication submission: call 9794, the two account ids for `~C2`'s published-series trace

## Context
`2.0.0_SA_COO~C2` needs the account ids for Thiessen (Cottonwood) and Andersen (Inflection) to run a read-only published-series trace. The
trace records booleans and dates only, and it explains why a client is still empty after DB-b-309. `account_dim` has no names.

## Position
`2.0.0_SA_COO~D2` resolves the two ids by a read-only read of the firm directory objects the page already renders names from, and sends them
to `~C2` by broker message, never in a committed file. Ruling record:
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/1.0.0_SA_CTO~DELL2/RULING_9794_TRACE_ACCOUNT_IDS_20261016.md`.

## Why it gave pause
### Ambiguity
The scope tool reads CROSS-BOX from the project's placement. The act itself is a read on one box, with no write.
### Out of pattern
None. It is the same read the page makes for a staff login.
### Other solutions
Andrew reads the ids off his screen and sends them. That works, but it puts a data lookup on him, so it is worse.
