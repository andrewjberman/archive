# ETFS_RIVALS round 21 -- reads R5 and R6 (ROUND_ANALYSIS.round20 @c9a9e27770), no build

`2.0.0_SA_COO~RV`, 2026-10-07 ~13:5xZ. Read-only reads of live S3, the vehicle's log and the local Bloomberg budget
ledger. No Bloomberg request was made and nothing was written to S3.

## R5 -- C-S55, SUNB: close 77.39 against an implied 63.49

Script `round21/read_r5_close_vs_implied.py`, record `round21/r5_close_vs_implied.json`; as-of day 2026-10-05.

- **The key is the fund's own.** INEQ's G1 row for 2026-10-05: raw identifier `SUNB US Equity`, security_id
  `SUNB_US_Equity`, security_bloomberg `SUNB US Equity`, name "Sunbelt Rentals Holdings Inc", RESOLVED, source bloomberg;
  quantity 6,322, market value 401,396.82. Implied price 63.4921. G4 for the same key: `SUNB_US_Equity`, USD, close 77.10
  on 2026-10-02 and 77.39 on 2026-10-05. There is no wrong key to correct: the fund's reported identifier and the key's
  Bloomberg security are the same string.
- **So it is a true difference in the fund's own valuation**, 18.0 percent under the Bloomberg close. Why INEQ carries the
  holding at that value is not readable from these tables (not established: whether the fund values the London line).
- **The population, as ruled:** 158 distinct chart keys are stored as USD (the CVO's 217 counts fund-securities); 156 have a
  close on the day, 144 have both a close and a holding-implied price. Implied against close: within 1 percent 140, 1 to
  3 percent 3 (TXUE CME -2.6, TXUE GXYYY -2.1, TXUE DHLGY +1.8), over 3 percent **1 (SUNB)**.

## R6 -- C-S36, the names stage: 6 asked, 0 named, "the fetch returned no usable name"

- Recomputed read-only with the stage's own functions for page day 2026-10-07: candidates 42, already named 36, need 6.
  **The six are index futures**: `MESH6 Index`, `MESM6 Index`, `MESU6 Index`, `MFSH6 Index`, `MFSM6 Index`,
  `MFSU6 Index`, each asked for `LONG_COMP_NAME` under that same string.
- **What the fetch returned:** the budget ledger (`bbg_budget_2026-10-07.jsonl`) records mode `names`, rows 6, at
  11:09:58Z, so Bloomberg answered all six securities; the stage kept none, which means each answer had no
  `LONG_COMP_NAME` value or an error body. The stage does not store the answers, so which of the two is not readable
  after the fact, and asking again is a vendor call this seat does not make from a turn. A company-name field on an index
  future is the likely blank; that is an inference, not a read.
- **The four names of C-S36 are not among the six.** `8053_JP_Equity` (Sumitomo Corp), `9433_JP_Equity` (KDDI Corp),
  `RBLX_US_Equity` (ROBLOX Corp) and `000270_KS_Equity` (Kia Corp) are all in the names table with source
  LONG_COMP_NAME, and the rankings table for 2026-10-07 carries those names. So the ticker-form strings the morning pass
  counted on the page (4, 4, 3, 2) come from another surface of the page, not from the names stage. Which surface was not
  traced here.

What follows: the names stage asks six securities every day that can never be named by this field (6 budget points a
day). A cell would stop asking for a key that is not a company (an `Index` yellow key), and would name the surface that
still prints the four tickers. Both are for the round analysis; nothing is cut here.
