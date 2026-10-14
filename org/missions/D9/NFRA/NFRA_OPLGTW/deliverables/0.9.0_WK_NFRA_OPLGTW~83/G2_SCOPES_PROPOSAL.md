# G2 registry additions for master 08403355 -- PROPOSAL ONLY (OG-cl-0)

Nothing is applied. `org/standards/NFRA_OPLGTW_CONTRACT.json` and `infra/logic/registry/scopes.json` are unchanged by this cell (AC2 counts zero changed files against the fork point). The census (G2 section 2, item 5; section 3.2) and the v3.1 addendum (Ruling 5) name the gap: 08403355 is admitted by the gateway IAM and missing from both files.

Measured before writing this proposal:

- `gateway-schwab-read-role` grants `dim_position`, `dim_balance`, `dim_asset` and `dim_transaction` on `opal-data-assets/schwab/08403355/silver/*` (the same four as 08242234 and 08335338). `gateway-schwab-catalog-read-role` grants `schwab/08403355/meta/complete/*`. Both are in `G2_ROLES.json`.
- The 08403355 contract ids exist in the census (`opal-data-assets/silver/schwab_08403355_dim_position` and the rest, 18 tables).

## 1. Unruled field: the contract label for 08403355

The contract `masters` map carries a label per master (`"08242234": "SmartX"`, `"08335338": "BlackDiamond"`). The census (section 3.2) says the CTO ruling calls 08242234 and 08403355 the two Tax SMA masters, yet the contract labels 08242234 SmartX, and the data reads MAM and SmartX on the rows. The label is open item O-3 (census section 5). This proposal therefore cannot write the label exactly. The one field it leaves open is the label value below, shown as a placeholder.

## 2. `org/standards/NFRA_OPLGTW_CONTRACT.json`

Current rows (lines 6-9):

```json
  "masters": {
    "08242234": "SmartX",
    "08335338": "BlackDiamond"
  },
```

Proposed rows (the added line is `"08403355"`; its value is the ruled label, O-3):

```json
  "masters": {
    "08242234": "SmartX",
    "08335338": "BlackDiamond",
    "08403355": "<ruled label, open item O-3>"
  },
```

Current `data_prefixes` (lines 291-299) and `completion_prefixes` (lines 301-304) list only 08242234 and 08335338. Proposed additions, each matching a grant the role already holds:

```json
  "data_prefixes": [
    "schwab/08242234/silver/dim_position/",
    "schwab/08242234/silver/dim_balance/",
    "schwab/08242234/silver/dim_asset/",
    "schwab/08242234/silver/dim_transaction/",
    "schwab/08335338/silver/dim_position/",
    "schwab/08335338/silver/dim_balance/",
    "schwab/08335338/silver/dim_asset/",
    "schwab/08335338/silver/dim_transaction/",
    "schwab/08403355/silver/dim_position/",
    "schwab/08403355/silver/dim_balance/",
    "schwab/08403355/silver/dim_asset/",
    "schwab/08403355/silver/dim_transaction/"
  ],
  "completion_prefixes": [
    "schwab/08242234/meta/complete/",
    "schwab/08335338/meta/complete/",
    "schwab/08403355/meta/complete/"
  ],
```

The contract's `"contract_version": "1.4"` is a bump owner's decision and is not proposed here.

## 3. `infra/logic/registry/scopes.json`

Current row (the `49financial` FIRM row, line 23):

```json
      "masters": ["08242234", "08335338"],
```

Proposed:

```json
      "masters": ["08242234", "08335338", "08403355"],
```

Current MASTER row for 08335338 (lines 260-271; the 08242234 row sits just above it):

```json
    {
      "key": "08335338",
      "class": "MASTER",
      "long": "08335338",
      "short": "08335338",
      "tenancy": "FIRM",
      "firm": "49financial",
      "vendor": "schwab",
      "bucket": "opal-data-49financial",
      "bucket_provisioned": true,
      "aliases": []
    },
```

Proposed: insert directly after that row a sibling row for 08403355 (the same fields; the `bucket` value is copied from the sibling rows as they stand):

```json
    {
      "key": "08403355",
      "class": "MASTER",
      "long": "08403355",
      "short": "08403355",
      "tenancy": "FIRM",
      "firm": "49financial",
      "vendor": "schwab",
      "bucket": "opal-data-49financial",
      "bucket_provisioned": true,
      "aliases": []
    },
```

Checked on a scratch copy of `infra/logic/registry/` carrying both edits above: `lib/opal_naming.py` `validate()` returns no refusals (`([], [])`), the same as on the unmodified registry (positive control). The copy was not committed and the registry is untouched.

Open for the registry owner, not decided here: the sibling rows name `opal-data-49financial` as the master's bucket, while the census measures the Schwab silver under `opal-data-assets/schwab/<master>/`. Whether the new row should carry the same value is the owner's call.

Under A2 (Andrew-direct via CTO msg 34134) no `client_*` adapter reads `opal-data-49financial`, so the bucket value selects no client read in this proposal. The 08403355 data prefixes above are `opal-data-assets/schwab/08403355/silver/` keys, which are the only ones the adapters use.

## 4. What this proposal does not do

- It does not add `08403355` to `DATA_CATALOG.yaml` (catalog is NFRA_MCPINDEX's file).
- It does not change any IAM grant. The grant exists today; the proposal only names it in the contract and registry.
- It does not add the registry row to any LGIC name table. The row carries no new name.
