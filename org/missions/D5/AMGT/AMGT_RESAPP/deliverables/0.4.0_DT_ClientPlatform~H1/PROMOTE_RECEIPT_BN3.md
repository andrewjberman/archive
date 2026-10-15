# PROMOTE RECEIPT -- AMGT-bn-3 -- team estimate mark to portal PROD

Seat `0.4.0_DT_ClientPlatform~H1`, order `AMGT_RESAPP.TO-AMGT-bn-3` (GO msg 6301 from `2.0.0_SA_COO~R1`), approval row `dell1-20261015T221629Z-a333` (CTO `1.0.0_SA_CTO~DELL1`, APPROVED, head `bb56c53d12a5`). Read 2026-10-15 ~22:3xZ.

## Verdict

- Route changed: /security-analysis (Security Analysis, staff only).
- Class: Opal-internal; no client-facing page, no word from Andrew.
- Deploy run: completed.
- Conclusion: success, on PROD head `e0e69da7766d`.

## Release

| Field | Value |
|---|---|
| Release branch | `release/20261015T223053Z`, built by `.tools/portal-release-build.sh --features cand/dell1/amgt-sa-team-estimate-mark`; `RELEASE result=READY`, 1 feature, 0 unapproved, `PROMOTE-CLIENT-FACING count=0` |
| PROMOTE-LIST | `branch=cand/dell1/amgt-sa-team-estimate-mark class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261015T221629Z-a333 pages=Security Analysis` |
| PROD head before | `e0b43076d9daf56f8eb4937137180e3cf4246e7f` (the order named `e0b43076d9`: no deviation) |
| PROD head after | `e0e69da7766d87719571d7e6c0ccf59bf65fcae9` (fast-forward of the release, parity diff 0 bytes, typecheck rc 0, VALGATE D-1 PASS no-op) |
| Push state | on origin @e0e69da7766d (`git ls-remote origin refs/heads/PROD` read after the push: `e0e69da7766d87719571d7e6c0ccf59bf65fcae9`; push `e0b43076..e0e69da7`) |
| Merge-forward (step 1) | IN-DEV read: `bb56c53d12a5` is an ancestor of origin/DEV `ee278065576e` |
| Tag | `portal-v2.1.227` peels to `e0e69da7766d87719571d7e6c0ccf59bf65fcae9` (`portal-v2.1.226` peels to `e0b43076d9`) |
| Ledger | `org/critical_paths/change_management/20261015T2230Z_amgt-sa-team-estimate-mark-portal-promote-dell1-20261015_deploy_completion.md`, CLOSED, 3 legs proven |

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

Product file in the release: `src/pages/SecurityAnalysis/tabs/ModelTab.tsx` (+30/-2) plus the harness and three fixtures under `src/pages/SecurityAnalysis/__harness__/`. No client-facing page changed; no word from Andrew was needed.

## CI

`gh run 38817882585` "Deploy to Production" on headSha `e0e69da7766d`: status `completed`, conclusion `success`, read by polling `gh run view --json status,conclusion` until completed. It is the only workflow on that sha in the last 40 PROD runs.

Served-bundle read (host `opalinvest.dev`, the CloudFront alias): the same crawl before and after, 68 paths, 62 files read OK, 6 x HTTP 403. BEFORE: `research team estimate` 0 of 62 files, `data-model-team-mark` 0, controls `fiscal_unresolved` 1 and `Key Figures` 1. AFTER: `research team estimate` 1 file and `data-model-team-mark` 1 file (both `index-2eRxHeKz.js`), negative control 0. The chunk holding the page moved `index-HfuxrtGC.js` -> `index-2eRxHeKz.js`. The mark's render with live data is not read here (the page is staff-only behind a login); the harness result is the worker's `AMGT-bn-1` instance.

## Surprises

None filed. The main portal tree was fast-forwarded to origin/DEV `ee278065576e` (20 commits behind) for the workspace pointer; it is on DEV and clean.
