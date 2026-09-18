# RESULT -- DSGN_REBRND.TO-RB-s-8 (the archetype rewrites), worker `0.9.0_WK_DSGN_REBRND~2`

**Delivered.** The standing colour law is rewritten IN PLACE onto the light-canvas contract
`portal/DESIGN.md`, and every file says in dated terms that **Andrew's 2026-09-11 ruling supersedes
the 2026-07-15 archetype**. No second archetype document was created: RB8-AC4 reads 1 before and 1
after.
- Workspace commit `8cda2454ab` (branch `wk-dsgn_rebrnd-2c`, LOCAL) carries `design/brand/COLOR_ARCHETYPES.md`,
  `design/systems/portal/DESIGN_SYSTEM.md`, `design/process/UI_VERIFICATION.md`,
  `.claude/skills/frontend-dev/SKILL.md` and rows W2-S13..S16.
- Portal commit `b7dff90dfbe3b445be10a17b8eaca629e3473e27` (portal branch `wk-dsgn_rebrnd-2c`,
  LOCAL) carries `portal/CLAUDE.md` ("Color law" and "Verification law") and
  `portal/scripts/ui-smoke.mjs` (label only; the CANVAS print is unchanged).

**Proof:** `DSGN_REBRND.TO-RB-s-8.archetype-rewrites.proof_of_spec.json` in this folder.

## Census first (the order's NOT-EVALUATED files, printed before any edit)

| file | C3CADA | SILVER | CANVAS | FLOATING | carries the archetype? |
|---|---|---|---|---|---|
| design/brand/COLOR_ARCHETYPES.md | 1 | 3 | 6 | 1 | yes, in full (plus the HSL form) |
| design/systems/portal/DESIGN_SYSTEM.md | 4 | 19 | 7 | 9 | yes: the opening callout, the background tables and the decision tree |
| design/process/UI_VERIFICATION.md | 0 | 0 | 0 | 0 | **only by reference** (row W2-S16) |
| portal/CLAUDE.md | 0 | 4 | 5 | 0 | yes, **in HSL/rgb form only** (row W2-S13) |
| .claude/skills/frontend-dev/SKILL.md | 0 | 3 | 6 | 0 | yes; not in the four-file list (row W2-S14) |
| portal/scripts/ui-smoke.mjs | 0 | 1 | 4 | 0 | the canvas label only (row W2-S14) |

Applied state, read before writing: `portal/src/index.css:111` `--bg-page: var(--palette-canvas)`
(`#F4F6FA`). So the running theme already renders the light canvas, and the rewrite brings the
law in line with it. `Panel variant="chart"/"mixed"`, `PanelHeader`, `DarkCard` and `NestedCard`
are still band-valued, and each rewritten file states that as a known divergence (rows W1-S9,
W2-S5), not as law.

## Criteria (verbatim invocations, two runs byte-identical)

| id | verdict line | denominator | status |
|---|---|---|---|
| RB8-AC1 | `VERDICT: SUPERSEDED` | TOTAL 0 over 4 of 4 files (baseline TOTAL 5) | PASS |
| RB8-AC2 | `VERDICT: ALL-STATE-CANVAS` | MISSING 0 of 3 (baseline 3 of 3) | PASS |
| RB8-AC3 | `VERDICT: BOTH` | 2 of 2 elements (baseline clause False) | PASS |
| RB8-AC4 | `VERDICT: SINGLE-ARCHETYPE` | 1 archetype doc, bar exactly 1 | PASS |
| RB8-AC5 | (judgment) | 5 of 5 rewritten files carry a located supersession statement | UNVERIFIABLE-BY-INSTRUMENT -- `3.0.0_SA_CVO` at L9 |

Controls: four mutants, one per criterion, were run on scratch copies of the edited state. All
fired: `ARCHETYPE-SURVIVES`, `INCOMPLETE`, `MISSING-ONE`, `FORKED`. A supplementary census, a
different instrument from AC1, covered the old value in hex, HSL, rgb and "silver ... 81%" forms
and read 0 across the 6 edited files. `ui-smoke.mjs` still prints the canvas: on port 5184 it
printed `CANVAS: rgb(244, 246, 250)` at rc=0.

## The clause-cite step

`design/process/UI_VERIFICATION.md` step 4 and `/frontend-dev` step 4: a review that rejects a
page cites the contract clause NUMBER it violates, beside its evidence. A finding that names no
clause is reported as a contract gap, not a page defect. The render-LOOK-then-commit rule keeps its
name in both files. Worked example: `rb7-ac5-rejection-positioning.md` in this folder.

## Rows filed (all `UNDER_INVESTIGATION`)

| id | class | hazard | one line |
|---|---|---|---|
| DSGN_REBRND-W2-S16 | OBSERVATION | INERT | UI_VERIFICATION.md carried the archetype only by reference; AC1 cannot discriminate on it |
| DSGN_REBRND-W2-S13 | OBSERVATION | INERT | portal/CLAUDE.md carried the silver canvas in HSL/rgb only; AC1's hex count is blind to that form |
| DSGN_REBRND-W2-S14 | OBSERVATION | INERT | the skill and the ui-smoke label also carried the silver law; both are in `<paths>` and were rewritten |
| DSGN_REBRND-W2-S15 | OBSERVATION | ARMED (`2.0.0_SA_COO~D`) | three portal/src carriers outside the grant still state the silver law as current |

## Owed by others

- **L9:** `3.0.0_SA_CVO` grades RB8-AC5.
- **Integrator:** the `portal` gitlink bump at the drain.
- **Row W2-S15:** `2.0.0_SA_COO~D` decides who rewrites the three `portal/src` comments.
