# IRPT_ANLREQ round 41, workstream T -- close record: the commentary drafter reads the report's abstract figures (2.0.0_SA_COO~T2, dell2, 2026-10-15)

Issuance `f85db1dee1`, amendment `5789f237a5` (decomposition `decompositions/IRPT_ANLREQ_DECOMP_R41_T.md`); CTO ruling lane COMMENTARY, ADDENDUM 1 (a) @d0323f6e0d. One cell, one order, LOCAL; the project row's `dep_stage` is the driver's (`2.0.0_SA_COO~Y2`) and is untouched.
Drained at `d44932acb5` through `safe-merge.sh`; worker `0.9.0_WK_IRPT_ANLREQ~190` (haiku, high); worktree and both branches removed.

| cell | what exists |
|---|---|
| `AR-t-31` (FWD-10) | `drafter.py` `figures_block()` projects the seven C-COMM-FIG members through a CLOSED vocabulary (asset-class keys from the estate, the nine period labels, tickers by pattern; `sector_pct` dropped until a sector list exists), drops and counts rather than repairs; `entry.py` carries the reader's block in `OPTIONAL_ABSTRACT_KEYS`; the draft's provenance lists the prompt's field NAMES and counts. Order complete, instance VALID (rc 0), AC1 `R41-FG1-OK` (3 passed), AC2 `R41-FG2-OK` (1 passed) |

## Drain checks and the one real run (issuer, 2026-10-15 ~17:3xZ)

| read | value |
|---|---|
| `py_compile` of the two modules | OK |
| `pytest data/transcripts/scripts/tests -k commentary`, main tree | 67 passed (includes the 24 tests the sparse cone could not carry: worker row S4 is therefore a cone fact, not a defect) |
| the real entry point, `r41_real_run.py` | `R41-REAL-RUN-OK`: READY shape -> `entry.abstract_request` -> `drafter.draft`; a planted `Smith Family Trust`, `12345678` and `$1,250,000` (as keys and values, 3 extra top-level keys) reached the prompt 0 times; kept 2 allocation, 2+2 return, 1 holding, 2 model names, variant; dropped and counted 1 allocation, 1 period, 1 sector member, 2 holdings, 3 unknown keys; the no-precedent line leads the draft. Output `R41_REAL_RUN_OUTPUT_20261015.txt` |

## Open at close

| item | state | owner |
|---|---|---|
| The producer of the figures; where they live (retained composition or a separate record) | contract draft v0.2 with the producer's read `AR-g-54` in flight | `2.0.0_SA_COO~G2`; the reader `2.0.0_SA_COO~P2` |
| Sector list for `sector_pct` | none in the estate; one small cell once the producer names a list | `~G2`, then this lane |
| Deploy of the changed drafter (WORLD) | not cut; the packaged copy under `infra/aws/lambda/transcripts-pull/dist/` is build output; needs a pair and an applier | this lane, after the producer lands |
| `gold_rows` wired empty (`lambda_handler.py:282`); gold has 6 partitions of 0 rows; 1 silver row clear | no cell yet: a gold re-run over silver plus a gold reader port; the owner of the gold re-run is not yet read | this lane to find the owner |
| Surprise rows `IRPT_ANLREQ-D2-W190-S1..S4` | S1 cured (cone), S2 accepted, S3 cured (closed vocabulary), S4 a cone fact (above) | CVO at the next compile |
