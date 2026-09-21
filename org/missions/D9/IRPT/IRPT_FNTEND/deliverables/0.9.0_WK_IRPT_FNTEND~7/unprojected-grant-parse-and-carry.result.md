# IRPT_FNTEND.TO-FE-s-57 -- result (0.9.0_WK_IRPT_FNTEND~7)

Portal commits, in order, LOCAL on branch `wk-irpt_fntend-9-8-fe-s-57-portal` (portal frozen, not pushed):
- `b92448f3042e76718ede00d1f60acd882e9ca0dd` -- the parse-and-carry design
- `897dc5be` -- AMENDMENT 1: completed ~15 pre-existing test fixtures with `unprojected_grant`
- `9094772a` -- AMENDMENT 1: regenerated the three per-firm fe-s-14 smoke maps through their own ONE WRITER
- `0cb9b2ba` -- AMENDMENT 2: completed fe-s-32/holdings-no-answer.json and fe-s-47/no-status-reason.test.ts's envelopeBody()
- `b8c5df09` -- self-diagnosed follow-on: F47-AC9's extraction control excludes `unprojectedGrant` from its comparison

**Final HEAD for wave B to seat against: `b8c5df09`.**

## Final measured state (this worktree)
- F57-AC1 (typecheck): `rc=0`
- F57-AC2..AC5 (`carry.test.ts`): `4 pass / 0 fail`
- F57-AC6 (`fe-s-1` + `fe-s-14`, bun's substring match): `274 pass / 2 skip / 0 fail` -- **PASS**
- F57-AC7 (whole suite): `590 pass / 21 skip / 1 fail` of 612 -- **FAIL**, the sole residual being `fe-s-49/admin-gate.test.ts F49-AC8`, which fails because this isolated worktree's `src/App.tsx` carries 2 hunks unrelated to `unprojected_grant` (an `ArrowLeftRight` import, a `Trade Submission` nav mark). `App.tsx` has never been in this cell's `<paths>` in any version of the order. The coordinator's own AMENDMENT 2 message reports this ALREADY RESOLVED in the merged tree (portal `d67d550f`, via sibling `FE-s-51`'s unrelated work) -- but this worker's isolated worktree branched off DEV before that fix landed and workers do not merge branches. Expected to resolve automatically at the COO's drain.
- F57-AC8: judgment, RECORDED, no verdict.

Per the order's own rule ("If both read 0 fail, flip `<status>` to `complete`"), since F57-AC7 measures 1 fail (not 0) in this worktree, `<status>` stays `pending`.

## What amendment 2 fixed
- `__tests__/fe-s-32/holdings-no-answer.json`: all 9 non-refused envelopes completed with `unprojected_grant`. Fixture only, no test assertions touched. Closed 3 of the 5 residual fails (its own scenario-maps test, and both of `fe-s-41`'s `F41-AC5` subtests, which read this same shared fixture).
- `__tests__/fe-s-47/no-status-reason.test.ts`: `envelopeBody()` helper completed with `unprojected_grant`, closing the module-load-time throw that crashed the whole file as one `error`. The RULES table `FE-s-53` added was not touched.
- Self-diagnosed follow-on (same file, same session): completing `envelopeBody()` broke `F47-AC9`'s own extraction control, which compares a standalone re-execution of `carryAvailabilityFromStatus` against the full `parseIrEnvelope` pipeline's output -- the two now differed on `unprojectedGrant` alone, since the full pipeline's separate `carryUnprojectedGrant` step is never modeled by the narrow extraction. Fixed by excluding `unprojectedGrant` from both sides of the comparison, preserving the control's own stated purpose (the partialReason/state carry, RULING V). Filed as row `IRPT_FNTEND-W7-S3` (OBSERVATION, INERT).

## Rows filed
- `IRPT_FNTEND-W7-S1` -- answered by AMENDMENT 1.
- `IRPT_FNTEND-W7-S2` -- answered by AMENDMENT 2 for 2 of 3 named causes; the third (`src/App.tsx`/F49-AC8) remains, ARMED, `disarm_owner 2.0.0_SA_COO~F`.
- `IRPT_FNTEND-W7-S3` -- new, OBSERVATION/INERT, self-resolved within grant.

## Proof-of-spec
`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~7/IRPT_FNTEND.TO-FE-s-57.unprojected-grant-parse-and-carry.proof_of_spec.json` -- `proof-of-spec-check.py` rc=0 (structurally VALID; F57-AC7 carries `status: FAIL` by its own printed output, so the `complete` flip is correctly withheld).
