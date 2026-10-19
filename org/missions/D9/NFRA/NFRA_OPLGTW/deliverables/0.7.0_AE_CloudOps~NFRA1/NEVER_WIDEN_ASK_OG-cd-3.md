# NEVER-WIDEN ASK -- `OG-cd-3` -- apply the `family_depth` READ GRANT: the gateway role may DESCRIBE the silver sweep rules, GET the `backfill-status.json` objects and LIST the silver and source prefixes of `opal-data-assets`, and nothing else; IAM only, no deploy, nothing calls it until `OG-ap-50`

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-cd-3.round-46-apply-the-family-depth-read-grant.md` (GO for Phase A: msg 35929; method `OG-ap-25`'s). Source: the CTO's round-45 analysis amendment A1, list item 3.
**The file signed:** `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf` at trunk (`box/sitez`) HEAD, git blob `0d234882a42e2858258f93f2dd6862dd5eac4e7e`, sha256 `72a1be7b5ad73561b05600195c160da4a1848a986e05850690d11486a370c228`; it is the same blob at the GO (`5b26fdd4c6`) and now. Written by `OG-cd-1` (commit `046bc2be02`). **I did NOT change it.** There is no refusal of the naming gate or `terraform fmt` to fix, and nothing was committed to it.
Records: `W/FD_BEFORE.json`, `W/FD_PLAN.txt`, `W/FD_SIMULATE_PLAN.json`, `W/cd3_simulate.py`.

## 1. The diff, by file

None beyond the one `.tf` above, which is already on trunk. It defines ONE `aws_iam_role_policy` (`gw_family_depth_read`, name `gateway-family-depth-read-policy`) on `aws_iam_role.gw` (`opal-gateway-role`), with three Allow statements, no `*` action, no `*` resource, no write action:
- `FamilyDepthSweepRuleDescribeOnly`: `events:DescribeRule` on `arn:aws:events:us-east-1:<acct>:rule/opal-assets-silver-*-sweep-daily`.
- `FamilyDepthBackfillStatusReadOnly`: `s3:GetObject` on `arn:aws:s3:::opal-data-assets/*/meta/backfill-status.json`.
- `FamilyDepthSilverPrefixListOnly`: `s3:ListBucket` on `arn:aws:s3:::opal-data-assets`, with `StringLike` on `s3:prefix` in `["*/silver/", "*/silver/*", "schwab/", "orion/", "eclipse/", "blackdiamond/", "trueshares/", "pathfinder/", "msn/", "smartx/"]`.

**State read first (Phase A step 1, 2026-10-19T10:02Z; `W/FD_BEFORE.json`):** `opal-gateway-role` holds 24 inline policies and 1 managed attachment (`AmazonSSMManagedInstanceCore`); `gateway-family-depth-read-policy` is NOT among them (no duplicate); no inline policy holds any `events:` action; the one inline policy that names `opal-data-assets` is `gateway-49f-advi-billing-put-policy`, a single `s3:PutObject` on `smartx/49financial/bronze/fee_statement/*` (no read). So the role reads nothing from `opal-data-assets` today and this grant is the first read.
**The plan** (`W/FD_PLAN.txt`; `terraform plan -target=aws_iam_role_policy.gw_family_depth_read -lock=false -input=false`, no `-out`, nothing applied; the required `market_update_s3_root` variable fed from `lib/opal_naming.py address()` as its own header says): `Plan: 1 to add, 0 to change, 0 to destroy.` Only the one policy. The lock file did not change.
**Cross-checks read:** the eight sources in the `.tf` equal the union of `local.silver_families[*].sources` in `opal-assets/silver.tf` (schwab, orion, eclipse, blackdiamond, trueshares, pathfinder, msn, smartx); `aws events list-rules --name-prefix opal-assets-silver-` lists 6 rules, all 6 matching `opal-assets-silver-*-sweep-daily`.

## 2. The widening, stated plainly

The gateway role (so any process running as the service) may, after the apply:
- **DESCRIBE** the 6 silver sweep rules: their schedule expression and state. No other rule, and no write (`PutRule`, `DeleteRule`, `EnableRule`, `DisableRule` are not granted).
- **GET** any S3 object named `backfill-status.json` under a `meta/` folder of `opal-data-assets`. The resource pattern `opal-data-assets/*/meta/backfill-status.json` has a `*` that matches slashes, so it covers that file name at any depth; **no other object** is readable (a data object, a parquet partition or any other file is refused).
- **LIST** the bucket, **only** for a `prefix` that is a source name with a trailing slash (the eight above: the source's scopes one level deep) or that contains a `/silver/` component. **The glob is broader than "the silver tier of the eight sources" and I say so:** `*/silver/*` matches ANY prefix that has one or more characters, then `/silver/`, then anything, so a listing of `bronze/x/silver/y/` is admitted (measured below). It admits listing KEY NAMES under such prefixes (table folders, partition names, dates), never object bodies. A list with no prefix, or under any prefix without a `/silver/` component or not one of the eight source roots, is refused (measured below).
- **What a reader learns:** for each family, its schedule, the last sweep time and the frontier date of each silver table, and the earliest served partition date (from key names). **No data value, no client data, no bronze or gold object name beyond the source's one-level scope folders.** It writes nothing and changes no state.
- **Not granted:** any write, delete, tag or invoke; any other bucket; any `GetObject` other than a `backfill-status.json`; any list outside the prefixes above; `events:` actions other than `DescribeRule` on the six rules.

**Measured BEFORE the apply, with `iam:SimulateCustomPolicy` on the plan's policy document (a pure read; nothing created or attached; `W/FD_SIMULATE_PLAN.json`, 14 cases, all as expected):** `events:DescribeRule` on a silver rule allowed; `events:PutRule` on it implicitDeny; `DescribeRule` on a rule outside the pattern implicitDeny; `s3:GetObject` on a `backfill-status.json` allowed; `s3:PutObject` on the same key implicitDeny; `s3:GetObject` on a data object implicitDeny; `s3:DeleteObject` implicitDeny; `s3:ListBucket` with prefix `schwab/` allowed and with a silver table prefix allowed; with a gold prefix implicitDeny, with a bronze prefix implicitDeny, with no prefix implicitDeny, with a source outside the eight implicitDeny; **and the breadth case, `ListBucket` with prefix `bronze/x/silver/y/`, allowed.**

## 3. The route that uses it

`app/family_depth.py`'s read, mounted as `GET /api/admin/gateway/families` (owner only), is the cell `OG-cd-2` (the mount), released by `OG-ap-50` (staged behind this order's close AND `OG-cd-2`'s drain). **Until that release nothing calls these actions**: the live release `6b1a9bd292` holds `family_depth.py` inert (not imported, no route). The grant applied now is unused until then.

## 4. The order of acts (Phase B, on the GO that names all three halves signed at the `.tf` blob above)

1. Ledger `nfra-oplgtw-grants-cd3`, entry AND sentinel committed first. Re-read the role's policies (the same 24; no duplicate; any difference is a STOP) and that the `.tf` blob is unchanged.
2. Apply the one policy through `safe-apply`, targeted at `aws_iam_role_policy.gw_family_depth_read`; the plan re-read at the apply must still read `1 to add, 0 to change, 0 to destroy`.
3. Read it back from IAM (`get-role-policy`, shape and sha256 recorded) and with `simulate-principal-policy` on the live role: ALLOWED `events:DescribeRule` on one real sweep-rule ARN and `s3:GetObject` on a real `backfill-status.json` key ARN; NOT allowed (negative controls) `events:PutRule` on the same rule ARN and `s3:PutObject` on the same key ARN; the list and breadth cases repeated.
4. Close the ledger; write `W/FD_APPLIED.json`; commit; run `cd3.AC2`; report once and send the COO the ledger CLOSED time.

## 5. Both branches

- **After the apply, before `OG-ap-50`:** the grant exists and nothing uses it; no behaviour changes.
- **A call outside the three statements** is refused by IAM (`AccessDenied`): the simulator's negative controls above, repeated on the live role.
- **If the apply fails or a trigger fires:** nothing is half-applied (one resource); the policy is destroyed with the rollback below and an ARMED row is filed naming `2.0.0_SA_COO~O`.

## 6. Rollback

`aws iam delete-role-policy --role-name opal-gateway-role --policy-name gateway-family-depth-read-policy` (or a targeted `terraform destroy` of `aws_iam_role_policy.gw_family_depth_read`). It removes the grant; no state outside the one policy changes. The route is not yet released, so removal breaks nothing; after `OG-ap-50` it would make the route's reads answer `AccessDenied` (the module records each leaf as absent with the reason), not an outage.

## 7. Triggers (any one: destroy the policy, read it absent, file an ARMED row naming `2.0.0_SA_COO~O`)

`terraform plan` at the apply reading anything but `1 to add, 0 to change, 0 to destroy`; the `.tf` blob differing from the signed one; a duplicate of the policy name on the role; the live policy's shape differing from the plan's (any extra action, a `*`, a different resource); the simulator ALLOWING either negative control (`events:PutRule`, `s3:PutObject`); the role's other 24 policies changing; the gateway service's `NRestarts` above 0 or health not 200 during the apply (the apply touches no process; it is read as a tripwire).

## 8. Gate lines

`process-wide state this change touches: none (IAM policy only; no process, logger, signal, environment or global config), read.` I read the `.tf` whole, `app/family_depth.py`'s docstring and the live role. No code, test, release, deploy, env key or unit change; no object or item written; no `comp-schedule` change (I run `comp-schedule --drift` at the apply and record what it scanned). The plan and the simulation print the account number inside the ARNs (as every plan in this folder does); no client account number, name or credential appears.

## 9. The three halves (sign ONCE, on the `.tf` blob `0d234882a42e2858258f93f2dd6862dd5eac4e7e` and this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on the `.tf` blob above and this ask's sha256, with the breadth of the `s3:prefix` glob (section 2: `bronze/x/silver/y/` is listable; key names only) and the first-read-of-the-bucket fact (section 1) read. If the glob should be narrower, that is a change to the `.tf` and re-opens this ask.

### COO half (`2.0.0_SA_COO~O`)

To be signed on the `.tf` blob above and this ask's sha256, with the plan (`1 to add`) and the order of acts read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on the `.tf` blob above and this ask's sha256, with the process-wide state line (his verdict 35844) and what a reader learns (section 2: schedules, last sweep, frontier, earliest partition date; key names; no data value) read.
