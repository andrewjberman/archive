# EN-r-7 round 14 -- the result record

## 1. What changed

`render_population_table_r14.py` (this deliverable, line 33) defines ONE renderer:

```python
def render_cell(value):
    s = "" if value is None else str(value)
    return s.replace("{", "(").replace("}", ")")
```

`build_table_bytes()` routes every column of every row -- `current`, `canonical`, `verdict`, `type`,
`plane`, `where` -- through `render_cell` and nothing else, then rewrites
`PLACEHOLDER_POPULATION_TABLE_R13.md` in place from `NAMING_CENSUS_REPORT.r13.md`'s fenced json `rows`
list (3264 rows, the table's row denominator, unchanged). The rule chosen is escape-everywhere: before
this repair only `current`/`where` escaped `{`/`}` to `(`/`)`; `canonical` did not (S101). After it, all
six columns share the identical rule, so no column is singled out by carrying real brace bytes any more.

## 2. One path, one rule, denominator and subtraction (R7R14-AC1)

| | value |
|---|---|
| one render path | `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/render_population_table_r14.py:33` |
| columns in the table (denominator) | 6: `current`, `canonical`, `verdict`, `type`, `plane`, `where` |
| columns routed through the one path | 6 |
| NOT routed (denominator MINUS routed) | 0 |
| distinct rendering rules across the columns | 1: `escape { } to ( ) via render_cell` |
| witness | token `{snap}` renders as `(snap)` in both `current` and `canonical` (the same 7 rows carry it in both columns, e.g. `bronze/positions/{snap}.parquet` / `{source}/{scope}/bronze/positions/{snap}.parquet`) |

## 3. Population discriminator

The r13 preamble's own discriminator ("the `canonical` cell is the ONLY column left with real `{` `}`
bytes") is retired, because after this repair no column carries real brace bytes. R-38's population is
now read from `NAMING_CENSUS_REPORT.r13.md`'s fenced json `rows` list -- the RAW `canonical` field, before
rendering -- directly, never from which column's RENDERED table bytes still carry `{`.

## 4. Before / after (disclosure, not a bar -- AC1 does not grade these against each other)

Counted as ROWS carrying at least one occurrence of the token shape, over the same 3264-row denominator,
before (the pinned r13 artifact, byte-identical to `c05f9f9fc9`) and after (this round's regenerated
table):

| | canonical_braces | canonical_parens | current_braces | current_parens |
|---|---|---|---|---|
| before | 1303 | 0 | 0 | 15 |
| after | 0 | 1303 | 0 | 15 |

`current`'s counts are unchanged (it already escaped braces before this round); `canonical`'s flip from
1303 rows of real `{...}` to 1303 rows of `(...)` is the repair. (1303 rows carry 1449 token *occurrences*
in `canonical` since some rows carry more than one placeholder -- that overlap is EN-p-38's subject, not
graded here, and this record's grain field is intentionally absent per the order's BOUNDS.)

## 5. Third-column argument

A new column is added by appending its name to `COLUMNS` and reading its raw value into the same
row-build loop in `build_table_bytes()` -- every cell, old or new, already passes through `render_cell`
before it reaches the line. There is no second escaping branch to add or remember, so the new column's
braces render as parens the first time it is written.

## 6. Producer untouched (R7R14-AC2)

`lib/opal_naming.py` -- 0 commits by this cell since the cut, 0 elsewhere in the window (S101 already
resolved at the source that the producer is correct at the values). This cell changes rendering only.

## 7. Vintage (R7R14-AC3) -- RE-GRADED PASS, see row LGIC_ENFORCE-S106

ORIGINALLY: `r14-vintage-field` AND-combined a hard-coded pair of `EN-r-7` and `EN-p-38` records; this
worker's own block was clean (2 of 2 fixed inputs named at pin `a2e031e4c772737c29e328420dae9f1a17c6d2df`,
both resolvable) but `EN-p-38`'s record lived only in a sibling worker's own worktree
(`0.9.0_WK_LGIC_ENFORCE~2`), which this order forbids coordinating with and which was not on that branch,
so the shared arm read FAIL. Filed as `LGIC_ENFORCE-W1-S105` (BLOCKING, INERT, UNDER_INVESTIGATION)
rather than hidden or worked around.

RE-GRADE (2026-09-19, worktree `wk-lgic-enforce-14-1b`, base `3948ba37d9`, carrying the drain `dda2125b35`
that merged both `wk-lgic-enforce-14-1` and `wk-lgic-enforce-14-2`, plus the issuer's repair `acdba45160`
/ `LGIC_ENFORCE-S106`): the arm now grades the records PRESENT IN ITS CHECKOUT (2 found: `EN-r-7`,
`EN-p-38`) rather than a hard-coded pair, and refuses an empty population rather than passing vacuously.
Both records are present and clean on this branch, so `VERDICT: PASS-R14-VINTAGE-FIELD`. This cell's own
artifact (`render_population_table_r14.py`, `PLACEHOLDER_POPULATION_TABLE_R13.md`,
`ONE_RENDER_PATH_R14.json`) is byte-identical to commit `37865221aa` (`git diff 37865221aa -- <those
paths>` returns 0 lines) -- the FAIL-to-PASS transition is entirely the issuer's checker repair and the
drain landing the sibling cell's record, not a change to this cell's work.

## 8. Stale proofs (R7R14-AC4)

ORIGINALLY: 1 fixed-input commit since the cut pin `c05f9f9fc9`: `a2e031e4c7`, the L6 issuance that
minted `fixed_inputs/r14/` itself. No round-14 proof existed before that commit, so the honest set of
proofs at risk was empty for both cells and `stale_proofs.proofs_re_run` was `[]`.

RE-GRADE: 2 fixed-input commits since the cut pin now (`a2e031e4c7` the mint, plus `acdba45160` the S106
repair to `check_en_r14.py` itself). Still 0 proofs at risk for either cell -- no round-14 proof existed
before either commit -- so `stale_proofs.proofs_re_run` remains `[]` and no re-run was required.

## 9. Criteria table

| id | verdict | invocation | denominator |
|---|---|---|---|
| R7R14-AC1 | PASS-R7-ONE-PATH | `check_en_r14.py r7-one-path` | 6 of 6 columns routed, 1 distinct rule, witness identical in 2 columns |
| R7R14-AC2 | PASS-R7-NO-PRODUCER-CHANGE | `check_en_r14.py r7-no-producer-change` | 0 commits by this cell to `lib/opal_naming.py`, 0 elsewhere in window |
| R7R14-AC3 | PASS-R14-VINTAGE-FIELD (was FAIL, re-graded post-S106) | `check_en_r14.py r14-vintage-field` | 2 of 2 records present in this checkout graded (EN-r-7, EN-p-38), 2/2 fixed inputs named+resolvable each |
| R7R14-AC4 | PASS-R14-STALE-PROOFS | `check_en_r14.py r14-stale-proofs` | 2 commits since cut (mint + S106 repair), 0 proofs at risk, 0 enumerated, both cells |
| R7R14-AC5 | UNVERIFIABLE-BY-INSTRUMENT | judgment, CVO at L9 | N/A |

## 10. What is not claimed

All four mechanical criteria now PASS on this branch. This record does not claim R7R14-AC5 is met -- that
is a judgment call reserved for `3.0.0_SA_CVO` at L9, unchanged by this re-grade. It also does not claim
this worker repaired the checker or regenerated the table a second time: `LGIC_ENFORCE-S106` is the
issuer's (`2.0.0_SA_COO~G`'s) own repair, and this cell's artifact was never touched or reproduced --
verified byte-identical to `37865221aa` above.

## 11. Re-grade note (2026-09-19)

This is a SHORT RE-GRADE of an already-drained cell, not new work. The original FAIL on R7R14-AC3 was
correctly recorded rather than worked around (section 7, original text preserved above); the defect was
the issuer's shared-arm design (filed both as `LGIC_ENFORCE-W1-S105` by this worker and independently as
`LGIC_ENFORCE-S106`), and its repair at `acdba45160` is what turns AC3's verdict, not any change here.
`selftest-arms` was re-run first (`VERDICT: PASS-ARMS-DISCRIMINATE`, 33 arms, 9 positive-satisfiability)
before touching the proof instance, per the re-grade order's controls-first instruction.
