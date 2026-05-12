# DS Briefing — Concentration Risk Drill-Down (Firm → Security → HH)

**Pipeline:** Inflection partner / Advisor Intelligence
**Artifact:** **NEW** — `platinum/firm/firm_concentrations.json` (under `opal-data-inf`)
**Consumer:** `InflectionInsightsPanel` → Concentration Risk lens (`portal/src/pages/AdvisorIntelligence/_partners/inflection/InflectionInsightsPanel.tsx`)
**Status:** FE not yet rewritten. This brief drives both the new artifact AND the FE redesign that follows.

---

## 1. Summary

Restructure the Concentration Risk lens from a HH-centric treemap (each tile = household) into a **firm → security → household drill-down**:

- **Top-level treemap:** tiles are the firm's top concentrated securities (tile size = total firm position in that security)
- **Click a security tile:** drills into the top households holding that security (ranked by the security's % of *their* book)
- **Internal toggle inside the panel:** Single Stocks vs Funds (ETF + MF) — re-renders the top-level treemap to that subset

Almost all of the underlying data already exists in `INF_D_07.concentration_risk.py` (HH-level top-1) and `INF_D_02b` (firm top_holdings.json). What's new is the **per-security top-holder list** and **security_type classification**.

---

## 2. Motivation

The current HH-centric treemap answers "which households are concentrated?" — useful, but the next-step advisor question is always "concentrated in *what*, and who else is holding it?" Andrew's framing: surface the firm's actual concentration risk by *security*, then drill to the households driving it.

The toggle exists because the answer differs by security type:
- Concentrated in a single stock (e.g., NVDA at 35% of a book) → real idiosyncratic risk, often legacy/inherited positions
- Concentrated in an ETF (e.g., VOO at 35% of a book) → diversified internally, mostly a portfolio-construction observation

Advisors look at these two categories differently. The toggle lets them.

---

## 3. Current vs target state

**Current artifacts in this area:**
- `platinum/firm/concentration_risk.json` (INF_D_07) — HH-level: top-1 % per HH, HHI, risk tier
- `platinum/firm/top_holdings.json` (INF_D_02b) — firm-aggregated top 10 securities + Other rollup
- `platinum/clients/{household_id}/top_holdings.json` (INF_D_05) — per-HH top holdings drill

**What this brief adds:** one new artifact that *joins the question*: firm-level top securities **enriched with their top holders**, plus security_type classification driving the FE toggle.

**No existing artifact is replaced or removed.** `concentration_risk.json` and `top_holdings.json` keep their current shape and downstream consumers.

---

## 4. New artifact schema

**Path:** `platinum/firm/firm_concentrations.json`

```ts
interface FirmConcentrationsArtifact {
  generated_at:   string    // ISO timestamp
  data_as_of:     string    // YYYY-MM-DD of source holdings snapshot
  total_firm_aua: number    // for normalizing pct_of_firm_aua
  securities:     FirmConcentrationSecurity[]
}

interface FirmConcentrationSecurity {
  ticker:                  string       // e.g., "VOO", "META", "AAPL"
  asset_name:              string       // e.g., "Vanguard S&P 500 ETF"
  security_type:           SecurityType // see §5
  asset_class:             string       // equity | fixed_income | alternatives | cash | other (existing 4-bucket from Orion native classifier — same as INF_D_03 uses)
  total_position_value:    number       // dollars: sum of market_value across all HHs holding this ticker
  pct_of_firm_aua:         number       // total_position_value / total_firm_aua, 0.0–1.0
  holder_count:            number       // distinct HHs holding this ticker
  top_holders:             SecurityTopHolder[]   // ranked, capped at 10 (see §6)
}

interface SecurityTopHolder {
  household_id:            number       // Orion Int64, matches the existing canonical key
  position_value:          number       // this HH's $ position in this security
  hh_aua:                  number       // this HH's total AUA (for context)
  hh_concentration_pct:    number       // position_value / hh_aua, 0.0–1.0  — i.e., this security's share of THIS HH's book
}

type SecurityType = 'single_stock' | 'etf' | 'mutual_fund' | 'other'
```

**Cardinality:**
- `securities`: top **25** by `total_position_value`. (FE treemap can show fewer; oversupply is fine.)
- `top_holders`: top **10** per security by `hh_concentration_pct` descending. Ties broken by `position_value` descending.

**Filtering at source:**
- Include `security_type IN ('single_stock', 'etf', 'mutual_fund')` AND `asset_class IN ('equity', 'fixed_income', 'alternatives')`.
- Exclude cash / money_market — concentration risk doesn't apply to MM funds (Andrew confirmed 2026-05-12 follow-up).
- **CORRECTION (2026-05-12 19:53Z):** original v1 of this brief said "equity-class only" — that was wrong. Inflection's top 10 holdings have substantial fixed-income exposure (HTRB 7.1%, BAGIX 6.7%, BSIIX 5.4%) which is real concentration. Fixed income funds must be included.
- `security_type === 'other'` is permitted as a catch-all but should be rare. Flag if >5% of securities land in `other` so we can refine the classifier.

---

## 5. Security type classification — the new field

This is the only genuinely new derivation. We need `security_type ∈ {single_stock, etf, mutual_fund, other}`.

**Recommended approach (in priority order):**

1. **If Orion's `silver/assets_v2/{date}.parquet` has a native `product_type` or `instrument_type` field** that distinguishes ETF / Stock / Mutual Fund — **use it**. This is the canonical source per Andrew's 2026-04-29 "use what Orion uses" directive (already applied for asset_class via INF_D_03).

2. **If Orion only gives us product_category** (Equity/Bond/Money Market) without a sub-type, derive:
   - **mutual_fund**: ticker matches `^[A-Z]{4}X$` (5 chars, ends in X) — the standard MF ticker convention
   - **etf**: ticker is in a maintained ETF list (the existing `ETFClassifier` in `data/black_diamond/scripts/gold/lib/etf_classifier.py` has this — it loads `bd-securities` DynamoDB. Borrow the lookup, not the regex fallback)
   - **single_stock**: product_category === 'Equity' and not mutual_fund and not etf
   - **other**: everything that doesn't fit (warn-log these so we can audit)

3. **Hybrid:** if Orion has `product_type` for *most* tickers but is null/empty for some, fall back to (2) only for the gaps. Flag the fall-back rate in the run log.

**Acceptance: classification should be >95% confident on the top 25 securities by total_position_value.** These are the ones the FE actually renders. Tail accuracy is less critical.

---

## 6. Aggregation logic (the new joins)

For each ticker in scope (`security_type` ∈ {single_stock, etf, mutual_fund}):

1. Sum `market_value` across all (account, ticker) rows in `gold/holdings/{latest}.parquet`, grouped by `household_id` after joining `silver/accounts_dim`. Filter household HHs with `aua > 0`.

2. **Top 25 securities** by `total_position_value`.

3. For each of those 25, the **top 10 holders**:
   - Compute `hh_concentration_pct = position_value / hh_aua` per (household, ticker)
   - Rank households for that ticker by `hh_concentration_pct` desc
   - Tie-break by `position_value` desc
   - Take top 10

4. Compute `total_firm_aua` once from the same holdings snapshot (sum of HH aua values) for the `pct_of_firm_aua` field.

---

## 7. Acceptance criteria

- [ ] `platinum/firm/firm_concentrations.json` publishes at the same cadence as the existing concentration_risk.json
- [ ] Schema matches §4 — TypeScript interface drops in cleanly on FE side
- [ ] `securities.length` ≤ 25 (and is the top by total_position_value, not arbitrary)
- [ ] Each security's `top_holders.length` ≤ 10
- [ ] `security_type` classification rate: ≥95% are `single_stock | etf | mutual_fund` on the top 25; `other` flagged in run log if >5%
- [ ] `pct_of_firm_aua` values sum to a plausible total (the top 25 might cover 50-80% of equity AUA; flag if >100% — that's a bug)
- [ ] At least one security has `holder_count > 1` (proves the aggregation is working across HHs)
- [ ] At least one HH appears in `top_holders` for multiple securities (concentrated HHs hit multiple top lists — that's expected)
- [ ] `household_id` values are Int64 matching the canonical key space (same as `cash_drag` shipment §3 confirmation)
- [ ] Spot-check the top security manually: pull holdings for that ticker, group by HH, verify the top 10 list matches your output for hh_concentration_pct ranking
- [ ] `comp-validate firm_concentrations` config entry (P1 follow-up — file the AM TO; not blocking)

---

## 8. Coordination notes

**FE work follows this brief.** Once the artifact lands, I'll rewrite the Concentration Risk lens chart and table:
- Top-level treemap consumes `securities[]` directly
- Click a tile → secondary view consumes that tile's `top_holders[]`
- Internal panel toggle filters `securities[]` by `security_type` client-side (no separate fetch needed — one artifact, one toggle)

**`household_id` contract** — must be the Orion Int64 matching the existing canonical key. Confirmed format from your 2026-05-12 cash_drag reply applies here equivalently.

**No back-fill needed.** Going forward from first publish.

---

## 9. Out of scope (don't expand the work)

- Window toggle — Concentration Risk is point-in-time (latest snapshot only). The FE Window toggle is already disabled when this lens is active.
- Time series / historical drift of concentrations — separate future ask if ever.
- Per-advisor top concentrations — exists at `platinum/advisors/{advisor_key}/top_holdings.json` already; not part of this firm-level lens.
- Mutual fund deep-classification (active vs index, equity vs bond MF, etc.) — single bucket is enough for the toggle.
- Single bond instruments (individual corporate/treasury bonds) and options inclusion — explicitly out of scope. Bond *funds* (fixed_income asset class) ARE in scope per the §4 correction.
- Cash / money market funds inclusion — out of scope.

---

## 10. Open question for DS

**Does Orion's `silver/assets_v2` have a native `product_type` / `instrument_type` field that distinguishes ETF, Single Stock, and Mutual Fund directly?**

This is the only branch point in the classification logic (§5). If yes → use it as the primary source. If no → fall back to ticker-pattern + ETFClassifier-lookup hybrid. Whichever you pick, document the choice in the run log so we can audit.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Companion to the Cash Drag account-level brief (`2026-05-12_cash_drag_account_level_DS_briefing.md`) which DS shipped as `be241a8ce` in a 35-min cycle.*
*Lineage investigated against: INF_D_07.concentration_risk.py, INF_D_02b top_holdings publisher, INF_D_03.composition_artifacts, silver/assets_v2, ETFClassifier (black_diamond/lib/).*
