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

## 7. Vintage (R7R14-AC3) -- structurally cross-cell, see row LGIC_ENFORCE-W1-S105

`r14-vintage-field` grades BOTH `EN-r-7` and `EN-p-38` together. This worker's own block is clean (2 of 2
fixed inputs named at pin `a2e031e4c772737c29e328420dae9f1a17c6d2df`, both resolvable). `EN-p-38`'s
record lives in a sibling worker's own worktree (`0.9.0_WK_LGIC_ENFORCE~2`), which this order forbids
coordinating with and which is not on this branch, so the shared arm reads FAIL from here. Filed as
`LGIC_ENFORCE-W1-S105` (BLOCKING, INERT, UNDER_INVESTIGATION) rather than hidden or worked around.

## 8. Stale proofs (R7R14-AC4)

1 fixed-input commit since the cut pin `c05f9f9fc9`: `a2e031e4c7`, the L6 issuance that minted
`fixed_inputs/r14/` itself. No round-14 proof existed before that commit (measured: `git ls-tree -r
a2e031e4c7^ -- org/missions/D14/LGIC/LGIC_ENFORCE` carries no `-r14.` proof_of_spec path), so the honest
set of proofs at risk is empty for both cells and `stale_proofs.proofs_re_run` is `[]`.

## 9. Criteria table

| id | verdict | invocation | denominator |
|---|---|---|---|
| R7R14-AC1 | PASS-R7-ONE-PATH | `check_en_r14.py r7-one-path` | 6 of 6 columns routed, 1 distinct rule, witness identical in 2 columns |
| R7R14-AC2 | PASS-R7-NO-PRODUCER-CHANGE | `check_en_r14.py r7-no-producer-change` | 0 commits by this cell to `lib/opal_naming.py`, 0 elsewhere in window |
| R7R14-AC3 | FAIL-R14-VINTAGE-FIELD | `check_en_r14.py r14-vintage-field` | EN-r-7 clean (2/2 named, resolvable); EN-p-38 0/2 named -- cross-worktree, see LGIC_ENFORCE-W1-S105 |
| R7R14-AC4 | PASS-R14-STALE-PROOFS | `check_en_r14.py r14-stale-proofs` | 1 commit since cut (the mint), 0 proofs at risk, 0 enumerated, both cells |
| R7R14-AC5 | UNVERIFIABLE-BY-INSTRUMENT | judgment, CVO at L9 | N/A |

## 10. What is not claimed

This record does not claim R7R14-AC3 is met -- it is not, from this worktree, and that FAIL is recorded
verbatim rather than argued around. It claims only that EN-r-7's own half of that shared arm is correct
and complete, and that the remaining gap is structural (drain-dependent), not a defect in this cell's
work. Whether EN-p-38's own record will make the shared arm PASS once merged is that cell's own question,
never read or acted on here per the order's BOUNDS.
