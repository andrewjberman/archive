# PROMOTE RECEIPT -- AMGT-bo-2 -- withheld-reasons feature to portal PROD

Seat `0.4.0_DT_ClientPlatform~H1`, order `AMGT_RESAPP.TO-AMGT-bo-2` (GO msg 6409 from `2.0.0_SA_COO~R1`), approval row `dell1-20261016T013205Z-9365` (CTO `1.0.0_SA_CTO~DELL1`, APPROVED, head `01e06415f17f`). Read 2026-10-16 ~02:4xZ to ~02:5xZ.

## Verdict

- Route changed: /security-analysis (Security Analysis, staff only).
- Class: Opal-internal; no client-facing page, no word from Andrew.
- Deploy run: completed.
- Conclusion: success, on PROD head `ab2c43657e7b`.

## Release

| Field | Value |
|---|---|
| Release branch | `release/20261016T024935Z`, built by `.tools/portal-release-build.sh --features cand/dell1/amgt-sa-withheld-reasons`; `RELEASE result=READY`, 1 feature, 0 unapproved, `PROMOTE-CLIENT-FACING count=0` |
| PROMOTE-LIST | `branch=cand/dell1/amgt-sa-withheld-reasons class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261016T013205Z-9365 pages=Security Analysis` |
| PROD head before | `e0e69da7766d87719571d7e6c0ccf59bf65fcae9` (the order named `e0e69da7`: no deviation) |
| PROD head after | `ab2c43657e7b7bbfd528ec5f06c6ef3f0b45068b` (fast-forward of the release, parity diff 0 bytes, 10 files changed, typecheck rc 0, VALGATE D-1 no-op) |
| Push state | on origin @ab2c43657e7b (`git ls-remote origin refs/heads/PROD` read after the push: `ab2c43657e7b7bbfd528ec5f06c6ef3f0b45068b`; push `e0e69da7..ab2c4365`) |
| Merge-forward (step 1) | IN-DEV read: `01e06415f17f` is an ancestor of origin/DEV |
| Tag | `portal-v2.1.228` peels to `ab2c43657e7b7bbfd528ec5f06c6ef3f0b45068b` (`portal-v2.1.227` peels to `e0e69da7766d`) |
| Ledger | `org/critical_paths/change_management/20261016T0247Z_amgt-sa-withheld-reasons-portal-promote-dell1-20261016_deploy_completion.md`, CLOSED, 3 legs proven |

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

Product files in the release: `tabs/ModelTab.tsx`, `components/model/WhatChangedPanel.tsx`, new `components/model/withheldPeReason.ts`, plus the harnesses and five fixtures, all under `src/pages/SecurityAnalysis/`. No client-facing page changed.

## CI

`gh run 38842687915` "Deploy to Production" on headSha `ab2c43657e7b`: status `completed`, conclusion `success`, read by polling `gh run view --json status,conclusion` until completed. It is the only workflow on that sha in the last 40 PROD runs.

Served-bundle read (host `opalinvest.dev`, the CloudFront alias): the same crawl before and after, 68 paths, 62 files read OK, 6 x HTTP 403. BEFORE: `data-model-summary-pe-reason` 0 of 62 files, `P/E not shown: ` 0, `research team estimate` 1 (the earlier bn-3 mark), `Key Figures` 1. AFTER: `data-model-summary-pe-reason` 1 file, `P/E not shown: ` 1 file, `research team estimate` 1 file (all `index-C3r9t0Ge.js`), negative control 0. The chunk holding the page moved `index-2eRxHeKz.js` -> `index-C3r9t0Ge.js`. The rendered page on a staff session is not read here (staff-only login).

## Surprises

None filed. Worktree `.runtmp/portal-promote-20261016T025012Z` could not be physically deleted (Permission denied); `worktree prune` ran, and the directory is gitignored and inert. The main portal tree was fast-forwarded to origin/DEV `39dab87f3b0c` for the workspace pointer; it is on DEV and clean.
