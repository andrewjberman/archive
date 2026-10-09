# L8 drain end -- IRPT_DASHBD round 24, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~17:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @f71fd042c1

Both orders of the round are terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer on the
branch and again after the drain). 0 JUDGMENT criteria. Risk LOCAL: diagnosis, producer fix and local re-grade; no S3 write. One worker
(~21), one chain; the worktree and branch were removed. On: `1.0.0_SA_CTO~DELL2`'s round-23 analysis @9f285400cf items E1, E2 (FWD-4).

## The orders

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-36 (E1: diagnose the round-23 identity gaps) | @f71fd042c1 (worker ~21: 32caac124b, 0e4edcb0b6) | DB24-1-AC1..AC3 PASS | The ~1.1M account's window read term by term. Cause: CONDITIONAL-BY-COUNTERPARTY rows resolve to None in the served `classify_and_sum`, and on pandas 3 the None becomes NaN and the rows drop; plus in-kind lot basis. 10 value-moving types mapped to no term. The 39 gaps classed: ROUNDING 30, MISSING-TERM 9, at the tolerance 0.05 stated before the run |
| DB-b-37 (E2: fix and re-grade; amendment 1 @0473127246) | @f71fd042c1 (worker ~21: 5b6c8ea7a5, 2a094137e9) | DB24-2-AC1..AC3 PASS | Three fixes in `account_activity_lots.py`; `account_return_daily.py` not edited. Re-grade over the same 91 accounts: 55 pass, 36 fail (ROUNDING 32, MISSING-TERM 3, OTHER 1); round 23 was 52 / 39. Exercise window: account `acct#2fcb1889`, 2026-09-17..2026-10-05, realized and both flows non-zero, ties at 0.0075. Tests 31 (23 kept, 8 new) |

Drain hygiene: commit-gate clean on the producer and its tests; the folder's suite 78 passed; safe-merge 13 paths, 0 dropped, 0 foreign.

## Read before grading

- **FWD-4's first real exercise is shown on ONE window** (realized gain AND a flow, to the cent). It is a window that opens inside the
  period (beginning value 0). Two other qualifying windows with non-zero beginning values are in `IDENTITY_REGRADE_E2.json`.
- **36 of 91 windows still miss by more than a cent; 32 of them by 0.05 or less.** The 3 MISSING-TERM windows are a lot basis above the
  cash paid, unchanged from DB-b-36; the OTHER window is a custodian lot re-selection on an in-kind departure (row W21-S4). Gaps are
  carried, never plugged.
- **The pandas finding (W21-S1 -> issuer row S30).** The served reporting-gold function's layer carries pandas 2.2.3 (measured), so the
  SERVED `account_return_daily` gold is not affected. This box runs pandas 3.0.6: the local runs of rounds 21-23 were. The producer now
  runs the served call under the served behaviour and asserts every conditional row resolves (2,603 of 2,603). LATENT: the served code
  drops those rows if its layer ever moves to pandas 3; that hardening belongs to the served producer's next release.
- **W21-S5:** `LEG_LAG_DAYS = 3` is a bound the worker chose, not a measured one.
- The issuer's re-seat prompt omitted the inline face text and pointed at the order file on the branch; the worker read the order there
  (amendment 1 included). Recorded as the issuer's own defect in the drive log.

## Rows in the round

| row | class | standing |
|---|---|---|
| W21-S1 | OBSERVATION | disposed by issuer row S30 (DISMISSED_WITH_REASON: served layer pandas 2.2.3 measured) |
| W21-S2, W21-S3 | OBSERVATION, INERT | open (DB-b-36 observations) |
| W21-S4 | OBSERVATION, INERT | open: the OTHER window's residual |
| W21-S5 | OBSERVATION, INERT | open: lot-table lag bound chosen, not measured |
| W21-S6 | OBSERVATION, INERT | open: pandas option contexts are process-global |

OPEN 5, ARMED 0 (comp-surprise after the drain).

## What the round leaves

- The 4 non-rounding windows (3 MISSING-TERM, 1 OTHER) and the latent pandas-3 hardening of the served producer.
- The activity and lot tables are built and graded locally; none is released.
- The class release (FWD-3) waits only on the dell2 terraform kit; both halves are given and the pins are this seat's at the apply.
- FWD-8 stays HELD on Andrew's per-use word for the split BD pull.
- The live thread trace (FWD-1 hop 5) was not re-run this round.
