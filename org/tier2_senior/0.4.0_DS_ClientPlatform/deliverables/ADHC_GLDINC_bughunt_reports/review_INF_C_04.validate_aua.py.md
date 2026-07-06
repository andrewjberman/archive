# REVIEW -- INF_C_04.validate_aua.py

- script: `data/inf/scripts/gold/INF_C_04.validate_aua.py`
- verdict: **issues-found**
- runs_in_incremental: False
- findings: 3

## Finding 1 -- [medium/numeric-sign-units/full]
- **Location:** `data/inf/scripts/gold/INF_C_04.validate_aua.py:141-153 (holdings cross-check)`
- **Mechanism:** firm_aua is measured at target_date = client_performance's max date (line 114), but holdings_aua is summed from latest_holdings_date() (line 141) -- an INDEPENDENTLY computed latest holdings partition. In a daily pipeline these two 'latest' dates routinely differ (holdings can lag/lead client_performance by a day), so diff_pct (line 148) compares AUA across two DIFFERENT dates. Separately, if 'market_value' is absent from holdings, holdings_aua=0 (line 145) and max(holdings_aua,1)=1 makes diff_pct = abs(firm_aua-0)/1*100 = firm_aua*100 (~6.7e10 for $667M) -- a nonsense percentage. Note: this only emits a WARN into a non-blocking validator (script always exits 0, writes no artifact), so blast radius is a misleading/noisy validation, not a crash or a served number.
- **Failure scenario:** Holdings latest partition is 2026-04-19 while client_performance latest is 2026-04-20 and >5% net flow/market move occurred between the two dates -> a persistent false 'X% drift' WARN fires every run, training operators to ignore the drift alarm and masking a future REAL drift. Or if market_value is dropped upstream, diff_pct computes as ~6.7e12% -> garbage WARN.
- **Proposed fix:** Filter holdings to the SAME target_date used for firm_aua (or skip the cross-check when the two dates differ), and when holdings_aua<=0 skip the drift computation instead of dividing by max(holdings_aua,1).

## Finding 2 -- [medium/type-issue/full]
- **Location:** `data/inf/scripts/gold/INF_C_04.validate_aua.py:114-115`
- **Mechanism:** target_date is derived via cp['date'].max().date() (pure calendar date, line 114) but the row filter uses cp['date'] == pd.Timestamp(target_date), i.e. tz-naive midnight (line 115). cp['date'] was coerced with pd.to_datetime (line 107); if I_C02 writes 'date' with any intraday time component or as tz-aware, the equality matches ZERO rows even though that date's data exists. latest.empty then becomes True (line 116) and the AUA-range check, zero-AUA check, and firm-total logging (lines 119-138) are ALL skipped with only a soft 'no rows for date' WARN -- the core AUA validation silently does not run on the most important (latest) date.
- **Failure scenario:** client_performance 'date' stored as tz-aware '2026-04-20T00:00:00+00:00' (or with a non-midnight time). pd.Timestamp('2026-04-20') is tz-naive midnight; the elementwise comparison is all-False -> latest is empty -> firm AUA is never range-checked and zero-AUA households are never counted for the latest date, defeating the validator.
- **Proposed fix:** Normalize both sides before comparing: use cp['date'].dt.normalize() == pd.Timestamp(target_date) (and strip tz), or compare cp['date'].dt.date == the parsed date object.

## Finding 3 -- [low/empty-null-handling/full]
- **Location:** `data/inf/scripts/gold/INF_C_04.validate_aua.py:120,133`
- **Mechanism:** firm_aua = latest['total_aua'].sum() (line 120) skips NaN by pandas default, and the zero-AUA test (latest['total_aua'] <= 0) (line 133) evaluates NaN as False. Households with NaN total_aua are therefore neither included in the firm total nor flagged as zero/negative -- they are invisible to every check. Again a validation-quality gap only (no crash, no served output).
- **Failure scenario:** 50 households have NaN total_aua from an upstream join miss; firm_aua sums only the non-NaN rows (understated), so the firm total can read in-range while coverage is actually broken, and the zero-AUA count reports 0 -- the NaN population passes validation undetected.
- **Proposed fix:** Add an explicit NaN-count guard on total_aua (e.g. flag latest['total_aua'].isna().sum() > 0 as an issue) so missing values are surfaced rather than silently dropped from the sum and the zero-AUA test.
