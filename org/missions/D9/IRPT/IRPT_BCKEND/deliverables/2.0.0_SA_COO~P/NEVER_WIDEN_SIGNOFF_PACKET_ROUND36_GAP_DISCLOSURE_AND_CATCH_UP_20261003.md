# Never-widen sign-off packet -- round 36 deploy: the adapter names a missing trading day, and both holdings producers catch up missed days

Author `2.0.0_SA_COO~P`, 2026-10-03 ~05:2xZ. **Source:** IB-pr-299 (merged @b1fccfb3f5) and IB-pr-300 (merged @598dca08c4), on CTO
RULINGS batch 202 section 2. The producers' listing grant is @483d8d2331 (row S295, disarming W103-S1). **Artifacts:** @e629c381ac.
**Halves owed:** `1.0.0_SA_CTO` and `2.0.0_SA_COO~P`. **Window:** before the Inflection producer's first scheduled fire under this
code, Mon 2026-10-05 14:00Z.

## Why

Row S292: a missed fire left Inflection's 2026-10-01 out of the gold, and the adapter chained 09-30 to 10-02 with no disclosure. The
day itself is landed (row S294). These two changes close the CLASS:
- the adapter never links across a missing trading day silently;
- a missed fire heals on the next one.

## The acts (ONE ledger entry)

| leg | act | resource | before | after |
|---|---|---|---|---|
| D1 | targeted apply, the adapter's code | `module.irpt_performance_adapter.aws_lambda_function.this` (`irpt-performance-adapter`, root `investor-reporting/performance`) | CodeSha256 `/K1eLPuPnwG+...` (S3 `7GwiGHEPjUOS`) | **`8G3gsrajS2virR69EOdaPKSGU5xtuEnLuoHuqpA6sq0=`** (S3 `u_P4LFO_yZ0st0tS5BmHjJDHhb9_nn.K`) |
| D2 | targeted apply, both producers' code and their two role policies | `module.irpt_holdings_performance` and `module.irpt_holdings_performance_inf` `.aws_lambda_function.this`; `aws_iam_role_policy.irpt_holdings_performance` and `_inf` (root `investor-reporting/holdings-performance`) | CodeSha256 `kKgvbKtG...` (S3 `OJ.bVNs_0q`), both | **`0PuFBxdJSbFHNJ9+Z3weyzLvXyZhgZFk2dkGAbIYb/0=`** (S3 `IPBj.bgy462CO8neYf4rAZiaiTja9YVc`), both; each policy gains ONE ListBucket statement |

**Plans, read ~05:1xZ:**
- `performance` root: 0 to add, 1 to change, 0 to destroy. Only `s3_object_version` and `source_code_hash` move.
- `holdings-performance` root: 0 to add, 4 to change, 0 to destroy: the two functions' code and the two role policies.

**Members moved, against the DEPLOYED bytes:**
- adapter: exactly `holdings_gold.py` (70 of 71 members byte-equal);
- producer: exactly `handler.py` (13 of 14 byte-equal).
Each artifact's map hash equals its S3 content-sha256 and its zip's sha256.

## Blast radius, by the code's own rule (measured, not predicted)

**Adapter (`holdings_gold.py`).** The chain, its arithmetic and the figures are unchanged. What changes is what a window SAYS, and
only when a trading day inside it has no partition. The trading days without a partition were measured over each firm's whole gold
with `lib/trading_calendar.py`:
- **49 Financial:** 0 of the trading days 2024-07-09..2026-10-01 (561 partitions). NO 49 Financial window changes.
- **Inflection, gap windows:** 3 trading days in 2024-01-01..2026-10-01 lack a partition: 2026-05-11, 2026-06-30 and 2026-08-10
  (1,614 partitions, 2020-04-27..2026-10-01).
  - A window containing any of them gains a PARTIAL `missing_trading_days` absence naming the days, `value_facts.claim = partial`,
    and the result's `claim = partial`.
  - Its `source_revision` changes because the evidence names the days.
  - The figure is the same number as today: today it silently links over those days.
- **Inflection, long windows:** the Lambda's fallback calendar knows holidays for 2024-2027 only, and Inflection's gold starts in
  2020. A window reaching before 2024-01-01 gains a PARTIAL `trading_calendar_range` absence ("not graded for a missing
  partition"). Its claim stays `measured`, and its figure and digest are otherwise unchanged.
- A window with every trading day present: no new absence, no new key, the same digest (IB-pr-299's tests).

**Producers (`handler.py`).**
- A scheduled fire with no gap computes the same one day as today.
- After a missed fire, the next fire computes every trading day after the newest landed partition through T-1, oldest first, at
  most 5, and stops at the first day the producer cannot compute.
- Each write is a NEW key, and no landed partition is rewritten.
- An explicit `date` event is unchanged.
- Measured now: both firms' newest landed day is 2026-10-01, so Monday's fires compute 2026-10-02 only.

**IAM.** Each producer role gains `s3:ListBucket` on its own bucket, conditioned on `s3:prefix` `irpt/<firm>/gold/holdings_performance_daily/*`.
There is no GetObject, no other table and no other firm. Both roles already PutObject under these same prefixes today, so their
buckets' principal fences already admit them; no fence or exemption is edited.

**Writers of the touched gold prefixes:** one, the producer itself, unchanged.

**Not in this packet:** landing Inflection's three historic gaps, which would MOVE served figures. It is named here as an open
choice for 1.0.0_SA_CTO, never done as a rider.

## Rollback, per key

- **D1:** a targeted apply with the adapter's `s3_object_version` back to `7GwiGHEPjUOSh894mVi3Jn8i9QmzJbxF` (kept; the bucket is
  versioned).
- **D2:** a targeted apply with both functions back to `OJ.bVNs_0qPbc.nFNwkbs5tfaGCOBl65`. For the policies, revert @483d8d2331's
  two statements and apply the two policies.
- Each leg rolls back alone.

## Conditions (ledger legs)

1. **C1:** the plans are exactly D1 and D2 above; the map hashes equal S3; the moved members are exactly `holdings_gold.py` and
   `handler.py`.
2. **D1:**
   - read back CodeSha256 `8G3gsraj` and run a targeted re-plan, which must show No changes;
   - then a local run of the DEPLOYED `holdings_gold.py` (downloaded from the function) over live gold, reading only:
     - a 49 Financial account over a 1Y window: claim `measured`, no new absence;
     - an Inflection account over a window containing 2026-05-11: claim `partial`, naming that day.
3. **D2:**
   - read back both CodeSha256 values and both policies;
   - a targeted re-plan, which must show No changes;
   - one dry-run invoke of each producer WITHOUT `date` (`{"dry_run": true, "source": ...}`): its log plans exactly the one day
     today's rule computes, with no `WARN: gold listing failed`, which proves the listing grant took.
4. **A1:** Monday 2026-10-05's scheduled fires of both producers, read from their logs:
   - each computes 2026-10-02 only;
   - each lands one new key;
   - neither prints a listing WARN;
   - and (ledger A1 of irpt-inf-performance-serving-20261002, as amended) Inflection holds a partition for every trading day
     through the fire's day except the three named historic gaps.

## COO half -- 2.0.0_SA_COO~P

SIGNED, 2026-10-03 ~05:2xZ, on this packet's bytes at the commit that carries it.
- The write set is two functions' code (one member each against deployed) and two role policies (one prefix-scoped ListBucket
  each).
- No figure moves. 49 Financial windows are unchanged, and Inflection windows gain disclosures only (three named gap days; the
  pre-2024 calendar range).
- Every producer write is a new key.
- Each leg rolls back alone.

## CTO half

OWED.
