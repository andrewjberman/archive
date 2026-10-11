# IRPT_BCKEND round 139, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~18:1xZ. To: 3.0.0_SA_CVO. One order, terminal, READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 139 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1,
judgment=0). The three criteria were re-run by the issuer at box HEAD after the merge and pass; the proof reads VALID.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 139 | IB-pr-442 | the sizing under PRD ADDENDUM v0.39's seven admitted types; what the rest waits on; the reviewer's two points | branch tip 721d34910e, merged | 3 of 3 PASS |

## The sizing (FWD-3, Cottonwood) -- a SIZING, nothing stamped, no producer cut on it

- **737 securities the first witness does not carry:** 152 of an admitted type with bars; institutional share class 71; fund type
  with share class not available 78; no type or mixed 38; other pairs not admitted 19; no ticker to ask with 375; no bar 4
  (FPNIX, BRK.A, UHALB, JHG). The seven pair strings were found exactly as the transactions table writes them.
- **Account-days holding such a security: 34,789.** Freed (every such security admitted and at the day's close): 5,737, of which
  5,666 hold no other ungradeable kind; blocked by a prior-day-only row 80; by a row at neither 69; holding a security no witness
  may grade 28,903.
- **Sized:** blank 50.305 percent of 75,796 eligible account-days (58.157 in force); 357 of 999 accounts never served (382).
  The withdrawn sizing that counted every fund read 36.989 percent and 181, for reference only.
- **What the rest waits on (account-days; "only on" is an upper bound):** institutional class 23,562 holding any, 6,960 only on;
  fund type with share class not available 6,235 and 2,003; no ticker 4,619 and 1,871; other pairs 2,027 and 319; no type or
  mixed 497 and 96; no bar 12,248 and 43. FPNIX alone touches 12,115.
- **The reviewer's two points.** (3) "Next day only" to the cent: three trades, all dividend-reinvestment buys in institutional
  funds: PFMIX 2026-06-30 (price 9.4637; bars 9.47, 9.47, 9.46), VWIUX 2026-06-30 (13.805; 13.81, 13.81, 13.80), NHMRX
  2026-07-01 (14.5263; 14.52, 14.50, 14.53). (4) The 6,149 priced fund trades by the fund's pair: Inst 3,630 (60 funds);
  No Load 1,547 (9); Other 505 (12); Inv 285 (2; 284 of them the one fund with no bar); Retirement 98 (5); A 47 (6; 42 of them
  matching no bar); Adv 25 (1); MIXED 12 (8). Per-pair outcomes are in the record.
- Rows: IRPT_BCKEND-D2-W300-S1 (all 38 no-type-or-mixed securities pair Not Available with one stated value; the rule that would
  take the stated value was not applied), -S2 (the admitted pair Inv grades nothing outside the first witness: its one security
  is the fund with no bar, and the fund table's support for Inv is one trade), -S3 (two readings of the face the worker fixed
  and stated).

## What followed

1.0.0_SA_CTO~DELL2 msg 5501: 50.3 percent is the number under v0.39; the institutional class is not admitted on the smallness
of two days; one read-only cell (IB-pr-443, round 140, running) sets a third dated value beside both witnesses on the five
one-day-off security-days and asks whether the first witness's partition for the window's last day is the prior day's.
