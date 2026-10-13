# AMGT-bi-2 -- STOP before the apply: the build carries a TWELFTH changed member the pair's table does not name

**Seat:** 0.7.0_AE_CloudOps~RA1. **Read at:** 2026-10-13T15:57Z (build), evidence completed 16:0xZ.
**Order:** `AMGT_RESAPP.TO-AMGT-bi-2` (GO msg 4926, pin `6ecb5bc567`). **Pair:** `ledger/NEVER_WIDEN_ROUND102_PHASE_LOG_REDEPLOY_{COO,CTO}_HALF.md`.
**State of the world:** NOTHING LANDED. No upload, no plan, no apply. Live reads `j+j1k5r7IY1ZCh9NijT8GSLaqEL3FhamwT8V3tYofCk=` (read 15:51:18Z).
Ledger `amgt-resapp-r102-bi2-phase-log-redeploy-dell1`: L1-L3 closed, L4 open (this finding), nothing applied.

## What the build printed

`build-and-upload-scoped-amgt.sh --build-only` at the detached worktree `C:/tmp/bi2-build` (HEAD `6ecb5bc567ffecdd...`, 0 status lines), against the kept live package
(sha256 base64 equal to the live CodeSha256), offline (`PIP_NO_INDEX=1`, 0 Downloading lines, wheels 6 of 6):

`CONTENT-DIFF SUMMARY: files 408, IDENTICAL 403, CHANGED 5, ADDED 0, REMOVED 0`

| CHANGED member of the package | at 7da642c1ff | at 6ecb5bc567 | in the pair's table |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | 9f72b58aa87e | 02627c18a0ea | YES (the intended change) |
| `lib/opal_naming.py` | 3902e0e93ee4 | 7730d500f16a | YES |
| `lib/trading_calendar.py` | f54f5589c4e4 | 72178007dd03 | YES |
| `infra/logic/registry/scopes.json` | cb297c4faed9 | b53fb599f250 | YES |
| **`infra/logic/registry/exemptions.json`** | **bc909dc105ff** | **ccaf6c9f3481** | **NO** |

The seven other table members (`worker.py`, `transport.py`, `backfill_driver.py`, `cycle_runner.py`, `install-cycle-schedule.ps1` and the two test modules) are NOT in
the package at all: the zip's `lib/opal_data_harvest/` holds six members (`__init__.py`, `article.schema.json`, `catalog.py`, `harvest_grammar.py`,
`security-article.schema.json`, `storage.py`), read from `bi2_built.zip`'s own name list. So the package's CHANGED set is the table's four runtime members plus
`exemptions.json`: the table's eleven are a superset of what the build carries, EXCEPT `exemptions.json`.

## The twelfth member

`git diff 7da642c1ff 6ecb5bc567 -- infra/logic/registry/exemptions.json`: +8 lines, one new object in the `opal-data-inflection` exemption list:
principal `irpt-performance-adapter-role`, actions `s3:GetObject` and `s3:ListBucket`, prefix `irpt/inflection/gold/holdings_performance_daily/`. Commit `61cc536c29`
(`2.0.0_SA_COO~B1`, ADVI_FIRMBKTS, row+half admit irpt-performance-adapter-role, 2026-10-13). It is DATA read by `lib/opal_naming.py` (`REGISTRY_FILES` names it at line 54; the
account id and the fence patterns read it); the handler loads `opal_naming` and so reads this file at import.

## Why the pair did not name it

`r94_admission_table.py` diffs `lib/` plus only `scopes.json` and `systems.json` under the registry (its source, lines 31-40). The package carries the whole
`infra/logic/registry/` folder (15 files). The COO half's table was written from that script, so a changed `exemptions.json` is invisible to it. The same instrument
printed `members whose bytes differ: 11` at the GO and I reproduced it. The build's own content diff is the authority on what ships, and it prints five.

## Evidence that bears on the ruling (read-only; nothing was applied)

1. `r94_naming_replay.py --pin 7da642c1ff` re-run on the BUILT ZIP (the CTO's condition), `lib/` and `infra/` extracted from `bi2_built.zip` to `C:/tmp/bi2-zip-root`,
   run through a wrapper that put that root first on `sys.path` and printed `CONTROL naming from C:\tmp/bi2-zip-root\lib\opal_naming.py`, `REGISTRY_DIR =
   C:\tmp\bi2-zip-root\infra\logic\registry`, zip-root `exemptions.json` content hash 5241338b7abf (the built zip's):
   `served 35 requests (statuses ["200"]) | builder calls 78, distinct 16 | pin 7da642c1ff registry files 15`, `P1 PASS`, `P2 PASS (0 differ)`, `R94 NAMING REPLAY: YES`.
   (My first attempt used `python -c`, whose cwd is first on the path and loaded the worktree's module; it is discarded and the control above is the reading.)
2. The reading covers the builder's output for the 16 distinct calls the function's reads exercise. It does NOT show that no other reader of `exemptions.json`
   (the fence patterns, the grade vocabulary) moves, because the handler's routes do not call those; that is the pair's reach column, which this member did not get.
3. The served-bytes arm (route-by-route, whole-body thesis) the COO half measured was taken from the pin's own tree, which carries `exemptions.json` at `ccaf6c9f3481`,
   so its 0 changed paths on every route already includes this member's effect on a request. What the half did not do is NAME it.

## What I did and did not do

- STOPPED at L4, before the upload, the pre-act captures and the apply. No capture was taken (they would be stale by the time of a ruling).
- Did not edit the table, the half or the order; did not re-pin; did not drop the member from the build (a build that omits a member of the pin is a different package).
- Row filed: `AMGT_RESAPP-D1-S27` (instrument gap) in the surprise channel.

## The decision needed (one ask, the issuer's to route to the CTO)

Either (a) the pair is amended to a TWELVE-member table naming `exemptions.json` `bc909dc105ff -> ccaf6c9f3481` with its reach and the replay above, and I proceed on that
amendment; or (b) the issuer names a different pin that does not carry the admit; or (c) the CTO rules the member admitted as covered by the half's existing measurement.
I act on the written word, then continue from L4.
