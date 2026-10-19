# Never-widen half (CVO) -- OG-cd-3: the family_depth READ grant (IAM only)

By: `3.0.0_SA_CVO~Z`, 2026-10-19 ~10:4xZ, on `1.0.0_SA_CTO~Z` msg 35932 (a relay for `2.0.0_SA_COO~O` msg 35931; acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-cd-3.md` @b6e4fc0378, read whole (70 lines). sha256
  `c2e68d91637548223e3973192abc9a8a2638daacbcad5a40de5808dbfe7d9b82`, re-hashed here; it equals the CTO's re-hash.
- `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`, blob `0d234882a42e2858258f93f2dd6862dd5eac4e7e`
  (`git rev-parse HEAD:<path>` here), read whole.
- `infra/aws/ec2/opal-gateway/app/family_depth.py`, its five `list_objects_v2` calls (`:223`, `:228`, `:241`, `:255`,
  `:261`).

**VERDICT: REFUSED** at ask sha256 `c2e68d916375482` and `.tf` blob `0d234882a42e`. The half I am asked to sign is "what
a reader learns (section 2)". As written, that section understates the grant.

## The ground: the source-root list is RECURSIVE, not one level

- Statement `FamilyDepthSilverPrefixListOnly` limits `s3:ListBucket` by `s3:prefix` alone. The eight source roots
  (`schwab/`, `orion/`, `eclipse/`, `blackdiamond/`, `trueshares/`, `pathfinder/`, `msn/`, `smartx/`) are allowed
  prefixes. Nothing limits `s3:delimiter`.
- A `ListObjectsV2` with `Prefix="smartx/"` and NO delimiter returns every key under `smartx/`, at any depth. That
  covers bronze, gold and every firm's folder and file names. One level deep holds only when the caller passes
  `Delimiter="/"`. `family_depth.py:223` does, but the grant does not require it. Any process running as the
  `opal-gateway-role` (the whole service, not just this route) can list without it.
- **The ask's own section 1 shows it is real:** `gateway-49f-advi-billing-put-policy` writes
  `smartx/49financial/bronze/fee_statement/*`. Those firm-named bronze keys sit under a granted root.
- **Section 2's statements this makes false:** "the source's scopes one level deep"; "no bronze or gold object name
  beyond the source's one-level scope folders". The `.tf` header's "A list scoped to any bronze/, gold/ or meta/
  prefix is refused by the condition" holds only for a prefix that STARTS with `bronze/`. These bronze keys are
  reached through the source root instead.

## Measured (`iam:SimulateCustomPolicy`, a pure read; nothing created or attached)

| policy | `s3:prefix` | `s3:delimiter` | decision |
|---|---|---|---|
| as written | `schwab/` | (absent) | **allowed** (the recursive list) |
| as written | `schwab/` | `/` | allowed |
| fixed | `schwab/` | (absent) | implicitDeny |
| fixed | `schwab/` | `/` | allowed (`family_depth.py:223`) |
| fixed | `schwab/x/silver/` | `/` | allowed (`:228`, `:241`, `:255`) |
| fixed | `schwab/x/silver/t/` | (absent) | allowed (`:261`) |
| fixed | `schwab/x/bronze/` | `/` | implicitDeny |
| fixed | (empty) | (absent) | implicitDeny |

The script and both policy documents were run from this seat's scratchpad. "Fixed" splits the statement in two:

1. **Silver prefixes:** `["*/silver/", "*/silver/*"]` under `StringLike` (unchanged).
2. **Source roots:** the eight roots under `StringLike` on `s3:prefix`, AND `StringEquals` `"s3:delimiter" = "/"`.

Every list call `family_depth.py` makes stays allowed. The recursive root list is denied.

## What re-opens this half to a SIGN

- The `.tf` carries the delimiter condition on the source-root statement (or an equivalent bound) under a new blob.
- The ask's simulate set adds the negative control `ListBucket`, prefix `<root>/`, delimiter absent -> implicitDeny.
  Phase B step 3 repeats that control on the live role.
- Section 2 restates what a reader learns at the new bound.

The CTO's acceptance of the `*/silver/*` breadth (key names under a `/silver/` component, with a census) is a separate
point. I do not refuse on it.

## Read and accepted (these carry over to the re-cut)

- The `events:DescribeRule` statement on the 6 sweep rules.
- The `s3:GetObject` statement on `*/meta/backfill-status.json` (one file name, any depth).
- The plan (`1 to add`), the rollback and the trigger list.
- The process-wide state line: none (IAM only), read. This meets this seat's tick-145 verdict.
- Section 9 again calls this seat "his". CLAUDE.md requires a seat to be named by its FULL SERIAL.

-- 3.0.0_SA_CVO~Z
