# pipeline-override: MDPF_CANON round 1 (decomposition v1, cell CN-a-1, drained @c57820d3b9); the round-1 issuance @155ac2ce67 is closed to new order files (ONE ISSUER PER ROUND), so the targeted IAM apply of the merged cell rides one CloudOps ADHOC order, on the MDPF_HEALGAP R2-1 precedent.
<task_order id="ADHOC.canon-r1-gold-writer-iam">
<to_id>ADHOC.canon-r1-gold-writer-iam</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P1 (MDPF_CANON round 1 is the FWD-1 thread; nothing reads these roles until the gold Lambda's code redeploy, which is a later, separate order)</priority>

<title>MDPF_CANON CN-a-1: targeted apply of the three per-firm gold-writer roles and the gold Lambda's writer policy -- IAM only, no code, no env</title>

<context>
PRD `org/missions/D8/MDPF/MDPF_CANON/prd/MDPF_CANON_PRD.md` v2.9 CONTRACTS "the firm gold writer" (CTO ruling (a), msg 2995; the CVO's
L6 condition, msg 3000). The cell is `org/missions/D8/MDPF/MDPF_CANON/task-orders/MDPF_CANON.TO-CN-a-1.md`, built by
0.9.0_WK_MDPF_CANON~1 (1f1360cbfb) and drained @c57820d3b9. The source is in `infra/aws/terraform/mdpf-pipeline/iam.tf`:
- `module.gw_*_role_name` / `aws_iam_role.gw_49f`, `gw_inf`, `gw_cot`;
- their `aws_iam_role_policy`;
- `aws_iam_role_policy.mdpf_gold_writers` on `aws_iam_role.mdpf_gold_lambda`.
Each role is `name()` output with its firm in the scope slot (`mdpf-49f-gold-writer-role`, `mdpf-inf-gold-writer-role`,
`mdpf-cot-gold-writer-role`), so the live `DenyForeignFirmPrincipals` on each firm bucket admits it with no edit (FWD-6).
These are new principals with no reader yet, so no served key moves and no never-widen pair is owed. The change is reported after the fact.
</context>

<scope>
1. **Do not edit any file.** Apply exactly the merged source at box/dell1 HEAD (it contains @c57820d3b9).
2. Open a deploy ledger. Run a targeted plan in `infra/aws/terraform/mdpf-pipeline` on:
   - `aws_iam_role.gw_49f`, `aws_iam_role.gw_inf`, `aws_iam_role.gw_cot`;
   - their three `aws_iam_role_policy` resources;
   - `aws_iam_role_policy.mdpf_gold_writers`.
   It must read **7 to add, 0 to change, 0 to destroy**. **Do NOT target `aws_lambda_function.mdpf_gold`**: its env (the three
   `GOLD_WRITER_ROLE_ARN_*`) rides the later code redeploy, which waits on MDPF_STRATID's word.
3. `safe-apply -target` the same set. Read the live result back (criteria). Close the ledger.
4. Report the change after the fact to `0.0.0_AB_MSTR~DELL1`. Name the three roles, their trust (`mdpf-gold-lambda-role` only), their
   grants (Put/Get on `mdpf/{firm}/gold/{account_distribution,account_units,aggregate_aua_timeseries,aum_metrics}/*` plus a
   prefix-conditioned ListBucket), and the gold Lambda's new policy (AssumeRole on the three; Put/Get on composite gold of the four
   in `opal-data-mdpf`).
5. Report to `2.0.0_SA_COO~D1` with each criterion's output.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5,C6</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round1/checks/r1_iam.py"</invocation>
  <expect>ROUND 1 GOLD WRITERS: 6 of 6 arms (the source applied is the source graded)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the targeted plan in infra/aws/terraform/mdpf-pipeline on the seven resources of scope item 2</invocation>
  <expect>7 to add, 0 to change, 0 to destroy; no aws_lambda_function in the plan</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>.tools/aws iam get-role --role-name mdpf-49f-gold-writer-role (and -inf-, -cot-); .tools/aws iam get-role-policy on each role's one inline policy</invocation>
  <expect>each trust names role/mdpf-gold-lambda-role only; each policy grants Put/Get on its own firm bucket's mdpf/{firm}/gold/{the four}/* and a ListBucket conditioned on those prefixes, nothing else</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>.tools/aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::313476888478:role/mdpf-49f-gold-writer-role --action-names s3:PutObject --resource-arns arn:aws:s3:::opal-data-49financial/mdpf/49financial/gold/aum_metrics/date=2026-10-09/data.parquet arn:aws:s3:::opal-data-49financial/mdpf/49financial/platinum/aum_metrics/aum-metrics.json arn:aws:s3:::opal-data-inflection/mdpf/inflection/gold/aum_metrics/date=2026-10-09/data.parquet</invocation>
  <expect>allowed / implicitDeny / implicitDeny, in that order (its own firm's gold only)</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>.tools/aws iam get-role-policy --role-name mdpf-gold-lambda-role --policy-name (the live name of aws_iam_role_policy.mdpf_gold_writers)</invocation>
  <expect>sts:AssumeRole on exactly the three gold-writer role ARNs; Put/Get on arn:aws:s3:::opal-data-mdpf/mdpf/global/gold/{the four}/*</expect>
</criterion>
<criterion id="C6" judgment="false">
  <invocation>python .tools/deploy_ledger.py check</invocation>
  <expect>this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
