# 07-10-frontier ingestion check -- orion/inflection + eclipse/inflection bronze (monolith)

**Serial:** 0.6.2_AE_PartnerETL | **Date:** 2026-07-15 ~18:2x-18:4xZ | **Authority:** Andrew-direct
(COO terminal ~18:2xZ, dispatch 20260715T181941Z; evidence shape per CTO via COO 182145Z)
**Mode:** READ-ONLY throughout (ListObjectsV2 / describe-rule / get-function-configuration /
get-metric-statistics / source reads at HEAD). Zero writes, zero invocations by me, zero schedule
motion. INF-hold guards observed: nothing here advances the chain; Door 6 untouched; frozen-3 untouched.

**ANDREW'S HYPOTHESIS, VERBATIM:** "there is clearly no ingestion lambdas set up for any bronze
buckets that only have data through 7/10, so that is the first thing that needs to be checked on."

**VERDICT: REFUTED for both 07-10-frontier channels -- with the frontier fully explained.** The
ingestion path EXISTS, is ENABLED, FIRED CLEAN TODAY, and its destination is at exact SET PARITY
with its source. The 07-10 frontier is the UPSTREAM INF raw-producer death under the standing
INF-chain hold (Door 5 class) -- the mirror is faithfully reflecting a deliberately-held source,
not failing to ingest. MISSING-WIRING is excluded on live evidence; UPSTREAM-DEAD(-BY-HOLD) is
confirmed at source + live + census, below.

---

## (1) The ingestion mechanism that EXISTS (live primitives)

ONE lambda serves both channels; TWO EventBridge rules target it (denominator: enumerated live via
`list-rule-names-by-target` against the function ARN -- exactly 2, nothing else fires it):

| Primitive | Live state (read 2026-07-15 ~18:2xZ) |
|---|---|
| Lambda `opal-assets-ingest-mirror` | 512MB / 900s, `MONOLITH_BUCKET=opal-data-assets`, LastModified **2026-07-14T07:15:50Z** (the C2 leg -- the lambda is one day old) |
| Rule `opal-assets-ingest-mirror-inf-daily` | **ENABLED**, `cron(15 14 * * ? *)` -- "Poll opal-data-inf bronze (orion + eclipse) into the monolith, after the last orion pull of the day (inf-api-txn-daily, 13:47Z)" -- covers BOTH channels in scope |
| Rule `opal-assets-ingest-mirror-cot-daily` | **ENABLED**, `cron(30 3 * * ? *)` -- cot row, out of scope here |
| CW `AWS/Lambda Invocations` (Sum, daily, 07-10 -> 07-15) | 07-14: **10** (Errors 3 -- deploy-day runs), 07-15: **2** (Errors **0**). No datapoints 07-10..07-13: the lambda did not exist yet. **Both of today's scheduled fires ran clean, ~4h before this check.** |

Source map (mirror `lambda_function.py` MAP rows, source @ HEAD): orion row polls
`opal-data-inf` `bronze/{assets,positions,transactions,performance}/` -> `orion/inflection/bronze/`;
eclipse row polls `bronze/eclipse/` -> `eclipse/inflection/bronze/`. `COERCED_SUFFIXES=(".parquet",)`
is NEVER mirrored (ruling 16: raw only under bronze -- lambda_function.py:70-71).

**Exercised (the sharpest wiring proof -- the destination ties to the source exactly):**

| Channel | Monolith (dst) | Upstream raw (src) | Set parity |
|---|---|---|---|
| orion/inflection/bronze | 4,640 `.gz`, max 2026-07-10 | 4,640 `.gz` across the 4 type prefixes (2,265+2,265+58+52), max 2026-07-10 | **4,640/4,640** |
| eclipse/inflection/bronze | 624 `.json`, max 2026-07-10 | 624 `.json`, max 2026-07-10 | **624/624** |

A mirror at exact set parity with a source whose frontier is 07-10 produces a 07-10 destination
frontier while working PERFECTLY. That is what the census shows.

## (2) Bronze frontier vs the TRADING-DAY frontier (NEVER#1)

2026-07-10 is a FRIDAY; 07-11/07-12 are the weekend and do not count. `lib/trading_calendar.py`
(the one frontier definition): `trading_days_behind(2026-07-10 @ 2026-07-15)` = **3 trading days**
(07-13, 07-14, 07-15; wall-clock 5 days). Under the estate's T-1 default the healthy expectation
today is 07-14, so the TRUE gap net of convention is 2 trading days -- but this is not a staleness
finding either way: the gap is fully mechanism-explained below, and the number is quoted only
because the evidence shape asks for it.

## (3) The causal mechanism, GROUNDED (prior CONFIRMED, not inherited)

The recorded prior (mirror ran clean 07-14, wrote 0 on these rows, because the INF raw producer died
07-10 under the standing hold) is **CONFIRMED on three independent legs:**

- **Census discriminator (live, run-time enumerated):** in the SAME upstream prefixes, raw `.gz`
  stops at **2026-07-10** in ALL FOUR orion types (and eclipse `.json` likewise), while the coerced
  `.parquet` continues to **2026-07-15** in assets/positions. A dead SCHEDULE or missing WIRING
  cannot produce that signature -- only a dead RAW producer beside a live parquet producer can.
  (assets: 2,265 gz / 2,270 parquet; positions: 2,265 gz / 2,274 parquet.)
- **Source-confirmed at the mirror** (`opal-assets-ingest-mirror/lambda_function.py:20-30` @ HEAD):
  "The raw producer died 2026-07-10 while the parquet producer kept running, so 10 dates are
  parquet-ONLY (assets 3 + positions 7)... We do NOT backfill them from the .parquet" (ruling 16 /
  Rule 17a -- a coerced file never enters the canonical spine as bronze).
- **The hold doc** (`org/critical_paths/HOLD_INF_CANONICAL_NNA_REBUILD_20260713.md`): the raw sync
  dies at step zero on the basename-collision FATAL -- and fixing that collision IS Door 5 (doc
  headers at :72/:119; ":3239 Door 5 is opened by 0.7.0, reversibly, revert pre-staged -- never as
  'cleanup'", sovereign-order territory). "Restart the raw producer" IS Door 5. The 07-10 frontier
  is the HOLD WORKING.

**Discrimination verdict: UPSTREAM-DEAD (deliberately, under the standing hold). NOT missing
wiring, NOT a dead schedule, NOT an error stream** (today's fires: 0 errors; set parity exact).
Nothing INFERRED remains in the chain: every link above is cited to a live primitive or source line.

## Denominators (of every scan reasoned from)

- Rules in the path: 2/2 enumerated by target-ARN (no other trigger exists for this lambda).
- Lambdas in the path: 1 (the mirror); upstream producers characterized via their artifact trail
  (the census) + the hold doc -- not re-enumerated live, deliberately: enumerating the held INF
  producer estate is the hold's own record, and touching it is not this check's lane.
- Objects: monolith 4,640 + 624; upstream 4,535 + 4,539 + 107 + 102 + 624 (logs/ and
  _parity-snapshot/ excluded per the mirror's own exclusions).
- CW: 6-day window, daily buckets, Invocations + Errors both read.

## Surfaced smells (recorded, NOT acted on -- INF-side, not this lane)

1. Upstream `bronze/transactions/` + `bronze/performance/` PARQUET max is **2026-06-30** while
   their raw `.gz` reaches 07-10 -- the coerced producer's cadence differs by type. Whoever owns
   the INF census may already know; recorded here so it is not lost.
2. The 10 parquet-ONLY dates (assets 3 + positions 7) remain HONEST HOLES per ruling 16 -- already
   the recorded position; re-confirmed by this census, no drift.

## What this check did NOT do (guards)

No producer restart, no schedule motion, no event wiring, no writes anywhere, no Door-6 key
contact, no frozen-3 contact, no INF-chain advancement of any kind. Remediation of the frontier
== opening Door 5 == Andrew-by-name sovereign territory, per the hold doc's own terms.
