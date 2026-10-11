# IRPT_YCDGEN round 8, cell YCD-c-8 -- census of the 257 sections of the retained report of the run of record

**By:** `2.0.0_SA_COO~G2`, 2026-10-11. Request `REQ-5e4149d2863aea31cc87d660`, tenant 49financial, provider `OPAL_ENGINE`, computation_validation `CERTIFIED`.
ONE served read (`GET .../analysis/{id}/sections`) on irpt-status revision 6, window 8, HTTP 200 at 07:13:59Z. The record
`SECTION_CENSUS_REQ_5e4149d2_REV6_20261011.json` (same folder) holds only counts: no value is kept and every digit in a reason is masked `#`.

## 1. Denominator and the split

Sections: **257**. Groups in the record (page x status x method x type x reason): 199.

| status | method | reason the page would state | sections |
|---|---|---|---|
| NOT_AVAILABLE | OPAL_HELD | `INPUT_MISSING:held_<input>` | 155 |
| NOT_AVAILABLE | BUILDER_ONLY | `NOT_IN_THIS_VERSION` | 65 |
| NOT_AVAILABLE | VENDOR_SOURCED | `NOT_IN_THIS_VERSION` | 22 |
| NOT_AVAILABLE | OWN_SERIES | `NOT_IN_THIS_VERSION` | 9 |
| VALUE | (a value) | `-` | 6 |
| | | **total** | **257** |

OPAL_HELD reason prefixes over its 155 sections: `INPUT_MISSING` 155. Distinct OPAL_HELD reasons (digits masked): 146.

## 2. By report page

| page | BUILDER_ONLY / NOT_IN_THIS_VERSION | OPAL_HELD / INPUT_MISSING | OWN_SERIES / NOT_IN_THIS_VERSION | VALUE | VENDOR_SOURCED / NOT_IN_THIS_VERSION | total |
|---|---|---|---|---|---|---|
| 1 | 5 |  |  |  |  | 5 |
| 2 | 6 | 9 | 2 | 3 | 7 | 27 |
| 3 | 3 | 20 |  |  | 3 | 26 |
| 4 |  | 62 |  |  |  | 62 |
| 5 | 4 | 29 |  |  | 1 | 34 |
| 6 | 3 | 17 | 1 |  | 2 | 23 |
| 7 | 3 |  | 6 |  | 6 | 15 |
| 8 | 2 | 17 |  |  | 3 | 22 |
| 9 | 7 |  |  |  |  | 7 |
| 10 | 2 |  |  |  |  | 2 |
| 11 | 2 |  |  |  |  | 2 |
| 12 | 4 | 1 |  |  |  | 5 |
| 13 | 6 |  |  |  |  | 6 |
| 14 | 6 |  |  |  |  | 6 |
| 15 | 2 |  |  |  |  | 2 |
| 16 | 2 |  |  |  |  | 2 |
| 17 | 1 |  |  |  |  | 1 |
| 18 | 2 |  |  |  |  | 2 |
| 19 | 1 |  |  |  |  | 1 |
| 20 | 1 |  |  |  |  | 1 |
| 21 | 1 |  |  |  |  | 1 |
| 22 | 1 |  |  |  |  | 1 |
| 23 | 1 |  |  |  |  | 1 |
| 24 |  |  |  | 3 |  | 3 |

## 3. The 6 sections that carry a value

| page | section_type | sections |
|---|---|---|
| 2 | number | 3 |
| 24 | table | 3 |

## 4. OPAL_HELD inputs named missing, by input family (first two tokens after `held_`)

| input family | sections |
|---|---|
| `held_region_exposure...` | 67 |
| `held_bond_maturity...` | 17 |
| `held_stock_sector...` | 14 |
| `held_stock_style...` | 9 |
| `held_bond_credit...` | 8 |
| `held_bond_sector...` | 7 |
| `held_market_cap...` | 6 |
| `held_weighted_avg...` | 5 |
| `held_asset_allocation...` | 4 |
| `held_distribution_yield...` | 2 |
| `held_net_expense...` | 2 |
| `held_alpha_#y...` | 1 |
| `held_beta_#y...` | 1 |
| `held_cash_net...` | 1 |
| `held_average_coupon...` | 1 |
| `held_average_price...` | 1 |
| `held_avg_credit...` | 1 |
| `held_current_yield...` | 1 |
| `held_dividend_yield...` | 1 |
| `held_effective_duration...` | 1 |
| `held_number_of...` | 1 |
| `held_of_bond...` | 1 |
| `held_of_stock...` | 1 |
| `held_yield_to...` | 1 |
| `held_level_series...` | 1 |

## 5. What this census does and does not show

- Every one of the OPAL_HELD unavailable sections states a reason of the form `INPUT_MISSING:held_<input>`: the page would say an input Opal
  is meant to hold was missing, not that Opal does not keep it. Whether that is the holdings of this request truly lacking those
  characteristics, or a read that returned nothing, is NOT established here; the census reads the report, not the reader.
- The `NOT_IN_THIS_VERSION` sections (BUILDER_ONLY, VENDOR_SOURCED, OWN_SERIES) state the same reason regardless of the request.
- One request, one report. It is the run of record; it says nothing about another portfolio.
- Not graded here: row D2-S39 (b) is `1.0.0_SA_CTO~DELL2`'s to rule on this table.
