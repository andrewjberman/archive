# CRPS-ab-2 -- the series-median unit rule, ROUND 26 (0.9.0_WK_AMGT_CORPUS~2)

Every line below is the checker's own output (`ab2_check.py`, which rebuilds a TEMP map from the builder and reads it through `model_block_pull._resolved_unit`), printed from the rule and never predicted. The committed `field_map.json` was not written.

## The rule

- `series_median_abs(mnemonic, hist_rows)`: the median of |value| over the fiscal years whose merged row (`merge_by_fiscal_year`) carries a finite numeric value for the key. Exact zeros are left out (a zero has no scale); a series of only zeros keeps median 0. Row `AMGT_CORPUS-Z-W2-S19`.
- `unit_input_value`: that median when the key has a fiscal-year series, else the single sample (`sample_value`). `classify_unit` is unchanged: the same magnitude bands and families, only its input changes. Sign is still read from the sample.
- `build_entries` re-reads a per-security entry that carries an exception (it is not cleanly measured); a cleanly MEASURED entry is never overwritten. Row `AMGT_CORPUS-Z-W2-S18`.
- The band constants hash to the base recorded at the cut (`bands_unchanged True`).

## Summary line

```
ab2 bp_pe_ratio RATIO bp_prof_margin PERCENT keys 100 unresolved_before 31 unresolved_after 11 bands_unchanged True
```

## Outcome by class (before -> after)

| key | mnemonic | figures | served before | after the rule | from |
|---|---|---|---|---|---|
| BBSE3_BZ_Equity | CAPITAL_EXPEND | 10 | UNRESOLVED | UNRESOLVED | series median 0.172 (4 non-zero of 10 years), outside 1 < av < 1e7: genuinely out of band, stays UNRESOLVED |
| BP-SLASH-_LN_Equity | PE_RATIO | 10 | UNRESOLVED | RATIO | series median 24.65 (FY2016-2025, 10 years) in the ratio band |
| BP-SLASH-_LN_Equity | PROF_MARGIN | 10 | UNRESOLVED | PERCENT | series median 1.4285 (10 years) >= 0.3, PERCENT |
| TSM_US_Equity | CURR_ENTP_VAL | 1 | UNRESOLVED | UNRESOLVED | no fiscal-year series; the single sample 71993494.7 is outside both bands: stays UNRESOLVED |

Totals: 31 served UNRESOLVED figures before, 11 after (20 closed: BP PE_RATIO 10, BP PROF_MARGIN 10); 11 remain (BBSE3 CAPITAL_EXPEND 10, TSM CURR_ENTP_VAL 1). Key count beside every count: 100.

## FIG lines (31, verbatim from the checker)

```
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2016 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2017 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2018 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2019 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2020 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2021 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2022 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2023 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2024 UNRESOLVED -> UNRESOLVED
FIG BBSE3_BZ_Equity CAPITAL_EXPEND 2025 UNRESOLVED -> UNRESOLVED
FIG BP-SLASH-_LN_Equity PE_RATIO 2016 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2016 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2017 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2017 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2018 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2018 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2019 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2019 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2020 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2020 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2021 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2021 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2022 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2022 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2023 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2023 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2024 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2024 UNRESOLVED -> PERCENT
FIG BP-SLASH-_LN_Equity PE_RATIO 2025 UNRESOLVED -> RATIO
FIG BP-SLASH-_LN_Equity PROF_MARGIN 2025 UNRESOLVED -> PERCENT
FIG TSM_US_Equity CURR_ENTP_VAL None UNRESOLVED -> UNRESOLVED
```
