# IRPT_FNTEND.TO-FE-s-57 -- result (0.9.0_WK_IRPT_FNTEND~7)

Portal commits, in order, LOCAL on branch `wk-irpt_fntend-9-8-fe-s-57-portal` (portal frozen, not pushed):
- `b92448f3042e76718ede00d1f60acd882e9ca0dd` -- the parse-and-carry design (contracts/index.ts, adapt.ts, envelope.ts, __tests__/fe-s-57/carry.test.ts)
- `897dc5be` -- AMENDMENT 1: completed ~15 pre-existing test fixtures with `unprojected_grant`
- `9094772a` -- AMENDMENT 1: regenerated the three per-firm fe-s-14 smoke maps through their own ONE WRITER

**Final HEAD for wave B to seat against: `9094772a`.**

## What landed
- `contracts/index.ts`: new exported `UnprojectedGrant` interface; `Availability` gains `unprojectedGrant?: UnprojectedGrant | null` (OPTIONAL -- see row IRPT_FNTEND-W7-S1 for why not the order's literal non-optional text).
- `contracts/adapt.ts`: `EnvelopeParts.unprojectedGrant`; `wireEnvelope()` defaults every existing call site to `null`; new `carryUnprojectedGrant()` mirroring `carryAvailabilityFromStatus`'s recursion/null-safety exactly; `carryAvailabilityFromStatus` itself now carries `unprojectedGrant` forward unchanged.
- `contracts/envelope.ts`: `IrEnvelopeField` gains `'unprojected_grant'`; `parseIrEnvelope` refuses a non-refused response missing/misshaping the key (`EnvelopeMismatch('unprojected_grant', operation)`), unconditionally -- `irpt-holdings` is NOT special-cased (F57-AC3 confirms).
- `__tests__/fe-s-57/carry.test.ts`: F57-AC2..AC5.
- AMENDMENT 1: every hand-built non-refused response body across fe-s-1, fe-s-14, fe-s-19, fe-s-25 (via shared helper), fe-s-26 (via shared fixture), fe-s-30, fe-s-31, fe-s-33, fe-s-34 (via shared helper), fe-s-35, fe-s-39 (via shared fixture), fe-s-41, fe-s-42 (via shared fixture), fe-s-48 (via shared fixture), fe-s-49 (unaffected by unprojected_grant already), plus the fe-s-15 fixtures reached only via bun's substring path match -- completed with `unprojected_grant: {count: 0, denominator: <n>, kinds: []}`.

## Criteria
F57-AC1 (typecheck), F57-AC2, F57-AC3, F57-AC4, F57-AC5: **PASS**, unchanged since the first pass.

F57-AC6 (fe-s-1 + fe-s-14, bun's substring match): **PASS** -- `274 pass / 2 skip / 0 fail`. CLOSED by amendment 1.

F57-AC7 (whole suite): **FAIL as measured** -- `579 pass / 21 skip / 5 fail / 1 error` of 605, down from `532/52/1` before amendment 1. The residual, iteratively narrowed down and re-verified after each fix, traces to exactly one file this cell's grant does not reach (`__tests__/fe-s-32/holdings-no-answer.json`, needing the same completion as its in-grant sibling maps -- 3 of 5 fails) plus two pre-existing, unrelated defects confirmed present in the ORIGINAL pre-amendment run (`__tests__/fe-s-47/no-status-reason.test.ts`'s module-level throw, and `App.tsx`'s F49-AC8 gate-hunk mismatch). Filed as row `IRPT_FNTEND-W7-S2` (BLOCKING, ARMED, `disarm_owner 2.0.0_SA_COO~F`). The order's `<status>` stays `pending` -- not flipped to `complete`, per the order's own rule that F57-AC7 must read 0 fail first.

F57-AC8: judgment criterion, RECORDED, no verdict.

## Proof-of-spec
`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~7/IRPT_FNTEND.TO-FE-s-57.unprojected-grant-parse-and-carry.proof_of_spec.json` -- `proof-of-spec-check.py` rc=0 (structurally VALID; F57-AC7 carries `status: FAIL` by its own printed output, so the `complete` flip is correctly withheld).
