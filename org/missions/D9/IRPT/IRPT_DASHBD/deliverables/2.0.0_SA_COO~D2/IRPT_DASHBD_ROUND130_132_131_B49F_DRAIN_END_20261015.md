# IRPT_DASHBD rounds 130, 131 and 132, workstream B-49F -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~17:4xZ)

**Three rounds, all drained: round 130 (`DB-b-262`, Act 3 of the Cottonwood landing, WORLD, by the AE applier), round 131 (`DB-b-263`, the Cottonwood report-build handler, WORLD by the floor of its `infra/` path, no AWS write) and round 132 (the value-level read of the landed 2026-07-10 day, a LOCAL direct act, GET and LIST only). Counts, hashes and words only.** Merged: `DB-b-262` @691b95c160, `DB-b-263` @3cc2e295c0; the round-132 record @9d24eac8b6. Not pushed. `round-close-check` for rounds 130 and 131: 1 order each, complete, no JUDGMENT criterion, MAY-CLOSE. Every criterion was run by me in the worker's or applier's tree and again on the LANDED tree: PASS (`DBD129-1-AC1`, `DBD129-2-AC1`, `DB131-1-AC1..AC3`, `DB132-1-AC1`, `AC2`).

## Round 130 -- Act 3: the Cottonwood catch-up landed

64 days, 2026-07-13 to 2026-10-14, in **16 events of four days**, one synchronous invoke each, no retry, all status 200, nothing held, **Max Memory Used at most 627 MB (the 717 MB line), longest event 436 s (the 700 s line; about 109 s a day)**. The gold prefix now holds **3,390 partitions = 3,325 history + 2026-07-10 + the 64 new days**; every new day holds exactly `data.parquet` and `manifest.json`; the history partitions are unmodified since the apply; the function (1024 MB, 900 s) and the schedule (DISABLED) are unchanged; a REPORT line in the log group equals each of the 16 events. Three trading days with no Black Diamond silver pair (2026-08-19, 2026-09-24, 2026-09-25) were not named: the landing has no partition for them and the filled report will not either. The ledger `irpt-dashbd-cottonwood-account-return-daily-20261015` is CLOSED by me with that proof (all five legs). **The schedule is still DISABLED; enabling it is the CTO's separate word.** **Timing is n=17** (the first day's 118 s, then 16 events of about 109 s a day), not a standing guarantee.

**The sizing correction, disclosed:** the packet's 25-day events came from a local 22 s measurement; the Lambda measured 118 s for one day, so the order named four days. Two checker clauses failed honest records and were amended at the applier's report (the packet sha256 constant held revision 2; the handler returns `held` as the count 0).

## Round 132 -- the value-level read of 2026-07-10 (the CTO's round-128 binding, msg 8462)

The landed file (written by the layer's pyarrow **14.0.2**) re-read and compared with a reference derived locally by the same adapter code under pyarrow **25.0.1** from the same silver: **867 rows, the account and date key set equal, the same 11 columns, 1,734 float values over 7 columns equal (maximum absolute difference 0, the line was 1e-12), no non-float cell differs**; the landed file loads under a pyarrow 14.0.2 interpreter (a private environment outside the repo) with the same rows and key set. `DB132-1-AC1` and `AC2` PASS (the checker re-derives and re-reads everything itself). **A correction to the CTO's reading, offered not asserted:** the Cottonwood holdings-performance function does not read `account_return_daily` (read in its handler and producer); the 14.0.2 consumer of this table is the report-build function (round 131), whose own Lambda-side read is the first event of its apply. Only 2026-07-10 is value-compared; the 64 later days are graded by rows, objects, memory and duration.

## Round 131 -- the Cottonwood report-build handler (cell 1 of 4)

`infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py` with 21 tests: the `filled_report_values` stage for firm cottonwood only, one invocation per owed day with ONE `Event` self-invoke of its own ARN, a start floor of 2026-07-10 on the returns listing (3,325 Commonwealth-era partitions are never listed or opened), no overwrite of a landed day, one `put_object`; imports pyarrow only. The checker's probe stages the handler as packaged and runs it against a fake S3; it passed a scratch reference handler and failed six mutants (no floor, overwrite, dry-run put, synchronous chain, another firm, not-oldest). The worker's one deviation: the face's `FIRM = "cottonwood"` literal was refused by the commit-time naming gate and now reads the registry (`opal_naming.lookup("cottonwood")["key"]`). My read-only local run of the real build for 2026-07-10: 220 households, 854 accounts, 285,398 rows over the 117 members, four sibling tables absent as NO_SOURCE_YET, peak 408 MB.

## Issuer errors this period (mine, disclosed)

The landing pair carried three defects into signing from my round-123 order (no pyarrow layer; a role name on a policy; five builder names counted where six exist) and two checker constants were stale (packet revision; the `held` shape). In round 133's cell 2 the commit-time gate also refused a firm token I typed in the source-map entry's carriers; the order is amended (neutral token `iso`, row `D2-S90`), the worker resumed. The report-build checkers now run the real naming gate and read the layer before any worker commits.

## Rows held (owners named)

`W209-S3` (ARMED, CTO; disarmable on round 126's read); `D2-S72` (2.0.0_SA_COO~B1, no reply); `W182-S1`, `W401-S1` (0.0.0_AB_MSTR); `D2-S64` (2.0.0_SA_COO~F2). No ARMED row has a dark owner as far as this seat can read.

## What goes to the CTO

The schedule-enable word for the landing function after Act 3 (revision 3's terms): this seat recommends YES, with the first scheduled fire read by me. Cells 2 to 4 of the report build follow (round 133 in flight, then the pair, then the apply and first events). Hop 1's first fire is tomorrow around 11:41Z.

## What this does to the FWD outcomes

`FWD-11`, `FWD-21` (Cottonwood landing): landed from 2026-07-10 to 2026-10-14; the schedule is the remaining act. `FWD-1` (Cottonwood thread): the report build is cells 2 to 4. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
