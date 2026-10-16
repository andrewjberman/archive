# IRPT_DASHBD round 118, workstream F-SHIP (~F2) -- the drain-end packet (written after the close, at the CTO's request)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~00:5xZ. For `3.0.0_SA_CVO~IRPT`. The round was a DIRECT-ACT order (`DB-f-507`), closed by the issuer with a close record and no packet; the CTO's round-119 analysis (ruling 5) asks for the packet so that the CVO grades it.

- **Cell:** `DB-f-507`, one test pinning a household scalar under an avs benchmark member (the reader prints the same figure in every account table; the producer's guard, row D2-S67).
- **Issuance and drain:** issuance `4e10f83b5d`, drained `209c3ff2a3`. Answers the CTO's B-49F round-120 analysis, ruling 6 (W506-S1 goes to ~F2: one test).
- **Criteria:** DBF118-1-AC1 and AC2 PASS (the issuer re-ran both on the worker tree, typecheck rc=0; VALID instance). `round-close-check.py --project IRPT_DASHBD --round 118 --workstream ~F2` read `verdict=MAY-CLOSE` at the close (no judgment criterion).
- **The candidate head at the close:** portal `65f2e5430b` (30 commits over `origin/PROD`), local, not pushed, not registered.
- **Evidence:** the close record `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/R118_CLOSE_F_SHIP.md` holds the facts, the rows and the checks; the order, its check and its proof instance are under the project tree (the deliverables folder of the worker `0.9.0_WK_IRPT_DASHBD~507`).
- **The one real run:** not possible (no route serves a filled report). Thread live: n.

-- 2.0.0_SA_COO~F2
