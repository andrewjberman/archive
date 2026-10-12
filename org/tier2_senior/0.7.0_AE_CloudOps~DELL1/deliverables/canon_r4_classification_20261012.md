# ADHOC.canon-r4-code-deploy -- classification of every non-EQUAL name (leg e, read only)

Author: 0.7.0_AE_CloudOps~DELL1, 2026-10-12 ~17:45Z. Nothing is deployed from this table.
Input: `canon_r4_equality_AFTER_20261012.out` (trees 5, files 77, equal 44, not equal 33; BEFORE was 41 / 36, the
difference is exactly the three D1 names, which read EQUAL). Runner chain read from
`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh`, the accrual bridge from
`infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf`, imports by reading the scripts.

BASIS AND LIMIT: a name is RUNNER MEMBER when the dispatch (or the accrual bridge's SSM fire) executes it, or a script
those execute imports or opens it. Imports were read with the native search over `data/mdpf` and `infra/aws`; a lazy
import inside a function body or a path built at run time would not show, so a NOT A MEMBER below is "no reader found
in those two trees", not a proof of absence.

Counts: RUNNER MEMBER 8 | NOT A MEMBER 25 | total 33.

## RUNNER MEMBERS that differ (each is a deploy of its own, possibly moving served output, and takes its own pair)

| tree | state | name | reason |
|---|---|---|---|
| gold | DIFFER | build_portal_gold_accrual.py | executed on the runner by mdpf-accrual-trigger (SSM sync fire), not by the dispatch |
| gold | DIFFER | mdpf_model_registry.json | opened by pull_orion_model_composition.py, the WS-C feeder (dispatch:346) and mdpf_aggregate_aua.py (dispatch:407) |
| gold | DIFFER | taxsma_assets.py | imported by dim_mdpf_aggregate_aua_timeseries.py, which the dispatch uses as its library (:157, :605) |
| backfill | DIFFER | build_legacy_compat_emit.py | named by the dispatch (:417) |
| config | DIFFER | bronze_homes.json | opened by pull_orion_model_composition.py and the WS-C feeder; differs because the FIRMBKTS act-4 flip regenerated it (amendment 1: FIRMBKTS's change, reported as a fact) |
| config | MISSING_ON_S3 | partner_roster.json | opened by dim_mdpf_account_distribution.py and dim_mdpf_aggregate_aua_timeseries.py, both dispatch-run |
| gold | EXTRA_ON_S3 | partner_roster.json | same readers; an S3-only copy with no repo twin at that path, so equality is not measurable by this tool |
| gold | EXTRA_ON_S3 | _trading_day_calendar.py | imported by build_mdpf_etf_ownership_timeseries.py, which the dispatch names; S3-only, no repo twin |

## NOT A MEMBER

| tree | state | name | reason |
|---|---|---|---|
| gold | DIFFER | taxsma_reconcile.py | imported by the consolidator, taxsma_sources.py and tests; the dispatch names none of them |
| gold | MISSING_ON_S3 | dim_mdpf_aum_timeseries.py | no reference in the dispatch, build_package.py, infra/aws or data/mdpf |
| gold | MISSING_ON_S3 | gold_validate_config.yaml | a comp-validate QA config, named only in a usage docstring |
| gold | MISSING_ON_S3 | mdpf_gold_backfill.py | gold lambda package module; not in the dispatch |
| gold | MISSING_ON_S3 | mdpf_gold_parquet.py | gold lambda package module; not in the dispatch |
| gold | MISSING_ON_S3 | mdpf_name_discovery_declared.json | opened only by mdpf_name_discovery.py, which only its own test imports |
| gold | MISSING_ON_S3 | mdpf_revamp_count_source_audit.py | no reference found in the dispatch, package or either tree |
| gold | MISSING_ON_S3 | taxsma_prelude_run.py | a local CLI (usage `py -3.12 ... --grid`), not in the dispatch or the package |
| gold | MISSING_ON_S3 | tests/test_global_fold_flag2.py | a test |
| gold | MISSING_ON_S3 | tests/test_mdpf_bronze_homes.py | a test |
| gold | MISSING_ON_S3 | tests/test_mdpf_gold_backfill.py | a test |
| gold | MISSING_ON_S3 | tests/test_mdpf_gold_parquet.py | a test |
| gold | MISSING_ON_S3 | verify_mdpf_revamp_conditions.py | a QA verify tool; the dispatch does not name it |
| gold | EXTRA_ON_S3 | trading_calendar.py | S3-only; no dispatch-named script in the gold tree imports it by name (the lambda package ships lib/trading_calendar.py under this name) |
| backfill | DIFFER | HANDOFF_AE_lambda_route.md | a doc |
| backfill | MISSING_ON_S3 | build_mdpf_inflection_history_from_spine.py | a by-hand backfill CLI (usage docstring); the dispatch names none of the backfill CLIs below |
| backfill | MISSING_ON_S3 | build_mdpf_wsc_inflection_nonmodel_backfill.py | a by-hand backfill CLI; listed as an orphan in infra/aws/globgrph/comp_debt_baseline.json |
| backfill | MISSING_ON_S3 | patch_mdpf_per_date_partitions.py | a by-hand patch CLI; listed as an orphan in the same baseline |
| backfill | EXTRA_ON_S3 | .crosswalk_cache.pkl | an S3-only cache artifact; no reader found |
| backfill | EXTRA_ON_S3 | HANDOFF_AE_lambda_route.diff | an S3-only handoff diff |
| backfill | EXTRA_ON_S3 | aggregate_aua_count_backfill_pre0518.json | an S3-only backfill data file; no reader found |
| backfill | EXTRA_ON_S3 | build_custody_crosswalk_cache.py | an S3-only script; the dispatch does not name it |
| feeders | DIFFER | HANDOFF_DSA_wsd2_aggregator_wire.md | a doc |
| feeders | MISSING_ON_S3 | wsc_inflection_held_etf.py | the dispatch's feeder steps are wsb_49f_smartx_model_aua.py, gold/build_mdpf_wsc_inflection_feeder.py and wsd_partner_held_etf.py; this is none of them |
| config | MISSING_ON_S3 | route_bindings_tieout.py | the W-1 read-only tie-out validator CLI |

## What this table does and does not say

- It deploys nothing and proposes no deploy: the eight RUNNER MEMBER rows are the issuer's to carry to the CTO, each
  with its own never-widen pair.
- `mdpf_model_registry.json` and `partner_roster.json` are the two rows most likely to move served output, since the
  WS-A/WS-C/WS-D legs and the account-distribution producers read them on every dispatch.
- EXTRA_ON_S3 rows have no repo twin at their path, so "equal" cannot be measured for them by
  `mdpf-code-equality.py`; that is a limit of the tool, not a finding about the objects.
