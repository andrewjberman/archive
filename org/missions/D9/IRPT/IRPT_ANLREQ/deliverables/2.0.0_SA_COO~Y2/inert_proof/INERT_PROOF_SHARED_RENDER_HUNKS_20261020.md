# Inert proof: the shared render hunks of the v0.24 round change nothing on any page that does not pass the new props (2.0.0_SA_COO~Y2, 2026-10-20)

Asked by the CTO (msg 11130, after the CVO's ruling on row 71f6): prove the NativeSections and RetainedSections hunks are inert on every partner-reachable page, by byte-equal render output with the new props absent, for each page that mounts them, the page list read from the code. Measured by the issuer, read-only, no live call.

**Claim tags:** M = measured here. The comparison is of server-rendered markup (`renderToStaticMarkup`), not a browser.

## 1. Method (M)
- Two portal trees: **DEV** = `origin/DEV` `5c9b1d0de97e` (a detached worktree, no change) and the **candidate** = `cand/dell2/anlreq-ticket-center-cleanup` `15bf70d36c99` (six commits on that DEV).
- ONE scratch test file (`render_dump.test.tsx.txt` in this folder, never committed to the portal) copied into both trees and run with `bun test`. It renders `NativeSections` and `RetainedSections` with their **default props only** (no `mode`, no `operator`) over nine report fixtures, and writes every markup string to a file; the two files are compared by sha256.
- Fixtures (the shapes of the existing IV-e-122 and fe-s-6 tests, through `adaptAnalysisReportSlice`): vendor reports certified, uncertified and failed; a vendor report with no sections and one with twelve; Opal reports certified and uncertified (six sections), an Opal report with no sections and one with 147 sections mixing VALUE and NOT_AVAILABLE. `RetainedSections` is rendered once per fixture and `NativeSections` twice (no disclosures; two disclosures): **27 renders**.

## 2. Result (M)
**27 of 27 renders are byte-equal** between DEV and the candidate (`RENDER_HASHES.tsv`: fixture, the two sha256 prefixes, bytes, verdict; the markup sizes run from 475 to 161,973 bytes).
**Positive control (M):** in the candidate tree, `RetainedSections` over the 147-section Opal fixture rendered with `mode: 'report'` differs from the default render (sha256 prefixes `cebbb1826422` default, `0cad3e759edb` report): the harness can see a change.

## 3. The page list, read from the code (M, `git grep` at the candidate)
| mount | file:line | props passed | partner-reachable |
|---|---|---|---|
| `NativeSections` | `src/pages/InvestorReporting/tabs/analysis/RequestList.tsx:72` | none (default face) | the Analysis tab (Investor Reporting) |
| `RetainedSections` | `src/pages/InvestorReporting/tabs/analysis/OwnedRequestHistory.tsx:432` (the history dialog) | none (default face) | the Analysis tab |
| `RetainedSections` | `src/pages/TicketCenter/TicketCenter.tsx:214` (`OpenedReportPanel`) | `mode="report"`, `operator={internal}` | the Ticket Center (NOT default: the new face) |
| `RetainedSections` | `src/pages/TicketCenter/AnalysisRequestParts.tsx:538` (`OpenedPackageReport`) | `mode="report"`, `operator` | the Ticket Center (NOT default: the new face) |
| `SectionBlock` | inside `NativeSections` and `RetainedSections` only | `bare` only in the report face | follows its parents |
Other importers of `NativeSections.tsx` take unchanged exports only (`AnalysisDocument.tsx`: `OPAL_SECTION_SOURCE_WORDS`, `isOpalReport`; `VendorPdfPreview.tsx`: `isOpalReport`).

## 4. The export surface (M, `git diff origin/DEV HEAD`)
Three exported signatures changed and each only GAINED optional parameters with defaults: `SectionBlock(..., bare = false)`, `NativeSections({ report, mode = 'trace', operator = false })`, `RetainedSections({ report, mode = 'trace', operator = false })`. Nothing exported was removed or renamed; new exports are additions (`NativeSectionsMode`, `RetainedSectionsMode`, `isFigureSection`, `isUnavailableSection`, `reportDisclosureOrder`, `unavailableReasonCounts`, `OperatorTrace`). Four files change under `src/pages/InvestorReporting` (two components, two new test files: 366 insertions, 12 deletions).

## 5. What this proves and what it does not
- **Proves:** for every mount in section 3 that passes no new prop (the Analysis tab's `RequestList` and history dialog), the markup over these 27 renders is byte-identical to DEV's. The new behaviour is reachable only through `mode="report"`, which only the two Ticket Center mounts pass.
- **Does not prove:** the Ticket Center's own changes are inert. They are NOT: the form loses three fields, the models render at first paint, Open report shows the new face. Partners reach `/ticket-center` on DEV (`firmAccess.ts:141`, CTO msg 11130), so those commits stay client-facing and need Andrew's word.
- Not proven: browser rendering; fixtures beyond the nine (a report shape the fixtures do not cover); the PROD bundle.

## 6. Use
The shared render hunks (commits `710c3eed` AR-y-418 and `4b335a35` AR-y-422, without the Ticket Center hookup) can be registered as their own Opal-internal row citing this receipt; the Ticket Center commits (AR-y-416, AR-y-419, AR-y-425 and the hookup) stay with row `71f6` for Andrew.
