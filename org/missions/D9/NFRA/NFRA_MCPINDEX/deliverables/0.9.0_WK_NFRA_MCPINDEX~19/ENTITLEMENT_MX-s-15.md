# ENTITLEMENT_MX-s-15 -- does an existing Schwab grant cover `dim_transaction`?

Author: 0.9.0_WK_NFRA_MCPINDEX~19. Recorded, not changed (ruling B2). No identity, grant or sign-in path was created or
changed. Read at the worktree's HEAD (CLOUD @2cae2db258 plus this cell).

## Answer

**No. An existing grant does not cover `dim_transaction` automatically, at any of three layers.**

### 1. The principal's grant (`app/data_entitlement.py`)

A grant stores its datasets explicitly: `scope.datasets` (a list) and `scope.columns` (a map with exactly one key per
granted dataset) (`parse_scope`, `:240-283`; `columns` must name "every granted dataset and no other", `:266-269`).
`check_scope` refuses any request whose dataset is not in `scope.datasets` (`:494-496`) and any column not in
`scope.columns[dataset]` (`:517-522`). A grant issued before this cell names only `dim_position`, `dim_balance`,
`dim_asset`, so a `dim_transaction` request returns `("datasets", "dataset 'dim_transaction' is not granted")` and a
`("columns", ...)` failure. The new dataset is covered only by re-issuing the grant with `dim_transaction` and its
columns. Declaring it in `DATASETS` (`:72`) only lets a grant NAME it (`parse_scope` refuses a name outside `DATASETS`,
`:255-256`); it widens no existing grant. Existing grants still parse (their datasets are a subset). Proven by
`tests/test_schwab_transactions.py::test_mx_s15_entitled_like_dims`.

### 2. The contract the gateway and the grant tool read (`org/standards/NFRA_OPLGTW_CONTRACT.json`, outside this cell's paths)

`datasets` (`:10-14`) and `fields` (per dataset, `:152-187`) do not list `dim_transaction`. The grant admin tool
(`ops/schwab_entitlement_admin.py:166-169`) approves a requested column only if it is in the contract's `fields[dataset]`,
and the running service takes its dataset list from the contract (`integration.py:427,470` via `rules.datasets`;
`catalog.py:601,882` via `contract.datasets`). So until the contract lists the dataset, no grant can be issued with its
columns and a query names it `dataset_invalid`. Row `NFRA_MCPINDEX-Z-W19-S2`.

### 3. The reader role (`gateway-schwab-read-role`, APPLIED plane, issuer-measured 2026-09-30)

`s3:GetObject` on `schwab/08242234/silver/dim_position/...` is allowed and on `.../dim_transaction/...` is
`explicitDeny` (simulate-principal-policy). This cell adds the two `dim_transaction` prefixes to `schwab_data_prefixes`
in `infra/aws/terraform/opal-gateway/schwab_reader_iam.tf`. Not applied here; the apply is MX-r-6.

## What the release halves at MX-r-6 read

- Adding the dataset moves no existing principal's access. Nobody can read `dim_transaction` until (a) the contract lists
  it, (b) the reader role is applied, and (c) an operator re-issues a grant naming it, per principal.
- The default seeded grants in `tests/acceptance/conftest.py` use `data_entitlement.DATASETS`; with the contract not yet
  carrying the dataset that suite fails 8 of 14 (`KeyError: 'dim_transaction'`). Row `NFRA_MCPINDEX-Z-W19-S2`.
