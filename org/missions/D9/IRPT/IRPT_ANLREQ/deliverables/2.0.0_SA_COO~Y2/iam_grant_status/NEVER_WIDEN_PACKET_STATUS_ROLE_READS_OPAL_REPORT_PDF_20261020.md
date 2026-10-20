# Never-widen sign-off packet -- the status role may READ the retained Opal report PDF: one statement extended on irpt-status-role, at Terraform blob 04b6c4e8a8

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane). **Ledger:** `irpt-status-opal-report-read-20261020`.
**Authority:** CTO msg 11459 ("add that family for the same three firms to the same statement, GetObject plus GetObjectVersion, read only, with addresses as builder output (C-NAMES) ... under a never-widen pair ... IB2 applies by Terraform safe-apply, then simulates on the denied key") and msg 11473 (the packet is the critical path to run 7c). Grounding: FWD-9 needs the Opal report to open from the ticket; run 7b stopped at its route read.
**Scope:** ONE Terraform resource changes: `aws_iam_role_policy.irpt_status` (inline policy `irpt-status-policy` on the role `irpt-status-role`, Terraform root `infra/aws/terraform/investor-reporting/ops`). The one existing statement `ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly` gains three resource entries. No new statement, no new role, no trust change, no other policy of the role, no bucket policy, no KMS key policy, no Lambda, no table, no queue.

## 1. The measured gap

Run 7b (IB2 receipt `irpt_anlreq_commentary_e2e7b/A_E2E7B.txt`, closing line `RUN-DONE STOP at R code=UNEXPECTED`, row `IRPT_ANLREQ-D2-S231`): the status route `GET analysis/requests/{REQ}/commentary-pdf` answered the closed codes UNAVAILABLE and UNEXPECTED. The CTO read the cause in the `irpt-status` log (msg 11459): `s3:GetObjectVersion` DENIED on `opal-data-irpt/irpt/49financial/state/ycharts_opal_reports/ART-ed57.../...pdf`.
The issuer's live read (2026-10-20 ~17:4xZ, `iam get-role-policy`): `irpt-status-role` has four inline policies; `irpt-status-policy`'s statement `ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly` (`s3:GetObject`, `s3:GetObjectVersion`) lists 18 resources (six families under each of `inflection`, `cottonwood`, `49financial`: `vendor_documents`, `request_compositions`, `prospect_inputs`, `original_holdings`, `normalized_portfolios`, `platinum/analysis_reports`); none is under `state/ycharts_opal_reports`.

## 2. What ships

Content pin: `infra/aws/terraform/investor-reporting/ops/iam.tf` at git blob `04b6c4e8a8b8ce534d14b6bdc6d851e873dcd5df` (worker `0.9.0_WK_IRPT_ANLREQ~328`, order `TO-AR-y-463`; the drained commit is named in the GO message; a different blob voids both halves). Against the cut `e02d849d49` the file changes by +7 insertions and -1 deletion:
- the one existing `for family in concat([...], [local.original_holdings_family, local.vendor_pdf_family]) :` line gains `, local.opal_report_family` inside its second list (that line is the one deletion and its one replacement);
- two new locals: `irpt_ycdgen_research_policy` (selects the registry policy `irpt-ycdgen-research-v1`, because `YCHARTS_OPAL_REPORT` is registered there and not on `irpt-x10-v1`) and `opal_report_family = "<tier>/<table>"` read from that row's `YCHARTS_OPAL_REPORT` (tier `state`, table `ycharts_opal_reports`), never typed.
The statement's actions stay `s3:GetObject`, `s3:GetObjectVersion`; its resources become `arn:aws:s3:::<irpt product bucket>/irpt/<firm>/<family>/*` for the same enabled client firms, now seven families each (21 entries).
Checks (worker record, re-run by the issuer before the GO): `OPAL-REPORT-GRANT-OK firms=3 prefixes=3 builder_equal=yes real_key_covered=yes`; the selftest prints `CONTROL-FIRES`; the bound check prints `OPAL-REPORT-BOUND-OK numstat=<n>/1 files=1`. Terraform was NOT run on the authoring box (not installed): the plan is the applier's first proof.

## 3. Blast radius

| what | BEFORE | AFTER |
|---|---|---|
| `irpt-status-role` reading objects under `opal-data-irpt/irpt/<firm>/state/ycharts_opal_reports/` for the 3 enabled client firms | implicitDeny | allowed `s3:GetObject`, `s3:GetObjectVersion` |
| the same role writing, listing or deleting there | implicitDeny | implicitDeny (unchanged) |
| any other prefix, family, bucket, principal, table, queue, key | unchanged | unchanged |

**Who gains:** the `irpt-status` Lambda's role only, read of the retained Opal-generated report PDFs (synthetic and, later, real client analysis reports) of the firms it already serves, in the same bucket and by the same statement that already lets it read those firms' `original_holdings`, `request_compositions`, `normalized_portfolios` and `analysis_reports`. Which viewer may read which report is decided by the route's own authorization in the status Lambda, which this packet did not read; the IAM grant is the floor, not that policy. **Writers counted:** none added. **Not widened:** no write path, no new bucket, no new firm.

## 4. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob (`git hash-object` of this file is printed in the GO). Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the `ops` Terraform stack, the role `irpt-status-role` or its policy is a STOP). Outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act.
1. **R0, before-reads.** `get-role-policy` of `irpt-status-policy`: record the statement ids and the sha256 of the canonical (key-sorted, compact) JSON of the document; `simulate-principal-policy` for `irpt-status-role` on `s3:GetObject` and `s3:GetObjectVersion` against run 7b's retained PDF key (take the `ycharts_opal_reports` key from `irpt_anlreq_commentary_e2e7b/state_e2e7b.json`): both implicitDeny (the baseline). Any other state: STOP.
2. **C, scoped plan.** Root `infra/aws/terraform/investor-reporting/ops` at the drained commit, `terraform fmt -check iam.tf` first (rc 0), then `-target=aws_iam_role_policy.irpt_status`: `Plan: 0 to add, 1 to change, 0 to destroy`; the diff of the `policy` attribute adds exactly three resource entries (`arn:aws:s3:::opal-data-irpt/irpt/<firm>/state/ycharts_opal_reports/*` for the three firms; print them) to that one statement and changes nothing else. Anything else: STOP, nothing applied.
3. **A, apply** with `safe-apply` on the saved plan; never `aws iam put-role-policy`.
4. **V, after-reads.** G1 `get-role-policy`: the statement ids equal R0's, every statement other than `ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly` is byte-equal to R0's, and that statement's resources equal R0's plus the three; G2 the simulation: `s3:GetObject` and `s3:GetObjectVersion` on the real 7b key = allowed (print the matched statement id), `s3:PutObject` on it = implicitDeny, and a key under `original_holdings` unchanged; G3 re-plan reads `No changes`.
5. **Record and close** the ledger; report once.

## 5. Rollback

Revert the Terraform commit (or apply the pre-pin `iam.tf`), scoped plan `0 to add, 1 to change, 0 to destroy` removing exactly those three entries, `safe-apply`, G1 shows the R0 resources again. Nothing else moves. The route then fails at the PDF read again (the state of today).

## 6. Not claimed

- That the plan reads 0/1/0 (Terraform was not run at authoring; the applier's plan is the proof).
- That the route then serves the PDF: run 7c proves it; another denial deeper in the route would be a new row.
- That the three client firms of the `om_client_firms` list equal the policy row's firms in future (equal today: 3).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one IAM inline policy of one role (one statement's resource list extended by three entries). The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
