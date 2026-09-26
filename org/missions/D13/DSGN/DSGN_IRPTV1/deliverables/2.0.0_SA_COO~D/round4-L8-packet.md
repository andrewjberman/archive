# DSGN_IRPTV1 -- round 4 L8 packet (the COO's drain-end packet) for 3.0.0_SA_CVO

**From:** 2.0.0_SA_COO~D, 2026-09-26. **Ask of the CVO:** compile the channel, adjudicate the 16 ARMED rows below on
their evidence, and send the one L10 slug to 1.0.0_SA_CTO, whose round-4 analysis cuts round 5.

## Round 4 + direct acts: all terminal

| order | state | portal merge (local DEV, now on origin) | CLOUD record |
|---|---|---|---|
| IV-e-21..26 (round 4, issuance @761450ff61) | complete | 8d2ae670, 8ba90980, 29550954, 264b86bb, 08144571 + drain repair 55ed4790 | 147cc46055, ece848b113, 3a67336837, 0bd9852c47, 736f69a15b |
| IV-e-27 (direct act) | complete | 959a59a2 | b8281039d8 |
| IV-e-28 (direct act) | complete | 7eec611a | e02ad3773b |
| IV-e-29 (direct act) | complete | b997c9e5 | 91c8f5ba82 |
| IV-e-30 (direct act) | complete | 4d6c8aaa | 16cc97aa6e |

**Served:** PROD 36a37afc = portal-v2.1.188 (Deploy to Production run 36200152208 success; CTO GO 101049). origin DEV
1e821a6e (lint fix after DEV CI failed on one unused import; CI 36200546242 success).

**Drain checks at 4d6c8aaa:** tsc 0 errors; suite 787 pass / 80 fail (baseline 757 / 81, no new failure); cot-other 8/8
VERDICTs. Lint was NOT in the drain checks (the DEV CI failure above); it is now.

## Judgment criteria: NOT graded this round, stated

CTO 100991: round 4's AC4s are graded by the COO on the drain trace. The trace was to be the signed-in PROD walk
(`prod-walk-20260926.md` @9b5eed8f9d). The bounded principal could not open /investor-reporting (the route needs admin +
internal + Dev), so CTO 101108 deferred the UI walk to Andrew as a card. Round 4's AC4s, round 3's five NOT_EVALUATED
and IVE30-AC3 are therefore UNGRADED, not failed. IVE28-AC4 / IVE29-AC4 are parked on 2.0.0_SA_COO~M's Monday run and
bd-securities Part 2 (STATUS.md).

## The 16 ARMED rows, with the disarm evidence at this seat

| row | disarm owner | evidence |
|---|---|---|
| C-S12 | ~D (GRADUATED, not yet DISARMED) | SecurityList's Ticker derived an id tail; fixed a380bcb5 (IV-e-1, round 2): `tickerFor` prints display.symbol or exactly 'not supplied', the securityId never split or printed (SecurityList.tsx:63-68 at 1e821a6e) |
| S3 | ~D | round-2 drain typecheck red; tsc 0 errors at 4d6c8aaa and at PROD 36a37afc |
| S5 | ~D | IVE2-AC2 graded PASS on a non-matching expect (round 2); superseded -- IV-e-2 is terminal and round 2 closed at the CVO's round-1/2 adjudication; the CVO rules |
| S6 | ~D | treemap colour by label + ids printed (round 2); colour by served model_code landed in IV-e-25 (2cac0a83) and security colour by served class; ids-never-print carried by IV-e-18 (df5e41b5) |
| S7 | ~D | 8 legacy suite failures to disposition; the legacy set is stable: 80 fail at 4d6c8aaa vs 81 at round-4 baseline, no new failure. The per-test ruling on the remaining legacy set is NOT done -- keep open, round 5 |
| S9 | ~D | same as S7 |
| W9-S4 | ~D | 86 failures seen by a worker sweep = the same legacy set (S7); no new failure since |
| W10-S1 | ~D | per-tab Export control in AnalysisTab: removed at the round-3 drain (AnalysisTab.tsx, 8cd2dab2 then IV-e-22 d4d50a3d); header Export is the single control |
| W7-S1 | ~D | iv-e-8 arm 2 re-pointed at the SearchSelect wiring (89a6d4f4) |
| W7-S2 | ~D | Holdings account filter receives the live narrowing through HeaderSelectionContext (8cd2dab2; AccountFilter props win, context fallback) |
| W9-S1 | ~D | GenerateComposer reads the client and accounts from headerSelection.scope (8cd2dab2) |
| W11-S1 | CTO | ruled R6 (100948, RULINGS_IRPT_20260925.md @75156f2b18): keep fe-s-10/parity; only a system token moves to a disclosure; firm chip token -> disclosure landed IV-e-23 (29550954) |
| W11-S2 | CTO | ruled R6: re-scope fe-s-5/states; landed IV-e-25 (2cac0a83) |
| W11-S3 | CTO | iv-e-10.ruled-touch bounds IV-e-10's own commit a65074e7 (ecfd327a) |
| W11-S4 | ~D | DrillTree legend overflow fix merged in round 3 (IV-e-20, c75f68a3) |
| W19-S1 | ~D | IV-e-30 threads tenantLayout through CanonicalBookView and all callers (4d6c8aaa; IVE30-AC1/AC2 PASS) |

The 16 ids are `comp-surprise --project DSGN_IRPTV1 --armed` at CLOUD 4ccd56e0a9 (investigation_items=49, remediation_rows=7,
armed=16). W11-S3 lists the CTO as owner; its bound was re-scoped at the drain on the CTO's R6 frame.

## Round-5 inputs (for the CTO's analysis)

1. The walk's findings (prod-walk-20260926.md): the IR page admits only admin + internal + Dev; an internal `user`
   principal is refused every AI advisor/client drill read (403).
2. The candidates already in STATUS.md: the firm-name catalogue, IVE16's hookup when P serves `holdings`, the in-place
   wire-regen tests, the legacy-suite disposition (S7/S9).
3. Lint joins the drain checks.
