# IRPT_DASHBD round 150, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-16)

The page mirror takes on series contract 0.3.3 (cell DB-c-30). Issuance `bd95b6dec7`; merge `b8bff882d4` (worker ~421). Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md` section 19. `python .tools/round-close-check.py --project IRPT_DASHBD --round 150 --workstream B-CW`: `verdict=MAY-CLOSE` (1 order, 0 judgment). `DBC151-1-AC1` and `-AC2` PASS, re-run by this seat; typecheck rc 0; `proof-of-spec-check` VALID. Push: integrator-only; the merge and this commit are LOCAL.

## What happened

- Trunk contract moved to 0.3.3 (`~D2`, drain `40476cbde7`: `history_scope_claim` and `history_scope_basis` join `series.optional`, per your rulings on row `D2-S113`). `~D2` did not message the landing; I measured it at the tick: the page mirror (six names) no longer equalled the contract, so `iv-e-124` was red on trunk. DB-c-30 (one file, `seriesContract.ts`) makes `SERIES_OPTIONAL` the eight names in order and declares both new members as optional strings. The page prints nothing for them: `Returns from <date>.` already prints for any `history_scope` other than `FULL`, which is the rule you ruled.
- Class by your rule (msgs 9136, 9144): the candidate `cand/dell2/irpt-series-mirror-contract-033` @`831f974aa1` is two commits on the PROD tip `8012cd1afbaa` (the 0.3.1 mirror, re-cut, and DB-c-30), one file, +10 -1. Vite builds of origin/PROD and of the candidate are BYTE-IDENTICAL (88 of 88 dist files, 63 of 63 JS and CSS chunks, chunk-set hash `8890552b43cca4fe` both; the positive control is on record in `DB_C26_BUILD_BYTES_R148.md`): `deliverables/2.0.0_SA_COO~C2/prod_promote/DB_C30_BUILD_BYTES_R150.md`. Approval row `dell2-20261016T112339Z-6099`, class **opal-internal**, OPEN. On the candidate: `iv-e-124` and the round 147 test 9 of 9, typecheck rc 0.

## What the CTO's half decides

1. Approve row `6099` (opal-internal on the measured bytes). After it, an opal-internal PROD promote needs no word from Andrew (the push law); the DT's promote order follows on your word, as for 92c0, so PROD's mirror equals the contract and `iv-e-124` is green in any tree.
2. Nothing else is held for Andrew.

## Rows

`D2-S115` (this commit) dispositions worker 421's `W421-S1` and `W421-S2` (INERT, accepted). Nothing ARMED or BLOCKING of this round.

## Issuer's own defects this round

None found. (The proof instance carried the order stem, and the order status flip, row and packet are in this commit.)
