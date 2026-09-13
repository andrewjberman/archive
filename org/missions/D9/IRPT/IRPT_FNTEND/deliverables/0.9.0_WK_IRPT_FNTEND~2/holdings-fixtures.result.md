# TO-FE-s-26 -- holdings fixtures: result

Worker `0.9.0_WK_IRPT_FNTEND~2`, branch `wk-irpt_fntend-4-2-fe-s-26` (workspace and portal), portal commit
`ed90ce2d` (LOCAL, never pushed; PORTAL IS FROZEN). Workspace base `f3b42b1e0b`, portal base `237a9027`.

**The order is NOT complete, and `<status>` stays open.** F26-AC1 through F26-AC7 pass by output. **F26-AC8 FAILS**
by output: `26 pass / 2 fail`. Both failures are inside `__tests__/fe-s-22/capture-hash.test.ts`, whose F22-AC4 tests
assert the maps' defective state as fact, and that file is not in this order's `<paths>`. Filed as
`IRPT_FNTEND-W2-S20` (BLOCKING).

## What changed

One `status` member added to the **holdings envelope** of each of the three maps, and nothing else. Diffstat on the
three maps is 16/0, 22/0 and 22/0 (insertions/deletions). Each file was then re-parsed and compared with its original
after deleting the new member: equal in all three. The portal commit's other 5 paths are new files under
`__tests__/fe-s-26/`.

All three members are legal v1 `StatusEnvelope`s (`docs/contracts/investor-reporting/v1/StatusEnvelope.schema.json`).
Each carries all six required members. `business_date` is present because all three states are answer-bearing, where
the schema's `allOf` requires it. The three `source_dates` values come from each document's own fields, not from a
clock: `clocks.business_date` 2026-09-09, `source_set_revision[0].completion_date` 2026-09-09, and
`clocks.as_of_timestamp` 2026-09-10T02:15:00Z.

## The state given to each map, and why it is legitimate for that basis

This comes first because it is what F26-AC9 grades. Before choosing, I measured how the three maps actually differ,
using FE-s-22's own field walk:

- **observed vs target** differ at exactly **1** path: `nodes[].basis`.
- **observed vs missing-attribution** differ at **8** paths, all under `nodes[].classification`.
- Everything else is **identical in all three**: clocks, coverage (11 of 12 nodes resolved, a 4,200 USD remainder),
  custody totals, the source-set revision, and every node's provenance.

So a state based on any shared field would come out the same in all three maps and could not differ. Each state
below is argued from the one field that does differ. The contract never ties a state to a basis: `StatusEnvelope.state`
describes how complete the ANSWER is, and the `HoldingsSnapshot` contract section says nothing about state per basis.
The per-basis reasoning is therefore mine, written out here so the grader can reject it.

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
records what it costs FE-s-18.

## Criteria, as run at portal `ed90ce2d`

| id | invocation (from `<WS>/portal`) | deciding output | verdict |
|---|---|---|---|
| F26-AC1 | `timeout 180 bun run typecheck; echo rc=$?` | `$ tsc -b --noEmit` / `rc=0` | PASS |
| F26-AC2 | `timeout 120 bun test .../fe-s-26/fixtures-carry-status.test.ts` | `HOLDINGS MAPS CARRYING status: 3 of 3` | PASS |
| F26-AC3 | same file | `STATES DISTINCT ACROSS THE THREE: 3 of 3` | PASS |
| F26-AC4 | same file | `ENVELOPES STILL VALID: 27 of 27` | PASS |
| F26-AC5 | `timeout 120 bun test .../fe-s-26/not-defective.test.ts` | `DEFECTIVE FIXTURES: 0 of 3` | PASS |
| F26-AC6 | same file | `RULE IS IMPORTED, NOT COPIED: 1 module` | PASS |
| F26-AC7 | `timeout 120 bun test .../fe-s-26/renders-differently.test.ts` | `PANELS DISTINCT: 3 of 3` | PASS |
| F26-AC8 | `timeout 120 bun test .../fe-s-26 .../fe-s-22` | `26 pass` / `2 fail`, rc=1 | **FAIL** |
| F26-AC9 | judgment | recorded above; no verdict | RECORDED |

**Controls, each run and each firing:**
- AC2: delete one status in memory and it reports 2 of 3.
- AC4: force `contract_version` to `v2` and the parser refuses on `contract_version`.
- AC5: strip the status back out and it reports `DEFECTIVE FIXTURES: 3 of 3`. With identical digests or with distinct
  digests the defective count stays 0, while the number of refused pairs changes (3 vs 0). So the verdict is read from
  the defective-fixture check, not the collision check.
- AC6: the census looks for the definition line with an anchored pattern. An unanchored first version counted the
  test file's own search string as a copy; that was caught on the first run and fixed before commit.
- AC7: the same map rendered twice is identical, and with the status stripped the three collapse to `1 of 3`, which
  reproduces the defect.

## What the set still reads, so nobody reads this wider than it is

Run through FE-s-22's rule, the round-2 set is **still refused**, and that is correct: `refused-pairs=3, defective=0,
distinct digests=1 of 3`. The reason has changed from *defective fixture* to *the three PNGs are byte-identical*.
Clearing that means re-capturing, which is FE-s-18's job. FE-s-18 stays as it was; this cell took no capture and did
not enter `__tests__/fe-s-18/`.
