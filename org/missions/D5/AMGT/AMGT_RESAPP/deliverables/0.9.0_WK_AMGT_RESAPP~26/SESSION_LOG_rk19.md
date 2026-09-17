# SESSION LOG -- AMGT-rk-19 (producer half), 0.9.0_WK_AMGT_RESAPP~26

## Bar check
`git rev-parse --abbrev-ref HEAD` -> `wk-amgt-13-26-fpA`. `org/`, `.tools/`, `lib/research/filings/analyze.py`,
the deliverables dir, the surprise-channel investigation file and the task-order file all present. No BLOCKING row.

## What was built

`lib/research/filings/analyze.py` gained, ahead of `resolve_driver`:
- `_WHOLE_NUMBER_RE`, `_numeric_value`, `_find_value_span` -- whole-number matching with thousands
  separators normalised, comparing PARSED VALUE not first-match, so a block's own period label (itself a
  number) never satisfies a different target value.
- `locate_period_labels(periods, excerpt)` -- first-occurrence-anywhere location. This is the function AC1
  supplies its own `period_labels` around and AC2's `reverify_thesis_driver` calls directly; left UNCHANGED
  in contract so both criteria's literal invocations pass exactly as written.
- `_period_blocks(period_labels, text_len)` -- period label -> (start, end) block, TEXT-POSITION ordered,
  end at the next label or the excerpt's end (ADDENDUM 2 A2.3: a wrapped row stays inside its block).
- `verify_points_against_excerpt(points, excerpt, period_labels)` -- the re-keyed gate: AC1's literal
  function.
- `reverify_thesis_driver(points, excerpt)` -- AC2's literal function: locates via `locate_period_labels`,
  verifies via `verify_points_against_excerpt`.
- `_STANDALONE_LINE_TEMPLATE` / `_locate_period_labels_near_anchor(periods, excerpt, anchor)` -- a
  PRODUCTION-GRADE locator used ONLY by `_apply_point_verification` (never by AC1/AC2's functions): a full
  10-K excerpt mentions a year hundreds of times in prose (measured: "2025" occurs 156 times, "2024" 131
  times, "2023" 61 times, in BA's real excerpt), so first-occurrence-anywhere lands inside PROSE, not the
  table. This prefers
  a period token standing ALONE on its own line, and among repeats (BA's excerpt carries the SAME
  three-year table pattern twice, for two different metrics), picks the occurrence closest to the driver's
  own citation anchor.
- `_apply_point_verification(points, excerpt_text, passage_map, anchor=0)` -- shared by a fresh run
  (`resolve_driver`) and the one-time stored-object fix (`reverify_stored_thesis_driver`): verifies, then
  mints the ONE new TABLE passage a verified point's block needs ONLY when no existing passage already
  covers it (idempotent against an already-corrected object), ids continuing the same `P%04d` sequence.
- `resolve_driver` now calls `_apply_point_verification` on the normalised points before returning, adding
  `held_uncited` to the driver dict (distinct from the analysis-level `held_uncited` used for items) and
  `span`/`passage_id` on every kept point.
- `reverify_stored_thesis_driver(security_key, accession, client=None)` -- ADDENDUM 2 item 4, the one-time
  correction: fetches the stored source+analysis pair, re-derives the raw point set from BOTH the object's
  current `points` and `held_uncited` (never compounding an earlier, possibly wrong, split), reverifies, and
  rewrites the analysis object at its own pool key via `crosswalk.write_pool`.
- `main()` gained `--reverify-stored ACCESSION`, a CLI entry to the above, bypassing the normal analyze flow.

## A genuine defect caught and fixed in-session (not by the task order's own text)

The FIRST `--reverify-stored` run (before `_locate_period_labels_near_anchor` existed, using the plain
`locate_period_labels`'s first-occurrence-anywhere against BA's REAL 138K-char excerpt) mis-fired: "2025" and
"2024" occur dozens of times in ordinary prose before the actual delivery table, so the naive locator anchored
on the WRONG (much earlier) position and the resulting blocks did not contain the real numbers. That run wrote
BA's analysis.json to a WRONG state (points 1 [2023 only], held_uncited 2 [2025, 2024] -- read back and
confirmed). This was caught by re-reading the live object immediately after the write and finding a result
inconsistent with the toy AC1/AC2 examples' correctness. The fix (`_locate_period_labels_near_anchor`,
standalone-line + anchor-nearest) was added, verified against the real excerpt directly (labels/blocks printed,
matching the real table's known offsets), and the stored object was corrected again. AC1 and AC2's own
functions/contracts are UNCHANGED by this fix (they were correct throughout, on their own toy inputs); only
the production path (`_apply_point_verification`, used by `resolve_driver` and `reverify_stored_thesis_driver`)
needed the smarter locator.

## Surprise filed

`AMGT_RESAPP-Z-W26-S5`: at read time, BEFORE any edit or write by this worker, BA's live pool object was
ALREADY in the corrected state this order's fix targets (3 points with span+passage_id, held_uncited empty,
282-entry passage_map), contradicting the order's own section-1 MEASURED STATE (276 passages, unverified). A
fresh recompute of `build_passage_map` under the CURRENT (unmodified by this order) `passages.py` returns 276,
matching the order's figure and confirming the extra 6 entries predate this order. Cross-referenced against the
channel's own prior rows `AMGT_RESAPP-Z-S150`/`AMGT_RESAPP-Z-S151` (CVO/CTO, same morning), which already
establish the identical correction ahead of any round-13 order existing. Also recorded: this worker's own
first (broken) write was found REVERTED to the correct state on a later read, without this worker writing in
between -- flagged as a possible concurrent writer to the same pool key, not investigated further per channel
discipline (append and keep working).

## Controls

**Mutant** (the naive-vs-anchored locator, both actually run against the SAME real production data): the
DEFECTIVE path (`locate_period_labels` alone, first-occurrence-anywhere) produced the WRONG, spec-violating
result (2 of 3 real points wrongly held); the FIXED path (`_locate_period_labels_near_anchor`) produces the
CORRECT result (0 of 3 wrongly held) on the identical excerpt. FIRED-AS-EXPECTED.

**Determinism**: the AC3 read-back invocation was run twice, ~1 minute apart, after the corrected write;
both reads returned identical points_count=3, held_count=0. STABLE.

## Commit

`lib/research/filings/analyze.py`, this deliverables folder, the surprise-channel investigation row, and the
task-order file's `<status>` flip, committed together with `.tools/safe-commit.sh --only -- <paths>`.
