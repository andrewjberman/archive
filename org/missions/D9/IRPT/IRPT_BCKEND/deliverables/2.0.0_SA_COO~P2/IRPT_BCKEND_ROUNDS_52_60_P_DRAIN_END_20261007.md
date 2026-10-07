# L8 drain end -- IRPT_BCKEND rounds 52-60, workstream ~P (plus IRPT_DASHBD rounds 15-17, workstream B)

**Issuer:** `2.0.0_SA_COO~P2` (dell2), successor of `2.0.0_SA_COO~P` | **Date:** 2026-10-07 ~07:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

The predecessor issued and drained every order below. It closed its session on 2026-10-06 with this packet still owed
(`org/tier1_exec/2.0.0_SA_COO/logs/2026-10-06/session_close_1945-2135Z_andrew_p.md`, Next Steps). This seat wrote the packet
from the commits and the proof instances at HEAD c59c5420ca.

Every order of these rounds is terminal and merged:
- 8 IRPT_BCKEND orders (IB-pr-321..328) and 4 IRPT_DASHBD orders (DB-b-23..26);
- `proof-of-spec-check.py` reads VALID on all 12 instances at HEAD;
- 0 JUDGMENT criteria;
- 0 unmerged worker branches and 0 linked worktrees on this box (`git worktree list` lists the main tree only).

Round 55 has no order. It was the r55 re-pin plan (@db3b9632d3), which IB-pr-324 applied in round 56.

**Laptop branches not covered here.** The laptop holds 17 unmerged IRPT_BCKEND branches that are not on origin
(inventory by laptop `1.0.0_SA_CTO`, msgs 14 and 24). The ~P-attributable ones are wk-IRPT_BCKEND-84, wk-IRPT_BCKEND-61,
wk-irpt_bckend-6-1f, irpt-p-fence-20260924 and portal irpt-opal-scope-p-portal-20260923. All of them are older than round 52.
They are read for content when they reach origin.

## IRPT_BCKEND

| order | round | drain | criteria | real run / served state |
|---|---|---|---|---|
| IB-pr-321 (S260 + S175 reason codes) | 52 | @0fff3d8363 (proof @6f268a40f8) | VALID | served in r57 and r58 (below) |
| IB-pr-322 (W124 reason codes, the rest) | 53 | @23f867773a | VALID | served in r57 and r58 |
| IB-pr-323 (r54 release census tooling, BUILD_ONLY=1) | 54 | @72067cbae8 | VALID | CI tooling; used for the r57 and r58 censuses (@68648784e5) |
| IB-pr-324 (r55 re-pin, approved set) | 56 | @f36a8cdefd (proof @1a8ac6451a) | VALID | 20 staged_from pins moved over 7 functions; served as r57 |
| IB-pr-325 (S335 second directory refresh fire) | 57 | @45ac71f1c7 | VALID under amendment 1 (@1b30e3b6d6, the cadence-token name) | REAL RUN: applied @fb8f047e40 (1 add, 0 change, 0 destroy). The first fire, read 2026-10-06 13:40Z @3680d1cd3c, moved all three latest.json keys. Ledger irpt-s335-retry-schedule-20261005 is CLOSED |
| IB-pr-326 (enforcer_for refusals reach the wire) | 58 | @abf14e56ba | VALID; control: 3 of 6 new tests fail at the old code | served in r58 |
| IB-pr-327 (a pointer without a key is NOT_READY) | 59 | @d8d8e7d868 | VALID | served in r58. The NOT_READY branch is tested offline only and was never invoked live |
| IB-pr-328 (re-pin served.py and loaders.py for r58) | 60 | @b81cc27203 | VALID | served in r58 |

**Releases in the window.** Each one was a targeted apply under both never-widen halves. Each ledger is CLOSED.

- r57: 13 of 13 legs, @7091e7b1d9. Four functions changed: irpt-49f-reporting-read-lambda, irpt-export-render,
  irpt-directory-search and irpt-holdings.
- r58: 13 of 13 legs, @7d87b57ffb. Same four functions. A firm with no bucket now answers FIRM_BINDING, where it answered
  UNEXPECTED before.

r54 (holdings-performance for 49F and INF, IB-pr-320) also closed in this window, @9bb0ab46b7.

## IRPT_DASHBD (workstream B)

| order | round | drain | criteria | real run |
|---|---|---|---|---|
| DB-b-23 (routes.json: the reporting routes are ROUTED_ELSEWHERE) | 15 | @487429cb60 | VALID under amendments 1 and 2 | committed declaration only |
| DB-b-24 (commit the E3 ruling and the pull record) | 15 | @28efce5b4d | VALID | committed record only |
| DB-b-25 (the BD runner never stops silently) | 16 | direct act @98d439936a (amendment 1 @91a4d48e89) | VALID; instance written and status flipped by `2.0.0_SA_COO~P2` in this commit. The <status> read `issued`, so the flip was owed. AC1 and AC2 PASS at HEAD. The negative arm fails AC1 at 577237bea4, the parent of the fix | the relaunch on the fixed runner completed the pull: 5,252 of 5,252 landed (ledger leg P1 @54cbe5a477) |
| DB-b-26 (E2 tie-out, 49F served return vs Black Diamond) | 17 | @0685c40ec0 | VALID | REAL RUN over 9,082 segments: 2,103 within 0.35 pp; 6,975 outside; 6,250 unexplained, of which 4,905 fall within tolerance once BD fees are netted (row W12-S1). Ledger irpt-dashbd-e3-bd-population-pull-20261004 is CLOSED (@fbc0ee59df) |

## Rows filed or moved in the window

| row | class | standing |
|---|---|---|
| S335 | BLOCKING | remedied by IB-pr-325 and the first-fire read @3680d1cd3c. Its disarm row is not filed. Owner: this seat |
| S338 | OBSERVATION | OPEN. Inflection holdings_performance_daily has no partition for 3 of 189 2026 trading days (05-11, 06-30, 08-10). Whether Inflection held positions on those days is UNMEASURED. Ledger irpt-inf-performance-serving-20261002 stays OPEN on it |
| S340, S341, S342 | OBSERVATION, INERT | OPEN. The A1 proofs of three export-render ledgers were never exercised. Exercising them needs one named export, and that is Andrew's call |
| W12-S1 (IRPT_DASHBD) | OBSERVATION | OPEN. The fee question (net-of-fees served return, or fees added to the closed reason set) is put to `1.0.0_SA_CTO` |
| S343 | OBSERVATION, INERT | NEW, this commit. build-and-upload.sh:354 uploads under the function name, not the key Terraform reads (measured at HEAD) |
| S344 | OBSERVATION, INERT | NEW, this commit. record-terraform-deploy.sh sweeps a dirty audit file into its commit, and each retry duplicates CHANGELOG entries. HELD from the predecessor's log; not re-measured |

The packet for rounds 47-51 (@4e3b64b6ea) carried four more rows. This packet does not re-read them:

- S218: BLOCKING, ARMED.
- S204: OBSERVATION.
- S252: OBSERVATION, parked.
- W80-S1: OBSERVATION, ARMED.

Their latest citing rows decide their state at the compile.

## Open ledgers of this workstream (`org/critical_paths/.open_deploys/`)

- irpt-adapter-render-grant-kms-20260927 and irpt-adapter-render-selection-20260927. These wait on `1.0.0_SA_CTO` (batch 270:
  r57 evidence closes neither).
- irpt-inf-performance-serving-20261002. This waits on row S338.
