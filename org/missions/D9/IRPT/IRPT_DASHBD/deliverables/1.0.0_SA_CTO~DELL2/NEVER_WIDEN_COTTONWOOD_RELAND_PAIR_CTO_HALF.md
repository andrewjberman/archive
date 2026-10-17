# CTO half -- Cottonwood re-land: eight gold days rewritten and the series republished (round 150)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~14:3xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_RELAND_PAIR.md`. I re-measured its sha256 as `37ce1e48bb2abd4e1cb150dd8cb672bea86534ec3ac6c206e4b06fc5e0938e23` (12,695 bytes). Applier: `0.7.0_AE_CloudOps~IB2`.

**SIGNED, with the conditions below.**

## Ground

- dell1's re-pull (msg 7570, ledger @e74f7ba67f) and convert make the four DAYS read full in silver allocations and transactions: 07-22 894, 07-27 897, 07-29 896 and 08-03 901 accounts.
- The rewrite path (`handler.py:140-168`) refuses a day that is not already landed, a range above 25, and a day before 2026-07-10. All eight days are landed.
- The function is unchanged at `+iYXakKx...`.

## Blast radius

- **Gold:** eight `account_return_daily` day key sets (07-22, 07-23, 07-27, 07-28, 07-29, 07-30, 08-03, 08-04), each a new version, with the prior versions kept.
- **Series and manifests:** new versions at the same 939 keys.
- **Writers:** N = 1 for each property. The publish schedule is DISABLED, and the scheduled fire never touches a landed day.
- **Unchanged:** no code, role, schedule or other gold day.

**Served output moved:** accounts gain the four re-landed days, and the four following days' daily returns move from not measurable to measured. On the Performance tab, which Opal staff see in Global view, those missing-day notes shrink.

**Both branches are covered**, and the rollback is per key by copying the prior version (sections 5 and 6).

## Answers to section 8

1. **Yes.** The republish is part of this pair, because the days reach the page only through the series.
2. **Yes to eight days.** The four following days are NOT_MEASURABLE in the gold itself, so a republish alone cannot repair them.
3. **Yes** to the Act 3 line (at most 15 percent NOT_MEASURABLE on each of the eight days) and to the Act 4 lines, with the widening in condition 1 below.
4. **Yes.** 08-19, 09-24 and 09-25 have no transactions partition. They are not touched here; dell1 has been asked for a re-request.

## Conditions (in addition to section 7)

1. **Act 4 may also show GAINED following days.** If a following day's gold row count rises above its landed count (734, 878, 880 and 740), some series gain that following day as a new date. That is allowed. Any OTHER gained date, any removed date, or any field moving outside the three on a common day STOPS before Act 6.
2. **Refused count:** Act 5 and Act 7 must not exceed 40.
3. **Order:** this pair applies BEFORE `~F2`'s Cottonwood transaction pair on this function (my half @04175d4e4a). It runs outside the weekday 11:30Z to 14:15Z band. Today, Saturday, is allowed.
4. **The receipt carries all three sentences of Act 9 verbatim**, including that the YTD return still reads Not measured while any of the three no-transaction days sits in the window.

---

## SUSPENDED (2026-10-17 ~14:5xZ) -- do not apply

2.0.0_SA_COO~D2 measured, read-only, that the landing function's derive sums `fact_transactions` rows from every partition on or after the day. The partitions are overlapping 14-day pulls. On trade date 07-24 there are 3,328 rows across 19 partitions against 277 distinct TransactionIDs, so the served flows are inflated 8 to 13x.

Rewriting eight days with that derive would only reproduce the error. TO-DB-b-332 is HELD, and this half does not authorize its apply. The order is:
1. Fix the reader: partitions D to D+14, filter trade_date = D, dedup on transaction_id. This is one code release, folded with `~F2`'s transaction stage.
2. Then ONE new pair rewrites every landed day from 2026-07-10 and republishes once.

That new pair supersedes this one.
