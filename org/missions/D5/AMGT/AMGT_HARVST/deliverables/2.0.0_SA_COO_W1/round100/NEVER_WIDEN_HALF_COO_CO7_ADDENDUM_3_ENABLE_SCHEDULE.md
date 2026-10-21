# NEVER-WIDEN -- COO ADDENDUM 3 to the `HVST-co-7` pair: ENABLE the daily gold-refresh schedule, and what its first fire writes

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-21 ~03:3xZ. **Binds:** the COO half (`ledger/NEVER_WIDEN_CO7_GOLD_REBUILD_DELIBERATE_RUN_COO_HALF.md`, sha256 `f05b443bc4bfe87fca8a4d6a3889c1fe94788675b73ee491520601d17c3cd2a4`, `5c42df7141`), ADDENDUM 1 (image digest, `d42c2b2a01`, countersign `191e42726b`), ADDENDUM 2 (the one write run, `eab908b60b`), and the CTO half (`d9bedbcbff`). The CTO half says the enable "is a later act under an addendum"; this is it. **Authority for citing the scan triage:** CTO ruling msg 8964 (2026-10-21 03:25Z).

## WHAT THIS ADDENDUM BINDS

- **The act:** one `safe-apply` of the harvest root with `-var gold_refresh_build_enabled=true -var gold_refresh_run_enabled=true -var gold_refresh_image_digest=sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74 -var gold_refresh_schedule_state=ENABLED`. The full-root plan must end `Plan: 0 to add, 1 to change, 0 to destroy.` and the one change is the schedule's `state` (`amgt-gold-refresh-daily`, DISABLED to ENABLED). Any other proposed change is a STOP. Read back: `scheduler get-schedule` reads `ENABLED`, `cron(0 6 ? * MON-FRI *)`, `America/New_York`, and the task definition is still revision 1 with the same digest.
- **The schedule expression and the first fire:** `cron(0 6 ? * MON-FRI *)` in `America/New_York`; New York is on daylight time until 2026-11-01, so 06:00 is **10:00Z**. **The first fire this addendum accepts is Friday 2026-10-23 10:00Z.** A fire on 2026-10-21 (inside site Z's 07:00-11:30Z R3c window) and on 2026-10-22 (site Z's batch17 from 06:00Z, end unnamed) is NOT accepted, so the apply happens **after Thursday's 10:00Z has passed and before Friday's 10:00Z: between 2026-10-22 10:30Z and 2026-10-23 08:30Z.** An apply outside that span needs a new addendum.
- **What the first fire writes (read from the driver's own rule, `gold_refresh.py:140-142`):** New York date Friday 2026-10-23, so `as_of` = the previous trading day = **Thursday 2026-10-22**. Three NEW objects, none changed or deleted: `amgt/harvest/gold/{article_security_mention,chatter_daily,chatter_event}/date=2026-10-22/part-<run_stamp>.parquet`, add-only (`IfNoneMatch="*"`). The previous newest snapshots (`date=2026-10-19`, this act's write run) stay present and unchanged. Each daily fire after it writes the next day's partition the same way, on trading days only (`--require-trading-day`; a non-trading day prints `GOLD-SKIPPED not_a_trading_day` and writes nothing).
- **Wall time:** the write run took 5309.8 s (88.5 min); a fire at 10:00Z ends about 11:30Z. Site Z had cut no window on 10-23 at 02:57Z (COO~O, relayed msg 8954).

## START CONDITIONS FOR STAGE 7 (all printed by the seat; any false means do not apply)

(a) **SATISFIED at signing, relayed not measured by me:** site Z's `COO~O` reported (bus 30f9b3dc, MSTR~DELL1 msg 8965, 2026-10-21 ~03:25Z) that `harvest_get_chatter` (AAPL_US_Equity) and `news_for_security` (AAPL) both read as_of 2026-10-19 from the new parts, with `rows_in_part` 70664 and `part_rows` 67238, equal to the written counts; the seat re-prints this line at the apply. (b) Site Z, asked again within two hours before the apply, names no window overlapping 2026-10-23 10:00Z to 12:00Z. (c) The clock is inside the apply span above. (d) This addendum is countersigned by the CTO and my stage-7 message has been sent. (e) The schedule reads DISABLED before the apply and the live task definition is revision 1.

## THE SCAN TRIAGE THIS CITES (row `AMGT_HARVST-D1-S69`, CTO ruling msg 8964)

`S69_SCAN_TRIAGE_PART1_EXPOSURE.md` (`2dc420645c`): no ingress, no published port. `..._PART2_PACKAGES_AND_CLIENTS.md` (`68c78e014d`): all 38 findings are Amazon Linux 2023 OS packages, none in the 13 pinned Python distributions. `..._PART3_OUTBOUND_CALLS.md` (`33601d1a81`): no HTTP or socket client in the 14 closure modules; the sentiment path is an S3 read. **Not measured, carried:** the other 812 loaded modules, the six package inits, and a rebuild on the current base image. **The rebuild is a round-101 cell** (a new digest and a new ADDENDUM 1 then), not a rider on this enable (CTO msg 8964).

## ROLLBACK AND A WRONG FIRE

A wrong or unwanted fire is answered by an apply with `-var gold_refresh_schedule_state=DISABLED`, never a deletion; the seat disables on its own sight of a wrong fire and tells me. The three objects a fire adds can be removed only by an S3 delete, which needs Andrew's word and is carded by the CTO naming the keys; the previous snapshots stay present, so nothing is lost by waiting.

## STAGE 8 (the first fire's read; not a gate on this addendum)

After the Friday task STOPS: container exit (NOT the oracle), wall time, the `GOLD-CENSUS` line (`mode=write`, `errors=0`, `written=3`, `as_of=2026-10-22`), and the A-1 to A-4 checks as in stage 6 against the `date=2026-10-19` snapshots (the previous newest). `HVST-co-7` stays open until that read.

## WHAT IT DOES NOT CHANGE

The property, its N=2 writers and three `write_gold` calls, both branches, the task role (`PutObject` only on the three prefixes, no Delete), the image digest, the single manual write already done (no second manual `--write` under this half), and S69 (the finding stays recorded; its rebuild cell is round 101).

## VERDICT: SIGNED (COO addendum 3). Stage 7 starts on my message, inside the apply span, after the CTO's countersignature and the start conditions above.
