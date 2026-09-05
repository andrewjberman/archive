# EG-s-5 result -- the report states how complete it is, on its own face

**TO:** `ETFS_GUARDRAIL.TO-EG-s-5` | **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~2` | **Source (edited):**
`data/etfs/scripts/presentation/render_month_end.py` (now 874 lines -- 778 at the TO's cut, +57
already present at HEAD from EG-s-13's merged Orion-alignment cell, an unrelated sibling order in
this same round (778+57=835 at this order's own start, confirmed by `wc -l` before any edit);
this order's own edit added +39 lines net, 835 -> 874). **Read-only:** `data/etfs/scripts/coverage/`
(EG-s-4's classifier, imported, never edited or re-implemented).

---

## 1. Where the line renders (line numbers, at HEAD after this order's edit)

- **Import wiring** (`from coverage import classifier`, `data/etfs/scripts` put on `sys.path`
  resolved relative to `__file__`, same pattern as the existing Orion import beside it):
  `render_month_end.py:81-88`.
- **Computed** inside `render_month`, right after `present` (etfs-only reads, `series=daily[p]`
  reuses the already-loaded keys, no probe, no second bucket listing, computed on every path
  through the function): `render_month_end.py:409-417`.
- **Passed through** to `_html` as a new trailing `coverage` argument (default `None`, so no other
  caller of `_html` breaks): `render_month_end.py:550` (the call site), `:555-557` (the signature).
- **Rendered** in `_html`: a `coverage_lines` block built at `:589-593`, one `<div class="note">`
  per present partner (`<b>{Display} coverage:</b> {line}`, plain text, no chart, reusing the
  existing `.note` CSS class -- no new style), inserted directly beneath the SUMMARY table in
  slide 2 (`s2`) at `:688-691` (the choice named in the deliverable: a COVERAGE block under the
  summary table, not one line per table row, since the summary table's `<tr>` structure is
  otherwise untouched).
- **CSV comment row**, LAST row of each firm's file in `write_month_csvs`: computed at `:752-753`,
  written at `:754` (`w.writerow(["# coverage: <line>"])`, one cell, after the numeric ETF rows,
  which are unchanged in count and values).

---

## 2. Acceptance criteria, verbatim with rc and denominator

### S5-AC1 -- the four-arm battery is green

**Invocation:** `python -m pytest data/etfs/scripts/presentation/tests/test_coverage_line.py -q`
```
....                                                                     [100%]
4 passed in 1.25s
```
rc=0. Denominator: 4 of 4 arms passed (a, b, c, d). **PASS.**

Sanity check (not itself a criterion): the sibling `test_orion_alignment.py` (EG-s-13's battery,
same module) still passes unmodified after this edit -- `5 passed in 1.31s`, rc=0. Confirms the
classifier's `series=` code path never triggers an AWS call even when the caller does not
monkeypatch anything coverage-related.

### S5-AC2 -- the LIVE render of August 2026 still completes

**Invocation:** `python data/etfs/scripts/presentation/render_month_end.py --month 2026-08 --out .scratch/eg_s5_aug.html`
```
OK: 2026-08 -> .scratch/eg_s5_aug.html
OK: CSV -> .../.scratch/opaletfs_49financial_202608.csv
OK: CSV -> .../.scratch/opaletfs_inflection_202608.csv
OK: CSV -> .../.scratch/opaletfs_cottonwood_202608.csv
```
rc=0. Denominator: 1 of 1 render, 3 of 3 CSVs (main() also calls `write_month_csvs` as a side
effect of this invocation). etfs-only reads; no PDF, no S3 upload attempted. **PASS.**

### S5-AC3 -- one coverage line per present partner

**Invocation:** `python -c "h=open('.scratch/eg_s5_aug.html',encoding='utf-8').read(); print('COVERAGE_LINES=%d' % h.count('trading days;'))"`
```
COVERAGE_LINES=3
```
Denominator: 3 of 3 present partners (49 Financial, Cottonwood, Inflection all have August data).
**PASS.**

The three live lines (all 21/21 -- August 2026 is fully backfilled per the project's own prior
finding, PRD s.4 property 3):
```
49 Financial -> 21/21 trading days; 0 carried for missing data
Cottonwood   -> 21/21 trading days; 0 carried for missing data
Inflection   -> 21/21 trading days; 0 carried for missing data
```
And the matching CSV last rows (all three files, live-generated):
```
# coverage: 21/21 trading days; 0 carried for missing data
```

### S5-AC4 -- the commit gate is clean

```
All checks passed!
OK: no unguarded strict-utf8 log reads.
OK: pre-commit gate clean for 2 of 2 file(s)
```
rc=0. **PASS.**

### S5-AC5 -- the classifier is imported, never re-implemented

**Invocation:** `python -c "import re; s=open('data/etfs/scripts/presentation/render_month_end.py').read(); print('CLASSIFIER_IMPORTED=%s SECOND_IMPL=%d' % ('from coverage import classifier' in s or 'import classifier' in s, len(re.findall(r'def (?:classify_month|coverage_line)\(', s))))"`
```
CLASSIFIER_IMPORTED=True SECOND_IMPL=0
```
Denominator: 1 of 1 import string found; 0 of 0 re-implementations of `classify_month`/`coverage_line`
defined in the renderer. **PASS.**

### S5-AC6 -- judgment, RECORD; NO VERDICT

A reader of the PDF (HTML pre-PDF-conversion, this order does not touch `--pdf`) or the CSV can
tell, without opening anything else: the HTML carries a plain-text coverage line per partner
directly beneath the SUMMARY table (slide 2); the CSV carries the identical line as its last row.
The line is computed and rendered on **every** path through `render_month` -- it is not gated on
any verdict, any flag, or any conditional branch; `coverage` is computed unconditionally right
after `present` and passed to `_html` unconditionally. This order does not build `EG-s-6`'s REFUSE
branch (out of this cell's scope), but the coverage computation/render sits strictly upstream of
where such a branch would live (inside `render_month`, before the function returns), so a REFUSE
branch built on top of this order's `render_month`/`_html` call would inherit the line
automatically rather than needing to re-wire it -- this is the property `EG-s-6`'s own order will
verify directly. The CSV's numeric grid is unchanged: `write_month_csvs` still emits exactly
`["Date", ...]` then one row per ETF with `_carried_daily`'s values, unmodified; the coverage row
is strictly appended after that loop, never interleaved into it (S5-AC1 arm (d) proves this by
construction: row count == header + 1 ETF row + 1 coverage row, and the DIVZ row's values are
read back unchanged).

---

## 3. Bounds honored

- `data/etfs/scripts/coverage/` (slot 1's) was read only -- `git diff --stat HEAD -- data/etfs/scripts/coverage/`
  is empty (not itself a graded criterion, checked as a bound self-audit).
- No probe, no invoke, no firm bucket: `classify_month(...)` was always called with `probe=None`
  (the default) and `series=daily[p]` / `series=series` supplied directly, so `classifier.py`'s own
  `_load_series` (the only S3-touching path inside the classifier) is never reached -- confirmed by
  the live render completing with the SAME S3 read set the renderer already had (no new
  `list_objects_v2`/`get_object` call added; the classifier only inspects the keys of an
  already-loaded dict).
- No PDF, no `--s3-out`, no upload: `--pdf` and `--s3-out` were never passed to either invocation
  in this order.
- Restates nothing: the coverage line is a NEW, additive line describing the month; no existing
  numeric figure (marquis, summary, chart, delta table, daily matrix, CSV grid) was changed by
  this edit -- confirmed by S5-AC1 arm (d) and by the live CSVs' numeric rows being byte-identical
  in shape to the pre-existing convention (header + N ETF rows), with only the new trailing row
  appended.

## 4. Push state (measured)

See the WORKER REPORT for the value read at report time.
