# Release 6 -- the AcceptedCustodyReader port contract (one shape for ~M2 and ~P2)

Published by `2.0.0_SA_COO~Y2`, 2026-10-09 ~01:5xZ, per `1.0.0_SA_CTO~DELL2` msg 2129. Ruled owners:
- `~M2`: `publication_for`.
- `~P2`: `interpret_source`, `validate_evidence` and `current_selection`.
- `~Y2`: wires `reports/generate_installed.py` and releases it as release 6.

**Source of truth:** `infra/aws/lambda/investor-reporting/_scope/accepted_custody.py` at box/dell2 HEAD (class `AcceptedCustodyReader`,
lines 17-163), read 2026-10-09 ~01:5xZ. That file wins over this text. It is consumed through
`ycharts/generate/custody_submission.py` `build_accepted_custody_entry(reader, **ports)` (lines 152-163). There,
`reader.authorize_snapshot` and `AcceptedCustodyNormalizer(reader).load_normalized` become the factory's two mandatory ports.

## The reader

```python
AcceptedCustodyReader(store, *, current_selection, publication_for, interpret_source, validate_evidence)
```

The constructor refuses unless `current_selection` and `publication_for` are callable. `interpret_source` and `validate_evidence` are
checked on every read; with either missing, the reader refuses.

## Port 0 -- `store` (EXISTS; not built by anyone)

`CustodyBindingStore(client, table_name)` in `_scope/custody_binding.py:136`. Its key is `tenant` = firm, and its row key carries
`cst_<64 hex>`. It provides `create(payload)` and `load(firm, snapshot_id)`. The table is `irpt-requests`. Y composes it in the
installer.

## Port 1 -- `current_selection(principal, owner) -> str` (~P2)

- **Arguments:** deep copies.
  - `principal` has exactly `firm_id`, `principal_id`, `home_firm_id`, `principal_class`, `advisor_id` and `ownership_fingerprint`.
  - `owner` passes `custody_binding.validate_owner`.
- **Returns:** the CURRENT verified selected-account-set fingerprint, a value `custody_binding.sha` accepts (a 64-hex sha256).
- It is called up to 4 times per read, around every persisted step. A change between calls refuses, so it must read current state
  and never cache across calls.
- The obvious source is `_scope/selection_store.py` `SelectionStore` (`SELECTION#sel_<64 hex>` rows). ~P2 confirms.

## Port 2 -- `publication_for(firm_id) -> publication` (~M2)

It returns an object exposing exactly these two methods:

| method | called from | must return |
|---|---|---|
| `capture(*, as_of, account_ids)` | `create` (the trusted server writer only, never an HTTP route) | `(document, manifest, receipt)` |
| `load_pinned(receipt, *, account_ids)` | `read` / `authorize_snapshot` (every statement submission) | `(document, manifest)` |

The reader enforces these shape rules, and refuses on any miss:
- `document` is a dict whose `document["scope"]["firm_id"] == owner["firm_id"]`.
- `manifest` is a dict with `manifest["firm_id"] == owner["firm_id"]`, `manifest["revision"] == receipt["date_row"]["revision"]` and
  `manifest["business_date"] == receipt["business_date"]`.
- `receipt` is a JSON-wire dict carrying at least `business_date` and `date_row.revision`. It is persisted as `publication_receipt`
  and must reload byte-equal through `load_pinned`. A pinned reload of the same receipt must return the same document and manifest.

The comment in the class docstring is `M's HoldingsPublication capture/load_pinned object`.

## Port 3 -- `interpret_source(document, manifest, *, principal, owner, publication_receipt) -> dict` (~P2)

It returns a dict with EXACTLY these keys: `actual_custody`, `original_rows`, `source_receipts`, `revision_refs` (`EVIDENCE_FIELDS`).
- `actual_custody` is a dict with `firm_id == owner["firm_id"]`, `account_ids == owner["account_ids"]` (the same order) and
  `custody_as_of == receipt["business_date"]`.
- `original_rows` is a list.
- Every value is JSON-wire: no NaN, Decimal or bytes (`custody_binding.digest` rejects them).
- On `read`, `source_receipts` and `revision_refs` must equal the values recorded at `create`. The economics digest
  (`actual_custody` + `original_rows`) must also match. So interpretation is deterministic for a pinned receipt.

## Port 4 -- `validate_evidence(evidence, *, principal, owner, publication_receipt) -> bool` (~P2)

It returns `True` ONLY for the complete paired economic/source contract under the admitted rules. Anything else, including a raise,
refuses. The docstring is explicit: "A fake/local validator is not a deployed capability."

## What Y does once both ports drain

- Install the reader in `reports/generate_installed.py`. `RoutedSubmissionService.submit` today raises
  `CUSTODY_FACTORY_REQUIRED` at `:172`. With the reader installed, the no-`input_id` branch delegates to
  `build_accepted_custody_entry(reader, ...)`, sharing the installed Entry as its boundary.
- Re-pin the staged rows that carry the new ports, and run the release-5 census, symbol-closure and import gates.
- Ship it as release 6 under a fresh pair. Its after-read: a statement submission no longer raises `CUSTODY_FACTORY_REQUIRED`.
- **IAM:** the function role will need a read on whatever the two publication methods read, and on the store's table. Builders,
  state your read set in your packet so Y's pair can carry the grant.

**Open, owned by ~Y2:** naming the service principal whose token IRPT_CUSTDY E2a uses for its scoped POST, following the
`svc-analyst-intake` pattern (CTO msg 2124). It is answered in the release-6 pair.
