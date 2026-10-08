# L8 drain end -- IRPT_DASHBD round 27, workstream B

**Issuer:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-08 ~06:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Read at:** CLOUD @acb7066605

One order, terminal, merged and VALID at HEAD (`.tools/proof-of-spec-check.py`, rc 0, re-run by the issuer on the branch and after the
drain). 0 JUDGMENT criteria. Risk LOCAL: a local measurement; no S3 write, no deploy. On: `1.0.0_SA_CTO~DELL2` msg 1184 (cut S31 now,
correcting its round-26 analysis).

## The order

| order | drain | criteria (issuer re-run) | result |
|---|---|---|---|
| DB-b-46 (S31 population sizing) | @acb7066605 (f70cc737df, issuer amendment 10ef9f6ef9, 521e4122a0) | DB27-2-AC1 (under amendment 1), AC2 PASS | The extended handler, one process, 2026-10-06, its own population: 7,597 of 7,597 accounts. Returns 122.57 s / 257.8 MB; class 92.69 s / 295.6 MB; lots 244.65 s to a REFUSAL / 2,759.5 MB peak; total 461.06 s. Verdict **BREACH** on memory: at least 711.5 MB (34.7 percent) over 2,048 MB, a floor because the lots stage did not finish. Timeout not breached (461 of 900 s) |

## Read before grading

- **The lots stage refuses at population scale.** `realized_rows` raised on a realized lot id repeated within one day's frame: 2,523
  rows, 2,435 distinct ids, 87 ids repeated (175 rows; one thrice) across 36 accounts; 0 ids span accounts; 0 rows identical in every
  column. The 20-account sample of round 26 showed neither this nor the memory. As prepared, the release would skip the three tables on
  every fire and could exceed the function's memory.
- **AC1 amendment (issuer's own check defect).** AC1 as cut demanded a per-account tail; a refused stage has 0 per-account samples. The
  issuer amended AC1 to admit that branch (null tail, BREACH, refusal named); the record was not changed.
- **Measured on dell2** (8 cores, 63.7 GB, pandas 3.0.6, Windows); the served function runs pandas 2.2.3 on Linux.

## Rows in the round

| row | class | standing |
|---|---|---|
| W26-S1 | BLOCKING, ARMED -> gated | issuer row S33 (UNDER_INVESTIGATION): the release COO half stays withheld; the realized lot key and the lots stage's memory fit route to `1.0.0_SA_CTO~DELL2` |
| W26-S2 | OBSERVATION, INERT | the per-account tail is null (no samples) |

## What the round leaves

- For the CTO: the realized lot key (87 ids repeat within a day in 36 accounts) and how the lots stage fits in 2,048 MB (or the function's
  memory), so the activity-and-lot release can be signed. The release COO half is withheld on S31/S33 and on S32 (pandas 2.2.3, DB-b-43,
  waiting on the Python 3.12 kit).
- FWD-8's split BD pull (DB-b-45) waits on dell2's grant for `blackdiamond/49f/session`, not started at the laptop (MSTR msg 1211).
