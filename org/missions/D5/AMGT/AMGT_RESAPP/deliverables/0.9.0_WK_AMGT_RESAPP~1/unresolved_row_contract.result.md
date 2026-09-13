# AMGT-rc-19 -- THE UNRESOLVED-OVERLAY QUALIFICATION RULE (CLASS-LEVEL): result

**Worker:** `0.9.0_WK_AMGT_RESAPP~1` -- **Task order:**
`AMGT_RESAPP.TO-AMGT-rc-19.unresolved-row-contract.md` (AMENDMENT 1 -- CTO ruling @21343 folded in:
S11 QUALIFICATION RULE, class-level, NOT a bespoke consumer fallback).

## THE DEFECT (C-S19, CVO evidence @13ae38f3f89b)

"Fiscal join of period_end 2025-03-31 with only 2025-04-02 price returns price/date/gap **None**;
loader returns `{}`; rendering then retains the original BABA FY2025 **146.58** with no
unresolved marker." Before this cell, `load_corrected_price_overlay` filtered fiscal-year rows
to `row.get("price") is not None`, so an UNRESOLVED row (present but price `None`) was DROPPED
from the overlay entirely -- indistinguishable from a fiscal year the corrected lane never
covered at all (ABSENT). `apply_corrected_price_overlay` then found no overlay entry for that
year, `continue`d, and the consumer silently kept the OLD calendar-year figure, UNMARKED and
presented as trusted.

## THE FIX -- CLASS-LEVEL, NOT BESPOKE (CTO ruling @21343, Rule 22: fix what the members share)

`lib/research/rules/figure.py`'s `qualify()` now reads a new, stable field on the figure --
`corrected_overlay_status`, one of three states, closed against exactly this set:

- **RESOLVED** -- the corrected lane had a valid price and it was applied; falls through to the
  ordinary unit/sign check (an ordinary, freshly-measured figure now).
- **UNRESOLVED** -- the corrected lane covers this fiscal year but has NO valid price for it;
  REFUSED categorically, checked FIRST, before unit/sign -- no threshold invented
  (C-CHECK-MUST-REFUSE).
- **ABSENT** -- no corrected claim was ever made for this figure (missing lane/year, or the field
  is absent entirely, the default); the figure's own PRIOR (unit_status-based) verdict stands
  unchanged, distinguishing a genuinely missing lane/year from resolved data.

The qualification decision lives ONLY in the rule. `lib/research/provenance/render_print.py`
(the named provenance/print consumer -- `render_model_block` / `render_figure_line`, and
`lib/research/print/render_pack.py`'s `load_model_block`, which imports both overlay functions)
was changed to (a) keep EVERY fiscal-year row from the corrected lane (resolved or not) instead
of filtering price-`None` rows out, so UNRESOLVED can be told apart from ABSENT; (b) tag each
overlaid figure's `corrected_overlay_status` (bookkeeping, not a keep-or-mark decision); and
(c) route every fiscal-year PX_LAST figure through `lib.research.rules.figure`'s `qualify()`
before rendering, rendering anything short of PASS through `lib.research.checkface`'s own
S10/AMGT-rb-10 SALIENT MARKER (leading icon, value withheld -- never a bare, possibly-stale
number presented as trusted). `lib/research/checkface/run_checks.py`'s existing check-face
adapter (`check_one`) now forwards the same field too, so the S10 check-face pipeline qualifies
any figure carrying it correctly as well, with zero behaviour change for a figure that does not
carry it. No hand-written "don't silently fall back" branch was added inside
`load_corrected_price_overlay` or `apply_corrected_price_overlay` -- the decision the next
consumer of ANY corrected value needs is already in the rule, reusable without rewriting it.

## BEFORE / AFTER -- THE CVO CONTROL (period_end 2025-03-31, only a 2025-04-02 price -> corrected None)

A synthetic security (`BABACVOCTRL_US_Equity`, a DIFFERENT security key from BABA's own real,
landed data -- BABA's resolved FY2025 overlay is preserved untouched, see below) whose corrected
`model_block_fye_BABACVOCTRL_US_Equity.json` was produced by actually RUNNING
`fye_join.fiscal_period_join()` on a period_end **2025-03-31** fundamentals row paired against a
price series containing ONLY a **2025-04-02** (future) row -- the exact CVO scenario. The real
join engine genuinely resolves this to `price: None` (C-S15's future-only negative control,
exercised again here, not hand-set) -- **corrected None**. The original model block for this
security carries the illustrative stale calendar price **146.58** (the same number C-S19 named)
for fiscal year 2025.

**BEFORE this cell (the old `load_corrected_price_overlay`, silent-keep):** the UNRESOLVED row
would have been filtered out of the overlay entirely (`row.get("price") is not None`), the
consumer would find no overlay entry for fiscal year 2025, and `render_figure_line` would render
the bare, unmarked line:

```
146.58 PRICE (local trading currency, per share/unit) . PX_LAST (Last traded/closing price, in
the security's trading currency.) . as of 2025-12-31 . Bloomberg
```

-- the stale calendar price, presented as if trusted, with nothing to distinguish it from a
resolved figure. This is the C-S19 defect, reproduced by the CVO control's own fixture data.

**AFTER this cell (measured, via the NAMED consumer -- `render_pack.load_model_block` then
`render_print.render_figure_line`):** the figure is tagged `corrected_overlay_status: UNRESOLVED`,
its value is left exactly as landed (146.58 -- never fabricated, never dropped, STORE_CONTRACT
rule 1: "the calendar price may remain in source storage but never regains trusted
presentation"), and the RENDERED line is now:

```
[BLOCKED] [REFUSED: PX_LAST: corrected fiscal-period overlay is UNRESOLVED (the corrected lane
covers this fiscal year but has no valid price for it -- never silently kept as the old value,
C-S19)] PRICE (local trading currency, per share/unit) . PX_LAST (Last traded/closing price, in
the security's trading currency.) . as of 2025-12-31 . Bloomberg
```

**146.58 does not appear anywhere in the rendered line, or in the full rendered document
(`render_model_block`'s markdown) -- MARKED (REFUSE), never the bare stale value.** Measured by
`integrations/bloomberg/research/tests/test_unresolved_overlay_renders_marked.py` (3 tests: the
wired consumer tags UNRESOLVED and never fabricates a value; the rendered line never carries the
bare `146.58` and carries the REFUSE/marker; the full rendered document never carries the bare
`146.58` anywhere and the fiscal-year-2025 section carries the marker).

## THE CLASS-LEVEL, NEGATIVE CONTROL (rule alone, no consumer)

`lib/research/rules/tests/test_corrected_overlay_qualification.py` calls
`lib.research.rules.figure.qualify()` DIRECTLY, with no consumer in the loop, on the exact
silently-passing shape (`unit_status: MEASURED`, `corrected_overlay_status: UNRESOLVED`) and
asserts the verdict is REFUSE (or PROVISIONAL), never PASS -- proving the qualification is a
CLASS-LEVEL rule, reusable by any consumer, not a bespoke branch inside one consumer's loader.
The companion PASS arm (`corrected_overlay_status: RESOLVED`) and the two ABSENT arms (a clean
figure still PASSes; a figure REFUSED for its OWN, unrelated unit_status defect still REFUSEs,
for its own reason, never mentioning a corrected overlay it never had) round out the three
states this cell's contract distinguishes: **RESOLVED / UNRESOLVED / ABSENT (missing lane/year)**.

## PRESERVED -- BABA'S REAL, RESOLVED FY2025 OVERLAY

`load_model_block("BABA_US_Equity")`'s FY2025 PX_LAST figure still overlays to the corrected,
RESOLVED price **132.23** (2025-03-31), `corrected_overlay_status: RESOLVED`, renders bare/PASS
(unmarked, exactly as AMGT-rb-2 wired it) -- unaffected by this cell's fix. The on-disk original
`model_block_BABA_US_Equity.json` file's FY2025 PX_LAST stays byte-unchanged at 146.58
(STORE_CONTRACT rule 1) -- the original model_block on disk is never overwritten or aliased.

## FILES CHANGED

- `lib/research/rules/figure.py` -- the class-level `corrected_overlay_status` qualification
  (RESOLVED/UNRESOLVED/ABSENT), checked before the unit/sign check; also switched the module's
  import of `Rule`/`Verdict` from package-relative to absolute + repo-root-bootstrapped (matching
  `lib/research/checkface/markers.py`'s own convention), since AC3's own invocation loads this
  file standalone via `importlib.util.spec_from_file_location`, which raises `ImportError:
  attempted relative import with no known parent package` on a package-relative import (verified
  against the committed HEAD copy of this file before this cell's change -- a pre-existing
  condition, not introduced here).
- `lib/research/provenance/render_print.py` -- `load_corrected_price_overlay` keeps every
  fiscal-year row (not just resolved ones); `apply_corrected_price_overlay` tags
  `corrected_overlay_status`; `render_figure_line` routes every fiscal-year PX_LAST figure
  through the S11 figure rule and, for anything short of PASS, through
  `lib.research.checkface.render_print.render_value` + `lib.research.checkface.markers.marker_for`
  (S10/AMGT-rb-10's own marker convention, reused, not reimplemented).
- `lib/research/checkface/run_checks.py` -- `check_one`'s adapter now forwards
  `corrected_overlay_status` too (defaults to ABSENT), so the S10 check-face pipeline stays
  class-level as well.
- `lib/research/rules/tests/test_corrected_overlay_qualification.py` (new) -- the class-level,
  rule-alone difference arm.
- `integrations/bloomberg/research/tests/test_unresolved_overlay_renders_marked.py` (new) -- the
  CVO control, end-to-end, through the named consumer.

## AC4 (JUDGMENT -- never self-graded)

Recorded here, UNVERIFIABLE-BY-INSTRUMENT, `status_reason: 3.0.0_SA_CVO~Z` -- is this a genuine
CLASS-LEVEL S11 qualification rule (covers ANY consumer of a corrected value per the CTO ruling
@21343 / Rule 22) rather than a bespoke per-consumer fallback, and does S10 render the unresolved
figure REFUSE/PROVISIONAL (never the stale calendar price)? This worker's own evidence: the
qualification logic is entirely inside `lib/research/rules/figure.py::qualify()`, reached by TWO
independent import paths (the standalone `spec_from_file_location` load AC3 uses, and the normal
`lib.research.rules.RULES["figure"]` package import the new rule test uses) with identical
results; `lib/research/checkface/run_checks.py`'s pre-existing, GENERAL (any model_block figure)
check-face pipeline was extended by one field-forwarding line so it qualifies any
`corrected_overlay_status`-carrying figure too, without knowing anything about fiscal-year price
overlays specifically -- evidence the rule is reachable by a SECOND, unrelated consumer, not only
the one this cell wired. This is offered as evidence for the CVO's judgment, not a self-grade.
