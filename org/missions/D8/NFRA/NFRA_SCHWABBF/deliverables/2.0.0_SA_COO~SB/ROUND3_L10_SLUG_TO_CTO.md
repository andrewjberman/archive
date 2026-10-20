# NFRA_SCHWABBF round 3 -- L10 slug to 1.0.0_SA_CTO

**From:** `2.0.0_SA_COO~SB`, 2026-10-20 ~17:4xZ. **Round:** 3 (the per-master firm form, bronze side; decomposition `decompositions/NFRA_SCHWABBF_DECOMP_R3.md`, issuance `6c4675f585`).
`round-close-check --round 3`: 7 orders, 7 complete, proofs 7 of 7 valid, `verdict=MAY-CLOSE`. Nothing deployed, applied or moved.

## 1. What round 3 delivered (merged on `box/laptop`)

| cell | merge | what exists |
|---|---|---|
| BF-k-3 | `1fa08c5fb7` | the key function pair on the per-master rule: `FIRM_FORM_MASTERS` (08403355 + the four Cottonwood masters) take the firm key, 08242234 and 08335338 get TODAY's key byte-for-byte; 643 tests, incl. parity with the pre-round function |
| BF-m-3 | `1fa08c5fb7` | the move tool moves 08403355 only (`MOVE-REFUSED` rc 2 for any other master); live read-only plan: 6,074 keys in scope, 0 foreign, 20 tests |
| BF-r-3 | `3a0cbe7215` | the two readers (they read 0833) back to pre-round bytes |
| BF-w-3 | `24eb435138` | the puller: firm form for 0840, 0824 and 0833 as before (proven against the pre-round script); 13 tests |
| BF-t-3 | `25a713cd88` | the trace refuses masters outside the five; live `THREAD-OK` on the real 0840 day 2026-10-16 (legacy form) |
| BF-i-3 | `691598b66f` | the box role's firm-prefix write entry for 08403355 only (0824 and 0833 entries removed) |
| BF-n-3 | `00103d9f8a` | `modules/opal_name` regenerated (all five in-scope masters plus the new FIRM rows) with the `secret_name` output; `terraform test` 95 passed (48 before) |

Merged-tree checks: `data/canonical/schwab/tests` 783 passed; converter-side files 122 passed; `terraform test` 95 passed; `py_compile` clean. The deploy hazard of round 2 (the all-firm key function in a file the deploy gate maps to `opal-data-bd`) is gone: 0824's bd converters get today's key again.

## 2. Rows

Investigation file under `surprise-channel/investigations/`; 0 ARMED. Rulings I made inside the decomposition: W1-S4 (`MASTER_FIRM` not aliased; nothing reads it), W1-S3 (an unregistered eight-digit master takes the old form, as v0.7 says), W4-S7 and W6-S3..S5 (accepted as built). Carried for you: W3-S4 (the puller keeps a seven-master `Get-FirmOf` map and a five-master `Test-FirmForm`).

## 3. FINDING that blocks the meta and `_ops` half of C-TIERS (decision)

PRD v0.9 C-TIERS says 08403355's `silver/` (18 tables), `meta/` (`complete/`, `conversions/`, `pulls/`, `backfill-status.json`) and `_ops/` (`daily_pull/`) move to "the builder's `schwab/49financial/<tier>/...`". Measured against the builder today (`lib/opal_naming.py address()`):
- **silver: works.** `address('schwab','49financial','silver','dim_balance','date=2026-10-16')` returns `s3://opal-data-assets/schwab/49financial/silver/dim_balance/date=2026-10-16`; the file name `08403355.parquet` is appended as v0.9 says.
- **meta and `_ops`: REFUSED.** `address('schwab','49financial','meta','complete','date=...')` raises `tier 'meta' is not one of NAMING_SCHEMA.json key.tier`; `_ops` and `ops` are refused the same way. Per CLAUDE.md rule 30 a builder refusal is a missing registry row, not a hand-typed path.

So no meta or `_ops` cell can be cut until the registry has those tiers (a `4.0.0_SA_CRO` row, plus a ruling on the key shape: the collision-prone fixed names are `meta/complete/date=D.json`, `meta/backfill-status.json`, `meta/conversions/<run>.json`, `meta/pulls/<run>.json`, `_ops/daily_pull/last_run.json` and `runs/<run>.json`; one master's object must not overwrite another's in a shared firm folder).
Silver can be cut now. REC: route the registry row and the key-shape ruling to the CRO; I cut the silver cells (converter output key, move tier, equality, trace, IAM) as round 4 now, and the meta and `_ops` cells in round 5 when the rows land. Reply `go` to cut round 4 as silver-only, or say otherwise.

## 4. Release acts and the gateway

The 0840-only release plan (R0-R8 on the firm form, now with silver in the same window) is re-cut after round 4. Site Z: `2.0.0_SA_COO~O` owns the gateway edit, `0.7.0_AE_CloudOps~NFRA1` applies it in the same window; I owe both the date. The cutover waits on the silver cells, the CRO's meta/`_ops` rows, and Andrew's confirmation before any old key is deleted.
