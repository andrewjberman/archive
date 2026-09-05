# EG-s-10 -- the trading calendar: one library, three vendored copies, and which calendar each producer resolves

**TO:** `ETFS_GUARDRAIL.TO-EG-s-10` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `5376ecaa8b` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** verify (no source changed).

## 1. S10-AC1 -- the four-copy sha256 census

**Invocation:**
```
sha256sum lib/trading_calendar.py infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm/trading_calendar.py infra/aws/lambda/opal-assets-absence-check/trading_calendar.py
```
**Output (rc=0, denominator 4 of 4 paths):**
```
41b1c0c12651c62e59d27537a5bafb5bc34a3bb6562d94d57029a2f77ccac4c6 *lib/trading_calendar.py
41b1c0c12651c62e59d27537a5bafb5bc34a3bb6562d94d57029a2f77ccac4c6 *infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py
41b1c0c12651c62e59d27537a5bafb5bc34a3bb6562d94d57029a2f77ccac4c6 *infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm/trading_calendar.py
41b1c0c12651c62e59d27537a5bafb5bc34a3bb6562d94d57029a2f77ccac4c6 *infra/aws/lambda/opal-assets-absence-check/trading_calendar.py
```

**Drift verdict, per copy:**

| Path | sha256 | Drift vs `lib/trading_calendar.py` |
|---|---|---|
| `lib/trading_calendar.py` | `41b1c0c1...ccac4c6` | -- (the library itself) |
| `infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py` | `41b1c0c1...ccac4c6` | **IDENTICAL** |
| `infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm/trading_calendar.py` | `41b1c0c1...ccac4c6` | **IDENTICAL** |
| `infra/aws/lambda/opal-assets-absence-check/trading_calendar.py` | `41b1c0c1...ccac4c6` | **IDENTICAL** |

All four hashes match. Diff line count: 0 for all three vendored copies. No drift found at this commit.

## 2. Public API

```
is_trading_day(date: object) -> bool
prev_trading_day(date: object) -> dt.date
trading_days_between(start: object, end: object) -> list[dt.date]
trading_days_mtd(date: object) -> list[dt.date]
total_trading_days_in_window(start: object, end: object) -> int
calendar_source() -> str
```
All six names are present and importable (`lib/trading_calendar.py:81,93,123,143,155,160`). `calendar_source()` prints `"NYSE/pandas_market_calendars"` (measured directly, s.3 below).

## 3. S10-AC2 -- trading-day counts, 2026-07 and 2026-08

**Invocation:**
```
python -c "import sys; sys.path.insert(0,'lib'); import trading_calendar as t; print('SOURCE=%s AUG2026=%d JUL2026=%d' % (t.calendar_source(), len(t.trading_days_between('2026-08-01','2026-08-31')), len(t.trading_days_between('2026-07-01','2026-07-31'))))"
```
**Output (rc=0):**
```
SOURCE=NYSE/pandas_market_calendars AUG2026=21 JUL2026=22
```
August 2026 = 21 trading days, July 2026 = 22 trading days -- both match the brief's stated numbers (22 and 21).

## 4. S10-AC3 -- the library's own battery

**Invocation:**
```
python -m pytest lib/tests/test_trading_calendar.py -q
```
**Output (rc=0):**
```
22 passed in 1.69s
```

## 5. S10-AC4 -- neither target producer carries a calendar

**Invocation:**
```
python -c "import os; print('COT_HAS_CAL=%s BD49F_HAS_CAL=%s' % (os.path.exists('infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/trading_calendar.py'), os.path.exists('infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/trading_calendar.py')))"
```
**Output (rc=0):**
```
COT_HAS_CAL=False BD49F_HAS_CAL=False
```
The PRD's premise (s.7.2 row S10: "neither target producer has one") holds true at HEAD `5376ecaa8b`.

## 6. S10-AC5 -- THE ANSWER (judgment; recorded, no verdict)

### 6a. Which calendar each of the three named producers resolves at runtime today

| Producer | Calendar it resolves | Mechanism | Consequence for the reporting-obligation window |
|---|---|---|---|
| `inf-etf-ownership-daily` (Inflection, the only one of the three actually named in the PRD's S10 row with a copy) | **Its own vendored copy** — byte-identical to `lib/trading_calendar.py` (sha256 match, s.1 above) | `lambda_function.py:72 import trading_calendar as tcal`; used at `:142` (`tcal.prev_trading_day(day)`, freeze-vs-prior-session comparison) and `:164` (`tcal.is_trading_day(day)`) | Correctly identifies trading days and the prior session for its freeze check; a source-of-truth match with `lib/`, so its window logic agrees with the estate's ONE frontier definition (NEVER#1) as of this commit. No divergence risk *today*, but the file is a fourth un-reconciled copy under the pending CTO ruling (s.6c below). |
| `cot-etf-ownership-daily` (the `EG-s-1` target) | **NONE.** No `trading_calendar.py` exists in its source dir (`infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/`, confirmed empty of it by `S10-AC4`) | `lambda_function.py:85-94 _latest_partition()` enumerates the newest `date=` partition under `fact_holdings` by S3 `ListObjectsV2` and takes whatever key sorts last; no trading-day arithmetic anywhere in the file | It resolves **no calendar at all** and has no catch-up/backfill scan: `_latest_partition()` finds the newest partition present, so if an upstream date silently never lands (the file's own comment names the known 07-31 gap) or a scheduled run is missed, nothing re-checks earlier dates against a trading-day frontier -- a missed reporting day inside the obligation window is invisible to this producer as it stands today. This is exactly the gap `EG-s-1` is cut to close by vendoring the calendar and adding `_window_dates()`. |
| `bd-49f-etf-ownership-daily` (the `EG-s-2` target) | **NONE.** No `trading_calendar.py` exists in its source dir (`infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/`, confirmed by `S10-AC4`) | `lambda_function.py:50-56 _latest_partition()` enumerates the newest `date=` partition under `fact_rps`; same shape as `cot`, no trading-day arithmetic | Same consequence as `cot`: no calendar frontier, no catch-up scan, so a missed day inside the reporting-obligation window is not detected by the producer as it runs today. `EG-s-2` is cut to add exactly this. |

### 6b. Drift between the library and each vendored copy

Zero drift, all three (s.1). No `DIFFERS` verdict to report; the sha256 census is 4-for-4 identical, byte-for-byte, at this commit. `git log` shows no divergent edit history across the four paths as of `5376ecaa8b`.

### 6c. Vendoring recommendation for the ports (`EG-s-1`, `EG-s-2`) -- WITH A REASON, AND A CONFLICT TO RECORD

The TO's suggested default is "vendor `lib/trading_calendar.py` byte-identical into each producer's source dir and add it to the source map `files`, the same pattern `inf-etf-ownership-daily` already uses." That pattern is real (s.6a) and it is what `TO-EG-s-1` (`:23`, `S1-AC3`) and `TO-EG-s-2` (`:22`, `S2-AC3`) already mandate, byte-for-byte, as a MECHANICAL criterion.

**But the tree already carries a ruling against exactly that act for a new consumer.** `infra/aws/terraform/etfs-positioning/producer-lambda.tf:169-183` (commit `1da1e2b73b`, 2026-08-24, 11 days before this round's `5376ecaa8b` L6 issuance) records: *"CTO~Z ruled (msg 5462): MINT THE LAYER, NOT A FIFTH COPY. Rule 3 is dispositive -- dependencies go in layers and inline vendoring needs explicit approval; a fifth in-repo copy IS inline vendoring and nobody approved one. The estate's four existing byte-identical copies are that exception taken four times without a word."* -- and its own scope note: *"this authorises the layer for THIS function [`etf-positioning-producer`] and nothing else. The three pre-existing Lambda copies are NOT migrated -- a separate cell with its own owner."*

Read together: the four copies this TO's own S10-AC1 census just measured as identical are, per that ruling's own words, an unapproved exception "taken four times without a word" -- and `TO-EG-s-1`/`TO-EG-s-2` are cut to take it a fifth and sixth time, also without citing or reconciling the ruling. Neither the PRD's S10 row (`org/missions/D8/ETFS/ETFS_GUARDRAIL/prd/ETFS_GUARDRAIL_PRD.md:399`, drafted after the ruling landed) nor the round's decomposition (`decompositions/ETFS_GUARDRAIL_DECOMP.md:51`) mentions the layer mechanism or the ruling.

**Recommendation:** given the ruling exists and is scoped narrowly ("THIS function and nothing else," not a blanket authorization for future consumers), the correct mechanism for `cot-etf-ownership-daily` and `bd-49f-etf-ownership-daily` is a first-party Lambda layer built the same way `opal-trading-calendar-layer` is (`infra/aws/lambda/layers/opal-trading-calendar-layer/build-layer.sh`, copying from `lib/` at build time, committing nothing) -- attached via `layers = [...]` in each producer's `.tf`, NOT a sixth and seventh in-repo copy. This is a recommendation, not an act (this TO changes no code): it is filed as `ETFS_GUARDRAIL-W1-S1` in the round's investigation file because `TO-EG-s-1`/`TO-EG-s-2` as currently written direct the opposite mechanism as a MANDATORY, mechanically-graded criterion, and neither TO's issuer cites the ruling. Whoever executes those cells next, and the CVO at L9, should read `ETFS_GUARDRAIL-W1-S1` before those criteria are graded.
