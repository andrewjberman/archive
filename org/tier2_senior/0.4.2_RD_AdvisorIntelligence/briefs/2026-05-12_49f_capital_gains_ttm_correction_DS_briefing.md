# DS Briefing — 49 Financial `capital_gains_ttm` TTM-correction (BD pipeline)

**Recipient:** DS owner of BD (Black Diamond / 49F) pipeline — likely `0.4.0_DS_ClientPlatform` (base, or whichever suffix owns BD)
**From:** `0.4.2_RD_AdvisorIntelligence`
**Pipeline:** Black Diamond / 49 Financial / Advisor Intelligence
**Surface:** Cost Basis & Tax Status panel — `capital_gains_ttm` field at all drill levels
**Status:** Not urgent. Andrew flagged the parallel correction needed (`2026-05-12 SYNC #2`); explicitly deferred to a follow-up brief.

---

## 1. Summary

The `capital_gains_ttm` field emitted by the BD pipeline for 49 Financial is **labeled "TTM" but emits inception-cumulative numbers**. Same root issue DS~B just corrected for Inflection in `2e5539bac` — the input feed (`tax_unrealized` at account-grain) carries `date_range='Inception'` semantics; the TTM label has been a misnomer.

This brief requests applying the same TTM-locked correction pattern to BD that DS~B applied to INF, so the `capital_gains_ttm` field across both firms means the same thing.

## 2. Motivation

Andrew's verbatim direction (2026-05-12 SYNC #2):

> "Yeah i think this should be TTM-locked. easier to see and understand. honestly i think the same should be done with 49 but we'll get to that later."

"This" = the canonical interpretation of `capital_gains_ttm`. INF was corrected to:

> "12m delta in `account_performance.unrealized_gain`, summed per scope. NOT inception-cumulative."

49F's field is currently `nq_unreal_gain` style — accumulated since account inception, which can span years or decades. That's a useful number but it's not TTM. Users reading the panel header "Capital Gains (TTM)" expect a 12m window.

## 3. Required change

For the BD pipeline producing 49F's tax block at every drill level:

**Replace** the current `capital_gains_ttm` source (inception-cumulative `nq_unreal_gain` or equivalent) **with**:

```python
# pseudocode — mirror the INF pattern from 2e5539bac
latest_date = bd_account_performance['date'].max()
ttm_anchor  = closest_date_to(latest_date - timedelta(days=365))

unreal_now    = bd_account_performance[bd_account_performance['date'] == latest_date]
                  .groupby('account_id')['unrealized_gain'].sum()
unreal_anchor = bd_account_performance[bd_account_performance['date'] == ttm_anchor]
                  .groupby('account_id')['unrealized_gain'].sum()

capital_gains_ttm_per_account = (unreal_now - unreal_anchor).fillna(unreal_now)
# Then sum per scope: advisor / HH / firm
```

Edge case: accounts that didn't exist 12m ago — use the earliest observation in their history as the anchor (so partial-year accounts contribute their full delta, not get falsy-coalesced to the latest only).

## 4. Where to populate

Same drill levels as the INF emit (B0/B6 or whichever scripts produce these):

| Level | Artifact | Field path |
|-------|----------|------------|
| N1 (firm)    | `platinum/firm/clients_tab.json` (or BD equivalent)               | `summary.tax.capital_gains_ttm` |
| L2 (advisor) | `platinum/advisors/{advisor_key}/book.json`                       | `summary.tax.capital_gains_ttm` |
| L3 (client)  | `platinum/clients/{household_id}/client_detail.json`              | `summary.tax.capital_gains_ttm` |
| L4 (account) | account summary (if it has a tax block)                           | `summary.tax.capital_gains_ttm` |

## 5. Acceptance criteria

- [ ] `summary.tax.capital_gains_ttm` at every drill level equals "delta in cumulative unrealized gain over trailing 365 days" — NOT inception-cumulative
- [ ] Cross-firm parity: pick a comparable advisor at 49F and at Inflection; both `capital_gains_ttm` values should now mean the same thing (12m window) — interpretation no longer firm-dependent
- [ ] Field name unchanged (`capital_gains_ttm`) — no schema break; only the value computation changes
- [ ] Spot-check: known 49F advisor whose unrealized gain accumulated mostly pre-2024 (i.e., a long-tenured advisor). Old field would show large $; new field should show only the last 12m's incremental change. Confirm the diff makes sense.
- [ ] `nq_unreal_gain` (or whatever the existing source field is) can stay emitted as a sibling if other consumers depend on it — just don't expose it through the `capital_gains_ttm` slot.

## 6. Coordination notes

**Same compute pattern as DS~B's INF ship (`2e5539bac`)** — `account_performance.unrealized_gain` daily series, 365d delta, sum per scope. BD has the equivalent daily timeseries from Black Diamond's feed. Look at what DS~B did in `INF_D_02` and mirror in the BD equivalent script.

**`top_gain_positions` is already correct for 49F** — BD has real per-position cost_basis, so the existing emit is genuine "top positions by unrealized gain since inception/purchase." Leave that alone.

**`book_growth_ttm`** — 49F already has this (or close to it) via the existing book performance pipeline. Confirm but don't rebuild.

## 7. Out of scope

- `cost_basis_by_year` correction or restructure (already canonical at 49F)
- N1 firm-level `top_gain_positions` if it doesn't exist (separate ask if FE wants it)
- Changing the `nq_unreal_gain` source field — just reroute `capital_gains_ttm` to a new computation

## 8. Open questions

1. **Who owns the BD `capital_gains_ttm` emit currently?** I don't have visibility into BD-pipeline ownership — DS~B / DS~A / DS~D or other? Route this brief to whoever's responsible.
2. **Does 49F's `account_performance` equivalent have `unrealized_gain` per (account, date)?** If yes, this is mechanically identical to the INF fix. If no, the input source needs identification.

---

*Drafted by 0.4.2_RD_AdvisorIntelligence · 2026-05-12*
*Andrew's direction captured at SYNC #2 (DS~B inbox message, 2026-05-12 ~17:00Z): "honestly i think the same should be done with 49 but we'll get to that later."*
*Companion ship: `2e5539bac` (DS~B INF L2/L3 TTM-locked emit) — exact pattern to mirror.*
*Non-urgent — Andrew explicitly deferred. File for whenever the BD-pipeline owner has bandwidth.*
