# Cross-Surface Reconciliation Test — Black Diamond and Orion

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer · **Date:** 2026-07-22
**Commissioned:** Andrew-direct — test the open question both master briefings raised: *do a vendor's two
surfaces agree on value?*
**Egress:** **NONE.** Both tests run entirely on captured bodies and data we already store. No vendor API was
called.

> **THE FRAMING THAT GOVERNS EVERY RESULT BELOW (Andrew-direct, mid-test):**
> **Differentiate the VENDOR'S SHAPE from the TENANT'S DATA QUALITY** — Black Diamond shape vs Cottonwood
> data; Orion/Eclipse shape vs Inflection data. A zero, a gap, or a grain mismatch may be a property of *this
> book* rather than of *that platform*. This correction arrived while the BD test was running and it changed
> what I was entitled to conclude — flagged inline at each result.

---

## 1. Results at a glance

| Test | Axis | Verdict |
|---|---|---|
| **BD** Surface A (DataMining) × Surface B (product API) | Identity spine | **PASS (strong)** |
| | Structural treatment | **PASS (informative)** |
| | **Value** | **INCONCLUSIVE — and the "pass" is worthless, see §2.4** |
| **Orion** Surface A (our ingest) × Surface B (`Reporting/Scope`) | **Value** | **PASS — EXACT, to the cent** |
| | Engine internal consistency | **PASS — EXACT to 6 significant figures** |
| | Method-contract mechanism | **PROVEN by a live request (was previously inferred)** |

---

## 2. Black Diamond — DataMining × the product API

**Probe account:** Surface B `accountId 26725961` / `externalId z0926725961` (identity masked; a Cottonwood
household). **Surface A:** `s3://opal-data-cot/silver/holdings/{date}.parquet`.

### 2.1 Identity spine — **PASS (BD SHAPE)**

The two surfaces expose **one book of record under two encodings**:
- Surface B returns **both** `accountId` (integer, internal) **and** `externalId` (`z`-prefixed).
- Surface A carries **only** the `z`-prefixed form in `account_id`.
- The bridge is structural: **`accountId 26725961` ↔ `externalId z09`+`26725961`**.
- Conformance measured, not assumed: **707 of 707** account_ids on 2026-06-08 and **913 of 913** on 2026-07-20
  match `z09<digits>`. Relationship (`z09305730`) and portfolio (`z097031791`) ids share the convention.

**This is BD shape, and it is load-bearing** — it is the join that makes the ingest surface and the product
surface reconcilable at all. RCN-0001 noted the `z`-convention as a curiosity; it is actually the bridge.

### 2.2 Structural treatment — **PASS (BD SHAPE)**

BD Surface B reports the account `positionClosed: True`, `dataAsOfDate 2026-06-05`, top-level and all four
asset-class rollups **$0.00**. Surface A on 2026-06-08 and 2026-07-20 retains the account with **20 holding
rows, all zero**.

> **Both surfaces keep a closed account as a zero-value shell rather than dropping it.** That is a platform
> property with a direct consumer consequence: any "accounts with value" or account-count metric must filter
> on value, not on presence. *(Orion exposes the same idea as an explicit setting — `69CLIENTPE Household
> Performance Include`, with options down to "Accounts with value". BD leaves it to the consumer.)*

### 2.3 Value axis — **INCONCLUSIVE**

The only date where both surfaces overlap is **2026-06-08**, and there they agree: **$0.00 = $0.00**.

**I am not scoring that as a pass.** It is the textbook case from `INSTRUMENTS_AND_AXES` §3 — *an agreement
that could not have failed carries no information.* Two surfaces returning zero for unrelated reasons would
produce this identical result.

The one **non-zero** Surface-B reference is `beginningMarketValue = $102,739.131` (a coherent tree: $102,739
top → $63,357 → $12,087 at depth). It is a **period-start** value whose sibling endpoint places the window
start at ~**2026-05-20** — and **our Surface-A silver retention begins 2026-06-08** (29 partitions). *The
non-zero reference predates the data we keep.*

### 2.4 Shape vs data quality — the split Andrew called

| Observation | Which is it? |
|---|---|
| The probe account reads $0.00 on both surfaces | **Cottonwood DATA** — that household's positions closed ~06-05 |
| Surface-A retention starts 06-08 | **Opal pipeline choice**, not BD |
| Account count 707 (06-08) → 913 (07-20) | **Cottonwood DATA** — book growth |
| Shared `z09`+internalId identity space | **BD SHAPE** |
| Closed accounts persist as zero-value shells | **BD SHAPE** |
| `allocationOfParent`/`allocationOfTotal` are **objects** carrying point values in `allocation`, but **scalars** in `performancePeriod` | **BD SHAPE** — the same field name has two types across endpoints (§2.5) |

### 2.5 Incidental shape finding — polymorphic field naming

In `/api/allocation`, `allocationOfParent` and `allocationOfTotal` are **objects**
(`{beginningMarketValue, beginningAllocation, marketValue, shortMarketValue, accrual}`). In
`performancePeriod`'s `asOfDatePoints`, the same names are **scalars** (`1.0`). **A consumer that assumes one
shape breaks on the other**, and this cost me three contradictory probe results before I located it.

### 2.6 What would close the BD value test

**One BD capture of a live, non-zero client dashboard on any date from 2026-06-08 onward.** That is a single
dashboard visit. The test harness is now written and would run immediately against it.

---

## 3. Orion — our ingest × `Reporting/Scope`

**Probe account:** Orion `entity: 7` (Account), `entityIds: [2038]`, `asOfDate 2026-07-21`.
**Surface B:** a captured `POST /api/v1/Reporting/Scope` request **and** response from the RCN-0002 HAR.
**Surface A:** `s3://opal-data-inf/bronze/orion-api/latest/accounts_roster.json` (3,135 accounts, pulled
2026-07-22 09:51Z) and `s3://opal-data-inf/bronze/performance/2026-07-20.jsonl.gz`.

### 3.1 Value — **PASS, EXACT**

| Source | Field | Value |
|---|---|---|
| **Surface B** — `Reporting/Scope` on-demand calculation | `endValue` (2026-01-01 → 2026-07-21) | **$7,489.89** |
| **Surface A** — our ingested `accounts_roster.json` | `currentValue` | **$7,489.89** |

**Agreement to the cent.** This is the reconciliation the master briefing said was assumed but never measured.
**It holds.** Orion's on-demand calculation engine and the account roster we ingest daily report the same
value for the same account.

### 3.2 Engine internal consistency — **PASS, EXACT**

The response carries a **202-point daily `performance-breakdown` series** and a reported period return.
Geometrically linking the daily series reproduces the reported figure **exactly**:

```
link(202 daily points, as PERCENT)  = 7.3612 %
reported YTD `performance`          = 0.073612   (= 7.3612 %)
```

Six significant figures, no residual. **Orion's daily series composes exactly into its period return** — the
engine is internally consistent and the methodology is genuinely daily-linked TWR.

*(Sanity: simple value change is 7022.65 → 7489.89 = **6.6533%**, below the 7.3612% TWR. The gap is external
flows — precisely why TWR ≠ value change, and a further sign the engine is doing what it claims.)*

### 3.3 **NEW TRAP — mixed units inside one response**

| Node | Convention | Example |
|---|---|---|
| `calculated-performance` (period) | **decimal FRACTION** | `0.073612` = 7.36% |
| `performance-breakdown` (daily) | **PERCENT** | `0.549508` = 0.55% |

**The same response uses two conventions, and only one is documented.** Orion's docs warn *"Percentages are
decimals and will need to be converted"* — that applies to the period value and is **actively misleading for
the daily series**. Treating the daily points as fractions gives **−100.0001%**; treating the period value as
a percent understates by 100×. **A 100× error either way, from following the documentation.**

### 3.4 Method contract — **the mechanism is now PROVEN, not inferred**

RCN-0002 claimed the tenant settings and the request-time `performanceOption` are the same switchboard, based
on **name correspondence across two evidence layers**. The captured request settles it — it carries the block
live:

```json
"performanceOption": {
  "calculationMethod": "TWR",          "calcGrossOfFees": true,
  "includeAccruedInterest": "True",    "calcFirstDayPerformance": "True",
  "calcIntraDayPerformance": "True",   "annualize": "True",
  "annualizeIncludeDaysWithoutValue": false,
  "suppressMixedRanges": "False",      "suppressMixedAssetLevelGroups": "False",
  "calcAfterTax": "False",             "intradayCalculationMethod": "Enhanced",
  "flipSignForShort": true }
```

**And it demonstrates OVERRIDE, which is the part that mattered:**

| Parameter | Firm setting (RCN-0002) | This request | Result |
|---|---|---|---|
| Gross of fee | `1:69GROSSO = False` (**net**) | **`calcGrossOfFees: true`** | **request OVERRIDES the firm default** |
| Intraday method | `INTRA:CALC = Enhanced` | `"Enhanced"` | inherited |
| Annualization day-count | `1:69ANNUAL = Days with value only` | `annualizeIncludeDaysWithoutValue: false` | inherited — **and this confirms the semantic mapping** |

> **The firm setting is the persisted default; the request overrides it per call.** "Performance Viewer 3
> Ad-Hoc" asked for **gross** while the firm default is **net**. This is the single most transferable design
> idea from either vendor, and it is now demonstrated rather than argued.

### 3.5 A finding about OUR data, not Orion's

`bronze/performance/{date}.jsonl.gz` is `client_id · date · factor · pull_date` — **456,313 records, 315
clients, 2,247 dates (2020-05-26 → 2026-07-20)**.

**I hypothesised `factor` was a daily growth factor (1+r). That is FALSIFIED** — only 30% of values fall in
(0.9, 1.1), max is 170.7, and geometric linking explodes to ~10³⁹%.

**What it actually is:** a **cumulative TWR index rebased to 1.0000 at inception.** Measured on the
longest series — starts exactly `1.0000` (2020-05-26), ends `1.5822` (2026-07-20), 69% monotonic-increasing
(not 100%, correctly, because markets fall). **2026 YTD = 1.4770 → 1.5822 = +7.12%**, the same magnitude as
Orion's 7.3612% for its account.

> **The field name is misleading and it is ours, not Orion's.** `factor` reads as a per-period factor; it is a
> cumulative index. Anyone linking it would be catastrophically wrong — as I was, until the control caught it.
> **Correct usage is `factor[end]/factor[start] − 1`.** Worth a rename or a documented note.

### 3.6 Shape vs data quality — the Orion split

| Observation | Which is it? |
|---|---|
| `currentValue` == `endValue` to the cent | **ORION SHAPE** — surfaces agree |
| Daily series links exactly to period return | **ORION SHAPE** — engine consistency |
| Mixed units in one response | **ORION SHAPE** — a platform trap |
| Settings-as-defaults with request override | **ORION SHAPE** |
| Our store is **client-grain**, the captured call is **account-grain** | **OPAL/INFLECTION pipeline choice** — not Orion; Orion's `Scope` accepts 36 entity types incl. both |
| `factor` is a cumulative index with a misleading name | **OPAL DATA** — our field, our naming |
| `AttributionDetails` / `IndexBlends` returned `[]` in RCN-0002 | **INFLECTION DATA** — tenant has none; says nothing about Orion |

---

## 4. What this changes

1. **Orion is now a validated parity oracle.** Its value agrees with our ingest to the cent and its engine is
   internally exact. When `fact_account_return` is built, **Orion — not just BD — can serve as a check**, and
   for Inflection accounts it is the *better* one because we already ingest it daily.
2. **The BD value tie remains open**, and the master briefing's claim that it was "assumed, not measured" was
   correct. One live-account capture closes it.
3. **Two consumption hazards are now named**: Orion's mixed units (100×) and our own `factor` semantics.
   Both would have produced silently wrong numbers in a build.
4. **The method-contract override mechanism is proven**, which strengthens the `dim_return_method` design
   recommendation from "the incumbents have one" to "the incumbents have one *and* make it callable, and here
   is a live call doing it."

## 5. Limits

Both tests are **n=1 account**. Orion's exact match is strong evidence for the *mechanism* but does not
establish population-wide agreement — a fleet-level reconciliation (all 3,135 roster accounts vs a batched
`Scope` call) would, and would require an authorized live call. The BD test is bounded by a single closed
account and a retention window. Neither test touched returns *at account grain on our side*, because we do not
store them there.
