# NEVER-WIDEN -- COO HALF: I-1, disarm W4-S9 -- one deliberate 60-date marker batch through the deployed canonical-shape Lambda

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~21:5xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).
**Why:** the round-6 analysis @94f682c868, ruling 5: "W4-S9 is ARMED. The issuer act I-1 is owed now." The row: a marker-driven
G1 batch above ~45 report dates timed out the 900 s Lambda. Round 5 bounded it: `_budget_s` 600 s returns PARTIAL with a cursor,
and `run_gold_chain` re-runs G1 once inside an invocation. This act proves the bound on the deployed Lambda.

## VERDICT: SIGNED

## THE ACT

- `rivalfunds-build-canonical-shape-lambda`, deployed at CLOUD eb6e9f04ff (the bundle equals eb6e9f04ff on all 46 .py files).
- Event `{"date":"2026-10-01","mode":"daily","batch_id":"d5-gqgu-03","sink":"s3"}`: the GQGU batch that timed out three times on
  2026-10-01 (request 1984c6f7). Its build-silver marker lists 60 dates (2026-03-31..06-25); no G1 marker or cursor exists; all 60
  dates are already built.
- Invoked SYNCHRONOUSLY, read timeout > 900 s, no retries. A PARTIAL is continued by ONE more identical invoke. Nothing
  continues it organically today, and round-7 cell cu-1 makes the sweep do so.

## THE SERVED DELTA, MEASURED (C:/tmp/r7i1/, an overlay at the deployed code: S3 reads, local writes)

| invocation | result | seconds (local) | dates done |
|---|---|---|---|
| 1 | PARTIAL, cursor next 2026-04-27 then 2026-05-04 | 783 | 23/60 |
| 2 | PARTIAL, next 2026-06-03 | 766 | 44/60 |
| 3 | G1 OK at 567 s, then G2 155 s, G5 127 s | 850 | 60/60 |

The local run measured ~34 s per date. The Lambda replayed these same dates at 17-19 s per date, so the expectation is about
2 invocations, with the first PARTIAL at ~780 s and ~40 dates done. No invocation timed out.
- **G1:** 0 objects. G1 skips a date whose revision exists; a rebuild of 03-31 and 06-25 gave identical rows.
- **G2:** 10 coverage files (09-17..09-30) differed in the last digit under local Python 3.14. Under the Lambda's Python 3.11
  summation, all 10 equal the served ones. Today's deployed daily run rebuilt these keys and wrote nothing.
- **G5 and G6:** 0 objects.
- **State:** the cursor `d5-gqgu-03.cursor` (rewritten per window), plus the G1, G2, G5 and G6 markers of batch d5-gqgu-03
  under date=2026-10-01.
- **The publish leg** (fired by the G5 marker): 3 new A1 objects for date=2026-10-01. holding_contribution, buying_trend and
  input_census are rebuilt because they predate their inputs (RIV-st-1 at the deployed code). The 2026-10-01 page is
  republished ONCE: 1,656,993 -> ~1,895,845 B locally, under the 2,097,152 B cap. It is the round-6 render over the 10-01 data.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| Q1 | gold canonical_shape, GQGU 2026-03-31..06-25 | 60 dates built | unchanged (0 writes, measured) | none needed |
| Q2 | state markers, batch d5-gqgu-03 (date=2026-10-01) | build-silver only | + cursor + G1/G2/G5/G6 markers | markers are append-only records; nothing reads them for served output |
| Q3 | gold A1 tables, date=2026-10-01 | the 10-01 objects | + 1 object each (newest wins) | RE-PUT the prior objects' bytes as newer revisions, then one publish (CTO change 1, round 6); never an S3 delete |
| Q4 | platinum page 2026-10-01 | its last publish | republished ONCE at the round-6 render | prior page kept under `revisions/<ts>/` |

## GATES

1. Nothing in flight on the canonical-shape Lambda (10 min of logs).
2. The deployed code is still the eb6e9f04ff set (CodeSha256 7m7xens5.. for canonical-shape).
3. No G1 marker and no cursor exist yet for batch d5-gqgu-03.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Disarmed:**
  - every invocation's REPORT Duration < 900000 ms, with no `Status: timeout`;
  - the response reads `status:"PARTIAL"` with `detail.cursor` and then OK;
  - the batch's G1 marker is written, and G1 writes 0 objects;
  - W4-S9's timeout class is closed by a resolving row citing the RequestIds. Its continuation half stays open until round-7
    cu-1 lands (the sweep continues open cursors).
- **Not disarmed** (a `Status: timeout` in REPORT): the row stays ARMED, the timeout is the finding, and no retry is fired.
