# L8 drain end -- IRPT_DASHBD round 25, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-07 ~19:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @5ffd7b740d

All three orders of the round are terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer on the
branch and again after the drain). 0 JUDGMENT criteria. Risk LOCAL: measurement, rule fixes, a source-only hardening of the served
producer and local re-runs; no S3 write, nothing built, staged or deployed. One worker (~22), one queue; the worktree and both branches
were removed. On: `1.0.0_SA_CTO~DELL2`'s round-24 analysis @99580aac8c items E1, E2, E3 (FWD-4).

## The orders

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-38 (E2: lot-lag bound) | @5ffd7b740d (3185e316f8, 0507ca0bcd) | DB25-1-AC1 PASS | 887 of 887 trades matched to their lot row (765 buys, 108 sells, 10 in-kind arrivals, 4 in-kind departures), 0 unmatched; p50..p99 0 trading days, max 1. `LEG_LAG_DAYS` 3 -> 1, covering 100% |
| DB-b-39 (E1: the 4 non-rounding windows) | @5ffd7b740d (c9e69c981c, e428ed65a8) | DB25-2-AC1, AC2 PASS | All 4 named as RULE causes and fixed through the rule, no account id in the producer: a wash-sale basis rule (3 MISSING-TERM windows: the lot basis carried the disallowed loss) and an in-kind re-selection true-up (the OTHER window); plus a sale link broken by acquired date where an event id repeats. 91-window re-run: 58 tie, 33 miss, all ROUNDING (0.05); 0 MISSING-TERM, 0 OTHER. No window's gap grew |
| DB-b-40 (E3: pandas option once; None hardening) | @5ffd7b740d (ba544b6064, aa4f460db3) | DB25-3-AC1, AC2 PASS | `future.infer_string` set once per process at the producer entry; the per-call context is gone; 2 threaded tests. `classify_and_sum` in `account_return_daily.py`: 3 lines (explicit `object` column, `isna`), 4 None tests. Source only: shipping is the next release's half |

Drain hygiene: commit-gate clean on the 4 code files; the folder's suite 88 passed; safe-merge 20 paths, 0 dropped, 0 foreign.

## Read before grading

- **The round-24 sample now ties except for rounding.** 58 of 91 within one cent; the other 33 are within 0.05. FWD-4 stays exercised
  locally and not served; the CTO's analysis puts the tables' release after E1, under its own halves, carrying W20-S1 and W20-S3.
- **Controls (worker, issuer-read in the records):** with both DB-b-39 rules off, the 4 windows return round 24's gaps exactly; 102 of
  102 lots carrying a disallowed loss satisfy cost basis minus loss = original cost. The threaded test fails on a copy rewritten to a
  per-call context. 3 of 4 None tests fail on the pre-hardening source; with inference off, old and new source give identical output.
- **Not measured: the hardened `classify_and_sum` on pandas 2.2.3 (the served layer).** This box has pandas 3.0.6 only; the worker used
  equality with string inference off as the stand-in. Downloads were not used. The release half that ships this change should run its
  tests on the served layer's pandas.
- **Issuer repair on the branch:** the worker's append to `INVESTIGATION_v1.md` normalized 26 CRLF endings in earlier rows (content
  identical). The issuer restored the base bytes with the 5 new rows appended unchanged (b8c331275d); the channel diff is append-only.

## Rows in the round

| row | class | standing |
|---|---|---|
| W22-S1 | OBSERVATION, INERT | the lag bound governs only in-kind legs; reinvested-dividend lots carry the trade date in `orgpurch_date` |
| W22-S2 | OBSERVATION, INERT | a lot event id repeats after a wash sale re-dates it (fixed by the acquired-date tie-break) |
| W22-S3 | OBSERVATION, INERT | new `basis_source` member `WASH_SALE_EXCLUDED_BASIS`, METHOD_VERSION 3, SCHEMA_VERSION 1.2; the lot contracts under `org/standards/` do not list `basis_source` -- for the release |
| W22-S4 | OBSERVATION, INERT | round 24's `identity_regrade_e2.py` no longer runs (`served_runtime()` removed) |
| W22-S5 | OBSERVATION, INERT | `classify_and_sum` raises on a repeated index label, before and after the hardening |

OPEN 5, ARMED 0 (comp-surprise after the drain).

## What the round leaves

- The release of the activity and lot tables (CTO analysis): its two halves, the contract update for `basis_source` (W22-S3), the stated
  0.05 tolerance where a reader meets it, W20-S1 and W20-S3.
- The served producer's None hardening ships with the next reporting-gold release, tested on the served layer's pandas.
- The class release (FWD-3) waits only on the dell2 terraform kit.
- FWD-8: the yes/no card for the 2,299-account BD pull is in front of Andrew (MSTR msg 1015).
