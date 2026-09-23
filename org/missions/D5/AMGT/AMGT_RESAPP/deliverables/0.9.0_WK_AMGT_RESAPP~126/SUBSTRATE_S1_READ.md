# AMGT_RESAPP substrate card S1 -- can Bloomberg's dated `bestdata` vintages give a consensus REVISION series?

`0.9.0_WK_AMGT_RESAPP~126`, round 32, cell `AMGT-rk-126`. READ-ONLY, zero Bloomberg calls, zero pulls, zero
spend -- every number below comes from objects already in `s3://opal-data-harvest/bloomberg/harvest/bronze/bestdata/`.
Full working (Q1/Q2 script output) in `.scratch/r126/ac1.py` and `.scratch/r126/ac2.py` output, reproduced in this
cell's proof-of-spec instance.

**Store census (AC0), reproduced independently and matching the issuer's s.1 table exactly:** 7 objects across 4
securities -- `992_HK_Equity` ONE vintage, `CAT_US_Equity` / `CSL_AU_Equity` / `6861_JP_Equity` TWO vintages each.

---

## (a) What a vintage CONTAINS

One `bestdata` bronze object (e.g. `992_HK_Equity/20260922T201211Z.json`, Lenovo, read for Q1) holds:

- **3 fiscal-year period blocks** (`1FY`, `2FY`, `3FY`), each keyed by the Bloomberg security name.
- **6 distinct `BEST_*` field names per period** -- `BEST_DPS`, `BEST_EBITDA`, `BEST_EPS`, `BEST_PE_RATIO`,
  `BEST_SALES`, `BEST_PERIOD_END_DATE` -- **18 `BEST_*` field-value instances total** (6 fields x 3 periods). This
  is the DENOMINATOR Q1 asked for.
- A `requests` log: 3 `ReferenceDataRequest` records (one per fiscal-period override), each carrying its own `at`
  fetch timestamp, which is identical to the object's own key stamp.
- **No estimate-count or analyst-count field of any kind.** Checked against 7 candidate Bloomberg field-name
  shapes (`BEST_ANALYST_EST_NUMB`, `BEST_EST_NUM`, `BEST_NUM_ANALYSTS`, `BEST_NUM_ESTIMATES`,
  `NUMBER_OF_ANALYSTS_EPS`, `NUM_EST`, `BEST_EPS_NUMEST`) -- all 7 ABSENT -- and cross-checked exhaustively
  against every field name actually present in the object (the same 6 names above, nothing else). **The number
  of contributors behind a consensus figure is not carried anywhere in this schema.**
- The vintage's own AS-OF identity (when this consensus snapshot was taken) lives ONLY in the object key and the
  `requests[].at` field -- **not** inside the `BEST_*` value block itself.

A revision series needs: the consensus value per period (PRESENT), the fiscal-period identity it applies to
(PRESENT, `BEST_PERIOD_END_DATE`), and the AS-OF vintage (PRESENT, but only via the key/envelope, not the body).
It does NOT have the contributor count (ABSENT), which matters because without it a value move cannot be told
apart from a change in WHO is contributing to the average.

## (b) What the store DEMONSTRABLY PRESERVES, on the interval actually available today

Q2 diffed the earlier vintage against the later for all three two-vintage securities. **Note:** the task order's
own text states the two vintages are "~33 minutes apart"; the measured interval, computed twice independently
from the object-key stamps this session, is **~152.5 minutes (2h 32m 29s-30s)** for all three pairs -- filed as
surprise row `AMGT_RESAPP-Z-W126-S1` (the order's worked example, 12:48 -> 15:21, already subtracts to ~2h33m by
plain clock arithmetic, so the stated figure does not reconcile with its own worked times). The numbers below are
the MEASURED ~152.5-minute interval, not the order's stated ~33.

For all three securities (`CAT_US_Equity`, `CSL_AU_Equity`, `6861_JP_Equity`):

- 48 leaf fields present in both vintages, 0 added, 0 removed.
- 3 fields VALUE-MOVED -- all three are `requests[i]/at`, moving from the earlier stamp to the later stamp. This
  is the request log's own fetch timestamp, which by construction equals the object's own vintage stamp -- **not**
  a consensus signal.
- **Every one of the 18 `BEST_*` consensus field-value instances is byte-identical between the two vintages, in
  all three securities.**

**This demonstrates:** the store keeps each fetch as a distinct, immutable, separately-keyed object (never
overwritten -- confirmed by both vintages of each security co-existing under the same `security_key=` partition
with different stamp-named keys), and a reader can list, fetch and field-by-field diff two vintages of the same
name, correctly reporting fields in both / added / removed / value-moved with denominators. **This is the WEAK
claim and it is now measured, not assumed.**

**This does NOT demonstrate** that a consensus revision would be captured -- see (c). The 33-minute (stated) /
152.5-minute (measured) gap is too short for consensus to move on real estimates, so the IDENTICAL result here is
the *expected* outcome of the weak claim, and is not evidence about the strong one.

## (c) What remains UNANSWERED, and what a real test would need

**Whether the store would capture a genuine consensus REVISION -- a change in `BEST_EPS`/`BEST_SALES`/etc. driven
by analysts actually updating their estimates -- is UNTESTED by anything this estate currently holds.** Every
pair on disk today spans, at most, ~152.5 minutes on the SAME calendar day (2026-09-19); one of the four
securities (`992_HK_Equity`) has only ONE vintage and cannot be diffed at all yet. Consensus estimates do not
move meaningfully within a single afternoon; a null diff over that window is uninformative about revision
capture in either direction.

**What a real test needs, named for the CTO's card, not sized as an act to take here:**

- **Interval:** vintages spaced far enough apart to plausibly cross a real revision event for the name -- at
  minimum several DAYS apart, and to have a realistic chance of crossing an analyst update or corporate-action
  driven re-estimate, an interval on the order of WEEKS (spanning at least one earnings date or scheduled
  estimate-refresh window for the security) is the interval that would give a genuine test rather than another
  null result by construction.
- **Pull count:** at least 2 ADDITIONAL vintages per security beyond what is on disk today, spaced across that
  weeks-long window (3+ vintages total per security), so a step change can be told apart from single-sample
  noise; more than 2 additional pulls (e.g. one per week across a month) would let a reader see a trend rather
  than a single before/after pair.
- **A field this schema does not yet carry:** the contributor/estimate-count field named ABSENT in (a). Without
  it, even a real value move across a weeks-long gap cannot be told apart from a change in the contributor
  roster (analysts entering/leaving coverage) versus an actual re-estimate by the same panel -- so a genuine
  revision test also needs a request-schema question (does Bloomberg expose an analyst/estimate-count field for
  this request type at all, and if so under what field name), which is itself unanswered by anything on disk.

None of the above is proposed as an act this cell is taking or requesting to take -- it is stated so the interval,
pull count and open schema question can be carded by the CTO against the standing NO on a vendor subscription.
