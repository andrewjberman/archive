# AMGT_CORPUS round 5 -- never-widen pair, the AIA Group registration (one call, one put, the 95th folder)

The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`ledger/`). **Authority for the act:** Andrew-direct ~23:1xZ, verbatim *"go ahead with AIA"*
(`org/tier1_exec/2.0.0_SA_COO~X/deliverables/ANDREW_DIRECT_20260925_231xZ_GO_AHEAD_WITH_AIA.md`); the one Bloomberg identity
call sits under R-21 as the earlier fires did.

## COO HALF -- `2.0.0_SA_COO~X`

### THE ACT

The same producer and the same table, now 42 rows (AIA Group -> 1299 HK added, tier DOC: its memo names "AIA Group Limited
(HKEX: 1299 | ADR: AAGIY)"), ONE run after `bloomberg_health`:

    OPAL_INDUCTION_FIRE=1 python -m lib.research.corpus.induction_run --fire --as-of <today UTC> \
        --evidence org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/UNRESOLVED40_CALLS_20260924.json

41 rows are already registered and skip with no call; AIA is called: **at most 1 Bloomberg reference call**, one batch call,
at most one conditional put.

### THE KEY -- named for BOTH sides of midnight, because `--fire` refuses any as-of but today's

- **run before 00:00Z -> `s3://opal-data-harvest/crosswalk/v1/2026-09-25.json`**: before-state (23:12:03Z) 2 versions, latest
  VersionId `PoGljdVKce67e4GnBEY5wVab7wdkRJZd` (05:50:52Z, 593054 bytes), 0 delete markers. Rollback: copy that VersionId forward.
- **run at or after 00:00Z -> `s3://opal-data-harvest/crosswalk/v1/2026-09-26.json`**: before-state ABSENT (23:12:03Z). The
  newest-key reader serves it on landing. Rollback without a delete: put the 09-25 latest body (`PoGljdVKce67e4GnBEY5wVab7wdkRJZd`)
  as a new version of the 09-26 key -- its own `as_of` field then discloses 2026-09-25.
Whichever applies is re-measured immediately before the put and named in the fire's commit; no other key is written.

### BLAST RADIUS -- as every earlier fire's

1. One conditional put on the key above (IfMatch, digest-differs only, read-back raises on mismatch).
2. At most 1 write-once raw identity landing (`bloomberg/harvest/bronze/identity/security_key=1299_HK_Equity/...`).
3. `lib/research/identity/registrations.json` +1 row, committed after the run or reverted.
NOT written: any other key, `universe/v1/`, any delete.

### WRITER CENSUS -- N = 2, unchanged

`add_security._mint_pool` (this act) and `crosswalk.main --write-pool`; both build through `crosswalk.build_crosswalk` and both
pass the live folder list (`5ef2158828`).

### EXPECTED OUTCOME -- the pre-flight on committed bytes (identity tree 0 modified), 42-row table

`already-registered 41, called 1 (APPEND); records 235 -> 236, MEASURED 235 -> 236, UNRESOLVED 0; registered 47 -> 48; twins
0; multi-claimed 0; 235 of 235 prior keys present; 1 new key (1299_HK_Equity); folder-form coverage 42 of 42; VERDICT PASS`.
The disclosure then reads `folders_in_records 95 == research_folders_live 95` (the library reads 95 at 23:0xZ). Branches: a call
that does not MEASURE leaves AIA unrecorded and the put still carries the rebuilt document (folders_in_records 94 vs live 95,
disclosed); nothing lands at all -> `pool_puts 0`.

**Discriminator after the put:** the key's version count +1; `folders_in_records` == `research_folders_live` == the records'
own folder count == 95; twins 0, multi-claimed 0; 235 prior keys present; `1299_HK_Equity` carries folder `AIA Group` and its own
harvester form.

Signed: `2.0.0_SA_COO~X`, 2026-09-25 ~23:2xZ.

## CTO HALF -- `1.0.0_SA_CTO~Z`

Owed, in the CTO's own lane (`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`).
