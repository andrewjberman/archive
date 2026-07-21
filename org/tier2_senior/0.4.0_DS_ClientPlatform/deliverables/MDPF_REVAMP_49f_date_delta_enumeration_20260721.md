# MDPF_REVAMP -- 49F aggregate-aua-timeseries DATE-SET symmetric diff, fully enumerated

**Author:** 0.4.0_DS_ClientPlatform | **For:** 1.0.0_SA_CTO (gate 135429Z/142516Z) + 0.2.0_DT_PortfolioAnalytics (parity harness)
**Date:** 2026-07-21 | **Grounding:** live S3 (read-only) + canonical `lib/trading_calendar.py`

## Why this exists
CTO gate item (135429Z, confirmed 142516Z): the DT parity harness index-joins two DIFFERENT
date SETS -- my serve-real real-trading axis vs the legacy rederived-business-day axis -- which
compares wrong dates from the first divergence (Verification Law #6: a rigorous instrument on the
wrong axis SURVIVES review). Before an N=3 pass can count, the full symmetric diff must be a
**fully-explained named structural delta**, not hand-waved. CTO: "ANY date you cannot explain is a
BUG." This enumerates and characterizes every date, against the ONE canonical NYSE calendar.

## Sources (both read-only)
- **SERVED (legacy):** `s3://opal-data-portal-v2/json/mdpf/49financial/aggregate-aua-timeseries.json` -> `dates[]`
- **MINE (serve-real):** the exact `dates` the artifact builds = `aum_daily._day >= 2024-11-01`
  (`fact_model_aum_daily`, opal-data-assets smartx silver), via the artifact's own `load_aum_daily`.
- **Classifier:** `lib.trading_calendar.is_trading_day` (NYSE; the estate's single frontier definition).

## Result (grounded 2026-07-21; REFINED to the EXPLICIT canonical calendar axis)
| set | n | span |
|---|---|---|
| SERVED (legacy) | 429 | 2024-11-01 .. 2026-07-18 |
| MINE (serve-real, canonical NYSE axis) | 427 | 2024-11-01 .. 2026-07-20 |
| COMMON | 407 | -- |
| SERVED-ONLY | 22 | all NON-trading |
| PUBLISHED-ONLY | 20 | all real trading days |

**PARITY-NEUTRAL GUARD REFINEMENT (2026-07-21, CTO calendar-wiring):** wiring the axis to the
EXPLICIT canonical NYSE calendar (`_trading_day_calendar`, byte-identical to `lib/trading_calendar`)
caught that **`fact_model_aum_daily` carries a datapoint for 2025-01-09** -- the Carter National Day
of Mourning, when the **NYSE was CLOSED**. The canonical calendar correctly drops it, so the axis is
**428 -> 427** and **2025-01-09 moves from common to SERVED-ONLY** (a holiday-fill like the other 21).
Refined diff: **407 common / 22 served-only / 20 published-only**, identical across all 3 firms
(shared axis). CTO's original 427/19 reconciles: the +1 published (07-20 fresh tail) and the -1 common
(01-09 dropped) net to 427 with 20 published-only. This is the guard doing exactly its job -- an
implicit-partition axis silently included a non-trading day; the explicit calendar excludes it.

### SERVED-ONLY (22) -- legacy has, serve-real omits -> ALL synthetic holiday-fills
Every one is a NYSE non-trading day (weekend or holiday). The legacy rederived-business-day axis
filled these forward; serve-real correctly omits them (no real trading occurred). **0 real trading
days were dropped from serve-real.** Dates: 2024-11-28, 2024-12-25, 2025-01-01, **2025-01-09
(Carter National Day of Mourning, NYSE closed -- caught by the parity-neutral guard)**, 2025-01-20,
2025-02-17, 2025-04-18, 2025-05-26, 2025-06-19, 2025-07-04, 2025-09-01, 2025-11-27, 2026-01-19,
2026-02-16, 2026-04-03, 2026-05-25, 2026-06-13(Sat), 2026-06-14(Sun), 2026-06-19, 2026-06-20(Sat),
2026-06-21(Sun), 2026-07-18(Sat). (CTO pre-accepted 21 as holiday-fills; 01-09 added by the guard.)

### PUBLISHED-ONLY (20) -- serve-real has, legacy omits -> ALL real trading days w/ real data
Every one is (a) a real NYSE trading day AND (b) carries real measured `aum_daily` data (7-8 model
rows, 7 nonzero core/blend models, summed closing_equity $1.11B-$1.43B, scaling correctly over
time). **0 parse artifacts. 0 non-trading days. 0 empty/zero (i.e. none is spurious axis-padding).**

- **1 fresh frontier tail:** `2026-07-20` (Mon) -- the real trading day past legacy's last real
  date (legacy's last is 07-17 Fri; it padded to Sat 07-18). This is the +1 vs CTO's 427 count.
- **19 in-range real trading days the legacy backfill/rederive process failed to emit** (now
  correctly present in serve-real): 2025-12-24, 2025-12-30, 2025-12-31, 2026-01-02, 2026-02-02,
  2026-03-02, 2026-04-01, 2026-05-01, 2026-06-01, 2026-06-08, 2026-06-26, 2026-06-29, 2026-06-30,
  2026-07-01, 2026-07-09, 2026-07-10, 2026-07-13, 2026-07-14, 2026-07-15.

  **Observation (legacy-gap pattern, NOT a claim about my data):** the 19 cluster at month
  boundaries (first trading day of Dec'25/Jan/Feb/Mar/Apr/May/Jun/Jul) + month/year ends
  (12-24, 12-30, 12-31, 06-26, 06-29, 06-30) + a recent run (07-09..07-15). This is consistent
  with the legacy artifact's rederived-business-day axis being an INCOMPLETE sampling of the NYSE
  calendar (its own gaps), not a complete trading-day frontier. This is a legacy deficiency; every
  one of these dates is a real measured trading day that serve-real correctly includes. (If CTO/DT
  want the legacy MECHANISM source-confirmed rather than observed, I can trace
  `data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py` -- flagged, not assumed.)

## Conclusion
The full symmetric diff is FULLY EXPLAINED: **408 common + 21 synthetic holiday-fills (served-only,
correctly dropped) + 19 legacy real-trading-day gaps + 1 fresh frontier tail (published-only, all
real measured).** My serve-real axis is the CORRECT and COMPLETE NYSE trading-day frontier; the
legacy axis both over-includes (21 fills) and under-includes (19 real-day gaps). **No unexplained
date -> no bug in the serve-real axis.**

## Implications for the harness + CTO's S3 re-verify (IMPORTANT -- same wrong-axis class)
The date-set divergence propagates into the LATEST checks, not just the history join. Because my
frontier (07-20) is PAST served's (07-17 real / 07-18 fill):

1. **Date-JOIN, not index-join, for the 408 common** (already confirmed to DT).
2. **The "latest tie" MUST be evaluated at the LAST COMMON date, never positional `[-1]`.** My
   `model_aua[-1]`/`custody[-1]` sit at 07-20 -- a date the served artifact does not contain.
   Comparing my `[-1]` to served `[-1]` compares 07-20 vs 07-18: the SAME wrong-axis error one
   level up. The correct tie: `mine[@last_common_date] == served[@last_common_date]`.
3. **`len` is dynamic, not frozen 427.** It is `n real NYSE trading days in [2024-11-01 .. current
   aum_daily frontier]` -- 428 as of 07-21 and growing daily. CTO's locked `len==427` and
   `custody[-1]==$1,665,338,126.76` are keyed to the 07-17/18 vintage; at stage time the frontier
   will have advanced, so re-anchor the tie/len targets to the stage-time frontier (or the values
   verify at the last-common-date, with my fresh tail recorded as a named published-only delta).

These are recorded so the N=3 pass is evaluated on the right axis and does not false-fail (or
false-pass) on the latest cross-section.

## Reproduce
`scratchpad/enumerate_49f_date_delta.py` (reads served + builds mine via the artifact's own loader
+ classifies via `lib.trading_calendar`; also proves per-date real data presence).
