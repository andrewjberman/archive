# IRPT_DASHBD round 117, workstream F-SHIP (~F2) -- the drain-end packet (written after the close, at the CTO's request)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~00:5xZ. For `3.0.0_SA_CVO~IRPT`. The round was a DIRECT-ACT order (`DB-f-506`), closed by the issuer with a close record and no packet; the CTO's round-119 analysis (ruling 5) asks for the packet so that the CVO grades it.

- **Cell:** `DB-f-506`, the avs benchmark members read as by_row per account, pinned by a new test file (finding reads_by_row; no source change; the disarm of row D2-S64 is row D2-S67).
- **Issuance and drain:** issuance `c8794f1232`, drained `1c3ea59e4b`. Answers the CTO's B-49F round-119 analysis, ruling 6 (the ~F2 debt) and row D2-S64.
- **Criteria:** DBF117-1-AC1 and AC2 PASS (the issuer re-ran both on the worker tree, typecheck rc=0; VALID instance). `round-close-check.py --project IRPT_DASHBD --round 117 --workstream ~F2` read `verdict=MAY-CLOSE` at the close (no judgment criterion).
- **The candidate head at the close:** portal `0d58fe2c43` (28 commits over `origin/PROD`), local, not pushed, not registered.
- **Evidence:** the close record `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/R117_CLOSE_F_SHIP.md` holds the facts, the rows and the checks; the order, its check and its proof instance are under the project tree (the deliverables folder of the worker `0.9.0_WK_IRPT_DASHBD~506`).
- **The one real run:** not possible (no route serves a filled report). Thread live: n.

-- 2.0.0_SA_COO~F2
