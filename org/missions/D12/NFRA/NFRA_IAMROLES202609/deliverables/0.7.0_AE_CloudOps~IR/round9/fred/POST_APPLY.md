# IAM-z-6 PHASE B -- POST-APPLY: the retire landed, the 23:00Z fire ran clean, and the served yield curve is unfrozen after 67 days

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-6` - **Risk:** WORLD
**Pair:** `ledger/NEVER_WIDEN_ROUND9_Z-6_COO_HALF.md` @`f7eb4cf699` + `..._CTO_HALF.md` @`c6fc383a85`
**NEVER-2 entry:** `iamroles-r9-fred-retire` (opened 22:28Z, legs committed @`4810c26f07`)
**Graded run:** the scheduled `cron(0 23 * * ? *)` fire, RequestId `73f2db9d-a435-4223-ae87-6a68017f7455`
**Read time:** 2026-10-11 23:00Z - 23:15Z.

---

## THE TWO REQUIRED LINES

```
FRED-RUN: statusCode=200 yield_curve_success=true
SERVED-KEY: LastModified=2026-10-11T23:00:58+00:00 as_of=2026-10-11
```

### How each half of the first line was established

`yield_curve_success=true` is **read directly**: the run's own log carries
`Yield curve refreshed: 10 series` and `OK: Uploaded to s3://opal-data-portal-v2/json/macro/yield_curve_fred.json`,
which the handler emits only on the fold's success path.

`statusCode=200` is **DERIVED from the log, not read off it**, and the derivation is stated because an
async EventBridge invocation does not log the handler's return value -- there is no line in CloudWatch
that contains the string `statusCode`. Every premise is a log line from this run:

1. `Successfully processed 3/3 series for daily frequency` -- so `process_frequency` returned via its
   success path. Its only other return is `{'success': False, 'error': 'No series configured'}`, which
   is preceded by `No series configured for frequency:` -- **0 occurrences** in this run.
2. **0** lines matching `Lambda execution error` and **0** matching `ERROR` across all **138** log lines,
   and the stream ends with a normal `END` + `REPORT` -- so the outer `except` never fired.
3. The handler's only branch is `if result['success']: return 200 else: return 500`.

(1) and (2) fix `result['success'] is True` and no exception, so (3) yields 200. If a future reader wants
a measured `statusCode`, it needs a synchronous `invoke`; I did not make one, because an extra invocation
would write the served key outside "the function's own next fires", which is the only writer the pair
permits.

---

## BRANCH: **A**, not A'

The CTO half's addition was that `run()` uploads even when tenors are only carried forward, so a moving
`LastModified` is not proof of fresh data, and the grade must read the `PRESERVE:` lines. Measured:

| probe | result |
|---|---|
| `PRESERVE:` lines in the run log | **0** |
| `NO-REGRESSION GUARD` lines | **0** |
| `preserved_tenors` in the served object | **`[]`** (empty) |
| `Successfully fetched 10/10 series` | present; every tenor on **attempt 1/3** |
| tenors valued in the object | **10 of 10**, 497 observations each |

So nothing was carried forward from the 2026-08-05 artifact. This is branch **A**.

---

## THE ONE THING THAT DID NOT MATCH THE HALVES, AND WHY IT IS NOT A DEFECT

Both halves name the expected newest observation as **Friday 2026-10-09**. The artifact's newest
observation is **2026-10-08** (Thursday), uniformly across all ten tenors.

Resolved against the trading calendar before calling anything stale (`lib/trading_calendar.py`,
`calendar_source: NYSE/hardcoded-fallback-2010-2027`):

```
is_trading_day 2026-10-08 Thu = True    2026-10-09 Fri = True
               2026-10-10 Sat = False   2026-10-11 Sun = False   2026-10-12 Mon = True
expected_last_trading_day(at the 23:00:58Z fire) = 2026-10-09
prev_trading_day(2026-10-11)                     = 2026-10-09
trading_days_behind(2026-10-08)                  = 1
trading_days_behind(2026-10-09)                  = 0
```

So the curve is **one trading day** behind the last trading day. Two reasons this is the source's
frontier and not something this act introduced:

1. **The lag is uniform across all ten tenors** (`len(set(newest_per_tenor)) == 1`). A fetch defect or a
   partial preserve would differ per series; a publisher frontier is the same for all. The log confirms
   each tenor succeeded on **attempt 1/3** with 497 observations -- the fetches returned everything FRED
   held.
2. **The frozen artifact had the identical shape.** Reading the pre-act version
   `4B7uNcT9Rli6_4LWUQORdWyhoBaABq.l` as a control:

   | | frozen version | this run |
   |---|---|---|
   | written | 2026-08-05 (Wed) | 2026-10-11 (Sun) |
   | newest observation | 2026-08-04 (Tue) | 2026-10-08 (Thu) |
   | trading days behind its own write date | **1** | **1** |
   | tenors valued | 10 | 10 |
   | `preserved_tenors` | n/a | `[]` |

   Both sit exactly one trading day behind. **The lag is unchanged by this act** -- the fold is producing
   exactly what it produced before the freeze. FRED publishes the H.15 DGS series one business day late.

`2.0.0_SA_COO~ZI` read the same fire independently at 23:04-23:08Z (msg 33412) and reached the same
conclusion on all three counts (branch A, `preserved_tenors=[]`, 10-08 as FRED's frontier). Recorded as
corroboration, not as the basis: both reads used the same two instruments, so they are not independent
evidence of the frontier claim -- the uniformity and the frozen-version control are.

---

## A PRE-EXISTING LABEL DEFECT IN THE SERVED ARTIFACT (not introduced, not mine to fix)

The object's `data_as_of` is the **generation date**, not the data's as-of date:

| version | `data_as_of` | `generated_at` | newest observation |
|---|---|---|---|
| frozen 2026-08-05 | `2026-08-05` | `2026-08-05T23:02:29` | `2026-08-04` |
| this run | `2026-10-11` | `2026-10-11T23:00:57` | `2026-10-08` |

In both, `data_as_of == generated_at`'s date and **differs from** the newest observation. A portal
consumer reading `data_as_of` would believe the curve is as of 2026-10-11 when its freshest point is
2026-10-08 -- a value that does not carry its claim, in a SERVED artifact. It is **pre-existing**: the
control above shows the same mislabel in the artifact written before this act, so this is not a
regression and the `as_of=` figure in the required SERVED-KEY line above is reported as the object states
it, not as I would compute it. Out of this cell's BOUNDS (only `lambda_fred_ingestion.py` changes; the
field is written by `ingest_yield_curve_fred.py`). Filed as a row rather than fixed in flight.

---

## THE ACT, AS LANDED

| step | evidence |
|---|---|
| baseline re-read (the pair's stop condition) | served key `4B7uNcT9Rli6_4LWUQORdWyhoBaABq.l` and `CodeSha256 ztoby...` both **MATCHED** -> signed |
| code | `2bc65a62f5` on `wk-iamroles-r9-fred`, drained to `box/sitez` at `b8370f67eb` (safe-merge rc=0; tree check 1 needed / 0 dropped / 0 foreign) |
| artifact | uploaded as VersionId `J2lfVxO4FBCQeDR5Iwyt7oiSPikII6DS`; `content-sha256` metadata **read back off the object** as `KdzPgI23K0f4Af5dIOqbyJTQ2SaeZgR+pKI5T4rMdRM=` |
| apply | `safe-apply` of the **saved** targeted plan: 1 changed, 0 added, 0 destroyed; tombstone-gate CLEAN |
| equality check | 3 of 46 attributes moved: `s3_object_version` T5QPdx->J2lfVx, `source_code_hash` ztoby->KdzPg, computed `last_modified`. No env, schedule, IAM, add or destroy |
| live function | `CodeSha256` == signed value; `State Active`, `LastUpdateStatus Successful`; env keys still **0** |
| 0-diff | untargeted plan **28 resource_changes, all no-op**, 0 to destroy |
| running bytes | deployed zip re-downloaded: member sha256 `cdb8a33a...` **== the committed blob**; 195 members; `ingest_yield_curve_fred.py` byte-unchanged; `put_object` occurrences in the running code **0**, with `FREDYieldCurveIngestion` present as the positive control |
| the fire | RequestId `73f2db9d`, 23:00:28->23:00:57Z, Duration 28510 ms, Max Memory 105/512 MB, 0 ERROR lines of 138 |
| served key | `2026-08-05T23:02:30Z` / `4B7u...` / 675314 B -> **`2026-10-11T23:00:58Z` / `iPk91o5i_rip1lrwK0gxVcCmRzSiKtdO` / 672091 B** |

**One correction to the PHASE A survey:** it recorded the diff as `26 insertions / 90 deletions`. The
committed diff is `26 insertions / 91 deletions` -- the survey's count was taken before the gate caught
the orphaned `import os`, whose removal is the 91st deletion. The form, the file and the permitted set
are unchanged; the number in the signed-against document was one line stale and is corrected here rather
than left to stand.

---

## THE OTHER FOUR FIRE PATHS (branch C's scope)

Only the daily path has fired since the apply. The other four rules that drive this function
(`weekly` THU 14:00, `monthly_early` 1st FRI 15:00, `monthly_mid` the 15th, `monthly_late` the 25th) have
not yet fired, and all four previously failed for the same `NoSuchBucket` reason. They take the identical
`process_frequency` path the daily run just exercised at 3/3 series, so the expectation is 200 -- but
that is **inferred, not measured**, and the first measurement is the Thursday 2026-10-15 weekly fire.
Branch C stays live until then; I am not closing it by assertion.

---

## DISPOSITION

- Branch **A** realized. The served portal yield curve moved after **67 days** frozen.
- `AC1` PASS: `LastModified 2026-10-11T23:00:58+00:00` is after `2026-10-11T22:59:00`.
- `AC2` PASS: the `FRED-RUN:` line above, with its derivation stated.
- `AC3`: the NEVER-2 entry closes with this record.
- `AC4` is JUDGMENT and not self-graded (`3.0.0_SA_CVO~Z`): the data for it is 10 of 10 tenors valued at
  497 observations each, newest 2026-10-08 = 1 trading day behind, and no other frequency measured yet.
