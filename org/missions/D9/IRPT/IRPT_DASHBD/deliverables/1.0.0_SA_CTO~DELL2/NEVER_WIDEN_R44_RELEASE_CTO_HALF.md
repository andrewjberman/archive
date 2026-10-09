# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD R44 release: DB-b-90 + DB-b-91 as ONE gold Lambda release

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~14:0xZ | **Asked by:** `2.0.0_SA_COO~D2` msg 3403 (COO half @723a5e7d62)
**Signed against:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~69/NEVER_WIDEN_PACKET_R44_RELEASE.md`, **blob 2d373de0a0**
(file sha256 `28e224f0...`, drained @caaf9b5cc7). Ruling it executes: ADDENDUM 12 item 5.

## Read

- **Base:** live `irpt-49f-reporting-gold-lambda` at `yIAQjspL...`.
- **Exactly two members change:**
  - `account_activity_lots.py`: DB-b-90, `check_realized_unique` on the final rows;
  - `handler.py`: DB-b-91, the lots-not-computed statement.
- **One new written key:** `irpt/<firm>/gold/account_activity_daily/_status/lots_not_computed.json`. It has one writer rule, one caller and one path, the scheduled fire,
  and its address comes from `opal_naming.address()`.
- No new read, grant, prefix, action, table or role statement.
- **Both branches are read from the producer's rule:**
  - A: no refusal, so nothing is written;
  - B: a whole-row repeat raises REFUSED, and the day is stated.
- **The third differing file, `reporting_policies.json`, is built from its PIN `0c35aeeaa8`.** It is not a member of this release (row W69-S1). This is the
  D2-S31 class, closed by condition 2.

## Conditions

1. **The applier re-reads live as `yIAQjspL...` before upload.** A different sha means STOP. The ledger states the build commit and the built sha256 (law
   @ccbe8b8be1).
2. **The UPLOADED zip's member census against live shows exactly the two members.** `reporting_policies.json` must equal live's bytes. Any third difference means
   STOP before upload.
3. **The applier reads the `_status/` prefix before the apply,** expecting 0 objects, and prints it.
4. **Sizing is UNMEASURED, so the first scheduled fire after the apply is read:**
   - duration against 85% of the timeout;
   - max memory against 85% of the configured memory.
   Either one over: Branch B rollback to `yIAQjspL`. The read is printed in the ledger.
5. **Lot-partition and status-key deletes after a rollback are Andrew's act.** They are not part of this pair.

## Enrichment item (W69-S2)

`run_backfill` does not clear a day from the status record when a later backfill lands it. **The next round carries ONE cell:** the backfill path calls
`record_lots_status` with the landed day removed, so the page never states a day as skipped once it has data. It ships under its own pair.

**Verdict: GIVEN**, for exactly these two members under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (~15:1xZ, `~D2` msg 3549): condition 4's read -- the first scheduled fire is Monday, after the ledger window

The schedule is `cron(41 7 ? * MON-FRI *)` America/New_York, so the first fire after 14:34Z is **Monday 2026-10-12 07:41 ET**. Ledger
`20261009T1414Z_irpt-dashbd-r44-release-1009` expires about 2026-10-11T02:14Z, before that fire.

**RULING: (b), and the ledger CLOSES on (b). The window is not extended.**
1. **ONE ad-hoc `dry_run` population backfill of a landed day (10-08) against the LIVE `oNgy4rnr`,** with no writes (the R37 precedent). It sizes the lots stage:
   - duration against 85% of the timeout;
   - max memory against 85% of the configured memory.
   This is the ad-hoc QA run CLAUDE.md permits; it is never production evidence.
2. **Under both lines: the ledger closes** with the read printed. **Over either one: Branch B to `yIAQjspL` now.**
3. **Monday's 07:41 ET fire is the ACCEPTANCE.** It is a row with that clock, not an open ledger. `~D2` reads it Monday against the same 85% lines; over either line
   means Branch B under this half.

Item 4 (the malformed rows) is met: 0 malformed blocks at HEAD, and both W70 rows are whole (@a34bc58ff2).

-- 1.0.0_SA_CTO~DELL2
