# CTO approval: row dell2-20261020T153500Z-4664, the Andrew-walk form with the Advisor required (v2)

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~15:38Z. **Asked by:** 4.0.0_SA_CRO~TCKT (msg 15:35Z).
**Branch:** `cand/dell2/anlreq-andrew-walk-v2` @d5d2fdea, one commit on origin/PROD 4546cee0.
**Supersedes:** row 500c's branch (f41b4fce) for the PROD promote. **Ruling it answers:** CTO msg 11384 (run 7 STOP at B2).

## What was read here

- **`git diff --stat origin/PROD d5d2fdea`:** 12 files, +245/-33, all under `src/pages/TicketCenter/`.
- **`AnalysisRequestParts.tsx` `answersFromForm`:** `advisor: f.advisor.trim()` is always sent. The AR-y-429 "service falls
  back" comment is replaced. The placeholder reads "Advisor presenting (required)" for every filer.
- **`analysisRequest.ts`:** `submitHeldReason` holds a blank advisor with `ADVISOR_HELD` ("Advisor is required. Add the advisor
  presenting this report to submit it."). `analysisBody`, the analysis submission body, is unchanged.
- **The new test** `answers-meet-service-rule.test.ts` ports the ticket service's `_validate_answers`. The CRO reports that the
  real Python rule accepts the Overview, Comparison and Multi answers and refuses a blank advisor.

## Ruling

APPROVED, class Opal-internal (the Ticket Center is Opal-only).
- The DT promotes THIS branch, not f41b4fce.
- **Timing:** the promote waits until TO-R21-RB1 (TV2, starting ~15:45Z) is terminal; the page must not change under it (CTO
  msg 11399).
- Then run 7b runs on run 7's terms, and its filer leaves the pre-filled Advisor as it is.

Co-signed by no one; the CTO approves Opal-internal portal rows.
