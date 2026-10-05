# Andrew-direct, 2026-10-05 ~14:3xZ, in 2.0.0_SA_COO~Y's session (IRPT_YCDGEN issuer) -- VERBATIM

> When you are doing these ycharts runs, it is very important that we assess exactly what the shape of the payload
> (field-level contracts) for each of the four APIs. Then when we run their generation "GET" to compile it, we want to
> cross-reference that file (each variant 1 2 3) with the contracts/content of those four underlying API calls. The
> reason for doing this, is because I believe this process should be largely migrated to Opal AWS. Our goal is to take
> over this process and run it internally, not have to rely on YCharts, because of the tenuousness/slowness of their
> connection and processes. If you have already gotten all the information on payload shape and test export compiled
> packets for each of the 3 variants, then I want to pivot to studying these and assessing how we can rebuild it in our
> cloud, with a focus on doing as much as we can do sleekly on premises and ideally reducing dependencies on YCharts to
> zero.

## What this seat does with it (scope relayed verbatim, not widened)

1. **Field-level payload contracts** for each of the four API calls, from what is measured and kept: the kept answers
   and their shapes, the generation recipe and its HAR-measured fixtures.
2. **A cross-reference of each compiled variant file** (1 Overview, 2 Comparison, 3 Multi) against those contracts: for
   every element of each report, which call's field it comes from. Where none does, whether it is our own input, a
   YCharts computation, or boilerplate.
3. **The pivot study:** how the process is rebuilt in Opal's cloud, as much as possible on premises, with YCharts
   dependencies reduced toward zero. Each remaining dependency is named, along with what replaces it.

## Routing

- The study (1-3) is this seat's act now.
- Building the in-house process changes IRPT_YCDGEN's endpoint (its PRD names YCharts' endpoints as the source), so the
  build goes through the canonical chain: the brief is 4.0.0_SA_CRO's and the endpoint is 1.0.0_SA_CTO's. This seat sends
  the CTO this record and the assessment. No other seat's work is gated by it.
- Round 5's close acts stay in flight until the study's findings say otherwise:
  - E6, the budgeted live Overview, is held only by a runner defect, fixed today;
  - E4 is FWD-2's after-close run.
