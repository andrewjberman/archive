# AF1-s-1 -- the gap between the per-model rows and Opal's model total, explained

**Task order:** POSN_AGGFIX.TO-A1-1 (cell AF1-s-1, C-GAP-EXPLAINED). **Author:** 0.9.0_WK_POSN_AGGFIX~1.
**Produced by:** `a1_gap_explain.py` beside this file, run at workspace `ed1db8f1db`. Every AMOUNT, VersionId and count below is
printed by that run; line and commit citations are the author's reads at `ed1db8f1db`.

## The served file

- `s3://opal-data-portal-v2/platinum/mdpf/global/aum-metrics.json` VersionId `OVcFBOpgjFywfYJGYjowX2VSVwLdiyez`, LastModified 2026-09-15T13:50:50+00:00, period **2026-09-14**.
- `total.model_aum` = 1,800,437,987.06; `sum(by_model[].aum)` over 7 rows = 1,792,113,521.90.
- **Gap = 8,324,465.16.**

## The gold input, and the gap reproduced from it

- `s3://opal-data-assets/gold/mdpf_revamp/global/aggregate_aua_timeseries.json` VersionId `.UzblTWLJpsPRnUPs067bC5KuoRhP648`, LastModified 2026-09-15T13:31:07+00:00,
  `as_of_last` 2026-09-14. This is the object `dim_mdpf_aum_metrics.py` reads as `AGG_GLOBAL_KEY` (`:54`, `:114`),
  at the newest version written before the served file.
- `model_aua` at the frontier row = 1,800,437,987.06. The producer serves this value, rounded, as `total.model_aum`
  (`compose_current` `:184`, `:234`; `build_aum_metrics` `:488`, `:541`).
- The fold carries 10 `by_model` keys. The producer's per-key loop (`:497-512`) walks only its fixed `MODEL_ORDER` tuple
  (`:94-102`, 7 keys), keeping cohort `model`. Those 7 keys sum to 1,792,113,521.90.
  **Gap from gold = 8,324,465.16**; it differs from the served gap by 0.00. Of the served rows, 7 of
  7 equal the fold's per-key value.
- The sum of ALL cohort `model` keys at the frontier is 1,800,437,987.06; `model_aua` minus that sum =
  0.00. So `model_aua` is exactly the sum of the fold's cohort `model` keys.
- Cohort `model` keys the fold carries but `MODEL_ORDER` does not list: 1. They are `opal_fixed_income` (fold display_name 'Fixed Income', cohort_class 'model') 8,324,465.16,
  summing to 8,324,465.16. The gap minus that sum = 0.00.
- Keys with another cohort (opal_growth_sma [sma], opal_div_sma [sma]) are not in `model_aua`, so they are
  not part of this gap.
- Control arm: one served `by_model` row raised by 1.00 in memory moved the computed gap by 1.00.

## What the gap is

The gap is **the Fixed Income model's assets** (`opal_fixed_income`). The global fold counts that key in `model_aua`, and so
in the served `total.model_aum`. The served `by_model` has no row for it: `dim_mdpf_aum_metrics.py` builds its rows from a
fixed seven-key `MODEL_ORDER` (5 primary models + 2 blends) and has no `SERVED_MODEL_NAME` entry for Fixed Income.

The key joined the fold's `GLOBAL_MODEL_KEYS` at `2d5f8a7f74` (2026-08-26; `dim_mdpf_aggregate_aua_timeseries.py:126-140`).
That comment lists the files that must change in the same commit when a key is added, and `dim_mdpf_aum_metrics.py` is not
on the list. `dim_mdpf_aum_metrics.py` was last changed at `4707880967` (2026-08-06), before the key existed.

The crosswalk (`mdpf_revamp_model_crosswalk.py:126-139`) records Fixed Income as `served=False`, meaning "not in the 49F
SmartX served by_model{7} projection", and says "model_aua already carries these dollars -- by_model was the SHORT side".
The two blends in these served rows are `served=False` too, so that flag does not decide which keys get a row here.

DEFECT: against the producer's own stated contract. `dim_mdpf_aum_metrics.py:31-32` defines `by_model` as
"cohort_class=='model' ONLY", and `:27-28` defines `total.model_aum` as the `model_aua` frontier. The fold marks
`opal_fixed_income` cohort `model` and counts it in `model_aua`, yet the served rows omit it, so they fall short of
`total.model_aum` by exactly its value. The mechanism is a fixed key tuple (`:94-102`, walked at `:497`) that did not grow
when the fold's key set grew; the same tuple would silently omit any later cohort `model` key too. The producer's owner is
`0.4.0_DS_ClientPlatform` (Author line `:39`, gate `1.0.0_SA_CTO`). This project edits nothing there; the surprise row
POSN_AGGFIX-Z-W1-S1 carries the finding.

## What this means for the Positioning aggregate (read-only note)

Fixed Income is not a primary model and not a blend of primary models (`org/standards/POSN_AGGREGATE_MODEL_SET.json` v1.0).
Under that standard's `membership_rule`, its 8,324,465.16 falls outside the aggregate and is reported with the assets
left out. The standard's `measured_against.rows_outside_the_rule: 0` counts the seven served `by_model` rows. That count is
right for those rows, but it cannot see this key, because the served rows never carry it.
