# ECLIPSE (INFLECTION) SLEEVE-NAME CENSUS -- MDPF_STRATID TO-ST-t4

Author: `0.9.0_WK_MDPF_STRATID~3`. Read-only (S3 GetObject / List). Nothing built, no code edited. Read 2026-10-08.

SOURCE: s3://opal-data-assets/eclipse/inflection/silver/{fact_models,fact_model_composition,fact_portfolios_full,fact_portfolios_simple}/date=YYYY-MM-DD/data.parquet -- latest partition date=2026-10-08 (fact_models 18 rows, fact_model_composition 9 rows, fact_portfolios_full 863 rows, fact_portfolios_simple 846 rows) read in full; earlier partitions: ALL 132 partitions per table, 2026-05-15 through 2026-10-08 (528 partition reads in total), scanned for the same name columns. Bronze cross-check, one object: s3://opal-data-assets/eclipse/inflection/bronze/2026-10-08/model_composition_28.json (shows modelDetail.children are Security Set names).

DENOMINATOR: 1363

RESULT: NONE-FOUND

Reading the lines above. DENOMINATOR is the count of DISTINCT name strings on the latest date (2026-10-08) pooled over every name column listed in the next section. Over all 132 partitions the distinct pool is 1418. RESULT is NONE-FOUND for tickers and full fund names: of the 1363 latest names (1418 over history), zero contains `DIVZ`, `IDVZ`, `PFDE` or `PFOE` as a whole word (case-insensitive, boundary = not letter/digit), and zero contains "Pathfinder Disciplined" or "Pathfinder Focused Opportunit". This is a zero over a stated pool, not an absence of Opal ETF sleeves: the Eclipse silver tables hold no holdings or sleeve-composition lines (see "Not read"). The ETF list used is `s3://opal-data-etfs/config/etf_universe.json` as read today: DIVZ, IDVZ, PFDE, PFOE (4 tickers, last_updated 2026-06-23).

## Where the names live (columns scanned, distinct names on 2026-10-08)

| table | column | distinct names |
|---|---|---|
| fact_models | name | 18 |
| fact_models | description | 17 |
| fact_model_composition | name | 9 |
| fact_model_composition | description | 2 |
| fact_model_composition | modelDetail (JSON; model name and every `children[].name`, recursive) | 11 |
| fact_portfolios_full | model (the model name each portfolio sits under) | 18 (one is blank: the 17 sleevePortfolio=1 rows) |
| fact_portfolios_full | name (portfolio/client account name) | 861 |
| fact_portfolios_simple | name | 846 |
| fact_portfolios_simple | accountName | 459 |

The sum of the column counts exceeds 1363 because the same string appears in several columns; 1363 is the pool after de-duplication. `fact_portfolios_full.model` and `fact_models.name` / `fact_model_composition.name` are the Eclipse MODEL names (the nearest Eclipse thing to a sleeve); the 17 rows with `sleevePortfolio=1` carry a client name in `name` and a blank `model`, so no sleeve name beyond a client name exists there.

## Matches

Ticker matches: 0. Full-name matches: 0. Opal-only matches (name contains "Opal", no ticker, no fund full name): listed below, so a reader can judge. 13 names on the latest date, 20 over history. "Opal Dividend Income" and any "Opal" + fund word of that form: not present. The nearest is `Opal DIV SMA` (contains `DIV` but not the whole word `DIVZ`).

| name | match | dollars / accounts on 2026-10-08 | column the name came from |
|---|---|---|---|
| Opal Intermediate Growth | Opal-only | $78,008,756.28 / 218 accounts (portfolios_full totalValue); model AUM $83,637,728.61 (composition) | fact_model_composition.name, fact_portfolios_full.model |
| 50/50 Opal Intermediate/Opal Long Term | Opal-only | $35,492,967.56 / 165 | fact_models.name, fact_model_composition.name, fact_portfolios_full.model |
| Opal Long Term | Opal-only | $14,180,649.40 / 94 (composition modelAUM $15,487,124.40) | fact_model_composition.name, fact_portfolios_full.model, modelDetail child |
| 50/50 Opal Short Term/Intermediate | Opal-only | $7,700,352.95 / 24 | fact_model_composition.name, fact_portfolios_full.model |
| Opal Short Term | Opal-only | $5,809,037.58 / 29 (composition modelAUM $7,512,031.92) | fact_model_composition.name, fact_portfolios_full.model, modelDetail child |
| 90/10 Opal Long Term/Ultra Short Term | Opal-only | $4,124,259.05 / 4 | fact_portfolios_full.model only (not in fact_models or fact_model_composition) |
| Opal Ultra Long Term | Opal-only | $2,268,181.71 / 33 | fact_model_composition.name, fact_portfolios_full.model, modelDetail child |
| Opal Ultra Short Term | Opal-only | $2,035,893.55 / 15 (composition modelAUM $3,288,754.27) | fact_model_composition.name, fact_portfolios_full.model, modelDetail child |
| 90/10 Opal Intermediate/Ultra Short Term | Opal-only | $617,256.11 / 1 | fact_portfolios_full.model only |
| Opal Growth SMA | Opal-only | $0.00 / 0 (composition modelAUM 0.00; no portfolios_full model row) | fact_model_composition.name |
| Opal DIV SMA | Opal-only | $0.00 / 0 (composition modelAUM 0.00; no portfolios_full model row) | fact_model_composition.name, modelDetail child |
| Opal Intermediate | Opal-only (Security Set name) | not a model; child of the two 50/50 models and of Opal Intermediate Growth | fact_model_composition.modelDetail child |
| Opal Global SMA | Opal-only (Security Set name) | not a model; child of Opal Growth SMA | fact_model_composition.modelDetail child |

Names that existed earlier and are absent on 2026-10-08 (Opal-only, no dollars today): `50/50 OPAL INT/OPAL LTC` and `50/50 OPAL ST/INT` (models, 2026-05-15 to 2026-06-07, 19 partitions each); Security Set names `Opal Int`, `Opal LTA`, `Opal LTC`, `Opal ST`, `Opal UST` (2026-05-15 to 2026-06-07).

Dollar basis: `fact_portfolios_full.totalValue` summed over `isDeleted != True` rows grouped by `model` (863 rows, 0 deleted), and `fact_model_composition.modelAUM` where given. The two bases disagree for some models; both are shown, neither is reconciled here.

Other non-Opal names seen in the model columns, for completeness: 13 `IWM ...` models (fact_models) and `PCOFX` (a mutual fund ticker, sleeveCount 1, 0 portfolios). `PCOFX` is not on the Opal ETF list.

## Not read (stated blindness, not a zero)

1. Holdings. No Eclipse silver table read here carries per-portfolio or per-sleeve security holdings. A client sleeve whose NAME is a client name but which HOLDS DIVZ/IDVZ/PFDE/PFOE is invisible to this census. `fact_model_composition` carries only the model's Security Set children (11 distinct names), not tickers.
2. Sleeve names. The 17 `sleevePortfolio=1` portfolios (on 2026-10-08, $10,282,708.36 in total) have a client name and a blank model; their parent-model link was not read, and no separate sleeve-name column exists in the four tables.
3. Bronze beyond one object. Bronze `portfolios_full.json`, `portfolios_simple.json` and `models.json` for 2026-10-08 exist but were not read separately; silver is derived from them. `eclipse/inflection/reconstructed/`, `_history/`, `_meta/` and `eclipse_membership_map/` under bronze were listed, not read.
4. Description columns hold free text; they were scanned (fact_models.description 17 names, fact_model_composition.description 2) and held no match.
5. The Opal-ETF list is a one-object read dated 2026-06-23; a ticker added after that date to `etf_universe.json` would be read here (the file was read today), but a ticker not yet in the file is not covered.
6. Client-name columns (portfolio name, accountName) were scanned by pattern only; no client name is reproduced in this document.
