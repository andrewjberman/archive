# Never-widen sign-off packet -- the resident role may READ the Opal model return series and the positioning object: one inline-policy statement on irpt-ycharts-runner-role, at pin 50f7c709af

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane). **Ledger:** `irpt-resident-model-source-read-20261020`.
**Authority:** PRD IRPT_ANLREQ v0.25 @b83ce81b5b, contract C-MODEL-SOURCE ("through ONE read grant on the resident policy under a never-widen pair"); CTO ruling R1 (`CTO_RULINGS_MODEL_WEIGHTS_SWAP_AUDIT_20261020.md` @665110f9c2, key corrected @b9de1e559d, msg 11381); CTO msg 11442 (decompose and issue FWD-10). The precedent for the act and its shape is Y2's packet `iam_grant/NEVER_WIDEN_PACKET_RESIDENT_ROLE_READS_COMMENTARY_DRAFT_20261020.md` (commit 430cd08b2aa).
**Scope:** ONE Terraform resource changes: `aws_iam_role_policy.runner_resident` (inline policy `irpt-ycharts-runner-resident-policy` on the role `irpt-ycharts-runner-role`) gains ONE statement, and one `locals` entry is added. No new role, no trust change, no other statement, no bucket policy, no KMS.

## 1. The measured gap

FWD-10 (Core) compares the portfolio with Opal models and reads two firm-neutral objects of the bucket `opal-data-portal-v2`: `json/benchmarks/model_portfolio_timeseries.json` (the model return series; plain JSON, 780,910 B at 2026-10-20 11:06:27Z) and `json/positioning/positioning_data.json` (the models' current positioning; gzip-compressed JSON, 6,890 B). The resident runs on the YCharts runner host as `irpt-ycharts-runner-role`; the issuer's trace (`0.9.0_WK_IRPT_ANLREQ~304/MODEL_COMPOSITION_TRACE.md`, Q5) found it has no grant on either, and `resident.tf` at the pin carries none. Read-only measurements by the issuer on 2026-10-20 (own credentials, no client data):
- both keys exist: `head-object` returned the two sizes above; the address in the CRO research (`yang/global/platinum/...`) is 404 and was corrected by the CTO (msg 11381);
- both objects are `ServerSideEncryption: AES256` (S3-managed), no KMS key, and the bucket default is AES256: **no KMS grant is needed**;
- the bucket policy holds three `Allow` statements (two CloudFront principals and an advisor-router OAI) and no `Deny`: nothing blocks an in-account role that has an identity-policy allow.
The objects are overwritten daily by the yang pipeline; the grant reads no version, so `s3:GetObject` alone is enough.

## 2. What ships

Pin `50f7c709af2` (the Terraform edit, alone; merged to `box/dell2` at `e408831dd8f`): `infra/aws/terraform/investor-reporting/ycharts/resident.tf`, 16 insertions, 0 deletions, by worker `0.9.0_WK_IRPT_ANLREQ~331` (order `TO-AR-g-172`, criteria AR-GRANT build/guard/regress all OK, re-run by the issuer):
- a local `model_source_bucket = "opal-data-portal-v2"` (the bucket is in no other local, variable or remote-state output of this root);
- ONE statement placed after `ReadTheHeldFundCharacteristics`: `Sid ReadTheModelReturnSeriesAndPositioning`, `Effect Allow`, `Action ["s3:GetObject"]`, `Resource` = exactly `arn:aws:s3:::opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json` and `arn:aws:s3:::opal-data-portal-v2/json/positioning/positioning_data.json`.
No wildcard, no list, put, delete or version action.

## 3. Blast radius

| what | BEFORE | AFTER |
|---|---|---|
| the role `irpt-ycharts-runner-role` reading the two objects above | implicitDeny | allowed `s3:GetObject` |
| the same role writing, listing or deleting there, or reading any OTHER key of the bucket | implicitDeny | implicitDeny (unchanged) |
| any other role, principal, bucket, key, table, queue | unchanged | unchanged |

**Who gains:** the resident host's role only, read of two Opal-owned, firm-neutral, already-public-to-CloudFront data objects (the same numbers the Performance and Positioning tabs show). No client data is in either object (one is a model return series, the other a model holdings and allocation snapshot). The application decides who sees the report that uses them.

## 4. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the ycharts Terraform stack, the role `irpt-ycharts-runner-role` or its policy is a STOP).
1. **R0, before-reads.** `get-role-policy` of `irpt-ycharts-runner-resident-policy`: record the statement ids and the sha256 of the canonical document; `simulate-principal-policy` for the role: `s3:GetObject` on each of the two keys = implicitDeny; `s3:GetObject` on a third key of the bucket (`json/benchmarks/other.json`) = implicitDeny.
2. **C, scoped plan.** Root `infra/aws/terraform/investor-reporting/ycharts` at the pin, `terraform fmt -check resident.tf` first (rc 0), then `-target=aws_iam_role_policy.runner_resident`: `Plan: 0 to add, 1 to change, 0 to destroy`; the diff of the `policy` attribute shows exactly the one added statement and nothing else. Any other change in the plan is a STOP (report, do not apply).
3. **A, apply** with `safe-apply` on the saved plan; never `aws iam put-role-policy`.
4. **V, after-reads.** G1 `get-role-policy`: the statement ids are the R0 ids plus `ReadTheModelReturnSeriesAndPositioning`, and every other statement is byte-equal; G2 the simulation: `s3:GetObject` on the two keys = allowed; `s3:PutObject`, `s3:DeleteObject` on them and `s3:GetObject` on the third key = implicitDeny; G3 a real `get-object` of each key with the host role's credentials (IB2's probe style): HTTP 200, the series parses as JSON, the positioning body starts with the gzip magic bytes.
5. **Record and close** the ledger.

## 5. Rollback

Revert the Terraform commit (or apply the pre-pin `resident.tf`), scoped plan `0 to add, 1 to change, 0 to destroy` removing exactly that statement and the local, `safe-apply`, G1 shows the R0 statement ids again. Nothing else moves. The comparison section then reads each model comparable as `not available for <name>: the Opal model series could not be read` (FWD-12) and the run does not fail.

## 6. Not claimed

- That the plan reads 0/1/0 (Terraform was not run at authoring; the applier's plan is the proof).
- That the FWD-10 code is live: the producer stage, the layout elements and the resident ports ship in a later resident release under its own pair (round 60, cells AR-g-171 and AR-g-173 to AR-g-175). This grant alone changes no report.
- That the yang job keeps the two keys where they are today (a moved key makes the reader refuse, stated in words; the key is one constant in `model_source.py`).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one IAM inline policy of one role (one statement added) and one Terraform local. The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
