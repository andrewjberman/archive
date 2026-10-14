# ADVI_BDPRCE -- the review page for the price fix (FWD-7 packet, round 3, amendment R1.3)

Prepared by `0.9.0_WK_ADVI_BDPRCE~22` (cell BP-c-3). Read-only: nothing is served, written or deployed. The
figures come from the list the R1.3 replay produced (`BEFORE_AFTER3.csv`, `ESTIMATED_ROWS3.csv`) and from the
lot extract of the 49 Financial book (198,295 lots, sha256 `e7e618d7...2b50b`). Machine record: `PACKET3.json`.
Movers: `MOVERS3.csv`. Every number below says its denominator.

## 1. What is proposed

The rule the CTO amended (amendment 3) changes the VALUE of a served price where the trade record supports a
different value. It never changes an asset's UNIT: a price stays per 100 or per unit as the asset is served.
Under the amended rule each served price is re-read from the trade record. A price with a trade on its date takes
the median of that day's distinct trades. A price with no trade on its date takes the last earlier trade, and the
page says which date that trade was. Where the unit cannot be read, or no earlier trade exists, the price is
withheld and shown as withheld. Nothing has been served. This page asks you to review what would move.

## 2. The latest snapshot

| item | value | denominator |
|---|---|---|
| latest date carried by a majority of lots | 2026-10-09 | 196,675 of 198,295 lots |
| share of lots on that date | 99.18% | 196,675 / 198,295 |
| lots not on that date (not counted in the snapshot) | 1,620 | 198,295 lots |
| snapshot lots with no current price (text "nan" in the extract) | 34 | 196,675 snapshot lots; none in an asset that moves |

## 3. What moves on the snapshot date

| item | value |
|---|---|
| prices that move on 2026-10-09 | 15 (8 changed on a trade, 7 carry-forwards) |
| assets that move | 15 |
| carry-forwards that equal the served price (touched, not moved) | 0 |
| lots held in the moving assets | 819 |
| of those, in assets not in the extract (no lots, so no dollar effect) | 6 assets (the Fidelity index and fund rows) |
| value of the 819 lots, quantity x current price | $15,095,778.50 |
| share of the snapshot value (priced lots, $1,341,907,669.01) | 1.12% |

Across the whole window (2026-09-16 to 2026-10-13) the replay moves 759 served rows (599 changed, 160 carry-forwards),
of which 754 differ from the served value. The snapshot figures above are the ones the dollar effect counts.

## 4. The dollar effect

The effect of one price move is (new price - served price) x quantity, summed over that asset's lots on the
snapshot date. The order's basis is quantity x price, not the served market value.

| basis | total effect | what it means |
|---|---|---|
| **served price basis (the headline)** | **$90,964.76** | (new - served price) x quantity, on the 819 lots |
| served market value basis | $103,614.56 | each lot's served market value scaled by new / served price |
| lot price basis | $358,069.95 | (new - the lot's own current price) x quantity |

The headline and the lot price basis differ by $267,105.19. The reason: 726 of the 819 lots carry a current
price that is not the served price of their asset (93 of 819 agree). For example, 300 lots of VANGUARD MORNINGSTAR
GROWTH ETF carry 83.78 where the served price is 91.98. Which base is the true change for Andrew's book is a
question this packet does not settle; it is listed in section 9.

Market value identity: 21,471 of the 196,641 priced snapshot lots have a served market value that is not
quantity x current price (tolerance as the census used). Of those, 96 lots sit in the moving assets. On those 96
lots the effect is -$20,122.90 on the quantity basis and -$7,385.15 on the served market value basis.

## 5. The 15 movers (every mover; the list is not padded to 25)

Only 15 prices move on the snapshot date, so the list holds all 15 and fewer than 25 exist. Ranked by the headline
effect. Full columns in `MOVERS3.csv`.

| rank | asset | class | served price | new price | lots | effect, served basis | observation date |
|---|---|---|---|---|---|---|---|
| 1 | SIX FLAGS ENTERTAINMENT CORP COM | carry-forward | 11.41 | 30.805 | 1 | +96,431.94 | 2025-08-04 |
| 2 | EXXONMOBIL HOLDINGS CORP COM SHS | carry-forward | 168.94 | 168.29 | 95 | -24,308.09 | 2026-10-08 |
| 3 | SPACE EXPLORATION TECHN CORP CLASS A COM STK | changed (trade) | 163.02 | 163.47 | 32 | +18,280.14 | 2026-10-09 |
| 4 | INTERNATIONAL EQUITY INDEX POOL | changed (trade) | 28.5135 | 28.61 | 33 | +317.33 | 2026-10-09 |
| 5 | SMALL CAP EQUITY POOL | changed (trade) | 58.3333 | 58.75 | 28 | +206.72 | 2026-10-09 |
| 6 | VANGUARD MORNINGSTAR GROWTH ETF | changed (trade) | 91.9833 | 91.985 | 574 | +37.78 | 2026-10-09 |
| 7 | VANGUARD MORNINGSTAR VALUE ETF | changed (trade) | 220.54 | 220.49 | 17 | -22.59 | 2026-10-09 |
| 8 | TREASURY INFLATION PROTECTED SECS | changed (trade) | 14.5833 | 14.60 | 27 | +20.70 | 2026-10-09 |
| 9 | VANGUARD MORNINGSTAR TOTAL STOCK MARKET ETF | changed (trade) | 381.8522 | 381.8601 | 12 | +0.84 | 2026-10-09 |
| 10-15 | six FIDELITY rows (FIDELITY ADVISOR MEGA CAP STOCK Z, ENHANCED SMALL CAP CORE ETF, GLOBAL EX US INDEX, INTERM TRS BD INDEX, MID CAP GROWTH INDEX, MID CAP VALUE INDEX) | 1 changed, 5 carry-forwards | | | 0 | 0.00 each | |

Ranks 1 to 9 hold the 9 assets with lots; their effects sum to $90,964.76. The largest single move, SIX FLAGS, is a
carry-forward from 2025-08-04 and is 170% above the served price; it is worth Andrew's specific look before anything
else. Its unit was unreadable in the replay, but an Equities row is not withheld by unit, so the price is kept.

## 6. Prices that are withheld, and why nothing is priced from them

Withheld means the row is shown NOT_RECOMPUTABLE: the served price stays, and nothing is priced from it.

| where | count | reasons |
|---|---|---|
| window, all served rows | 183 of 1,689 | 151 no earlier trade; 19 unit unreadable; 3 carry refused on a withheld last trade; 10 ratio not recognised |
| snapshot date, rows | 31 of 63 | 15 unit unreadable; 15 no earlier trade; 1 carry refused |

These rows carry zero dollar effect. Across the window the replay withholds 12,070 Fixed Income trade rows on 102
assets; 19 served rows, each of a Fixed Income asset whose unit cannot be read, are withheld by unit. A withheld
row is a row no price was taken from; it is not a price.

## 7. Units and the per-100 example

No served row changes its unit: 0 rows changed unit, and 0 rows are held out for a unit. The only per-100 series in
the served set is MORGAN STANLEY FIN LLC 0% 05/03/2029 (a par bond). Its series is per 100, and the replay keeps it
that way. The worked example, each shown with its observation date:

| date | served price | new price | class | observation date |
|---|---|---|---|---|
| 2026-10-05 | 115.995 | 100.00 | carry-forward (last traded) | 2025-05-28 |

Its 27 interpolated rows in the window (2026-09-16 to 2026-10-13) all carry 100.00, last traded 2025-05-28, in place
of estimates of 111.58 to 115.995. The asset has no lots in the extract, so it has no dollar effect on the snapshot.

## 8. The estimated rows: what happens to each

The replay's 18,397 interpolated rows (the estimated prices the CTO banned) each get one fate.

| fate | rows | share | replacement |
|---|---|---|---|
| trade price | 0 | 0.0% | none needed: no interpolated row becomes a trade price |
| last traded on a stated date | 16,025 | 87.1% | the last earlier trade price, with its date |
| unresolved | 2,372 | 12.9% | none: no earlier trade under the rule, so the estimate has no replacement |

The three add to 18,397. Ten examples of each fate (window dates, first in file order):

Last traded on a stated date (served -> replacement, observation date):

| date | asset | served (estimate) | replacement | last traded |
|---|---|---|---|---|
| 2026-09-16 | ABRDN PHYSICAL SILVER SHARES ETF | 57.5504 | 56.53 | 2026-08-04 |
| 2026-09-16 | ACI WORLDWIDE INC COM | 51.1211 | 45.7601 | 2026-06-17 |
| 2026-09-16 | AFFILIATED MANAGERS GROUP COM | 347.9234 | 342.4001 | 2026-06-25 |
| 2026-09-16 | AGGRESSIVE PORTFOLIO | 10.6696 | 10.7296 | 2026-09-08 |
| 2026-09-16 | ALLSPRING ASSET ALLOCATION A | 16.5135 | 14.00 | 2025-01-14 |
| 2026-09-16 | ALLSPRING CORE BOND CIT CLASS E2 | 10.5274 | 10.6258 | 2026-09-04 |
| 2026-09-16 | ALLSPRING CORE PLUS BOND INSTL | 10.6522 | 11.37 | 2025-09-24 |
| 2026-09-16 | AMENTUM HOLDINGS INC COM | 19.3079 | 20.0317 | 2026-09-01 |
| 2026-09-16 | AMERICAN AIRLINES GROUP INC COM | 12.8782 | 12.8124 | 2026-09-10 |
| 2026-09-16 | AMERICAN FDS US GOVT MMKT FUND CL 529-A | 1.0000 | 1.0000 | 2026-09-01 |

Trade price: none (0 rows), so there are no examples to show.

Unresolved (served estimate, no replacement; reason no earlier trade):

| date | asset | served (estimate) |
|---|---|---|
| 2026-09-16 | ALLSPRING SPECTRUM GROWTH A | 14.4469 |
| 2026-09-16 | AMERICAN BEACON DEVELOPINGWLDINCFD-YCL | 7.7550 |
| 2026-09-16 | AMERICAN FUNDS AMCAP F-2 | 46.1996 |
| 2026-09-16 | AMERICAN FUNDS AMERICAN BALANCED F-3 | 40.0922 |
| 2026-09-16 | AMERICAN FUNDS GROWTH FD OF AMER F-3 | 87.1448 |
| 2026-09-16 | AMERICAN FUNDS INCOME FD OF AMER F-3 | 27.7031 |
| 2026-09-16 | AMERICAN FUNDS TAX-EXEMPT BOND C | 12.0200 |
| 2026-09-16 | ASHMORE EMERGING MKTS FRONTIER EQ INSTL | 14.1617 |
| 2026-09-16 | CAMBIAR INTERNATIONAL EQUITY INSTL | 33.0366 |
| 2026-09-16 | CANTOR FITZGERALD COMMODITY RET STRAT I | 30.8633 |

On the snapshot date alone there are 649 interpolated rows: 562 last traded, 87 unresolved. 323 of the 562 change
price. They are NOT in the dollar effect in section 4, which counts the served transaction rows only (see section 9).

## 9. The readers that move

A reader is any file or project that reads a served 49F price or lot value. This census is NOT the C3 census; it names
the readers the repo and the PRD establish. Where a reader's read of a 49F lot was not traced to a line, the claim is
inferred and the page says so.

| reader | class | sums lots into an account or firm figure? | evidence |
|---|---|---|---|
| MDPF_SECCLASS BD Mix (client-facing restated-history push) | client-facing | not traced | MDPF_SECCLASS_PRD.md:744; ADVI_BDPRCE_PRD.md:137 |
| IRPT_DASHBD client reporting dashboard | client-facing | not traced (claim inferred) | IRPT_DASHBD_PRD.md:1; ADVI_BDPRCE_PRD.md:137 |
| IRPT performance math (a reader of the lots) | unknown | not traced (claim inferred) | ADVI_BDPRCE_PRD.md:96 |
| BD account gains (B_03, account market value by account) | unknown | yes: sums market value by account | data/black_diamond/scripts/gold/B_03.account_gains.py:222-223, 465-466 |
| Portal InvestorReporting holdings tab | client-facing (inferred) | not traced; the wire carries the custody total | portal/src/pages/InvestorReporting/tabs/holdings/SliceTable.tsx:216, :273; contracts/wire/HoldingsSnapshot.ts:36 |
| ADVI exec-summary generator, platinum reader | unknown | no (the file has no sum) | infra/aws/lambda/exec-summary-generator/platinum_reader.py:155, :175, :196; lambda_function.py:254-259 |
| INF_D_07 concentration risk (shares the canonical price object) | unknown | yes: sums market value by household | data/inf/scripts/gold/INF_D_07.concentration_risk.py:141-147 |

Seven readers are named (the order asks for four). Classes: 3 client-facing (1 from the PRD text, 2 inferred from the
PRD and the portal route), 4 unknown. Nothing here is a count of accounts or firms the figures reach; that is
the C3 census's job.

What does NOT move: an account's total value. Under the PRD's CONTRACTS an account's served total stays BD's own
account value and is never a sum of lots, so the account totals do not change with these lot prices.

## 10. What the packet does not know

- Which price is the lot's true value. 726 of the 819 lots in the moving assets carry a price other than the served
  price. The headline uses the served price, as the order's formula does. The lot price basis is $267,105.19 higher.
- The 34 snapshot lots with no current price (text "nan"). None is in a moving asset, so they change no figure here,
  but the census identity check left them out without naming them.
- The effect of the 323 snapshot-date interpolated rows that change price is outside the headline. A supplementary
  computation gives $5,227.11 on 826 lots, using the canonical estimate as the old price. It is not a dollar effect
  on the order's basis and is not added to the headline.
- The six Fidelity rows move but have no lots in the extract, so they cannot be priced here.
- The readers' code paths are traced for four; the rest are named from the PRD and marked inferred.
- The 2026-10-14 partition, which is the current day's file, may change; the replay read it once.
- The order's "exact sentence" of the decision was not given in the order; the sentence below is composed from the
  order's stated content.

## 11. The decision asked of Andrew

**Andrew, please review the named list of 15 price moves on 2026-10-09 (section 5) and the readers they reach (section 9), per fix, and approve or refuse each; nothing is served until you have seen it.**
