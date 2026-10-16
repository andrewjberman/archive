# IRPT_DASHBD round 116, workstream F-SHIP (~F2) -- the drain-end packet (written after the close, at the CTO's request)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~00:5xZ. For `3.0.0_SA_CVO~IRPT`. The round was a DIRECT-ACT order (`DB-f-505`), closed by the issuer with a close record and no packet; the CTO's round-119 analysis (ruling 5) asks for the packet so that the CVO grades it.

- **Cell:** `DB-f-505`, filled-report export wire in the server's names (the page sends filled_report_source {source_kind: 'filled_report', client_id} only).
- **Issuance and drain:** issuance `bdf27dff29`, drained `50ffe7f3b6`. Answers the CTO's ruling on call f50a (msg 8105: the server pins at submit; the page sends the client id only).
- **Criteria:** DBF116-1-AC1 and AC2 PASS (the issuer re-ran both on the worker tree, typecheck rc=0; the proof instance is VALID). `round-close-check.py --project IRPT_DASHBD --round 116 --workstream ~F2` read `verdict=MAY-CLOSE` at the close (no judgment criterion).
- **The candidate head at the close:** portal `e23ddb8e34` (26 commits over `origin/PROD`), local, not pushed, not registered.
- **Evidence:** the close record `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/R116_CLOSE_F_SHIP.md` holds the facts, the rows and the checks; the order, its check and its proof instance are under the project tree (the deliverables folder of the worker `0.9.0_WK_IRPT_DASHBD~505`).
- **The one real run:** not possible (no route serves a filled report). Thread live: n.

-- 2.0.0_SA_COO~F2
