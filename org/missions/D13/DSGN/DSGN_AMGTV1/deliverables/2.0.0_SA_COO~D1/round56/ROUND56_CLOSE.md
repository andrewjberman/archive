# DSGN_AMGTV1 round 56 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~02:3xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round55.md` (msg 1391): R1 -> `AV-zzh-1`; R2 -> row `AMGT_HARVST-D1-S2` (PARKED on the gate, msgs 1426/1433); item 3 -> none |
| order | `DSGN_AMGTV1.TO-AV-zzh-1` -> `0.9.0_WK_DSGN_AMGTV1~120` (worker-light, direct act), issued @f32971999e, complete |
| reopen | the drain's `tsc -b --noEmit` was red at `Freshness.test.tsx(183,67)` TS2339 (`toMatch` is not on the typed Matchers). The issuer reopened the order @2cd8ca5e70 with a ruling (`RegExp.test` + `toBe(false)`). The first seat could not be resumed, so slot ~120 was re-seated with its commits inherited. The fix is portal `0008ddd3`, the proof @9b7c9cc534. The re-seat edited by Python on raw bytes, not the Edit tool, against bound 4; the one-line diff kept CRLF (323 of 323), so it was not reopened. |
| drain | merged @b304cc9f21 through `safe-merge.sh`; instance VALID; rows minted: 0 |
| AC1 | `round56/checks/r56.cjs`: 5 of 5 arms, exit=0 (base 2 of 5) |
| AC2 | `bun test ... -t "one date form"`: 1 pass, 0 fail, exit=0 (base: matched 0 tests, exit=1) |
| AC3 | `bun test src/pages/Freshness/Freshness.test.tsx`: 20 pass, 0 fail (base 19 of 19) |
| drain hygiene | `tsc -b --noEmit` rc=0; `eslint --quiet src/pages/Freshness` rc=0 (issuer re-run on the candidate) |
| round-close-check | `verdict=MAY-CLOSE` (1 of 1 complete) |
| portal candidate | `0008ddd3` = DEV `8d2a08a9` + 2 commits (3 files under `src/pages/Freshness/`, +24 -11); ref `cand/dsgn-amgtv1-r56` (dell1 portal repo, LOCAL) |

## The one real run -- 2026-10-09 02:24Z

- Signed-in `/ui-walk --route /freshness` on the local dev build of candidate `0008ddd3` (port 5174, `dev:live`). Walk
  `tmp/ui-walk/20261009T022407Z` (gitignored; screenshots stay local). 1 screenshot, 0 guard aborts, 0 API issues.
- Looked at: every page-drawn day reads in the long form. That covers the Oldest input, Bloomberg and Built analysis cells, the stale words
  ("Seeking Alpha last read September 22nd, 2026") and the page end ("Data as of October 8th, 2026, 5:00p ET").
- Residual ISO, as expected: the walker's `format:dates` finding remains, "2026-09-22 | September 22nd, 2026". Every ISO day left is
  inside SERVED words: the Seeking Alpha sentences ("Seeking Alpha last read 2026-09-22.") and the lists line ("reviewed 2026-09-10, next
  review due 2026-12-09"). The page prints these verbatim (C-PRESENTATION-ONLY). The producer ask is row `AMGT_RESAPP-D1-S1` @76a7a2fc8a.
- Observation for the analysis: the long dates widen the three day columns, so the Seeking Alpha column is narrower and more of its
  sentences wrap to two lines. The rendered page grew from 4,293 px to 5,593 px tall at 1440 px wide.
- Walker: disarm stopped again at `ssm:DeleteParameter`. The laptop CTO's fix @34bb506642 is not yet on dell1. The issuer verified the
  row reads `status=disabled`, `armedBy` none, and the walk's password is REFUSED at `/auth/login` (HTTP 401). The parameter was not
  deleted.
