# LGIC_ENFORCE.TO-EN-b-42-r9 -- stale-backlog-owners -- RESULT

Worker `0.9.0_WK_LGIC_ENFORCE~3`, branch `wk-lgic-enforce-9-3`, base `a6476ef28f`, record commit `96c198f441`.

## Measured at write time

The gate's own limb was CALLED, never re-derived:
`srg._stale_open_row(srg._remediation_rows_for_project(root, "LGIC_ENFORCE")[0], 9, srg.STALE_OPEN_ROW_N_ROUNDS)`,
read from the checkout's INDEX (the gate's own read).

| figure | value |
|---|---|
| current_round | 9 |
| N_ROUNDS (read, not written) | 2 |
| intermediate: ids_from_tuple (`_remediation_ids_for_project` unpacked as a tuple) | 113 |
| intermediate: rows (`_remediation_rows_for_project`) | 113 |
| remediation rows | 113 |
| STALE at round 9 | **94** (register 91 at round 8; issuer 94 at the cut; this write 94) |

## Coverage, asserted AFTER the write

`build_stale_backlog_r9.py` writes the record, then re-calls the limb and re-reads the file:

    AFTER WRITE: re-measured stale=94 ; assigned 93 + deferred 1 = 94 ; set-equal True ; remainder 0
    COVERAGE-AFTER-WRITE: HOLDS

## Owners -- 6 distinct, every one resolving (serial shape or a code on org/missions/DIRECTIVES.yaml, 93 of 93)

| owner | rows |
|---|---|
| 1.0.0_SA_CTO | 47 |
| 2.0.0_SA_COO~G | 40 |
| 0.0.0_AB_MSTR | 2 |
| NFRA_COMPEFFICACY | 2 |
| LGIC_CANON | 1 |
| 0.7.0_AE_CloudOps | 1 |
| DEFERRED | 1 (LGIC_ENFORCE-W1-S23) |

87 rows keep their own `remediation.owner` with a stated basis. 6 are REASSIGNED because the remedy named a
category or a party that cannot act:

- `S18` -> `0.0.0_AB_MSTR` (same remedy verbatim as S17, already MSTR's; one remedy, one owner).
- `W1-S3` -> `NFRA_COMPEFFICACY` ("each tool's owner"; comp-find; the active comp-tool project).
- `W2-S1` -> `NFRA_COMPEFFICACY` ("each tool's owner"; comp-iam; NFRA_COMPTOOLS is closed).
- `W1-S24` -> `LGIC_CANON` (the remedy names it; infra/logic/** admits only 4.0.0_SA_CRO serials, so the prior owner 1.0.0_SA_CTO cannot write it).
- `S72` -> `0.7.0_AE_CloudOps` ("a seat whose grant reaches ..."; the path is lane CLOUD_OPS_OR_ETL; the prior owner is stated in the row itself to be unable).
- `W1-S70` -> `1.0.0_SA_CTO` ("the round that takes it"; each branch is a ruling on the naming contract).

Deferred: `W1-S23` -- the remedy is one assert in LGIC_NAMING round-3 fixed inputs; LGIC_NAMING is complete,
those instruments are frozen, the path is lane TIER0_MSTR and no open order grants it. Un-defers when any
order re-runs or reuses `blind_seat.py` / `check_ln_r3.py`; that order's issuer takes it.

## Criteria (post-commit, at 96c198f441)

    B42R9-AC1  VERDICT: PASS-B42-REMEASURED        (cell measured 94 | register 91 at r8 | issuer 94 at the cut)
    B42R9-AC2  VERDICT: PASS-B42-EVERY-ROW-OWNED   (owned 93 + deferred 1 = 94 ; population 94 ; remainder 0)
    B42R9-AC3  VERDICT: PASS-B42-NO-CATEGORY-OWNERS (assignments inspected 93 ; categories 0)
    B42R9-AC4  VERDICT: PASS-B42-DEFERRED-REASONS  (deferred rows 1 ; missing why/un_defers_when 0) -- NOT vacuous: 1 deferral exercised
    B42R9-AC5  JUDGMENT -- no verdict from this worker; 3.0.0_SA_CVO at L9.

Controls: selftest-arms 27 arms / 13 positive / 0 failures, run before any write. Four live mutants on the
committed record, each exercised alone, each returned its own arm's FAIL token; restored bytes equal and all
four PASS again. Two rebuilds are byte-identical to each other and differ from the committed record only in
`built_at_head` (the HEAD moved by this cell's own commit).

## What this record does NOT do

The seated owners live in THIS record only. The channel's remediation rows still carry their prior
`remediation.owner`, which is what the gate reads (row `LGIC_ENFORCE-W3-S19`). No row was closed, disarmed,
graduated or remediated; `.tools/surprise-row-gate.py` and `STALE_OPEN_ROW_N_ROUNDS` were not edited.

Surprise rows: `LGIC_ENFORCE-W3-S18` (face vs checker record keys), `LGIC_ENFORCE-W3-S19` (owner field vs remedy
text; seated owners not on the rows the gate reads). Both OBSERVATION, INERT.
