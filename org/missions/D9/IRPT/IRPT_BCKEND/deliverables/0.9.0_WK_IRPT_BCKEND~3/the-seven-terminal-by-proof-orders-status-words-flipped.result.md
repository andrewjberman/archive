# IRPT_BCKEND.TO-IB-rth-3 -- result

**Cell:** the seven terminal-by-proof orders' status words, dispositioned per CTO ruling 98990/98993
(the per-order honest-word rule -- no uniform terminal value).

## What was measured

Ran the gate's own resolver (`.tools/surprise-row-gate.py::_open_tos_for_project`) for `IRPT_BCKEND`.
It named the same seven orders the task order's premise names: `IB-rt-6`, `IB-rtf-3`, `IB-rtf-4`,
`IB-rtf-7`, `IB-rtf-10`, `IB-rtf-12`, `IB-rtf-14` -- each terminal-by-proof (a VALID proof-of-spec
instance at HEAD) while carrying a non-terminal `<status>` word.

For each, resolved its face + its proof instance, confirmed `proof-of-spec-check.py --governing-order
<face>` reads **VALID (rc=0)**, and read the graded criterion's own `status`/`status_reason`.

## Per-order disposition

| cell | criterion | proof | disposition | reason |
|---|---|---|---|---|
| `IB-rt-6` | `RT6-AC1` | FAIL | **LEFT NON-TERMINAL** | own `status_reason`: "BLOCKED, not unattempted ... the order stays open" (2 checks rest on a premise outside this order's `<paths>`) |
| `IB-rtf-3` | `R60-AC1` | FAIL | **LEFT NON-TERMINAL** | genuine MEASURED FAIL (2 of 4 outcome arms failed on pre-existing world defects, not an authorization defect); no bound admits `complete` on a disclosed FAIL |
| `IB-rtf-4` | `R61-AC1` | FAIL | **LEFT NON-TERMINAL** | genuine MEASURED FAIL (`terraform fmt -check -diff` rc=3, proven pre-existing) |
| `IB-rtf-7` | `R64-AC1` | FAIL | **LEFT NON-TERMINAL** | own `status_reason` states verbatim "IB-rtf-5 stays staged and the order stays open" |
| `IB-rtf-10` | `R67-AC1` | FAIL | **LEFT NON-TERMINAL** | genuine MEASURED FAIL (apply landed as signed, (a)-(e) PASS, 9 of 10 live requests UNEXPECTED at (f)) |
| `IB-rtf-12` | `R69-AC1` | FAIL | **LEFT NON-TERMINAL** | genuine MEASURED FAIL (apply landed as signed, (d)/(e) PASS, 3 of 8 counted requests UNEXPECTED at (f)) |
| `IB-rtf-14` | `R71-AC1` | FAIL | **LEFT NON-TERMINAL** | FAILED at its own expected first-pass outcome: arm (b) STOP (0 of 2 halves at HEAD), (c)/(d) NOT RUN |

**None flipped to `complete`:** no order's own bound expressly permits completion with a disclosed FAIL
(the OG-r-1/R-58 shape -- see `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-r-1...md` for
that shape's own example) -- absent from all seven.

**None flipped to `superseded`:** read the decomp's `supersedes` column across rounds R3-R8
(`org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md`) plus a project-wide text
search for "supersed" against each of the seven ids -- no later round's cell names any of the seven as
its target. Filed as a surprise row (`IRPT_BCKEND-W3-S51`, INERT): the task order's own text asserts
`superseded` is "true for some of the seven, false for others," which this worker's measurement does
not confirm (true for zero, by the evidence read).

## Verification (arm c)

Re-ran the resolver after committing the seven ISSUER-CORRECTION annotations (word unchanged, only a
reason clause appended to each face's own `<status>` field, one line per face): the resolver's
"proven" set is still EXACTLY the same seven cells, matching this table's residual. `battery_ib_rth_3.py`
cross-checks this programmatically and prints `IBR78-STATUS-WORD-AND-PROOF-RESOLVER-AGREE` on match.

**R78-AC1: PASS** -- the residual is exactly the seven faces left NON-TERMINAL, each named with its
reason; no order was flipped to `complete` on a failing proof.

## Deliverables

- `battery_ib_rth_3.py` (the resolver/status-word cross-check)
- `IB-rth-3_R78-AC1_battery_output.txt` (its run, pinned to commit `7a74155d0e`)
- this result file
- `IRPT_BCKEND.TO-IB-rth-3.the-seven-terminal-by-proof-orders-status-words-flipped.proof_of_spec.json`
- the seven face edits (commit `023b4697df`) and the surprise row (commit `7a74155d0e`)
