# MDPF_CANON round 11 -- the XA-6cad ruling read against CN-s-5 and cell (B) (2.0.0_SA_COO~D1, 2026-10-16 ~15:2xZ)

**archetype:** DIAGNOSE

Input: the laptop CTO's ruling on call `dell1-20261016T143036Z-c7de` (cross-adjudication `XA-20261016T143752Z-6cad`, ruled 14:43:09Z; box CTO msg 6758): (B) with (C) as the interim, (A) refused. (C) = "Variant 1 without the pre-2026-05-15 stitch, one Models band there", shipping with CN-s-4's promote. (B) = the producer writes the stitched pre-05-15 per-model series into a Global-scope aggregate field, under a never-widen pair, with the condition "any per-model point backed by exactly ONE firm is suppressed in the Global field".

## 1. CN-s-5 as built does not implement (C) -- it is superseded by it (the issuer's ruling inside its own decomposition)

Read at `buildGlobalTrendRows` (portal DEV base `39dab87f3b`, `src/lib/trendGrouping.ts`, with CN-s-4 applied) and at the CN-s-5 diff (portal `e206e06e`):
- The Models band is set only when `mode === 'variant2' && pre` (before `per_model_detail_begins`). In `variant1` the pre-05-15 span has no band.
- With CN-s-5 a demo session gets `mode = variant1` and the two single-firm reads enabled. On PROD the edge refuses both (403, ruling context), so the queries return nothing; the stitch memo then returns an object whose two maps are EMPTY, not null, so `stitchOn` is true with empty series: the five pre-05-15 model lines are null AND the band is null. The pre-05-15 span would draw no model composition at all, not "one Models band".
- Everything Variant 1 adds over Variant 2 is the stitch (and a composition footnote that, by its own doc comment, "names two partner firms" and is for internal sessions). Without the stitch, "Variant 1 with one Models band" IS Variant 2, which is what the demo tenant draws today. So (C) needs no portal change beyond CN-s-4: CN-s-4 repairs Variant 2's band, and the demo, still on Variant 2, picks it up.
- Not read: whether the page also gates the composition footnote on `internal`.

**Disposition:** CN-s-5's commit (`e206e06e` on the worker's portal branch, proof instance VALID, wiring 10 of 10) stays on that branch as a build of a design the CTO's ruling replaced. It is NOT cherry-picked into any landing candidate. Its order `MDPF_CANON.TO-CN-s-5` is set `superseded` with the pointer to XA-6cad and this file. If (B) lands, the demo's Variant 1 wiring is re-cut against the field (a different gate set), not this one.

## 2. Cell (B) is empty under its own condition -- MEASURED

Read-only, 2026-10-16 ~15:2xZ, the served per-firm `aggregate-aua-timeseries` objects of 49financial, inflection and cottonwood (`opal-data-portal-v2/platinum/mdpf/<scope>/`), counts only: the Global `meta.by_model_fold.per_model_detail_begins` reads 2026-05-15; there are 383 Global dates before it (2024-11-01 .. 2026-05-14). For each of the five primary models, the number of firms with a strictly positive value on each of those dates:

| model | 0 firms | 1 firm | 2 firms | 3 firms |
|---|---|---|---|---|
| Ultra-Short Term | 50 | 333 | 0 | 0 |
| Short Term | 0 | 383 | 0 | 0 |
| Intermediate Term | 0 | 383 | 0 | 0 |
| Long Term | 0 | 383 | 0 | 0 |
| Ultra-Long Term | 0 | 383 | 0 | 0 |

(A first count that treated a zero-padded value as a value read 2 firms on every date; the zeros are padding, so the table counts strictly positive values.) Every pre-05-15 per-model point is backed by exactly ONE firm (1,865 points), so the CTO's condition suppresses ALL of them: the suppression count is 1,865 of 1,865, the surviving series is empty, and the demo would read nothing from (B) that (C) does not already draw. The Global `model_aua` that Variant 2's band reads before 05-15 is itself one firm's value today (an existing state, not changed by this round).

## 3. What is asked of the CTO (one ask)

Confirm (C) as the final form and strike (B) as vacuous, or say what (B) is for if it is not the demo's pre-05-15 span (for example a different suppression rule, a wider definition of "firm", or Andrew's word that the demo should see the single-firm history, which FWD-3 and the ruling's own reasoning refuse).
