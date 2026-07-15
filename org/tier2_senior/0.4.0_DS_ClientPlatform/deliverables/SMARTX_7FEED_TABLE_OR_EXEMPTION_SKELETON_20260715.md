# SMARTX PART-2: 7-FEED TABLE-OR-EXEMPTION SKELETON
## The bronze feeds with NO planned silver shape -- for CTO's parity/exemption ruling

**Filed by:** 0.4.0_DS_ClientPlatform, 2026-07-15 ~15:2xZ. **For:** CTO family ruling (each unplanned
feed gets a `fact_{type}` table OR a recorded exemption -- Andrew's full bronze/silver parity bar).
**0.5.0 builds AFTER the ruling** (nothing of theirs blocks on this today). **Follows:** parts 1 + 1b.

### Grounding
- Denominators: live recursive census of `s3://opal-data-assets/smartx/` @ 2026-07-15 ~14:4xZ.
- Shapes: one live `boto3 get_object` per feed (payload structure + grain), read ~15:2xZ.
- This is a table-OR-exemption RECOMMENDATION per feed (shape + rationale), NOT a pinned row-expectation
  report -- those follow per-table when 0.5.0 schedules a build (as parts 1/1b did).

### CADENCE NOTE (NEVER call these stale -- resolve cadence first)
Three feeds have their latest partition on **20260714**, not 20260715, at census time:
`account/allocations`, `account/detail`, `platform/nonzerosleeve`. The model/platform feeds fired
09:3x-09:4x ET today; the account-scope sweep + nonzerosleeve did NOT land a 20260715 partition yet.
**This is a cadence fact, not a staleness finding** -- confirm each feed's schedule before treating a
missing 20260715 as anything. Denominators below are the latest LANDED partition.

---

### RECOMMENDATIONS (6 FACT candidates + 1 EXEMPTION)

| # | feed | denom (latest) | grain | key fields | recommendation |
|---|---|---|---|---|---|
| 1 | `account/{uuid}/bronze/allocations` (sweep) | 7,066 (07-14) | per-account list of its allocations | account, advisor, id, leverage, tradingType, isApmAllocation, matchModelLeverage, status, type, openTimestamp | **FACT** `fact_account_allocation` |
| 2 | `account/{uuid}/bronze/detail` | 91 (07-14) | one envelope/account | **brokerageAccountNumber**, custodian{id,name}, repCode, accountType, enterprise, targetWeightId, status, feature[~10] | **FACT** `fact_account_detail` |
| 3 | `model/{rmid}/bronze/holdings` | 11 (07-15) | per-model list of holdings | symbol, quantity, price, marketValue, multiplier, percentOfPortfolio | **FACT** `fact_model_holdings` |
| 4 | `model/{rmid}/bronze/performance` | 11 (07-15) | per-model perf series (nested) | model{id,name}, performance{grouping, range, recordCount, performance[]} | **FACT** `fact_model_performance` |
| 5 | `model/{rmid}/bronze/changerequests` | 11 (07-15) | per-model list of trade requests | activity, ticker, company, from, to, percentage, quantity, price, requestedBy, tradeTimestamp | **FACT** `fact_model_changerequests` |
| 6 | `platform/bronze/nonzerosleeve` | 1 obj / 511 recs (07-14) | list of account-sleeve money rows | **brokerageAcctNum**, accountId, allocationId, opening/closing {equity,cash,dividend,fee,interest}, long/shortPositionCount, enterpriseId | **FACT** `fact_nonzerosleeve` |
| 7 | `platform/bronze/access_roster` | 1 (07-15) | one access-control envelope | accountAccess, modelAccess, enterpriseAccess, permissions, targetWeightGroupAccess (mostly empty lists) | **EXEMPTION** (access-control meta) |

### RATIONALE + the two things that raise the stakes

**Why 6 are FACT candidates (not exemptions):** each carries real measures or identity NOT derivable from
the 5 planned tables -- model composition (3), a model perf series (4), a rebalance event log (5), and
two IDENTITY/MONEY carriers (2, 6). Exempting any of these would drop client-relevant data, which the
full-parity bar forbids.

**THE TWO HIGH-STAKES CARRIERS -- the custody join keys live here, nowhere else in smartx silver:**
- **(2) `account/detail` carries `brokerageAccountNumber`** + custodian + repCode. This is THE account
  identity that joins smartx to custody (Schwab/gold). BYTE-FAITHFUL string -- a leading zero lost here is
  a failed gold join. Only 91 accounts, but they are the identity spine.
- **(6) `nonzerosleeve` carries `brokerageAcctNum`** + the opening/closing money leg (equity/cash/
  dividend/fee/interest) at sleeve grain. The inventory's "money-leg + 2nd identity carrier" -- it
  corroborates (2) and adds the money. Exempting it drops a money leg.
Recommend both FACT, both with the account-number byte-faithful discipline (Rule 17), so gold has the
custody join covered.

**Why (7) `access_roster` is an EXEMPTION:** it is platform access-control / permissions config
(who-can-see-what), not client financial data -- no AUM, holdings, positions, or money. Nested handling
(feature[] in (2), performance[] in (4)) is a per-table nested-grain question -- either a child fact table
or a preserved JSON column (Rule 17: preserve, never slim), CTO to rule per table.

**Also exempt by construction:** `meta/pulls/*manifest.json` (16 objects) -- producer manifests, not data.

### OPEN (CTO to rule)
- Confirm 6 FACT / 1 EXEMPTION split, or reclassify.
- Per-table nested-grain handling for (2) feature[] and (4) performance[] (child table vs JSON column).
- Whether (1) `fact_account_allocation` overlaps/merges with the existing `fact_allocation_account_map`
  (feed-9) or stays distinct (it carries trading config the map does not).
- Cadence confirmation for the 3 20260714-latest feeds before any freshness treatment.
- Pinned per-table row-expectation reports follow, per feed, when 0.5.0 schedules the build.
