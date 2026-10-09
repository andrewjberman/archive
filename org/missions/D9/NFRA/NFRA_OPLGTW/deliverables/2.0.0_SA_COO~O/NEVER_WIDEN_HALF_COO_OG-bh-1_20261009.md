# Never-widen half (COO) -- OG-bh-1, the full history of the Tax SMA master 08403355

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~08:2xZ.
Against: the ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~46/NEVER_WIDEN_ASK_OG-bh-1.md`, drained
@b94791df35 (worker commit 298a89d708). The CTO half is `1.0.0_SA_CTO~O`'s.

## The scope, from Andrew's own words

The census found the source starts 2023-10-03: 758 dates and 6002 files, not "maybe April 2026". Andrew's follow-up,
verbatim (record @98c4e6a47f): *"That means doing full backfill, it probably doesnt go even 1 year, i expect maybe april
2026."* The order he gave is the FULL backfill; the April date was his estimate of where the source starts, not a cap.
Row Z-W46-S1 reports the difference, and this half carries it to him through the record, not as a gate.

## SIGNED: section 7, the decisions

1. **Era A (2023-10-03..2024-09-26, 248 dates, 526 files, rld and tcf only) is IN scope.** 08335338's own bronze also
   reaches back to 2023-07-12, so "EXACT SAME" includes the early era. It runs last anyway (batches B8-B9, newest first). A
   date in era A whose record does not qualify goes to `unavailable` with the producer's reason. It is never guessed and
   never forced, and it does not stop the run (see 3).
2. **Pace as asked.** Nine batches of about 700 files, newest first, plus the closing 2000-day run. Strictly one puller in
   flight. The gate between batches is: every date of the batch read back, the DLQ at or below its depth at the batch's
   start, and the converter's Throttles and Errors named. The quiet windows are `[09:15,11:35)Z`, `[21:15,23:35)Z` and
   `[12:00,12:50)Z`: start outside them and finish before them. Batch 1 is the measurement: its puller minutes and silver
   drain time go into the backfill record before batch 2 starts. The worker does not report and wait between batches.
3. **Stop rule, the worker's with two edits.** STOP and report on any of these:
   - an era B or C date whose record reads not qualified for a reason other than missing sibling files;
   - any puller `Die` other than 7;
   - DLQ depth ABOVE its depth at the batch's start (the queue is shared, so the baseline is measured, never assumed 0);
   - a puller that did not start (Administrator console logged off).
   Era A non-qualification is recorded, not a stop. No blind retry.
4. **No leg for the applier.** No deploy, no Terraform, no grant.

## SIGNED: sections 2-6, the blast radius

- **Write set.** Everything is under `schwab/08403355/` only: bronze 6002 zips, about 7,483 silver objects, 758
  completion keys (with versions as closures recompose), run manifests, the puller's run records, and
  `meta/backfill-status.json`. There is no delete, setting, notification, policy, grant, Lambda or Terraform change, and
  nothing under 08242234, 08335338 or `opal-data-schwab`.
- **Writers, N printed.**
  - 1 principal for bronze, `_ops` and `meta/pulls`: the box role.
  - 1 principal for silver and `meta`: the converter role.
  - `meta/complete/` has 2 call sites of one function. The `:922` unconditional fallback writes a record that never
    qualifies, so a date it touches ends `unavailable` and is never served.
- **Consumers, both branches.** The bucket has 12 notification configurations; the one on `schwab/08403355/` is the
  converter.
  - Converts: silver, a manifest and a closure recompute.
  - Skips: a hole type, or an already-landed key, writes nothing downstream.
  - No 49F accelerator or gold dispatch reads 08403355 (live read 2026-10-09), so no gold run can start.
- **What moves in the world.** The gateway starts serving the newly qualified 08403355 dates, inside each principal's
  existing grant window. No grant changes. This is the served-output move this pair signs.
- **Rollback per key.** The prefix is empty today, so every written key is a first version. Rollback is
  `delete-object --version-id` per recorded version, by the operator identity, in the ask's order (completion records
  first). Keys the scheduled 10:45Z/22:45Z pulls write are not this order's and are not rolled back.

## Not covered

The 49F accelerator for 08403355 (Andrew's word needed). Any change to the puller, converter or schedule.

-- 2.0.0_SA_COO~O
