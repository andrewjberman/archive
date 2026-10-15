# IRPT_DASHBD round 126, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-15)

Issuance `ff1a4c7c90` (checker amendment `2420fd102e`); merge `ed18a47a03` (worker ~413: DB-c-21). Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md` section 13. Cut on the CTO's analysis answering rounds 117 to 125 (msg 8325, `@46345ab631`). `round-close-check.py --project IRPT_DASHBD --round 126 --workstream B-CW`: `verdict=MAY-CLOSE` (1 order, 0 judgment criteria). Push state at the last measurement (13:39Z, fetch): 0 behind and 1 ahead of `origin/box/dell2`; the later commits are LOCAL and the integrator moves them (a push by this seat is refused by LD-0367).

## The one real run

`DBC126-1-AC1`, `-2-AC1` and `-3-AC1` PASS on the worker's tree (re-run by this seat) and `-1` and `-2` PASS on the merged tree (each recounts the silver, gold, household and crosswalk figures from a fresh S3 read). Record `deliverables/0.9.0_WK_IRPT_DASHBD~413/COTTONWOOD_FWD1_TRACE_R126.json` and its note.

## The CTO's ruling 1 condition: the naming gate re-run (recorded)

`deliverables/2.0.0_SA_COO~C2/NAMING_GATE_RERUN_R126.md` (`bc74eed671`): the landed Cottonwood source-map entries graded as NEW literals in a scratch worktree at the pre-entry tree: **`NAMING-GATE: PASS 0 graded`** over 262 added lines; the planted `cot-planted` control in the same setup: `REFUSE 1 graded`. No `--no-verify` after `eda88f89c7`.

## The trace (B-CW FWD-1 for Cottonwood)

| hop | verdict | what the record reads |
|---|---|---|
| silver to gold `holdings_performance_daily` | HOLDS | silver `fact_holdings` (94 partitions) and the gold both newest 2026-10-14; 1001 rows, 1001 accounts |
| silver to gold `account_dim` | HOLDS | silver `fact_allocations` (145) and `fact_holdings` newest 2026-10-14; `account_dim` 2026-10-14: 1004 rows, 226 households, 37 accounts without a household; the crosswalk to the holdings accounts: overlap 1001, 0 only in holdings, 3 only in `account_dim` |
| gold to reporting-gold households | **BREAKS** | the Cottonwood reader's own `households()` would return 226 households from the 2026-10-14 partition, but the SCHEDULED reporting-gold build never calls it: the build is declared for one custody source only (`data/assets/scripts/gold/irpt_reporting/sources.json` holds `schwab_08335338` and nothing else, re-read by this seat), takes its firm from that entry and its households from that firm's crosswalk |
| reporting-gold output | **BREAKS** | the scheduled build writes no Cottonwood filled report (output prefix null, 0 objects), and its schedule file carries no Cottonwood event; absent kinds in words: no `account_activity_daily`, `account_lot_realized`, `account_lot_unrealized_daily` or `account_class_daily` gold table for Cottonwood (the reader's `NO_SOURCE_YET`) |

## A correction of mine

The DB-c-19 packet's Both branches section, and my COO half over it, said the first landed `account_dim` partition changes the household source of the next reporting-gold run (and the CTO's half accepted a one-day lag at the 07:41 New York fire). That holds only for a run configured for Cottonwood. The scheduled build is not: it is the 49 Financial build. No harm followed (one key was written into a table nothing scheduled reads yet), but the claim was an inference from the reader's code that I did not check against the build's declaration. Row `D2-S86`.

## What the CTO's half decides

1. Wiring Cottonwood into the reporting-gold build is the one thing between the live gold and a Cottonwood report: a Cottonwood custody source in the declaration or its own scheduled invocation, the filled-report output prefix for Cottonwood, and the siblings the reader names absent (activity, lots, class are separate gold tables Cottonwood lacks). Whether that is a build cell under the existing endpoint or needs a PRD addendum is the CTO's ruling. Inflection is in the same state by the declaration (one custody source), which this trace did not read.
2. Nothing in the live Cottonwood gold needs a change; the two tables are correct as ruled.

## Rows

`D2-S86` dispositions worker 413's `W413-S1` (BLOCKING, INERT: the sparse cone built from the order's `<paths>` omitted the folders the order reads; the issuer extended the cone and the worker re-ran from the start; the provision script's sparse set should include the folders an order reads), `S2` (accepted) and `S3` (the finding). Nothing ARMED of this round. Earlier: `D2-S82` (the first scheduled Cottonwood holdings fire) and the ledgers: `irpt-dashbd-cottonwood-account-dim-20261015` CLOSED (`5d246810d2`) and `irpt-dashbd-cottonwood-holdings-performance-20261015` CLOSED by this seat (`91e47b905b`) after `~DB2`'s L8 close (`d4535647db`, msg 8336).

## Issuer's own defects this round

The provisioning gap above (the sparse cone from `<paths>`); the checker's bounds arm now reads the worker's commits from the merge-base with the shared branch (`2420fd102e`), as the CTO's ruling 6 asks. One commit-subject error (the Cottonwood holdings fire row was `S82`, the subject says `S77`). Every commit went through `.tools/safe-commit.sh`.
