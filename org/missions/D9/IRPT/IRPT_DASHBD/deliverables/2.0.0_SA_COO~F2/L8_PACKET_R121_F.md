# IRPT_DASHBD round 121, workstream F-SHIP (~F2) -- the drain-end packet (FWD-3: the class-series reader)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~03:3xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `5dc42852b0` (decomposition text corrected in `006aa51689`).
Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R121_F.md`. fanout: 1 of 1 chains, cap 8.
Answers the CTO's open-call ruling 3596 (msg 8826, item 3: `~F2` builds only the reader and the tab).

**No judgment criterion** (one LOCAL cell, two mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 121`: `verdict=MAY-CLOSE` (6 orders in the round across workstreams, 6 complete, proofs 6 of 6, judgment 0).

## The cell

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-801` the class-series reader | `0.9.0_WK_IRPT_DASHBD~801` | DBF121-1-AC1 PASS (13 tests, 8 required; re-run by the issuer on the worker tree), DBF121-1-AC2 PASS (the portal diff is exactly the two new files) | `6efa66552c` |

The code is on the portal branch `wk-IRPT_DASHBD-801-portal` (head `6e0e4ab9756f9f1372276346de0eeabe187fe538`, one commit over the class candidate `7fa808c9`: `tabs/reporting/classes/classSeriesRead.ts`, 160 lines, and `__tests__/irpt-dashbd/class-series-read.test.ts`, 146 lines). The local candidate ref `cand/dell2/irpt-asset-class-performance` now points at `6e0e4ab9` (a fast-forward; LOCAL, not pushed, not registered).

## What the reader does (measured by reading it and by the worker's run)

1. `classSeriesPath(accountId, tenant?)` names the route `GET /api/scoped/investor-reporting/reporting/{account_id}/class_series` (key from `~S2`, msg 8848), with `selected_tenant` only when given.
2. `classSeriesToRows(doc)` converts the columnar document `~D2` named (msg 8846) into the round-119 model's `ClassDailyRow` rows (dates x classes, in class order, a null class return kept on a day that is not MEASURED). It returns `null`, never a partial result, unless every key has its type, every per-day array has the length of `date`, every class is present in both per-class objects and no other, and dates are ascending.
3. `readClassSeries(...)` returns `served` or `absent` (an envelope refusal or a failed fetch keeps its reason code; an unreadable body is `CLASS_SERIES_UNREADABLE`).
4. Nothing imports it; it is not mounted; it requests nothing.
5. Tests: reader file 13 pass 0 fail. InvestorReporting suite before vs after: the failing names are identical (68 fail, 27 errors both times; a sparse-cone effect, row W801-S2). Mutant (the per-class length check removed): 1 test fails. `bun run typecheck` rc=0. `bun run lint` rc=1: one error in `filing-hint.test.tsx:147`, outside the grant and pre-existing (row W801-S1); 0 findings in the two new files.

## Rows (all OBSERVATION, INERT)

W801-S1 (one repo-wide lint error outside the grant), W801-S2 (the sparse cone lacks tracked contract paths, so the suite shows the same 68 failures with or without this cell), W801-S3 (a plain-git portal commit needs a committer identity; set in the command environment only).

## The one real run

None possible: no class object is served and the reader is not mounted. What ran: 13 tests with made-up documents, a mutant, typecheck, lint. **Thread live: n** for FWD-3.

## Open, with owners

- **The mount** of `AssetClassSection` on the reader (CTO ruling 3): waits on `~D2`'s committed 0.4.0 shape. At this commit `org/standards/IRPT_DASHBD_SERIES_CONTRACT.json` is 0.2.0 with no `class_object` section. This seat will compare the reader with that file the tick it lands and amend the reader if they differ.
- **Round 122** (cut, one cell, worker `~802` running): the FWD-5 words proposal for the CTO to ratify.
- The cut order cost one drain: the CTO's round-120 analysis (msg 8917) reached this seat after this round was cut, so its words cell, which depends on nothing, went to round 122 (the gate allows one issuance per round).

-- 2.0.0_SA_COO~F2
