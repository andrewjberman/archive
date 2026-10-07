# L8 drain end -- IRPT_CUSTDY round 5

**Issuer:** `2.0.0_SA_COO~K2` (dell2) | **Date:** 2026-10-07 ~13:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile; one JUDGMENT criterion: CU15-AC3)

Round 5 is the round-4 analysis's E1-E2 (`1.0.0_SA_CTO~DELL2` @16d9b128c0), one issuance @9ca7469fc3 (`fanout: 2 of 2 chains, cap 8`)
from `decompositions/IRPT_CUSTDY_DECOMP.round5.md`. It supersedes round 3's unspawned E3 order CU-c-3. Both orders are terminal and merged;
0 linked IRPT_CUSTDY worktrees.

| order | worker | drain | proof | real run on dell2 |
|---|---|---|---|---|
| CU-e-1 (E1) the 4 unkeyed accounts | ~13 | @5b85219599 | VALID: AC1 16 passed, AC2 `UNKEYED-LOOKUP advisor=matthew_gooch accounts=4 found=0 not_held=4 classified=4`, AC3 `SUITE passed=126 failed=0` (its branch) | 39 Schwab silver tables, 8 identifiers per account, 0 matches; a positive control (a real `z`-prefixed account) classed FOUND through the same code |
| CU-e-2 (E2) the 49F ClientReportDocument | ~12 | workspace @8029bc6635; portal 99addd80 (branch `wk-IRPT_CUSTDY-12-portal`, not on DEV) | VALID: AC1 10 pass / 0 fail, AC2 `REAL-RENDER households=1 accounts=2 periods=4 si_labels=2 not_ok_noted=30 bd_field_names=0`, AC4 `TYPE-LINT-OK` (tsc 0 errors; eslint 0 errors, 3 react-refresh warnings); **AC3 JUDGMENT (C-SHAPE) for the CVO** | bun only as `bun --no-install` in a worktree with node_modules linked (msgs 492/500/508/516/555); the real data stayed under `.scratch/` and was deleted with the worktree |

**The one real run at close** (~13:0xZ): `HOP3-REAL-RUN advisor=matthew_gooch as_of=2026-09-30 households=10 accounts=14 uncovered=0 held_si=0
not_in_directory=4 of=18 not_covered=4 error=none` -- 18 of 18 granted accounts in the report data: 14 with SI OK, 4 carrying `not_covered`
with the reason `NOT_HELD: no Schwab record under any identifier of this account` (row S11; the file holds client figures and is not committed).

**CTO review of the portal candidate** (msg 581): PASS, with one note -- the template renders no `not_covered` account yet; add one fixture
account and one test before the branch is pushed to portal origin. DEV landing waits on Andrew's word (laptop 106221).

**Drain checks on CLOUD:** `SUITE ... passed=125 failed=1` -- the one failure is the round-2 tracer test, red again because IRPT_BCKEND IB-pr-348
(11ba48fdc7) made the seam guard case-insensitive; no refusing spelling remains (row S10).

**FWD-1 thread: NOT LIVE.** Hops 1-4 run on real data for every granted account; the template exists and renders a real household locally.
Hop 5's served render waits on IRPT_BCKEND a1-a4 (the print kind that mounts the document) and on the template's DEV landing (Andrew); hop 6 is
Andrew's.

## Rows of the round

| row | class | standing | note |
|---|---|---|---|
| W13-S1 | OBSERVATION | INERT | the real split: 0 found, 4 not held |
| W13-S2 | OBSERVATION | INERT | a not-held account sits in its own household document without household_returns/lineage; `validate_document` and `si_anchor_probe.py` would reject it if they read it |
| W12-S1 | OBSERVATION | INERT | `hop3_real_run.py` exceeds 120 s (the anchor probe's S3 listing); completes under 1500 s |
| W12-S2 | OBSERVATION | INERT | the face listed a per-account `name_source`; real documents carry `name_sources` at file level -- typed optional |
| S10 | OBSERVATION | INERT | drain red: the tracer test after IB-pr-348; retire it |
| S11 | OBSERVATION | GRADUATED | the round's close and real-run grade |

**For the round-5 analysis (not rows):** the template's `not_covered` rendering (CTO note); retiring the tracer test (S10); the 30 'not
described' holdings in the real render (class and sector stay null until the describe() join is applied to hop3's documents); the
`hop3_real_run.py` run time (W12-S1); `validate_document`'s handling of a `not_covered` account (W13-S2).

-- 2.0.0_SA_COO~K2
