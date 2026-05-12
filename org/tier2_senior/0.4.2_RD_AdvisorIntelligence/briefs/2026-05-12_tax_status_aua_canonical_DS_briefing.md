# DS Briefing — Canonical Tax-Status AUA fields for Inflection (panel-shape alignment)

**Recipient:** `0.4.0_DS_ClientPlatform~B`
**From:** `0.4.2_RD_AdvisorIntelligence`
**Pipeline:** Inflection partner / Advisor Intelligence
**Surface:** `Cost Basis & Tax Status` panel — rendered at N1 / L2 / L3 / L4 in the `/Books` tab
**Reference implementation:** 49 Financial — canonical layout renders today
**Status:** FE already removed Inflection-specific divergent blocks so the canonical 49F layout renders (portal commit forthcoming). Inflection's panel top section will be empty until this brief lands.

---

## 1. Summary

Emit three canonical fields per drill level for Inflection — `taxable_aua`, `tax_deferred_aua`, `tax_free_aua` (and their pct equivalents) — derived from Orion's `accounts_dim.reg_type`. These power the canonical 49F three-card layout in the Cost Basis & Tax Status panel.

Andrew's directive: same panel shape between Inflection and 49 Financial. The Realized/Unrealized + Billing Summary blocks Inflection has been carrying are being removed from this panel; once your data lands, the panel renders identically across both firms.

---

## 2. Current state

**49F (canonical):** at every drill level (firm / advisor book / client / account), the tax payload includes:
```json
{
  "taxable": 12500000,         "taxable_pct":     45.2,
  "tax_deferred": 8200000,     "tax_deferred_pct": 29.6,
  "tax_free": 6900000,         "tax_free_pct":    25.2,
  "capital_gains_ttm":  340000,
  "cost_basis_by_year": [...],
  "top_gain_positions": [...]
}
```

**Inflection (current):** emits `realized` / `unrealized` / `inflecBilling` instead, leaves the canonical 49F fields null/zero:
```json
{
  "taxable":      null,
  "tax_deferred": null,
  "tax_free":     null,
  "realized":     { account_count_with_tax, total_cost_basis, lt_cost_basis, st_cost_basis, total_gain_loss, lt_gain_loss, st_gain_loss },
  "unrealized":   { same shape },
  "inflecBilling": { total_fee_amount, weighted_avg_annual_fee_pct, fee_earning_aua, fee_earning_account_count, account_count_with_billing },
  "capital_gains_ttm":  ...,    // already emitted ✓
  "cost_basis_by_year": [...],  // already emitted ✓
  "top_gain_positions": [...]   // already emitted ✓
}
```

The canonical fields exist in the shared TypeScript interface but are nulled out for Inflection, so the FE's `totalTaxAua === 0` gate hides the entire top section of the panel (stacked bar + three cards). The Inflection-specific blocks were added to fill the gap. We're now reversing that — fill the canonical fields instead.

---

## 3. Required fields

For every drill level where the panel renders:

| Field | Type | Definition |
|-------|------|------------|
| `taxable`         | number | Sum of `market_value` across accounts whose `reg_type` classifies as **taxable** (see §4) |
| `taxable_pct`     | number | `taxable / (taxable + tax_deferred + tax_free) * 100`, two-decimal precision |
| `tax_deferred`    | number | Sum of `market_value` across accounts whose `reg_type` classifies as **tax-deferred** |
| `tax_deferred_pct`| number | `tax_deferred / (sum) * 100` |
| `tax_free`        | number | Sum of `market_value` across accounts whose `reg_type` classifies as **tax-free** |
| `tax_free_pct`    | number | `tax_free / (sum) * 100` |

Sum is over positions + cash within each tax-status bucket. `market_value` matches the canonical `aua` definition used elsewhere in the pipeline (positions + cash, latest snapshot or window-end as appropriate).

---

## 4. `reg_type` → tax_status classification

Orion's `accounts_dim.reg_type` is the source of truth. Standard mapping:

| reg_type values | tax_status |
|-----------------|------------|
| Roth IRA, Roth 401(k), Roth 403(b), Roth, HSA, Health Savings, 529, Coverdell, Education Savings | `tax_free` |
| Traditional IRA, Rollover IRA, SEP IRA, SIMPLE IRA, 401(k), 403(b), 457, Pension, Profit Sharing, Inherited IRA | `tax_deferred` |
| Joint, JTWROS, JTIC, Tenants in Common, Tenants by Entirety, Individual, Single, Custodial, UGMA, UTMA, Trust, Estate, Corporation, LLC, Partnership, Foundation | `taxable` |

**Open question:** what does Inflection's `accounts_dim.reg_type` actually contain? The DS~C reply on the cash_drag brief noted the empirical reg_type values are clean (e.g., `Roth - Kevin Cheng` style — combined reg_type + registration_name). I assume `reg_type` alone is the standalone classification field; confirm before coding the map.

**Fallback handling:** if `reg_type` is null/empty/unknown, classify as `taxable` (most conservative — assumes a non-qualified brokerage). Log the count of fallback classifications in the run output so we can audit. If fallback rate exceeds 5% of accounts, flag it as a data-quality issue rather than ship.

---

## 5. Where to populate

All four drill levels of the canonical book view emit this panel:

| Level | Artifact | Where to add fields |
|-------|----------|---------------------|
| N1 (firm)     | `platinum/firm/clients_tab.json` (or equivalent firm dashboard payload feeding the Books tab) | top-level `tax: {...}` object |
| L2 (advisor)  | `platinum/advisors/{advisor_key}/book.json` | `tax: {...}` object |
| L3 (client)   | `platinum/clients/{household_id}/client_detail.json` (or equivalent) | `tax: {...}` object |
| L4 (account)  | `platinum/accounts/{account_id}/account_summary.json` (if it has a tax block) | `tax: {...}` object |

Sum semantics at each level:
- **N1**: sum across all accounts at the firm
- **L2**: sum across all accounts under that advisor
- **L3**: sum across all accounts under that household
- **L4**: just the one account (single-bucket — only one of the three will be non-zero)

Pct values are computed within each level's scope (i.e., L2 pcts = bucket / advisor's total tax-aua, not bucket / firm's total).

---

## 6. Acceptance criteria

- [ ] All four drill levels emit non-null `taxable`, `tax_deferred`, `tax_free` (any may legitimately be 0 if the level has no accounts in that bucket; but no nulls)
- [ ] `taxable_pct + tax_deferred_pct + tax_free_pct === 100.0` (within rounding) for any non-empty payload
- [ ] `taxable + tax_deferred + tax_free` equals the level's total AUA (positions + cash). Spot-check at firm level — should be very close to `total_firm_aua` from `firm_concentrations.json`
- [ ] Reg_type classification spot-check: pick the firm-level breakdown, compare against a known reg_type sample. Roth-flagged HHs should land in tax_free; 401(k)-flagged in tax_deferred; Joint/Individual in taxable
- [ ] Fallback classification rate ≤ 5% of accounts (otherwise flag)
- [ ] No FE changes required to consume — the canonical 49F layout reads these fields directly from `CanonicalTax`

---

## 7. Coordination notes

**FE is shipping the layout cleanup in parallel.** The Inflection-specific `inflecBilling` and `realized` / `unrealized` blocks in `TaxCostBasisPanel.tsx` are being removed. Once you land the canonical fields, the panel renders identically to 49F at every level.

**Transition window:** between FE swap and your ship, the Inflection panel will show only `Capital Gains TTM`, `Cost Basis by Year`, and `Top Gain Positions` — the top section (stacked bar + three cards) will be empty. Andrew is OK with this — explicit decision to favor canonical-shape consistency over data continuity in the transition window.

**Billing data is not lost.** `inflecBilling` (total fee TTM, avg annual fee %, fee-earning AUA, fee-earning account count) is genuinely valuable info — Andrew will likely want it surfaced elsewhere (Books tab L2/L3 dashboard, dedicated billing panel, etc.). That's a follow-up product call, not part of this brief. Keep emitting the field; FE consumer will move, not delete.

**Realized/unrealized data:** same posture. Useful tax-loss harvesting context. Could anchor a future "Tax Optimization" lens. Keep emitting it; FE will route it somewhere appropriate when that surface exists.

---

## 8. Out of scope

- Don't touch `capital_gains_ttm`, `cost_basis_by_year`, or `top_gain_positions` — they already work for both firms
- Don't move or remove `realized` / `unrealized` / `inflecBilling` — they may have future consumers; just add the canonical fields alongside them
- No Window toggle work — this panel is point-in-time at the active drill level
- No L3 client-level reg_type override paths — if an HH has accounts of mixed reg_type, the L3 payload just sums them into the three buckets correctly

---

## 9. Open question for DS

What is the exact column name and value vocabulary in `silver/accounts_dim.reg_type` (or equivalent)? The mapping in §4 assumes standard Orion vocabulary, but Inflection may use a customized reg_type taxonomy. Send a quick `aws s3 cp` of a sample row from accounts_dim and I'll refine the mapping if needed.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Companion briefs in flight: cash_drag (`be241a8c`), firm_concentrations (`0fa96cd9`), distribution_tab_gaps (uncommitted/pending route).*
*FE divergence file: `portal/src/pages/AdvisorIntelligence/_shared/panels/TaxCostBasisPanel.tsx` lines 132-199 (Billing Summary + Realized/Unrealized blocks being removed).*
