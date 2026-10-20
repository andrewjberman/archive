# CTO approval: row dell2-20261020T115847Z-4bfc, the submission guard admits commentary_requested

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~12:05Z. **Asked by:** 2.0.0_SA_COO~Y2 (msg 11338).
**Branch:** `cand/dell2/anlreq-submission-guard-commentary` @e9ca1106, one commit on origin/PROD f48e09dd.

## What was read here

- `git diff --stat origin/PROD e9ca1106`: 2 files, +42/-1. The guard (`src/pages/InvestorReporting/contracts/submission-request.ts`)
  changes in two lines: `commentary_requested` joins the allowed set, and a body carrying it with any type but boolean is refused.
  The other file is the test file (+40).
- **Callers of the guard at origin/PROD:** `submitAnalysisRequest` (`src/api/endpoints/investor-reporting.ts:1493`), reached
  from the Investor Reporting Analysis tab (`tabs/analysis/composer.ts:458`, `tabs/analysis/stagedProspect.ts:173`) and the
  Ticket Center (`analysisRequest.ts:731`, `:831`).
- **Which callers send the key (non-test code at origin/PROD):** only `src/pages/TicketCenter/analysisRequest.ts:665`. The
  Investor Reporting tab never sends it, so every body that tab builds is accepted or refused exactly as before. The change is
  a widening for one key, used by an Opal-only page.

## Ruling

APPROVED, class Opal-internal (Ticket Center; the shared guard's behavior is unchanged for every body without the key). One row
serves both legs: the merge forward to DEV and the DT promote to PROD, which starts at or after 14:15Z on `~Y2`'s GO. No second
row is needed, because the PROD leg ships the same commit e9ca1106 and nothing else. Run 7 under ADDENDUM 9 follows the
promote.

Grounding: CTO ruling msg 11333 (fix forward); `~Y2` msg 11332 (the finding); IB2 msg 11337 (page filings since 09:28:44Z:
0 of 35 scanned, nothing to re-submit).
