# V2 record -- the 2026-10-01 19:19Z production Gold run (Tax on, HEALGAP catch-up's first run)

**Author:** 4.0.0_SA_CRO. **For:** the successor of 2.0.0_SA_COO~M (ledger `healgap-cottonwood-catchup-m-20261001`) and
leg V2 of `mdpf-gold-healgap-hookup-20261001`, per 1.0.0_SA_CTO msg 103954. V2's named target stays the
2026-10-02 13:30Z scheduled run; this record covers the run that first executed the catch-up.

## The run

- Function `mdpf-gold-lambda`, CodeSha256 `wKfgTBeq6yCiH8MI+XttYRmytUanrY+OcBxjlQGmaIo=` (pin 0f1a67e196), Tax enabled.
- Request `79bdb589-be06-4846-962f-9826f377b151`, input = the scheduled floor's own; status green, errors none, 16 of 16.
- Log stream `2026/10/01/[$LATEST]e4dbc5e2086d4271b045fe5e11514d47`. Catch-up lines 19:18:50-53Z: value dates
  2026-08-18, 08-20, 08-21, 09-23 and 09-24 rebuilt with `--upload`.
- Ledger `mdpf-taxsma-serve-today-20261001`: CLOSED, 5 of 5.

## The ten points (served after publisher run 20261001T192817Z-480ff6b0)

Cottonwood `opal_aggregate_aua` (model / non_model), absent -> measured. Key
`portal/gold/mdpf/cottonwood/aggregate-aua-timeseries/2026-09-30.json`, VersionId `ThA.4W1RehAKxMn4IW94iljKLLyK_fb5`:

| date | total | model | non-model |
|---|---|---|---|
| 2026-08-18 | 485,906,497.48 | 136,124,300.89 | 349,782,196.59 |
| 2026-08-20 | 478,225,040.53 | 139,107,569.53 | 339,117,471.00 |
| 2026-08-21 | 488,460,108.95 | 139,653,361.92 | 348,806,747.03 |
| 2026-09-23 | 555,728,472.01 | 175,667,910.62 | 380,060,561.39 |
| 2026-09-24 | 553,649,223.31 | 176,412,889.04 | 377,236,334.27 |

Global `opal_aggregate_aua`, carried -> measured. Key `portal/gold/mdpf/global/aggregate-aua-timeseries/2026-09-30.json`,
VersionId `zZ3uHjEM7miccPxIlvcAIFdlTFbW5oHO`:

| date | before (dry run, catch-up not run) | after | account_count_total |
|---|---|---|---|
| 2026-08-18 | 2,027,693,477.82 | 2,027,029,375.20 | 7791 -> 8259 |
| 2026-08-20 | 2,023,089,726.85 | 2,022,506,004.97 | 7791 -> 8262 |
| 2026-08-21 | 2,033,575,559.04 | 2,033,537,629.55 | 7791 -> 8263 |
| 2026-09-23 | 2,074,727,633.67 | 2,073,280,336.91 | 7799 -> 8328 |
| 2026-09-24 | 2,070,628,914.02 | 2,069,926,595.68 | 7799 -> 8331 |

Method: the stored series compared with the deployed Tax-on dry run of 19:08Z (request f2632444), key by key.
Cottonwood and Global differ from it ONLY at these five dates (fields `opal_aggregate_aua`, `model_aua`,
`non_model_aua`, `base_excluding_tax_aua`, account counts, `point_class`, `cohort_provenance`, plus `by_model`, `meta`
and `_provenance`, whose per-date content was not split further).

## The Tax identities (TX-r-3 branch 1), valued 2026-09-30

- (a) 49financial: 1,757,099,818.07 = 1,738,331,604.42 + Tax 18,768,213.65 (11 of 11 accounts; 14,318,213.65 measured
  + 4,450,000.00 workbook-stated). Global: 2,085,492,328.94 = 2,060,678,513.01 + Tax 24,813,815.93 (13 of 13). To the
  cent.
- (b) Cottonwood: SMA 0.00 -> 6,045,602.28, Client 362,817,714.13 -> 356,772,111.85 (down by the same amount), total
  541,313,055.76 unchanged.
- (c) Inflection's time series gains the extension fields with null values (`NOT_APPLICABLE`); its other documents
  are unchanged.
- (d) The seven keys Tax does not change keep their 13:31:19Z VersionIds.

## Not read

- The fee-basis component of identity (c).
- The DEV page: Andrew validated on PROD, verbatim "It works, i just smoked on PROD and looks great."
