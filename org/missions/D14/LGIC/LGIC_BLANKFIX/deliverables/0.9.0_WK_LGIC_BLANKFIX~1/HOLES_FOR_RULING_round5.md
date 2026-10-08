# Holes for ruling -- round 5 (LGIC_BLANKFIX, BF-s-5)

Source: `sort_holes.py`, run over every root of `infra/logic/registry/root_map.json`; the lines are in `HOLES_SORTED_round5.txt`. One row per DISTINCT (type, name); `lines` is how many hole lines that name closes. Bucket is the one the check read, `-` where it read none. This file states facts and asks; it proposes no name.

## carded (S1): 22 lines, 15 distinct names

Ask: S1 -- for each name: its whole correct name, or that none is owed, with the reason.

| type | name | root | where | bucket read | what the line says is missing | lines |
|---|---|---|---|---|---|---|
| S3Key | `_quarantine/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-silver-bd49finsurance/silver_registry.py:49; infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/silver_registry.py:49; infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/silver_registry.py:38; infra/aws/lambda/opal-assets/opal-assets-silver-etf/silver_registry.py:49; infra/aws/lambda/opal-assets/opal-assets-silver-orion/silver_registry.py:38; infra/aws/lambda/opal-assets/opal-assets-silver-schwab/silver_registry.py:49 | - | skipped by a card; the card gives no correct name and does not say none is owed | 6 |
| S3Key | `blackdiamond/49f/_ops/probe/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py:72 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `blackdiamond/49f/_ops/pull_state.json` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py:74 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `blackdiamond/49f/_ops/taxsma_roster.json` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/taxsma_registry.py:27 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `blackdiamond/cot/session-trigger-mode.json` | cot-pipeline | infra/aws/lambda/cot-pipeline/cot-bd-session-trigger/lambda_function.py:38 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `blackdiamond/cottonwood/meta/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py:417 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `blackdiamond/cottonwood/meta/templates/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:163 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `forwardfill_v2/` | investor-reporting/performance, opal-assets | infra/aws/lambda/investor-reporting/performance/tenants.py:164; infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:142 | - | skipped by a card; the card gives no correct name and does not say none is owed | 2 |
| S3Key | `investor-reporting/directory/latest.json` | investor-reporting/holdings, investor-reporting/ops | infra/aws/lambda/investor-reporting/holdings/snapshot.py:665; infra/aws/lambda/investor-reporting/ops/status.py:407 | - | skipped by a card; the card gives no correct name and does not say none is owed | 2 |
| S3Key | `investor-reporting/holdings` | investor-reporting/holdings | infra/aws/lambda/investor-reporting/holdings/snapshot.py:64 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `quarantine/` | investor-reporting/core | infra/aws/lambda/investor-reporting/_keys/keys.py:114 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `smartx/platform/silver/fact_model_allocation_roster` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:60 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `smartx/platform/silver/fact_model_aum_daily` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:58 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3Key | `trending_reports/` | investor-reporting/narrative | infra/aws/lambda/investor-reporting/narrative/evidence.py:59 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |
| S3_BUCKET | `opal-data-news-v2` | investor-reporting/narrative | infra/aws/lambda/investor-reporting/narrative/evidence.py:58 | - | skipped by a card; the card gives no correct name and does not say none is owed | 1 |

## event-fired rule with no ruled token (S3): 3 lines, 3 distinct names

Ask: S3 -- for each rule: the token for a rule fired by an event (the form asks for a cadence; an event rule has none).

| type | name | root | where | bucket read | what the line says is missing | lines |
|---|---|---|---|---|---|---|
| EVENT_RULE | `cot-bronze-complete` | cot-pipeline | infra/aws/terraform/cot-pipeline/eventbridge.tf:172 | - | partial form blackdiamond-cot-bronze-complete-{cadence}; could not fill {cadence}: event rule: its on-{event} token is not ruled | 1 |
| EVENT_RULE | `cot-session-complete` | cot-pipeline | infra/aws/terraform/cot-pipeline/eventbridge.tf:121 | - | partial form blackdiamond-cot-session-complete-{cadence}; could not fill {cadence}: event rule: its on-{event} token is not ruled | 1 |
| EVENT_RULE | `cot-silver-complete` | cot-pipeline | infra/aws/terraform/cot-pipeline/eventbridge.tf:219 | - | partial form blackdiamond-cot-silver-complete-{cadence}; could not fill {cadence}: event rule: its on-{event} token is not ruled | 1 |

## source-owned bucket on a multi-firm root (S2): 3 lines, 1 distinct names

Ask: S2 -- for each bucket: how a bucket owned by a data source (no firm in its name) is written on a root that serves several firms.

| type | name | root | where | bucket read | what the line says is missing | lines |
|---|---|---|---|---|---|---|
| S3_BUCKET | `opal-data-ycharts` | investor-reporting/core, investor-reporting/export, investor-reporting/intake | infra/aws/lambda/investor-reporting/export/handler.py:62; infra/aws/lambda/investor-reporting/intake/poller.py:62; infra/aws/terraform/investor-reporting/core/s3.tf:20 | opal-data-ycharts | partial form opal-data-{scope}; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm; the firm could not be checked: the key's bucket was not read (no bucket literal in the file) and the root entry's fills (system) leave out scope, so it gives no firm to compare with // partial form opal-data-{scope}; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm; the firm could not be checked: bucket opal-data-ycharts names no firm and the root entry's fills (system) leave out scope, so it gives no firm to compare with | 3 |

## first word no vocabulary holds (S4): 4 lines, 4 distinct names

Ask: S4 -- for each name: is it a real stored path or group (then it needs a ruling) or a pattern in the code (then it is printed as a pattern)?

| type | name | root | where | bucket read | what the line says is missing | lines |
|---|---|---|---|---|---|---|
| IAM_GROUP | `calculated-group` | investor-reporting/performance | infra/aws/lambda/investor-reporting/performance/orion_adapter.py:36 | - | R1.f: 'calculated' is in no vocabulary; no registry row resolves it | 1 |
| S3Key | `bbg/` | investor-reporting/core | infra/aws/lambda/investor-reporting/ycharts/research/layout_overview.py:195 | - | K1: segment 1 'bbg' is neither a source nor a tier | 1 |
| S3Key | `firms/` | investor-reporting/export | infra/aws/lambda/investor-reporting/export/backfill_covered_account_ids.py:135 | - | K1: segment 1 'firms' is neither a source nor a tier | 1 |
| SECRET | `astn/kimi/api-key` | investor-reporting/ycharts | infra/aws/lambda/investor-reporting/ycharts/generate/kimi_port.py:19 | - | R1.c: 'astn' is an unresolved token (V2) | 1 |

## NEW: no class of S1 to S4 takes the line: 6 lines, 6 distinct names

Ask: NEW -- the class is not among S1 to S4: for each name, which of the four routes serves it, or a new ruling form is needed. The lines say the firm place {scope} is open on a multi-firm root.

| type | name | root | where | bucket read | what the line says is missing | lines |
|---|---|---|---|---|---|---|
| S3Key | `bronze/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:117 | - | partial form {source}/{scope}/bronze/; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm; the firm could not be checked: the key's bucket was not read (the key's own statement names several buckets, none picked: opal-data-cot, opal-data-inf) and the root entry's fills (system) leave out scope, so it gives no firm to compare with | 1 |
| S3Key | `bronze/eclipse/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:124 | - | partial form eclipse/{scope}/bronze/; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm; the firm could not be checked: the key's bucket was not read (the key's own statement names several buckets, none picked: opal-data-cot, opal-data-inf) and the root entry's fills (system) leave out scope, so it gives no firm to compare with | 1 |
| S3Key | `code/bronze/templates/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:162 | opal-data-cot | partial form {source}/{scope}/code/bronze/templates/; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm | 1 |
| S3Key | `gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:69 | opal-data-assets | partial form {source}/{scope}/gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm; the firm could not be checked: bucket opal-data-assets names no firm and the root entry's fills (system) leave out scope, so it gives no firm to compare with | 1 |
| S3Key | `platinum/mdpf/aggregate_aua/` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py:67 | opal-data-portal-v2 | partial form mdpf/{scope}/platinum/aggregate_aua/; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm; the firm could not be checked: bucket opal-data-portal-v2 names no firm and the root entry's fills (system) leave out scope, so it gives no firm to compare with | 1 |
| S3Key | `schwab/silver/account_xref` | opal-assets | infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/bd49f_dim_conversion.py:78 | opal-data-bd | partial form schwab/{scope}/silver/account_xref; could not fill {source}/{scope}: this root serves more than one firm; its map entry does not give the firm | 1 |

