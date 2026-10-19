# IRPT_DASHBD: where things stand, measured 2026-10-19 ~18:1xZ, for Andrew's test on PROD

Issuer 2.0.0_SA_COO~D2. Written under the pause (Andrew-direct 2026-10-19 ~17:0xZ): no new work is cut; this is the IRPT_DASHBD part of the clean statement the pause asks for. Counts and words only. Every line says how it was read; "NOT READ" names what no agent has seen.

## 1. On PROD now (portal)

- PROD is `8cd45f62` (tag portal-v2.1.243), read by `git describe` on origin/PROD. It contains the dell2 promote `9107d48a` (portal-v2.1.242, live 2026-10-19 16:22:04Z), read by merge-base.
- That promote carried 49 files: the Investor Reporting Performance set (the template view and its states, the performance report and export, the print window, the holdings panels, the chart breaks) and the Trade Request form, with Trade Request offered in the New Ticket list.
- DEV is `64d7fce7` and carries the same: the fold landed, and no file of those 49 differs between PROD and DEV (read).
- **NOT READ by any agent: the Performance template view rendering on PROD.** It mounts only for a real staff session with a 49 Financial client selected (the DT's ui-smoke stub cannot give that). Where to look: Global view, pick a 49 Financial client, Performance tab. It is on Andrew's test list (CTO msg 10858); P4 of the promote order stays open until he reports.

## 2. The data behind the Performance tab

- **49 Financial:** the filled-report pass is live. Its first scheduled fire (2026-10-19 11:41Z, one invocation, 494.8 s) reached the filled stage and landed it, and its whole log holds 0 FILLED_CATCHUP_LIST_FAILED lines (read by me and independently by ~F2).
- **Cottonwood (Black Diamond):** 66 gold days are landed from 2026-07-10, and 939 series are published. **KNOWN DEFECT you will see in the numbers: the landed daily external flows are inflated.** The reader summed each trade across every overlapping transaction partition. A read-only derivation of all 66 days with the corrected reader (on the trunk at 5bec535804, NOT deployed) shows the summed absolute flows more than double on 61 of the 66 days, up to 14 times on the largest. Daily returns that depend on those flows are therefore wrong on those days until the fix is deployed and the gold is rewritten. The surprise row is D2-S137 (ARMED, this seat is the disarm owner).
- **Also in the Cottonwood series:** 08-19, 09-24 and 09-25 have no gold day (their transactions partitions are awaiting dell1's re-request), so the YTD return still reads "Not measured" while any of them is in the window; the four days after the re-landed days 07-22, 07-27, 07-29 and 08-03 are mostly not measurable in the landed gold (83 to 100 percent of their rows).
- **Inflection:** ~F2's pair for Tuesday stays as signed (CTO msg 10809).

## 3. What would fix the Cottonwood numbers, and where each stands

| step | state |
|---|---|
| the corrected reader and the 14-day settle (cell TO-DB-b-333) | built, drained, on the trunk |
| the release re-pin (cell TO-DB-b-334) and the bundle build | built, drained; bundle hash agreed with ~F2 |
| the release applied to the function (with ~F2's transaction stage) | ~F2's Cottonwood pair, signed on REVISION 2, scheduled Wednesday per ~F2 |
| the all-days rewrite of the 66 gold days and one republish | packet DRAFTED, checker p201 built, apply order NOT cut: it is new work and waits for the pause to lift |
| the class series object (class_series.json.gz) | contract 0.4.0 on the trunk; the writer is not cut (the CTO ruled it after the rewrite) |

## 4. What I cannot say

I have not seen the PROD pages. Every statement above about the data plane comes from reads of logs and objects, not from a page. The pause does not change any of them.
