# AMGT-ba-14 dry run (0.9.0_WK_AMGT_RESAPP~280)

Command: `PYTHONPATH="$(pwd)" python -m lib.research.scores.run_scores --dry-run` (read-only on the pool, rc=0, 2026-10-06).

| figure | value |
|---|---|
| names keyed | 237 (crosswalk/v1/2026-09-29.json) |
| records built, none written | 237 |
| forecasts MEASURED | 92 |
| forecasts ABSENT | 145 |
| names with a consensus FY1 free cash flow | 86 |
| names with dispersion statistics | 0 |
| sd(D) | none: 0 names have a measured D (n = 0) |
| gate | served False: fewer than two names have a comparison score |
| correlation, house FY1 FCF to consensus FY1 FCF | 0.9429792728490989 |
| n for the correlation | 84 |

ABSENT forecasts by reason (145):

| count | reason |
|---|---|
| 137 | no reported financial history has been pulled for this name |
| 7 | only 0 years of reported free cash flow beside revenue are carried; at least 3 are needed |
| 1 | the reported annual revenue years are not consecutive, so growth is not measurable |

Beside the printed summary (a second read-only pass, same names): across the 84 names carrying both a house forecast and a consensus FY1 figure, the plain gap against consensus has median +5.3 percent, minimum -183.9, maximum +3902.9. Consensus and revenue units and currencies matched on all 84. Of the 92 measured forecasts, 4 carry no annual announcement date (the reference says so with its reason).

Printed summary, verbatim:

```
{
  "crosswalk_key": "crosswalk/v1/2026-09-29.json",
  "keyed_count": 237,
  "written_count": 237,
  "summary": {
    "forecasts_measured": 92,
    "forecasts_absent": 145,
    "forecasts_absent_by_reason": {
      "no reported financial history has been pulled for this name": 137,
      "only 0 years of reported free cash flow beside revenue are carried; at least 3 are needed": 7,
      "the reported annual revenue years are not consecutive, so growth is not measurable": 1
    },
    "names_with_consensus_fy1": 86,
    "names_with_dispersion_statistics": 0,
    "universe_gate": {
      "sd_D": null,
      "n": 0,
      "degenerate": null,
      "served": false,
      "reason": "fewer than two names have a comparison score, so its spread across the names cannot be checked and no value is shown",
      "floor": 0.25,
      "correlation_house_vs_consensus": 0.9429792728490989,
      "n_correlation": 84,
      "correlation_absent_reason": null
    }
  }
}
```
