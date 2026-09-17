# SESSION LOG -- `AMGT_RESAPP.TO-AMGT-rk-8` -- the five-route exercise surface

- **Worker:** `0.9.0_WK_AMGT_RESAPP~23` (Chain A, order 2 of 5)
- **Worktree:** `C:/tmp/wk-amgt-12-23`, branch `wk-amgt_resapp-12-23`, base tip `5432756013`
- **Portal worktree:** `C:/tmp/wk-amgt-12-23/portal`, branch `wk-amgt_resapp-12-23-portal`, HEAD `2453a7b4c6b7ff91ea89db499890a9486265d1a0` (`AMGT-rk-1`'s DEV-integrated branch)
- **Session:** 2026-09-16, ~18:40Z to ~19:0xZ
- **Governing order vintage:** carries ISSUER AMENDMENT 11 (the fifth route corrected from `/posture` to `/coverage`)

## 1. The bar

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-12-23`; `test -d org && test -d .tools` -> `TREE-OK`.
All six `<paths>` entries verified present before any act (`PATH1-OK` .. `PATH6-OK`). No BLOCKING condition.

Premises re-grounded against live state, not assumed:
- portal worktree on the DEV-integrated branch at `2453a7b4` (`git rev-parse` in the portal worktree)
- `portal/node_modules` PRESENT -- **no install was run**
- `errorEmpty.harness.cjs` present in `portal/src/pages/SecurityAnalysis/__harness__/`

## 2. Criteria, in order, each run LITERALLY under a bound

Every criterion was run byte-for-byte as the order writes it, under `timeout 120`. No invocation was
edited, widened or substituted. No criterion timed out; no retry was needed.

| id | result | deciding output | denominator |
|---|---|---|---|
| AC1 | PASS-by-output | `captured 5` | 5 of 5 routes |
| AC2 | PASS-by-output | `files 5` / `nonempty-bodies 5` / `overlay-has-description True` / `overlay-has-posture True` | 5 of 5 bodies |
| AC3 | PASS-by-output | `CHECKS-OK 12 of 12`, `rc=0` | 12 of 12 checks |
| AC4 | RECORDED (judgment) | `routes_captured 5 of 5` | 5 of 5 routes -- graded at L9 by `3.0.0_SA_CVO~Z`, NOT self-graded |

AC1 captured all five routes from the DEPLOYED adapter (`opal-amgt-scoped-api`) in one act, each at
statusCode 200. The five capture filenames are named exactly, never paraphrased:

```
.scratch/rk8/api_scoped_amgt_security_BA_US_Equity_overlay.json    50630 bytes
.scratch/rk8/api_scoped_amgt_security_BA_US_Equity_peers.json      20036 bytes
.scratch/rk8/api_scoped_amgt_lead-panel_rankings_trending_chatter.json  7319 bytes
.scratch/rk8/api_scoped_amgt_security_BA_US_Equity_thesis.json    221015 bytes
.scratch/rk8/api_scoped_amgt_security_BA_US_Equity_coverage.json    1696 bytes
```

Capture-set content hash (sha256 over sorted basename+bytes): `9a8171a09c241269a02eb6ef0d34a5454fb48849cbbdae10f37aa4698c7797e4`.

Round 11 could exercise TWO routes; this cut exercised FIVE, so the header's description, the publisher
feed and the whole Peers panel are now inside the exercised set (`overlay-has-description True`,
`peers-has-members True` at 10 of 33 peer sets carrying members -- PRINTED, not barred, since that
population is `AMGT-rk-4`'s).

AC3's browser half ran against the DEV-INTEGRATED branch `wk-amgt_resapp-12-23-portal` @`2453a7b4`, NOT
a local vite serve of a drain ref -- the change of meaning ADDENDUM 1 A1.4 chained this cell for.

## 3. Instrument note on AC3's `rc=0`

AC3's literal invocation ends `| tail -16; echo rc=$?`, so `$?` is **`tail`'s** exit code, not the
harness's. The recorded `rc=0` is the literal invocation's output as required. Because the claim feeds a
committed record, the harness's OWN exit code was measured separately on a second instrument
(`node ... >/dev/null 2>&1; echo "node_true_rc=$?"`) and is also **0**, so the recorded value is not a
pipeline artifact. Both readings are in the instance.

## 4. Controls

- **MUTANT (fired):** the `/overlay` capture was moved aside and AC2's invocation re-run BYTE-UNCHANGED
  -> `files 4`, `nonempty-bodies 4`, `overlay-has-description False`. The capture was restored and the
  re-run matched the baseline byte-for-byte (`restored_matches_baseline True`). The bar discriminates.
- **DETERMINISM (stable):** two same-input runs of AC2 compared -> `identical True`, rc identical.
  Disclosed: AC1 is a LIVE read, so its byte lengths move with live data (the issuer's amendment dry run
  measured overlay 50197 / peers 19603; this cut measured 50630 / 20036). The count bar `captured 5` and
  the rankings/thesis/coverage lengths were identical across both readings.

## 5. Surprise rows filed (two; work continued in both cases)

- **`AMGT_RESAPP-Z-W23-S2`** (OBSERVATION / INERT) -- AC4's invocation reads `portal/.git/HEAD`, but in a
  LINKED WORKTREE `portal/.git` is a FILE (a gitdir pointer), so the existence guard is False by
  construction and the invocation prints its fallback `branch_under_judgment see AC3 evidence` instead of
  the branch. AC3's evidence names no branch either, so the branch reached the L9 grader from neither
  named source. Supplied MEASURED in AC4's `output_evidence` instead, which is why the hazard is INERT.
- **`AMGT_RESAPP-Z-W23-S3`** (OBSERVATION / INERT) -- AC2's `overlay-has-posture` is an `any()` across all
  five bodies, and `posture` rides TWO of them (`/overlay` AND `/thesis`), so the bar reads True from
  `/thesis` alone. Surfaced BY this cell's own mutant control. AC2 is still met truthfully -- `/overlay`
  was captured, served 200 and does carry `posture`; the sibling bar `overlay-has-description` does
  discriminate `/overlay`. Residual named, not adjudicated here.

Both rows judge FORM only. Neither was repaired, widened or worked around: the criteria were run as
written and recorded as they came out.

## 6. Bounds honoured

No portal source edit was needed or made (this is an exercise cell). The superproject `portal` gitlink
was NOT staged and stays at `be8cf218`. Nothing pushed, merged, rebased, stashed or cleaned. No install.
No alarm/monitor/notification. No vendor call beyond the named deployed-adapter invokes. Collection left
off. Non-ASCII added to the channel: ZERO (file delta 122 before and 122 after, measured both sides).
