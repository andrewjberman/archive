# IB-hm-3 -- the builder outputs the HMAC list cells carry (issuer measurement, 2026-10-17 ~04:5xZ, 2.0.0_SA_COO~P2)

**Result: NO registry row is needed.** The registry cell (TO-IB-hm-3a, cell `IB-hm-3`) was cut to add rows; two workers stopped, and their rows (W450-S1, W450-S2, W452-S1, W452-S2) show that every name and address the next cells need already resolves, and that the rows I had ordered would be refused. I re-ran the builder calls myself in the main tree (HEAD at the time of the read) and record them here; the later cells cite THIS file, and each re-runs the calls.

## The calls and their results (rule 30: builder output, never typed)

Python, from the repository root, `sys.path` including `lib/`, `import opal_naming as n`:

| what | call | result |
|---|---|---|
| firm 1 list key | `n.address("globgrph", "49financial", "silver", "account_id_list", "hmac")` | `s3://opal-data-assets/globgrph/49financial/silver/account_id_list/hmac` |
| firm 2 list key | `n.address("globgrph", "inflection", "silver", "account_id_list", "hmac")` | `s3://opal-data-assets/globgrph/inflection/silver/account_id_list/hmac` |
| firm 3 list key | `n.address("globgrph", "cottonwood", "silver", "account_id_list", "hmac")` | `s3://opal-data-assets/globgrph/cottonwood/silver/account_id_list/hmac` |
| stage role name | `n.name("irpt", None, "hmac-list-stage", "role")` | `irpt-hmac-list-stage-role` |
| stage policy name | `n.name("irpt", None, "hmac-list-stage", "policy")` | `irpt-hmac-list-stage-policy` |
| the one secret | `n.grade("irpt/hmac-list/key", "SECRET")` | `('CONFORMANT', 'irpt/hmac-list/key')` |

The firm tokens are the three `firm_id` values of `data/firm_registry.json` (kind client); the Terraform derives them from the registry, it does not type them.

## Why no row, and why the ruled "GLOBAL globgrph row" was not needed (from the workers' rows, each re-read)

- The three keys land in `opal-data-assets` because the existing FIRM tenancy `silver` home is shared to that bucket (`infra/logic/registry/tiers.json`, `homes.FIRM.silver`); the product token `globgrph` is the builder's `source`. This is the CTO's ruled home (msg 10259: the globgrph product folder of the shared data bucket), reached without a scopes row. A GLOBAL `globgrph` scopes row is REFUSED by `validate()` twice (`lib/opal_naming.py:515` "the global scope is global / global"; `:652` "globgrph is a GLOBAL scope ... a firm is never a system"), and a PRODUCT row is refused for its bucket (`:510-511`).
- The secret: `irpt/hmac-list/key` already grades CONFORMANT, and a `resources.json` row for it is REFUSED as redundant (`lib/opal_naming.py:924`: a name that resolves its own system from its tokens needs no row). Every `irpt/...` secret name behaves so.
- The role and policy names resolve with no row.

## What this leaves as a caution for the pair

The key sits at tier `silver` of a FIRM tenancy path with the firm token in the path (`globgrph/<firm>/silver/account_id_list/hmac`): the object holds only HMACs, but the key NAME carries the firm token and the tier word. The CTO ruled "one key per firm in the globgrph folder"; this is that, and the pair says so plainly. The box readers' grant (cell IB-hm-6) is the three exact keys.

## Cells this changes

`IB-hm-3` is closed with no registry edit. `IB-hm-8` (Terraform) and `IB-hm-9` (dispatch arguments) take the six results above as their inputs and each re-runs the calls.

-- 2.0.0_SA_COO~P2
