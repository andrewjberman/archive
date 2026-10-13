# CARD-A P1: income rows in the Cottonwood transactions, and option C re-priced with a total-return field (2.0.0_SA_COO~Q1, 2026-10-13) -- CTO msg 4946; no draw

Read only (silver transactions via `lock._load_transactions`, the merged P1 builder on box/dell1 @9de742d8f9); no vendor call. Counts and CUSIPs only; no account data.

## Read 1: do the transactions carry the income rows across the CARD-A window?

**Yes.** 606 priced P1 names, 20,763 transaction rows. Income rows by `Transaction_Type`:

| kind | codes | rows | names |
|---|---|---|---|
| interest | `int`, `intx` | 5,577 | 539 |
| dividend | `dv`, `dvx` | 3,087 | 18 |
| dividend reinvested | `dvr`, `dvrx` | 2,490 | 10 |
| **all income** | | **11,154** | **556 of 606** |

- Every one of the 11,154 rows has a trade date and a non-zero `Amount`, and every one lies inside its name's own window.
- By year: 2013 88, 2014 186, 2015 298, 2016 441, 2017 501, 2018 644, 2019 1,382, 2020 1,151, 2021 638, 2022 646, 2023 1,181, 2024 1,589, 2025 1,702, 2026 707.
- By `Asset_Type`: Fixed Income 352 of 370 names have income rows, Cash Equivalent 199 of 227, Alternative Investment 5 of 9. 50 names have none (18 Fixed Income).
- **What the rows are:** the CLIENT's own received income (dates and amounts), not the security's published distribution schedule.

## Read 2: option C re-priced with a total-return field (at 2,673 cells a day)

Option C = flow dates plus month-ends, over the whole window (the earlier table: 30,858 cells for `PX_LAST`).

| fields | cells | days of quota |
|---|---|---|
| `PX_LAST` only (as priced before) | 30,858 | 12 |
| `PX_LAST` + `TOT_RETURN_INDEX_GROSS_DVDS` (the level, which makes a return between any two sampled dates) | 61,716 | 24 |
| option D (daily after 2026-04-22) with both fields | 70,580 | 27 |
| every trading day with both fields | 936,236 | 350 |

**Which field.** The porting test is built on `TOT_RETURN_INDEX_GROSS_DVDS` (a level). A level at sampled dates gives the return across any sampled interval; `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS` is a one-day return and does not
compose across a month-end gap. Two fields is the cost of making the series total-return at the same sampling.

## The cheaper reading, for the CTO to put to Andrew

The client's total-return needs the client's cash flows: price at the sampled dates plus the client's own income. The transactions carry those income rows for 556 of 606 names, so a TWR for the client can
use `PX_LAST` at option C (12 days) with the income rows from transactions. The vendor total-return field is needed where a SECURITY-level total return (against a benchmark or a peer) is the surface's
reading, not the client's. This is a choice about meaning, not a number; both prices are above.

## The 50 names with no income row in the window (CTO msg 4952), counted

By `Asset_Type`: **Cash Equivalent 28, Fixed Income 18, Alternative Investment 4.**

By the span each name is held inside its own window (calendar days, first to last day of the window): **90 days or fewer: 14; 91 to 183: 16; 184 to 365: 9; more than 365: 11.**
The 11 held longer than a year are all Fixed Income; the other 39 were held under a year and mostly under two coupon periods (median 2 transaction rows a name, only buys, sells and transfers).

Security master. No source I can read carries a coupon, a maturity or a zero-coupon flag: `gold/dimensions/assets_dim` holds ticker, name, market value and units only, and `silver/cot_holdings.parquet`
(the 2026-06-09 held snapshot) holds the asset name text and a `cash_equivalent` flag. Of the 50: **14 are in that snapshot** (all 14 carry the `cash_equivalent` flag; 1 has name text reading as a
bill, strip, zero or discount), and **36 are UNREAD**.

What this says: 30 of the 50 are held 183 days or less and 28 are cash equivalents, which is the pattern of no coupon in the window. The 11 held more than a year (Fixed Income, none in the
snapshot that I could confirm) are the ones where a paying security with no income row would make the income basis wrong; they need a zero-coupon / discount check against a master I have not found, or
the total-return field. Nothing here was drawn.
