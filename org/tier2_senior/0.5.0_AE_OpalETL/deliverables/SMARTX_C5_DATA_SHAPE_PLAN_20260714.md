# C5 DATA-SHAPE / INGESTION-STRUCTURE PLAN — SmartX → opal-data-assets

**Author:** 0.5.0_AE_OpalETL · 2026-07-14 ~07:4xZ · **To:** 1.0.0_SA_CTO (shape gate) · CC 2.0.0_SA_COO
**Ordered by:** Andrew (via CTO 060551Z: "they will need help potentially to structure a proper data
shape for the ingestion and so on but ill have them send you a plan") + Andrew-direct 07:05Z (the
client-identity table from the yaliu HAR, recorded @ `d8aa44b6e`).
**Grounding vintage:** every live number in this doc was measured 2026-07-14 07:2x–07:3xZ (probe +
ListObjectsV2 census) unless it cites the landed bronze/silver of run-date 2026-07-14. Code refs are
@ `c7cad5762` (CLOUD).

---

## 0. COVERAGE DENOMINATORS — what is ACTUALLY landed (live listing, 07:3xZ)

`s3://opal-data-assets/smartx/` = **9,534 objects / 50,040,347 B**:

| tree | n | bytes | dates | scopes | verdict |
|---|---|---|---|---|---|
| `allocation/{id}/bronze/holdings` | 9,525 | 45,654,262 | 20260714 | 9,525 | **THE ATOM: COMPLETE day-1 backfill** (the ~35/s run Andrew cited) |
| `model/{rmid}/bronze/holdings` | 1 | 4,430 | 20260714 | 1 | 1 of 11 models — model tier INCOMPLETE |
| `model/{rmid}/bronze/changerequests` | 1 | 4,055 | 20260714 | 1 | same |
| `model/{rmid}/bronze/performance` | 1 | 187,800 | 20260714 | 1 | same |
| `model/{rmid}/bronze/model_allocations` | 1 | **267** | 20260714 | 1 | **the OLD-endpoint EMPTY SHELL — must re-land from `enterprises/allocations?modelid=`** |
| `model/{rmid}/bronze/model_aum` | 0 | — | — | 0 | new feed (claimed code) — **never landed** |
| `platform/bronze/access_roster` | 1 | 9,301 | 20260714 | — | landed |
| `platform/silver/allocation_positions` | 1 | 3,050,617 | 2026-07-14 | — | crashed session ran silver once (draft-grade) |
| `platform/silver/allocation_valuation` | 1 | 1,126,821 | 2026-07-14 | — | same |
| meta/pulls manifests | 2 | 2,794 | 20260714 | — | landing+content denominators on the record |

**So the C5 "remainder" is precisely:** re-pointed model-tier pull for 11/11 models (incl. first
`model_aum` + re-landed `model_allocations`), the client-identity resolver (§3 — gated), the daily
lambda + TF, and the schema-pinned silver (§4).

---

## 1. THE FEED MAP — re-pointed + re-grounded, per-feed live bytes

**Auth:** opal7 SPLIT secrets (Andrew ~05:5xZ: opal7 STAYS; graduation dead). **Pacing:** none —
there is NO vendor rate limit (Andrew-direct, verbatim @ `c7cad5762`); `SMARTX_MAX_WORKERS` is the
throughput lever; the observed ceiling is most likely our own S3 write I/O.

| # | feed | endpoint (fetch id) | live grounding | bronze key | emptiness class |
|---|---|---|---|---|---|
| 1 | access_roster | `users/access` | 9,301B today; 11 fullAccess models, 0 accountAccess, ~900 view skipped | `smartx/platform/bronze/access_roster/{d}/` | expected-populated; `expect_min_models=11` RAISE |
| 2 | model holdings | `reportedmodels/{rmid}/holdings` | 4,430B landed (1 model) | `smartx/model/{rmid}/bronze/holdings/{d}/` | expected-populated per funded model |
| 3 | changerequests | `reportedmodels/{rmid}/changerequesthistory` | 4,055B landed | `.../bronze/changerequests/{d}/` | legitimately-sparse |
| 4 | performance | `models/{modelId}/performance?grouping=daily` | 187,800B landed | `.../bronze/performance/{d}/` | expected-populated per tracked model |
| 5 | model_allocations | **`enterprises/allocations?modelid={modelId}`** (re-point; the old `enterprises/reports/model/{id}/allocations` is a 267B empty shell at opal7 — re-confirmed live today) | 9,525 roster rows measured (crashed session, basis register) | `.../bronze/model_allocations/{d}/` | **expected-populated fleet-level: zero rows across ALL 11 models = broken endpoint, FAIL LOUD** |
| 6 | model_aum | **`enterprises/aum?modelid={modelId}`** | $1.428B daily closingEquity series (measured; variant 2 in the basis register). D4 §8.6: `totalAum` MIS-SCALED — gold uses per-day `closingEquity`; bronze stores raw regardless | `.../bronze/model_aum/{d}/` | expected-populated per funded model |
| 7 | **THE ATOM** — allocation holdings | `allocations/{allocationId}/holdings` | 9,525/9,525 landed, 45.6MB; $1.419B canonical basis reconciles to the penny (§7b basis register) | `smartx/allocation/{id}/bronze/holdings/{d}/` | expected-populated for open allocations; a single sparse allocation is legitimate; **fleet-zero = FAIL** |
| 8 | activity ledger (16-mo) | `accounts/{accountId}/activity` | **UNREACHABLE AT OPAL7 — measured today** (§5) | `smartx/account/{id}/bronze/activity/{d}/` (reserved) | n/a until tier resolves |
| 9 | **NEW: allocation_account_map** (Andrew-direct 07:05Z) | `enterprises/reports/model/{modelId}/allocations` **on an account-granted credential** | yaliu HAR: 755KB for ONE model — 3,182 records of `{accountId, accountNumber, accountName, allocationId, aumValue}` for 'Opal Conservative Growth'. **At opal7: 267B / 0 rows, live today** | `smartx/model/{rmid}/bronze/allocation_accounts/{d}/` (reserved) | expected-populated per funded model **when the grant exists**; reconciliation guard vs feed 5 (§2) |

**Filing law (unchanged):** all model feeds FILED under `reportedModelId`; fetch id per family
(rmid for `reportedmodels/*`, modelId for the rest) — the C2-class trap the first live pull caught.

---

## 2. THE CONTENT GUARD — per-feed emptiness contracts (ruled bar, PRD v2.1 ruling 26)

Reference case: the 267B near-miss — a well-formed empty payload is a PERFECT landing (key present,
Size>0, set-identity reconciles, guard_ok=True). Landing conservation and content sufficiency are
different properties; each gets its own instrument. Implemented and claimed @ `eab9c6693`:

- **Per-result `rows` denominator** (`pull.py::_row_count`) on every landed object, into `meta/pulls/`.
- **Fleet-level assert** (`backfill.py::assert_fleet_content`): a feed whose TOTAL rows across the
  enumerated roster is zero FAILS LOUD (`EmptyFleetError`). One empty scope is legitimate — 4 of
  Opal's 11 models are genuinely unfunded (0 accounts, $0); an empty FLEET is a broken endpoint.
- **Impossibly-empty statements per feed:** access_roster: <11 owned models = RAISE (not merely
  empty). atom: 0 positions across all 9,525 allocations = impossible. model_allocations: 0 across
  11 models = impossible (measured 9,525). model_aum: 0 days across funded models = impossible.
  changerequests: empty legitimate (sparse by nature). performance: empty on a tracked model =
  suspicious → WARN-level, fleet-zero = FAIL.
- **NEW cross-feed reconciliation (feed 9 vs feed 5):** for each model, `|allocation_accounts|`
  must equal that model's row count in `model_allocations`, and `sum(aumValue)` should tie to the
  roster `value` basis (variant 1). A resolver that returns fewer rows than the roster is a PARTIAL
  identity table and must fail loud, not silently under-attribute.
- **22:00Z tonight (separate lane, C4):** the ETF first-fire verify includes content non-emptiness
  ON the landed bronze object — open it, SEE the content (CTO 061206Z, folded).

## 3. THE CLIENT-IDENTITY RESOLVER — Andrew's table, and the measured grant boundary

**What Andrew ordered (verbatim @ `d8aa44b6e`):** derive who-is-who from the client-holdings surface
in the yaliu HAR; land it as another bronze/silver shape; match in gold.

**What the HAR yields (the MAP, per CTO pin):** the resolver is
`enterprises/reports/model/{modelId}/allocations` → per-model records carrying **exactly the join
key + identity**: `allocationId ↔ accountId, accountNumber, accountName (+ aumValue)`. One call per
model. Secondary surfaces if ever needed: `4.1/accounts` (paged roster: accountTitle,
brokerageAccountNumber, custodian, enterprise, repCode) and `3.1/allocations?accountId=` (inverse).

**The measured boundary (probe, 07:29Z, opal7, all HTTP 200):** resolver = 267B/0 rows on an owned
funded model; `4.1/accounts` = 414B/**0 accounts**; `users/access` accountAccess = 0 → **no account
id is enumerable, so feeds 8+9 are UNREACHABLE at opal7 — grant boundary, exercised, not assumed.**
Same endpoint, same model family, on yaliu: 3,182 identity rows. **This is the
tier-inaccessibility finding routed to you** (it also closes the feed-8 residual as far as opal7
can close it).

**Options (I do not adjudicate; evidence attached):**
- **(a) Scoped bundle-credential use for feed 9 (+8) only.** `auth_bundle` carries the dormant
  BUNDLE shape (env-selected, `SMARTX_CRED_BUNDLE_SECRET`). The opal7-stays ruling settled the
  VALUATION pipeline's credential; a scoped identity-feed grant is a new, narrower question.
  Caution from the crashed session's measurement: the yaliu-grade grant is MISSING 4 of Opal's 11
  models and downgrades 7 to view — so feed 9 on a bundle credential must pair with the
  `expect_min_models` class of guard on ITS roster, and it changes nothing about feeds 1–7.
- **(b) One-time HAR seed.** Andrew's literal words support seeding the table from the HAR capture;
  your 071035Z pin (HAR-is-map, bytes never land in bronze) was premised on opal7 pullability,
  which today's probe falsified. If ruled, it lands as a clearly-labeled `meta/seeds/` artifact
  (never `bronze/` — 17a: bronze is what the SOURCE delivers), and the API feed replaces it the day
  a grant exists.
- **(c) Vendor grant widening on opal7** (Andrew ↔ SmartX; longest path, cleanest end-state).

## 4. SILVER SHAPES — the fact tables + pinned pyarrow schemas (V2-8 contract)

Law: Rule 17 strict — dedup + dtype ONLY; every vendor column preserved (vendor bugs included:
`assetType` uniformly 'equity', `industry` 'Unknown / Not Available' — classification is a GOLD
join to ETFClassifier); **NO basis computation in silver** (five internally-consistent AUM bases
exist — basis register §7b of the architecture doc; Andrew ruled `longEquity + cash` GROSS
canonical and reserved the right to change it → basis applied in GOLD so a change is a one-line
gold edit, never a re-ingest). Silver lands at platform scope (firm-wide fact tables).

| table | grain | key columns (pyarrow explicit schema in the converter — no inference) |
|---|---|---|
| `allocation_positions` (THE ATOM) | allocation × symbol × as_of | ids/str: allocation_id, owner_id, ticker, symbol_id, symbol_alias_id, company, asset_type, industry; ts: as_of, last_seen_date, run_date, _ingested_at; f64: quantity, price, multiplier, market_value, value |
| `allocation_valuation` | allocation × as_of | ids/ts as above; f64: equity, long_equity, short_equity, cash, accrued_dividends, accrued_fees, accrued_interest; i32: long_position_count, short_position_count, total_count — **all five basis components, always** |
| `model_aum_daily` | model × day | str: model_id, rmid; date: day; f64: closing_equity (+ every other per-day vendor field raw; `totalAum` PRESERVED but flagged mis-scaled — gold ignores it) |
| `model_allocation_roster` | model × allocation × run_date | from feed 5: advisor fields, model, value, status, opened_date — the roster basis (variant 1) preserved |
| `allocation_account_map` (NEW, gated §3) | model × allocation × run_date | str: model_id, rmid, allocation_id, account_id, account_number, account_name; f64: aum_value — **the gold client↔allocation match key** |

Draft-quality deltas from the crashed session's one silver run, fixed in the V2-8 build: explicit
`pyarrow.schema([...])` per table (today it infers via pandas), and landing verify moves
head_object → **ListObjectsV2 key+ETag+Size** (the monolith's acceptance instrument; HeadObject is
s3:GetObject and is never the acceptance instrument).

Gold (downstream, not this plan's scope to build): atom × `allocation_account_map` → client-level
time series (Andrew's ADVI requirement: "clients will want access to time series and views
associated with their model holdings"); basis applied per the canonical ruling.

## 5. FEED-8 RE-CHECK ON OPAL7 — verdict (spec part 4)

Executed today (probe 07:29Z): the 16-month activity ledger requires an `accountId`; **zero
accounts are enumerable at opal7** (`users/access` accountAccess=0; `4.1/accounts` 200/0 rows;
`accounts/counts` returns counts but no ids). **Feed 8 is grant-blocked at opal7 — measured, not
conceded.** It rides the same §3 decision.

## 6. FENCE ATTACH — the one-gate rider (your 072924Z)

**TF plan (targeted, run 07:3xZ): `1 to add, 0 to change, 0 to destroy` — pure add.**
`aws_iam_role_policy_attachment.assets_pull_fence`: role `smartx-assets-pull-role` ←
`arn:aws:iam::313476888478:policy/opal-assets-one-way-fan-in-fence`.

**22a exercise list post-attach (each simulate = ONE `--resource-arns`; positive control ISOLATED):**
1. POSITIVE CONTROL (separate invocation): `simulate-principal-policy` role=smartx-assets-pull-role,
   action=`s3:PutObject`, resource=`arn:aws:s3:::opal-data-assets/smartx/platform/meta/pulls/probe.json`
   → expect **allowed** (the belt must not eat the legitimate write).
2. `s3:PutObject` on `arn:aws:s3:::opal-data-etfs/silver/etfs_netassets/probe.parquet` → expect
   **explicitDeny** (upgraded from implicit — the V2-5 S04/S05 gap this attach closes).
3. `s3:PutObject` on `arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json` (Door 6) →
   expect **explicitDeny**. (No `--context-entries` needed: the fence policy is unconditioned —
   verified in the policy doc before simulating; if a Condition is found, entries get passed.)
4. APPLIED truth: `aws iam list-attached-role-policies --role-name smartx-assets-pull-role` shows
   the fence ARN (comp-iam view = DESIRED only).
5. BEHAVIORAL exercise: the next real pull writes `meta/pulls/` under the attached role and the
   listing shows it landed (config-read is not a works-claim).

## 7. ORCHESTRATION (C5 remainder — build order after your shape gate)

1. **Model-tier completion pull** (11/11 models, re-pointed feeds 5+6, content guards armed) —
   backfill.py to convergence; re-lands the empty `model_allocations` from the right endpoint.
2. **Daily lambda** (single invocation: platform + models + 9,525 allocations; unpaced,
   `MAX_WORKERS=16` measured-safe; minutes, not hours) + EventBridge schedule + TF (pure-add per
   the new-territory rule) + source-map row + deliberate sizing (Rule 5).
3. **Silver converter** per §4 pinned schemas (V2-8 contract) — after your shape gate.
4. **Feed 9 resolver** — the moment §3 is ruled, same engine, same guards.

**22:00Z tonight outranks everything when due** (C4/parity lane, unchanged). V2-1 producer stays
untouched until the first-fire proof.
