# Unidentified strategy candidates -- Cottonwood, Rebalancer date 2026-10-08 (MDPF_STRATID TO-W2-3, ST-w-3 / ST-w-4)

SOURCE: s3://opal-data-assets/blackdiamond/cottonwood/silver/fact_model_roster/date=2026-10-08/, fact_model_definition/date=2026-10-08/ (names); gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json (as_of_last 2026-10-07, by_model model_value, last non-null date per name); silver/fact_model_assignment/date=2026-10-08/ + fact_holdings/date=2026-10-07/ (fallback, joined fact_model_assignment.external_id = fact_holdings.AccountID, sum Market Value; latest holdings partition)
DENOMINATOR: 362 distinct names scanned (stripped; roster.model_name 71, definition.model_name 91, definition.sleeve_name 42, definition.component_name 271 distinct) ; looks-Opal 45
RESULT: LISTED 12
EXCLUDED-AS-MODEL: 26 -- roster.is_opal true (29 model names, fact_model_roster date=2026-10-08), looked Opal, no sleeve rule: Opal Satellite 50; Opal Satellite 60; Opal Satellite 80; Opal Satellite 70; Opal Ultra Short Term; Opal Satellite 40; Opal Moderate Income Portfolio; Opal Income Portfolio - Gillham; Opal UST/ Sat 70; Opal - Cash + Satellite 50; Opal 66% Long Term / 34% UST; Opal Satellite 30; Opal Satellite 15; Opal_Tax_Efficient_Income/Muni60/40; Opal Hendrickson LT/UST; Opal Moderate Income Portfolio (Tax Efficient); Opal Satellite 98; Blended Opal / Satellite 50; Opal UST/Sat 80 33/67; Opal Sat 50+ 15% cash; Opal_Satellite_20; Opal_UST/Moderate Income Blend; Opal 15/85 Income Portfolio; Opal Satellite 90; Opal 25/75 UST/ULT; Opal - Beecherl Legg

Rule: looks Opal = 'Opal' as a word, a list ticker as a word, a full name, or an sma_name_rules match; an Opal Model name (roster is_opal true) is excluded unless it matches a sleeve rule; listed when member_of (rebalancer_schemas.opal_sma_member_of) returns None or the matching rule has member null. Dollars are NOT summed across rows (a model and its sleeves overlap); None = neither source gives dollars, never 0.

| firm_id | name | dollars | reason | dollars_source | found_in |
|---|---|---|---|---|---|
| cottonwood | Opal_Muni_Income | 64,119,753.85 | RULE_NOT_COUNTED | HOLDINGS 1 of 1 accts | definition.model_name, definition.sleeve_name, roster.model_name |
| cottonwood | Opal Short-Term | 22,134,299.94 | NO_MEMBER | BY_MODEL opal_short_term @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Fixed Income | 8,274,779.91 | NO_MEMBER | BY_MODEL opal_fixed_income @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal_Moderate_Income_Tax_Efficient | 3,168,819.77 | NO_MEMBER | BY_MODEL opal_moderate_income_tax_efficient @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Long-Term Aggressive | 1,415,346.94 | NO_MEMBER | BY_MODEL opal_long_term_aggressive @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal_Muni_Sleeve | 550,823.07 | RULE_NOT_COUNTED | BY_MODEL opal_muni_sleeve @2026-10-07 | definition.model_name, definition.sleeve_name, roster.model_name |
| cottonwood | Opal Moderate Income | 192,694.43 | NO_MEMBER | BY_MODEL opal_moderate_income @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | OPAL INTERNATIONAL DIVIDEND INCOME ETF | None | NO_MEMBER | NONE | definition.component_name |
| cottonwood | Opal Conservative Growth | None | NO_MEMBER | NONE | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Intermediate-Term | None | NO_MEMBER | NONE | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Ultra Short-Term Income | None | NO_MEMBER | NONE | definition.model_name, definition.sleeve_name |
| cottonwood | POLEN DIVIDEND INCOME ETF | None | NO_MEMBER | NONE | definition.component_name |
