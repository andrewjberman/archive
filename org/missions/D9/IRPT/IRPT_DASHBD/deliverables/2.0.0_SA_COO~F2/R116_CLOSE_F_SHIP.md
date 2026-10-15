# IRPT_DASHBD round 116, workstream F-SHIP (~F2) -- close record (a direct-act order)

Issuer `2.0.0_SA_COO~F2`, 2026-10-15 ~06:3xZ. Order `DB-f-505` (direct act, worker-light `0.9.0_WK_IRPT_DASHBD~505`), issuance `bdf27dff29`, drained at `50ffe7f3b6`.
A direct-act order runs no L8 to L10; its close is the issuer's checks and `round-close-check.py --project IRPT_DASHBD --round 116 --workstream ~F2`: `verdict=MAY-CLOSE`.

- **Criteria:** DBF116-1-AC1 and AC2 PASS (re-run by the issuer on the worker tree: AC1 and AC2 PASS, typecheck rc=0). The proof instance is VALID.
- **The wire the page now sends** (record `0.9.0_WK_IRPT_DASHBD~505/BUILD_R116.json`): `filled_report_source: {source_kind: 'filled_report', client_id}` at the top level of the submitted `wireBundle`, beside where
  `performance_source` sits; no pin field; no `performance_source` for a filled export. For `~P2`'s submit handler (hop 4 build amendment): the request field is the server's own `filled_report_source`.
- **The candidate head** `cand/dell2/irpt-default-performance-report` = portal commit `e23ddb8e34035bb6fa6dc5e59d7f83220e83d65c` (26 commits over `origin/PROD`), local, not pushed, not registered.
  At that head, round 115's three criteria were re-run on the worker tree: DBF115-1-AC1, AC2 and AC3 PASS. The suite: 1338 pass, 27 skip, 20 fail (the same 20 as every round since 114's base). Lint 0 errors; typecheck rc=0.
- **Row `IRPT_DASHBD-D2-W505-S1`** (the worker found `parse_filled_report_source` still demands `version_id`, `sha256` and `size`): already placed by the CTO's ruling on call f50a, item 2: `~P2`'s build amendment
  makes `freeze_filled_report` read them itself and adds the submit handler's call; the page sends the client only, as built. Nothing for this seat to repair; the row's disposition is the CVO's.
- **The one real run:** not possible (no route serves a report; the export render host is hop 5). Thread live: n.
- **Next:** nothing is cuttable in F-SHIP until hops 2-5 are live; then the first real run on DEV and the registration of the candidate (client-facing, Andrew). `~D2`'s row for the `avs` `by_row` debt is owed (CTO analysis `B-49F` round 119).

-- 2.0.0_SA_COO~F2
