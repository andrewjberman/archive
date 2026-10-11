# CN-d-3 AC3 -- the tooltip read the packet left open (2.0.0_SA_COO~D1, 2026-10-11 ~07:1xZ)

The render in `ROUND4_CLOSE.md` did not raise the tooltip. This one does (`ui-smoke.mjs portfolios --click Trend --hoverlast`, the page served
from the candidate worktree @133fb8af, the same one-object fixture: global `aggregate-aua-timeseries` of 2026-10-08, read-only get).
Screenshot: `round4/runs/cn_d_3_global_trend_tooltip_20261008_133fb8af.png`.

- **Sampled date:** 2026-10-08, the frontier of the daily chart; both additive series are non-null there.
- **Tooltip, read from the PNG:** Total AUA $2.15B; rows include `Other AUA` $290M, `Additive SMA sleeves` $410K and `Tax-Managed SMA` $28.8M beside
  the five core models and the small cottonwood models.
- **Rows against the Total:** the displayed rows sum to about $2.148B, which rounds to the $2.15B Total (the figures are the tooltip's own,
  rounded to three digits; this is a reading of the picture, not an exact sum).
- **Exact identity from the same arrays:** `opal_aggregate_aua - (model_aua + non_model_aua + tax_additive_aua + sma_additive_aua)` = 0.00 at
  2026-10-08 (and the 4-term identity holds on 484 of 484 non-null dates, `r4_cn_d_1.py` arm A4).
- **Not read:** other additive dates (only the frontier was sampled); a hover on the quarterly bars; the per-firm views (the candidate shows no
  band there by construction, `!timeSeriesData.isPerFirm`, and this render is the Global view only).
- **Unchanged from the first render:** the category-views panel reads "could not be loaded" (its request was not stubbed); it is not this cell's.
