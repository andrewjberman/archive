# MDPF_CANON -- the fe9b Global fold: what is measured before the cell is cut (2.0.0_SA_COO~D1, 2026-10-12 ~14:2xZ)

Input: the cluster lead's ruling (A) relayed in msgs 4391 and 4393; local record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/RECORD_FE9B_RULED_BY_CLUSTER_LEAD_20261012.md`. The laptop record is not on this box yet. Nothing here is a cell, an
order or a decomposition: it is the read the cut will stand on. Read-only gets of the four scopes' `aggregate-aua-timeseries` for 2026-10-09.

## 1. The fold set at the as-of 2026-10-09 (aggregate-aua-timeseries)

`min_firms = 2`, "held" = a nonzero `account_count` at the as-of in the firm scope's own object (the CN-c-1 / CN-d-2 basis rule), carries counted as carries.
Global carries 20 `by_model` lines; 14 are held at fewer than 2 firms, 6 are not:

| held at | lines |
|---|---|
| exactly one firm: cottonwood (8) | `opal_15_85_income_portfolio`, `opal_fixed_income`, `opal_income_portfolio_gillham`, `opal_moderate_income`, `opal_moderate_income_portfolio`, `opal_moderate_income_tax_efficient`, `opal_muni_sleeve`, `pfde` |
| exactly one firm: inflection (2) | `opal_blend_5050_int_ltc`, `opal_blend_5050_st_int` |
| no firm, a `count_as_of` carry (2) | `opal_growth_sma`, `opal_div_sma` |
| no firm, null at the as-of (2) | `opal_income`, `opal_moderate_income_portfolio_tax_efficient` |
| two or more firms (6, stay as lines) | not re-listed in this read; by the CN-c-1 basis these are the five core models and `tax` |

8 + 2 + 2 + 2 = 14 folded, 6 kept, 20 read.

## 2. "per as-of": the two readings agree on recent history

The ruling says min_firms is "computed per as-of from the firm scopes' own objects, never a static list". Two readings: (a) evaluated at each served object's as-of
and applied to its whole history arrays; (b) evaluated date by date inside the arrays. Measured over the last 60 dates for the 14 folded keys: 0 of 14 change fold
status on any date, so (a) and (b) produce the same fold set on that window. They can differ on older history or when a model gains a second firm; the cut states
(a) unless the CTO names (b), because a line that appears and disappears by date would put None gaps in a chart line.

## 3. What the cut has to settle (not decided here)

- Which served objects carry per-model lines: the four global types (`aggregate-aua-timeseries`, `aum-metrics`, `account-distribution`, `category-views`) and
  their meta (`by_model_channels`, `count_as_of`). "JSON keys unchanged" is read as: the objects' top-level key sets do not change; the `by_model` dict loses
  folded keys and gains one other-models key.
- The other-models line's key, display name and cohort class (registry row), and how a folded carry's `count_as_of` is stated in-band.
- The sum rule for the other-models line per date: the sum of the folded lines' values; `None` only where every folded line is `None` (absent is not zero).
  Headline sums (`opal_aggregate_aua`, `model_aua`, `non_model_aua`, additive terms) must read equal before and after on every date.
- The never-widen pair: every global leaf read before and after (value-equal outside `by_model`; the new line equals the sum of the removed ones), the rollback per
  key, and the writer count N for each type.
- Sequencing: the fold edits `mdpf_gold_consolidator.py`, the file CN-d-1's deploy (`ADHOC.canon-r4-code-deploy`) is about to ship. The fold's deploy comes
  after that order's ledger CLOSED, in its own window, and after FIRMBKTS's flip receipt for any shared surface it touches (R2).
- Process: round 5's decomposition is frozen and its slug is HELD, so the cell is round 6's, cut on the CTO's round-5 analysis or on an addendum to it that
  cites the record above.
