# Unidentified strategy candidates -- Cottonwood, Rebalancer date 2026-10-08 (MDPF_STRATID TO-W2-3, ST-w-3)

SOURCE: s3://opal-data-assets/blackdiamond/cottonwood/silver/fact_model_roster/date=2026-10-08/, fact_model_definition/date=2026-10-08/ (names); gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json (as_of_last 2026-10-07, by_model model_value, last non-null date per name); silver/fact_model_assignment/date=2026-10-08/ + fact_holdings/date=2026-10-07/ (fallback, joined fact_model_assignment.external_id = fact_holdings.AccountID, sum Market Value; latest holdings partition)
DENOMINATOR: 362 distinct names scanned (stripped; roster.model_name 71, definition.model_name 91, definition.sleeve_name 42, definition.component_name 271 distinct) ; looks-Opal 45
RESULT: LISTED 38

Rule: looks Opal = 'Opal' as a word, a list ticker as a word, a full name, or an sma_name_rules match; listed when member_of (rebalancer_schemas.opal_sma_member_of) returns None or the matching rule has member null. Dollars are NOT summed across rows (a model and its sleeves overlap); None = neither source gives dollars, never 0.

| firm_id | name | dollars | reason | dollars_source | found_in |
|---|---|---|---|---|---|
| cottonwood | Opal_Muni_Income | 64,119,753.85 | RULE_NOT_COUNTED | HOLDINGS 1 of 1 accts | definition.model_name, definition.sleeve_name, roster.model_name |
| cottonwood | Opal Satellite 50 | 36,851,854.34 | NO_MEMBER | HOLDINGS 90 of 90 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Satellite 60 | 34,014,145.04 | NO_MEMBER | HOLDINGS 89 of 89 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Short-Term | 22,134,299.94 | NO_MEMBER | BY_MODEL opal_short_term @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Satellite 80 | 22,051,129.97 | NO_MEMBER | HOLDINGS 72 of 72 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Satellite 70 | 18,664,416.41 | NO_MEMBER | HOLDINGS 46 of 46 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Ultra Short Term | 18,297,784.85 | NO_MEMBER | BY_MODEL opal_ultra_short_term @2026-10-07 | definition.model_name, roster.model_name |
| cottonwood | Opal Satellite 40 | 17,274,676.91 | NO_MEMBER | HOLDINGS 29 of 29 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Moderate Income Portfolio | 8,382,556.99 | NO_MEMBER | BY_MODEL opal_moderate_income_portfolio @2026-10-07 | definition.model_name, definition.sleeve_name, roster.model_name |
| cottonwood | Opal Fixed Income | 8,274,779.91 | NO_MEMBER | BY_MODEL opal_fixed_income @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Income Portfolio - Gillham | 4,025,964.13 | NO_MEMBER | BY_MODEL opal_income_portfolio_gillham @2026-10-07 | definition.model_name, definition.sleeve_name, roster.model_name |
| cottonwood | Opal_Moderate_Income_Tax_Efficient | 3,168,819.77 | NO_MEMBER | BY_MODEL opal_moderate_income_tax_efficient @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal UST/ Sat 70 | 2,324,902.63 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal - Cash + Satellite 50 | 2,258,997.37 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal 66% Long Term / 34% UST | 2,135,891.81 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Satellite 30 | 1,801,565.72 | NO_MEMBER | HOLDINGS 5 of 5 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Satellite 15 | 1,707,633.17 | NO_MEMBER | HOLDINGS 5 of 5 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Long-Term Aggressive | 1,415,346.94 | NO_MEMBER | BY_MODEL opal_long_term_aggressive @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal_Tax_Efficient_Income/Muni60/40 | 1,377,057.67 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Hendrickson LT/UST | 1,374,302.20 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Moderate Income Portfolio (Tax Efficient) | 1,117,136.69 | NO_MEMBER | BY_MODEL opal_moderate_income_portfolio_tax_efficient @2026-09-25 | definition.model_name, roster.model_name |
| cottonwood | Opal Satellite 98 | 1,047,602.46 | NO_MEMBER | HOLDINGS 11 of 11 accts | definition.model_name, roster.model_name |
| cottonwood | Blended Opal / Satellite 50 | 1,007,674.43 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal UST/Sat 80 33/67 | 925,274.31 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Sat 50+ 15% cash | 769,232.25 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal_Satellite_20 | 590,860.61 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal_Muni_Sleeve | 550,823.07 | RULE_NOT_COUNTED | BY_MODEL opal_muni_sleeve @2026-10-07 | definition.model_name, definition.sleeve_name, roster.model_name |
| cottonwood | Opal_UST/Moderate Income Blend | 385,388.87 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal 15/85 Income Portfolio | 301,905.52 | NO_MEMBER | BY_MODEL opal_15_85_income_portfolio @2026-10-07 | definition.model_name, definition.sleeve_name, roster.model_name |
| cottonwood | Opal Satellite 90 | 217,082.33 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal 25/75 UST/ULT | 200,882.87 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | Opal Moderate Income | 192,694.43 | NO_MEMBER | BY_MODEL opal_moderate_income @2026-10-07 | definition.model_name, definition.sleeve_name |
| cottonwood | Opal - Beecherl Legg | 0.00 | NO_MEMBER | HOLDINGS 1 of 1 accts | definition.model_name, roster.model_name |
| cottonwood | OPAL INTERNATIONAL DIVIDEND INCOME ETF | None | NO_MEMBER | NONE | definition.component_name |
| cottonwood | Opal Conservative Growth | None | NO_MEMBER | NONE | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Intermediate-Term | None | NO_MEMBER | NONE | definition.model_name, definition.sleeve_name |
| cottonwood | Opal Ultra Short-Term Income | None | NO_MEMBER | NONE | definition.model_name, definition.sleeve_name |
| cottonwood | POLEN DIVIDEND INCOME ETF | None | NO_MEMBER | NONE | definition.component_name |
