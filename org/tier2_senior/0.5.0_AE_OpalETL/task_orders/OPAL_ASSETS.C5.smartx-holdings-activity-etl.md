# OPAL_ASSETS.C5 — SmartX holdings-activity-grain ETL into `opal-data-assets/smartx/` (backfill + daily)

<issued_to>0.5.0_AE_OpalETL</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<go>Andrew-direct 2026-07-14 ~04:0xZ: "brief on how to run this for backfill and daily pulls at individual holdings activity grain in our opal-data-assets/smartx/ folder … give it to 0.5.0_AE_OpalETL for implementation now." This is C5 (the SmartX reconstruction) brought forward; SmartX is Opal's own model platform = the OpalETL charter.</go>
<project>OPAL_ASSETS — Grand Consolidation (§4a SmartX reconstruction + §4b population campaign)</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4a/§4b · findings: org/tier1_exec/1.0.0_SA_CTO/deliverables/SMARTX_YALIU_HAR_FINDINGS_AND_DAILY_VALUATION_PLAN_20260714.md · endpoints: docs/architecture/DATA_PLATFORM_D4_smartx_endpoint_sweep.md</prd>

## 0. THE GOAL (Andrew, verbatim intent)
Land SmartX at **individual-holdings-activity grain** in `opal-data-assets/smartx/`, so it **rolls up to
model-summary level** when needed AND powers **model-specific client views in Advisor Intelligence**.
This TO's deliverable is **the design + the ETL ingestion + the writes** (bronze + silver). Gold
(the rollups, the DDB cohort rows, the AdvI serving) is a LATER TO — not this one.

## 1. THE GRAIN + THE BUCKET STRUCTURE
The atomic unit is **(account | model) × holding-symbol × day** — a position and its activity over time.
Everything aggregates UP from there (holding → account → model → platform). Bronze is raw JSON
byte-for-byte; silver is parquet, dedup+dtype only, every vendor column kept (Rule 17). Grammar mirrors
the monolith's `{source}/{scope}/{layer}/{feed}/{date}/`:

```
opal-data-assets/smartx/
  platform/bronze/models_summary/{YYYYMMDD}/summary.json        897 models: stats + per-model performanceStartDate (the lookback FLOOR)
  platform/bronze/access_roster/{YYYYMMDD}/access.json          users/access — 906 models + 452 accounts + each startTrackingDate  (THE ITERATOR)
  platform/bronze/model_allocations/{YYYYMMDD}/{rmid}.json      enterprises/reports/model/{rmid}/allocations — model→accounts + per-account AUM
  model/{rmid}/bronze/holdings/{YYYYMMDD}/holdings.json         reportedmodels/{rmid}/holdings — model composition snapshot (symbol/qty/price/mv/%)
  model/{rmid}/bronze/performance/{YYYYMMDD}/{grouping}.json    models/{id}/performance?grouping=daily|weekly|monthly — flow-adj return series (FULL history per call)
  model/{rmid}/bronze/changerequests/{YYYYMMDD}/history.json    reportedmodels/{rmid}/changerequesthistory — trade/rebalance events (position-moving)
  account/{acctId}/bronze/holdings/{YYYYMMDD}/holdings.json     accounts/{id}/holdings — account position snapshot (symbol/qty/price/multiplier/mv/%)
  account/{acctId}/bronze/activity/{YYYYMMDD}/activity.json     accounts/{id}/activity — FULL 16-mo ledger in ONE unparameterized call (cash/div/fee events, per-symbol, dated)

  {same tree}/silver/{feed}/date=YYYY-MM-DD/data.parquet        parquet, dedup+dtype only, every vendor column preserved
```

## 2. THE ENDPOINT → FEED MAP (grounded on the yaliu HARs; per-feed backfill + daily semantics)
| feed | endpoint | backfill (one-time) | daily | idempotency key |
|---|---|---|---|---|
| models_summary | `performance…/models/summary?platform=` | 1 bulk call | 1/day snapshot | (model, run_date) |
| access_roster | `api/3.1/users/access` | 1 call | 1/day (the iterator; re-read to pick up new models/accounts) | (relationship, run_date) |
| model_allocations | `api/3.1/enterprises/reports/model/{rmid}/allocations` | 1/model | 1/day/model | (rmid, accountId, run_date) |
| model_holdings | `reportedmodels/{rmid}/holdings` | **snapshot-only** — cannot backfill history; **accrue daily from now** | 1/day/model | (rmid, symbol, run_date) |
| model_performance | `models/{id}/performance?grouping=daily` | **full series to the model's `performanceStartDate`** (one call returns full history) | 1/day delta, dedup on period | (id, period_date) |
| changerequests | `reportedmodels/{rmid}/changerequesthistory` | **full trade log** (one call) | 1/day delta | (rmid, tradeTimestamp, ticker, activity) |
| account_holdings | `accounts/{id}/holdings` | **snapshot-only** — accrue daily from now | 1/day/account | (acctId, symbol, run_date) |
| account_activity | `accounts/{id}/activity` | **FULL 16-mo ledger, ONE unparameterized GET** (CONFIRMED: the CSV date-range is client-side; the endpoint has no date params, returns everything) | 1/day delta, dedup on event | (acctId, activityTimestamp, symbol, activity, amount) |

**THE KEY BACKFILL MECHANICS:** the append-only feeds (`activity`, `performance`, `changerequests`)
return their **complete history in a single call** — so "backfill" for them is one pull each, then
daily dedup. The snapshot feeds (`holdings`, `model_holdings`, `allocations`) have **no history
endpoint** — their backfill IS "start the daily snapshot now"; historical per-holding value is a GOLD
reconstruction (holdings anchor + changerequests + activity), not a pull. **The one open probe** (a
holdings screen with an as-of date change) would confirm whether `holdings?asOf=` exists — if it does,
holdings backfill becomes a dated pull; UNTIL confirmed, treat holdings as accrue-forward.

## 3. THE ETL MECHANISM
**Auth (reuse, do not rebuild) — AND THE CREDENTIAL/COOKIE BUNDLE LIVES IN SECRETS MANAGER (Andrew-direct
2026-07-14, verbatim: "we will need that cookie or authentication mechanism bundled in aws secrets
manager for env use or something like that in the associated retrieval devices"):** the parked-JWT
pattern already exists — `smartx-jwt-refresher` (OIDC ROPC → Secrets Manager `smartx/jwt/current`). One
JWT spans `api.`/`performance.`/`identity.` (D4 §2). **This TO makes the full auth bundle a
Secrets-Manager-resident artifact that every retrieval device (the pull Lambda, and any future channel
EC2) reads from env at runtime — NEVER hardcoded, never in repo, never in an image.** See §3a. ⚠
**Credential grant note (for CTO/Andrew, not for you to resolve):** the HARs were captured on `yaliu`
(Yang's personal, higher-grant login); the pipeline's `opal7` is a narrower manager-portal grant.
**Build against the JWT/secret abstraction with the credential CONFIGURABLE** — do not hardcode either.
Flag in your RAVC which grant your build was exercised against; the production-credential decision
(request a dedicated service login at the yaliu grant) is Andrew's.

### §3a. THE AUTH-BUNDLE SECRETS ARCHITECTURE (Andrew-direct — required, build it this way)
The SmartX auth is not a single static token — it is a bundle (ROPC username/password → minted JWT +
refresh token, ~2h JWT lifetime; plus, if the higher-grant `smartx.smartxadvisory.com` app path is
adopted, potentially a session cookie). **All of it lives in Secrets Manager; the retrieval devices read
it from env, mint/refresh as needed, and write the refreshed token back.** Concretely:
- **`smartx/credentials/{username,password}`** (existing) — the ROPC seed. Read by the refresher ONLY.
- **`smartx/jwt/current`** (existing) — the minted access token + refresh_token + expires_at, refreshed
  daily by `smartx-jwt-refresher`. **Migrate its S3 co-park OFF `opal-data-bd`** (the firm-boundary
  violation, PRD ruling 10 / D4 §9.5) — the S3 mirror retires; Secrets Manager is the single source.
- **`smartx/cookie/current`** (NEW, only if the app-path/cookie auth is used) — any session cookie/bundle
  the higher-grant path needs, same read-from-env + refresh-write-back lifecycle as the JWT. Build the
  slot even if unused today (empty/absent = the REST path suffices), so adopting the app path later is a
  config change, not a re-architecture.
- **Retrieval-device contract:** the pull Lambda (and any future SmartX channel EC2) gets an IAM grant
  to `GetSecretValue` on EXACTLY these `smartx/*` ARNs (enumerated, never `smartx/*` wildcard-if-avoidable
  — pin the specific secret names), loads them into env at cold-start, and NEVER logs them. A refresh
  writes back via `PutSecretValue` scoped to the refreshable secrets only. Verify the grant per Rule 22a
  (live `simulate-principal-policy` on the exact secret ARNs, positive control separate).
- **Rotation-safe:** an expired/rotated JWT triggers a re-mint from the ROPC seed, not a hard failure —
  the failure mode of a stale token is a loud re-auth, never a silent 401 read as "no data" (the
  0824-outage class). Confirm the SNS/alert on repeated auth failure reaches a CONFIRMED subscription.

**Rate limit (hard):** ≤17/min per credential (D4 §8, shared credential ~20/min ceiling). With ~906
models + ~452 accounts the full backfill is ~2,700 calls ≈ **~2.6 hours** — this is **NOT a 900s Lambda
job.** Backfill runs as a **bounded, resumable one-time process** (skip-if-landed off S3, re-invokable
to convergence — the SAME shape C2 used, and heed the C2 lesson below). Daily is the delta and DOES fit
a Lambda (existing `smartx-rest-pull` pattern, extended).

**Idempotency + absent-day discipline (§0.3 hyperrobust):** skip-if-landed keyed on the table's
idempotency key; `--force` rewrites; an absent day is ABSENT (no roll-forward, no zeros). Every writer
**verifies its landed object** (`exit 0` = bytes-in-S3, head-object confirmed).

**⚠ THE C2 CORRUPTION LESSON — BAKE THE DISTINCT-LANDING GUARD IN FROM PASS ONE (CTO doctrine, this
session):** the C2 mirror's conservation guard counted copy_object CALLS, not DISTINCT LANDED KEYS, and
passed a last-writer-wins key collision reading clean. **Your write-path conservation MUST assert on
DISTINCT LANDED KEYS / set-identity, never a write or call tally** — enumerated-unique == landed-distinct
== source count, RAISE on shortfall. And your key mapping must **preserve every distinguishing segment**
(scope + feed + date + symbol) — a flat key that collapses two feeds onto one path is the exact C2 bug.
This is a required design property, exercised (feed the guard a synthetic collision, prove it RAISES),
not asserted.

## 4. SILVER (Rule 17 strict)
Parquet per feed, dedup + dtype standardization ONLY. **Preserve the vendor's bugs AS DELIVERED** —
`holdings.assetType` is uniformly-wrong "equity" and `industry`="Unknown" (D4 §8): silver keeps them
verbatim; classification is a GOLD join to Opal ETFClassifier, never a silver fix (the completeness
law — storage never Opal-filtered). `performance` ignores date params and returns full history each
call, so silver dedups on the period key. Event feeds (`activity`, `changerequests`) dedup on their
event key. Silver is event-driven off bronze `ObjectCreated` on the monolith (the C6 registry pattern);
no cron downstream of the pull.

## 5. FENCES + SCOPE
IN scope (yours): the pull(s) + bronze writes + silver conversion for the 8 feeds above, backfill +
daily, into `opal-data-assets/smartx/`. OUT of scope (later TOs): gold rollups, the DDB cohort row, the
Advisor-Intelligence serving wiring, and retiring the legacy `smartx-exporter` EC2 scrape (sequenced
separately). SmartX vendor egress is Andrew-lifted (recurring, standing) — no per-use word needed.
New-territory: everything you create is NEW (new bucket prefixes, new schedule, new/extended Lambda) —
do not modify any existing SmartX resource to get there; the legacy `opal-data-smartx-v2` stores and the
DDB `opal-data-smartx` are UNTOUCHED (C12 inventories them). The 1,386 GUI-era `exports/` objects
(§4b P-1) mirror in channel-labeled `gui-era` as a separate step — flag it, do not fold it into the REST
pull. NOT touched: INF hold, never-summed, 17a.

## <compiler_tools_mandate>
Phase 1: `comp-iam service` on the pull Lambda for the SmartX + monolith-write grants (necessary NOT
sufficient); live `simulate-principal-policy` per 22a against the exact `opal-data-assets/smartx/*` ARNs
(one --resource-arns/call, positive control separate — comp-iam FAILS GREEN on a new prefix). Every .py
`from __future__ import annotations` (Rule 15). Phase 2: `.tools/commit-gate.sh`. Phase 3: head-object /
listing evidence per feed + the distinct-landing guard exercised.
</compiler_tools_mandate>

## <cross_domain_coordination>
Reuses `smartx-jwt-refresher` (do not duplicate the JWT mint). Coordinate the monolith-write IAM with
0.7.0 (C1 role owner) — a NEW scoped `smartx/*` write grant, never-widen. Nothing writes
`opal-data-inf/gold/meta/pipeline-complete.json`. Your ETF-parity window (day-2 22:00Z) OUTRANKS this —
this is fill for the idle hours, the laptop stays on, `_cloudprobe/` untouched.
</cross_domain_coordination>

## <acceptance_criteria>
1. DESIGN FIRST (Andrew: "the first step is sorting out the design"): a short design note confirming the
   8-feed map, the grain, the backfill-vs-daily semantics per feed, and the credential/rate/resumability
   choices — routed to CTO for a design-gate BEFORE the pull runs at scale. (A wrong key mapping is
   permanent in bronze; get the design ruled before writing bytes, per the C2 lesson.)
2. Backfill: the 3 append-only feeds land their full history (activity to its ledger floor, performance
   to each model's `performanceStartDate`, changerequests full) — denominators printed per feed, run-time
   enumerated, never a hardcoded count.
3. Daily: a delta run lands only new events/snapshots; a re-run lands 0 (idempotency exercised).
4. The distinct-landing conservation guard is EXERCISED (RAISES on a synthetic collision) — mutant-tested.
5. Silver parquet exists per feed with every vendor column (column-count parity vs raw, both denominators),
   vendor bugs preserved.
6. **AUTH BUNDLE IN SECRETS MANAGER (Andrew-direct, §3a):** the credential/JWT/refresh (+cookie slot)
   bundle is Secrets-Manager-resident; every retrieval device reads it from env, never hardcoded/logged/
   in-repo; the refresher writes back; the `opal-data-bd` JWT S3 co-park is retired; the GetSecretValue/
   PutSecretValue grants are pinned to exact `smartx/*` ARNs and 22a-verified. Exercised: an expired token
   re-mints loudly, never a silent 401.
7. `comp-validate` before signaling any consumer. Session log + Compiler Tools section; RAVC evidence
   to COO (progress) and CTO (the design gate + any architecture fork).

---

## V2-4 ADDENDUM (2026-07-14 ~06:0xZ, COO per V2 PRD @ 53ba45c5f — this TO IS V2-4; PRD §V2-4 governs)

**CREDENTIAL STATE, CORRECTED (your own 05:49Z correction is the governing record):** the 906 at
yang-shared are SmartX MARKETPLACE view-only entitlements; NEITHER credential suffices alone
(opal7 = model-tier authority, fullAccess all 11 Opal models, 0 accounts; yang-shared = account-tier
authority, 452 accounts, view-only/ABSENT on 4 of Opal's own models). **ANDREW-OPEN:** (a) dual-credential
per-tier now vs (b) wait on the dedicated SmartX service credential — recommendation (a) now + (b) in
parallel. Do not wire either until his word.

**CTO-RULED REGARDLESS (ratifying your encoding):** the model iterator filters
`permissionName == "fullAccess"` — never the raw entitlement list — and RAISES when the enumerated
Opal-model count misses the expected census, so an under-granted roster fails LOUD instead of quietly
under-covering.

**HARD GATE ON THE ACCOUNT TIER:** no account backfill until the 452-vs-~5,800 (D4) census check closes —
the account tier may itself be incomplete; that check is its own deliverable, run + reported before any
account-grain pull.

**IAM changes at graduation:** any grant change rides 0.7.0 never-widen review -> CTO apply gate -> 22a
on the exact new ARN. Bundle-secret support stays defaults-OFF until Andrew's credential word.
</acceptance_criteria>
