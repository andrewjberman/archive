<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R30b.ticket-kms-decrypt-grant-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-14</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed Addendum 1 (sections 3 and 4): ONE statement, kms:Decrypt only, on the one key behind irpt-requests, through DynamoDB only, for that table only; the second widening of release 29b; no person gains anything.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN-AS-THE-ACT -- step 3 reads the live key and policy, step 4 applies one statement through the scoped plan, step 6 simulates it; no IAM change is made except through the scoped plan and safe-apply.
comp-adversary: RUN -- by reading your STOP report (msg 7710) and the Addendum against this cell; the lens: a plan that changes more than the one statement, a Resource that is the alias or a wildcard, a condition that does not discriminate (a decrypt allowed without ViaService or for another table), a DescribeKey added silently when the K1 re-run still answers 503. The order requires the exact statement text, the resolved key ARN equal to the table's, and a simulator read that MUST deny without ViaService and with another table's context. NOT seen: the key policy beyond your read, the Terraform state until step 4.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZD: Addendum 1 of release 29b (the KMS read).
<owned_cells>AR-y-321</owned_cells>
</decomp_ref>

  <objective>
    Add the ONE statement `IrptRequestsDecryptViaDynamoOnly` to the ticket role's policy `opal_ticket_api_ddb`, exactly as the signed Addendum 1 gives it, apply it through the scoped plan, read it back, prove its shape with the simulator, and tell 2.0.0_SA_COO~Y2. NO code rollback (CTO half, msg 7715). Then STOP: `TO-EXERCISE-R30` (R0i, then K1 to K3) resumes on my message.
  </objective>

  <context>
    Load /cloud-ops first. Signed: the COO addendum org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release29b/NEVER_WIDEN_PAIR_ANLREQ_RELEASE29B_ADDENDUM_1_KMS_DECRYPT.md (read its git hash-object and print it; it is the file at HEAD) and the CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE29B_ADDENDUM_1_KMS_DECRYPT_CTO_HALF.md (@6dc939b104). The statement text in the COO addendum's section 3 is THE text: copy it, do not compose another. The 29b NEVER-2 ledger irpt-ticket-r29b-20261014 and the sitting ledger irpt-r30-ticket-sitting-20261014 stay OPEN across this order (the CTO half, item 4): do not close either.
  </context>

  <the_act>
    GO: both halves are signed. Start at step 1.
    1. Read both halves at HEAD. Read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the ticket role or ticket-center, other than your own two 29b ledgers, is a STOP. Open ledger irpt-ticket-r29b-kms-20261014 (legs G2 plan, A apply, S shape, T5 simulator) and commit it.
    2. Read the table's key: `dynamodb describe-table --table-name irpt-requests` -> SSEDescription.KMSMasterKeyArn (expected arn:aws:kms:us-east-1:313476888478:key/7f4d3042-10d8-49a7-b55e-3c963cea8111). Read the role's policy now (get-role-policy opal-tickets-table-rw): four statements by Sid (TicketsTableRW, UsersDirectoryReadForClaimEnrichment, UsersDirectoryEmailIndexQueryForClaimEnrichment, IrptRequestsInputOwnerRead). Anything else: STOP and report.
    3. In your own worktree (OUTSIDE the product tree, DETACHED at the trunk HEAD that carries the 29b Terraform source; state the sha; `git -c core.longpaths=true worktree add --detach`), edit infra/aws/terraform/ticket-center/main.tf to add EXACTLY the statement of the addendum's section 3 after IrptRequestsInputOwnerRead inside the Statement list of opal_ticket_api_ddb (the closing bracket of the list moves after it; nothing else changes). Print `git diff` and its `git hash-object`; `terraform fmt -check` on the file if the binary is installed. Commit it on a local branch of yours with `.tools/safe-commit.sh` under your author line. If the data source attribute `server_side_encryption[0].kms_key_arn` does not exist in the provider version the root pins, the plan will say so: STOP and report (do NOT hard-code the key ARN).
    4. The scoped plan from infra/aws/terraform/ticket-center with `-target=aws_iam_role_policy.opal_ticket_api_ddb`: it must show ONE in-place update of that policy that ADDS the one statement and nothing else; the resolved Resource must equal the table's KMSMasterKeyArn of step 2; Action exactly [kms:Decrypt]; the two StringEquals conditions exactly as given. ANY other change: STOP, nothing applied. `.tools/safe-apply.sh` on the saved plan; never `aws iam put-role-policy`. Re-plan: `No changes`.
    5. Read the policy back (get-role-policy): FIVE statements, the new one exactly once and equal to the signed text, the earlier four equal to step 2.
    6. T5 kms arms: `simulate-principal-policy` for the ticket role, ONE resource per call, `kms:Decrypt` on the key ARN: (a) with context kms:ViaService = dynamodb.us-east-1.amazonaws.com and kms:EncryptionContext:aws:dynamodb:tableName = irpt-requests -> expect allowed; (b) WITHOUT kms:ViaService -> MUST be denied; (c) with the right ViaService and kms:EncryptionContext:aws:dynamodb:tableName = opal-tickets (a different table) -> MUST be denied; (d) kms:GenerateDataKey on the key with the full context of (a) -> MUST be denied (implicit). Print every decision. (a) not allowed, or any of (b) (c) (d) allowed: the statement is not what was signed: remove the new statement through the same scoped plan, apply, read back four statements, and report at once.
    7. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r30/A_AFTER_R30b.txt with, ONE line each, exactly: `K0 IrptRequestsDecryptViaDynamoOnly present 1 of 5`, `K1a kms:Decrypt ViaService+context allowed`, `K1b kms:Decrypt no ViaService DENIED`, `K1c kms:Decrypt other table DENIED`, `K1d kms:GenerateDataKey DENIED`, then the hash-object of your diff and the commit. Do NOT close the ledgers. Report ONCE to 2.0.0_SA_COO~Y2: "G2 closed" with the decisions and the commit. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact.
  </the_act>

  <bounds>
    One policy statement through Terraform; one local commit of main.tf in your own worktree. No Lambda code, environment, route, table, key or other IAM change. No request is submitted; no identity is minted. No code rollback. Not in this order: the sitting K1 to K3 (TO-EXERCISE-R30 resumes on my message), the partner page. Remove the throwaway worktree you made when you report (git worktree remove). Rollback of this order: remove the statement through the same scoped plan.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r30/IRPT_ANLREQ.TO-APPLY-R30b.ticket-kms-decrypt-grant-aq2.proof_of_spec.json`.
    <criterion id="R30b-AC1" cell_refs="AR-y-321">The statement is present once of five and the simulator discriminates (allowed with the DynamoDB context; denied without ViaService, for another table, and for GenerateDataKey).<invocation>grep -c -E '^(K0 IrptRequestsDecryptViaDynamoOnly present 1 of 5|K1a kms:Decrypt ViaService\+context allowed|K1b kms:Decrypt no ViaService DENIED|K1c kms:Decrypt other table DENIED|K1d kms:GenerateDataKey DENIED)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r30/A_AFTER_R30b.txt</invocation><expect>^5$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed addendum (not a worker cell); the cell AR-y-321 is the issuer's, as for TO-APPLY-R30a.
