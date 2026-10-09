# HANDOVER -- IRPT_CUSTDY to IRPT_DASHBD (`2.0.0_SA_COO~K2` -> `2.0.0_SA_COO~D2`), DRAFT

**Status: DRAFT.** It is sent at `~K2`'s next drain-end, after the svc-custody-statement mint pair lands (the one act in flight
the ruling leaves with `~K2`). Ruling: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_IRPT_PERFORMANCE_CONSOLIDATION_20261009.md`
@ca5f74553d (msg 2413). IRPT_CUSTDY closes as `superseded_by: IRPT_DASHBD` at this handover, with its FWDs mapped. The mapping is
the CTO's CONSOLIDATION addendum; this file does not number new ids.

Naming: the product is the "Performance client statement" (Andrew-direct ~21:2xZ, @b15e76c232). Code ids are unchanged:
`CUSTODY_REPORT`, `irpt-custody-x10-v1`, `custody-report-read`.

## 1. Open orders (task-orders/, 21 files; 19 complete, 1 superseded, 1 pending)

| order | cell | state | what it waits on | resumes under |
|---|---|---|---|---|
| `TO-CU-g-2a` | CU-g-5 (E2a): one real Performance client statement retained + persisted | `pending`, HELD by AMENDMENT 1 @d2a0d31e7f; never spawned on the current text | (1) irpt-ycharts-generate release 6 live (TO-APPLY-Y77); (2) `~P2`'s writer cells IB-pr-385 (built, proof VALID @07218e4cb3) + IB-pr-387, released; (3) the svc-custody-statement mint pair landed | `~D2`: recut as an APPLY order to `0.7.0_AE_CloudOps~DELL2`, which holds the token (ruling line 27) |

**Uncut cell:** CU-g-6 (E2b). The statement's export reaches READY through the PROD print page; one rendered statement is read
against hop 3 (JUDGMENT, CVO). Its gate: the print page is on portal DEV (fd345aef, landed 04:2xZ, msg 2408, CTO-approved msg 2392).
PROD is Andrew's word (dell2 open-calls row `dell2-20261008T192510Z-0347`).

## 2. FWD-1..9 status (orders served FWD-1 x20, FWD-9 x1; FWD-2..8 x0)

| FWD | status at handover | evidence |
|---|---|---|
| FWD-1 (one statement end to end) | hops 1-4 real for 18 of 18 accounts (CTO round-6 analysis section 1). Hop 5: server half live (IB-pr-364/378); real statement NOT yet run (CU-g-5); render through PROD NOT yet (CU-g-6) | round-6 analysis; rows W18-S1, S15 |
| FWD-2..FWD-8 | no IRPT_CUSTDY order served them. FWD-5 (BD comparisons) folds into DASHBD FWD-8 (ruling item 4) | order census: outcome_ref over 21 orders (FWD-1 x20 incl. the superseded CU-c-3 and the pending CU-g-2a; FWD-9 x1) |
| FWD-9 (where Opal gets each BD figure) | map BUILT and read for every field of one real BD 49F report. 7 Run Report bases, 32 pages, 49 fields, 70 rows: 47 MAPPED, 23 MISSING (18 BD-only classification tree, 4 benchmark, 1 MTD period). Structural only: no figure tied out | `deliverables/0.9.0_WK_IRPT_CUSTDY~17/BD_FIELD_MAP_CU-g-3.{json,md}`, drained @63cef63eab; leak check CLEAN (1,671 tokens) |

## 3. Template state

- **ClientReportDocument** (portal) carries `as_of_date` (CU-g-4) and the mixed-document refusal (E1). It is on portal DEV (landed
  d1b21c970c and onward).
- **The print page** (PrintEntry admits custody-report, mounts ClientReportDocument) is on portal DEV at fd345aef. It is not on PROD.
- **The Black Diamond layout baseline** is `deliverables/0.9.0_WK_IRPT_CUSTDY~17/LAYOUT_BASELINE_CU-g-3.md`. Gaps the template lacks:
  - the Value Summary table over four periods with benchmark rows;
  - the allocation donuts and the performance line chart;
  - Summary of Portfolio Accounts;
  - Holdings Overview by class;
  - the two gain/loss sections;
  - the page header band;
  - the MTD and last-12-months periods;
  - landscape orientation.

  BD puts portfolio pages first, then three per account. These are enrichment inputs for the merged project.
- **Client data:** the BD PDF stays outside the repo (C:\Users\Test\Downloads\17752262.pdf). Only names and counts are in the record.
  The field-map tools are LOCAL, never deployed (no-deploy declaration @ff6a14d121).

## 4. Open rows (surprise channel)

comp-surprise reports `open: 7, armed: 0`. By latest disposition: 6 UNDER_INVESTIGATION and 14 GRADUATED. The two counts differ by
one, and this file does not reconcile them; re-read at the handover.

- **UNDER_INVESTIGATION:**
  - **W18-S1 (BLOCKING):** the live generator refused custody submissions. Its remedy is in flight: release 6, IB-pr-385.
  - **S13:** an empty accounts array renders a shell.
  - **W17-S1..S4:** raster charts; the empty portal submodule in a worktree; the Portfolio basis only (a Relationship-basis report
    is an enrichment input, and is no longer egress-blocked, law 4597dfacc6 / 4d77a9c3ea); Write-tool non-ASCII.
- W9-S3/S4 read hazard `ARMED` but are DISMISSED_WITH_REASON by C-S4 (latest).

## 5. Carried artifacts `~D2` inherits

- The svc-custody-statement mint pair (COO half; signed by `~K2` before the handover).
- ADDENDUM 2 of round 7: the E2 split into CU-g-5 / CU-g-6.
- The draft E2a criteria (CU21-AC1..AC3), in TO-CU-g-2a.
- Rotation of the svc-custody-statement token: due 14 days before exp. The owner moves to `~D2`.
