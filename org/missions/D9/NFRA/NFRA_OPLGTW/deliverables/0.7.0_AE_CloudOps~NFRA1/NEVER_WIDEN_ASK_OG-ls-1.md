# NEVER-WIDEN ASK -- `OG-ls-1` -- narrow the gateway role's silver `s3:ListBucket` grant from "any first component" to the eight sources; ONE list in ONE statement of ONE policy; a strict NARROWING; IAM only, no deploy, no code

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ls-1.round-47-narrow-the-silver-list-grant-to-the-eight-sources.md` (GO for Phase A: msg 36166; method `OG-cd-3`'s). Source: the CTO's round-46 analysis, "the `*/silver/*` ListBucket narrowing", from the CTO half of `OG-cd-3` ("narrow to `<source>/*/silver/*` if the count is non-zero"; the `OG-cd-3` census `W/FD_CT3_CENSUS.json` counted 4).
**Phase A writes NOTHING to IAM and applies nothing in any form.** The only repo change besides records is the one `.tf` edit below, committed at `1017106c75`.

**The file signed:** `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`, git blob `42fee26095781c61a1574b1f20c8a838aff15887`, sha256 `a88ffa655b980b285965baaa1006d8a2907acea573b840f9cb18eaf707314621`, at commit `1017106c75` on `box/sitez` (local, not pushed).
**This is the ONLY edit.** Blob BEFORE `0f5da21da8d9a68287182a1509b44c6af0a3d75c` (sha256 `3c5a87f6f3b13f6e5ba793abc1ba0ea9706c6112ecad1d7424c9b07d48603243`, the file `OG-cd-3` applied); blob AFTER as above. `terraform fmt -check` clean.
Records: `W/LS_BEFORE.json`, `W/LS_PLAN.txt`, `W/LS_SIMULATE_PLAN.json` (14 cases, all as expected), `W/ls1_before.py`, `W/ls1_simulate.py`.

## 1. The diff

One list, in one statement (`FamilyDepthSilverPrefixListOnly` of `aws_iam_role_policy.gw_family_depth_read`, policy name `gateway-family-depth-read-policy` on `opal-gateway-role`):
- BEFORE: `"s3:prefix" = ["*/silver/", "*/silver/*"]`
- AFTER: `"s3:prefix" = flatten([for s in local.family_depth_sources : ["${s}/*/silver/", "${s}/*/silver/*"]])`, which is 16 patterns, two for each of `schwab orion eclipse blackdiamond trueshares pathfinder msn smartx`.
- The file's header comment about statement (a), which said the glob admits ANY prefix with a `/silver/` component under any first component, now says the glob is per source (7 insertions, 5 deletions in all, all in comments and that one list).
The other three statements (`FamilyDepthSweepRuleDescribeOnly`, `FamilyDepthBackfillStatusReadOnly`, `FamilyDepthSourceRootListOneLevelOnly`) are byte-equal; the file keeps FOUR Allow statements, one resource, and the three read actions `events:DescribeRule`, `s3:GetObject`, `s3:ListBucket`. No `*` action, no `*` resource.

**State read first (`W/LS_BEFORE.json`, 2026-10-20T10:16Z):** the policy is live with four statements; policy hash prefix `2dd3ee621be1436d`; its silver patterns read `*/silver/` and `*/silver/*` as expected; the role holds 25 inline policies. `iam:SimulatePrincipalPolicy` on the live role before the change: `s3:ListBucket` with prefix `bloomberg/global/silver/`, `gateway/global/silver/` and `yahoo/g/silver/` each read `allowed` (the defect), and `schwab/x/silver/t/` `allowed`.
**The plan** (`W/LS_PLAN.txt`; `terraform plan -target=aws_iam_role_policy.gw_family_depth_read -lock=false -input=false`, no `-out`, nothing applied; `market_update_s3_root` fed from `lib/opal_naming.py address()`): `Plan: 0 to add, 1 to change, 0 to destroy.` It shows the two old globs removed and the sixteen per-source patterns added (`<source>/*/silver/` and `<source>/*/silver/*`). No other attribute changes.

## 2. The widening: NONE

This is a strict narrowing: the set of listable prefixes after is a strict subset of the set before. Every pattern added is matched by an old pattern (`schwab/*/silver/` is matched by `*/silver/`).
**What stops being listable:** any prefix with a `/silver/` component under a first component OUTSIDE the eight sources. The `OG-cd-3` census found four such first components holding a silver child (`bloomberg`, `commonwealth`, `gateway`, `yahoo`); the glob also stopped admitting a `bronze/x/silver/y/`-shaped prefix (the breadth case the `OG-cd-3` ask named) and any other first component. **Nothing the gateway runs reads them through this policy:** `app/family_depth.py` lists `<source>/<scope>/silver/<table>/` for the eight sources only; the gateway's client tools read `commonwealth/cottonwood/silver` through other policies (the Schwab and client readers), which this order does not touch. Phase B proves it with one `family_depth` read on the host.
**What stays listable:** a silver prefix under each of the eight sources (with or without a delimiter, as `family_depth.py` makes the call), and each source root WITH delimiter `/` (statement (b), untouched). No grant is added; no principal other than `opal-gateway-role` is involved.

## 3. The order of acts (Phase B, on a GO that names all three halves signed at the blob above)

1. Ledger `nfra-oplgtw-grants-ls1`, entry AND sentinel committed first. Re-read the policy (four statements, patterns still `*/silver/` and `*/silver/*`, hash prefix `2dd3ee621be1436d`) and that the `.tf` blob is still `42fee26095`; any difference is a STOP. Run `comp-schedule --drift` and record what it scanned.
2. ONE apply through `safe-apply`, targeted at `aws_iam_role_policy.gw_family_depth_read`; the plan re-read at the apply must still read `0 to add, 1 to change, 0 to destroy`.
3. Read the policy back from IAM (`get-role-policy`: exactly FOUR statements, shape and hash recorded) and simulate against the LIVE role: ALLOWED `s3:ListBucket` with prefix `<real source>/<real scope>/silver/<real table>/` (found by a `list-objects-v2 --delimiter / --max-keys 5` walk); NOT allowed with prefix `bloomberg/global/silver/`, `gateway/global/silver/`, `yahoo/g/silver/`; source-root list with delimiter `/` allowed and without it NOT allowed; the unchanged statements still ALLOW `events:DescribeRule` on one real sweep-rule ARN and `s3:GetObject` on one real `backfill-status.json` key ARN while `events:PutRule` and `s3:PutObject` on the same ARNs are NOT allowed.
4. Run the `family_depth` read ONCE on the host from the deployed tree under the hard guard, as the instance role; `families` and `denominator` must equal `W/FWD20_DRIVEN_READ.json` (the round-46 driven read) or I say why not.
5. Close the ledger, write `W/LS_APPLIED.json`, commit, run `ls1.AC2`, report once, and send `2.0.0_SA_COO~O` the ledger CLOSED time.

## 4. Both branches (the simulator, before any apply; `W/LS_SIMULATE_PLAN.json`, `iam:SimulateCustomPolicy` on the live policy with only the silver list replaced; nothing created or attached)

- **ALLOWED:** `s3:ListBucket` with prefix `schwab/x/silver/t/` (no delimiter) and `smartx/x/silver/t/` with delimiter `/`; the source-root list `schwab/` WITH delimiter `/`; `events:DescribeRule` on a silver sweep rule; `s3:GetObject` on a `backfill-status.json`.
- **NEGATIVE (all `implicitDeny`):** silver list under `bloomberg`, under `gateway`, under `yahoo` and under `commonwealth`; a source-root list with NO delimiter; a bronze-rooted prefix with a `/silver/` component; a gold prefix under a source; `events:PutRule` on the same rule; `s3:PutObject` on the same key.
- **If the apply fails or a trigger fires:** one resource, one attribute; revert per section 5 and file an ARMED row naming `2.0.0_SA_COO~O`.

## 5. Rollback

Revert the one list to `["*/silver/", "*/silver/*"]` in the `.tf` and apply again through `safe-apply` (the rollback is a re-widening to the state `OG-cd-3` signed; it is taken only on a trigger). The old policy hash prefix `2dd3ee621be1436d` is in `W/LS_BEFORE.json`. Nothing outside this one policy changes either way; no data, process or release is involved.

## 6. Triggers (any one: revert the list, apply, read it back, file an ARMED row naming `2.0.0_SA_COO~O`)

The `family_depth` read run once on the host after the apply fails, or answers fewer families than before; the live policy's shape is not four statements, or carries an extra action, a `*`, or a different resource; any decision in the live simulation differs from the plan's simulation (the three census prefixes must read NOT allowed, the source prefix allowed); the plan re-read at the apply reads anything but `0 to add, 1 to change, 0 to destroy`; the `.tf` blob differs from the signed one; the role's other 24 inline policies change.

## 7. Gate lines

`process-wide state this change touches: none (IAM policy only; no process, logger, signal, environment or global config), read.` I read the `.tf` whole before and after, `app/family_depth.py`'s list calls (named in the `OG-cd-3` ask), the live policy and the `OG-cd-3` census. No code, test, release, deploy, env key or unit change; no object or item written; Phase A touches IAM with reads and simulations only. No client account number, name or credential appears in any record (the plan and the simulation carry no account number; the simulation's rule ARN is built at run time and is not saved).

## 8. The three halves (sign ONCE, on the `.tf` blob `42fee26095781c61a1574b1f20c8a838aff15887` and this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on the `.tf` blob above and this ask's sha256, with the per-source form (section 1), the statement that nothing the gateway runs reads the removed prefixes through this policy (section 2) and the Phase B host read as the proof (section 3 step 4) read.

### COO half (`2.0.0_SA_COO~O`)

To be signed on the `.tf` blob above and this ask's sha256, with the plan (`0 to add, 1 to change, 0 to destroy`), the 14 simulation cases and the order of acts read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on the `.tf` blob above and this ask's sha256, with the process-wide state line (the verdict 35844), the widening statement (NONE, a strict narrowing) and what stops being listable (section 2) read.
