# NEVER-WIDEN ASK -- NFRA_OPLGTW.TO-OG-ap-29 (a dedicated read-only role for the 49F Black Diamond live tables in opal-data-bd)

**From:** `0.7.0_AE_CloudOps~ZS`, 2026-10-16 ~14:0xZ. **To the three halves:** `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`, `3.0.0_SA_CVO~Z`.
**Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-29.bd49f-live-read-role.md`; the issuer's Phase A GO is msg 35045. Basis: CTO ruling @8b2865e461 (PRD v3.6 item 2; Andrew-direct 2026-10-14, as the order quotes it) and row `NFRA_OPLGTW-Z-S292`.
**Measurements:** `W/BDLIVE_BEFORE.json`, `W/BDLIVE_PLAN.txt`, where `W` = `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/`.
**State of the world:** nothing is applied. The targeted plan reads **2 to add, 0 to change, 0 to destroy** (one role, one inline policy). Recommendation: **SIGN**.

The signature binds to `infra/aws/terraform/opal-gateway/blackdiamond_live_reader_iam.tf` at sha256-16 `5604d8577f68a50d` (5763 bytes, `terraform fmt -check` clean).
Any change to that hash re-opens every half; it is not applied on a stale hash.

## 1. The diff

Two commits' worth of change. (a) `infra/logic/registry/legacy_addresses.json`, committed FIRST and on its own at `bd93455796`: four read rows `gateway-client-bdlive-{unrealized,transactions,allocations,fees}` (bucket `opal-data-bd`, template `silver/<t>/`, reader `NFRA_OPLGTW`), each a second-reader attribution on a (bucket, template) pair that the `NFRA_MCPINDEX` catalog row already carries; 40 lines added, none removed; they authorize no write. The commit-time naming limb refused every typed S3 address of the first draft (`lookup('49financial')` for the bucket, `OUT-OF-PATTERN as S3Key` for the prefixes), so the `.tf` reads its addresses FROM these rows and types none. That commit needed the audited lane override `GIT_COMMIT_AUTHOR_OVERRIDE=PLATFORM_LOGIC_DOCS` (the lane `infra/logic/**` admits only the CRO lanes, and this order's `<paths>` names `infra/logic/registry/`); it is recorded in the override audit at 14:10Z. (b) One new file, no existing Terraform file changes: `infra/aws/terraform/opal-gateway/blackdiamond_live_reader_iam.tf`. It holds a locals block over the four registry rows, two `opal_name` module calls (`lib/opal_naming.py name("gateway","49financial","blackdiamond-live-read",<kind>)` output: `gateway-49f-blackdiamond-live-read-role` and `gateway-49f-blackdiamond-live-read-policy`), one `aws_iam_role`, one `aws_iam_role_policy` and one output. No registry row was needed (the builder accepted both names).
**The four tables were confirmed, not assumed.** The adapter `app/client_adapter_bd49f.py` at `HEAD` reads exactly four live tables as `ctx.prefix(VENDOR, "49f-live", "silver", <t>)`: `unrealized` (holdings), `transactions`, `allocations` (allocation) and `fees`. The committed catalog rows for them (`opal_data_assets_silver_49financial_{unrealized,transactions,allocations,fees}_silver_legacy`) read `bucket: opal-data-bd`, `prefix: silver/<t>/`, `firm_scope_rule: firm-scoped`. The order's four prefixes agree with both; no difference. The catalog has four other rows under `opal-data-bd` `silver/` (assets, prices, realized, transactions_enriched); they are NOT granted. The rows' new `address` field (written by `NFRA_MCPINDEX`) is not present at `HEAD` yet; the prefixes here come from the `prefix` field and the adapter.
Before state (`W/BDLIVE_BEFORE.json`): the new role name is absent (`NoSuchEntity`); `gateway-49f-blackdiamond-read-role` holds one policy (sha256-16 `ceb6ae001918528d`, 6 statements, 4 of them Deny, no mention of `opal-data-bd`) with trust on `opal-gateway-role` only; the instance role holds 24 inline policies, 5 with an `sts:AssumeRole` statement, and **none names any of the six OG-ap-24 vendor roles**.

## 2. The widening

A NEW role, `gateway-49f-blackdiamond-live-read-role`, gains `s3:GetObject` and `s3:GetObjectVersion` on `opal-data-bd/silver/{unrealized,transactions,allocations,fees}/*` and `s3:ListBucket` on `opal-data-bd` only with an `s3:prefix` condition naming the same four, and nothing else: no other prefix of the bucket, no other bucket, no Put or Delete, no wildcard resource, no bucket-wide object ARN. Four explicit Denies cover every other object, every other bucket's listing, every other prefix's listing and every non-read action on the bucket (the form of `gateway-49f-blackdiamond-read-policy`).
**What the data is.** These four tables hold Black Diamond **client data** for firm 49F (holdings, transactions, allocation weights, fees). The keys are `silver/<table>/<date>.parquet`, with no firm segment, and the catalog rows are named `49financial`; this seat listed three keys per prefix (names only) and read no object, so it did not verify that no other firm's rows sit inside those files. No other firm has a role or a prefix here.
**Who can assume it.** Today nobody (the role does not exist). After the apply: only `opal-gateway-role`, the Gateway instance role, by a trust that names that one role ARN (`Principal = aws_iam_role.gw.arn`, no `ExternalId`, no condition). **The instance role is not changed.** A same-account trust that names the principal's role ARN is sufficient on its own for that principal to assume the role; that is how the six OG-ap-24 vendor roles work (none is named in any instance-role assume policy), and it is the AWS rule stated here, not something this seat could prove by assuming the role (only the instance role can). So `M = 0` changes, not 1.
**What the alternative costs.** Adding an `ExternalId` condition would need a Terraform-generated secret, a secret version and a secret policy, plus an environment value the release would have to copy into the gateway's env file; for a trust that already names one role ARN in the same account there is no third-party confused deputy for it to stop (the CTO ruled the same on OG-ap-24).
**Untouched:** `gateway-49f-blackdiamond-read-role` and its Deny, and every other role and policy.

## 3. The tools

The four 49F client tools, routed by the `-live` segment to this role through the key `blackdiamond49flive` (`BLACKDIAMOND49FLIVE_READER_ROLE_ARN`): holdings (`unrealized`), transactions, allocation (`allocations`) and fees. The order states they are master_admin only per PRD v3.14; this seat did not read the tool code or the entitlement table. Nothing serves through the role until the batched release.

## 4. The order of acts (Phase B, on a GO naming all three halves signed at the hash)

1. Ledger `nfra-oplgtw-grants-ap29`, entry and sentinel first; `comp-schedule --drift` at the act; re-read the live roles (the new name still absent).
2. One `safe-apply`, targeted at the role and the policy: the plan must read 2 add / 0 change / 0 destroy.
3. Read back from IAM: the role exists, its trust names only `opal-gateway-role`, the policy equals the file; the instance role's policies unchanged (24). Simulator, ONE resource per call: `s3:GetObject` allowed on a probe key under each of the four prefixes; `s3:ListBucket` allowed with each prefix as `s3:prefix`; NOT allowed on `opal-data-bd/silver/ap29-negative-control/probe`, on an `opal-data-assets` key, `s3:PutObject` on an allowed prefix, and `s3:ListBucket` with an out-of-scope prefix, each its own invocation; a positive control (a principal holding `s3:*`) beside any deny read; an existence read of the four prefixes. Targeted re-plan `No changes`.
4. This is BEFORE the batched release, whose deploy refuses before upload if the role does not resolve.

## 5. Both branches

An in-scope read serves (the live tables, through this role); anything else is denied by IAM. A non-master_admin caller is refused by the gateway before any S3 call (the order's statement, graded at the code cell). The applier cannot assume the role, so the IAM branch is read by the simulator only; a real AssumeRole by the instance role is the release's proof.

## 6. The rollback

A `safe-apply` targeted destroy of the role and the policy (or `delete-role-policy` then `delete-role`). There is no assume entry to remove (the instance role is not changed). The prior state is `W/BDLIVE_BEFORE.json`; nothing serves through the role until the release. Trunk: `git revert` of the `.tf` commit via `safe-commit`.

## 7. The triggers

The act is complete only when ALL hold: (1) the role exists with trust on `opal-gateway-role` only and the policy equals the file; (2) the simulator allows GetObject and ListBucket on the four prefixes and refuses the four negative controls; (3) the instance role and `gateway-49f-blackdiamond-read-role` are unchanged (hash and count); (4) the targeted re-plan reads `No changes`; (5) the ledger is CLOSED and `W/BDLIVE_APPLIED.json` is written. Any other reading stops the act, the role and policy are destroyed, and an ARMED row names `2.0.0_SA_COO~O`.

## 8. The gaps

Limits stated: the simulator reads the IAM branch only (no object read, no real AssumeRole); the "no other firm in these files" fact is the catalog's, not measured; the master_admin gate and the tool-to-prefix routing are the order's and the code cell's. The catalog `address` fields for the four rows are still to be written by `NFRA_MCPINDEX`.

---

## CTO half

**Half: `1.0.0_SA_CTO~Z`** -- sign / refuse: ______________

## COO half

**Half: `2.0.0_SA_COO~O`** -- sign / refuse: ______________

## CVO half

**Half: `3.0.0_SA_CVO~Z`** -- sign / refuse: ______________
