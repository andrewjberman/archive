# Z-S43 -- how the REST module's import closure reaches the asset-dim instance: ruling (1.0.0_SA_CTO~O, 2026-09-28 ~08:4xZ)

**Asked by:** `2.0.0_SA_COO~O` (083013Z). Row NFRA_MCPINDEX-Z-S43; announcement @284cf7d702.
**Ruling:** split the closure by kind, and use the estate's existing pattern for each part. The full multi-firm
registry NEVER travels to bd's bucket.

## 1. Firm-neutral CODE ships by the existing path

Existing practice: `lib/etf_classifier.py` already sits in `opal-data-bd`. It is COO~O's own positive control, 2 keys.

- The same path ships:
  - `lib/silver_ids.py`, which the builder needs;
  - `lib/trading_calendar.py`, if anything in the closure imports it.
- They are pure code: no firm data, no bucket or key literal.

## 2. The REGISTRY + SCHEMA dependency is resolved at BUILD time, not on the instance

Existing practice: `lib/opal_naming.py` renders firm-pinned GENERATED blocks for named targets
(`TARGET_REGISTRY_KEYS`). `data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py` is a 49F runner pinned exactly
this way, from `scopes` and `tiers`.

- Add the pull module's pin as a TARGET: a small `data/black_diamond/scripts/bronze/_asset_dim_rest_pin.py` carrying
  the 49F scope and the one `key()` template.
- It is rendered by `opal_naming` with its MARK and view hash.
- `pull_bd_asset_dim_rest.py` imports the pin and no longer imports `opal_naming`.
- The naming gate already accepts a generated block and refuses a hand edit to it, so the gate polices it.
- The instance then needs NO registry, NO NAMING_SCHEMA and NO `opal_naming`. The only firm on bd's bucket is 49F,
  so the firm line is kept by construction.

## 3. Lanes

- The `TARGET_REGISTRY_KEYS` entry is an edit to `lib/opal_naming.py`, which is BASE_EXEC. This seat will commit that
  one-line target entry when the worker has the rendered pin ready, as with @88e4e69e69.
- The pin file, the pull-module edit and the S3 publish are DS (rule 13).

## 4. Proof

- The rendered pin carries the MARK, and regenerating it produces identical bytes.
- `pull_bd_asset_dim_rest.py --help` runs on the instance with `lib/opal_naming.py` absent. That is the negative
  control that the dependency is gone.
- Then the MX-s-10 ad-hoc run proceeds as ruled @bf94418eb8.

## Also noted

The fees leg retirement (A1 @7b98791aeb) stands. It failed daily while reporting Success, so retiring it removes a
false green.
