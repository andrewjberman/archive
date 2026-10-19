# NEVER-WIDEN ASK -- `OG-cd-3` (RE-CUT under amendment A1) -- apply the `family_depth` READ GRANT: the gateway role may DESCRIBE the silver sweep rules, GET the `backfill-status.json` objects and LIST the silver prefixes and, ONE LEVEL DEEP BY THE GRANT, the eight source roots of `opal-data-assets`, and nothing else; IAM only, no deploy, nothing calls it until `OG-ap-50`

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-cd-3.round-46-apply-the-family-depth-read-grant.md` (GO for Phase A: msg 35929; AMENDMENT A1: msg 35936; method `OG-ap-25`'s). Source: the CTO's round-45 analysis amendment A1, list item 3.
**This ask SUPERSEDES the first cut (`.tf` blob `0d234882a4`, ask sha256 `c2e68d916375`), which `3.0.0_SA_CVO~Z` refused (`NEVER_WIDEN_HALF_CVO_OG-cd-3_20261019.md` @adba2df9a0): that blob's source-root list was RECURSIVE, because it limited `s3:ListBucket` by `s3:prefix` alone, so a call with prefix `schwab/` and no delimiter listed every key under the root at any depth. `1.0.0_SA_CTO~Z`'s half @673a4582d9 lapses with the old blob. All three halves are signed again on the new bytes.**
**The file signed:** `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf` at trunk (`box/sitez`) HEAD `f5e908b78e`, git blob `0f5da21da8d9a68287182a1509b44c6af0a3d75c`, sha256 `3c5a87f6f3b13f6e5ba793abc1ba0ea9706c6112ecad1d7424c9b07d48603243`. It is the old file (written by `OG-cd-1`, commit `046bc2be02`) with THIS ONE change, made by me under the amendment (commit `b2e75e528d`): the `s3:ListBucket` statement is split in two, and the header comment is corrected. `terraform fmt -check` clean. Nothing else changed.
Records: `W/FD_BEFORE.json`, `W/FD_PLAN.txt` (re-run), `W/FD_SIMULATE_PLAN.json` (re-run, 17 cases), `W/cd3_simulate.py`.

## 1. The diff, by file

One file, `family_depth_read_iam.tf`, 29 insertions and 11 deletions:
- the `s3:ListBucket` statement `FamilyDepthSilverPrefixListOnly` keeps `s3:prefix` `StringLike` `["*/silver/", "*/silver/*"]` and loses the eight source roots;
- a NEW statement `FamilyDepthSourceRootListOneLevelOnly` (`s3:ListBucket` on `arn:aws:s3:::opal-data-assets`): `s3:prefix` `StringLike` one of `"<source>/"` for the eight sources AND `s3:delimiter` `StringEquals` `"/"`;
- the header comment, which said a list under a bronze, gold or meta prefix "is refused by the condition", now states what the two list statements admit.
The policy (`gw_family_depth_read`, name `gateway-family-depth-read-policy`, on `aws_iam_role.gw` = `opal-gateway-role`) now has FOUR Allow statements; the other two (`FamilyDepthSweepRuleDescribeOnly`: `events:DescribeRule` on `rule/opal-assets-silver-*-sweep-daily`; `FamilyDepthBackfillStatusReadOnly`: `s3:GetObject` on `opal-data-assets/*/meta/backfill-status.json`) are byte-equal to the first cut (checked by diff). No `*` action, no `*` resource, no write action.

**State read first (Phase A step 1, 2026-10-19T10:02Z; `W/FD_BEFORE.json`):** `opal-gateway-role` holds 24 inline policies and 1 managed attachment (`AmazonSSMManagedInstanceCore`); `gateway-family-depth-read-policy` is NOT among them (no duplicate); no inline policy holds any `events:` action; the one inline policy that names `opal-data-assets` is `gateway-49f-advi-billing-put-policy`, a single `s3:PutObject` on `smartx/49financial/bronze/fee_statement/*` (no read). So the role reads nothing from `opal-data-assets` today and this grant is the first read.
**The plan, re-run on the new blob** (`W/FD_PLAN.txt`; `terraform plan -target=aws_iam_role_policy.gw_family_depth_read -lock=false -input=false`, no `-out`, nothing applied; `market_update_s3_root` fed from `lib/opal_naming.py address()`): `Plan: 1 to add, 0 to change, 0 to destroy.` It prints the new statement and `"s3:delimiter" = "/"`; the lock file did not change.
**Cross-checks read:** the eight sources in the `.tf` equal the union of `local.silver_families[*].sources` in `opal-assets/silver.tf`; `aws events list-rules --name-prefix opal-assets-silver-` lists 6 rules, all matching `opal-assets-silver-*-sweep-daily`.

## 2. The widening, stated plainly, at the new bound

The gateway role (so any process running as the service) may, after the apply:
- **DESCRIBE** the 6 silver sweep rules: their schedule expression and state. No other rule, and no write.
- **GET** any S3 object named `backfill-status.json` under a `meta/` folder of `opal-data-assets` (the `*` in the resource pattern matches slashes, so that file name at any depth). **No other object** is readable.
- **LIST** the bucket in exactly two ways: (a) with a `prefix` that contains a `/silver/` component (`*/silver/` or `*/silver/*`), with or without a delimiter; (b) with a `prefix` that is one of the eight source roots (`schwab/`, `orion/`, `eclipse/`, `blackdiamond/`, `trueshares/`, `pathfinder/`, `msn/`, `smartx/`) **and `delimiter` `/`**. **A source-root list is one level deep BY THE GRANT, not by the caller's courtesy:** without the delimiter, or with any other delimiter, it is refused. A list with no prefix, or under any other prefix, is refused.
- **The breadth that remains, and I say so:** statement (a)'s glob `*/silver/*` admits ANY prefix with a `/silver/` component under any first component, so `bronze/x/silver/y/` is listable (measured below). It admits KEY NAMES (table folders, partition names, dates), never object bodies. `family_depth.py:261` lists silver table prefixes with no delimiter, which is why (a) does not require one. If the signers want (a) narrowed, that is a further change to the `.tf` and re-opens this ask.
- **What a reader learns:** for each family, its schedule, the last sweep time and the frontier date of each silver table, the earliest served partition date (from key names), and the scope folders one level under each of the eight source roots. **No data value, no client data.** It writes nothing and changes no state.
- **Not granted:** any write, delete, tag or invoke; any other bucket; any `GetObject` other than a `backfill-status.json`; any recursive list of a source root; `events:` actions other than `DescribeRule` on the six rules.

**Measured BEFORE the apply, with `iam:SimulateCustomPolicy` on the plan's policy document (a pure read; nothing created or attached; `W/FD_SIMULATE_PLAN.json`, 17 cases, all as expected):** `events:DescribeRule` on a silver rule allowed; `events:PutRule` on it implicitDeny; `DescribeRule` on a rule outside the pattern implicitDeny; `s3:GetObject` on a `backfill-status.json` allowed; `s3:PutObject` on the same key implicitDeny; `s3:GetObject` on a data object implicitDeny; `s3:DeleteObject` implicitDeny; **`list a source root WITH delimiter /` allowed; `NEGATIVE: list a source root with NO delimiter` implicitDeny; `NEGATIVE: list a source root with a delimiter other than /` implicitDeny**; a silver table prefix with no delimiter allowed (the call `family_depth.py:261` makes) and with the delimiter allowed; a gold prefix, a bronze prefix, no prefix and a source outside the eight each implicitDeny; and the breadth case, prefix `bronze/x/silver/y/`, allowed.

## 3. The route that uses it

`app/family_depth.py`'s read, mounted as `GET /api/admin/gateway/families` (owner only), is the cell `OG-cd-2` (the mount), released by `OG-ap-50` (staged behind this order's close AND `OG-cd-2`'s drain). **Until that release nothing calls these actions**: the live release `6b1a9bd292` holds `family_depth.py` inert (not imported, no route).

## 4. The order of acts (Phase B, on the GO that names all three halves signed at the `.tf` blob above)

1. Ledger `nfra-oplgtw-grants-cd3`, entry AND sentinel committed first. Re-read the role's policies (the same 24; no duplicate; any difference is a STOP) and that the `.tf` blob is unchanged.
2. Apply the one policy through `safe-apply`, targeted at `aws_iam_role_policy.gw_family_depth_read`; the plan re-read at the apply must still read `1 to add, 0 to change, 0 to destroy`.
3. Read it back from IAM (`get-role-policy`: exactly FOUR statements, shape and sha256 recorded) and with `simulate-principal-policy` on the live role: ALLOWED `events:DescribeRule` on one real sweep-rule ARN, `s3:GetObject` on a real `backfill-status.json` key ARN, and `s3:ListBucket` with prefix `schwab/` and delimiter `/`; NOT allowed `s3:ListBucket` with prefix `schwab/` and NO delimiter, `events:PutRule` on the same rule ARN and `s3:PutObject` on the same key ARN. `sample_root_prefix` (`schwab/`) goes into `W/FD_APPLIED.json`.
4. The CTO's `CT3` census (real top-level prefixes of `opal-data-assets` beyond the eight roots that hold a `silver/` child) is a read-only Phase B step: listed with `Delimiter="/"` and `Prefix=""` from this seat's own role, counts and prefix NAMES only; the result goes to `W/FD_CT3_CENSUS.json`.
5. Close the ledger; commit; run `cd3.AC2`; report once and send `2.0.0_SA_COO~O` the ledger CLOSED time.

## 5. Both branches

- **After the apply, before `OG-ap-50`:** the grant exists and nothing uses it; no behaviour changes.
- **A call outside the four statements** is refused by IAM (`AccessDenied`): the simulator's negative controls above, repeated on the live role.
- **If the apply fails or a trigger fires:** nothing is half-applied (one resource); the policy is destroyed with the rollback below and an ARMED row is filed naming `2.0.0_SA_COO~O`.

## 6. Rollback

`aws iam delete-role-policy --role-name opal-gateway-role --policy-name gateway-family-depth-read-policy` (or a targeted `terraform destroy` of `aws_iam_role_policy.gw_family_depth_read`). It removes the grant; no state outside the one policy changes. The route is not yet released, so removal breaks nothing; after `OG-ap-50` it would make the route's reads answer `AccessDenied` (the module records each leaf as absent with the reason), not an outage.

## 7. Triggers (any one: destroy the policy, read it absent, file an ARMED row naming `2.0.0_SA_COO~O`)

`terraform plan` at the apply reading anything but `1 to add, 0 to change, 0 to destroy`; the `.tf` blob differing from the signed one; a duplicate of the policy name on the role; the live policy's shape differing from the plan's (not exactly four statements, an extra action, a `*`, a different resource, a source-root list without the delimiter condition); the simulator ALLOWING any negative control (`events:PutRule`, `s3:PutObject`, a source-root list with no delimiter); the role's other 24 policies changing; the gateway service's `NRestarts` above 0 or health not 200 during the apply (the apply touches no process; it is read as a tripwire).

## 8. Gate lines

`process-wide state this change touches: none (IAM policy only; no process, logger, signal, environment or global config), read.` I read the `.tf` whole, `app/family_depth.py` (the list call at line 261 and its delimiter use) and the live role. No code, test, release, deploy, env key or unit change; no object or item written; I run `comp-schedule --drift` at the apply and record what it scanned. The plan and the simulation print the account number inside the ARNs (as every plan in this folder does); no client account number, name or credential appears.

## 9. The three halves (sign ONCE, on the `.tf` blob `0f5da21da8d9a68287182a1509b44c6af0a3d75c` and this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on the `.tf` blob above and this ask's sha256, with the delimiter bound (section 2: a source-root list is one level deep by the grant), the remaining breadth of the `*/silver/*` glob and the first-read-of-the-bucket fact (section 1) read. The `CT3` census is a Phase B step (section 4).

### COO half (`2.0.0_SA_COO~O`)

To be signed on the `.tf` blob above and this ask's sha256, with the plan (`1 to add`, four statements) and the order of acts read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on the `.tf` blob above and this ask's sha256, with the process-wide state line (the verdict 35844) and what a reader learns (section 2: schedules, last sweep, frontier, earliest partition date, key names and one-level scope folders; no data value) read.
