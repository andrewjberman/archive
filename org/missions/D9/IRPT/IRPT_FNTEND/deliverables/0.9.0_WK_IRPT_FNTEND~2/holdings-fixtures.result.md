# TO-FE-s-26 -- holdings fixtures: result

Worker `0.9.0_WK_IRPT_FNTEND~2`, branch `wk-irpt_fntend-4-2-fe-s-26` (workspace and portal). Portal commits
`ed90ce2d` (the fixtures and `__tests__/fe-s-26/`) `f95fa1db` (FE-s-22 input re-point) and `346d2b90` (the pair correction), all LOCAL and never
pushed, because PORTAL IS FROZEN. Workspace base `f3b42b1e0b`; grant widened by the issuer at `bf95fb7b9a` and the bound corrected at `49f4026218`.

**Every mechanical criterion, F26-AC1 through F26-AC8, passes by output, and the order is flipped to `complete`.**
F26-AC9 is recorded without a verdict, for L9.

## History, in one paragraph

At `ed90ce2d`, F26-AC8 read `26 pass / 2 fail`. Two assertions in `__tests__/fe-s-22/capture-hash.test.ts`
(`:252` `defectiveFixtures.toHaveLength(3)`, `:282` `exact.toEqual([])`) asserted the round-2 maps' defective
state, but they read the LIVE files this order repairs. So F26-AC5 and F26-AC8 could not both pass. That file was
outside `<paths>`, so I refused and filed `IRPT_FNTEND-W2-S20` (BLOCKING). The issuer added the one file to
`<paths>` at `bf95fb7b9a`, with a bound: re-point only those two assertions' INPUT, do not change what either
claims, and show both readings. That was done at `f95fa1db`. My row `W2-S22` then showed that the bound had split a PAIR: FE-s-22's
exact-vs-suffix control read `exact` from the round-2 copy but `suffix` from the live map, where it hit
the real holdings `status`, so nothing was demonstrated. The issuer corrected the bound at `49f4026218`,
and at `346d2b90` both halves and the path denominator read the same round-2 copy.

## What changed

**Fixtures (`ed90ce2d`).** One `status` member added to the holdings envelope of each of the three maps, and
nothing else. numstat is 16/0, 22/0 and 22/0. Each file was re-parsed and compared with its original after
deleting the new member: equal in all three. All three members are legal v1 `StatusEnvelope`s: all six required
members are present, and `business_date` is present because every state here is answer-bearing, where the
schema's `allOf` requires it. Every `source_dates` value comes from the document's own fields, not from a clock.

**FE-s-22 test (`f95fa1db`, INPUT ONLY).** numstat 42/6.
- `roundTwoShapedSources()` parses each live map fresh and deletes exactly the holdings `status` FE-s-26 inserted.
  Before relying on it, I measured the result equal to the parsed maps at portal `25062fce` for 3 of 3. The maps
  have an empty diff between `25062fce` and `237a9027`, and the same diff over the fe-s-26 folder is non-empty, as
  a control.
- `:252`'s `verdict` and `:282`'s `exact` now read that copy. The live maps are printed beside each.
- **The two `expect(...)` lines are byte-identical:** 0 of the changed lines contains `expect(`.
- `capture-hash.ts`, the RULE, has an empty diff against HEAD and against `25062fce`.
- Every other arm still reads `fileSources` exactly as written.
- **Pair correction (`346d2b90`, numstat 6/5, bound `49f4026218`):** the control's `suffix` and its printed path
  denominator now read the same round-2 copy as `exact`, so the control reads ONE map. On it the exact path has
  0 hits in 325 paths, and the suffix hits `/api/scoped/investor-reporting/analysis/.data.extraction_validation.status`,
  a field on a different response. That is the false pass shown by output, and it matches FE-s-22's own output
  at `237a9027`. Again, 0 changed lines contain `expect(`, and `capture-hash.ts` is unchanged.

## The state given to each map, and why it is legitimate for that basis

This comes first because it is what F26-AC9 grades. Before choosing, I measured how the three maps actually differ,
using FE-s-22's own field walk:

- **observed vs target** differ at exactly **1** path: `nodes[].basis`.
- **observed vs missing-attribution** differ at **8** paths, all under `nodes[].classification`.
- Everything else is **identical in all three**: clocks, coverage (11 of 12 nodes resolved, a 4,200 USD remainder),
  custody totals, the source-set revision, and every node's provenance.

So a state based on any shared field would come out the same in all three maps and could not differ. Each state
below is argued from the one field that does differ. The contract never ties a state to a basis:
`StatusEnvelope.state` describes how complete the ANSWER is, and the `HoldingsSnapshot` contract section says
nothing about state per basis. The per-basis reasoning is therefore mine, written out here so the grader can reject it.

| map | state | public_reason_code | what in the document supports it |
|---|---|---|---|
| observed | `READY` | `OBSERVED_CUSTODY_SERVED` | Every node has `basis: OBSERVED`, `classification.authoritative: true` and `provenance.claim: "measured"`. The only source the answer rests on is custody, and it is named: `source_set_revision` = smartx, completed 2026-09-09, the same as the business date. Every field the document asserts can be asserted. |
| target | `UNCERTAIN` | `TARGET_BLEND_MODEL_REVISION_UNNAMED` | Every node has `basis: TARGET` and `model_id.namespace: OPAL_MDPF`. But `source_set_revision` has exactly **one** row, source `smartx`, which is the CUSTODY source. A target weight comes from the model definition, and the document gives no revision or as-of date for the models anywhere. The weights are present, but whether they are current cannot be asserted. UNCERTAIN is an answer-bearing state that says exactly that. |
| missing-attribution | `PARTIAL` | `NODE_ATTRIBUTION_UNAVAILABLE` | `classification` is **absent on every node**. That is legal, because the schema makes it optional on a node, but it means the supervision and billing split cannot be asserted at all. PARTIAL is the contract's "the payload's data fields may not be asserted as complete". The view derives "Narrow the scope" as the remedy for PARTIAL, and that suits this map, because the schema defines classification as authoritative per scope. |

**The weakest of the three, stated against my own case:** the `target` argument rests on something the document
leaves out (it names no model revision), not on anything it states. Also, the same unnamed source sits in the
observed map, where it does no harm because an observed answer does not depend on the models. A grader who reads
"UNCERTAIN" as "chosen to be different from READY" should weigh that. I also avoided one option on purpose:
`UNCERTAIN` is the parser's *explicit-unknown* value (`EXPLICIT_UNKNOWN_STATE`), so giving it to the
missing-attribution map would have looked identical, at the view, to a map with no `status` at all. On `target` it is
told apart by its reason code, which a map without a status does not have.

**The cost of three distinct states** (row `IRPT_FNTEND-W2-S21`, OBSERVATION, ARMED): `HoldingsTab` mounts its body
only on READY. So only `observed` shows its basis as holdings content. `target` and `missing-attribution` show the
status panel, and their basis appears only through the reason code. With all three READY, all three bases would be on
screen and the bodies would still differ, but that fails F26-AC3 as written. The criteria settled the choice; the row
records what it costs FE-s-18. The issuer has said the row reaches FE-s-18's re-run.

## Criteria

| id | invocation (from `<WS>/portal`) | graded at | deciding output | verdict |
|---|---|---|---|---|
| F26-AC1 | `timeout 180 bun run typecheck; echo rc=$?` | `346d2b90` | `$ tsc -b --noEmit` / `rc=0` | PASS |
| F26-AC2 | `timeout 120 bun test .../fe-s-26/fixtures-carry-status.test.ts` | `ed90ce2d` | `HOLDINGS MAPS CARRYING status: 3 of 3` | PASS |
| F26-AC3 | same file | `ed90ce2d` | `STATES DISTINCT ACROSS THE THREE: 3 of 3` | PASS |
| F26-AC4 | same file | `ed90ce2d` | `ENVELOPES STILL VALID: 27 of 27` | PASS |
| F26-AC5 | `timeout 120 bun test .../fe-s-26/not-defective.test.ts` | `ed90ce2d` | `DEFECTIVE FIXTURES: 0 of 3` | PASS |
| F26-AC6 | same file | `ed90ce2d` | `RULE IS IMPORTED, NOT COPIED: 1 module` | PASS |
| F26-AC7 | `timeout 120 bun test .../fe-s-26/renders-differently.test.ts` | `ed90ce2d` | `PANELS DISTINCT: 3 of 3` | PASS |
| F26-AC8 | `timeout 120 bun test .../fe-s-26 .../fe-s-22` | `346d2b90` | `28 pass` / `0 fail`, rc=0 | PASS |
| F26-AC9 | judgment | -- | recorded above; no verdict | RECORDED |

**Why AC2–AC7 were not re-run:** they are graded at `ed90ce2d`. `git diff --name-only ed90ce2d 346d2b90` lists one
path, `fe-s-22/capture-hash.test.ts`, and none of those six tests reads it. Their inputs are byte-identical at the
final HEAD, so a second run would repeat the first rather than confirm anything.

**Both readings, from F26-AC8's own output at `346d2b90`:**
```
ROUND-2 SHAPED COPY (status absent): DEFECTIVE FIXTURES: 3 of 3
LIVE MAPS (repaired by FE-s-26): DEFECTIVE FIXTURES: 0 of 3
EXACT '/api/scoped/investor-reporting/holdings/.status' (round-2 shaped copy, status absent, 325 paths): 0 hit(s)
PATH DENOMINATOR: 325 paths in src/pages/InvestorReporting/fixtures/smoke/fe-s-18-holdings-observed.json (round-2 shaped copy, status absent)
EXACT '/api/scoped/investor-reporting/holdings/.status' (live map, repaired by FE-s-26): 1 hit(s)
SUFFIX 'status': 1 hit(s) -- /api/scoped/investor-reporting/analysis/.data.extraction_validation.status
```

**Controls, each run and each firing:**
- AC2: delete one status in memory and it reports 2 of 3.
- AC3: three identical states report 1 of 3.
- AC4: force `contract_version` to `v2` and the parser refuses on `contract_version`.
- AC5: strip the status and it reports 3 of 3 defective. With identical or distinct digests the defective count
  stays 0 while the refused pairs change (3 vs 0).
- AC6: the census looks for the definition line with an anchored pattern and has a positive control on the
  imported module.
- AC7: the same map rendered twice is identical, and with the status stripped the three collapse to 1 of 3.

## Rows

- `IRPT_FNTEND-W2-S20`, BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO`: the AC5/AC8 contradiction. It is resolved by
  the widening at `bf95fb7b9a` and the re-point at `f95fa1db`. The row is not edited; its disposition is the CVO's.
- `IRPT_FNTEND-W2-S21`, OBSERVATION, ARMED, disarm_owner `3.0.0_SA_CVO`: only READY mounts the Holdings body.
- `IRPT_FNTEND-W2-S22`, OBSERVATION, INERT: the first widened bound split FE-s-22's exact-vs-suffix control
  across two maps. It is resolved by the issuer's correction at `49f4026218` and the pair re-point at `346d2b90`.
  The row is not edited; its disposition is the CVO's.

## What the set still reads, so nobody reads this wider than it is

Run through FE-s-22's rule, the round-2 set is **still refused**, and that is correct: `refused-pairs=3, defective=0`
on the live maps. The reason has changed from *defective fixture* to *the three PNGs are byte-identical*. Clearing
that means re-capturing, which is FE-s-18's job. FE-s-18 stays as it was; this cell took no capture and did not enter
`__tests__/fe-s-18/`.
