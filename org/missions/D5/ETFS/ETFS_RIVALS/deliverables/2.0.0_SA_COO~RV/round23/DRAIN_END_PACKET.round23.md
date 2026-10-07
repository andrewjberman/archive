# ETFS_RIVALS round 23 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~19:1xZ)

One cell, RIV-ks-1, item 1 of ROUND_ANALYSIS.round22 @f8a61834fd (R1, R2): the repair of rows ETFS_RIVALS-Z-S65 and
Z-S66. Issuance 90b1a83ca1; build 3d05e19e1b; proof 4e260752a2; close 97149dd163; merge d7bbe4f5a3 on site-Z CLOUD
(LOCAL). **Not deployed:** the live Lambdas are at beb13d39ff (rounds 15 to 22) and still serve the fault.

## Mechanical criterion

ks-1.AC1 PASS 0 failures, 6 of 6 arms, re-run by the issuer on the branch; proof instance VALID; the check file is
unchanged by the worker. On merged CLOUD abc0541e42: package suite 877 passed, 2 skipped, 0 failed; 27 of 27 check files
under `round15/checks/` PASS 0 failures.

## The cause (replaces "not traced" of row Z-S66)

The fund traded the security under a raw key (a CUSIP in the trade schedule), so `render._fund_keys` counted that key as
one the fund holds; the raw key's page name differs from the tabled key's only in case; the stored account cites the raw
key; `_panel_page` and `_name_link` let the citation decide; `_sec_dialogs` builds sections from contribution and trend
rows only. The name therefore linked to a dialog holding a name and nothing else.

## The repair

Inside fund F's panel a mention links only to a key that has a section for F. `_fund_keys` no longer counts a trade-only
key; a new `_panel_key`, applied in `_rich` after `_name_link`, takes a key without a section to the one key of the same
name (case ignored) that has one, else the mention reads as plain text. Stored account text is not rewritten.

## The issuer's real run (day 2026-10-07, from the branch; live inputs, local writes only)

Record `round23/real_run_2026-10-07.after_ks1.json`, against the page served since 17:47Z.

| read | served (rounds 15-22) | round 23 |
|---|---|---|
| `fund_sections` missing, of 2,247 buttons | 4 | **0** |
| dialogs with no section | 2 (`30303M102`, `N07059210`) | **0** |
| buttons in account text | 830 | 830; exactly 4 changed: GQGU's two META and two ASML mentions now target `META_US_Equity` and `ASML_US_Equity`; none other gone or added |
| index.html | 1,690,862 B | 1,690,296 B; dialogs 410 -> 408; 690 chart frames |

The worker's caution -- a name the fund never held now reads plain where it linked to another fund's dialog -- changes
0 buttons on this day.

## Row Z-S57 (analysis R2)

Not the same cause, by the issuer's read and the worker's: Z-S57 is one security under two buckets in the buying_trend
TABLE; this was a LINK choosing a trade-only key. Round 20 repaired Z-S57's read and it is deployed since 17:3xZ; its
re-read on the served page is the CVO's.

## Why the publisher's FAIL line reached no row (analysis R1)

The real-run record carried `fund_sections.missing` from round 17 (3, then 6 from round 21) and the issuer's packets
did not read that field. From this round the packet prints it (table above), and the served grade script reads it.

## Judgment criterion owed at L9

RIV-ks-1 J1, on this run: in GQGU's panel the META and ASML mentions open the dialog that carries GQGU's section; no
mention on the page opens a dialog holding only a name.

## What waits, and on whom

- A deploy of round 23 is a new served act: a never-widen pair, a ledger entry, one republish. The issuer asks
  1.0.0_SA_CTO~Z whether it goes today as its own act or rides the next deploy.
- Ledger `etfs-rivalfunds-r22`: L3 Andrew's look; L4, L5 the 2026-10-08 11:00Z and 13:00Z runs.
