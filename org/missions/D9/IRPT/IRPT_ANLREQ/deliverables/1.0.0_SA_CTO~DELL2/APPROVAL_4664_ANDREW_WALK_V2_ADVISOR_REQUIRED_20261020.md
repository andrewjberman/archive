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

## Row dell2-20261020T153733Z-37f6 (DEV landing of the same fix), ~15:40Z

**Asked by:** 4.0.0_SA_CRO~TCKT (msg 15:37Z). **Branch:** `cand/dell2/anlreq-andrew-walk` @448a6ea9.

**Why a second row:** v2 cannot merge forward to DEV, because DEV already holds f41b4fce (row 500c) and the merge conflicts.

**Read here:**
- `git log origin/DEV..448a6ea9` lists exactly one commit, 448a6ea9.
- `git diff 448a6ea9 d5d2fdea -- src/pages/TicketCenter` prints nothing, so DEV gets the same TicketCenter tree that PROD gets.

**Ruling:** APPROVED for DEV only. PROD still promotes d5d2fdea (row 4664).

## Rows dell2-20261020T162029Z-5779 (PROD set @602ca19e) and dell2-20261020T162121Z-3067 (DEV landing @381a835a), ~16:2xZ

**Why:** the DT's PROD gate (msg 11419) found one release-only failure: `prospect-no-price-date.test.tsx:117`, test (d), which
asserted the Needed-by date input that Andrew removed.

**Read here:**
- `git diff --stat d5d2fdea 602ca19e`: 1 file, the test only (+5/-3). Test (d) now asserts no date input and still asserts
  priceDate empty.
- `git log origin/DEV..381a835a` lists one commit.
- `git diff 381a835a 602ca19e` prints nothing, so the two branch trees are equal.
- The CRO reports that the whole suite shows 78 failures on both 602ca19e and origin/PROD 4546cee0, with the same set.

**Ruling:** both rows APPROVED, Opal-internal. They supersede d5d2fdea and 448a6ea9: the DT promotes 602ca19e, and DEV takes
381a835a. Run 7b follows the promote.
