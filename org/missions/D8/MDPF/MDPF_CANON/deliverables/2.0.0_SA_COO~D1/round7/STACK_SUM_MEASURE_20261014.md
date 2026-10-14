# The AUA Trend stack against the Total, measured (2.0.0_SA_COO~D1, 2026-10-14 ~19:0xZ) -- the input to the CN-i-2 ruling

Instrument: a read-only script over the NEWEST served Global time series `s3://opal-data-assets/portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-13.json` (496 dates, 487 with a Total, a non-model value and a model value). Per date,
the stack is what the CN-i-1 candidate draws: the sum of every non-SMA model line, plus `sma_additive_aua` plus the two carve-out SMA lines (`opal_div_sma`, `opal_growth_sma`), plus `tax_additive_aua`, plus the Other AUA remainder (`non_model_aua` minus the carve-outs).
The gap is `opal_aggregate_aua` minus that stack. The object's own `meta.by_model_fold` reads `min_firms 2` and `per_model_detail_begins 2026-05-15`.

## Result (MEASURED)

| range | dates | dates with |gap| > $0.02 | max |gap| | median |gap| |
|---|---|---|---|---|
| before 2026-05-15 (before the per-model detail begins) | 383 | 383 (all) | 1,349,270,858.88 | 853,979,716.37 |
| from 2026-05-15 | 104 | 55 | 58,576,784.27 | 26,403,642.48 |

- Before 2026-05-15 there is NO model line (every `model_value` is absent), so the stack misses the whole of `model_aua`: on 2024-11-01 the gap is 436,842,747.89 against a `model_aua` of 436,842,748; the gap IS the model dollars. The Trend therefore draws only the non-model band there, while the Model Portfolios
  headline reads the full Total (for example the Q1 2026 figure of $1.48B on the Snapshot's Total AUA strip against a Mar 31 2026 period-end bar near $0.27B on the Trend; both read off the issuer's local screenshots, so approximate and not re-measured from the data).
- From 2026-05-15 the 55 gaps (about $26M median, $58.6M at the largest, 2026-09-03) are of the same order as the pooled "Other Models" line ($69,190,304.67 on 2026-10-13, the CTO's figure), which would be exception (ii) in FWD-9 (2) -- CONSISTENT WITH it, NOT ESTABLISHED; the last five dates (2026-10-07 to 2026-10-13) are exact to the cent. NOT verified here: that each of the 55 equals that date's suppressed
  amount (the fold's own per-date record is not in the object; only the two keys named above are).

## What this corrects in my own work

The CN-i-1 data arm `D1` (`r7_cn_i_1.py data`) printed "exact 24, model_aua rounding gap 463, failing 0" and passed. Its second branch allows a gap up to `0.02 + |model_aua - sum(lines)|`, and the Total is built as model + non-model + SMA + tax, so the gap
EQUALS `model_aua - sum(lines)` by construction: the branch accepts every date and the arm cannot fail. "Rounding gap" was the wrong name for model dollars that no line carries. The CVO's NOT MET on the stack clause was right, and the worker's row D1-W18-S3 ("worst residual in the billions") named it.

## The ruling this needs (an ENDPOINT-text question, the CTO's)

FWD-9 (2) says the whole stack sums to `opal_aggregate_aua` to the cent EXCEPT (i) a negative Other AUA remainder and (ii) FWD-3's fold-suppressed dates. It names no exception for the 383 dates before `per_model_detail_begins`; it was written when the per-model history ran from 2024-11-01.
REC: an addendum exception (iii): on a date before `per_model_detail_begins` the model dollars are drawn as ONE band (working name "Models (detail withheld)", a colour distinct from every model colour by the CVO's colour-distance rule), so the stack equals the Total on every date and the withheld detail is stated on the face.
