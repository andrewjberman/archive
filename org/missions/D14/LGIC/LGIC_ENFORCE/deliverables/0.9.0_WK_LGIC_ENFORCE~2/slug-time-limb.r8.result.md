# slug-time-limb.r8.result -- LGIC_ENFORCE.TO-EN-g-37-r8 (EN-g-37), 0.9.0_WK_LGIC_ENFORCE~2

**Built at commit `1fc3d7c8b2` (the limb), record at `a830bcdd77`** (worktree `wk-lgic-enforce-8-2`,
cut from round-8 issuance `fa90229c09`).

## The cell

Add ONE limb to `.tools/surprise-row-gate.py`: refuse a slug (a NEW remediation row commit) when a
GRADUATED item under the project carries no remediation row. `R8_BASE.json` pinned the token's absence
at the cut (0 hits over 2437 lines) -- the negative control for this arm.

## What was built

- `_remediation_ids_for_project(root, code)` -- a STANDALONE census of the item ids a remediation row
  under the project actually carries, read from the index. Kept separate from `_latest_dispositions`
  rather than added as a second return value: `_resolve_latest` already folds remediation-row presence
  into "GRADUATED", but a CVO row can ALSO carry `disposition: GRADUATED` directly at L9 with no
  remediation row ever minted, and the two paths land on the identical string -- only an independent
  read of remediation ids can tell them apart.
- `_graduated_without_row(latest, remediation_ids)` -- the PURE core (the name the acceptance arm
  reads): item ids whose latest disposition is GRADUATED while absent from `remediation_ids`. Returns
  `None` (never an empty list) when either census could not run.
- `_graduated_without_row_violations(...)` -- the wrapper `check_file` calls, wired into the same L10
  precondition block as the two existing route/investigations preconditions, with the identical
  merge-carried exemption (`_row_was_carried`).
- Twelve new arms inside the gate's own `--self-test`: positive, mutant, a non-GRADUATED item is NOT
  flagged, both censuses fail closed to `None`, both merge branches (carried vs minted), and a negative
  control proving this limb never reads the `_stale_open_row` token that is EN-k-38's alone.

## Rowlessness only

The limb grades ONLY whether a GRADUATED item has a remediation row. An OPEN row that exists but has
not moved is untouched -- `_graduated_without_row` never inspects `remediation.state`, `disarm`, or any
staleness signal, and the negative control arm asserts the `_stale_open_row` token appears in neither
new function's source. That is EN-k-38's question, the second order on this slot.

## The two controls, run end-to-end, not just as pure-function calls

`.scratch/g37_e2e_test.py` (worktree-local, never committed) builds an ISOLATED scratch git repo per
run -- never the production channel -- with two GRADUATED investigation items committed at HEAD, then
calls the REAL `check_file(root, rel)` on a STAGED new remediation-row commit:

- **MUTANT**: the staged remediation row covers `TESTPRJ-S1` only; `TESTPRJ-S2` is GRADUATED with no
  row. `check_file()` returned 1 violation naming `TESTPRJ-S2` and citing S74. **REFUSED.**
- **POSITIVE CONTROL**: the same slug, but the staged commit covers BOTH `TESTPRJ-S1` and `TESTPRJ-S2`.
  `check_file()` returned 0 violations. **PASS.**

The two runs differ in exactly one fact (whether S2's row is covered); every other limb `check_file`
also grades (route precondition, investigations precondition, coordinate discipline, duplicate-id
census, schema validation) ran alongside and produced no violation in either run, so the one observed
difference is attributable to the new limb alone.

## Acceptance

| id | invocation | expect | result |
|---|---|---|---|
| G37R8-AC1 | `check_en_r8.py g37-limb-present` | `PASS-G37-LIMB-PRESENT` | PASS -- `_graduated_without_row` occurs 19 times over 2570 gate lines |
| G37R8-AC2 | `check_en_r8.py g37-controls` | `PASS-G37-CONTROLS` | PASS -- positive control PASS, mutant REFUSED, distinct inputs |
| G37R8-AC3 | `check_en_r8.py g37-gate-unmoved` | `PASS-G37-GATE-UNMOVED` | PASS -- gate self-test rc=0 (156 of 156 arms) |
| G37R8-AC4 | judgment (3.0.0_SA_CVO at L9) | N/A | `UNVERIFIABLE-BY-INSTRUMENT`; evidence recorded below |

`selftest-arms` on `check_en_r8.py`: 31 of 31 arms, 13 of 13 positive-satisfiability, 0 failures --
`VERDICT: PASS-SELFTEST-31-ARMS-13-POSITIVE`. Gate's own `--self-test`: 156 of 156 arms pass, rc=0,
including the 12 new EN-g-37 arms and the unchanged live NFRA_COMPEFFICACY census (51 items, 0
undispositioned, 1 known duplicate-id collision) -- no existing limb's behaviour moved.

## Proof

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/LGIC_ENFORCE.TO-EN-g-37-r8.slug-time-limb.proof_of_spec.json`
-- `python .tools/proof-of-spec-check.py <instance> G37R8-AC1,G37R8-AC2,G37R8-AC3,G37R8-AC4 --governing-order
org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-g-37-r8.slug-time-limb.md`.

## Surprises

None filed. The tree matched the order's premises, `<paths>` covered every file touched, and no
capability was missing.
