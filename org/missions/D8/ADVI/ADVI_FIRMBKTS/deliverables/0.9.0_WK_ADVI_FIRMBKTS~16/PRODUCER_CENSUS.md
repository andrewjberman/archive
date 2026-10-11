# FB-f-6 -- PRODUCER CENSUS: who writes 49 Financial's served platinum keys (human view)

Source of truth: `PRODUCER_CENSUS.json` in this folder (the grader reads that file). Read-only measurement:
no producer, `lib/config.py`, schedule or registry row was edited. Every writer line below was re-read at
build time (58 of 58 contain the quoted key text). Counts are object counts from the F7 manifest
(`0.9.0_WK_ADVI_FIRMBKTS~8/F7_MANIFEST.tsv.gz`, 52,910 objects; a key belongs to the longest class prefix).

## 1. Per class

| class | objects | writers | orphan | runner (writers) | schedule |
|---|---:|---:|---|---|---|
| `gold/artifacts/` | 44 | 15 | no | UNKNOWN: no E_ id in gold_dispatch.sh CATALOG or PHASE_*; gold_dispatch.sh PHASE_C5; gold_dispatch.sh PHASE_D1; gold_dispatch.sh PHASE_D2; gold_dispatch.sh PHASE_D3; gold_dispatch.sh PHASE_D4 | null (see section 5) |
| `gold/entities/accounts/` | 8563 | 1 | no | gold_dispatch.sh PHASE_D3 | null (see section 5) |
| `gold/entities/advisors/` | 773 | 7 | no | gold_dispatch.sh PHASE_D1; gold_dispatch.sh PHASE_D3 | null (see section 5) |
| `gold/entities/clients/` | 18194 | 4 | no | gold_dispatch.sh PHASE_C5; gold_dispatch.sh PHASE_D1; gold_dispatch.sh PHASE_D3 | null (see section 5) |
| `gold/platinum/firm/` | 2 | 2 | no | gold_dispatch.sh PHASE_D4 | null (see section 5) |
| `gold/views/` | 10 | 6 | no | gold_dispatch.sh PHASE_B5; gold_dispatch.sh PHASE_C4; gold_dispatch.sh PHASE_C5; gold_dispatch.sh PHASE_D1 | null (see section 5) |
| `platinum/49financial/` | 1 | 1 | no | gold_dispatch.sh PHASE_D1 | null (see section 5) |
| `platinum/accounts/` | 7562 | 1 | no | gold_dispatch.sh PHASE_D4 | null (see section 5) |
| `platinum/advisors/` | 980 | 5 | no | gold_dispatch.sh PHASE_D4 | null (see section 5) |
| `platinum/clients/` | 16766 | 5 | no | gold_dispatch.sh PHASE_D4 | null (see section 5) |
| `platinum/firm/` | 15 | 11 | no | gold_dispatch.sh PHASE_D4; gold_dispatch.sh PHASE_D5 | null (see section 5) |
| **total** | **52910** | | | | |

## 2. Writers (script:line -- key expression as it appears on that line)

### `gold/artifacts/` (44 objects)

- `data/black_diamond/scripts/gold/C_08.advisor_fee_efficiency.py:554` -- `Key=ADVISOR_FEE_EFFICIENCY,` -- bucket: S3_BUCKET (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_C5 (gold_dispatch.sh:602-603), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/E_24.rebuild_fee_scorecard.py:254` -- `Key=ADVISOR_FEE_EFFICIENCY,` -- bucket: S3_BUCKET (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: UNKNOWN: no E_ id in gold_dispatch.sh CATALOG or PHASE_* (searched that file); comp-pipescript io reports 'Script not found' for it
- `data/black_diamond/scripts/gold/D_00.portal_aggregates.py:1118` -- `_save_json(clients, CLIENTS_TAB, dry_run=dry_run)` -- bucket: S3_BUCKET inside lib/gold_utils._save_json (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_00.portal_aggregates.py:1124` -- `_save_json(hm, HEADER_METRICS, dry_run=dry_run)` -- bucket: S3_BUCKET inside lib/gold_utils._save_json (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_00.portal_aggregates.py:1128` -- `_save_json(filters, FILTERS_DIMENSIONS, dry_run=dry_run)` -- bucket: S3_BUCKET inside lib/gold_utils._save_json (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_00.portal_aggregates.py:1133` -- `_save_json(snap, key, dry_run=dry_run)` -- bucket: S3_BUCKET inside lib/gold_utils._save_json (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_00b.portal_timeseries.py:1412` -- `_save_json(chart, TIMESERIES_CHART, dry_run=dry_run)` -- bucket: S3_BUCKET inside lib/gold_utils._save_json (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D2 (gold_dispatch.sh:610-611), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py:1390` -- `_save_json(emp_lb, EMPLOYEE_LEADERBOARD, dry_run=dry_run)` -- bucket: S3_BUCKET inside lib/gold_utils._save_json (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_01.partner_analytics.py:2547` -- `key = partner_analytics_key(granularity)` -- bucket: S3_BUCKET (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D2 (gold_dispatch.sh:610-611), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py:3217` -- `_save_json(impl_lb, IMPLEMENTOR_LEADERBOARD)` -- bucket: S3_BUCKET inside D_02 _save_json (lib.config import, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D3 (gold_dispatch.sh:614-615), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:507` -- `Key=FIRM_MIX_VIEWS_DAILY,` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:526` -- `Key=FIRM_MIX_VIEWS,` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:3464` -- `_write_json_to_s3(artifact, OUT_OF_SCOPE_ARTIFACT_KEY)` -- bucket: _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270), BUCKET alias of lib.config S3_BUCKET -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:3736` -- `_write_json_to_s3(artifact, C1_RECOVERED_ARTIFACT_KEY)` -- bucket: _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270), BUCKET alias of lib.config S3_BUCKET -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/E_01.account_quality_tiers.py:333` -- `json_key = account_quality_tiers_json_key(target_date)` -- bucket: S3_BUCKET (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: UNKNOWN: no E_ id in gold_dispatch.sh CATALOG or PHASE_* (searched that file); comp-pipescript io reports 'Script not found' for it

### `gold/entities/accounts/` (8563 objects)

- `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py:2269` -- `items.append((response, account_aua_timeseries_key(str(acct_id))))` -- bucket: S3_BUCKET inside D_02 _save_json_batch (lib.config import, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D3 (gold_dispatch.sh:614-615), run on bd-gold-layer-runner EC2

### `gold/entities/advisors/` (773 objects)

- `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py:1578` -- `books.append((_advisor_output_key(adv_id), book))` -- bucket: S3_BUCKET inside D_02 _save_json_batch (written at line 3269) -- runner: gold_dispatch.sh PHASE_D3 (gold_dispatch.sh:614-615), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py:2151` -- `items.append((response, advisor_timeseries_key(adv_id)))` -- bucket: S3_BUCKET inside D_02 _save_json_batch -- runner: gold_dispatch.sh PHASE_D3 (gold_dispatch.sh:614-615), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py:2342` -- `_save_json(response, advisor_mix_timeseries_key(adv_id))` -- bucket: S3_BUCKET inside D_02 _save_json (lib.config import) -- runner: gold_dispatch.sh PHASE_D3 (gold_dispatch.sh:614-615), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:549` -- `dk = advisor_mix_daily_key(adv_id)` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:573` -- `mk = advisor_mix_key(adv_id)` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:583` -- `tk = advisor_mix_timeseries_key(adv_id)` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:799` -- `advisor_composition_key(adv_id),` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) via _write_json_batch (line 811) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2

### `gold/entities/clients/` (18194 objects)

- `data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py:363` -- `key = client_timeseries_key(rel_id)` -- bucket: S3_BUCKET (lib.config) at put_object line 366 -- runner: gold_dispatch.sh PHASE_C5 (gold_dispatch.sh:602-603), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py:2216` -- `items.append((response, client_aua_timeseries_key(str(rel_id))))` -- bucket: S3_BUCKET inside D_02 _save_json_batch -- runner: gold_dispatch.sh PHASE_D3 (gold_dispatch.sh:614-615), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py:2947` -- `items.append((response, client_detail_key(rel_id_str)))` -- bucket: S3_BUCKET inside D_02 _save_json_batch -- runner: gold_dispatch.sh PHASE_D3 (gold_dispatch.sh:614-615), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:912` -- `client_composition_key(rel_id),` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) via _write_json_batch -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2

### `gold/platinum/firm/` (2 objects)

- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:3123` -- `_write_json_to_s3(summary, COHORT_A_ARTIFACT_KEY)` -- bucket: _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270), BUCKET alias of lib.config S3_BUCKET -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:3223` -- `_write_json_to_s3(summary, CASH_COVERAGE_ARTIFACT_KEY)` -- bucket: _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270), BUCKET alias of lib.config S3_BUCKET -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2

### `gold/views/` (10 objects)

- `data/black_diamond/scripts/gold/C_05.client_tax_liability.py:401` -- `s3.upload_file(str(local_path), S3_BUCKET, output_key)` -- bucket: S3_BUCKET (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_B5 (gold_dispatch.sh:582-583), run on bd-gold-layer-runner EC2 (EC2_CODE_DEPLOYMENT_STANDARD.md:321-331)
- `data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py:417` -- `Key=MIX_DAILY_SUMMARY,` -- bucket: S3_BUCKET (lib.config, env BD_S3_BUCKET, default opal-data-bd) -- runner: gold_dispatch.sh PHASE_C5 (gold_dispatch.sh:602-603), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/C_07.advisor_attribution.py:477` -- `ACCOUNT_TEAM,` -- bucket: S3_BUCKET (lib.config) via local _write -> s3.upload_file (line 473) -- runner: gold_dispatch.sh PHASE_C4 (gold_dispatch.sh:598-599), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/C_07.advisor_attribution.py:478` -- `RELATIONSHIP_TEAM,` -- bucket: S3_BUCKET (lib.config) via local _write -> s3.upload_file (line 473) -- runner: gold_dispatch.sh PHASE_C4 (gold_dispatch.sh:598-599), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/C_07.advisor_attribution.py:479` -- `REL_ARCHITECT_LOOKUP,` -- bucket: S3_BUCKET (lib.config) via local _write -> s3.upload_file (line 473) -- runner: gold_dispatch.sh PHASE_C4 (gold_dispatch.sh:598-599), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_03.composition_artifacts.py:767` -- `_write_json(firm_comp, FIRM_COMPOSITION, upload,` -- bucket: BUCKET (alias of lib.config S3_BUCKET, env BD_S3_BUCKET, default opal-data-bd) via _write_json (line 202) -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2

### `platinum/49financial/` (1 objects)

- `data/black_diamond/scripts/gold/D_00.portal_aggregates.py:1138` -- `_save_json(ownership, platinum_advisor_ownership_key(FIRM_ID),` -- bucket: S3_BUCKET inside lib/gold_utils._save_json (lib.config, env BD_S3_BUCKET, default opal-data-bd); FIRM_ID env default '49financial' -- runner: gold_dispatch.sh PHASE_D1 (gold_dispatch.sh:606-607), run on bd-gold-layer-runner EC2

### `platinum/accounts/` (7562 objects)

- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1411` -- `items.append((summary, f'platinum/accounts/{acct_str}/summary.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2

### `platinum/advisors/` (980 objects)

- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:752` -- `items.append((summary, f'platinum/advisors/{aid}/summary.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:759` -- `items.append((ts_gated, f'platinum/advisors/{aid}/timeseries.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:763` -- `items.append((mix_data, f'platinum/advisors/{aid}/mix.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2740` -- `items.append((payload, f'platinum/advisors/{aid}/nna_clients.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2937` -- `items.append((payload, f'platinum/advisors/{aid}/positions.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2

### `platinum/clients/` (16766 objects)

- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1180` -- `items.append((summary, f'platinum/clients/{rid}/summary.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1184` -- `items.append((views, f'platinum/clients/{rid}/views.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1188` -- `items.append((comp, f'platinum/clients/{rid}/composition.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1239` -- `f'platinum/clients/{rid}/mix_timeseries.json'` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1247` -- `f'platinum/clients/{rid}/concentration.json'` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2

### `platinum/firm/` (15 objects)

- `data/black_diamond/scripts/gold/D_00f.advisor_nna_canonical.py:928` -- `_write_json_s3(artifact, OUTPUT_KEY)` -- bucket: literal 'opal-data-bd' (D_00f.advisor_nna_canonical.py:87), NOT the lib.config seam via _write_json_s3 put_object(Bucket=S3_BUCKET) at line 768 -- runner: gold_dispatch.sh PHASE_D5 (gold_dispatch.sh:622-623), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:410` -- `(dashboard, 'platinum/firm/dashboard.json')` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:554` -- `(summary, 'platinum/firm/mix_summary.json')` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1940` -- `(overview, 'platinum/firm/timeseries_overview.json')` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:1992` -- `items.append((data, f'platinum/firm/partner_analytics_{gran}.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2228` -- `(chart, 'platinum/firm/cumulative_chart.json')` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2469` -- `Key='platinum/firm/leaderboard.prior_week.json',` -- bucket: BUCKET (alias of lib.config S3_BUCKET) on copy_object (line 2467) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2478` -- `(leaderboard, 'platinum/firm/leaderboard.json')` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2547` -- `(slim, 'platinum/firm/clients-tab-slim.json')` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2582` -- `items.append((header_metrics, 'platinum/firm/header_metrics.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2
- `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2595` -- `items.append((timeseries_chart, 'platinum/firm/timeseries_chart.json'))` -- bucket: _write_batch -> _write_json_to_s3 -> put_object(Bucket=BUCKET) (D_04.client_portal_summary.py:269-270,277-292) -- runner: gold_dispatch.sh PHASE_D4 (gold_dispatch.sh:618-619), run on bd-gold-layer-runner EC2

Distinct writer scripts: 14 (C_05, C_06, C_07, C_08, D_00, D_00b, D_00c, D_00f, D_01, D_02, D_03, D_04, E_01, E_24).

Convention: the line cited is the line whose text carries the key expression the write consumes. Where a
helper performs the put (`_write_batch`, `_write_json_to_s3`, `_save_json`, `_save_json_batch`,
`_write_json_batch`), the helper's own put line is named in the bucket column, not repeated per entry.

## 3. The bucket seam

- Definition: `data/black_diamond/scripts/gold/lib/config.py:14` -- `S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')`.
- Importers of `S3_BUCKET` from `lib.config` under `data/black_diamond/scripts/gold` and `data/assets/scripts/gold`: 42 (recounted by the grader).
- `separable_per_output`: false.

lib/config.py:14 defines S3_BUCKET once, from the process environment (BD_S3_BUCKET, default opal-data-bd). Every one of the 42 importers binds that one name (D_03.composition_artifacts.py:77 and D_04.client_portal_summary.py:83 import it as BUCKET) and uses it for every get_object, list, put_object and copy in the same process, so reads and writes are bound to one bucket per process. A script cannot send one output to another bucket without editing the script: the only switch is the environment variable, which moves every read and every write of that process together. Writes that bypass the seam are not in the 42: D_00f.advisor_nna_canonical.py:87 hard-codes S3_BUCKET = 'opal-data-bd' and writes platinum/firm/advisor_nna_canonical.json. Searching the gold directories for bucket literals returns only the bd default, that D_00f literal, and opal-data-assets / opal-data-inf / opal-data-schwab literals in B_00 and lib/schwab_* (none of them a served-class writer).

## 4. Every place `BD_S3_BUCKET` is set or defaulted (outside `org/`, `*.md`)

Bd-bucket defaults or launch-time settings (these route a run to opal-data-bd unless the env var is overridden):

- `data/black_diamond/scripts/gold/gold_dispatch.sh:77` -- `BD_S3_BUCKET="${BD_S3_BUCKET:-opal-data-bd}"` (the gold dispatcher; its phases are the runner).
- `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh:13` and `setup-instance.sh:29` -- `S3_BUCKET="${BD_S3_BUCKET:-opal-data-bd}"` (EC2 runner defaults).
- `infra/aws/ec2/bd-gold-qa-runner/setup-instance.sh:36` and `:122` -- same default (QA runner).
- `infra/aws/ec2/canonical-schwab-runner/setup-instance.sh:13` and `:26` -- `BD_BUCKET="${BD_S3_BUCKET:-opal-data-bd}"`; `user-data.sh:28` -- `BD_S3_BUCKET="${BD_BUCKET}" /tmp/setup-instance.sh` (explicit launch-time setter).
- `infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py:64` -- `BD_S3_BUCKET = "opal-data-bd"`, exported to `os.environ` at `:205`.
- `infra/aws/lambda/bd-pipeline/bd-49f-fees-runner/lambda_function.py:38` and `:72` -- same pattern.
- `infra/aws/lambda/bd-pipeline/bd-silver-merge/lambda_function.py:40` and `:73` -- same pattern (silver merge).
- `data/black_diamond/scripts/silver/*.py` and `data/black_diamond/scripts/classification/*.py` -- module-level default `os.environ.get('BD_S3_BUCKET', 'opal-data-bd')` (reads; outside the gold seam).
- No Terraform block under `infra/aws/terraform/bd-pipeline` sets `BD_S3_BUCKET` (searched that directory).

Settings that point the same variable elsewhere (not opal-data-bd; recorded so no one reads them as bd):

- `data/cot/scripts/gold/gold_dispatch.sh:62` and `infra/aws/terraform/cot-pipeline/ssm.tf:233,331` -- `opal-data-cot`.
- `infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf:157` -- `aws_s3_bucket.monolith.id`.
- `infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:62` -- default `opal-data-assets`.

## 5. Runners and schedules (what was read, and what was not)

- Runner for the BD gold chain: `gold_dispatch.sh` phases on the persistent EC2 `bd-gold-layer-runner` (`docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md:34` lists it as persistent, stopped; `:242` and `docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md:321-331` show the start-and-dispatch commands).
- Schedule: `null` for every writer. No scheduler resource for this runner was found in `infra/aws/terraform/` (searched `bd-pipeline`, `bd-bucket-lifecycle` and the whole tree for `bd-gold-layer-runner` / `gold_dispatch`); `comp-schedule` is a gate ledger, not a cron ledger. Whether an out-of-repo scheduler exists was NOT read (no AWS act in bounds): UNKNOWN.
- Runner for `E_01` and `E_24` (and the other E-series): UNKNOWN. `gold_dispatch.sh` has no E_ entry; `comp-pipescript io` returns `Script not found` for 25 of the 26 E-series ids (see the surprise rows).

## 6. What could not be determined

- Schedules and triggers: `null` for all writers (section 5); no live AWS read was made.
- Runner of the E-series writers `E_01` and `E_24`: UNKNOWN (section 5).
- Legacy dual-writes: the `LEGACY` map (`lib/s3_layout.py:312-340`) lands on `gold/<name>` root keys and on the `gold/positions_cube/`, `gold/holdings_lots/`, `gold/client_timeseries/` legacy prefixes, none of which is one of the 11 served prefixes. The advisor and client legacy builders used by D_02 and D_03 (`legacy_advisor_mix_key`, `legacy_client_composition_key`, and the others) were NOT all resolved to their targets: whether any of them lands under a served prefix is UNKNOWN.
- Writers outside the two gold directories: the served-prefix grep over `data/assets`, `data/inf`, `data/cot`, `infra/aws/lambda`, `infra/aws/ec2` found 75 files; bucket literals were read for all of them, and the ones naming opal-data-bd were read line by line (`runners_49f/d_publisher_port.py` reads role_aua from opal-data-bd at line 202 and writes only to opal-data-portal-v2 at lines 483-490 and 615-618; `investor-reporting/directory_runner.py` holds a firm-to-bucket map with no served-prefix write; `mdpf-daily-trigger` names a `platinum/mdpf/` prefix that is not a served class). The remaining files were not read line by line.
- The graph (`comp-pipescript io`) is not used as the census source: it under-reports helper-mediated writes and lists a read as a write for D_04 (surprise row ADVI_FIRMBKTS-D1-W16-S1).
- The `platinum/49financial/ownership_map.json` key is written to opal-data-bd by D_00 (this census). Whether the 49F runner family in `data/assets/scripts/gold/runners_49f/d08_firm_ownership_map.py` writes an equal-named key to any bucket was not traced to its put: UNKNOWN.

## 7. Surprise rows filed (investigation channel, this folder's sibling file)

- `ADVI_FIRMBKTS-D1-W16-S1` -- graph under-reports D_04 writes and lists a read as a write (INERT).
- `ADVI_FIRMBKTS-D1-W16-S2` -- D_00f writes a served platinum key through a hard-coded bucket outside the seam (ARMED, disarm owner 2.0.0_SA_COO~B1).
- `ADVI_FIRMBKTS-D1-W16-S3` -- comp-pipescript cannot resolve 25 of 26 E-series ids; E_01 and E_24 write served keys with no dispatch entry (INERT).

