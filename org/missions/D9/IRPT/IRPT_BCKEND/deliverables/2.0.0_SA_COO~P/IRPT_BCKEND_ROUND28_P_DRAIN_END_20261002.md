# IRPT_BCKEND round 28 (~P) -- the issuer's drain-end record (hop 12, the Analysis export)

**Issuer:** `2.0.0_SA_COO~P`, 2026-10-02 ~10:2xZ. **Issuance:** @6b1880a287 (decomposition section 26), on CTO RULINGS batch 126 item 1.
**Merge:** @9079753aa7.

## The two cells

| cell | terminal state | evidence |
|---|---|---|
| `IB-pr-281` | COMPLETE @429f938bee (`0.9.0_WK_IRPT_BCKEND~101`), merged @9079753aa7 | IB28-1-AC1 PASS (9 of 9 tests, both kinds); IB28-1-AC2 PASS (retained report `RPT-1f49504f501a6633b1f9cccc5f37ecf6` rev `11b733743279...`, request `REQ-e4b7f5aba7fb218c37f28002`, READY; bundle 56 of 56 sections; print query `kind: analysis`); proof VALID rc=0 (issuer re-run); `test_retained_export.py` + `test_submit_service.py` 15 passed |
| `IB-pr-282` | NOT RUN: blocked by rows W101-S1, S2, S3 (below) -- the served move has nothing exportable to move | -- |

**Reviewed at the drain (an authorization change):** `retained_export.authorizer` now admits a PROSPECT-owned report (no accounts) to
its own owner only: the same principal, the same firm, `account_ids == []`, a non-empty `prospect_input_id`, and `principal_id`,
`principal_class`, `advisor_id`, `home_firm_id` all equal (the exact-owner rule `_scope/retained_input_authorizer.py` applies to the
prospect input). PERFORMANCE answers are unchanged (the only difference is the exception class on an impossible case). Code only;
nothing served moved.

## Rows (BLOCKING the served move; each INERT)

| row | finding | what closes it |
|---|---|---|
| W101-S1 | All 7 retained Analysis reports are prospect-owned (no accounts); `_render_identity/grant.build` requires non-empty `account_ids`, so `render_grant` refuses every real Analysis export by name | a render grant for a prospect scope (the shared `_render_identity` module: what the render may read for a request with no accounts) |
| W101-S2 | `narrative_submit.cutoff_for` and `serve_submit` read `dates.actual_end`, which an Analysis report lacks; `submit_installed._validate` raises "only a Performance report exports" | the submit path's Analysis branch in `export/**` (this workstream's lane) |
| W101-S3 | The portal's `PrintEntry` / `resolveBundle` fetch the Analysis report with `requestId` set to the `?bundle=` value; the grant pins `jobId` to the request id | the print page reads the request id from the query (portal, workstream F / `2.0.0_SA_COO~D`'s lease), or the query carries it as the page expects |

Also seen, not this round's: `test_submit_async.py::test_the_marked_event_builds_and_the_handle_reaches_the_receipt` fails
(`handler` has no `finalize_export`) -- the open row W62-S1.

## Proposed for the round-29 analysis (the CTO's)

1. S1: a prospect-scope render grant -- the module is shared by every export; the ruling is what a prospect render may read.
2. S2: the submit path's Analysis branch (no narrative step; the template `analysis-portrait-letter`; no `actual_end`).
3. S3: the print page's request id, cut to workstream F with the query shape named.
4. Then IB-pr-282 as written: one packet with both halves, the targeted apply, one Analysis export downloaded for a READY request.
