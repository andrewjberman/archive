# MDPF_DEMQUE: the two-week Bloomberg total by surface, before the first new draw (2.0.0_SA_COO~Q1, 2026-10-13) -- for CTO msg 5165

Window: 2026-10-14 to 2026-10-27. **The draw hold lifted (CTO msg 5165), but the drawer cannot draw most of this yet: see "What the drawer can draw today".**
Every figure is tagged **measured** (read from a file or a run), **inferred** (arithmetic on measured figures) or **UNMEASURED** (needs a figure only site Z holds).

## 1. Capacity: backfill history cells in the window

| item | cells | claim |
|---|---|---|
| History ceiling per drawer fire (`bbg_allowance.json` `history.ceiling`) | 5,858 | measured (a completed ledger day, no limit hit) |
| Fires in the window (`standing_drawer.py --schedule`): Sat 10-17, Sun 10-18, Sat 10-24, Sun 10-25 | 4 | measured (the schedule) |
| **At the day rate, no carry-over (what the dell1 quote counts)** | **23,432** | inferred (4 x 5,858) |
| Carry-over events: the two Saturday fires carry the trading days before them (10-12 to 10-16 and 10-19 to 10-23); the Sunday fires carry none | 2 events, at most 5 x 5,858 each | inferred |
| Carry-over upper bound (production leaves its whole trading-day allowance unused) | 58,580 | inferred bound |
| **Carry-over actually available** | **UNMEASURED** | production's spend per trading day sits in the site Z `bbg_budget` ledger only; the drawer reads it at run time (t-54) and prints it in each receipt |
| **Capacity with the expansion** | **between 23,432 and 82,012** | the true figure is unknown until the 10-17 receipt |
| Surface E reserve held back from it (10 percent of each fire's ceiling, released if unused) | 2,340 | inferred (4 x 585) |

## 2. Demand by surface, in the order A, B, E, C, D

| surface | request | cells | claim |
|---|---|---|---|
| **A** production daily | A1 to A5 pulls | on production's own trading-day allowance, not in the backfill capacity | n/a; A4's added total-return field is about +500 a day, forward only |
| **B** client history | B1 Cottonwood option C (613 CUSIPs; the 8 rejected funds joined; ABNFX held back as P2) | 37,439 | measured (`bbg_quote.py --quote`) |
| B | fund-type check, 227 cash equivalents x `FUND_TYP` (reference channel) | 227 | measured |
| B | porting test, 326 securities x 5 intervals | 3,195 | measured |
| **E** Opal ad-hoc | reserve, not a request | 2,340 (above) | inferred |
| **C** product history | C1 rival funds: field-matched, staged 30 then 90 then 365 days, 213,149 total | stage 1 (30 days) about 17,500; stage 2 (to 90) about 35,000; stage 3 (to 365) about 160,600 | **inferred only**: the form states the total, not the stages; these assume cells are linear in days |
| **D** research | D1 TR remainder 1,004 + D2 ABNB 989 + D3 ICT 1 + D4 scanner slice 1 50 | 2,044 | measured |
| D | D5 full scanner list, only if slice 1 reads non-USD | 1,038 | measured; conditional, not counted |

**Two-week demand if C1 stage 1 is included: about 40,861 (B) + 17,500 (C1 stage 1) + 2,044 (D) = about 60,400 cells, plus the 2,340 surface E reserve = about 62,700.**

## 3. Does it fit?

- **At the day rate alone: no.** 62,700 against 23,432. B1 on its own is 37,439, so even surface B does not finish in two weeks without the expansion; the quote's own finish for B1 is 2026-11-07.
- **With the expansion: only if production leaves at least about 39,300 cells of its two weekdays' allowance unused** (62,700 - 23,432), which is 67 percent of the 58,580 bound. That figure is **UNMEASURED**; the first honest reading is the 10-17 receipt.
- **If the expansion is short,** the order in which the queue draws is by tier (B1 tier 2, then C1 tier 3, then the research requests tier 4), which is surface B, then C, then D: D's 2,044 cells are the first to slip, then C1 stage 1.

## 4. What the drawer can draw today (the part the hold lift does not change)

`standing_drawer.py open_requests` returns exactly one request: **DEMQUE-TR-COMPARISON-DIVIDEND-PAYERS** (D1). The others are not drawable by it as built:

- **B1 and the porting test:** their securities carry a CUSIP and, for B1, a `dates` list and a per-entry `fields` override. The drawer requires a Bloomberg ticker (`security["bloomberg"]`) on every security and draws a start-to-end window per security. It cannot draw them.
- **The fund-type check:** a `reference`-channel request; the standing drawer draws the `history` channel only. The reference route is `0.0.3_BG_BBGTerminal`, or another seat the CTO names.
- **C1 and ABNB/ICT/scanner:** C1 is the ETFS_RIVALS producer's own in-process run at site Z (its request is not a drawable list); ABNB is a `model_block` request, ICT and the scanner are `reference`: none is drawn by the history drawer.
- **P2/P3:** the priority gate refuses them for client requests (merged), so B1 will not carry a former client.

So the first drawable work on 2026-10-17 is D1's 1,004 cells. Making B1 and the porting test drawable is a drawer cell (identifier resolution from CUSIP, `dates` entries, per-entry fields); it is cut as DQ-t-56 (see the decomposition).
