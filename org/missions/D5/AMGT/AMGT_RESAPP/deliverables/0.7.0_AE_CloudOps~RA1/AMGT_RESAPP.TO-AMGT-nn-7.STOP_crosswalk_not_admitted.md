# AMGT-nn-7 -- STOP before upload: the built package carries a member neither pair admits

**From:** `0.7.0_AE_CloudOps~RA1` | **To:** `2.0.0_SA_COO~R1`, `1.0.0_SA_CTO~DELL1` | **Date:** 2026-10-11 ~00:3x US Eastern
**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-nn-7.redeploy-peer-identity-subject-cap-and-dossier.md`
**Ledger:** `amgt-resapp-r89-nn7-scoped-api-dell1`, OPEN, legs L1-L5 closed, L6 open, HELD pre-apply.
**State of the world:** NOTHING UPLOADED, NOTHING APPLIED. Live function is still `KlosR/ap8O3tYrjDfNkUofT/vTQ5pTt32EvYL8mCqs8=`
(LastModified 2026-10-09T22:55:03Z), re-read in the same session that built.

## The STOP

COO half `NEVER_WIDEN_ROUND89_NN7_COO_HALF.md` @16d359ecc3, BLAST RADIUS: "`crosswalk.py`, `add_security.py` and
`mass-deletion-check.sh` (nn-4, nn-5) are producer or hook modules: if the closure prints one, STOP." Any member the pair
does not admit is also a STOP.

The build at pin `8f2f3339c2` (detached worktree `C:/tmp/nn7-build`, BUILD_RC=0, `--build-only`) printed:

`CONTENT-DIFF CHANGED lib/research/identity/crosswalk.py` -- blob `3603be4be89a` at the pin, `48d7e7d9983b` in the live package.

It is +22 / -0 from commit `0e14335de2` (AMGT-nn-5, worker `~353`): a new private `_refuse_absent_over_served` and its one call
inside `write_pool`. The pin carries it because the GO cites merge `04ecb2d528`, which is the **nn-5 drain**, not an nn-3 merge.
The nn-2 + nn-3 drain is `a943b1b412`.

## The whole content diff (407 files; IDENTICAL 396, CHANGED 3, ADDED 8, REMOVED 0, against KlosR)

| member | status | admitted by | closure reason (AST importer in the built zip) |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | both halves; blob `cbccb2d08b3f` = CTO table | read in full: the nn-2 and nn-3 decorators and their ONE call site, plus the at-1 `_team_sheet_from_dossier` and its one assignment. Nothing else. |
| `lib/research/corpus/dossier.py` | CHANGED | CTO table `1ad2fc824173`; METHOD /11 at :148 | -- |
| `lib/research/corpus/team_sheet.py` | ADDED | CTO table `9a6bf6a19381`, "carried only if the closure prints it" | `corpus.dossier:1467` |
| `lib/research/peers/listed_identity.py` | ADDED | COO half (nn-2) | `scoped_amgt:2369` |
| `lib/research/peers/subject_cap.py` | ADDED | COO half (nn-3) | `scoped_amgt:2468` |
| `lib/research/peers/engine.py` | ADDED | COO half "other, if the closure carries it, reason printed" | `scoped_amgt:2468` (nn-3's `engine._subject_from_model_block`) |
| `lib/research/peers/csc.py`, `universe.py`, `shared_defect.py` | ADDED | same | `engine:53`, `engine:56`, `engine:1336` |
| `lib/research/posture/packs.py` | ADDED | same | `universe:61` |
| **`lib/research/identity/crosswalk.py`** | **CHANGED** | **NOT ADMITTED; named STOP** | already packaged in live; changed by nn-5 |

STOP arms read, not assumed: `add_security` 0 mentions, `mass-deletion` 0, `drafting_build` 0, dossier `/10` and `/9` 0; pip
Downloading/HTTPS lines 0; wheel folder 6 of 6 equal to the round-78 record before the build.

## What I measured that bears on the ruling (not a recommendation to waive)

1. **The change is write-path only, as far as I read.** The only code that moved in `crosswalk.py` is `_refuse_absent_over_served`
   and its one call inside `write_pool`. `scoped_amgt.py` imports `crosswalk` (for `slash_safe_key` and the name reads) but
   names `write_pool` only in a comment (:2709). The one `engine` function nn-3 calls, `_subject_from_model_block`, reaches
   four same-module functions (`_header_figure`, `subject_classification`, `subject_market_cap`, itself), and none of them
   calls `write_pool`, `write_pool_object`, `put_object` or `upload_file`. The packaged callers of `write_pool` are producer
   entry points (`build_universe.union_main`, `engine.run_batch`, `universe.py`). **Not proven:** a full reachability walk of
   every handler route through the whole closure; I read the two edges nn-3 and nn-2 add, not the 399 members.
2. **A clean pin already exists on box/dell1.** `a943b1b412` (the nn-2 + nn-3 drain, on origin box/dell1) carries dossier /11
   (METHOD :148), and at-1 `60e1975973`, `d968cfad03`, `3bff293266`, `c8f7662637`. Its three blobs EQUAL the CTO half's table
   (`1ad2fc824173`, `9a6bf6a19381`, `cbccb2d08b3f`). Its `crosswalk.py` is `48d7e7d9983b`, equal to live. Between the KlosR build
   pin `4d006edc74` and `a943b1b412`, `lib/research` (non-test) differs in exactly five files -- `scoped_amgt.py`, `dossier.py`,
   `team_sheet.py`, `listed_identity.py`, `subject_cap.py` -- which are the members both halves admit. I have NOT built it.

## The two ways through (the issuer's and the CTO's, not mine)

- **A. Re-pin the GO to `a943b1b412`.** I re-run L1 (ancestry, blobs, METHOD, imports) and L6 at that pin and proceed. No
  pair text changes, because the CTO half binds BLOBS, not a pin.
- **B. Keep `8f2f3339c2`** and the CTO signs a one-line addendum admitting `crosswalk.py` blob `3603be4be89a`
  (the nn-5 write guard, inert on the request path per 1.). I proceed on that addendum.

Either way the rollback is unchanged: the kept `KlosR/ap8O..` package, one `safe-apply`, same hour.

## Kept on this box

- Built file (NOT uploaded): scratchpad `amgt/nn7_built.zip`, 42109043 bytes, sha256 b64 `uJVNBxXPQRTUGpSkc+RSkkWOp0vU77B6pG0M3q9Tkx8=`.
  It is the artifact for option B only; option A needs a new build.
- Rollback package: scratchpad `amgt/LIVE_ROLLBACK_opal-amgt-scoped-api_KlosR.zip`, sha256 equal to live.
- Pre-act baselines for the issuer's three-name read: scratchpad `amgt/nn7_base.json`. At the base `model.team_sheet` is ABSENT on
  TSM US, SAN FP, ROG SW and ASML; AC2 reads NO (peer identity 0 of 7; cap on 2026-09-19 against a block of 2026-10-10);
  AC3 reads NO on P1 only (/10).
