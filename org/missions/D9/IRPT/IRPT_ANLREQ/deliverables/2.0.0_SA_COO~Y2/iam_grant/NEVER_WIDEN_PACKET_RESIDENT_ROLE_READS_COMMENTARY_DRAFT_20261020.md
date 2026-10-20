# Never-widen sign-off packet -- the resident role may READ the commentary draft: one inline-policy statement on irpt-ycharts-runner-role, at pin 430cd08b2a

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane). **Ledger:** `irpt-resident-commentary-read-20261020`.
**Authority:** CTO msgs 11262 and 11264 ("add s3:GetObject ONLY ... shaped like the existing grant ... from builder output ... expects exactly 0/1/0 ... Andrew's word is not needed: a read grant of a project-owned prefix to the project's own role"). Grounding: FWD-1 needs the four attachments; the packager must read the commentary draft to attach it.
**Scope:** ONE Terraform resource changes: `aws_iam_role_policy.runner_resident` (inline policy `irpt-ycharts-runner-resident-policy` on the role `irpt-ycharts-runner-role`) gains ONE statement. No new role, no trust change, no other statement, no bucket policy, no KMS key policy, no Lambda, no queue, no table, no resident host change.

## 1. The measured gap

Run 6 (IB2 receipt `irpt_anlreq_commentary_e2e6/A_E2E6.txt`): the commentary-time package attach raised `ClientError`. IB2's probe B (`irpt_anlreq_packager_probe/A_PACKAGER_PROBE.txt`, run in the service's environment as the host role): one head and one one-byte get of run 6's commentary draft object under `analysis_commentaries/` returned `head=403 get=AccessDenied`. The issuer's `iam simulate-principal-policy` for the role on run 6's real keys: `analysis_commentaries` `s3:GetObject` and `s3:PutObject` **implicitDeny**; `extraction_evidence`, `normalized_portfolios`, `ycharts_opal_reports` allowed get and put; `original_holdings` and `request_compositions` allowed get. KMS (`GenerateDataKey`, `Decrypt` on the bucket key), `irpt-requests` and the packager secret are already allowed to the role (IB2 read A_PACKAGER_CLIENTERROR.txt R3).

## 2. What ships

Pin `430cd08b2aac7ef74dd31ba78a856032a0343ad3` (the Terraform edit, alone; merged to `box/dell2` at `bb3c5906b25`): `infra/aws/terraform/investor-reporting/ycharts/resident.tf`, 21 insertions, 0 deletions, by worker `0.9.0_WK_IRPT_ANLREQ~320` (order `TO-AR-y-445`):
- a local `resident_commentary_policy` selecting the registry policy row `irpt-anlreq-x10-v1` (the way `resident_reporting_policy` selects `irpt-x10-v1`);
- a list `resident_commentary_read_prefixes`: one entry per client firm of `local.resident_scopes`, `arn:aws:s3:::<reporting bucket>/<source>/<firm long>/<tier>/<table>/*` with the family `ANALYSIS_COMMENTARY` (tier `state`, table `analysis_commentaries`), no typed bucket, firm, tier or table;
- ONE statement after `ReadFrozenCompositionAndNormalizedInput`: `Sid ReadTheAnalysisCommentaryDraft`, `Effect Allow`, `Action ["s3:GetObject", "s3:GetObjectVersion"]`, `Resource local.resident_commentary_read_prefixes`.
Checks (worker record, re-run by the issuer): `COMMENTARY-GRANT-OK firms=3 prefixes=3 builder_equal=yes` (each prefix equals the key the naming builder `lib/opal_naming.py key()` gives for that firm and family, and run 6's real prefix lies under one of them); the selftest with the table name changed prints `CONTROL-FIRES`; `COMMENTARY-BOUND-OK numstat=21/0 files=1`. Terraform was NOT run on the authoring box (not installed): the plan is the applier's first proof.

## 3. Blast radius

| what | BEFORE | AFTER |
|---|---|---|
| the role `irpt-ycharts-runner-role` (the resident host's role) reading objects under `<reporting bucket>/irpt/<firm>/state/analysis_commentaries/` of the 3 client firms | implicitDeny | allowed `s3:GetObject`, `s3:GetObjectVersion` |
| the same role writing, listing or deleting there | implicitDeny | implicitDeny (unchanged) |
| any other prefix, family, bucket, principal, table, queue, key | unchanged | unchanged |

**Who gains:** the resident host's role only, read of the commentary DRAFT objects (Opal-generated analysis commentary text per request) of the firms the resident already serves. The application layer still decides which subject reads: the repository's `SERVICE_READERS` registers `svc-irpt-packager` for the family (`live_read_artifact` refuses `COMMENTARY_READER_UNWIRED` otherwise); the IAM grant is the floor, not the policy. **Writers counted:** none added. **Not widened:** no write path, no cross-firm bucket (the reporting bucket is the one the role already reads other families from).

## 4. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the ycharts Terraform stack, the role `irpt-ycharts-runner-role` or its policy is a STOP). Outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act.
1. **R0, before-reads.** `get-role-policy` of `irpt-ycharts-runner-resident-policy`: record the statement ids and the sha256 of the canonical document; `simulate-principal-policy` for the role: `s3:GetObject` on a run-6-shaped `analysis_commentaries` key = implicitDeny (the baseline).
2. **C, scoped plan.** Root `infra/aws/terraform/investor-reporting/ycharts` at the pin, `terraform fmt -check resident.tf` first (rc 0), then `-target=aws_iam_role_policy.runner_resident`: `Plan: 0 to add, 1 to change, 0 to destroy`; the diff of the `policy` attribute adds exactly one statement `ReadTheAnalysisCommentaryDraft`, removes and changes nothing else. Anything else: STOP, nothing applied.
3. **A, apply** with `safe-apply` on the saved plan; never `aws iam put-role-policy`.
4. **V, after-reads.** G1 `get-role-policy`: the statement ids are the R0 ids plus `ReadTheAnalysisCommentaryDraft`, and the other statements are byte-equal; G2 the simulation: `s3:GetObject` on the real run-6 `analysis_commentaries` key = allowed, `s3:PutObject` on it = implicitDeny, `s3:GetObject` on `original_holdings` unchanged; G3 re-plan reads `No changes`.
5. **Record and close** the ledger.

## 5. Rollback

Revert the Terraform commit (or apply the pre-pin `resident.tf`), scoped plan `0 to add, 1 to change, 0 to destroy` removing exactly that statement, `safe-apply`, G1 shows the R0 statement ids again. Nothing else moves. The packager then fails at the commentary read again (the state of today).

## 6. Not claimed

- That the plan reads 0/1/0 (Terraform was not run at authoring; the applier's plan is the proof).
- That the packager can then attach: the ticket port is refused with HTTP 403 (IB2 probe A: `ATTACH_REFUSED:403`), a separate blocker under read (`TO-READ-PACKAGER-403`).
- That the commentary draft object keys are all under the registry prefix (run 6's key is; checked by the issuer's check).
- That the three client firms of `resident_scopes` equal the policy row's firms in future (equal today: 3 and 3; row W320-S3).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one IAM inline policy of one role (one statement added). The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
