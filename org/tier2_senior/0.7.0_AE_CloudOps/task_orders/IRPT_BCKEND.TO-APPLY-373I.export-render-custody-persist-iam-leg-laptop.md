<task_order>
  <metadata>
    <id>IRPT_BCKEND.TO-APPLY-373I.export-render-custody-persist-iam-leg-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>IRPT_BCKEND</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP_R68_Y.md</decomp_doc>
<owned_cells>IB-yr-681</owned_cells>
<decomp_context>The IAM leg (row D2-W181-S1) of dell2's IB-pr-373, which its CTO half @ece42ad420 condition 2 makes its own sign-off. dell2 2.0.0_SA_COO~P2 msg 1819 (relay 107422). Dells write no IAM until NFRA_CTLPLN cell 3 applies, so the laptop applies this one (Andrew ~22:0xZ: the laptop keeps a Dell act only where the Dell's identity still refuses it). The cell id is the nearest R68 cell on the laptop tree; the leg's own specification is the pair below.</decomp_context>
</decomp_ref>

  <objective>
    Add ONE inline policy, `aws_iam_role_policy.export_render_custody_persist` (`irpt-export-render-custody-persist-policy`), to
    `aws_iam_role.export_render` in `infra/aws/terraform/investor-reporting/export`, exactly as dell2's pair states, by a targeted
    apply: `1 to add, 0 to change, 0 to destroy`.
  </objective>

  <context>
    Pair: `git show 7c08fe294e:org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-373_IAM_LEG.md`
    (origin box/dell2; blob f98f340b38). COO half @7c08fe294e (dell2). CTO half SIGNED by `1.0.0_SA_CTO~DELL2` (msg 1823):
    `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_373_IAM_LEG_CTO_HALF.md` @5f65b4f40e (origin
    box/dell2). Its ADDED CONDITION: S1's `dynamodb:LeadingKeys` limit stands only if the requests table's partition key is the tenant
    -- before step 1, run `aws dynamodb describe-table` on the table and print its KeySchema; if the HASH key is not the tenant
    attribute, S1 stands table-wide WITHOUT the condition and the report records the live key schema as the reason (the only edit
    to the pair's HCL this order permits). The pair's HCL (one `locals` block and one resource, statements S1-S5) is the whole change; every ARN and
    prefix is built from the root's own outputs and the registry (no ARN typed). The root already defines `local.b1_served_firms`,
    `local.b1_reporting_policy`, `local.region`, `local.account_id` and `aws_iam_role.export_render` (iam.tf) -- measured by the
    issuer ~22:4xZ. The route `POST /api/scoped/investor-reporting/custody-report` is NOT applied and is not part of this order.
  </context>

  <the_act>
    The apply runs only when BOTH halves are SIGNED; the GO names the dell2 CTO half's hash.
    1. Load /cloud-ops. Add the pair's `locals` block and resource, byte-for-byte from the pair, to a new file
       `infra/aws/terraform/investor-reporting/export/custody_persist_iam.tf`. `terraform validate` passes. Commit it (your lane).
    2. Save `aws iam list-role-policies` and `list-attached-role-policies` for the role.
    3. Targeted plan at `aws_iam_role_policy.export_render_custody_persist`: EXACTLY `1 to add, 0 to change, 0 to destroy`, that
       address only; the rendered policy has 5 statements; the S3 resources render to `irpt/{49financial,cottonwood,inflection}/platinum/custody_reports/*`
       and `irpt/{...}/state/request_compositions/*` in the reporting bucket; no `"*"` resource; no `dynamodb:UpdateItem`. Anything
       else -> apply nothing, report.
    4. One NEVER-2 entry (rollback: remove the resource and a targeted apply, `0/0/1` on that address).
    5. ONE `.tools/safe-apply.sh` with that plan. Read back `aws iam get-role-policy --role-name <the role> --policy-name
       irpt-export-render-custody-persist-policy`; a targeted re-plan reads no changes. Close the entry.
    6. Report the applied time to me and to dell2 (2.0.0_SA_COO~P2) via 0.0.0_AB_MSTR. The pair's after-reads (the persist through
       the route) are dell2's, after its own route order.
  </the_act>

  <bounds>
    - This one resource and the new file only. No other resource in the root, no route, no function code.
    - `safe-apply` only. No push of a shared branch.
  </bounds>

  <paths>
    infra/aws/terraform/investor-reporting/export/custody_persist_iam.tf
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN by the applier at step 3 (the rendered statements, resources and actions) and step 5 (get-role-policy read-back).
comp-adversary: RUN -- a wider grant (exact 1/0/0 at one address; rendered prefixes checked; no "*"; no UpdateItem); typed ARNs (the pair builds every ARN from outputs and the registry); a reachable write (the route is not applied; the function fails closed until then); BLIND: S2/S5 KMS actions are inferred by the pair, measured by dell2's after-read; a refused KMS call is a row, not a widening.
lane: the <paths> block names the one new .tf file, the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="IB-yr-681"><invocation>terraform -chdir=infra/aws/terraform/investor-reporting/export plan -input=false -no-color -lock=false -detailed-exitcode -target=aws_iam_role_policy.export_render_custody_persist; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the validate result; the saved role policy lists; the plan count and the rendered resources; the
    applied time in UTC in the subject; the read-back; the ledger entry; commit hashes and the measured push state. Leave the status
    flip to the issuer.
  </report>
</task_order>
