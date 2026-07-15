# SmartX part-2 expectation report — six pinned tables (pre-build gate, 0.5.0's build order)

**Author:** 0.4.0_DS_ClientPlatform, 2026-07-15 ~18:0xZ. **Gates:** each 0.5.0 part-2 build run is
measured against ITS section here (the part-1/1b pattern; runs wait on these pins per 0.5.0 173906Z).
**Binding law folded:** CTO part-2 rulings R1–R4 (153851Z) · grain law + envelope-attestation rulings
@ b3df964aa (relayed 175031Z) · column expectation = **the committed pinned schemas in
`infra/aws/lambda/smartx_assets_pull/silver.py` @ b3df964aa** ("expect THOSE") — this report pins
DENOMINATORS, GRAINS, VOCABS, INVARIANTS, and the payload shapes I measured MYSELF.
**Grounding:** every number below measured this session, read-only, directly on the landed bronze
(scratchpad `smartx_sweep_ground*.py`, `smartx_part2_ground3.py` + the two follow-up probes);
0.5.0's fleet numbers independently CONFIRMED where cited (two instruments agree).

**Cadence facts (R4 confirm-first binds 1–3):** account-tier + platform-tier part-2 feeds are
**20260714-latest** (sweep 20260715 = 0 objects; detail + nonzerosleeve likewise) while the model
tier fires daily (20260714 AND 20260715 present, 11 objects each). A 07-15 absence on feeds 1–3 is
a CADENCE FACT until 0.5.0 confirms each schedule — never a staleness finding (NEVER#1 at feed
granularity). Bronze basenames per feed (grounds the contract rule-10 event-rule set):
`allocations.json` · `nonzerosleeve.json` · `detail.json` · `holdings.json` · `performance.json` ·
`history.json` (changerequests).

---

## 1. fact_account_allocations (the sweep) — STATE-GRAIN (allocation_id, run_date)

- **Source objects:** `smartx/account/{uuid}/bronze/allocations/20260714/allocations.json` =
  **7,066** (my census == 0.6.2's skeleton == 0.5.0). Envelope: {data[], count, version,
  hostDetails, statusCode, requestId, timestamp}.
- **Vendor self-check (pin as refuse-gate):** `count == len(data)` — measured 60/60 sampled objects.
- **Rows:** sample n=180 objs -> 563 recs (min 0 / median 3 / max 8 per account; 15/180 objects
  carry EMPTY data[] = accounts with zero allocations, a lawful state, count==0 attests it).
  **EXPECT fleet total ~22,100 rows; band [19,000 – 25,500]** (sample-mean extrapolation, 2.5%
  sample — the atom precedent ran 2.7% off at this sample class).
- **Record shape (measured):** scalars `id`:str (THE allocation id — the natural key), `type`:str,
  `status`:str, `tradingType`:str, `leverage`:float, `isApmAllocation`:bool,
  `matchModelLeverage`:bool; nests `account{id}`, `advisor{id,name,crd}`, `model{id,name}`,
  `openTimestamp{timestamp,friendly}`, `closeTimestamp{timestamp,friendly}`.
- **Structural presence laws (pin all three):** `model` present <=> `type=='model'` (measured
  212/212 exact); `closeTimestamp` present <=> `status=='close'` (43/43 exact); everything else
  563/563 present.
- **Vocab pins:** type ∈ {managedPortfolio, funding, model, protected} (sample: 165/165/212/21);
  status ∈ {open, close} (520/43). model-null 62% == the non-model share, BY CONSTRUCTION.
- **R3 CONTAINMENT PIN (the ruled invariant, framed so either verdict is information):** the map
  (`fact_allocation_account_map` date=2026-07-14, 7,141 rows) is the MODEL-allocation resolver;
  the sweep spans ALL FOUR types. Therefore the containment matrix is BY TYPE x STATUS: EXPECT
  `type=='model' AND status=='open'` sweep ids largely ⊂ map allocation_id; non-model types
  legitimately OUTSIDE. My 60-obj sample: 214 sweep ids -> 65 in map / 149 outside (the outside
  set is dominated by non-model types). **The build prints the full matrix (type x status x
  in-map) with counts; a model-open id NOT in the map is the finding class to surface.**
  fact_account_allocations stays DISTINCT from the map (merge = gold join, R3).

## 2. fact_nonzerosleeve — STATE-GRAIN (sleeve_id, run_date)

- **Source:** `smartx/platform/bronze/nonzerosleeve/20260714/nonzerosleeve.json` = **1 object**;
  envelope {count, data[], statusCode, requestId, timestamp}; `count==len(data)` TRUE.
- **EXPECT rows = 511 exactly** (full read, not a sample).
- **Shape (full profile, FLAT — no nests):** 22 fields, ALL 511/511 present+non-null EXCEPT
  `parentEnterpriseId`/`parentEnterpriseName` (present, ALL-NULL — preserve as delivered).
  ids/names str (`id` = the sleeve id, `accountId`, `accountName`, `allocationId`,
  `enterpriseId`, `enterpriseName`); opening/closing value pairs float64 (Cash, Dividend, Equity,
  Fee, Interest x2); `longPositionCount`/`shortPositionCount` int; **`asOfTimestamp` is an ISO
  STRING — the third vendor timestamp rendering** (not {ts,friendly}); pin it string, no epoch.
- **Custody carrier AC (R1):** `brokerageAcctNum` 511/511 non-null, 8-digit numeric STRING —
  byte-faithful string discipline + the leading-zero mutant in the suite (this partition has 0
  leading-zero instances — the mutant guards the day one arrives; Int64 coercion is the defect).
- **Cross-feed note:** `allocationId` here is a JOIN EDGE to the sweep's `id` — worth a
  containment count in the manifest (informational, not a gate).

## 3. fact_account_detail — STATE-GRAIN (account_id, run_date)

- **Source objects:** `smartx/account/{uuid}/bronze/detail/20260714/detail.json` = **91**.
  **`data` is a single ENVELOPE DICT per object (not a list)** — grain = one row per account;
  **EXPECT rows = 91 exactly** (count field ties trivially).
- **Shape (25-obj sample, all fields 25/25 present+non-null):** 26 fields. Nests:
  `custodian{id,name}`, `enterprise{id,name}`, `createdOn{timestamp,friendly}`. Lists (R2
  CONFIG-PRESERVE -> canonical-JSON columns, the _encode_cell idiom): `feature[]` (len 10 on ALL
  sampled — a stable flag block) and `repCode[]` (len 1 on all sampled — still a LIST, preserve
  as JSON, no scalar flattening).
- **BOOLEANS: I measure NINE** (isTrading, isApm, shouldRebalance, mutualFundDividendReinvest,
  equityDividendReinvest, hasRepCode, isDemo, isExcluded, isBlackListed) — 0.5.0's build-order
  note said 8; the committed schema is the tiebreak, and a 9th-bool delta between my sample and
  the schema REFUSES rather than coerces. Named so the discrepancy cannot pass silently.
- **Custody carrier AC (R1):** `brokerageAccountNumber` str, byte-faithful + leading-zero mutant
  (same law as sec-2; 0 leading-zero instances in this partition, guard stands).
- **Scalars:** accessLevel/accountTitle/accountType/internalType/marginType/optionLevel/
  permission/name/status/targetWeightId/id — strings.

## 4. fact_model_holdings — STATE-GRAIN (rmid, symbol_id, run_date)

- **Source objects:** `smartx/model/{rmid}/bronze/holdings/20260715/holdings.json` = **11**
  (daily-firing feed; both 07-14 and 07-15 present).
- **EXPECT rows = 164 @ 20260715 exactly** (my full read == 0.5.0's pin — two instruments agree).
- **Record shape:** {marketValue, multiplier, percentOfPortfolio, price, quantity, symbol{assetType,
  companyName, defaultSymbolAliasId, id, industry, multiplier, ticker}}. **`multiplier` exists at
  BOTH levels on ALL 164 rows (measured 164/164) — TWO columns, both preserved** (record-level +
  symbol-level; never collapsed, never assumed equal).
- **Vendor-bug preservation class:** assetType/industry land as delivered (the atom-positions
  precedent — 'equity'-uniform and 'Unknown/Not Available' are vendor states, preserved).

## 5. fact_model_performance — STATE-GRAIN (rmid, day, run_date), R2 SERIES-EXPLODE

- **Source objects:** `smartx/model/{rmid}/bronze/performance/20260715/performance.json` = **11**.
- **FULL PATH (my grounding adds a level to the record):** `data.model{id,name}` +
  `data.performance{grouping, recordCount, range, performance[]}` — the ENVELOPE is at
  data.performance; the inner performance[] explodes to rows {range{start,end each
  {timestamp,friendly}}, pnl{dollar,percent}, summary{7 keys incl. isFullRange:bool +
  transactions}} (R2: measures/series explode; the envelope attrs ride as columns).
- **EXPECT grand total = 6,456 inner rows @ 20260715** — independently recounted, exact; per-model
  recordCounts pinned: 467/467/362/554/554/467/554/467/492/554/1518 (matches 0.5.0's corrected
  173906Z+174039Z numbers; the 5,973 figure is superseded).
- **ENVELOPE SELF-CHECK (CTO ruling b, KEPT — pin as refuse-gate):** `recordCount ==
  len(performance)` per object — measured 11/11; a truncated payload REFUSES rather than landing
  short, guarding the 6,456 from below.
- **DTYPE PIN (the name lies):** `summary.transactions` is a DOLLAR AMOUNT — float64 with
  1,280/6,456 fractional values measured (independently confirmed). NEVER int-coerced (the
  delta-7 value-semantics class). isFullRange bool 6,456/6,456; other summary fields float64.
- **Sparsity law:** the FULL series exists even for aum-empty models (all 11 models carry full
  series) — sparsity is per-FEED, not per-model.

## 6. fact_model_changerequests — **EVENT-GRAIN (ruled: exact-row dedup ONLY, no natural key)**

- **Source objects:** `smartx/model/{rmid}/bronze/changerequests/20260715/history.json` = **11**;
  `data` is a plain LIST.
- **EXPECT recs = 1,058 @ 20260715 exactly** (my full count == 0.5.0 — two instruments agree).
- **GRAIN LAW (CTO ruling a, carried explicitly as ruled):** this table is EVENT-GRAIN by
  construction — ledger-like, two partial trades can legitimately collide on every business
  field; **exact-row dedup only, NO conflict key, NO conflict-RAISE**. I CONCUR with 0.5.0's
  parser treatment — this is the one part-2 table where a natural-key assertion would be the
  defect.
- **Record shape:** {activity:str, company:str, ticker:str, requestedBy:str (plain string),
  percentage:float, price:float, quantity:float, from{percent,quantity}, to{percent,quantity},
  tradeTimestamp{timestamp,friendly}}. Vocab pin: activity ∈ {buy 641, sell 417} @ 20260715.

---

**Standing for all six:** pinned pyarrow schemas in silver.py @ b3df964aa are the column
expectation; ids/dates string, counts int32, values float64 (family dtype law); Rule 17
passthrough-complete; manifests cite THIS report as expectation source (the part-1 pattern);
ListObjectsV2 acceptance; per-run manifests to the meta home. Cadence-confirm (R4) precedes any
freshness treatment on feeds 1–3.
