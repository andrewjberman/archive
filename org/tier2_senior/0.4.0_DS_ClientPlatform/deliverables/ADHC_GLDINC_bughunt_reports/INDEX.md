# ADHC_GLDINC bug-hunt -- per-agent report index

Raw per-agent outputs from workflow `wf_ebf64891-fcd` (fan-out). 46 review + 24 verify = 70 agents, one file each in this folder. NOT triaged/aggregated -- these are the granular agent reports for reference; aggregation + fix-planning comes after.

## Review agents (one per script)
| file | verdict | findings (C/H/M/L) | runs_in_incremental |
|---|---|---|---|
| review_INF_09.generate_partner_analytics.py.md | issues-found | 0/0/0/1 | True |
| review_INF_A_-1.materialize_txn_cache.py.md | issues-found | 0/1/1/1 | False |
| review_INF_A_00.accounts_dimension.py.md | issues-found | 0/0/2/0 | False |
| review_INF_A_01.advisor_assignments.py.md | issues-found | 0/0/1/2 | False |
| review_INF_A_02.fee_rate_history.py.md | clean | 0/0/0/0 | False |
| review_INF_A_03.positions_cube.py.md | issues-found | 0/0/1/1 | False |
| review_INF_A_04.client_dimension.py.md | issues-found | 0/1/0/1 | False |
| review_INF_B_00.canonical_holdings.py.md | issues-found | 0/0/2/2 | False |
| review_INF_B_01.holdings_lots.py.md | issues-found | 0/1/1/2 | False |
| review_INF_B_01b.classify_new_securities.py.md | clean | 0/0/0/0 | False |
| review_INF_B_02.canonical_lots.py.md | issues-found | 0/1/3/1 | False |
| review_INF_B_03.account_gains.py.md | issues-found | 0/1/1/2 | False |
| review_INF_C_00.canonical_performance.py.md | issues-found | 0/1/1/1 | False |
| review_INF_C_01.canonical_nna.py.md | issues-found | 1/1/2/1 | False |
| review_INF_C_01b.role_aua_backfill.py.md | issues-found | 0/1/0/0 | False |
| review_INF_C_02.client_performance.py.md | issues-found | 0/0/1/1 | False |
| review_INF_C_03.account_performance.py.md | issues-found | 1/0/0/1 | False |
| review_INF_C_04.validate_aua.py.md | issues-found | 0/0/2/1 | False |
| review_INF_C_05.client_tax_liability.py.md | issues-found | 0/0/2/0 | False |
| review_INF_C_06.client_mix_timeseries.py.md | issues-found | 0/0/0/1 | False |
| review_INF_C_07.advisor_attribution.py.md | issues-found | 0/1/0/1 | False |
| review_INF_C_08.advisor_fee_efficiency.py.md | issues-found | 0/0/2/2 | False |
| review_INF_C_09.fee_status_audit.py.md | issues-found | 0/0/0/2 | False |
| review_INF_D_00.portal_aggregates.py.md | issues-found | 1/0/0/0 | True |
| review_INF_D_00b.portal_timeseries.py.md | issues-found | 0/0/0/2 | True |
| review_INF_D_00c.portal_leaderboard.py.md | issues-found | 0/0/0/2 | True |
| review_INF_D_00d.cumulative_chart.py.md | issues-found | 0/0/1/2 | True |
| review_INF_D_00f.advisor_nna_canonical.py.md | issues-found | 0/1/1/0 | True |
| review_INF_D_02.advisor_client_detail.py.md | issues-found | 0/0/0/2 | True |
| review_INF_D_02b.top_holdings.py.md | issues-found | 0/1/2/0 | True |
| review_INF_D_02c.client_directory.py.md | issues-found | 0/0/0/1 | True |
| review_INF_D_02d.firm_mix_summary.py.md | issues-found | 0/0/3/0 | True |
| review_INF_D_03.composition_artifacts.py.md | issues-found | 0/0/2/1 | True |
| review_INF_D_04.client_portal_summary.py.md | issues-found | 1/0/1/0 | True |
| review_INF_D_04b.client_publishers.py.md | issues-found | 0/1/3/1 | True |
| review_INF_D_05.activity_scan.py.md | issues-found | 0/0/0/2 | False |
| review_INF_D_05.client_top_holdings.py.md | issues-found | 1/0/1/1 | False |
| review_INF_D_06.cash_drag.py.md | issues-found | 0/0/1/3 | False |
| review_INF_D_06.client_timeseries.py.md | issues-found | 0/2/0/0 | False |
| review_INF_D_07.concentration_risk.py.md | issues-found | 0/1/0/2 | False |
| review_INF_D_07a.firm_concentrations.py.md | clean | 0/0/0/0 | False |
| review_INF_D_08.nmec_nmnc_nna.py.md | issues-found | 1/0/2/1 | False |
| review_INF_D_09.account_timeseries.py.md | issues-found | 0/0/2/2 | True |
| review_INF_E_00.eclipse_model_portfolios.py.md | issues-found | 0/1/3/0 | True |
| review_INF_build_canonical_prices.py.md | issues-found | 0/0/1/2 | False |
| review_INF_run_c_chain.py.md | issues-found | 1/1/1/0 | False |

## Verify agents (one per adversarial check of a material finding)
| file | target | is_real | confidence | corrected_sev |
|---|---|---|---|---|
| verify_01_INF_B_01.holdings_lots.md | INF_B_01.holdings_lots.py | True | confirmed | high |
| verify_02_INF_B_02.canonical_lots.md | INF_B_02.canonical_lots.py | True | confirmed | high |
| verify_03_unknown.md | unknown | False | refuted | low |
| verify_04_unknown.md | unknown | True | confirmed | high |
| verify_05_unknown.md | unknown | True | confirmed | high |
| verify_06_unknown.md | unknown | True | confirmed | high |
| verify_07_INF_B_03.account_gains.md | INF_B_03.account_gains.py | True | confirmed | high |
| verify_08_INF_A_00.accounts_dimension.md | INF_A_00.accounts_dimension.py | True | confirmed | high |
| verify_09_unknown.md | unknown | True | confirmed | high |
| verify_10_INF_C_01b.role_aua_backfill.md | INF_C_01b.role_aua_backfill.py | True | confirmed | medium |
| verify_11_INF_C_00.canonical_performance.md | INF_C_00.canonical_performance.py | False | refuted | low |
| verify_12_INF_C_07.md | INF_C_07.py | False | refuted | low |
| verify_13_unknown.md | unknown | True | confirmed | high |
| verify_14_INF_D_02b.top_holdings.md | INF_D_02b.top_holdings.py | True | confirmed | medium |
| verify_15_INF_B_00.canonical_holdings.md | INF_B_00.canonical_holdings.py | True | plausible | medium |
| verify_16_INF_D_04.client_portal_summary.md | INF_D_04.client_portal_summary.py | True | confirmed | high |
| verify_17_unknown.md | unknown | False | refuted | low |
| verify_18_INF_B_01.holdings_lots.md | INF_B_01.holdings_lots.py | True | confirmed | high |
| verify_19_INF_run_c_chain.md | INF_run_c_chain.py | True | confirmed | low |
| verify_20_INF_D_06.client_timeseries.md | INF_D_06.client_timeseries.py | True | confirmed | high |
| verify_21_INF_B_00.canonical_holdings.md | INF_B_00.canonical_holdings.py | True | confirmed | high |
| verify_22_INF_run_c_chain.md | INF_run_c_chain.py | False | refuted | low |
| verify_23_unknown.md | unknown | False | refuted | low |
| verify_24_unknown.md | unknown | False | refuted | low |