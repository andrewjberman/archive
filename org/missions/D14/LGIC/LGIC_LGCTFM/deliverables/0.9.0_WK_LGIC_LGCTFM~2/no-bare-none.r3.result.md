# LT-r-2 round 3 -- no bare "(none)": every column states its coverage

Worker `0.9.0_WK_LGIC_LGCTFM~2`, order `LGIC_LGCTFM.TO-LT-r-2-r3`, branch `wk-lgic-lgctfm-3-2`.
Code change: `lib/lgctfm_render.py` @ `d701235a50` (`_coverage_lines()` added; `_columns_block()` takes the
contract's `coverage` block; both `render_current` and `render_desired` pass it). Nothing under
`workflows/legacy_transform/` was written (R-43); every render below went to the worktree's `.scratch/`.

## The line format chosen

Every column section opens with ONE coverage line, then its rows:

- contract WITH a `coverage` block (LT-e-5 shape, carried in R3_BASE.json):
  `  coverage: <R> row(s) of <I> involved node(s)[ -- short by <I-R>, named below]`
  followed by
  `  coverage by node_type (rows/involved): <NT> <r>/<i>; ...`
  `  instrument: <instrument> | legs <legs> | vintage <vintage>`
  `  not covered: [<NT>] <name> -- <reason>`   (one per not_covered entry)
  R and I are the sums of `rows` / `involved` over the by_node_type entries that `NODE_TYPE_COLUMN` assigns
  to that column (a node_type not in the map is not summed -- the same rule the checker's `column_sums` uses).
- contract WITHOUT a block (every run before round 3), on EVERY column, empty or not:
  `  coverage: NOT MEASURED -- this contract carries no coverage block, so the rows below are what the walk rowed, not what the subject has; an empty or short <COL> column is the instrument's limit, not proof the subject has none`
- an empty column, either form, ends with
  `  no rows rendered in <COL> -- read the coverage line above before reading this as 'the subject has no <col>'`
  in place of the old `  (none)`.

## The graded run's COMPUTE section (run 20260918T011619Z-8db9eb1), rendered into scratch

Before (renderer at `6018f62ed3`):

```
   -- COMPUTE --
  (none)
```

After (renderer at `d701235a50`):

```
   -- COMPUTE --
  coverage: NOT MEASURED -- this contract carries no coverage block, so the rows below are what the walk rowed, not what the subject has; an empty or short COMPUTE column is the instrument's limit, not proof the subject has none
  no rows rendered in COMPUTE -- read the coverage line above before reading this as 'the subject has no compute'
```

Illustration only (NOT graded, NOT a claim about the live plane): the same graded contract with a DEMO
coverage block marking the R3_BASE cut-floor's 9 Lambdas and 1 EC2 instance as involved and not covered
renders COMPUTE as `coverage: 0 row(s) of 10 involved node(s) -- short by 10, named below`, then
`coverage by node_type (rows/involved): EC2_INSTANCE 0/1; LAMBDA 0/9`, the instrument line, and ten
`not covered:` lines naming each node.

## Bare "(none)" census, every run under workflows/legacy_transform/

5 of 5 contract.json files rendered (10 flow files), stripped-line equality with `(none)`:
before 10, after 0.

## Criteria (run after the commit, from the worktree)

| id | invocation | deciding output | at the cut |
|---|---|---|---|
| R2R3-AC1 | `timeout 900 python <C> r2-no-bare-none` | `contracts rendered: 5 of 5` / `bare '(none)' lines: 0` / `graded run: columns lacking a NOT MEASURED line: [] (of 4)` / `VERDICT: PASS-R2-NO-BARE-NONE` rc 0 | FAIL (10 lines; 4 of 4 columns lacking) |
| R2R3-AC2 | `timeout 900 python <C> r2-coverage-lines` | `every column prints its sum` / `bare '(none)' lines: 0` / `VERDICT: PASS-R2-COVERAGE-LINES` rc 0 | FAIL (all 4 columns missing their sums) |
| R2R3-AC3 | `timeout 900 python <C> r2-regen` | `deterministic (two renders byte-identical): True` / `one row removed -> picture changes: True` / `VERDICT: PASS-R2-REGEN` rc 0 | PASS (guard-shaped, disclosed) |
| R2R3-AC4 | judgment | recorded for `3.0.0_SA_CVO` at L9, no verdict here | -- |

`selftest-arms` run first, before the change and again after it: 27 of 27 arms PASS,
`VERDICT: PASS-ARMS-DISCRIMINATE`, rc 0 both times. No arm was unsatisfiable by a correct renderer, so no
blocking row was owed.

## Surprises

None filed. Observed and judged not a surprise: the committed `flow.current.md` in the graded run differs
from a render by the pre-change renderer at line 1 byte 54 -- the end of the first line, i.e. the CRLF this
`core.autocrlf` checkout renders; the order's own premise (the COMPUTE text) matched exactly.
