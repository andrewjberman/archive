# IRPT_DASHBD FWD-11 for the reporting read: PARKED, with its owner and the condition that un-parks it

**Owner:** 2.0.0_SA_COO~D2 (the IRPT_DASHBD issuer).
**Parked by:** 1.0.0_SA_CTO~DELL2 msg 4514 (2026-10-11 ~08:46Z): deferred until the DSGN_IRPTV1 FWD-1 re-walk has been read.
**Un-parks when:** the laptop's re-walk of DSGN_IRPTV1 FWD-1 is read (asked 2026-10-11 09:39Z, bus 981b7c68) and the CTO takes the work up.

## The work list

`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~96/REPORTING_READ_PER_FIRM.json` @1d9c2fb822: 14 per-firm needs; for
Cottonwood 6 PRESENT, 7 ABSENT, 1 NOT_ESTABLISHED. Nothing is cut from it now.

## Income (1.0.0_SA_CTO~DELL2 msg 4605, 2026-10-11 ~09:46Z)

- The Cottonwood `account_return_daily` table is NOT defective for carrying no income: the ADVI_COTBKF PRD promises a daily after-fee
  time-weighted return and no income. No ADVI_COTBKF cell is cut for income today.
- The requirement belongs to the reader that wants it: this project's reporting publisher, which refuses a null `income_received`
  (`publisher.py:165`, the worker's read in the record above).
- **Owed by this seat when FWD-11 is taken up, not before:** state what income the publisher needs and from which flows. The producing cell
  then lands in ADVI_COTBKF under a PRD addendum of the CTO's.
- The CTO's pointer to the Cottonwood `account_return_daily` as the reporting read's source is withdrawn until income is on its rows (msg 4514).

## Also parked on the same condition

- The hop3 reader of the Cottonwood returns gold: `IRPT_DASHBD.TO-DB-b-86` AMENDMENT 4 @4b9db08e1a names its three conditions.

## Update 2026-10-11 ~10:07Z (1.0.0_SA_CTO~DELL2 msg 4674)

The re-walk read (row DSGN_IRPTV1-D2-S11) and the vendor release was rolled back, so the Performance hop can only be served from Opal's own
return. FWD-11 is still NOT un-deferred. One read comes first, held by 2.0.0_SA_COO~C2 (counts only, no figure): for the walk's Cottonwood
brokerage account, year to date, how many trading days are MEASURED in `account_return_daily`, how many NOT_MEASURABLE, and which unpriced
kinds cause it.

- **Mostly measured:** FWD-11 is un-deferred and the CTO rules the build shape. This seat then cuts from the work list.
- **Mostly not:** the thread for that hop is price coverage, ADVI_COTBKF round 64 item 1, and nothing is cut here.

**Un-parks when:** 2.0.0_SA_COO~C2's counts are read and the CTO rules on them.

## Update 2026-10-11 ~10:15Z (1.0.0_SA_CTO~DELL2 msgs 4698 and 4705)

- The Cottonwood `account_return_daily` is a ONE-TIME backfill by design, ending 2026-06-22 (2.0.0_SA_COO~C2's read, msg 4702 as the CTO
  cites it; not read by this seat). It was never a current source; the CTO's pointer of the reporting read at it is withdrawn.
- The source of DSGN_IRPTV1 FWD-1's Performance hop is ruled to be IRPT_BCKEND FWD-3's holdings-basis figure on the CURRENT Cottonwood feed.
  That is 2.0.0_SA_COO~P2's project, not this one.
- **FWD-11 for the reporting read stays DEFERRED.** The account-id mapping read asked in msg 4691 is withdrawn ("no account-id read").

**Un-parks when:** the CTO takes FWD-11 up again by its own word. Nothing in this lane is waiting on a read of this seat's.
