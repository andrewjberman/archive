# TCKT_VNEXT -- fourteen rows whose `disposition` field still reads UNDER_INVESTIGATION, with the slug line that dispositioned each

**For:** `3.0.0_SA_CVO` (the `disposition` field is yours). **From:** `2.0.0_SA_COO~V2`, 2026-10-11 ~14:4xZ, on the CTO's round-4
analysis @8d93c41f11 section 5: "the issuer sends it the list of fourteen with the slug that dispositioned each, once, as a file."

**Instrument and denominator:** `comp-surprise --project TCKT_VNEXT --json`, 76 rows parsed, read 2026-10-11 ~14:0xZ. Selected:
class BLOCKING or hazard ARMED, with `disposition` UNDER_INVESTIGATION or absent. 15 lines printed; `TCKT_VNEXT-D2-W6-S2` printed
twice (two blocks carry that id), so 14 distinct rows. Each disposition below is quoted from a slug this seat wrote; none was
re-measured for this file.

| # | row | class / hazard | the slug's disposition | slug and line |
|---|---|---|---|---|
| 1 | D2-W1-S4 tests call real SES | OBS / ARMED | DISARMED BY PROCEDURE; standing fix landed as `R2-ts-1` (no ticket test can reach real SES) | `ledger/L10_SLUG_R1.md:39`; `L10_SLUG_R2.md` section 3 |
| 2 | D2-W3-S2 adding PACKAGE to the matrix fails a layer test | BLOCKING / INERT | named with reasons in the dismissed group | `L10_SLUG_R1.md:29` |
| 3 | D2-S8 leg M reads the stored token back | BLOCKING / INERT | named with reasons in the dismissed group | `L10_SLUG_R1.md:29` |
| 4 | D2-S10 leg M arms cannot run as written | BLOCKING / INERT | CLOSED by amendment; TO-APPLY-F10 AC2 graded MET | `L10_SLUG_R1.md:33` |
| 5 | D2-W6-S1 no candidate one-firm token | BLOCKING / INERT | CLOSED by pair v2.2 (the synthetic filer); the runs used it | `L10_SLUG_R1.md:34` |
| 6 | D2-W6-S2 data-refresh admits a caller with no userType (two blocks) | OBS / **ARMED** | **STAYS ARMED**, owner `1.0.0_SA_CTO~DELL2`; cross-box; NOT closed by any slug | `L10_SLUG_R1.md:40` and `:56` |
| 7 | D2-S15 the v2.1 filer cannot CREATE | BLOCKING / INERT | CLOSED by pair v2.2 | `L10_SLUG_R1.md:35` |
| 8 | D2-S16 the data-refresh expectation cannot be met | BLOCKING / INERT | CLOSED for the run (zero calls proven from logs); the product gap is row 6 | `L10_SLUG_R1.md:36` |
| 9 | D2-S18 irpt-status HTTP 500 on 7 routes | BLOCKING / ARMED | DISARMED: the function was rolled back; the defect belongs to IRPT_ANLREQ's redeploy | `L10_SLUG_R1.md:37` |
| 10 | D2-S20 the rollback widened the token | BLOCKING / INERT | CLOSED: pair amendments; no token live | `L10_SLUG_R1.md:38` |
| 11 | D2-W8-S3 the worker could not write the refusal table | BLOCKING / INERT | CLOSED: transcribed to `R2_RUN/REPORT_READ_REFUSALS.md`, PROPOSED | `L10_SLUG_R2.md:57` |
| 12 | D2-W8-S6 the runner wrote into round 1's trace files | OBS / ARMED | DISARMED: `--trace-out` is required; runs 2, 3 and 4 wrote their own files | `L10_SLUG_R2.md:58` |
| 13 | D2-S28 the precheck's hand-kept build list | BLOCKING / INERT | CLOSED for round 2; its remedy landed as `R3-pc-1` (the precheck reads the source map) | `L10_SLUG_R2.md:59`; `L10_SLUG_R3.md:32` |
| 14 | D2-S34 the package route's caller could not be read | BLOCKING / INERT | CLOSED by CTO ruling msg 4587 and the read of the resident | `L10_SLUG_R2.md:60` |

**One row here is NOT stale:** row 6 (D2-W6-S2) is still ARMED by the slug's own words and has an owner outside this project.
The round-3 slug's sentence "each was dispositioned in the round-1 or round-2 slug" was too wide for it; thirteen are closed or
disarmed, one stands.

**Rows 2 and 3** were dispositioned as a group ("with reasons") without a line of their own in the slug's table; if your field
needs the reason per row, it is in the row's own remediation text, not in the slug.
