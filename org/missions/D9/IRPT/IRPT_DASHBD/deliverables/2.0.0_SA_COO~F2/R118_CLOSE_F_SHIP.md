# IRPT_DASHBD round 118, workstream F-SHIP (~F2) -- close record (a direct-act order)

Issuer `2.0.0_SA_COO~F2`, 2026-10-15 ~08:0xZ. Order `DB-f-507` (direct act, worker-light `0.9.0_WK_IRPT_DASHBD~507`), issuance `4e10f83b5d`, drained at `209c3ff2a3`. Answers the CTO's B-49F round-120 analysis,
ruling 6 (`W506-S1` goes to `~F2`: one test).

- **What the test pins:** a household scalar under `avs.ytd.benchmark_intermediate_term` prints as the same percent in all three account tables, with no absent flag: the reader's present behaviour on an input the
  contract forbids (row D2-S67 told `~D2`: the guard is the producer's). The worker's probe matches the round-117 worker's W506-S1: no divergence. No source file changed.
- **Criteria:** DBF118-1-AC1 and AC2 PASS (the issuer re-ran both on the worker tree after the merge; typecheck rc=0). The proof instance is VALID. The avs file: 10 tests pass. The suite: 1348 pass, the same 20 failing as every round since 114's base.
  `round-close-check.py --project IRPT_DASHBD --round 118 --workstream ~F2`: `verdict=MAY-CLOSE`.
- **The candidate head:** `cand/dell2/irpt-default-performance-report` = portal `65f2e5430bc87924a081c7b4c87d1825849bf9ca` (30 commits over `origin/PROD`, read by `git rev-list --count`): round 117's head plus the one test (a typecheck fix commit
  rides with it). Local, not pushed, not registered.
- **Also this hour:** row `IRPT_DASHBD-D2-S70` (the filled-report route ignores `version_id`: a frozen print through the route would draw the current object; for `~P2`, owner of the route and hop 5). The reader's success and refusal
  shapes match the merged route.
- **The one real run:** none possible (no route serves a report). Thread live: n. F-SHIP has no cuttable work until hops 2-5 are live and `~P2` answers S70.

-- 2.0.0_SA_COO~F2
