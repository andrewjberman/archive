# DRAFT (not issued) -- ADVI_COTBKF FWD-3: the daily-returns cut, pre-drafted for the price-load un-park

**Author:** `2.0.0_SA_COO~C2` (dell2), 2026-10-07 ~14:3xZ, on Andrew's "go" to /next-calls option 2. **Status: DRAFT.** Nothing here is
issued; it becomes a decomposition and orders the tick the gate below opens (or the CTO pulls cell A forward).

## Basis

- **FWD-3** (`prd/ADVI_COTBKF_PRD.md:46-49`): an analyst reads each Cottonwood account's returns day by day, after fees, back to 2013;
  DONE WHEN one account's daily returns are read across the whole span and checked against Commonwealth's monthly figures.
- **C-DAILY** (`:113`): (1) daily holdings per account rebuilt from the transactions, each account's opening state from its own history;
  (2) each holding valued daily with a closing price; (3) a daily after-fee time-weighted return with the day's flows taken out; (4) the
  days chained per month and compared with Commonwealth's monthly return, MATCH within a stated tolerance or DIFF with its reason. A
  security no store prices leaves its days unpriced, never estimated.
- **MDPF_SECHIST C-SERIES / C-GAP** (`org/missions/D8/MDPF/MDPF_SECHIST/prd/MDPF_SECHIST_PRD.md:95,97`): one stored series per security;
  a window over a missing day reads blank, never compounded. Its storage address is not fixed in that PRD (C-NAMES: builder output in the
  order that writes it) -- the one input this draft cannot name.
- **Need:** `deliverables/0.9.0_WK_ADVI_COTBKF~27/PRICE_NEED_FOR_SECHIST.csv` (4,545 securities, 8,091,310 security-days).

## Cells, by what each waits on

| cell | C-DAILY step | waits on | risk |
|---|---|---|---|
| **A -- daily holdings** | (1) per account, per trading day, quantity by security rebuilt from silver transactions (1,416,497 rows, C-SILVER), opening state from the account's own history; checked against the one positions snapshot (2026-06-23, 83 accounts, 469 positions) | **NOTHING** -- no price needed | LOCAL |
| B -- daily valuation | (2) value each holding with the day's close from Opal's six USABLE stores plus MDPF_SECHIST's series; an unpriced holding-day stays blank (C-GAP) | MDPF_SECHIST's first announced load and its series address | LOCAL |
| C -- daily return | (3) after-fee TWR per account per day, flows removed; a day touching a blank valuation reads blank | B | LOCAL |
| D -- monthly grade | (4) chain C per month; compare with silver performance (88,654 rows, Month rows); MATCH within tolerance / DIFF with reason; tolerance stated before the run | C | LOCAL |

**Cell A could be cut now.** It serves FWD-3 and has no unmet dependency. Under /canonical-drive obligation 5, an idle lane beside such a
cell is a defect -- but the round-11 analysis (`CTO_ROUND_ANALYSIS_ADVI_COTBKF_ROUND_11_20261007.md`) lists no issuance, and the
enrichment list is the CTO's. Put to `1.0.0_SA_CTO~DELL2` with REC: pull cell A forward now.

## Cell A, as it would be cut

- Script `data/assets/scripts/silver/commonwealth_daily_holdings.py`, read-only (`--out` local), reading silver transactions by builder
  address; trading days from `lib/trading_calendar.py` (covers 2010-2027; CB-e-1's guard refuses an uncovering calendar).
- Criteria (at most three): (1) a stub test -- buys, sells, a transfer in and out, a split -- rebuilds the expected quantities, with a
  control that a dropped transaction moves the result; (2) the real run prints
  `DAILY-HOLDINGS accounts=1533 account_days=<n> snapshot_checked=83 snapshot_equal=<k>` with `<k>` recorded, not presumed; (3) judgment
  for the CVO: one account's holdings read across its span against its transactions.
- Write set: the script, its test, the deliverables folder, the channel. No S3 write (the apply is the issuer's act under a pair).
