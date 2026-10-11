# IRPT_BCKEND round 137, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~17:0xZ. To: 3.0.0_SA_CVO. One order, terminal, READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 137 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1,
judgment=0). The three criteria were re-run by the issuer at box HEAD after the merge and pass; the proof reads VALID.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 137 | IB-pr-439 | under PRD ADDENDUM v0.38: the source's instrument-type field; the sizing; priced fund transactions | merged from branch tip e6462bdd4a | 3 of 3 PASS |

## What it found (FWD-3, Cottonwood)

- **The holdings source states no instrument type.** 85 partitions, 1,411,352 rows, 26 distinct column names; nine candidate
  columns examined (a cash flag, two supervision flags, a display name null on every row, three one-valued technical columns,
  two numbers, an alternative identifier): none says what kind of instrument a row is. The cell STOPPED there as ordered: no
  overlap table, 0 fetch calls, no outside source asked.
- **So no class is admitted to the second witness** and the sizing under v0.38 equals the rule in force: blank 58.157 percent of
  75,796 eligible account-days; 382 of 999 accounts never served; the one fund with no data touches 12,115 account-days.
- **A CORRECTION this seat owes the record:** the rounds 135-136 packet @dc47506c21 carries "blank 58.2 to 37.0 percent, never
  served 382 to 181" as a sizing. PRD ADDENDUM v0.38 withdrew it: it counted mutual funds as graded, and the reads behind it do
  not establish that the reader's bar carries the NAV's own date. The counts in that packet stand as counts; the sizing does not.
- **Counted, not fetched:** 894 securities both witnesses could carry (890 distinct tickers).
- **Fund transactions:** `fact_transactions`, beside the holdings table, carries a Price. For the nine funds of round 134: 361
  priced buy or sale fund-dates, 346 inside the 85 days. An older transactions table read by ADVI_COTBKF has no Price column.
- **The find (row IRPT_BCKEND-D2-W297-S1):** that transactions table carries `SEC Asset Type` and `Share Class Type` by CUSIP,
  NOT used by the cell. The CTO ruled (msg 5376) that the field classes nothing until an addendum is written on two tables, and
  ordered them: IB-pr-441, round 138, running. Row -S2: two transaction tables exist and only one has a Price.

## Open in the workstream, not part of this packet

Round 138: IB-pr-440 (can a served holdings answer carry a sleeve leaf with no security node; FWD-5) and IB-pr-441 (the two
tables), both read only and running. IB-pr-426: both halves signed, no apply order until the CTO's word after st32. IB-pr-413
L4 and IB-pr-404 L6 wait on Monday 2026-10-12 14:15Z.
