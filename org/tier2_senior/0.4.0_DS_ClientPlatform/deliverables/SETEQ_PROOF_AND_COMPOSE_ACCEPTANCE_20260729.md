# Set-Equality Proof + Option-1 Compose Acceptance — 2026-07-29 ~0020Z

Owner: 0.4.0_DS_ClientPlatform. Orders: CTO 235422Z (set-equality), CTO 235944Z
(Andrew-direct Option 1 fix-then-flip), CTO 0004Z rider (scope consistency),
CTO 001553Z (identification accepted; compose design approved; rider proposal
accepted — one-live-composition invariant BINDING).

## 1. Set-equality: COO's 31 moved dates == Finding B, both directions

Artifacts (all S3 `opal-data-assets`, versioned GetObject):

| role | key / version | axis |
|---|---|---|
| refreshed | global/aggregate_aua_timeseries.json `Szlp_6rM...` @2026-07-28T23:48:38Z | 450 dates ..07-27 |
| served baseline (COO's) | same key, version `A2QBuod0Amch...` @2026-07-23T21:44:26Z | 447 dates ..07-22 |
| one-off backfill | cottonwood/aggregate_aua_timeseries_interpolated.json (frozen 07-23) | 447 dates; 45 interp (05-28..07-20) + 2 measured (07-21/22) + 400 absent |

- **Baseline identified:** refreshed-vs-A2QBuod reproduces COO's diff exactly:
  31 moved, earliest 05-28, latest 07-20, deltas @07-16/17/20 =
  -121,977,246.29 / -124,223,589.28 / -123,894,784.66, 07-21 unchanged.
- **Direction A (moved − interp = ∅):** every moved date is interp-labeled in
  BOTH provenance channels (old fold + one-off, 45/45 agreement), and
  `(old_total − new_total) == (old_model − new_model) == one-off MODEL leg`
  **31/31 to the cent**. The axis that makes it a proof: the fold consumes
  ONLY the cottonwood MODEL leg — the one-off's non_model (~$334mm @07-20)
  never participated (naive total-vs-total fails by construction).
- **Direction B (interp − moved = 14, all characterized):** on all 14 the
  global row is NULL in both artifacts (point_class=absent, 49F/INF legs
  None): weekends 05-30/31, 06-06/07, 06-13/14, 06-20/21; Juneteenth 06-19;
  and 06-01, 07-01, 07-13/14/15 — which are exactly members of the fold's own
  `GLOBAL_CROSS_AXIS_EXEMPT_DATES` (legacy-omitted trading days). A
  contribution added to a null row cannot move a total. **31 + 14 = 45, no
  remainder.**
- **Step +136,978,678.52 @07-20→21 is pure composition:** = cottonwood
  measured @07-21 (124,376,009.73; byte-equal in daily slice and one-off) +
  2-firm market delta (+12,602,668.79). 07-21 old==new to the cent. Old step
  +13,083,893.86 = same 2-firm delta + (measured 07-21 − interp 07-20
  123,894,784.66). No value change in either leg.
- Incidental, named non-material: 2025-11-03 + 2025-11-18 carry offsetting
  ±$0.01 model/non-model rounding flutter; totals identical.

Scripts + inputs: session scratchpad `setcheck/` (analyze.py + supplements);
denominators printed on every scan.

## 2. The Option-1 fix (compose, not revert)

`dim_mdpf_aggregate_aua_timeseries.py`: new `compose_cottonwood_leg(daily,
oneoff)` + `load_cottonwood_slice` now loads BOTH artifacts fail-closed and
composes. Rule (CTO 235944Z, Andrew verbatim carried in-code): splice one-off
values ONLY for dates strictly < first_measured_date (derived from the daily
covered set — 07-21 today, never hardcoded); labels preserved VERBATIM
(`interpolated_estimate`, never relabeled); counts never backfilled;
measured-vs-backfill collision refuses the build; daily slice remains the ONE
source for measured/frontier data (read-preference removal NOT reverted; the
one-off is still not a fallback for an absent daily leg). The composed leg
carries its own `cohort_provenance`, so the fold consumed it with ZERO fold
changes. `meta.composed_backfill` names source/window/authority/law.

**One-live-composition invariant (CTO 001553Z, binding):** tonight the
composition lives in the global producer's leg loader; post-fires it MOVES
into `build_cottonwood_mdpf_slice.py` (with the value_date re-key + W-2b under
CTO's three conditions) and the loader splice is REMOVED in that same change.
Until then the platinum cottonwood scope tab stays the 2-date stub — disclosed
to Andrew by CTO, named not hidden.

Tests: `tests/test_global_fold_flag2.py` 16/16 (11 existing + 5 new boundary:
window selection, 07-20/21 seam end-to-end, label integrity/verbatim,
loud collision, underivable-window refusal).

## 3. Acceptance (full-axis oracle, dry-run local build 00:20Z)

Build: gates all PASS (cross-axis, composition gate 450 dates, carry 3 dates
from measured as_of=07-22 window 3).

| row | required | measured |
|---|---|---|
| 31 previously-moved dates | restored to served values, residuals NAMED | **31/31 to the cent, zero residuals** |
| 3 fresh frontier dates | tonight's values held | 07-23/24/27 byte-match; headline **1,950,519,805.86 @07-27** |
| movers vs current serve | exactly the 31 | 31; both set-differences empty |
| +$137mm 07-20/21 seam | GONE, market scale | **+13,083,893.86**; only other >$60mm steps (05-14→15 +77.3mm launch seam; 07-10→16 +115.2mm across the null gap) are byte-identical in the served baseline — pre-existing |
| labels | interp never surfaces as measured/carried | slot histogram 400 absent / 45 interpolated_estimate / 2 measured / 3 carried; point_class interp on exactly the 31 value-bearing rows; null rows stay null |
