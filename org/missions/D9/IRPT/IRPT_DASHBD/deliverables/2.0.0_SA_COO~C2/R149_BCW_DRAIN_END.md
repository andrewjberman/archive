# IRPT_DASHBD round 149, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-16)

FWD-10 for 49 Financial: the coverage census of the gold tables and the labelled test read of the published series through the page (cell DB-c-29, read only). Issuance `8c1db7c3f3`; merge `5379548cdb` (worker ~420). Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md` section 18. `python .tools/round-close-check.py --project IRPT_DASHBD --round 149 --workstream B-CW`: `verdict=MAY-CLOSE` (1 order, 0 judgment). `DBC150-1-AC1`, `-AC2` and `-AC3` PASS, re-run by this seat (AC1 and AC2 make their own fresh S3 reads); `proof-of-spec-check` VALID rc=0. Push: integrator-only; the merge and this commit are LOCAL.

## What was measured (TEST READ, counts only; no identifier, key or value in any file)

- **Where the data starts.** `account_return_daily` holds 571 date partitions from 2024-07-08 to 2026-10-14 and `holdings_performance_daily` 570 from 2024-07-09 to 2026-10-14. Of the 6,949 published series, 4,097 start after the gold first day (the oldest start on it).
- **Which trading days the source did not report.** The gold census finds ZERO absent trading days and zero runs in either table over the whole span. No published series carries the unreported-days pair (0 of 6,949) and none carries `income_claim`: the 49 Financial source makes no such statement, so by the contract's rule the page prints nothing about unreported days for it. The page therefore cannot separate "no trading day is missing" from "not measured".
- **How current.** `as_of` is 2026-10-14 on 6,946 series; three end earlier (2026-10-02, 2026-10-12, 2026-10-13). The page prints `Data through <as_of>` on the Performance panel.
- **What the page does with them.** All 6,949 series are read by the page's reader (0 refused, 0 threw, 0 income coerced to zero; income holds numbers in all of them, unlike the Cottonwood publish). `history_scope` is `PARTIAL_HISTORY` on all 6,949, including accounts whose first day equals the table's first day, so the round 146 note `Returns from <date>.` prints on every 49 Financial account. A day-quality sentence prints for 6,945 accounts; the excluded-days note for none. Day-quality day totals: MEASURED 2,578,713, LARGE_FLOW 44,505, FLOW_UNRECONCILED 6,139, NOT_MEASURABLE 57,492; return-basis totals TWR 2,623,218 and NOT_MEASURABLE 63,631 (equal to NOT_MEASURABLE plus FLOW_UNRECONCILED).
- **Not established:** the kind of 4,344 other objects under the series prefix (`W420-S2`); whether `PARTIAL_HISTORY` for a series starting on the table's first day is intended (the scope flag does not separate them).

## What the CTO's half decides (no build cell of this workstream follows without a word)

1. **Should the 49 Financial series state its unreported days?** The gold partitions would let the publisher write the pair from the calendar (here an empty list, a statement "no trading day is missing"). Today the page says nothing, which reads the same as "not measured". The series' producer is `~D2`'s (workstream B-49F); I cut nothing.
2. **Is `Returns from <date>.` on every 49 Financial account the wanted reading?** You ruled it so for Cottonwood (msg 9187). For 49 Financial the same rule applies to a population where the scope is `PARTIAL_HISTORY` even for accounts starting on the table's first day; stated for your ruling.
3. **The next B-CW cell.** Inflection has no data yet (nothing to census). The remaining B-CW items are the parked first scheduled Cottonwood report-run read (2026-10-16T16:00Z) and whatever your next analysis names.

## Rows

`D2-S112` (this commit) dispositions worker 420's `W420-S1` (no 49 Financial document carries the pair) and `W420-S2` (the 4,344 other objects), both INERT. Nothing ARMED or BLOCKING of this round.

## Issuer's own defects this round

None found in the cut or the drain (the proof instance carried its order stem, so `round-close-check` read MAY-CLOSE first time). One note: the worker deviated twice, both harmless: it left the order's status to me (as the BOUNDS say) and it wrote the partition template on the command line, not in a script, to stay clear of the identifier-token check.
