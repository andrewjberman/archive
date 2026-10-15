# NFRA_CTLPLN round 14 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-14 ~23:0xZ)

All five round-14 orders are `complete` (issuance `868b773335`, decomposition `NFRA_CTLPLN_DECOMP.round14.md` with amendment 1). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 14` reads `verdict=MAY-CLOSE`, `judgment=2 graded=2 ungraded=0 self_graded=0` (no judgment criterion of this round; the two are earlier `TO-APPLY` rows). Pins are commits on `box/laptop`, LOCAL unless stated. Each cell below carries the issuer's own re-run, not the worker's report.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | order status | merge | issuer re-run |
|---|---|---|---|
| `CT-ad-1` | complete (WORLD by path floor, no AWS call) | `8dd69fce60` | `ROUND14-BATCH arms=9/9 ok=True`; checker self-test 63 of 63 (unchanged); `FENCE-SCOPED rows_today=45 ... ok=True` (unchanged); the `routes.tf` diff holds only the two comment lines |
| `CT-ad-2` | complete | `8bd2a0817e` | `SAFE-COMMIT-DERIVATION cases=17/17 ok=True`; `NAMING-GATE-SELF-TEST: PASS`; `safe-commit.sh --help` rc 0; the issuer read the diff (derivation only, the graded set is still the eight extensions) |
| `CT-ad-3` | complete | `9358a02962` | `MEASURE-CALENDAR-COPIES arms=4/4`; `CALENDAR-COPIES found=4 same_2026_2027=4 differs_2026_2027=0 import_failed=0 ok=True` |
| `CT-ad-4` | complete (WORLD by path floor; injected fake only) | `91f58a8bff` | `CHECK-FRESH-BOUNDED arms=5/5 ok=True`; offline `ROLE-CENSUS ... roles=175 ok=True` unchanged |
| `CT-ad-5` | complete | `ee02e2b697` | `OPEN-CALL-ACT-ROOTS arms=8/8 ok=True`; `APPLY-GATES-TEST cases=100/100 ok=True` |

## 3. Real runs of the outcomes

- **`D2-S3` (CTO ADDENDUM 1, the done-when):** dell2's row `dell2-20261013T214715Z-f61b` read from the CLUSTER copy (S3, `kind` `act`, project `IRPT_BCKEND`, `roots` empty, OPEN). Through `measure_open_call`: `matched=0` against `infra/aws/terraform/irpt-status` and against `infra/aws/terraform/opal-ticket-api`; with its `roots` set to name `irpt-status`, `matched=1` there and `matched=0` against the other root. The check ran on a temporary repository root holding that one row, since the laptop's working-tree copy of dell2's list lacks the row. The OPEN-CALL limb stays WARN until the CTO arms ENFORCE.
- **Calendar copies (`W12-S1`):** four copies, none differs in the 2026-2027 holiday set, all four differ from the library in bytes. No deploy cell is warranted for the holidays.
- **`NFRA_MCPINDEX-Z-W34-S8`:** the merged `safe-commit.sh` carries the change; the next commit on this tree runs through it (this packet's own commit is the first real run).
- No UI is touched, so no screenshot.

## 4. FWD state

`FWD-11` is a qualified wait on Andrew's word (open call `laptop-20261014T205216Z-7841`); `FWD-9` PARKED; `W89-S3` ROUTED by the CTO to ADVI_FIRMBKTS (amendment 1 of the decomposition).

## 5. Rows this round minted

`W92-S1..S3`, `W93-S1`, `W94-S1`, `W95-S1`, `W95-S2`, all INERT observations, dispositions in each order's `<status_reason>`. Carried and unchanged: `S9118`, `S9119`, `S9120`, `Z-S3`, `S9103`, `W12-S1` (now measured: no holiday difference), `NFRA_MCPINDEX-Z-W34-S8` (fixed by `CT-ad-2`).

## 6. Not measured here

The real `--check-fresh` against the account (the cell was tested only with an injected fake); the UNREAD-role path in the resumable checkpoint (read from code, no arm exercises it); the PRD FWD grade table, which the CTO's coverage read governs.
