# SCOPE_DROP_RECORD -- MX-c-30 (NFRA_MCPINDEX round 18, workstream RESEARCH, worker 0.9.0_WK_NFRA_MCPINDEX~50)

Scope: Andrew's scope, advisor intelligence and investor reporting surfaces are out of the gateway catalog (PRD v0.17 of
NFRA_MCPINDEX, C-GROUP scope line). The exclusion is the prefix list in `workflows/atom_decomposition/scope_exclusions.json`
(`platinum/advi/`, `platinum/irpt/`), applied by `gen_silver_rows.py` to `leading_prefix(c, rec)`.

## 1. Dropped entities (2)

| entity | prefix (leading_prefix) | row file removed |
|---|---|---|
| `opal_data_portal_v2_platinum_advi_49financial_perfrp` | `platinum/advi/49financial/` | `workflows/atom_decomposition/catalog_entries/opal_data_portal_v2_platinum_advi_49financial_perfrp.yaml` |
| `opal_data_portal_v2_platinum_advi_49financial_twins` | `platinum/advi/49financial/` | `workflows/atom_decomposition/catalog_entries/opal_data_portal_v2_platinum_advi_49financial_twins.yaml` |

The generator prints both at the default run (verbatim):

    excluded opal_data_portal_v2_platinum_advi_49financial_twins: platinum/advi/49financial/
    excluded opal_data_portal_v2_platinum_advi_49financial_perfrp: platinum/advi/49financial/

## 2. platinum/mdpf/ candidates that stayed (2)

Neither is advisor intelligence or investor reporting; both are model-portfolio (MDPF) surface, read from each row's `business_meaning`.

| entity | prefix | why it stays |
|---|---|---|
| `opal_data_portal_v2_platinum_mdpf_cottonwood_account_units` | `platinum/mdpf/cottonwood/account-units.json` | business_meaning: account-units for the Cottonwood firm only, unit values (384 points, per model, 12 models): a model-portfolio unit series, not advisor or investor reporting. |
| `opal_data_portal_v2_platinum_mdpf_manifests_and_archive` | `platinum/mdpf/` | business_meaning: the MDPF publish manifests (one per publish run) and the frozen archive of daily aggregate_aua snapshots and ETF ownership series: the model-portfolio publish record, not advisor or investor reporting. |

## 3. Orphan registry entries (2, not edited)

`infra/logic/registry/catalog_fork_keys.json` still names both dropped entities in its `entities` array (lines 4940 and 4941 at
the worktree HEAD of this order): `opal_data_portal_v2_platinum_advi_49financial_perfrp` and
`opal_data_portal_v2_platinum_advi_49financial_twins`. The registry file is not in this order's `<paths>` and was not edited.
The emitter ran without refusal on them (`emit_catalog_v02.py --overlay-ref 06cfb6db64`: HARVEST ROWS 78 emitted, 0 refused;
SILVER 224 emitted, 0 refused; TOOL INDEX N=99 served tools).

## 4. Counts

- Generator, fresh run on the pinned inputs: `wrote 214 rows`, rc=0; two `excluded` lines.
- Catalog rows committed before this order: 216 contracts; after: 214 row files written by the generator (the two removals are the `git rm`).
- Unit tests: `workflows/atom_decomposition/tests` 228 passed at baseline; 239 passed after (11 new in `test_scope_exclusions.py`).
