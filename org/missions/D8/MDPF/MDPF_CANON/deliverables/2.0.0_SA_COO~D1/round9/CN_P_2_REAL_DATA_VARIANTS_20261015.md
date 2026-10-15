# CN-p-2: the Global Trend rows on the REAL served 2026-10-14 objects, both variants (2.0.0_SA_COO~D1, 2026-10-15 ~14:5xZ)

Evidence for the CVO's AC4 of `MDPF_CANON.TO-CN-p-2` (and for the packet's stated limit that no NON-internal session was rendered). It is NOT a render: it runs the page's own pure module (`buildGlobalTrendRows`, `portal/src/lib/trendGrouping.ts` as on DEV `e0b033253b`, blob-equal to PROD `c3b21a40e2`) over the newest gold objects of Global, 49 Financial and Inflection (2026-10-14, written by the 13:31Z scheduled fire), with the stitch built as the page's memos build it. Script: `round9/checks/measure_real_variants.ts` (`UNROLLED=1`: the page as built). Read-only; nothing written to AWS.

## Variant 1 (an internal session; the stitch ON)
- 497 rows, frontier 2026-10-14. **Custom Models: first value 2026-05-15 (26.25M), last 2026-10-14 (68.88M), NO null after the first value; 21 rolled dates (the 9 carried dates plus 12 where the pool is not served).** 34.30M at 2026-06-30 (the CRO spec oracle), 66.92M at 2026-09-30.
- The five model lines before 2026-05-15 are the 49 Financial series (1,915 non-null cells over the 383 earlier rows); no Models band.

## Variant 2 (every other session, the demo tenant included; the stitch OFF)
- The 383 rows before the per-model detail begins (2026-05-15) each carry ONE `Models` band (383 of 383), and the five model lines carry **0** cells there: no single-firm value reaches a non-internal session.
- Custom Models is suppressed (`customSuppressed`) on 55 dates, 2026-05-15 to 2026-09-09, and drawn from the served difference on the dates where the pool is served (50 of 114 later rows have a value); the footnote text is the module's `SUPPRESSED_FOOTNOTE`.
- Total, Client Supervised, ETF Strategies and ALT Strategies read identically in both variants on every one of the 497 rows (the groups are served fields, not recomposed).

## Limit
This grades the function on real data. It does not show a browser session of a non-internal login (none exists), and `isInternal()` / the auth claims are the page's, not exercised here.
