# IAM-s-7 -- Historical remediation completion, established on the artifact

Method for every plan below: read the plan's own proposed change, then go to the thing it said it
would change (Terraform source, or the live IAM object read directly via `aws iam get-*` /
`list-*`) and read that. Verdicts are never drawn from which subfolder a plan document sits in
(`active/` vs `completed/`); a plan's folder is not consulted anywhere in this analysis.

Repo HEAD at the time of this grading: `21d42b3b16` (this worktree).

---

## Plan 1 -- `infra/security/remediation/active/iam-least-privilege-rollback-plan.md`

Pinned vintage: `6aad42da0d`, 2026-02-17, Andrew Berman ("UNTOUCHED SINCE FEBRUARY" per brief F10).
Re-confirmed at grading time: `git log -1 -- infra/security/remediation/active/iam-least-privilege-rollback-plan.md`
still returns `6aad42da0d` -- nothing moved it mid-round.

**What it proposed:** a Blue-Green dual-attach migration of 40 overly-permissive IAM policies onto
two named custom policies (`OpalLambdaLeastPrivilege`, `OpalEC2SSMLeastPrivilege`), tracked via an
`IAMMigrationStatus` tag on each role, rolled out in four risk tiers naming eight specific roles.

**On the artifact:**

* `comp-find "OpalLambdaLeastPrivilege|OpalEC2SSMLeastPrivilege" --all` over the whole repo returns
  **10 hits, all inside the plan document itself plus this worker's own tool logs** -- zero hits in
  `infra/aws/terraform/` (569 files scanned) or anywhere else in first-party source, at `21d42b3b16`.
* Live check, `aws iam list-policies --scope Local --query "Policies[?contains(PolicyName,
  'LeastPrivilege')]"` returns `[]` -- no customer-managed policy of that name exists in the account
  today (live read, this grading pass).
* Of the plan's eight named target roles, **five do not exist**: `docker-builder-temp-role`,
  `trending-image-selector-role`, `smartx-ingestion-pipeline-role`, `opal-portal-data-proxy-role`,
  `news-layer3-curation-role` all return `NoSuchEntity` on `aws iam get-role` (live read).
* The three that survive -- `bd-allocation-checker-lambda-role`, `bd-gold-detail-generator-role`,
  `bd-exporter-ec2-role` -- carry **no `IAMMigrationStatus` tag** (`aws iam get-role --query
  Role.Tags`, live read) and still the exact AWS-managed policies the plan proposed to replace
  (`AWSLambdaBasicExecutionRole`, `AmazonSSMManagedInstanceCore`), alongside role-specific custom
  inline policies (`bd-allocation-checker-permissions`: scoped to `opal-data-bd` + one SNS topic;
  `bd-gold-detail-cloudwatch-logs` / `bd-gold-detail-s3-access`; `bd-securities-access`) that are
  already narrower than the plan's own proposed shared templates (which granted `s3:*Object` on
  `opal-data-*/*` and `secretsmanager:GetSecretValue` on `opal/*` -- broader than what these roles
  hold today).

**VERDICT: NOT-LANDED @21d42b3b16** -- the plan's specific mechanism (the two named policies, the
migration tag) was never created, on the artifact, at any point this repo or this account records.
Cause, stated rather than invented per the bounds: this is not necessarily a diligence gap against
this plan -- the three surviving target roles already carry tighter, role-specific custom policies
than the plan's own shared templates would have produced, so least-privilege for those three appears
to have been reached later by a **different, per-role route**, not by this plan's blue-green
mechanism. The other five targets were retired outright. Neither observation rescues this plan's own
verdict: **NOT-LANDED**, as this plan's proposed artifact.

---

## Plan 2 -- `infra/security/remediation/secrets-allowlist-narrowing-and-least-privilege-PLAN-20260709.md`

Pinned vintage: `11d00bc906`, 2026-07-09, 0.5.0_AE_OpalETL.

**What it proposed:** Phase A -- narrow four `secret:opal/*` (and `opalinvest/*`) wildcard grants to
exact-ARN allowlists on `opal-portal-lambda-role`, `opalinvest-auth-lambda-role`,
`news-ingestion-lambda-role`, `yang-pipeline-lambda-role`. Phase B -- on `market-update-lambda-role`
and `opal-news-lambda-role`: detach `SecretsManagerReadWrite` (replace with scoped `GetSecretValue`),
and separately scope `AmazonDynamoDBFullAccess` / `AmazonS3FullAccess` to table/bucket-specific
grants.

**On the artifact -- Phase A:**

* `infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:56-80` (commit `0cf8aed766`,
  2026-07-09, comment "NARROWED 2026-07-09 (NFRA_TERRAFORM-P2 Phase A). Was `secret:opal/*` in BOTH
  regions.") declares exactly the three exact-suffix ARNs the plan named.
* `infra/aws/terraform/news-pipeline/iam.tf:65-80` (same commit `0cf8aed766`) narrows
  `news-ingestion-lambda-role`'s `NewsIngestionPolicy` the same way; `iam.tf:129-142`
  (`SecretsManagerAccess`) is untouched by design (different secret family), consistent with the plan.
* Live reads confirm all four roles hold only exact-ARN (`-??????`) secret grants today: `aws iam
  get-role-policy` on `opal-portal-lambda-role/SecretsManagerAccess`, `news-ingestion-lambda-role/NewsIngestionPolicy`,
  `yang-pipeline-lambda-role/yang-pipeline-lambda-permissions`, `opalinvest-auth-lambda-role/opalinvest-auth-permissions`
  -- zero `opal/*` or `opalinvest/*` wildcards remain on any of the four.
* `org/critical_paths/change_management/20260709T1227Z_20260709T1222Z_terraform-p2-phaseA-secret-allowlist-narrowing_deploy_completion.md`
  records all 7 legs `CLOSED`, including a real-auth-flow behaviour exercise on the SEV1 login path.

**VERDICT (Phase A): LANDED @0cf8aed766** -- confirmed independently of the plan document and the
ledger, on the live IAM objects themselves.

**On the artifact -- Phase B, secrets:**

* `infra/aws/terraform/news-pipeline/iam.tf:174` carries the comment "REMOVED 2026-07-09:
  `SecretsManagerReadWrite`... Replaced by the role-scoped read", commit `0cf8aed766`.
* Live reads: `market-update-lambda-role` and `opal-news-lambda-role` attached-policy lists (`aws iam
  list-attached-role-policies`) show **no `SecretsManagerReadWrite`** on either role today; both carry
  scoped `GetSecretValue`-only inline policies (`market-update-secrets-read`, `opal-news-secrets-read`).
* `org/tier1_exec/3.0.0_SA_CVO/deliverables/CERT_terraform-p2-B1-least-privilege-write-root-lega_20260709.md`
  certifies, by live `simulate-principal-policy` sweep (180/180, `no-verdict:0`), `allowed: NONE` on
  `PutSecretValue` for both `orion/credentials` and `blackdiamond/cot/credentials`.

**VERDICT (Phase B, secrets): LANDED @0cf8aed766** -- confirmed live, independent of the CVO cert and
the plan's own text.

**On the artifact -- Phase B, DynamoDB/S3 FullAccess scoping:**

* `market-update-lambda-role`: `infra/aws/terraform/market-overview/least-privilege-dataplane.tf`
  (commit `dac6d52a6c`, 2026-07-09, header "B2: replace `AmazonDynamoDBFullAccess` with table-scoped
  access, and REMOVE `AmazonS3FullAccess` outright") defines `market_update_dynamodb_scoped`. Live
  `list-attached-role-policies` on `market-update-lambda-role` shows **only** `market-update-lambda-policy`
  attached -- no `AmazonDynamoDBFullAccess`, no `AmazonS3FullAccess` anywhere on the role.
  **LANDED @dac6d52a6c.**
* `opal-news-lambda-role`: `infra/aws/terraform/news-pipeline/iam.tf:175-178` still declares
  `resource "aws_iam_role_policy_attachment" "opal_news_dynamodb_full" { policy_arn =
  "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess" }` -- undisturbed at the same commit
  (`0cf8aed766`) that removed the role's `SecretsManagerReadWrite` two resource blocks above it. Live
  `list-attached-role-policies` on `opal-news-lambda-role` confirms `AmazonDynamoDBFullAccess` (and
  `AmazonS3ReadOnlyAccess`) are attached today. **NOT-LANDED @0cf8aed766** -- the resource that would
  scope it was never authored; this is a plan line item that was explicitly never picked up, not a
  drift from something that was.

**VERDICT (Plan 2, overall): PARTIAL @0cf8aed766** -- Phase A landed in full (4/4 roles); Phase B's
secrets-detach landed in full (2/2 roles); Phase B's DynamoDB/S3 FullAccess scoping landed for
`market-update-lambda-role` only. `opal-news-lambda-role` still carries `AmazonDynamoDBFullAccess`
today. Cause is established, not guessed: the credential-plane portion of Phase B was executed and
certified; the capacity-plane portion (DynamoDB/S3) was executed for one of the two named roles and
never authored for the other.

---

## Plan 3 -- `infra/security/remediation/secretsmanager-readwrite-least-privilege-20260709.md`

Pinned vintage: `c0d864ddac`, 2026-07-09, 0.5.0_AE_OpalETL.

**What it proposed:** this is the root-cause finding behind Plan 2's Phase B -- ground each role's
actually-used secrets across every expression form, replace `SecretsManagerReadWrite` on
`market-update-lambda-role` and `opal-news-lambda-role` with role-scoped `GetSecretValue`, and close
the loop with a completeness cert (`comp-firmsep-sweep --write-only`, bar `allowed: NONE` universe-wide,
not merely `NON-OWNER: NONE`). Its own remediation step 3 (DynamoDB/S3 FullAccess scoping) is
explicitly marked in this file as **"out of scope for the credential-plane program, but the same
shape and the same role"** -- i.e. this plan's own scope excludes it; Plan 2 carries that item
instead (graded above, PARTIAL).

**On the artifact:**

* Identical live/Terraform evidence as Plan 2's "Phase B, secrets" section above:
  `infra/aws/terraform/news-pipeline/iam.tf:174` (commit `0cf8aed766`) plus the market-overview
  equivalent under `47024e28e2` (`NFRA_TERRAFORM-P2 least-privilege PHASE B1 AUTHORED`); live
  `list-attached-role-policies` on both roles shows `SecretsManagerReadWrite` absent, today.
* `org/critical_paths/change_management/20260709T1031Z_20260709T1035Z_terraform-p2-B1-least-privilege-secretsmanager-readwrite_deploy_completion.md`:
  6/6 legs `CLOSED`, including `denytest-implicitdeny` (4/4 `implicitDeny` against a pre-apply
  `allowed` baseline -- a falsifiable negative, not a vacuous one) and `also-allowed` (the roles'
  legitimate reads, e.g. `opal/external-apis`, remain `allowed` -- no collateral denial).
  `cvo-cert-lega` leg cites the CVO cert directly.
* `org/tier1_exec/3.0.0_SA_CVO/deliverables/CERT_terraform-p2-B1-least-privilege-write-root-lega_20260709.md`
  certifies the exact bar this plan's step 5 demanded: `allowed: NONE` (not merely `NON-OWNER: NONE`)
  on `PutSecretValue` for all four firm credential secrets, `180/180` simulated, `no-verdict: 0`,
  `rows == roles`, enumerated by simulation (not grant-shape, which cannot see an AWS-managed
  `Resource:"*"` policy in the first place).

**VERDICT: LANDED @47024e28e2** -- this plan's own proposed remediation (root-cause grounding,
`SecretsManagerReadWrite` detach on both named roles, plan-RAVC gate, completeness cert at the
`allowed: NONE` bar) is fully present on the live artifact and independently re-confirmed by this
worker via `aws iam list-attached-role-policies`, not merely by the plan's or the CVO's own say-so.
The step-3 DynamoDB/S3 item this file itself declares out of scope is graded under Plan 2 instead,
where it is PARTIAL; that does not change this plan's own verdict.

---

## Summary

| plan | verdict | primary citation |
|---|---|---|
| `iam-least-privilege-rollback-plan.md` (Feb 2026) | NOT-LANDED | `21d42b3b16` (repo-wide + live-account absence) |
| `secrets-allowlist-narrowing-and-least-privilege-PLAN-20260709.md` | PARTIAL | `0cf8aed766` |
| `secretsmanager-readwrite-least-privilege-20260709.md` | LANDED | `47024e28e2` |

No verdict above was drawn from, or influenced by, which subfolder a plan document is filed under.
`infra/security/remediation/` does carry both an `active/` and a `completed/` subfolder (the latter
holds two unrelated 2026-02-17 moltbot documents, neither of which is one of this cell's three
plans). Plan 1 sits in `active/` and reads NOT-LANDED -- the folder name would have suggested the
opposite. Plan 2 and Plan 3 sit in the flat `remediation/` root, in neither subfolder, and read
PARTIAL and LANDED respectively -- on the strength of the Terraform commits and live IAM reads cited
inline, never the filename or its directory.
