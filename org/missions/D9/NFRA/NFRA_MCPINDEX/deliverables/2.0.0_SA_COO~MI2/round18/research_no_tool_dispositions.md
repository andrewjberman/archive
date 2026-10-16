# NFRA_MCPINDEX round 18 RESEARCH -- disposition of the 43 rows with no tool planned

Author 2.0.0_SA_COO~MI2, 2026-10-16. Basis: OPLGTW classification files ~109/~110 (the `reason` field read per row) and the committed row files. Rule (CTO msg 34632): a named gap owner does not meet the line; each row is (a) a tool NFRA_OPLGTW owes, or (b) not a served surface, ruled out with its reason. Row names are catalog entry names (file stem). Andrew's scope already excludes platinum/advi/ and platinum/irpt/ (MX-c-30).

## (a) a tool NFRA_OPLGTW owes (11 rows)

| row | why |
|---|---|
| `opal_data_portal_v2_served_correlation_data` | live served dataset, read by pages only; no tool |
| `opal_data_portal_v2_served_etf_returns` | live served dataset (page rows mp.04-06); no tool |
| `opal_data_portal_v2_served_factor_tilts` | live served dataset, read by pages only; no tool |
| `opal_data_portal_v2_served_model_portfolio_timeseries` | live served dataset (page rows mp.04-06); no tool |
| `opal_data_portal_v2_served_model_portfolios_views` | live served dataset; no tool |
| `opal_data_portal_v2_served_peer_performance` | live served monthly dataset (page row mp.07); no tool |
| `opal_data_portal_v2_served_trending_latest` | live served dataset; news_market_mood reads a different object |
| `dynamodb_dynamodb_market_updates` | authored market updates; a read of the Opal-internal table |
| `dynamodb_dynamodb_opal_harvest_articles` | harvest article items per security (declared; confirm the table holds items before the tool is built) |
| `dynamodb_dynamodb_opal_harvest_security_metrics` | harvest per-ticker metrics by axis and date |
| `dynamodb_dynamodb_semantic_news_trending_daily` | semantic themes per day; sibling of the trending tool |

## (b) not a served surface, ruled out of the finish line (32 rows)

| row | reason |
|---|---|
| `dynamodb_dynamodb_seeking_alpha_article_urls` | ingest plumbing: discovered article ids per run day; no reader needs it |
| `dynamodb_opal_tickets` | Opal-internal ticket app table (opal-tickets); not a research surface |
| `dynamodb_opal_trade_submissions` | client trade submissions; account-grain, needs its own never-widen grant |
| `opal_data_etfs_config_etf_universe` | the CRO spec proposes no tool for the universe config (folds it into the NAV tool's ticker enum; a hand-maintained config, not a served read) |
| `opal_data_etfs_silver_bbg_characteristics` | the CRO spec proposes no tool for the Bloomberg characteristics table (existing etfs_get_positioning verdict keep) |
| `opal_data_etfs_silver_bbg_constituents_issuer_fill` | the CRO spec proposes no tool for the issuer-fill copy of silver/holdings (existing etfs_get_positioning verdict keep) |
| `opal_data_etfs_silver_bbg_history_topup` | the CRO spec proposes no tool for the security price history top-up (existing etfs_get_positioning verdict keep) |
| `opal_data_etfs_silver_bloomberg_etf_holdings` | a rival-funds silver that is the input of gold canonical_shape; the CRO G5r spec serves the rival holdings from canonical_shape, so this silver has no tool of its own |
| `opal_data_etfs_silver_bloomberg_history_gaps` | the CRO spec proposes no tool: a single unattributed ops artifact (producer not attributed) |
| `opal_data_etfs_silver_etf_history_csv` | the CRO spec proposes no tool: a CSV duplicate of netassets_daily.parquet (read the parquet) |
| `opal_data_etfs_silver_issuer_site_holdings` | a rival-funds silver that is the input of gold canonical_shape; the CRO spec proposes no tool for it, and G5r serves the rival holdings from canonical_shape |
| `opal_data_etfs_silver_netassets` | superseded: the CRO spec names silver/netassets_daily as the one-read backing for NAV ranges since 2026-07-09, and the merged etfs_get_fund_nav_history reads that daily table |
| `opal_data_mdpf_feeds_etf_net_assets` | CRO G4 section 3.2: contracted with no new tool; the G5 fund-NAV tool reads the issuer silver this feed copies (G5 owns it) |
| `opal_data_mdpf_feeds_model_aua_positions_49financial` | account-grain client data (catalog fork_keys account); CRO G4 proposes mdpf_get_account_model_aua, which needs its own role and never-widen grant; catalog row retired=True |
| `opal_data_mdpf_feeds_model_aua_positions_inflection` | account-grain client data (catalog fork_keys account); CRO G4 proposes mdpf_get_account_model_aua, which needs its own role and never-widen grant; catalog row retired=True |
| `opal_data_mdpf_feeds_non_model_aua` | catalog row retired=True; the 49F feed is a superseded v0_9 method, do-not-serve (G4 section 3); the inflection values are already served by mdpf_get_aggregate_aua |
| `opal_data_mdpf_feeds_partner_held_etf_49financial` | catalog row retired=True; the DIVZ value is rolled forward from an RPS dated 2026-07-23 (do-not-serve, G4 section 3); G5 holds the current figure |
| `opal_data_mdpf_gold_ai_classified_securities` | CRO G4 section 3.3 open item: its tool reads the canonical DynamoDB etf-classifications table outside this bucket; this index is provenance only |
| `opal_data_news_av_silver_seeking_alpha` | raw scraped silver (one JSON per article); not a served read |
| `opal_data_news_v2_gold_semantic_clusters` | 17-40 MB per-day json, 160 trading days behind (NOT CURRENT); frozen producer |
| `opal_data_portal_v2_platinum_advi_49financial_perfrp` | client account-level PII (account keys, relationship and advisor names); catalog platinum/advi NOT YET; CRO G3 section 3.4 does not propose it |
| `opal_data_portal_v2_platinum_advi_49financial_twins` | client-derived ADVI data (PII); catalog platinum/advi NOT YET; CRO G3 section 3.4 does not propose it |
| `opal_data_portal_v2_platinum_mdpf_cottonwood_account_units` | catalog DENY or held (G3 section 2.5 row mp.12); no CRO tool proposal |
| `opal_data_portal_v2_platinum_mdpf_manifests_and_archive` | ops manifests and frozen archive snapshots, provenance only (G3 section 2.5); no CRO tool proposal |
| `opal_data_portal_v2_platinum_mdpf_non_model_assets` | catalog DENY or held (G3 section 2.5 row mp.11); no CRO tool proposal |
| `opal_data_portal_v2_served_benchmark_returns` | held at Andrew (catalog held_at_andrew, G3 section 2.5); no CRO tool proposal |
| `opal_data_portal_v2_served_cma_assumptions` | annual edition, frozen by design (G3 section 2.3 row cma.01); no CRO tool proposal |
| `opal_data_portal_v2_served_cma_views` | frozen 190 trading days with no refresh (G3 section 2.3 row cma.02); no CRO tool proposal |
| `opal_data_portal_v2_served_keyword_history` | catalog DENY (G3 section 2.5); 720 frozen objects since 2026-04-07 with 0 page callers |
| `opal_data_portal_v2_served_market_all_returns_legacy` | catalog DENY; fallback leg only, frozen 128 trading days (G3 section 2.3 row mkt.02) |
| `opal_data_portal_v2_served_portfolios_legacy` | legacy firm-partitioned json/portfolios tree, frozen 57-58 trading days, consumer gone (G3 section 2.2, row ft.04) |
| `opal_data_portal_v2_served_smartx_model_performance` | catalog DENY; frozen 94 trading days (G3 section 2.5) |

## Amendments (2026-10-16 ~03:0xZ, 2.0.0_SA_COO~MI2)

- CTO ruling @32a4dd88dd (msg 34656): 29 of the 32 ratified. `opal_data_portal_v2_served_benchmark_returns` is HELD AT ANDREW (excluded, reason class `held_at_andrew`, reopens on his word). Two of the 32 (`..._platinum_advi_49financial_perfrp`, `_twins`) were already removed by MX-c-30. The 28 landed by MX-c-38 are listed in `entity_exclusions.json`.
- `opal_data_portal_v2_served_cma_assumptions` moves to (a): measured the served object is the 2026 year edition (row freshness, claim measured) and `getCMAAssumptions` in `portal/src/api/portal-proxy.ts` is called by the CapitalMarketAssumptions page.
- `opal_data_mdpf_gold_ai_classified_securities` leaves (b): no tool in the gateway code reads the DynamoDB `etf-classifications` table (DATA_CATALOG.yaml names it only as existing and "not censused by any group"). The TABLE goes to (a): it needs a census row and a tool from NFRA_OPLGTW.
- (a) is now 13 rows (11 + cma_assumptions + ai_classified_securities) plus the uncensused `etf-classifications` table. `2.0.0_SA_COO~O` (msg 34657) measured three of the original 11 as not servable by the line: `opal_harvest_articles` (table empty, 0 items since 2026-09-11, catalog says do not serve), `market_updates` (183 trading days behind), `semantic_news_trending_daily` (160 days behind); it routed the other 8 to the CTO for a PRD addendum. The three are NOT excluded until the CTO rules.
