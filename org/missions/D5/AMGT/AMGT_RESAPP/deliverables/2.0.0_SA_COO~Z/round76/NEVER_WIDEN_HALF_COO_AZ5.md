# AMGT_RESAPP round 76 -- `AMGT-az-5` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-06 ~19:3xZ

**The act** for `opal-amgt-scoped-api`, under ONE NEVER-2 entry. Executor `0.7.0_AE_CloudOps~A`. Order:
`task-orders/AMGT_RESAPP.TO-AMGT-az-5.the-code-redeploy.md`. Two legs, in this order:

1. **Code leg.** ONE artifact built from a DETACHED worktree at EXACTLY `de48559928` (the az-4 drain; az-2's drain
   `1ef4cd99de` is its ancestor). It is never built "at or after" that commit. Then ONE code-only `safe-apply` on
   `infra/aws/terraform/harvest/`, plan graded UNTARGETED: only the function's code (its artifact object and hash) may move;
   any other resource is a STOP. `memory_size` stays 1769. Then `round71/checks/leadpanel_cold_warm.py --label after` and the
   cold invokes' `AMGT_PHASE` lines.
2. **Snapshot event.** ONE direct invoke with exactly `{"amgt_scheduled_action": "refresh_freshness_snapshot"}`, so the
   /freshness snapshot is written by the new code. Read its stamp.

No grant, no schedule, no IAM, no memory change.

## THE BASE, read live at signing (~19:2xZ) -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `D29LJCXhOStZ51JD4TTt2Jk0QUVDUbXDouXRTUS1ULI=` (round 75 ay-5, built at `ab28d0ba01`), MemorySize 1769, python3.11, LastModified 2026-10-06T11:28:32Z | the prior artifact through the module, one code-only `safe-apply` |
| the /freshness snapshot object | written daily by `amgt-global-freshness-snapshot-daily` (12:30 UTC) through the same function | re-put of the prior version (copy-object from its VersionId); NEVER an S3 delete |
| open NEVER-2 entries on this function | none on the shared tree's HEAD. RESAPP sentinels `r56-af6`, `r73-aw7`, `r74-ax5` appear ONLY on stale branch copies in other projects' worktrees (`og-rb*`, `og-rel*`, `wk-dsgn-amgtv1-104`, `wk-oplgtw-15-r20`), cut before those entries closed; the deployed hash is the later ay-5 artifact, so each is world-done | -- |

## THE CONTENT-DIFF, measured by the issuer at signing

A detached worktree at `de48559928`, `build-and-upload-scoped-amgt.sh --build-only`, then `content_diff.py --zip` against
deployed `D29LJCXh`: files 372, IDENTICAL 364, CHANGED 7, ADDED 1, REMOVED 0.

| class | file | source |
|---|---|---|
| CHANGED | `lib/research/api/scoped_amgt.py` | az-2 (top_band, input_provenance) |
| ADDED | `lib/research/api/top_band.py` | az-2 |
| CHANGED | `lib/research/api/monthly_chatter.py`, `lib/research/api/names_read.py`, `lib/research/coverage/pool_reader.py` | az-4 (the cold read cut) |
| CHANGED | `lib/trading_calendar.py` | NFRA_MCPINDEX `3d7fb62105`: ADDITIVE only (+34, a new `weekly_production_day`); no existing function changes |
| CHANGED | `infra/logic/registry/reporting_policies.json` | IRPT_YCDGEN `0798635fec`: one policy row PENDING_ENFORCEMENT -> ACTIVE |
| CHANGED | `infra/logic/registry/systems.json` | CRO `8e39143feb`: +9, one VENDOR row added |

**The two registry files ARE read at request time:** `lib/opal_naming` loads and validates every registry file when the
snapshot path (`lib/research/freshness/snapshot.py`) or the /thesis path (`harvest.store`) builds an address. Measured at
`de48559928` in the build worktree: the registry loads and validates; `snapshot_address()` is
`s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json`, the same key round 75 granted;
`test_harvest_prefixes.py` + `test_freshness_snapshot.py` 24 passed. So the function's addresses do not move.

- **Size:** 255,360,320 B against 262,144,000 B (97.4%).
- **VERIFY-SCOPE:** cold-start FATAL [] and request-time break []; 90 of 90 required modules packaged.
- **Any file outside this table is a STOP.**

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **The /overlay body:** two ADDED fields only (`top_band`, `input_provenance`); no existing field changes value (az-2 bound 2,
  `test_overlay_check_face.py` key set).
- **The chatter body:** EQUAL (az-4 AC2, 3 of 3 windows byte-equal).
- **The snapshot object: N = 1 writer,** `refresh_freshness_snapshot()` in this function, reached by the daily schedule and this
  act's one event. Same data, same producer rule as round 75.

## EXPECTED OUTCOMES (both branches)

| check | before (D29LJCXh) | expected after | if not |
|---|---|---|---|
| r76 c62 / c63 deployed | FAIL (no top_band, no input_provenance) | YES each (local: 95 of 95) | rollback of the code leg |
| r75 c59 deployed (snapshot served, rows EQUAL) | YES | YES after the event | a row; the route falls back to compute |
| r75 c57 / c58 / c61, r74 c53 / c55 / c56, r71 c38 deployed | YES | YES (no regression; c55 pinned) | rollback of the code leg |
| cold chatter read (leadpanel `after`) | cold 2,987-3,177 ms (generation read 1,632 ms) | reported; inferred about 2.4-2.7 s | not a rollback; above about 2 s keeps provisioned concurrency on Andrew's list |
| new CodeSha256 | `D29LJCXh...` | differs AND equals the artifact built at `de48559928` | an unchanged hash is a 0-diff deploy: STOP |

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-06 ~19:3xZ. The CTO half is owed by `1.0.0_SA_CTO~Z`.
