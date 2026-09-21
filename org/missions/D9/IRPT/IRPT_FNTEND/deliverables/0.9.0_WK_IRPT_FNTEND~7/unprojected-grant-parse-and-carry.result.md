# IRPT_FNTEND.TO-FE-s-57 -- result (0.9.0_WK_IRPT_FNTEND~7)

Portal commit `b92448f3042e76718ede00d1f60acd882e9ca0dd` on branch `wk-irpt_fntend-9-8-fe-s-57-portal` (LOCAL, portal frozen, not pushed).

## What landed
- `contracts/index.ts`: new exported `UnprojectedGrant` interface; `Availability` gains `unprojectedGrant?: UnprojectedGrant | null` (OPTIONAL -- see row IRPT_FNTEND-W7-S1 for why not the order's literal non-optional text).
- `contracts/adapt.ts`: `EnvelopeParts.unprojectedGrant`; `wireEnvelope()` defaults every existing call site to `null`; new `carryUnprojectedGrant()` mirroring `carryAvailabilityFromStatus`'s recursion/null-safety exactly; `carryAvailabilityFromStatus` itself now carries `unprojectedGrant` forward unchanged.
- `contracts/envelope.ts`: `IrEnvelopeField` gains `'unprojected_grant'`; `parseIrEnvelope` refuses a non-refused response missing/misshaping the key (`EnvelopeMismatch('unprojected_grant', operation)`), unconditionally -- `irpt-holdings` is NOT special-cased (F57-AC3 confirms the general rule already handles it).
- `__tests__/fe-s-57/carry.test.ts`: F57-AC2..AC5, built from the same route/schema/producer-fixture harness as `fe-s-14/envelope.test.ts`.

## Criteria
F57-AC1..AC5: PASS by measured output (see proof-of-spec instance).

F57-AC6 and F57-AC7: **FAIL as measured.** The order's own BOUNDS mandates an unconditional throw ("binds every non-refused response ... do not special-case"), and F57-AC6/AC7 demand `0 fail` on the existing suite. Both cannot hold at once inside this cell's `<paths>` grant: ~52 pre-existing tests across ~20 files outside the grant (fe-s-1, fe-s-14, fe-s-19, fe-s-25, fe-s-26, fe-s-30, fe-s-31, fe-s-33, fe-s-34, fe-s-35, fe-s-39, fe-s-41, fe-s-42, fe-s-48, fe-s-49) build non-refused response bodies with no `unprojected_grant` key, and now throw. Filed as row `IRPT_FNTEND-W7-S1` (BLOCKING, ARMED, `disarm_owner 2.0.0_SA_COO~F`). The order's `<status>` stays `pending` -- not flipped to `complete`.

F57-AC8: judgment criterion, RECORDED, no verdict (per the order).

## Proof-of-spec
`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~7/IRPT_FNTEND.TO-FE-s-57.unprojected-grant-parse-and-carry.proof_of_spec.json`
