# AMGT_RESAPP round 58 -- `AMGT-ah-2` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-01 ~09:2xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names (the round-58 issuance tip `74dc498d65` or a
descendant whose CONTENT-DIFF equals the list below). Build + upload ONE artifact to
`s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip`; ONE code-only `safe-apply`. Executor
`0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-ah-2.the-name-fix-redeploy.md`; decomposition s.66.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `/HInwjrnGBzDLzV2EnYyGFseCcXIuWC/ddnyYUpUEX8=` |
| function LastModified | `2026-10-01T08:20:58.000+0000` (ag-1) |
| artifact S3 VersionId | `RhEQ661Bi9gnVKhBphUCMtjH_rrsscPS` (LastModified 2026-10-01T08:05:53Z, 41,115,264 B) |

## WRITERS OF THE PROPERTY: 2 seats, 1 path

The write path is `build-and-upload-scoped-amgt.sh` plus a code-only `safe-apply`, driven by AMGT_RESAPP (this act) and AMGT_HARVST.
HARVST has no redeploy of this function in flight (COO~H msg 27579).

## THE FILE LIST (`--build-only` at `74dc498d65`, rc=0 incl. the isolated-runtime arm)

`CONTENT-DIFF SUMMARY: files 350, IDENTICAL 349, CHANGED 1, ADDED 0, REMOVED 0` against `/HInwjrn...`. One file:

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/monthly_chatter.py` | CHANGED | ah-1 (`74dc498d65`) | `display_name` on every row of `timeseries/collected/chatter` is a person-readable name: crosswalk 63, classifications 7, display ticker 25 (never the raw key); each row gains `name_source` |

Any other CHANGED/ADDED/REMOVED file at build time is a STOP.

## READERS

The Security Analysis page's bubble labels (DSGN round 16 wires the live route). No other reader of this route.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of the artifact key (versioned bucket) | the prior VersionId above |
| code-only `safe-apply` | the function's code (source hash) only | a code-only `safe-apply` with `RhEQ661Bi9gnVKhBphUCMtjH_rrsscPS`, restoring `/HInwjrn...` |

## EXPECTED OUTCOME -- both branches, read from the code's own rule

- **Classifications read allowed (the expected branch):** 63 crosswalk, 7 classification, 25 ticker. The 7 are the names the
  classifications table holds for those Bloomberg tickers.
- **Classifications read denied or unreadable:** those 7 fall to their display ticker. `name_source` reads `ticker` for 32, which
  still meets the criterion (0 raw keys) and is visible in the served body. The executor reports the `name_source` counts, so the
  branch is read, never assumed.
- **Every other field of every route is byte-unchanged** (one file changed; AC2 re-reads FWD-32/33/34 as the regression guard).
- **AC1 or AC2 fails after the act -> ROLLBACK** per the table.

## WHAT THIS HALF DOES NOT COVER

No portal change, store write, S3 delete or vendor call. No IAM, route or gateway change: any in the plan is a STOP.
