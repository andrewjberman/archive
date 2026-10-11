# ROW3_VS_COTTONWOOD -- IRPT_DASHBD.TO-DB-b-116 (worker 0.9.0_WK_IRPT_DASHBD~91)

Machine record: `ROW3_VS_COTTONWOOD.json` (15 field groups, each with file-and-line evidence).

**Verdict: ROW3_TRUE.** No field reads FALSE. Stamping method_version 3 on the Cottonwood rows asserts nothing row 3 states that the code contradicts.

## Fields (what row 3 states / what Cottonwood does)

| Field | Verdict | Note |
|---|---|---|
| valuation_source | TRUE | positions_based / entry positions_x_as_traded_close |
| method | TRUE | TWR_DAILY_GEOMETRIC / FWD-3 ret = (value - flow) / prior value - 1 |
| flow_convention | TRUE | END / FWD-3 default flows at end of day |
| income_basis | TRUE (with a stated gap) | cash_when_received / income is inside value via the cash ledger, posted at the pay date |
| value_basis | TRUE | positions at the declared price basis plus cash / as-traded close plus cash leg |
| value_basis_ruling | TRUE | the entry names its own row 3 |
| fee_basis | NOT_STATED | per entry; entry field `fee_treatment` = net_of_fees carries it |
| tolerance, large_flow_share, plausibility band, comparability ceiling | NOT_STATED | copied from a thresholds file at write time; Cottonwood has none (thresholds=None, guard never reached) |
| guard_substitution | TRUE | fallback never emitted |
| day_count | NOT_STATED | not read by the daily return |
| tieout fields | NOT_STATED | producer constants |
| gips_alignment | TRUE | same label |
| measured_at, schema_version, source_pipeline | NOT_STATED | provenance |
| firm | TRUE | z09 resolves to cottonwood |
| method_version | TRUE | entry names 3 |

## Open items (not established)

1. Income basis: cash-posted income (dv, dvlt, dvst, int) enters value when the cash posts (default pay date; the valuation run call passes no `ex`). Whether a bond's stored close carries accrued interest is outside these files, and the exact flags of the 107,316-row run are not recorded in the repo; the code defaults are what is established.
2. A Cottonwood row 3 cannot be written without a thresholds file (producer line 2031), and no measured thresholds exist for this firm. Which values a Cottonwood row 3 carries is not decided here.

## dim row 3 partition

Address (builder output, firm scope cottonwood): `s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3`.
Read: head-object on its manifest.json through the `.tools/aws` shim returned 404 Not Found. **exists = false.**
Positive control: `s3://opal-data-49financial/irpt/49financial/gold/dim_return_method/method_version=2`, same call, returned the object. **exists = true.**
