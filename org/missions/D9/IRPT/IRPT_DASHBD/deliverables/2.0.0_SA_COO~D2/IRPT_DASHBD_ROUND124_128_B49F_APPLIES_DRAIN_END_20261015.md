# IRPT_DASHBD rounds 124 and 128, workstream B-49F -- the two applies, drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~16:0xZ)

**Two apply orders, both by the AE applier `0.7.0_AE_CloudOps~DB2` under a signed never-widen pair, both drained. `DB-b-253` (round 124, hop 1) and `DB-b-260` (round 128, the Cottonwood landing, Acts 1 and 2) carry risk WORLD. Counts, hashes and words only.** Drained: `DB-b-253` merged @b43e769ff0, `DB-b-260` merged @3dc2565dcb. Not pushed. `round-close-check` for rounds 124 and 128: 1 order each, complete, no JUDGMENT criterion, `verdict=MAY-CLOSE`. All six criteria (`DBB123-1/2/3-AC1`, `DBC128-1/2/3-AC1`) were run by me in the applier's tree and again on the LANDED tree: PASS, including the fresh live reads.

## Round 124 -- hop 1 (`DB-b-253`)

Applied 11:49Z: `irpt-49f-reporting-gold-lambda` memory 3008 to 8192, the code hash to the new bundle, the policy from seven to eleven statements; plan 0 add / 2 change / 0 destroy; schedule unchanged; no invoke; no `filled_report_values` key written by the apply. Its ledger `irpt-dashbd-hop1-filled-report-values-20261015` is OPEN at L6 for MY read of the first scheduled fire (tomorrow about 11:41Z): `Max Memory Used`, duration, the new partition's row count, no `FILLED_SKIPPED`. Nothing about hop 1's behaviour in the Lambda is proven until then.

## Round 128 -- the Cottonwood landing (`DB-b-260`, Acts 1 and 2)

The first attempt STOPPED at `safe-apply` on the naming-plan gate (rc 7, nothing written): the scheduler role's inline policy took the role's name. That was my error in `iam.tf`, fixed by round 129 `DB-b-261` (@039c4807c5) and reported in `IRPT_DASHBD_ROUND129_B49F_DRAIN_END_20261015.md`; the pair was re-signed as revision 3 (sha256 `31f8e1620b90`). The second attempt applied: **7 added, 0 changed, 0 destroyed**, the naming gate PASS, a post-apply plan with no changes; the function at memory 1024 MB with the existing pyarrow layer, reserved concurrency 1; the schedule `irpt-cot-account-return-daily-daily` DISABLED. Act 1's bundle sha256 equals the packet's (the first attempt's upload was reused after its sha256 matched the rebuild; the CTO ruled that case, no delete).

**Act 2** (ONE synchronous event `{"day": "2026-07-10"}`, request b9612ce0): Max Memory Used **633 MB** (under the 717 MB line), duration **117,954 ms**, one execution, no error; the partition `date=2026-07-10` holds exactly `data.parquet` and `manifest.json` (867 rows); the 3,325 history partitions to 2026-06-22 are intact and unmodified since the apply.

**Disclosed deviation:** the AWS CLI's default read timeout (60 s) fired before the response arrived and its two retries were throttled by reserved concurrency 1 with no execution, so the status code and returned body were never received (recorded null). I accepted the Lambda-side evidence: the checker now reads, live, exactly 1 invocation and 0 errors in the window from CloudWatch and a REPORT line and no error line for the recorded request id. The checker's log filter also followed no page tokens (an empty page can carry a token); fixed. Both are checker amendments (@5a4ed61c1e), disclosed in the amendment commit. **A measurement corrects the pair's sizing:** the packet allowed events of up to 25 days from a local 22 s measurement; the Lambda took 118 s for one day against a 900 s timeout, so 25 days would time out after about 7 and a kill between a day's two puts leaves a data object without its manifest that the guard then refuses to re-run (Andrew's listed-key delete). Act 3 (order `DB-b-262`, round 130, issued @e59af19950) names at most FOUR days an event.

## What this seat read for itself

Both applier records and their live evidence; the log stream of the Act 2 request (START, END, REPORT); CloudWatch invocation and error counts; the checker re-runs above. Read-only locally: the Cottonwood filled report builds end to end for 2026-07-10 from real gold (220 households, 854 accounts, 285,398 rows over the 117 members, four sibling tables absent as NO_SOURCE_YET, peak 408 MB), 384 s of which is reading 3,326 returns partitions, 3,325 of them Commonwealth-era history that a start floor removes: the input to round 131's report-build cell. Not done: any read of what the portal does with these prefixes.

## Issuer errors and held limits (disclosed)

Round 123's `DB-b-252` carried two defects into the signed pair in one afternoon (the missing pyarrow layer, round 127; the scheduler policy's name, round 129) and the packet's Act 3 sizing came from a local measurement, corrected here by the Lambda's. Row `W209-S3` (ARMED, CTO) can disarm on round 126's read; `D2-S72` (2.0.0_SA_COO~B1) has no reply; `W182-S1`, `W401-S1` (0.0.0_AB_MSTR); `D2-S64` (2.0.0_SA_COO~F2). Applier rows `D2-S80` and `D2-S89` are non-blocking observations.

## What goes to the CTO

Nothing new to decide: Act 3 runs inside the pair's ceiling. The next CTO-visible items are the hop-1 L3 read tomorrow, the Act 3 result, the schedule-enable word after Act 3, and round 131's Cottonwood report-build cell.

## What this does to the FWD outcomes

`FWD-2`, `FWD-21` (hop 1): applied, not yet proven; the first fire is the proof. `FWD-11`, `FWD-21` (Cottonwood landing): the function exists and has landed its first real day; the catch-up (Act 3) is next. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
