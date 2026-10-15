# NEVER-WIDEN PAIR (b), ADDENDUM 1 -- IRPT_BCKEND: the Orion Scope account feed

**Status: DESIGN. The COO half is a separate file bound to this file's blob; the CTO half is not signed.** Nothing here is built, pulled, deployed, written to AWS, invoked, signed or sent; no Orion request is made by this file.

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~16:0xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO round-118 analysis ADDENDUM 1 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_B-IN_ROUND_118_20261015.md`, msg 8411) and the rulings of rounds 119, 120 and 121 that bear on the feed. It amends the Orion pairs packet V3 (`deliverables/2.0.0_SA_COO~P2/ORION_RECUT_PAIRS_PACKET_V3.md`) and changes no other line of it. The feed was part of the voided IB-pr-556 (the CTO half voided at 06:12Z); this addendum replaces that text.

## 1. What the feed is

A new pull step of the Inflection gold chain (the producer that runs today at about 11:32Z; pair (b) keeps that time, V3 section 2): one Orion Scope call per household with the Account grouping, writing account-level daily returns to the feed's OWN bronze and silver prefixes. It is not a third pair and moves no existing step, trigger or schedule.

## 2. The rules the build carries (each from a CTO ruling)

1. **One call per household, paced, no retry, the INNER scope body.** The request is the body `orion_selected.requests_for(...)["scope"]` builds in the serve path (entity household, `entityIds` one household, grouping Account, the daily returns series); the POST body is the inner scope, never the wrapper (round 117: the wrapper drew HTTP 400). Pacing by the estate's `AdaptiveRateLimiter`; a call that fails is recorded and not retried in the run.
2. **`calcGrossOfFees` is false on every request; `fee_basis` is recorded per call as `NET`** with the note "calcGrossOfFees false; tied on 1 household, 2 fee-bearing accounts, Q3 2026" (round 119 ruling 1). The basis cannot drift by request.
3. **The coverage rule, inside the feed (round 118 ruling 1).** Each account the household holds on a day either carries Orion's return for that day, or a row marked `ABSENT` with its reason class. **Never a zero, never an Opal-computed fill.** The reason classes: `NO_GROUP` (the account has no Account group in the response); `GROUP_NO_SERIES` (a group with no return or series; its cause `NOT_DETERMINED`); `NO_START_DATE_AT_SOURCE` (the roster `accounts_v2` shows a null `accountStartDate` for the account, derived by joining the roster the pull already lands, with no extra vendor call), with its claim carried per account: `measured` only on an account whose absence a probe or the feed's own call has observed (2 accounts at the time of round 121), `inferred (pattern measured on 2 households)` on the other null-start accounts, and an account later observed missing by the feed's own call is promoted to measured by that call (round 121 erratum). `NO_MODEL_AT_SOURCE` is withdrawn (round 121 ruling 2).
4. **"Each account the household holds on a day"** is the roster's household membership (`accounts_v2`) intersected with the accounts holding positions on that day in the Inflection positions silver; the build states both sources and the day it reads.
5. **The one-account limit in `orion_account_mapping.py` is lifted in the same release** (its own small cell: the `members != 1` refusal removed, a household-members helper added, its test flipped). Each account is attributed to itself; no household figure is built from the feed's account rows (V1 CTO half condition 5, carried).
6. **Writes only its own prefixes**, both built by `lib/opal_naming.py address()` for source `orion`, scope `inflection`, tiers bronze and silver, a new table name (`scope_account_returns`), dated partitions. No registry row is needed for a new table name (the agent read of `address()`); a builder REFUSAL is a missing registry row to add, never a typed address. The bronze object is a `.json.gz` (NOT `.jsonl.gz`: the silver-orion S3 notification fires on `orion/inflection/bronze/*.jsonl.gz`, so a different suffix cannot trigger it; the build proves the name).

## 3. The write set, and its disjointness from pair (a)

| writer | writes | does not write |
|---|---|---|
| the feed step (new, in the chain's pull stage) | `orion/inflection/bronze/scope_account_returns/date=<day>/...json.gz`; `orion/inflection/silver/scope_account_returns/date=<day>/data.parquet` | any existing bronze or silver key, the 33 backfill keys of pair (a), any gold key, any schedule, IAM principal or Terraform resource |

Pair (a) writes 33 flat bronze keys of the positions, transactions and performance feeds; the feed writes a prefix that holds none of them. No byte of the backfill depends on the feed and none of the feed on the backfill (the CTO's reading, addendum 1).

## 4. The change set at the apply (not now)

1. The feed script as an S3 code object beside the chain's other pull scripts (`code/gold`), uploaded before the chain runs (the chain syncs the code directories once at start).
2. One catalog row `INF_API_PULL_SCOPE_ACCTS|pull_inflection_scope_account_returns.py|--upload` in the chain's dispatch script and its entry in `CHAIN_PULL`, `CHAIN_INCREMENTAL` and the full chain, as a TOLERATED pull (a pull step in the dispatch is bounded by a timeout and its failure does not stop the chain). The dispatch script exists as an S3 object (row W404-S4: the repository copy's equality with the live object is unread); the apply order reads the live object's hash and refuses a difference, and edits it by exactly the one row and its three chain entries.
3. The lifted account mapping ships with the next release of the performance function; it is a separate cell and a separate apply.

## 5. Blast radius, rollback, stop rule

- **Writes:** the feed's two prefixes only, new keys, read ABSENT first. **Reads:** the Orion API (one call per household per run) and the roster and positions silver. **Served values changed: none** (nothing reads the feed until the B-IN adapter cell is cut). The chain's other steps, order and time are unchanged; a tolerated failure of the new step cannot stop the chain.
- **Requests (an estimate, not measured):** one per household per run; the household count is read at the apply from the roster; the run's real count comes from the feed's own log. The apply order states the bound.
- **Rollback, per key:** the new keys are removed (the bucket is versioned; a delete is Andrew's act) and the catalog row and chain entries are reverted from the saved copy of the dispatch object; no other key is touched.
- **Stop rule:** stop on a call whose body is not the inner scope; on any request that is not `calcGrossOfFees` false; on a key not read ABSENT first; on a zero written for a missing account; on any need to edit an existing step, schedule, IAM or a key outside the feed's prefixes; on a 429 or throttle response persisting after the limiter's own retries.

## 6. What this addendum does not cover

The B-IN adapter that reads the feed (`~I2`'s cell, cut when the feed lands its first bronze and silver); the reason class beyond the four above; fixing the null start dates at the source (Andrew's act, a partner-firm request); the 117 dimension accounts not in the active roster; the IAM of the chain runner for the Scope secret (the apply order reads it; a missing grant is a stop, not a rider); the serve path's use of the lifted mapping.

-- 2.0.0_SA_COO~P2
