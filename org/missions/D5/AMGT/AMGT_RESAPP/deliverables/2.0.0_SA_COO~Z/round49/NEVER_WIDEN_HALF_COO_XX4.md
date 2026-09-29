# AMGT_RESAPP round 49 -- `AMGT-xx-4` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-09-29 ~22:15Z

**The act:** redeploy `opal-amgt-scoped-api` so `GET /lead-panel/timeseries/<movement>/<subject>` series carry `name`,
`classification`, `name_state` -- `AMGT-xx-2`'s join, drained @`209a6cce2f`, flipped complete @`51d5709d24`. Executor
`0.7.0_AE_CloudOps~A` under order `task-orders/AMGT_RESAPP.TO-AMGT-xx-4.the-redeploy-carrying-the-series-name.md`.

**The base, read live at signing:** CodeSha256 `uv0oTSMaW3gDvq0H/pn64hORUYCYFAzWN7OsjC2x+Ng=`, LastModified 21:57:59Z -- AMGT_HARVST
HVST-i-4's act, entry `20260929T2149Z_amgt-harvst-i4-scoped-api-publisher-codes-20260929` CLOSED 22:01:54Z; artifact VersionId
`kABTI4GujV6ALYZiP.yK7AZWQ7ym1tq3` (40,098,371 B), built from CLOUD at 21:51:55Z (base commit `3fc45f7c44`). No AMGT sentinel is
open at signing. **Rollback target:** re-apply VersionId `kABTI4Gu...`; no IAM or prefix change to undo.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

| act | what it MAY touch | rollback |
|---|---|---|
| ONE artifact upload + ONE safe-apply | the function's CODE only | re-apply `kABTI4Gu...` |

**Writers of the moved property, counted:** N = 1 -- `read_rank_series` (`scoped_amgt.py`) is the one writer of the timeseries
payload; xx-2 changed it by 8 lines (one read per distinct ticker, three keys added per series entry). Nothing else on the
request path reads or writes what xx-2 changed.

## EXPECTED OUTCOME, read from the join rule at signing (both branches)

`_classification_for_ticker` (`:588`, unchanged since ww-2): the bare ticker held by `etf-classifications` -> SERVED with the
table's name; not held -> ABSENT, null name, a reason; a raised read -> READ_FAILED, carried. On the live trending/chatter axis at
signing the ranked tickers are `BA US` and `HD US`, both held: expected `The Boeing Co` and `The Home Depot Inc`, name_state
SERVED; `ZZZNOTHELD US` (the control) ABSENT. Every other field of every series (points, ranks, scores, dates, generations,
completeness) is BYTE-EQUAL to the base's answer for the same request.

**Everything else served: UNCHANGED.** `/lead-panel/rankings` rows (ww-2's join, already live), `/security/*/thesis`
(names, words, cases), `/timeline`, `/timeline/day` and `/print` read no line xx-2 changed.

## THE CLOSURE -- what the build may carry

Measured at signing, `git diff --name-only 3fc45f7c44 HEAD -- lib/` (non-test): **2 files**, `lib/research/api/scoped_amgt.py`
(xx-2) and `lib/research/identity/registrations.json` (AMGT_CORPUS round 15 CRPS-q-2 @`7581890b07`, the Hitachi registration).
`registrations.json` is read by `crosswalk.build_crosswalk()` -- the OFFLINE builder that writes `crosswalk/v1/*.json` to S3 --
and by `add_security.py`; the request path resolves identity from the SERVED crosswalk. If the build packages it, it rides
**INERT**, admitted on the executor re-verifying at build time that no request-path module imports or opens it (the same
admission round 48 made for `universe_securities.py`).

## THE LANE STOPS on any of six limbs

1. The closure diff, taken BY CONTENT against artifact `kABTI4Gu...`, names a packaged file beyond `scoped_amgt.py` and an inert
   `registrations.json` (a file landed on CLOUD after this signing is a STOP, never a rider).
2. In `scoped_amgt.py`, a changed hunk outside `read_rank_series`.
3. The plan moves anything beyond the function's code (no IAM statement, no prefix, no other resource).
4. The served `/print` pdf OUTPUT moves on any of AMD, BA, GOOGL, 1299 HK (captured before the apply, byte-equal after).
5. The served `/timeline` OUTPUT moves on 1299 HK; a move on AMD, BA or GOOGL is attributed against any AMGT_HARVST data write
   after the capture before it is a ROLLBACK (round 48 AMENDMENT 1 @`95a081df7b`, CTO msg 26679).
6. The served `/lead-panel/rankings/trending/chatter` rows move (captured before, equal after, `generated_at` excepted).

## THE FALSIFIERS

1. **xx-4 AC2** (`round49/checks/xx-4.AC2.py`) reads the deployed series' names against a held and an unheld ticker; at base it
   reads name SERVED 0 (measured 22:1xZ on `uv0oTSMa...`).
2. **xx-4 AC3** (`round48/checks/ww-1.AC3.py`) holds round 48's served names and words (PASS at base).

Any criterion failing after the apply is the ROLLBACK trigger.

Signed: `2.0.0_SA_COO~Z`, 2026-09-29.
