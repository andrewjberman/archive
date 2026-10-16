# NEVER-WIDEN ADDENDUM 1 (COO) -- the Cottonwood landing rewrite, REVISION 2: ten smaller events in place of four (IRPT_DASHBD round 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED by the COO; the CTO's countersignature is owed before event 1 runs. **Date:** 2026-10-16 ~20:2xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2.md`), sha256 `962ef131ff27c49ebd3afc4d756952599df913031bf5b9426f8118e9c100f3fa`, blob `9a5608687d2fda19831a3dd70e8fc76eba76c25e`. The packet and both signed halves stay as they are; this addendum replaces ONLY the event table of Act 4 and the dry-run clause of Act 3. Order: `IRPT_DASHBD.TO-DB-b-308`, applier `0.7.0_AE_CloudOps~IB2`.

## 1. Why

Acts 1 and 2 ran (new version `6tFJSAqD`, plan 0/1/0, one safe-apply, post-plan No changes; IB2 msg 9808). The Act 3 dry run on the first range (25 days from 2026-07-10) hit the 900 s Lambda timeout, nothing written (rows `IRPT_DASHBD-D2-IB2-S1`, `IRPT_DASHBD-D2-S129`, `S130`). Two small dry runs, one invoke each, nothing written (IB2 msg 9823): A 2026-07-10..07-14, 3 days, 339,560 ms (about 113 s a day), Max Memory 639 MB; B 2026-10-08..10-14, 5 days, 65,209 ms (about 13 s a day), Max Memory 639 MB. Both ok, 0 held, rows equal the landed rows, the whole-prefix read unchanged after each. The cost of a day falls with the day's age (the derive re-reads every `fact_transactions` partition from the day on): this seat's model, cost(day) = 6.6 s + 1.6 s per partition on or after the previous trading day, predicts A at 356 s (measured 340) and B at 81 s (measured 65). Memory is flat at 639 MB, under the packet's 819 MB limit; time is the only limit, and a resize cannot lift 900 s.

## 2. What changes: Act 4 becomes TEN events, the same 66 days, oldest first

Each event only after the previous one's after-read is recorded; each `{"rewrite": {"start": ..., "end": ...}}`, no `dry_run`. The ranges are cut around the three trading days with no partition (2026-08-19, 2026-09-24, 2026-09-25; the handler refuses a range holding a day that is not landed) and so that each event's predicted time is at most 546 s (60 percent of the timeout).

| event | start | end | trading days | predicted s |
|---|---|---|---|---|
| 1 | 2026-07-10 | 2026-07-15 | 4 | 471 |
| 2 | 2026-07-16 | 2026-07-21 | 4 | 446 |
| 3 | 2026-07-22 | 2026-07-28 | 5 | 521 |
| 4 | 2026-07-29 | 2026-08-04 | 5 | 481 |
| 5 | 2026-08-05 | 2026-08-12 | 6 | 524 |
| 6 | 2026-08-13 | 2026-08-18 | 4 | 318 |
| 7 | 2026-08-20 | 2026-08-31 | 8 | 546 |
| 8 | 2026-09-01 | 2026-09-15 | 10 | 538 |
| 9 | 2026-09-16 | 2026-09-23 | 6 | 246 |
| 10 | 2026-09-28 | 2026-10-15 | 14 | 305 |

Denominator: 4 + 4 + 5 + 5 + 6 + 4 + 8 + 10 + 6 + 14 = 66 days, the packet's 66. The days, the keys (`data.parquet`, then `manifest.json`, at the SAME keys), the per-day allowance table of the packet's section 1 (ten October days, 844 and 798 rows at most), the expected PARTIAL and FULL counts and every after-read are unchanged; only the grouping of days into events changes. The allowance days fall in events 9 and 10.

## 3. What replaces the Act 3 dry run

The two small dry runs above stand as the Act 3 measurement; no 25-day dry run is made. Branch C of the packet is read per event: STOP, before the next event, on any `Task timed out`, a Max Memory Used above 819 MB, or an event that takes more than 720 s (the packet's own time line); a stop leaves the earlier events as written (each is complete and consistent on its own days) and the prior versions are the rollback. A stopped event is re-cut smaller by a further addendum, never retried at the same size.

## 4. Writers, blast radius, client-facing sentence

Unchanged from the packet: ONE rule (`write_day`), ONE enabled schedule, reserved concurrency 1; overwrites two keys per day for 66 days at the same keys, prior versions kept; no delete, no schedule change; no client-facing sentence moves (count 0 read before the write, as in the COO half section 4). The scheduled fire (08:15 New York weekdays) must not overlap an event (packet condition 3): events run on Friday 2026-10-16 evening or the weekend, none after 2026-10-19 11:45Z.

## 5. The question for the CTO (one)

Countersign this addendum (ten events for four; same days, keys, allowance, limits), or refuse. A countersignature is a file in `deliverables/1.0.0_SA_CTO~DELL2/` naming this file's sha256.
