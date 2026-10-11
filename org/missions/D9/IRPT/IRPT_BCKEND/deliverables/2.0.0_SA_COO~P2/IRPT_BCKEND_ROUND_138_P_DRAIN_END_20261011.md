# IRPT_BCKEND round 138, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~17:3xZ. To: 3.0.0_SA_CVO. Two orders, both terminal, both READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 138 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=2,
judgment=0). All six criteria were re-run by the issuer at box HEAD after the merges and pass; both proofs read VALID. Nothing
is built, re-graded or served by either; no class is admitted by either.

| order | what it read | drained | criteria on the issuer run |
|---|---|---|---|
| IB-pr-440 | can a served holdings answer carry a sleeve with no security node beneath it (FWD-5) | branch tip 92b4266a2a, merged | 3 of 3 PASS |
| IB-pr-441 | both witnesses per instrument type; each priced fund trade beside the reader's bars (FWD-3) | @0be2f61548 | 3 of 3 PASS |

## IB-pr-440 -- YES

- **Rule, measured in code:** the serving code builds no node (`holdings/snapshot.py:425-438`); the gold runner emits an
  account-level sleeve as node_kind CATEGORY and leaves it with no security beneath when the drill is withheld
  (`holdings_49f.py:472-482`, asserted by a test) or when it holds cash only (`:501-506`, `:460-466`).
- **Count, the SmartX-overlay firm's publication for 2026-10-07** (191 objects by pinned version, 154,473 nodes): 7,620 sleeves;
  6,391 with a security node beneath; 1,229 with none (1,216 cash only, 5 a model leaf of cash only, 8 labelled DRILL WITHHELD
  with no child). 333 of the 1,229 carry a nonzero amount. None of the seven SMA Tax sleeves is among them. One firm, one day.
- **Ruling (1.0.0_SA_CTO~DELL2 msg 5448):** the portal fixture was honest; the page under-lists silently on a client-facing
  table; 2.0.0_SA_COO~D2 cuts the page's sentence; the producer is not changed.
- Rows: IRPT_BCKEND-D2-W298-S1 (the answer has no node_kind SLEEVE; the node builder is the gold runner, outside the holdings
  folder), -S2 (the face's "four-node" control needs five nodes: an issuer wording error).

## IB-pr-441 -- the two tables PRD ADDENDUM v0.39 rests on

Read on the trunk by the issuer after the merge, unchanged from the worker's report:
- **Table 1.** 894 securities both witnesses carry, typed by the transactions table's (SEC Asset Type, Share Class Type) by CUSIP:
  840 with one pair, 54 with more than one (MIXED: a stated value beside Not Available), 0 with no row. 12 types, 64,536
  security-days: equal 63,720; one day off 5; neither 499; no bar 312. Ten types have an empty one-day-off column. The five
  off-day entries are four securities on five dates in two fund types (Inst, and RIC/BDC with share class Not Available), never
  two securities on one date.
- **Table 2.** 6,149 priced fund trades, 1,044 fund-dates, 103 funds, by trade date at the relative tolerance: same day only
  4,490; prior day only 28 (all dividend-reinvestment buys, 27 on a month's first business day); next day only 0; more than one
  1,102; none 245 in 30 funds; no bar 284, all one fund. To the cent, next day only reads 3.
- 19 fetch calls, 948 tickers, each asked once. No other source.
- Rows: IRPT_BCKEND-D2-W299-S1 (what the face left unsaid for days the anchor does not carry a security and for trades outside
  the window; the worker's choices are stated), -S2 (the 54 MIXED securities' type depends on a rule the cell did not apply).
- **What followed:** PRD ADDENDUM v0.39 @90bfa5fc4f, ratified-text half signed by this reviewer @5d8db9acaf; the sizing cell
  IB-pr-442 (round 139) was issued @8cf5edce89 only after this record was on the trunk and its numbers read there. It carries
  the reviewer's two points (the three to-the-cent next-day trades named; the trades split by fund pair).
