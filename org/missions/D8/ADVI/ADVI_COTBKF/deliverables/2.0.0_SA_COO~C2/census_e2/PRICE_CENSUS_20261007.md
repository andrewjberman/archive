# Commonwealth price census, round 4 (2026-10-07T10:14Z)

40 of 40 buckets graded: 35 USABLE, 5 BARRED. Calls made under a BARRED bucket (counted by a client wrapper): 0. Nothing was written to S3.

Universe: 4634 distinct non-blank CUSIPs from silver transactions s3://opal-data-assets/commonwealth/cottonwood/silver/transactions/date=2026-06-23/. Needed days are an UPPER BOUND (every NYSE trading day from each CUSIP's first Trade_Date through 2026-06-23).

Union across USABLE stores: priced on any day 1720 of 4634 securities; 1297651 of 9388961 security-days covered (13.8%).

## Every bucket

| bucket | grade | firm | stores read | securities priced | what it holds |
|---|---|---|---|---|---|
| opal-313476888478-globgrph | USABLE | (none) | - | 0 | 14 top-level prefixes, 3 root objects: archive/, build-source/, c3materialize-b4/, code/, contract_integrity/, contracts/, cse-seed/, producers/, projection/, served/, snapshots/, stitch-source/, stitch/, warehouse/ |
| opal-313476888478-lambda-artifacts | USABLE | (none) | - | 0 | 39 top-level prefixes, 0 root objects: bd-pipeline/, cot-pipeline/, data-refresh/, deck-generation-pipeline/, demov1/, drift-producer/, ec2/, etfs-canon/, etfs-netassets/, etfs-positioning/, exec-summary/, fred-pipeline/, globgrph/, harvest/, imo-pipeline/, inf-pipeline/, investor-reporting/, lambda/, layers/, market-overview/, mdpf-pipeline/, mdpf-secclass/, news-pipeline/, opal-assets/, opsec/, partners-api/, portal-auth/, portal-content/, portfolio-management/, research/, security-scanner-pipeline/, shared-infra/, smartx-pipeline/, surface-check/, ticket-center/, trade-pipeline/, workflows/, yang-pipeline/, ycharts-pipeline/ |
| opal-313476888478-lambda-layers | USABLE | (none) | - | 0 | 0 top-level prefixes, 13 root objects: (empty) |
| opal-313476888478-terraform-state | USABLE | (none) | - | 0 | 73 top-level prefixes, 0 root objects: aaii-v2-bucket-lifecycle/, amgt-resapp/, analytics-dashboard/, astn-pipeline/, bd-49f-auto-login/, bd-bucket-lifecycle/, bd-pipeline/, bloomberg-tunnel/, c3materialize-b4/, canonical-schwab-ec2/, canonical-schwab-si2-schedule/, compdiff-cot-value-parity/, compdiff-inf-value-parity/, compdiff-served-guard-49f/, compdiff-served-guard-cot/, compdiff-served-guard-inf/, consolidation-gold-runner/, cot-pipeline/, crawl-harness/, daily-sprint-generator/, data-refresh/, deck-generation-pipeline/, ec2-auto-shutdown-enforcer/, estate-report/, etfs-canon/, etfs-netassets/, etfs-positioning/, etfs-reports/, etfs-rivalfunds/, exec-summary/, fred-pipeline/, github-actions-runner/, globgrph/, harvest/, imo-pipeline/, inf-pipeline/, inf-sentinel-deny/, investor-reporting/, lambda-layers/, market-overview/, mdpf-pipeline/, mdpf-secclass/, news-pipeline/, news-v2-bucket-lifecycle/, nfra-agentbus-alyssa01/, nfra-agentbus/, nfra-ctlpln-agentbus/, nfra-ctlpln-identity/, opal-assets-absence/, opal-assets/, opal-gateway/, opsec/, partner-etl-ops-alerts/, partner-firms/, partners-api/, portal-auth/, portal-content/, portal-notifications/, portfolio-management/, public-api-cdn/, ... |
| opal-313476888478-yang-qa-scratch | USABLE | (none) | - | 0 | 0 top-level prefixes, 0 root objects: (empty) |
| opal-cloudtrail-logs-313476888478 | USABLE | (none) | - | 0 | 1 top-level prefixes, 0 root objects: AWSLogs/ |
| opal-cur-313476888478 | USABLE | (none) | - | 0 | 1 top-level prefixes, 1 root objects: cur/ |
| opal-data-49financial | BARRED | 49financial | - | 0 | NOT OPENED (BARRED: a bucket of firm 49financial) |
| opal-data-assets | USABLE | (none) | - | 0 | 16 top-level prefixes, 0 root objects: _probe/, blackdiamond/, code/, commonwealth/, config/, eclipse/, gateway/, gold/, json/, orion/, pathfinder/, portal/, schwab/, smartx/, sprint/, trueshares/ |
| opal-data-astn | USABLE | (none) | - | 0 | 3 top-level prefixes, 0 root objects: digest/, email/, raw/ |
| opal-data-bd | BARRED | 49financial | - | 0 | NOT OPENED (BARRED: a bucket of firm 49financial) |
| opal-data-cot | USABLE | cottonwood | cottonwood-silver-canonical-prices, cottonwood-gold-canonical-holdings | 1717 | price stores read: cottonwood-silver-canonical-prices, cottonwood-gold-canonical-holdings |
| opal-data-cottonwood | USABLE | cottonwood | - | 0 | LIST FAILED: AccessDenied |
| opal-data-demo | BARRED | demo | - | 0 | NOT OPENED (BARRED: a bucket of firm demo) |
| opal-data-etfs | USABLE | (none) | rivalfunds-etfs-gold-security-market, etfs-bbg-testpull-ticker-history, etfs-bbg-fund-daily | 134 | price stores read: rivalfunds-etfs-gold-security-market, etfs-bbg-testpull-ticker-history, etfs-bbg-fund-daily |
| opal-data-harvest | USABLE | (none) | - | 0 | 24 top-level prefixes, 0 root objects: amgt/, barrons/, bloomberg/, crosswalk/, derived/, drafting/, filings/, ft/, identity/, issuer-site/, lib/, management/, packs/, peers/, posture/, publication-links/, publications/, raw/, scores/, sec/, seeking-alpha/, social/, universe/, wsj/ |
| opal-data-imo | USABLE | (none) | - | 0 | 7 top-level prefixes, 0 root objects: _probe/, archives/, code/, config/, corp/, serving/, telemetry/ |
| opal-data-inf | BARRED | inflection | - | 0 | NOT OPENED (BARRED: a bucket of firm inflection) |
| opal-data-inflection | BARRED | inflection | - | 0 | NOT OPENED (BARRED: a bucket of firm inflection) |
| opal-data-irpt | USABLE | (none) | - | 0 | 1 top-level prefixes, 0 root objects: irpt/ |
| opal-data-mdpf | USABLE | (none) | - | 0 | 5 top-level prefixes, 0 root objects: bmkaud-evidence/, code/, diagnostics/, mdpf/, telemetry/ |
| opal-data-news-av | USABLE | (none) | - | 0 | 2 top-level prefixes, 0 root objects: lambda-packages/, seeking-alpha/ |
| opal-data-news-v2 | USABLE | (none) | - | 0 | 10 top-level prefixes, 1 root objects: codebuild/, lambda-deployments/, lambda-packages/, layer3_package/, logs/, market_update/, rss_trending/, semantic_clusters/, tmp/, trending_reports/ |
| opal-data-pm | USABLE | (none) | - | 0 | 2 top-level prefixes, 0 root objects: PFDE/, PFOE/ |
| opal-data-portal-v2 | USABLE | (none) | portal-canon-return-daily-values | 0 | price stores read: portal-canon-return-daily-values |
| opal-data-portfolio | USABLE | (none) | - | 0 | 1 top-level prefixes, 0 root objects: PFDE/ |
| opal-data-security | USABLE | (none) | - | 0 | 1 top-level prefixes, 0 root objects: waf-logs/ |
| opal-data-security-access-logs | USABLE | (none) | - | 0 | 2 top-level prefixes, 0 root objects: evidence-store/, security-evidence/ |
| opal-data-trade-submissions | USABLE | (none) | - | 0 | 2 top-level prefixes, 0 root objects: parquet/, submissions/ |
| opal-data-transcripts | USABLE | (none) | - | 0 | 3 top-level prefixes, 0 root objects: _provisioning/, outlook/, teams/ |
| opal-data-ycharts | USABLE | (none) | - | 0 | 2 top-level prefixes, 0 root objects: firms/, research/ |
| opal-estate-report | USABLE | (none) | - | 0 | 8 top-level prefixes, 1 root objects: adjudicated/, code/, config/, daily/, logs/, manifest/, outset/, text-input/ |
| opal-infrastructure-snapshots | USABLE | (none) | - | 0 | 32 top-level prefixes, 0 root objects: 2026-09-06/, 2026-09-07/, 2026-09-08/, 2026-09-09/, 2026-09-10/, 2026-09-11/, 2026-09-12/, 2026-09-13/, 2026-09-14/, 2026-09-15/, 2026-09-16/, 2026-09-17/, 2026-09-18/, 2026-09-19/, 2026-09-20/, 2026-09-21/, 2026-09-22/, 2026-09-23/, 2026-09-24/, 2026-09-25/, 2026-09-26/, 2026-09-27/, 2026-09-28/, 2026-09-29/, 2026-09-30/, 2026-10-01/, 2026-10-02/, 2026-10-03/, 2026-10-04/, 2026-10-05/, 2026-10-06/, 2026-10-07/ |
| opal-mcp-athena-results | USABLE | (none) | - | 0 | 0 top-level prefixes, 0 root objects: (empty) |
| opal-mcp-audit | USABLE | (none) | - | 0 | 2 top-level prefixes, 0 root objects: _athena_cvo_verify/, audit/ |
| opal-runner-shared | USABLE | (none) | - | 0 | 1 top-level prefixes, 0 root objects: code/ |
| opal-security-evidence | USABLE | (none) | - | 0 | 2 top-level prefixes, 0 root objects: cases/, reports/ |
| opal-served-key-write-trail-logs | USABLE | (none) | - | 0 | 1 top-level prefixes, 0 root objects: AWSLogs/ |
| opal-website-backups | USABLE | (none) | - | 0 | 3 top-level prefixes, 0 root objects: backups/, code/, migration/ |
| opalinvest-portal | USABLE | (none) | - | 0 | LIST FAILED: AccessDenied |

## BARRED buckets (never opened) and the stores they are known to hold

- `opal-data-49financial` (firm 49financial): canonical_positions table (one data.parquet per date partition) under the firm's gold tree gold/advi
- `opal-data-bd` (firm 49financial): canonical_prices table (silver tier, one parquet object); historical_prices table (silver tier, one parquet object)
- `opal-data-demo` (firm demo): no price store known
- `opal-data-inf` (firm inflection): canonical_prices table (silver tier, one parquet object); historical_prices table (silver tier, one parquet object)
- `opal-data-inflection` (firm inflection): no price store known

## USABLE price stores read

| store | bucket | objects | priced any day | security-days covered | matched CUSIP / ticker | reused, not credited |
|---|---|---|---|---|---|---|
| cottonwood-silver-canonical-prices | opal-data-cot | 1 | 1263 | 1280457 | 0 / 1263 | 126 (120287 days) |
| cottonwood-gold-canonical-holdings | opal-data-cot | 130 | 1028 | 8644 | 1020 / 8 | 53 (461 days) |
| rivalfunds-etfs-gold-security-market | opal-data-etfs | 7 | 56 | 0 | 56 / 0 | 0 (0 days) |
| etfs-bbg-testpull-ticker-history | opal-data-etfs | 173 | 122 | 110204 | 0 / 122 | 16 (10602 days) |
| etfs-bbg-fund-daily | opal-data-etfs | 32 | 0 | 0 | 0 / 0 | 0 (0 days) |
| portal-canon-return-daily-values | opal-data-portal-v2 | 8 | 0 | 0 | 0 / 0 | 0 (0 days) |

## Union by asset type

| asset type | securities | priced any day | priced in window | days covered | days needed |
|---|---|---|---|---|---|
| Alternative Investment | 22 | 1 | 1 | 11 | 25305 |
| Annuity | 29 | 0 | 0 | 0 | 60198 |
| Cash | 3 | 1 | 1 | 593 | 8682 |
| Cash Equivalent | 488 | 54 | 51 | 6283 | 482359 |
| ETF | 349 | 276 | 273 | 259474 | 610978 |
| Equity | 1830 | 934 | 923 | 860664 | 4033672 |
| Fixed Income | 778 | 184 | 184 | 2012 | 1749889 |
| Mutual Fund | 978 | 237 | 227 | 160020 | 2015941 |
| Mutual Fund (Closed End) | 99 | 33 | 32 | 8594 | 233016 |
| Unit Investment Trust | 58 | 0 | 0 | 0 | 168921 |

A price counted here may be a carried-forward, interpolated, transaction-observed or custodian-mark value; the JSON carries each store's `by_source` split. No vendor was called.
