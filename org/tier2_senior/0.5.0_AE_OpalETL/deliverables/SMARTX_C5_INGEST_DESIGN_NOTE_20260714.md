# OPAL_ASSETS.C5 — SmartX holdings-activity ETL: DESIGN NOTE (for the CTO design gate)

**Author:** 0.5.0_AE_OpalETL · **Date:** 2026-07-14 · **For:** 1.0.0_SA_CTO (design gate) → then the build.
**Status:** DESIGN — routed to CTO for the gate. **NO bronze bytes, no at-scale pull, until this is ruled.**
**Grounding (Rule 22):** CTO's `SMARTX_YALIU_HAR_FINDINGS_AND_DAILY_VALUATION_PLAN_20260714.md` (yaliu HARs #1/#2/#3)
+ `DATA_PLATFORM_D4_smartx_endpoint_sweep.md` (opal7 baseline, FINAL/CVO-PASS) + the C5 TO (9c7f234c0).
Every endpoint semantic below cites one of those; nothing here is invented.

> **Why this note exists before any code:** a wrong key mapping is PERMANENT in bronze (17a: bronze is never
> rewritten in place). The C2 mirror shipped a key mapping un-gated and its first mirrored data is corrupt.
> This note exists so the key grammar is RULED before a byte lands, not discovered after. The decisions that
> are genuinely CTO's to make are collected in §7 — I have not pre-decided them.

---

## 1. THE GRAIN + WHAT ROLLS UP FROM IT

Atomic unit: **(account | model) × holding-symbol × day** — a position/flow and its movement over time.
Everything aggregates UP: holding → account → model → platform. This TO delivers **bronze + silver only**;
gold (daily-valuation reconstruction, DDB cohort rows, AdvI serving) is a later TO and is out of scope.

The higher-granularity story, per CTO's findings, is honest about one limit:
- **Model & account-equity layers are a real upgrade** on yaliu (897 models w/ vendor-stated `performanceStartDate`
  floors; account daily equity via `nonzerosleeve.closingEquity` + `asOfTimestamp`; 906-model return access).
- **Per-holding daily HISTORY is NOT a single pull.** Holdings are snapshot-only; `?asOf` was never exercised
  on holdings even in HAR#2 (findings §2b). So per-holding daily value is a GOLD reconstruction
  (holdings anchor + `changerequesthistory` trades + `activity` cash flows + `performance` series), NOT a silver pull.
  **This note designs the INPUTS to that reconstruction; it does not attempt the reconstruction.**

---

## 2. THE 8-FEED MAP (grounded; per-feed backfill vs daily)

| # | feed | endpoint (host) | id space | backfill | daily | idempotency key | source |
|---|---|---|---|---|---|---|---|
| 1 | models_summary | `performance…/models/summary?platform=` | — | 1 bulk call (897 models) | 1/day snapshot | (model, run_date) | HAR#1 §1 |
| 2 | access_roster | `api/3.1/users/access` | — | 1 call | 1/day (THE ITERATOR) | (relationship, run_date) | HAR#1 §1 |
| 3 | model_allocations | `enterprises/reports/model/{rmid}/allocations` | reportedModelId | 1/model | 1/day/model | (rmid, accountId, run_date) | HAR#2 §2b |
| 4 | model_holdings | `reportedmodels/{rmid}/holdings` | reportedModelId | **snapshot-only → accrue fwd** | 1/day/model | (rmid, symbol, run_date) | D4 §3, §8.4 |
| 5 | model_performance | `models/{id}/performance?grouping=daily` | **modelId** | **full series to `performanceStartDate`** (1 call) | 1/day, dedup on period | (id, period_date) | D4 §3, §8.5 |
| 6 | changerequests | `reportedmodels/{rmid}/changerequesthistory` | reportedModelId | **full trade log** (1 call) | 1/day delta | (rmid, tradeTimestamp, ticker, activity) | D4 §3 |
| 7 | account_holdings | `accounts/{id}/holdings` | accountId | **snapshot-only → accrue fwd** | 1/day/account | (acctId, symbol, run_date) | HAR#2 §2b |
| 8 | account_activity | `accounts/{id}/activity` | accountId | **FULL 16-mo ledger, ONE unparameterized GET** | 1/day delta | (acctId, activityTimestamp, symbol, activity, amount) | HAR#2/#3 §2b |

**Two structural facts that drive the whole design:**

**(A) THE APPEND-ONLY vs SNAPSHOT split is the backfill design.**
- Append-only (feeds 5, 6, 8) return their COMPLETE history in a single unparameterized call
  (`performance` ignores date params — D4 bug 5; `activity` has no date params, the CSV range is client-side —
  HAR#3 §2b). So "backfill" for these is **one pull each, then daily dedup on the event/period key**.
- Snapshot (feeds 1, 3, 4, 7) have **no history endpoint**. Their "backfill" IS "start the daily snapshot now";
  historical per-holding value is the GOLD reconstruction, not a pull. Absent days ABSENT — no roll-forward, no zeros.

**(B) THE MODEL TREE MIXES TWO ID SPACES — this is the key-mapping hazard (D4 §4).**
`modelId` and `reportedModelId` are **two different UUID spaces**. Holdings, changerequests, and allocations are
fetched by **reportedModelId**; performance is fetched by **modelId**. Calling `reportedmodels/{modelId}/…` → HTTP 400.
The pull MUST chain `models/{modelId}` → read `.data.reportedModelId` → use that for the reportedmodels/* feeds.
**Design decision §7-Q1 rests entirely on this.**

**(C) CREDENTIAL-GRANT DEPENDENCY PER FEED (CTO gate expectation #2 — so the credential fork does not silently kill a feed).**
D4's surface is the **opal7 manager-grant** (+ the 2026-06-24 sweep); CTO's yaliu findings are the **newer, higher-grant**
surface. Where they differ, yaliu is the fresher vintage — but a feed that exists ONLY at yaliu-grant is a **dependency on
Andrew's credential decision** (§7-Q4). Marking each:

| feed | grant basis | at opal7 (narrower) |
|---|---|---|
| 4 model_holdings, 5 model_performance, 6 changerequests | **opal7-D4-CONFIRMED** | works — these are D4 §3 live-200 on opal7. SAFE under either credential. |
| 2 access_roster (endpoint) | both | endpoint exists at opal7; the **906/452 row scope is yaliu** — opal7 returns its narrower roster. |
| 1 models_summary (897-model scope) | **yaliu-observed** | opal7 saw ~11 models via other endpoints; the 897-model `models/summary` surface is yaliu. Narrower/absent at opal7. |
| 3 model_allocations (3,182 accts) | **yaliu-observed** (HAR#2) | D4's opal7 had `enterprises/allocations?modelid=` (a different shape); this rollup is yaliu. |
| 7 account_holdings, 8 account_activity | **yaliu-observed** | ⚠ opal7's `/accounts` was **EMPTY** in D4, "now returns content" only in the 06-24 sweep. The 452-account holdings+activity grain is a **yaliu-grant dependency** — at opal7 these feeds may return empty or a narrow account set. |

**→ The ACCOUNT-GRAIN feeds (7, 8) and the WIDE model surface (1, 3) depend on the yaliu-grade credential.** If Andrew
resolves the fork to opal7 (§7-Q4), those feeds narrow or empty — NOT a pull bug, a grant boundary. The pull builds against
the credential abstraction and the guard's run-time-enumerated denominator absorbs a narrower roster without false-alarming;
but the *design* names this dependency so a thin account feed is read as "opal7 grant," never as "the pull broke."

---

## 3. THE KEY-MAPPING GRAMMAR (the thing the gate must rule)

Monolith grammar is `{source}/{scope}/{layer}/{feed}/{YYYYMMDD}/…` (PRD ruling 9/15, as C4 landed). For SmartX,
`source = smartx`. The proposed tree (reconciling the TO §1 and the findings §3, which differ slightly):

```
smartx/platform/bronze/models_summary/{YYYYMMDD}/summary.json
smartx/platform/bronze/access_roster/{YYYYMMDD}/access.json
smartx/model/{rmid}/bronze/model_allocations/{YYYYMMDD}/allocations.json
smartx/model/{rmid}/bronze/holdings/{YYYYMMDD}/holdings.json
smartx/model/{rmid}/bronze/performance/{YYYYMMDD}/{grouping}.json
smartx/model/{rmid}/bronze/changerequests/{YYYYMMDD}/history.json
smartx/account/{acctId}/bronze/holdings/{YYYYMMDD}/holdings.json
smartx/account/{acctId}/bronze/activity/{YYYYMMDD}/activity.json
```

**THE CRITICAL INVARIANT (and the C2 collision risk stated concretely):**
`{rmid}` in EVERY `smartx/model/…` path is the **reportedModelId**, for ALL FOUR model feeds — INCLUDING
performance, which is *fetched* by modelId. So the pull resolves modelId→reportedModelId and files performance
under the model's reportedModelId. **If performance is ever filed under its modelId, that one model acquires TWO
path roots** — the exact "two feeds collapse / one entity splits" class the distinct-landing guard exists to catch.
modelId appears ONLY as (a) a fetch parameter and (b) a recorded field inside the JSON — **never in a path segment.**
→ **§7-Q1 asks CTO to ratify: path key = reportedModelId for the whole model tree.**

**Note the scope segment is two path components (`model/{rmid}`, `account/{acctId}`)** — deeper than C4's single-token
scope (`trueshares`, `filepoint`). This is a legitimate grammar question for the gate (§7-Q2): is a per-entity
2-segment scope in-grammar, or does CTO want `{entity_type}_{id}` as one token, or the id as a `{feed}`-level segment?

---

## 4. THE DISTINCT-LANDING GUARD (set-identity, baked in pass one — EXERCISED)

Per the TO §3 C2 lesson and CTO's four-things #3. The guard asserts on **DISTINCT LANDED KEYS**, never a call/write tally.

```
For each feed, per run:
  enumerated_targets  = the set of keys the pull INTENDS to write (built from the run-time roster, not a constant)
  landed_keys         = ListObjectsV2 over the feed prefix for {run_date}, distinct keys actually present (ETag+Size non-empty)
  ASSERT  set(landed_keys) == set(enumerated_targets)      # set identity, both directions
  RAISE   on shortfall (missing) OR surplus (an unexpected key = a mapping collided or a stray write)
```

- **Every distinguishing segment preserved:** scope + entity-id + feed + date (+ symbol at silver row grain). A flat
  key that drops any segment can collapse two entities onto one path — that IS the C2 bug.
- **Denominators enumerated AT RUN TIME (PRD 13b), never hardcoded** — the roster is 906 models / 452 accounts TODAY;
  the guard reads the count from `users/access`, so a roster that grows does not silently under-cover.
- **EXERCISED, mutant-tested:** feed the guard a synthetic collision (two enumerated targets mapping to one key, and a
  surplus key) and prove it RAISES on both. A guard never made to fire is indistinguishable from no guard.
- **The verdict is on LANDED BYTES, not the copy loop** — set-identity over a fresh ListObjectsV2, the sound kind
  0.6.2 used, not the call-count the C2 mirror used.

---

## 5. THE AUTH BUNDLE (Secrets Manager — Andrew-direct §3a, REQUIRED)

Reuse the existing `smartx-jwt-refresher` (OIDC ROPC → Secrets Manager); do NOT rebuild the JWT mint. The bundle:

| secret | state | contents | who reads / writes |
|---|---|---|---|
| `smartx/credentials/{username,password}` | existing | ROPC seed | refresher reads ONLY |
| `smartx/jwt/current` | existing | access token + refresh_token + expires_at | refresher writes daily; retrieval devices read |
| `smartx/cookie/current` | **NEW slot, may be empty** | session cookie for the higher-grant app path, if adopted | same read-env / refresh-write-back lifecycle |

- **Retrieve from env at cold-start, mint/refresh as needed, write refreshed token back** (`PutSecretValue` scoped
  to the refreshable secrets only). **Never hardcoded, never logged, never in repo/image.**
- **RETIRE the `opal-data-bd` JWT S3 co-park** (`s3://opal-data-bd/smartx/jwt/current.json`, D4 §5) — it is the
  firm-boundary violation (PRD ruling 10 / D4 §9.5). Secrets Manager becomes the single source; the S3 mirror retires.
- **IAM (22a-verified on the live primitive):** `GetSecretValue` pinned to the EXACT `smartx/*` secret ARNs (enumerated,
  never a `smartx/*` wildcard if avoidable). One `--resource-arns` per `simulate-principal-policy` call, positive
  control separate (comp-iam FAILS GREEN on a new secret ARN).
- **Rotation-safe / fail-LOUD:** an expired/rotated JWT triggers a re-mint from the ROPC seed — NEVER a silent 401
  read as "no data" (the 0824-outage class). Confirm the auth-failure SNS alert reaches a CONFIRMED subscription.

---

## 6. THE ETL MECHANISM (rate, resumability, silver)

- **Rate ≤17/min per credential** (D4 §8.7; shared-credential ~20/min ceiling). Backfill ≈ 906 models × (holdings +
  performance + changerequests + allocations) + 452 accounts × (holdings + activity) ≈ **~2,700 calls ≈ ~2.6h**.
  **NOT a 900s Lambda.** Backfill = a **bounded, resumable, one-time process**: skip-if-landed off S3, re-invokable to
  convergence (the C2 shape, minus the C2 guard bug). **Daily delta fits a Lambda** — the existing `smartx-rest-pull`
  pattern extended.
- **Idempotency + absent-day discipline:** skip-if-landed keyed on the feed's idempotency key; `--force` rewrites; an
  absent day is ABSENT (no roll-forward). Every writer **verifies its landed object** (head-object/listing = bytes-in-S3),
  never rc=0 (the rc-through-a-pipe class I already banked this session).
- **Silver (Rule 17 strict):** parquet per feed, dedup + dtype ONLY, every vendor column preserved. **Vendor bugs kept
  AS DELIVERED** — `holdings.assetType` uniformly-wrong "equity", `industry`="Unknown" (D4 §8.3): silver keeps them
  verbatim; classification is a GOLD join to Opal ETFClassifier (the completeness law — storage never Opal-filtered).
  `performance` returns full history each call → dedup on period key. Event feeds dedup on their event key. **Silver is
  event-driven off bronze `ObjectCreated`** (the C6 registry pattern) — no cron downstream of the pull.
- **Semantic caveat to preserve in silver, not "fix":** `account_activity.ledger` is **CASH events (deposit/withdrawal/
  dividend/fee), NOT buy/sell trades** (HAR#2 §2b) — position-quantity moves live in `changerequests`. Silver keeps them
  as the two distinct feeds they are; joining them is gold's job.

---

## 7. DECISIONS FOR THE GATE (these are CTO's to rule — I have NOT pre-decided them)

**Q1 — Model tree path key = reportedModelId, for all four model feeds incl. performance?** (§3). My recommendation: YES —
performance is fetched by modelId but filed under the model's reportedModelId, with modelId only a fetch param + recorded
field. This is the single most permanent decision; a wrong choice splits one model into two path roots.

**Q2 — Is a 2-segment per-entity scope (`model/{rmid}`, `account/{acctId}`) in-grammar,** or do you want a single-token
scope (`{entity}_{id}`) or the id as a feed-level segment? (§3). C4's scope was one token; SmartX's per-entity explosion
is genuinely different and I want the grammar ruled, not assumed.

**Q3 — The holdings `?asOf=` probe (findings §4/§2b):** the ONE unconfirmed thing that would turn per-holding history from
a gold reconstruction into a direct dated pull. Options: (a) I treat holdings as accrue-forward now and we never revisit;
(b) I fold a single targeted probe into the backfill's first run and, IF `?asOf` honors a date, revise the holdings backfill
before it accrues. Recommend (b) — it is one call and it is the difference between a reconstruction and a pull. Your call
on whether it is in-scope for C5 or a separate probe TO.

**Q4 — Credential grant:** build against the JWT/secret abstraction with the credential CONFIGURABLE (I will exercise
against whichever grant the parked JWT currently holds and FLAG which one in RAVC). The production-credential decision
(request a dedicated yaliu-grade service login vs ride opal7's narrower manager grant) is **Andrew's**, per the TO — not
resolved here, only surfaced.

**Q5 — The 1,386 GUI-era `exports/` objects** (`opal-data-smartx-v2/exports/`, §4b P-1): the TO says mirror them
channel-labeled `gui-era` as a SEPARATE step. Confirm they are OUT of this design's scope (I will flag but not fold).

**Q6 — Backfill host:** a bounded resumable process at ~2.6h is not a Lambda. Options: a local-driven resumable script
(S3-checkpointed) for the ONE-TIME backfill, daily delta on the extended `smartx-rest-pull` Lambda. Confirm the one-time
backfill may run as an operator-driven resumable process (it is not a scheduled runner, so it is not a NEVER-ad-hoc-gold
concern — it is a bronze pull, not a gold re-derive — but I want that explicit).

---

## 8. SCOPE FENCES (what this design does NOT touch)

- **Bronze + silver ONLY.** Gold rollups, the DDB cohort row, AdvI serving, and legacy `smartx-exporter` scrape retirement
  are LATER TOs.
- **New-territory:** everything created is NEW (new prefixes, new/extended Lambda, new schedule). Legacy
  `opal-data-smartx-v2` stores + the DDB `opal-data-smartx` are UNTOUCHED (C12 inventories them).
- **INF hold stands, separate from the 49F lift:** nothing writes `opal-data-inf/gold/meta/pipeline-complete.json`.
- **Never-summed, 17a, no-ad-hoc-gold-runs:** all stand.
- **`_cloudprobe/` untouched, THE LAPTOP STAYS ON:** ETF parity day-2 (22:00Z) OUTRANKS this; C5 is idle-hours fill and I
  drop it for the gate run.
- **Basis-label discipline (findings §4a):** any AUM figure this pipeline ever emits carries its basis — SmartX
  `models/summary` stats and `nonzerosleeve` equity are their OWN basis, declared on every row. (Emission is gold/later —
  noted here so the silver schema keeps the fields that let gold declare it.)

---

## 9. WHAT I NEED FROM THE GATE

Rule Q1–Q6. On a GO I build in this order: (1) auth bundle + IAM (22a-verified) → (2) the distinct-landing guard, exercised
first → (3) the append-only backfill (one pull each: activity, performance, changerequests) → (4) the snapshot daily accrual
→ (5) silver per feed. Progress/RAVC to COO; this design gate + any architecture fork to you.
**No bronze byte lands before the Q1/Q2 key grammar is ruled.**
