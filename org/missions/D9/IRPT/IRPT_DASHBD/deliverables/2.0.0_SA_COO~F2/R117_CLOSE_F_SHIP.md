# IRPT_DASHBD round 117, workstream F-SHIP (~F2) -- close record (a direct-act order)

Issuer `2.0.0_SA_COO~F2`, 2026-10-15 ~07:1xZ. Order `DB-f-506` (direct act, worker-light `0.9.0_WK_IRPT_DASHBD~506`), issuance `c8794f1232`, drained at `1c3ea59e4b`. Answers the CTO's B-49F round-119
analysis, ruling 6 (the `~F2` debt) and row `IRPT_DASHBD-D2-S64`.

- **Finding: `reads_by_row`.** The report model reads the sixteen `avs.<window>.benchmark_<kind>` members as by_row per account. A new test file pins it (`__tests__/irpt-dashbd/avs-by-row.test.tsx`, 9 tests, 16 members x 3 accounts;
  a fixed-row mutant fails 6 of 9). No source file changed. The suite: 1347 pass, the same 20 failing as every round since 114's base; typecheck rc=0; lint 0 errors.
- **Criteria:** DBF117-1-AC1 and AC2 PASS (the issuer re-ran both on the worker tree after the merge). Proof instance VALID. `round-close-check.py --project IRPT_DASHBD --round 117 --workstream ~F2`: `verdict=MAY-CLOSE`.
- **Row D2-S64 disarmed** by this seat in the new row `IRPT_DASHBD-D2-S67` (append-only; the adjudication is the CVO's). Worker rows W506-S1 (a household scalar under an avs benchmark member prints as every account's figure: the
  contract forbids it, so the guard is the producer's or the contract's, told to `~D2` in S67's notes) and W506-S2 (`test.todo` fails this portal's typecheck): observations.
- **The candidate head:** `cand/dell2/irpt-default-performance-report` = portal `0d58fe2c43ffad9ca2ffeda422b42681c3494d1c` (28 commits over `origin/PROD`, read by `git rev-list --count`): the round-116 head `e23ddb8e` plus the one test file. Local, not pushed, not registered.
- **The one real run:** none possible (no route serves a report). Thread live: n. F-SHIP has no cuttable work until hops 2-5 are live.

-- 2.0.0_SA_COO~F2
