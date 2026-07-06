# INF incremental perf-pull -- M1 design + scope (CTO arch-gate request)

**Owner:** 0.6.1_AE_PartnerETL (INF pull lane)
**Date:** 2026-07-06
**Target script:** `data/inf/manual_api/pull_inflection_performance_rest.py` -> `s3://opal-data-inf/bronze/performance/{date}.jsonl.gz`
**Arch-gate:** CTO (touches the INF gold chain: bronze/performance -> convert_performance_to_silver -> INF_C_02/03 -> served perf).
**Why now:** this is the REAL root of the 07-02..07-06 gold freeze (the ceiling-bump was the interim; this is what lets `PERF_SILVER_STALENESS_CEILING_DAYS` revert 10->2).

---

## 1. Problem (confirmed live)

`bronze/performance/` is **frozen at 2026-06-30** (every object last-modified 2026-07-01 01:28Z; nothing written since -> 07-01..07-06 = 6-day gap). `silver/api_dims/performance/` is fresh to 07-06 -- that is the SEPARATE `pull_inflection_performance_dim.py` pull; the freeze is isolated to the REST TWR pull.

**Root mechanism (source-grounded, `pull_inflection_performance_rest.py`):** `_pull_client_continuous` re-pulls the ENTIRE history `HISTORY_START=2020-01-01 .. today` for EVERY client, EVERY night:
- `_chunk_windows(2020-01-01, today)` @ `CHUNK_DAYS=300` = ~8 windows/client.
- ~300 clients x 8 windows = **~2,400 Orion REST calls/night**, each `REQUEST_TIMEOUT_S=60` x up to 3 retries.
- When Orion slowed (since ~06-30), per-call latency x 2,400 calls blows past the 600s chain budget -> the step hangs -> `convert_performance_to_silver` staleness-blocks the chain.

~99% of those 2,400 calls re-fetch history that never changes. Only the recent tail carries new data each night.

## 2. M1 design -- trailing-window + prior-bronze merge + weekly-full backstop

### 2a. Nightly (default) = TRAILING window only
- Pull one window `[anchor_date, today]` per client where `anchor_date = today - TRAILING_DAYS` (propose `TRAILING_DAYS = 30`, single sub-300d window/client).
- ~300 clients x 1 window = **~300 calls/night** (8x fewer). At the adaptive limiter's rate this completes well under 600s.

### 2b. Prior-bronze merge (chain-link continuity)
- Load the most-recent prior `bronze/performance/{prev}.jsonl.gz` (the continuous cumulative-growth index, `factor[inception]=1.0`).
- For each client: keep prior rows `date < anchor_date`; take the trailing window's within-window daily returns (`r_d = wf[i]/wf[i-1]-1`, exactly the current chain-link math) and multiply onto the prior index's cumulative `factor[anchor_date]` (the splice point). Result = a gap-free continuous index identical in shape to today's full-pull output, at 1/8th the calls.
- The trailing window's first detail is the anchor (factor ~1.0, no return) landing ON `anchor_date`, which MUST exist in prior bronze -> its return chains onto `prior.factor[anchor_date]`. `TRAILING_DAYS=30` >> nightly cadence guarantees overlap even across a multi-day gap.

### 2c. Weekly-full backstop (self-heal)
- Once/week (and whenever: no prior bronze, a client absent from prior bronze [new client], a detected gap > TRAILING_DAYS, or an integrity-flag), run the existing FULL 2020->today pull for the affected clients (or all). Bounds drift, backfills history corrections, onboards new clients. The current full-pull code path is retained verbatim as this backstop -- M1 ADDS the incremental fast-path, it does not remove the full path.

### 2d. Correctness / integrity (unchanged guarantees)
- Same anchor-at-1.0 + positive-factor integrity asserts already in `main()` (L372-379) run on the merged frame.
- New-client fallback: client in `client_ids` but not in prior bronze -> full-pull that client (backstop path), never emit a partial index.
- Gap wider than TRAILING_DAYS (e.g. today's 6-day gap is FINE at 30d; a >30d outage) -> auto-escalate that client to full-pull.

## 3. Gap-backfill (07-01..07-06)

The 06-30 bronze is a clean merge anchor. First M1 run = a trailing window `[2026-06-30, 2026-07-06]` (7 days, single window/client) -> backfills the 6-day gap AND exercises the incremental merge path against a known-good anchor in one shot. If any client fails the merge, escalate that client to full-pull. Verify the merged 07-06 bronze row-count/continuity vs the 06-30 baseline before upload.

## 4. Scope, lane, sequence

- **Lane:** `data/inf/manual_api/pull_inflection_performance_rest.py` is a pull script (manual_api). Edit + deploy is my INF pull lane; I diagnose/design/deploy/verify + own the gap-backfill. CTO arch-gates the design (chain touch).
- **Deploy:** local -> S3 code -> the pull runs on the EC2 runner in the nightly chain (no Lambda/TF). Verify on the scheduled nightly artifact, not an ad-hoc gold run.
- **Sequence to ceiling-revert:** M1 lands + perf genuinely fresh nightly -> coordinate with DS~A's `orion_normalize_as_of` holiday-aware staleness-fix in `convert_performance_to_silver` -> THEN revert `PERF_SILVER_STALENESS_CEILING_DAYS 10->2` (never before perf is genuinely fresh; the 10d ceiling is the runway holding the DEFER honest).

## 5. Milestones + ETA

| Milestone | Content | ETA |
|---|---|---|
| **M1 design** (this doc) | trailing + merge + backstop design; root confirmed | DONE 07-06 |
| **M2 implement + backfill** | add incremental fast-path + `--mode {incremental,full}` (default incremental); prior-bronze merge; weekly-full backstop; run the 06-30->07-06 backfill; verify continuity | ~1 day (pending CTO arch-gate) |
| **M3 deploy + verify + revert-handoff** | deploy to runner; confirm nightly bronze/performance fresh + <600s on the scheduled run; RAVC; hand the ceiling-revert to the DS~A holiday-fix sequence | ~0.5 day after M2, verified on 1 scheduled nightly |

**Gate to start M2:** CTO arch-blessing of the trailing+merge+backstop design (esp. the chain-link splice + the weekly-full cadence). Requesting that GO.
