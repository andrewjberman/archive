# Portal candidate wk-IRPT_BCKEND-r174-candidate -- one fast-forward of origin/DEV for the CTO review lane

Issuer: 2.0.0_SA_COO~P2, 2026-10-13. Branch in the portal repo: wk-IRPT_BCKEND-r174-candidate. HEAD e50a1379. Base: origin/DEV 64980b4d (fetched, read). Seven commits cherry-picked and kept (not squashed), plus ONE integration commit of mine (e50a1379), in the CTO's order (msg 6825): 353 (fe-s-18 fixture generator), 346 (AnalysisReport wire copy and fixtures), 350 (fe-s-15 generator and selected_sections), 355 (export envelope covered_account_ids), 357 (six-class wire). Cherry-picks applied with no conflict. LOCAL, not pushed (the CTO reviews; a DEV push follows the push law).

## Full IR suite (bun test src/pages/InvestorReporting) on the combined head, against DEV's own

| head | pass | skip | fail | failing tests |
|---|---|---|---|---|
| origin/DEV 64980b4d | 1218 | 27 | 5 | F14-AC3, IVE26-AC3, IVE48-AC1, IVE98, producer fixtures |
| candidate e50a1379 | 1225 | 27 | 2 | F14-AC3, producer fixtures |

The candidate fixes IVE26-AC3, IVE48-AC1 and IVE98 (all three fail on DEV's own head) and adds 7 passing tests; F14-AC3 and producer fixtures fail on DEV too and are not touched.

## The integration commit (e50a1379), the one thing the combined branch needed

Candidates 346 and 350 each passed alone and meet only here: 350 aligned `selected_sections` in `fixtures/wire/ExportBundle.valid.json` and `fixtures/wire/requests/submit-export.request.json` to the AnalysisReport wire copy as it stood on the base (`S-RET-1`), while 346 moved that copy's section to the extractor form `2.annualized_return.c1`. On the combined head `S-RET-1` resolved to nothing (check IB171-5-AC2 FAIL; no portal test enforces it, the suite was green). e50a1379 sets both fixtures to `2.annualized_return.c1` (2 files, one line each, CRLF kept); IB171-5-AC2 reads PASS after it. The producer's own `ExportBundle.valid.json` still names `S-RET-1` (row W350-S4, outside this portal).

Generator checks on the combined head, all PASS: the fe-s-15 and fe-s-18 generators reproduce their committed outputs (IB171-5-AC1, IB172-2-AC1, IB173-2-AC1), and the frozen export envelope validates against the v1 ExportReceipt schema (IB173-2-AC3). A generator run rewrites line endings of some CRLF files in the working tree (end-of-line only; `git diff --ignore-cr-at-eol` is empty).

## Per-commit file list (portal-relative, git show --stat)

### f54d7ca6 fix(IRPT_BCKEND IB-pr-502, 0.9.0_WK_IRPT_BCKEND~353): fe-s-18 generator reproduces the six committed outputs
- .../__tests__/fe-s-18/gen-fixtures.ts              | 117 ++++++++++++++++++---
- 1 file changed, 101 insertions(+), 16 deletions(-)

### 9427632a fixtures(IRPT_BCKEND IB-pr-495): AnalysisReport wire copy and its fixtures carry the extractor section form
- .../InvestorReporting/__tests__/fe-s-32/holdings-no-answer.json   | 8 ++++----
- .../InvestorReporting/__tests__/fe-s-74/fixtures/one-bad-key.json | 8 ++++----
- src/pages/InvestorReporting/fixtures/smoke/default.json           | 8 ++++----
- src/pages/InvestorReporting/fixtures/smoke/fe-s-13-wire.json      | 8 ++++----
- src/pages/InvestorReporting/fixtures/smoke/fe-s-15-clean.json     | 8 ++++----
- .../fixtures/smoke/fe-s-15-needs-correction.json                  | 8 ++++----
- .../fixtures/smoke/fe-s-18-holdings-missing-attribution.json      | 8 ++++----
- .../fixtures/smoke/fe-s-18-holdings-observed.json                 | 8 ++++----
- .../InvestorReporting/fixtures/smoke/fe-s-18-holdings-target.json | 8 ++++----
- src/pages/InvestorReporting/fixtures/smoke/fe-s-21-queued.json    | 8 ++++----
- .../InvestorReporting/fixtures/wire/AnalysisReport.valid.json     | 8 ++++----
- 11 files changed, 44 insertions(+), 44 deletions(-)

### 86293960 fixtures(IRPT_BCKEND IB-pr-495, 0.9.0_WK_IRPT_BCKEND~346): the six fixtures that still carried the old AnalysisReport section (fe-s-15 job.ge
- src/pages/InvestorReporting/fixtures/fe-s-15/job.generating.json  | 8 ++++----
- src/pages/InvestorReporting/fixtures/fe-s-15/job.preparing.json   | 8 ++++----
- src/pages/InvestorReporting/fixtures/fe-s-15/job.queued.json      | 8 ++++----
- src/pages/InvestorReporting/fixtures/fe-s-15/job.ready.json       | 8 ++++----
- src/pages/InvestorReporting/fixtures/fe-s-15/job.waf-refresh.json | 8 ++++----
- src/pages/InvestorReporting/fixtures/smoke/fe-s-18-frozen.json    | 8 ++++----
- 6 files changed, 24 insertions(+), 24 deletions(-)

### 4c8dc57f fix(IRPT_BCKEND IB-pr-500, 0.9.0_WK_IRPT_BCKEND~350): fe-s-15 generator reproduces the committed job fixtures; selected_sections resolves
- .../__tests__/fe-s-15/gen-fixtures.ts              | 34 +++++++++++++++++++++-
- .../fixtures/wire/ExportBundle.valid.json          |  3 +-
- .../wire/requests/submit-export.request.json       |  3 +-
- 3 files changed, 35 insertions(+), 5 deletions(-)

### c2a53576 fix(IRPT_BCKEND IB-pr-504, 0.9.0_WK_IRPT_BCKEND~355): the frozen export envelope carries facts.covered_account_ids
- src/pages/InvestorReporting/__tests__/fe-s-18/gen-fixtures.ts | 11 ++++++-----
- .../InvestorReporting/fixtures/smoke/fe-s-18-frozen.json      |  5 ++++-
- 2 files changed, 10 insertions(+), 6 deletions(-)

### 58070e5c fix(IRPT_BCKEND IB-pr-504, 0.9.0_WK_IRPT_BCKEND~355): the four generator-rewritten fixtures carry facts.covered_account_ids (AMENDMENT 1 gran
- .../InvestorReporting/__tests__/fe-s-32/holdings-no-answer.json      | 5 ++++-
- .../fixtures/smoke/fe-s-18-holdings-missing-attribution.json         | 5 ++++-
- .../InvestorReporting/fixtures/smoke/fe-s-18-holdings-observed.json  | 5 ++++-
- .../InvestorReporting/fixtures/smoke/fe-s-18-holdings-target.json    | 5 ++++-
- 4 files changed, 16 insertions(+), 4 deletions(-)

### 3c551adb IB-pr-506 (0.9.0_WK_IRPT_BCKEND~357): the portal wire union keeps the SIX classes; multi_asset is a RETIRED member subtracted by the generato
- .../dsgn-irptv1/ib-174-multi-asset-label.test.ts   | 140 +++++++++++++++++++++
- .../dsgn-irptv1/iv-e-48.new-classes.test.tsx       |   6 +-
- .../__tests__/fe-s-13/gen-wire.ts                  |  14 ++-
- src/pages/InvestorReporting/contracts/adapt.ts     |  27 ++++
- .../contracts/wire/HoldingsSnapshot.ts             |   3 +-
- 5 files changed, 186 insertions(+), 4 deletions(-)

### e50a1379 fix(IRPT_BCKEND r174 candidate integration, 2.0.0_SA_COO~P2): selected_sections names 2.annualized_return.c1
- src/pages/InvestorReporting/fixtures/wire/ExportBundle.valid.json | 2 +-
- src/pages/InvestorReporting/fixtures/wire/requests/submit-export.request.json | 2 +-
- 2 files changed, 2 insertions(+), 2 deletions(-)
