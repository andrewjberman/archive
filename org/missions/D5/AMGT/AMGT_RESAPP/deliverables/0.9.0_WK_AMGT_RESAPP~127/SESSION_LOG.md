# Session log -- 0.9.0_WK_AMGT_RESAPP~127, AMGT-rk-127 (round 33)

Worktree: `C:/tmp/wk-amgt-33-127`, branch `wk-amgt-33-127`, cut from `cfb24cdf41`.

## What was built (additive, CODE ONLY, no deploy, no S3 write from this cell)

1. **Producer half** (`lib/research/harvest/filings.py`): `state_put_filing_attempt`'s existing
   CHANGED branch (AMGT-rk-105, unchanged) now ALSO calls a new helper,
   `_put_filing_attempt_held_marker(partition, new_doc, differing_field, client)`, which persists
   the NEW outcome as a sibling object at the SAME partition, addressed through `store.address_of`
   with `object_name="UNRESOLVED-SOURCE.HELD.json"` (a new module constant,
   `_FILING_ATTEMPT_HELD_MARKER_OBJECT`). The served object (`UNRESOLVED-SOURCE.json`) is never
   touched; `FilingAttemptChangedError` still raises afterward, unchanged. A new `_now_iso_utc()`
   helper produces the marker's own `retrieved_at` in the same shape `_fetched_at_of` reads back.

2. **Adapter half** (`lib/research/api/scoped_amgt.py`): a new constant
   `FILING_ATTEMPT_HELD_MARKER_OBJECT` (hand-typed, mirroring `FILING_ATTEMPT_STATE_PREFIX`'s own
   pattern -- this adapter's deployed closure never imports `lib.research.harvest.store` or
   `lib.opal_naming`), a new reader `_read_filing_attempt_held_marker` (same `_pool_client()` seam,
   same partition, as `_read_filing_source_object`), and a new helper
   `_apply_filing_attempt_held_state(bundle, security_key)` that mutates a bundle IN PLACE,
   additively: with a marker present it adds `drafting_reason_held=True`,
   `drafting_reason_newer`, `drafting_reason_newer_status`,
   `drafting_reason_newer_filing_identity` under their OWN keys -- `drafting_reason` (the served
   text) is never touched. With no marker, the bundle is left byte-identical. Wired into
   `read_thesis_bundle` right after the existing `drafting_reason = filing_source.get("reason")`
   line (AMGT-rk-24's fence, unchanged).

3. **Tests**: two new arms in `lib/research/harvest/tests/test_filing_attempt_skip_held.py`
   (SKIP-HELD writes no marker; a second CHANGED event overwrites the marker with the latest
   outcome, not the first); two existing arms in that file updated because they measured a
   now-legitimately-different `put_object` count (`test_changed_outcome_still_raises`,
   `test_battery_changed_outcome_is_changed_held_nonzero_exit`); `test_filings.py`'s
   `test_module_writes_only_through_store` updated from `count("put_object") == 1` to `== 2`; a
   new file `lib/research/api/tests/test_filing_attempt_held_marker.py` (6 arms) covering the
   adapter reader and the apply-helper, including the no-marker regression control.

## Baseline (AC1)

`git stash` is BLOCKED on this box as a shared-worktree hazard (never-rules-gate.sh). Used a
throwaway `git worktree add C:/tmp/wk-amgt-33-127-baseline cfb24cdf41...` (removed after use) to
run the UNCHANGED test suite: **323 passed, 0 failed**. This worktree's own HEAD is the same
commit (`cfb24cdf41`), so the baseline worktree carries byte-identical pre-edit source.

## AC0 (live, read-only)

Ran against Opal's own `opal-data-harvest` bucket via `_read_filing_source_object("992_HK_Equity")`
(the adapter's own key construction, unchanged by this cell) -- zero spend, zero egress off Opal,
no write. Confirmed the task order's quoted pre-state reason verbatim.

## Known estate gap

`.scratch/**` carries no static lane entry (row `Z-W126-S3`); if `owned-paths-validate.py` refuses
`.scratch/r127/*.py` at commit time, that is the disclosed gap, not a defect in this cell -- the
scripts and their printed output above stand regardless.
