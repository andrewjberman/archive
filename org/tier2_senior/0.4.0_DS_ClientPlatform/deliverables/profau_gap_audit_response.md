# ADVI_PROFAU.001 — DS Profile/Book Data-Gap Audit Response

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-04-13
**TO:** ADVI_PROFAU.001.ds-profile-book-data-gap-audit.md
**Status:** complete (pending AC validation)
**Framing:** "Ideally we can work with our existing tables and we already have all this information."

---

## Compiler Tools (Phase 1 + Phase 2)

| Phase | Tool | Command | Result |
|---|---|---|---|
| 1 | comp-pipescript | `comp-pipescript io D_00c` | D_00c reads 8 tables (FEE_RATE_HISTORY, ADVISOR_ASSIGNMENTS, ACCOUNT_TEAM, ACCOUNT_PERFORMANCE, CLIENT_DIMENSION, CANONICAL_NNA, ADVISOR_FEE_DETAIL, REL_ARCHITECT); writes EMPLOYEE_LEADERBOARD only |
| 1 | comp-pipescript | `comp-pipescript io D_04` | D_04 reads 20 inputs including EMPLOYEE_LEADERBOARD (from D_00c), client_detail_key, advisor_book_key; writes 21 platinum terminal outputs |
| 1 | comp-trace | `comp-trace employee_leaderboard --direction both --all` | D_00c -> gold/artifacts/employee_leaderboard.json -> D_04 -> platinum/firm/leaderboard.json. No further downstream (terminal). |
| 1 | comp-transform | `comp-transform schema-check AdvisorBookView` | PlatinumAdvisorSummary: 19 declared / 3 rendered / 13 UNUSED. PlatinumClientSummary: 13 declared / 5 rendered / 6 UNUSED. PlatinumAccountSummary: 6 declared / 3 rendered / 1 UNUSED. |
| 1 | comp-transform | `comp-transform schema-check AdvisorPublicProfile` | AdvisorDrilldownSummary: 13 declared / 1 rendered / 12 UNUSED. SCHEMA MISMATCH: timeseriesResp rendered but not declared on type. |
| 2 | Grep | `cost_basis_by_year|top_gain_positions|capital_gains_ttm in gold/` | Present in D_00 (per-client) and D_02 (per-account/per-client). D_04 line 1959 emits `capital_gains_ttm` only in CLIENT summary. NOT present in advisor summary builder (D_04 line 491-521). |
| 2 | Grep | `is_fee_paying in gold/` | Exists only in D_00c (W6-005 split-weighted leaderboard path). Zero matches in D_02. AdvisorClient type has no is_fee_paying field. |
| 2 | Grep | `fee_summary in gold/` | D_02 line 778: `_build_fee_summary_by_role` for L2 book.json. D_02 line 811: `_build_fee_summary_by_account` for L3 client_detail.json. D_04 lines 516+687 pass both through to platinum. |
| 2 | Grep | `total_market_value in gold/` | C_05 line 242: emitted in holdings_lots. D_04 line 888: emitted in `platinum/accounts/{*}/summary.json`. LIVE. |
| 2 | Grep | `fee_earning_aua in D_02` | D_02 lines 960-989: `fee_earning_mask = total_split_pct > 0` (no billability gate). Emitted at line 1085. |
| 2 | Read | D_04 lines 491-521 (advisor summary builder) | Confirms advisor summary emits `book.{ fee_earning_aua, non_fee_earning_aua, tagged_aua, fee_earning_account_count, non_fee_earning_account_count, implied_annual_revenue, avg_fee_bps_earned }` + top-level `role_breakdown`. None declared on PlatinumAdvisorSummary.book. |
| 2 | Read | types.ts 1837-1865 (PlatinumAdvisorSummary) | Declares `book: { book_name, client_count, account_count, total_aua, nna_qtd/ytd/mtd, growth, clients }` — MISSING fee/tagged AUA fields and role_breakdown. |
| 2 | Read | api/endpoints/advisor-intelligence.ts 711-734 | `getPlatinumAdvisorDrilldownSummary` reads `platinum/advisors/{id}/summary.json`, flattens `book.*` fields. `fee_earning_aua: book.fee_earning_aua` — sourced from D_02 (total_split_pct > 0 filter). |

---

## Q1 — L2 book-level capital-gains / cost-basis aggregates

**Label: COLUMN-ADD**

**Gap:** `TaxCostBasisPanel` supports `capitalGainsTtm`, `costBasisByYear[]`, `topGainPositions[]`. At L3 (per-client), all three render from `clientDetail.tax.*` (LIVE). At L2 (advisor/book), `AdvisorBookView` lines 259-266 pass only the 3-bucket taxable/tax_deferred/tax_free split — `capital_gains_ttm`, `cost_basis_by_year`, and `top_gain_positions` are NULL-AT-LEVEL.

**Evidence (absence at book level):**
- D_04 advisor summary builder (lines 491-521): `'tax_exposure': book.get('tax_exposure', {})` — D_02's book.json `tax_exposure` carries only the 3-bucket split. D_04 does NOT aggregate per-client cost-basis fields at the book level.
- D_04 line 1959 (`'capital_gains_ttm': tax_full.get('capital_gains_ttm', 0)`) is in the CLIENT summary builder (~line 1920), not the advisor summary builder.
- Grep: `cost_basis_by_year` + `top_gain_positions` found only in D_00 (per-client) and D_02 (per-account detail). No occurrence in any advisor-level aggregation path.

**Data exists upstream:**
- D_02 builds per-client `cost_basis_by_year` (lines 1529-1542), `top_gain_positions` (lines 1561-1575), `capital_gains_ttm` (line 1623) in `gold/entities/clients/{*}/detail.json`.
- D_04 reads `client_detail_key` (gold/entities/clients/{*}/detail.json) already in its read set.

**Canonical source recommendation:**
- Insert in D_04's advisor summary builder (lines ~415-523). Loop over `client_detail_key` files for all clients in the advisor's book. Aggregate: sum `capital_gains_ttm` across clients; reduce `cost_basis_by_year` grouping by year (sum `cost_basis + market_value + unrealized_gain`); merge and top-N `top_gain_positions` across all clients.
- Alternative: insert in D_02's advisor book.json builder (it already processes all clients). Either is valid; D_04 is cleaner if D_04 already has the client detail handles loaded.
- Output field: add `capital_gains_ttm`, `cost_basis_by_year`, `top_gain_positions` to `platinum/advisors/{id}/summary.json → tax_exposure`. Update `AdvisorTaxExposure` type.
- Then AdvisorBookView L259-266 needs to pass these to TaxCostBasisPanel (DE).

**Follow-up TO granularity:** Multi-script work (D_04 aggregation loop + type update + DE wiring). Recommend one DS TO (D_04 book-level tax aggregate) + one DE TO (TaxCostBasisPanel wiring at L2).

---

## Q2 — Per-client `is_fee_paying` flag on `AdvisorClient`

**Label: COLUMN-ADD**

**Gap:** L2 header needs `Clients: X fee-paying / Y non-fee-paying / Z total`. `bookData.book.clients` entries carry only `{ client_key, client_name, aua }` — no fee status. D_04 passes through `book.get('clients', [])` (line 511) from D_02's book.json unmodified. D_02 builds the clients list but does not compute per-client fee status.

**Evidence (absence):**
- `AdvisorClient` type (types.ts 1015-1019): `{ client_key, client_name, aua }` — no `is_fee_paying` field.
- Grep `is_fee_paying` in `data/black_diamond/scripts/gold/D_02*`: zero matches. `_is_fee_paying` exists only in D_00c (leaderboard path).
- `AdvisorBookResponse.clients` (types.ts 1044): `AdvisorClient[]` — same type, no fee flag.

**Data exists upstream:**
- D_02 loads `fee_rate_history` (grep line 394: "fee_rate_history not available → fee_summary will be null" warning proves it's loaded).
- Per-client `is_fee_paying` = "does this client (relationship_id) have at least one account with `is_billable = True AND split_pct > 0` for this advisor?" — derivable from D_02's existing `fee_rate_history` + `advisor_assignments_history` reads.

**Canonical source recommendation:**
- Chain insertion: D_02 when building the `clients` list in `book.json`. For each client (relationship), check if any of its accounts satisfies `is_billable AND split_pct > 0` for this advisor. Emit `is_fee_paying: bool` on each client entry.
- Downstream: D_04 passthrough (no change needed). DE adds count logic at L2 header using `book.clients.filter(c => c.is_fee_paying).length`.
- Update `AdvisorClient` type to add `is_fee_paying: boolean`.

**Follow-up TO granularity:** One-liner-ish column add in D_02 (join per-client to fee_rate_history/assignments + add bool flag). DE type update + count render is also small.

---

## Q3 — Reconcile `fee_earning_aua` / `non_fee_earning_aua` / `tagged_aua`

**Label: COLUMN-ADD** (definition alignment, not new data)

**Gap:** `AdvisorDrilldownSummary` declares `fee_earning_aua`, `non_fee_earning_aua`, `tagged_aua`. Post-W6-002 allChecked fix, the leaderboard computes fee-paying AUA via the D_00c split-allocated path (`billable AND split_pct > 0`). The question: do these reconcile?

**Analysis — they do NOT reconcile today:**
- `fee_earning_aua` in the drilldown summary: sourced from `getPlatinumAdvisorDrilldownSummary` (api.ts line 730) → `book.fee_earning_aua` → D_04 line 503 → D_02 lines 960-989.
- D_02 line 960: `fee_earning_mask = total_split_pct > 0`. No `is_billable` gate.
- D_00c W6-005: `_is_fee_paying = billable AND split_pct > 0`. For Travis: $340.5M.
- D_02's `total_split_pct > 0` includes non-billable accounts with split allocations → overstates. Travis likely shows ~$398M (matches the pre-W6-005 bug).
- `sum(role_breakdown[role].fee_paying.aua)` from the leaderboard: $340.5M (exact match to billing canonical, verified all 152 QTD advisors).
- `tagged_aua`: sourced from D_02 `book_summary.tagged_aua` — total AUA across all roles, fee-agnostic. This is correct.

**Canonical source recommendation:**
- Fix D_02 line 960: change `fee_earning_mask = total_split_pct > 0` to `fee_earning_mask = (total_split_pct > 0) & (is_billable == True)`. This aligns D_02's `fee_earning_aua` to the W6-005 canonical definition.
- After this fix, `fee_earning_aua` in the drilldown summary will match `sum(role.fee_paying.aua)` from the leaderboard within the same per-advisor tolerance ($0.02 verified via the post-hoc scale factor in D_00c).
- Note: the D_00c post-hoc scale factor exists precisely to handle PIT vs is_current drift in assignments. The same drift applies here, so residual differences of <$1 are expected and acceptable.
- If D_02 fix is deferred: the drilldown summary should read `fee_earning_aua` from the leaderboard's per-advisor `fee_breakdown.fee_paying.aua` rather than from the advisor summary. This requires a change in `getPlatinumAdvisorDrilldownSummary` to join to the leaderboard artifact.

**Follow-up TO granularity:** One-liner filter change in D_02 (line 960) + full incremental gold run. Low risk.

---

## Q4 — `PlatinumClientSummary.fee_summary: FeeSummaryByAccount`

**Label: EXISTS-UPSTREAM**

**Gap (frontend-only):** `fee_summary` is declared on `PlatinumClientSummary` (types.ts 1881) and listed as UNUSED by comp-transform in `AdvisorBookClientDetail.tsx` (L3).

**Evidence (data is LIVE):**
- D_02 line 811-813: `_build_fee_summary_by_account(fee_rates, acct_snap, rel_id)` — builds per-account fee bps + implied revenue per account in the relationship. Emitted at line 1768: `'fee_summary': _build_fee_summary_by_account(...)`.
- D_04 line 687: `'fee_summary': detail.get('fee_summary')` — passes D_02's `fee_summary` through to `platinum/clients/{*}/summary.json`.
- Type is declared, data is emitted, endpoint serves it. No DS action required.

**Data source:** `A_02 (fee_rate_history.parquet)` → D_02 `_build_fee_summary_by_account` → `gold/entities/clients/{*}/detail.json → fee_summary.by_account[]{account_id, fee_bps, implied_revenue}` → D_04 passthrough → `platinum/clients/{*}/summary.json → fee_summary`.

**Canonical source:** `platinum/clients/{*}/summary.json → fee_summary` (already populated by D_04). Nothing to do on DS side.

**Follow-up TO granularity:** DE one-liner — render `clientSummary.fee_summary` at L3 (e.g. per-account bps display in ConsolidatedOverviewPanel or a new fee row in ClientsTable). No DS TO needed.

---

## Q5 — `PlatinumAccountSummary.total_market_value`

**Label: EXISTS-UPSTREAM**

**Gap (frontend-only):** `PlatinumAccountSummary.total_market_value` (comp-transform: UNUSED at L4 in `AdvisorBookAccountDetail.tsx`).

**Evidence (data is LIVE):**
- C_05 line 242: `total_market_value=('market_value', 'sum')` — aggregated from holdings_lots per account.
- D_04 line 888: `'total_market_value': round(total_mv, 2)` — emitted in `platinum/accounts/{*}/summary.json`.
- Type `PlatinumAccountSummary` declares `total_market_value: number`. Data is populated.

**Canonical source:** `platinum/accounts/{acct_id}/summary.json → total_market_value` (C_05 → D_04 path, already live). No DS action required.

**Follow-up TO granularity:** DE one-liner — render `accountSummary.total_market_value` at L4 (e.g. balance/market value header in `AdvisorBookAccountDetail`). No DS TO needed.

---

## Q6 — Type drift on `PlatinumAdvisorSummary`

**Label: EXISTS-UPSTREAM**

**Gap:** `PlatinumAdvisorSummary` (types.ts 1837-1865) declared shape does not match what D_04 actually emits at `platinum/advisors/{id}/summary.json`. The actual emit is a superset of the declared type.

**Evidence:**
- D_04 advisor summary builder (lines 491-521) emits: `{ generated_at, data_as_of, advisor_id, book: { book_name, client_count, account_count, fee_earning_account_count, non_fee_earning_account_count, total_aua, tagged_aua, fee_earning_aua, non_fee_earning_aua, implied_annual_revenue, avg_fee_bps_earned, nna_qtd, nna_ytd, nna_mtd, growth, clients }, mix, mix_periods, concentration, fee_summary, tax_exposure, active_since, role_breakdown }`
- `PlatinumAdvisorSummary.book` (types.ts 1841-1851) declares only: `{ book_name, client_count, account_count, total_aua, nna_qtd, nna_ytd, nna_mtd, growth, clients }`.
- **Missing from the declared type's `book` block:** `fee_earning_account_count`, `non_fee_earning_account_count`, `tagged_aua`, `fee_earning_aua`, `non_fee_earning_aua`, `implied_annual_revenue`, `avg_fee_bps_earned`.
- **Missing from the top level:** `role_breakdown` (D_04 emits it at the top level via line 520; not declared on `PlatinumAdvisorSummary`).
- comp-transform schema-check confirms: 3 rendered fields, 13 UNUSED on declared type. "All rendered fields match their response types" — fields accessed via `bookData.book.*` path do hit the JSON correctly, but the type contract is incomplete.

**Why this matters now:** `getPlatinumAdvisorDrilldownSummary` (api.ts 711-734) correctly reads `raw.book.fee_earning_aua`, `raw.book.tagged_aua`, `raw.role_breakdown` — all of which are LIVE in the JSON — but TypeScript sees `raw` as `Record<string, unknown>` (untyped) because `PlatinumAdvisorSummary` doesn't declare them. This suppresses type-check coverage on the entire drilldown summary flatten.

**Canonical source:** D_04 lines 491-521 is authoritative. No data changes needed; this is a type-declaration gap.

**Follow-up TO granularity:** DE type-only fix — update `PlatinumAdvisorSummary.book` to add the 7 missing `book.*` fields + add `role_breakdown: Record<string, { aua: number; pct_of_tagged: number; ... }>` at the top level. Also tighten `getPlatinumAdvisorDrilldownSummary`'s input type from `Record<string, unknown>` to `PlatinumAdvisorSummary` once the type is complete. Zero gold-script changes needed.

**Note on role_breakdown fee_paying sub-objects:** `platinum/advisors/{id}/summary.json → role_breakdown` comes from D_02's book.json `role_breakdown` (D_04 line 520: `book.get('role_breakdown', {})`). D_02's role_breakdown does NOT have `fee_paying` sub-objects — those only exist in `platinum/firm/leaderboard.json` (D_00c). If AdvisorPublicProfile ever needs per-role fee AUA, it would need to read from the leaderboard entry (separate artifact) or D_02 would need to add the fee_paying sub-objects. This is distinct from the type-fix and would be its own TO.

---

## Q7 — `fee_earning_aua` vs `sum(role.fee_paying.aua)` canonical-source pick

**Label: COLUMN-ADD** (governance + D_02 filter fix)

**The governance question:** After D_00c's 3-case split-allocation rule (W6-005, already shipped as of 2026-04-13 commit `0804b377`), which field is canonical for the advisor-profile fee-AUA headline — `fee_earning_aua` from the advisor summary or `sum(role_breakdown[role].fee_paying.aua)` from the leaderboard?

**Answer: `sum(role_breakdown[role].fee_paying.aua)` from the leaderboard is the canonical.**

Reasoning:
1. W6-005 validation: all 152 QTD advisors show `sum(role.fee_paying.aua) == fee_breakdown.fee_paying.aua` within $0.02. This is exact alignment to the billing system.
2. D_00c filter: `_is_fee_paying = billable AND split_pct > 0` — matches C_08's fee definition.
3. D_02 `fee_earning_aua` filter: `total_split_pct > 0` (line 960) — no billability gate. Overstates by the set of non-billable accounts with split allocations (the ~$57.6M gap identified in W6-005 investigation for Travis).

**In-flight dependency:** W6-005 IS shipped (D_00c commit `0804b377`, D_04 `platinum/firm/leaderboard.json` verified 18:14:13 UTC 2026-04-13). The leaderboard source is canonical today.

**Recommended fix for D_02:** Update `fee_earning_mask` at D_02 line 960:
```python
# Current (looser, overstates):
fee_earning_mask = snap_latest['total_split_pct'] > 0

# Canonical (matches C_08 + D_00c W6-005):
fee_earning_mask = (snap_latest['total_split_pct'] > 0) & (snap_latest['is_billable'] == True)
```
After this fix, `fee_earning_aua` in `platinum/advisors/{id}/summary.json → book.fee_earning_aua` becomes canonical and consistent with the leaderboard sum.

**Deprecation question — should the non-canonical be removed?**
- If D_02 is fixed: both sources converge. Neither needs to be deprecated; they serve different granularity levels (book-level total vs role-attributed breakdown).
- If D_02 fix is deferred: the advisor-profile headline MUST read from the leaderboard, not from the advisor summary. `AdvisorDrilldownSummary.fee_earning_aua` would be deprecated or flagged as stale until D_02 is updated.

**Platinum surface audit for non-canonical `fee_earning_aua` occurrences:**
- `platinum/advisors/{id}/summary.json → book.fee_earning_aua` (D_04 pass of D_02 value) — stale until D_02 fix
- `AdvisorDrilldownSummary.fee_earning_aua` (api.ts line 730) — reads from the stale source
- `platinum/firm/leaderboard.json → [advisor].fee_breakdown.fee_paying.aua` — this IS canonical (D_00c W6-005)
- `platinum/firm/leaderboard.json → [advisor].role_breakdown[role].fee_paying.aua` — this IS canonical (D_00c W6-005)
- No other platinum surfaces expose `fee_earning_aua` directly.

**Follow-up TO granularity:** One-liner filter change in D_02 (line 960) + incremental gold run scoped to D_02+D_04. Low risk. Recommend ADVI_PROFAU.002 for this fix.

---

## Summary — Label Table

| Gap | Label | Data exists in | DS action | DE action | Granularity |
|---|---|---|---|---|---|
| Q1 — L2 capital gains / cost basis aggregates | **COLUMN-ADD** | D_02 per-client (detail.json) | D_04 aggregation loop across clients + emit in tax_exposure | Wire `capitalGainsTtm`, `costBasisByYear`, `topGainPositions` from advisor summary to TaxCostBasisPanel | Multi-script (DS D_04 loop + DE wiring) |
| Q2 — Per-client `is_fee_paying` flag | **COLUMN-ADD** | A_02 fee_rate_history + D_02 loads it | D_02: add `is_fee_paying` bool per client in book.clients, using `is_billable AND split_pct > 0` | Add `is_fee_paying` to `AdvisorClient` type; render count split at L2 header | D_02 one-liner + DE type + render |
| Q3 — fee_earning_aua reconciliation | **COLUMN-ADD** | A_02 (is_billable) already read by D_02 | D_02 line 960: add `is_billable` gate to `fee_earning_mask` | None (type already declared) | D_02 one-liner + full D_02+D_04 run |
| Q4 — PlatinumClientSummary.fee_summary | **EXISTS-UPSTREAM** | platinum/clients/{*}/summary.json (LIVE) | None | Render `clientSummary.fee_summary` at L3 | DE one-liner |
| Q5 — PlatinumAccountSummary.total_market_value | **EXISTS-UPSTREAM** | platinum/accounts/{*}/summary.json (LIVE) | None | Render `accountSummary.total_market_value` at L4 | DE one-liner |
| Q6 — PlatinumAdvisorSummary type drift | **EXISTS-UPSTREAM** | platinum/advisors/{*}/summary.json (LIVE, D_04 emits full shape) | None — all fields already emitted by D_04 | Update `PlatinumAdvisorSummary.book` to add 7 missing fee/tagged fields; add `role_breakdown` at top level | DE type-only fix |
| Q7 — Canonical fee_earning_aua pick | **COLUMN-ADD** | D_00c W6-005 leaderboard (canonical); D_02 fix needed | D_02 line 960 filter fix (`total_split_pct > 0 AND is_billable`) | None (once D_02 fixed, `fee_earning_aua` on AdvisorDrilldownSummary becomes canonical) | D_02 one-liner + run |

---

## ADVI_PROFAU.002+ TO Roadmap

| TO | Assignee | Scope | Effort |
|---|---|---|---|
| ADVI_PROFAU.002.ds-d02-fee-mask-alignment | DS | D_02 line 960: `is_billable AND split_pct > 0` filter fix. Covers Q2 (partial, same filter) + Q3 + Q7. | 1 gold run after commit |
| ADVI_PROFAU.003.ds-d04-book-level-tax-aggregates | DS | D_04 advisor summary: aggregate `capital_gains_ttm`, `cost_basis_by_year`, `top_gain_positions` from per-client client_detail.json across all clients in book. Covers Q1. | Multi-script, full D_04 run |
| ADVI_PROFAU.004.de-type-fix-platinum-advisor-summary | DE | Update `PlatinumAdvisorSummary.book` declared fields + add `role_breakdown`. Covers Q6. | Type-only, no gold |
| ADVI_PROFAU.005.de-wire-fee-counts-and-fee-summary | DE | (a) Add `is_fee_paying: boolean` to `AdvisorClient` type; (b) render Q2 count split at L2 header; (c) render Q4 `fee_summary` at L3; (d) render Q5 `total_market_value` at L4. | Frontend only, 4 one-liners |

---

## Do-Not Rules (from this audit)

- Do NOT read `book.fee_earning_aua` from the advisor summary as canonical until ADVI_PROFAU.002 D_02 fix lands. Use the leaderboard `fee_breakdown.fee_paying.aua` for any canonical fee-AUA display in the meantime.
- Do NOT aggregate `cost_basis_by_year` by simply summing rows across clients without grouping by `purchase_year` — years must be merged, not concatenated.
- Do NOT add `role_breakdown[role].fee_paying.*` to D_02's `book.role_breakdown` without a separate DS TO — that requires the full D_00c-style split_pct-weighted computation at the per-advisor-book level.
