# PROMOTE RECEIPT -- AMGT-gx-2 -- AI-row panel feature and its wording to portal PROD

Seat `0.4.0_DT_ClientPlatform~H1`, order `AMGT_RESAPP.TO-AMGT-gx-2` (GO msg 6736 from `2.0.0_SA_COO~R2`), approval rows `dell1-20261016T131944Z-6f4b` (head `31337460fcf7`) and `dell1-20261016T140659Z-5cf5` (head `9e13d8e1e933`), both closed APPROVED by `1.0.0_SA_CTO~DELL1`. Read 2026-10-16 ~14:1xZ to ~14:2xZ.

## Verdict

- Route changed: /security-analysis (Security Analysis, staff only).
- Class: Opal-internal; no client-facing page, no word from Andrew.
- Deploy run: completed.
- Conclusion: success, on PROD head `fa21a303d872`.

## Release

| Field | Value |
|---|---|
| Release branch | `release/20261016T141737Z`, built by `.tools/portal-release-build.sh --features cand/dell1/aifill-provenance,cand/dell1/aifill-provenance-wording-v2`; `RELEASE result=READY`, 2 features, 0 unapproved |
| PROD head before | `64f9dba10528593258b4b8a30b91763913122b76` (the order named `64f9dba1`: no deviation) |
| PROD head after | `fa21a303d87271a1e2d60c514d13501d71f9f020` (fast-forward of the release, parity diff 0 bytes, 2 files changed, 28 insertions, 4 deletions, typecheck rc 0) |
| Push state | on origin @fa21a303d872 (`git ls-remote origin refs/heads/PROD` read after the push: `fa21a303d87271a1e2d60c514d13501d71f9f020`; push `64f9dba1..fa21a303`) |
| Merge-forward (step 1) | IN-DEV read for both heads (`31337460fcf7` and `9e13d8e1e933` are ancestors of origin/DEV) |
| Tag | `portal-v2.1.232` peels to `fa21a303d87271a1e2d60c514d13501d71f9f020` (`portal-v2.1.231` peels to `64f9dba10528`) |
| Ledger | `org/critical_paths/change_management/20261016T1416Z_amgt-aifill-provenance-pair-portal-promote-dell1-20261016_deploy_completion.md`, CLOSED, 3 legs proven |

Builder lines, verbatim:

```
PROMOTE-LIST branch=cand/dell1/aifill-provenance class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261016T131944Z-6f4b pages=Security Analysis
PROMOTE-LIST branch=cand/dell1/aifill-provenance-wording-v2 class=opal-internal by=1.0.0_SA_CTO~DELL1 row=dell1-20261016T140659Z-5cf5 pages=Security Analysis
PROMOTE-CLIENT-FACING count=0
```

## Pages changed

| page | route | class |
|---|---|---|
| Security Analysis | /security-analysis | Opal-internal |

Files in the release: `src/pages/SecurityAnalysis/SecurityAnalysis.tsx` and `src/pages/SecurityAnalysis/components/InputProvenance.tsx`. No client-facing page changed.

## CI

`gh run 38914865382` "Deploy to Production" on headSha `fa21a303d872`: status `completed`, conclusion `success`, read by polling `gh run view --json status,conclusion` until completed. It is the only workflow on that sha in the last 40 PROD runs.

Served-bundle read (host `opalinvest.dev`, the CloudFront alias): the same crawl before and after, 68 paths, 62 files read OK, 6 x HTTP 403. BEFORE: `AI-written blocks` 0 of 62 files, both web-search wordings 0; controls `data-provenance-row` 1 and `Key Figures` 1. AFTER: `AI-written blocks` 1 file, `cites a web search made when it was written` 1, `cite web searches made when they were written` 1 (all `index-CJ0Jo9Y0.js`), negative control 0. The chunk holding the page moved `index-1lAjfLu8.js` -> `index-CJ0Jo9Y0.js`. The rendered row on a staff session is not read here (staff-only login); the CVO's PROD page read is the issuer's next step.

## Surprises

None filed. The main portal tree was fast-forwarded to origin/DEV `d1f9ca29675b` for the workspace pointer; it is on DEV and clean.
