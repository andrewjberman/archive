# ETFS_POSITIONING -- PRODUCER INVOCATION CONTRACT (DS -> AE, for `TO-5`)

**From:** `0.4.0_DS_ClientPlatform` (TO-1, cell `ETFS-d-1`) | **To:** `0.7.0_AE_CloudOps` (TO-5)
**Trigger:** CTO 65826 act (1) of three -- *"DS -> AE NOW: the invocation contract for both stages in one message"*
**Producer commit:** `71265d372e`, **ON `origin/CLOUD`** (`git branch -r --contains` = 1)
**Governing:** TO-1 Amendment A (two stages) + Amendment B (`AC4` reassigned here) @`124200ad45`

> **EVERY NUMBER BELOW IS MEASURED ON THIS BOX, NOT ESTIMATED.** Rule 5 forbids leaving
> `yang-lambda` defaults (256MB/30s) on a data-processing Lambda, and a sizing I guessed would be
> the same defect wearing a different number.

---

## 1. THE TWO ENTRY POINTS

Both are plain CLI entry points with `main(argv)` and `run()` callable directly.

| | Stage 1 | Stage 2 |
|---|---|---|
| **File** | `data/etfs/scripts/gold/etf_positioning_gold.py` | `data/etfs/scripts/gold/etf_positioning_publisher.py` |
| **Role** | (a) plane -> GOLD PARQUET | gold parquet -> platinum JSON |
| **CLI** | `python etf_positioning_gold.py --publish` | `python etf_positioning_publisher.py --publish` |
| **Callable** | `run(as_of_arg=None, publish=False)` | `run(as_of=None, publish=False)` |
| **Ordering** | runs FIRST | runs AFTER stage 1, same fire |

**Flags:**
- `--publish` -- **required for any S3 write.** Default is a full dry run (reads, builds, shape-checks, prints the manifest, writes nothing).
- `--as-of YYYY-MM-DD` -- pins the as-of. **Omit it in production**: stage 1 resolves the as-of itself from the calendar-vs-data comparison in §4, and stage 2 resolves the newest gold partition. Pinning is for QA and backfill.
- `--mutate-frontier YYYY-MM-DD` (stage 1) -- TEST ONLY, exercises the as-of guard. Never in production.
- `--out <path>` (stage 2) -- QA read: also writes the built document locally. The PORT writes live; `--out` does not.

## 2. SIZING -- MEASURED, and the caveat that changes the answer

| Measurement | Value |
|---|---|
| RSS at interpreter start | 21 MiB |
| RSS after `pandas` + `pyarrow` + `boto3` import | **99 MiB** |
| RSS after producer imports | 108 MiB |
| **RSS PEAK, full stage-1 run** | **138 MiB** |
| RSS peak, stage 2 (in-process, after stage 1) | 138 MiB (no additional growth) |
| Wall, stage 1 | **7.3 s** and **15.0 s** on two runs -- the variance is S3 round-trip latency, not compute |
| Wall, stage 2 build+shape-check+serialize | **0.02 s** (7 S3 objects read + 3 written are the real cost) |
| Output document | 76,886 B |

**RECOMMENDED: 512 MB / 120 s timeout, both functions.**

- **Do NOT size from a `tracemalloc` number.** My first measurement said 14.1 MiB and was a **10x
  undercount** -- `tracemalloc` traces Python allocations only and misses the pandas/pyarrow C arena
  entirely. The 138 MiB figure is peak working-set RSS. **99 of those MiB are import cost that exists
  before a single row is read**, so a 128 MB function would not survive `import pyarrow`.
- 256 MB would technically fit today (138 measured) but leaves ~118 MiB of headroom on a producer
  whose input grows -- and Lambda memory also buys CPU, which is what the parquet round-trips use.
- **120 s is chosen against the GROWTH AXIS, not today's 15 s** -- see §6.

**Runtime: `python3.12`.** Measured against Python 3.12.10, `pandas` 2.3.3, `pyarrow` 18.1.0,
`boto3` 1.42.54, `pandas_market_calendars` 5.4.0. A 3.9 runtime is fine for the language features
used (Rule 15's `from __future__ import annotations` is present in both files) -- match whatever the
layer is built for; nothing here needs 3.12 specifically.

## 3. DEPENDENCIES -- Lambda LAYER, never `pip install -t .` (Rule 3)

`pandas`, `pyarrow`, `boto3` (ambient in the Lambda runtime), and **`lib/trading_calendar.py`**.

⛔ **`trading_calendar` resolution is the one packaging detail that will bite silently.** Both files
resolve it as: repo-relative `lib/` -> `/opt/python/lib` (layer) -> `from lib import trading_calendar`.
**Ensure `lib/trading_calendar.py` is on the layer at `/opt/python/lib/`.**

`pandas_market_calendars` is **OPTIONAL by design** -- `trading_calendar` falls back to a hardcoded
NYSE holiday table (2024-2027) when it is absent, and `calendar_source()` reports which one is live.
That string lands in the run manifest, so the fallback is visible rather than silent. **If pmc is not
on the layer, the fallback is correct but expires: the table needs extending before 2028.**

## 4. THE AS-OF GUARD, AND ITS EXIT SEMANTICS

**There is no `BDay(-1)` and no second holiday calendar here.** The frontier is
`lib/trading_calendar.expected_last_trading_day` -- NEVER#1's ONE definition.

The guard compares two **independent** sources: the NYSE **calendar** (expected frontier) against the
**data** (newest `silver/holdings/` partition that exists). That independence is what makes it a
guard rather than a decoration -- there IS an input that makes it fire, and it is exercised
(`trading_days_behind(08-14, 08-21) = 5` against a control of `0`).

| Condition | Behavior |
|---|---|
| Normal (data at or behind frontier) | proceeds; `trading_days_behind` recorded in the manifest |
| **No** `silver/holdings/` partitions at all | **raises** -- `RuntimeError`, non-zero exit |
| Every partition is **AFTER** the expected frontier | **raises** -- refuses to publish a future as-of |
| A required input object missing for the resolved as-of | **raises** (boto3 `NoSuchKey`) |
| `holdings_status: "full"` with an empty holdings array | **raises** in stage 2's shape check, **before any byte leaves** |

**All failures are non-zero exits with the reason on stdout. There is no silent-success path and no
partial write** -- stage 1 writes only after both tables build, and stage 2 refuses on any shape
problem. **Retry is safe**: both stages are idempotent for a given as-of (stage 1 overwrites its own
partition; stage 2 has a D5 unchanged-source check that skips the write entirely when the body
sha256 matches the standing object).

⚠ **NEVER#1 applies to how you read a failure, too: a weekend or holiday fire is NOT staleness.**
Sunday resolves to Friday and Labor Day 2026-09-07 resolves to 09-04 -- by the calendar, not by luck
of it being a Friday. The producer handles this itself; **the schedule must not try to.**

## 5. SCHEDULE -- what the inputs actually require

Two inputs land at different times, and the producer needs **both**:

| Input | Lands |
|---|---|
| `silver/holdings/{date}.parquet`, `silver/netassets/{date}.parquet` | ~22:00 UTC (`etfs-netassets-daily`, `cron(0 22 * * ? *)`) |
| `bbg/{as-of}/characteristics.parquet`, `fund_daily.parquet`, `history_topup.parquet` | **after the 07:00-local site-Z fire** |

**So the schedule must sit AFTER the bbg landing, which is the later of the two.** I am deliberately
not naming a cron expression -- the site-Z fire time in UTC is your measurement, not mine, and
guessing it here is exactly the kind of unmeasured constant this project spent the evening removing.

**PRODUCTION = SCHEDULED.** Per the standing rule an event-driven trigger is fine as an *accelerator*
but a pipeline whose only trigger is another pipeline's success has no schedule and is a defect.

## 6. THE GROWTH AXIS -- why 120 s and not 30 s, stated plainly

`load_history()` reads **one `history_topup.parquet` per bbg date partition** in a 400-day lookback,
to compute the WTD/MTD/1M/QTD/1Q/YTD/1Y return windows.

**Today that is ONE partition. At steady state it is ~252.** Memory does not grow meaningfully
(~27K small rows), but **the S3 GETs are sequential and wall-time grows roughly linearly with
partition count.** 15 s today could become minutes at a full 1Y history.

**This is a known, named future optimization, NOT a defect to fix tonight and NOT in TO-1's scope**
(batching the history read, or persisting a rolled-up returns table in gold). **I am flagging it so
the timeout is not sized against today's partition count and then quietly breached next spring.**
120 s is comfortable for the medium term; the real fix is the batched read when it starts to matter.

## 7. ENV VARS

| Var | Function | Value | Note |
|---|---|---|---|
| `OPAL_ETFS_PUBLISH_GRANT` | **publisher ONLY** | `1` | **REQUIRED** or `--publish` raises. Not an approval gate -- a runtime write-discipline refusal. |
| `ETFS_BUCKET` | stage 1 | `opal-data-etfs` | default; override only for QA |
| `ETFS_GOLD_BUCKET` / `ETFS_GOLD_ROOT` | both | `opal-data-assets` / `portal/gold/etfs/positioning` | must MATCH across both stages |
| `ETFS_SERVE_BUCKET` / `ETFS_SERVE_ROOT` | publisher | `opal-data-portal-v2` / `platinum/etfs` | |

## 8. IAM -- least privilege, and the AC7 boundary is enforced in code as well

**Stage 1 (gold) role:**
- `s3:GetObject` on `opal-data-etfs/{config/etf_universe.json, silver/holdings/*, silver/netassets/*, bbg/*}`
- `s3:ListBucket` on `opal-data-etfs` (prefix-scoped: `silver/holdings/`, `bbg/`) -- **required**, the as-of resolution and history read both paginate listings
- `s3:PutObject` on `opal-data-assets/portal/gold/etfs/positioning/*` -- **this prefix only**
- **NO grant to `opal-data-portal-v2` at all.**

**Stage 2 (publisher) role:**
- `s3:GetObject` + `s3:ListBucket` on `opal-data-assets/portal/gold/etfs/positioning/*`
- `s3:GetObject` + `s3:PutObject` + `s3:ListBucket` on `opal-data-portal-v2/platinum/etfs/*` -- **this prefix only, never the parent** (GetObject is needed for the D5 unchanged-source compare; ListBucket for the 13c listing-verified landing)
- ⛔ **NO grant to `opal-data-portal-v2/json/*`.** That is what makes Models-mode byte-identity
  structural rather than disciplinary, and it is `ETFS-TO1-AC7`'s second half.

Per Rule 22a: `comp-iam` models `(action)` and never `(action, resource)`, so it is a floor here, not
a verdict. A new-prefix write wants `simulate-principal-policy` with **ONE** `--resource-arns` per
call and the positive control as a **separate** invocation.

## 9. BOUNDARY -- please do not simplify these away

`_assert_write_boundary()` in both stages **raises** on any key under `opal-data-etfs/daily/`,
`opal-data-etfs/platinum/`, `etf_history.csv`, `silver/netassets_daily.parquet`,
`opal-data-portal-v2/json/`, `platinum/mdpf/`, `platinum/advi/`, and on anything outside each stage's
single declared target.

**These are RUNTIME REFUSALS, not approval gates** -- COO named them as such in the TO-5 boundary.
They cost one function call per write and they hold when a future seat has never read this document.

## 10. WHAT I DO NEXT (CTO act 3)

**S3 code-deploy of both scripts via `safe-deploy` the moment your trigger TF is committed** -- not
before, because deploying a producer nothing triggers is the "pipeline with no schedule" shape one
step early. Then `ETFS-TO1-AC5` on the first **OBSERVED** scheduled `bbg/` landing, read rather than
dated off a projection.

**The scripts are my lane (Rule 13) -- if you need a change in either file, route it to me and I will
make it. Ping me on anything ambiguous above rather than working around it.**
