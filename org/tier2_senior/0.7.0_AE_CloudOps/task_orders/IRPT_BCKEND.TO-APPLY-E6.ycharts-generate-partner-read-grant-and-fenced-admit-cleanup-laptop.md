<task_order>
  <metadata>
    <id>IRPT_BCKEND.TO-APPLY-E6.ycharts-generate-partner-read-grant-and-fenced-admit-cleanup-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>IRPT_BCKEND</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP_R67_Y.md</decomp_doc> (dell2 @8c11ac4ff1; read it with `git show 8c11ac4ff1:<path>` until dell2's push is merged on the laptop), sections 3 and 6.2: the laptop legs of release 2 E6, cut by 2.0.0_SA_COO~C on `1.0.0_SA_CTO` msg 107142.
<owned_cells>IB-yr-671</owned_cells>
<decomp_context>dell2's R67 (on origin box/dell2; reaches the laptop tree at the next integrate) cuts E6 as cell IB-yr-671, whose text names this order's leg 2 ("the admit's records are deleted by the laptop's leg 2"). The laptop legs are that cell's support acts; the pair NEVER_WIDEN_PAIR_RELEASE2_E6.md @8c11ac4ff1 sections 3 and 6.2 is their specification.</decomp_context>
</decomp_ref>

  <objective>
    The three laptop legs of dell2 `2.0.0_SA_COO~Y2`'s IRPT_BCKEND release 2 E6: (0) the fenced-delete dry probe now;
    (1) the `irpt-ycharts-generate-role` GetItem grant on the three partner tables; (2) after dell2's on-behalf admit, the
    fenced read/delete of exactly the keys dell2 names.
  </objective>

  <context>
    dell2's own dry probe was refused: `cloudops-dell2-agent-user` lacks `kms:Decrypt` on key `7f4d3042-10d8-49a7-b55e-3c963cea8111`
    (relay `org/tier0_exec/0.0.0_AB_MSTR/deliverables/RELAY_DELL2_E6_DRY_PROBE_REFUSED_20261008_1922Z.md`). The laptop runs the
    probe and the cleanup under its own identity. Every result goes back to dell2 as a FILE through 0.0.0_AB_MSTR (relay to
    `2.0.0_SA_COO~Y2`). The pair is dell2's; the CTO signs its half on receipt of this order. Each leg has its own GO.
  </context>

  <the_act>
    LEG 0 -- DRY PROBE (GO: this order's first GO; no half needed, it writes nothing):
    1. `aws dynamodb delete-item --table-name irpt-requests --key '<a key that cannot exist, in the table's key schema: tenant +
       request_revision>' --condition-expression 'attribute_exists(tenant)'`. Read the table's key schema first
       (`describe-table`) and print the key you used.
    2. Expect `ConditionalCheckFailedException` (permission present, nothing written). Any AccessDenied is the finding: report it
       with the exact text and STOP leg 2 (the pair's branch B).
    3. Result file to dell2 via 0.0.0_AB_MSTR.

    LEG 1 -- THE GRANT (GO only when the CTO half is signed AND dell2's pin `1b94d50b8c` is on origin CLOUD; the GO names both):
    1. Load /cloud-ops. In `infra/aws/terraform/investor-reporting/ycharts/generate.tf`, add the ONE statement of the pair's
       section 3 (`ReadPartnerProfileRowForOnBehalfAdvisor`, `dynamodb:GetItem` on `opal-partner-{49financial,cottonwood,inflection}`,
       not demo), beside `ReadCanonicalUserProfileRow`. Commit it (your lane).
    2. Save the role policy as it is (`iam get-role-policy`). Targeted plan at `aws_iam_role_policy.generate` (inline policy `irpt-ycharts-generate`, generate.tf line 77): EXACTLY `0 to add, 1 to
       change, 0 to destroy`, the diff exactly that statement -> apply through `.tools/safe-apply.sh`. Anything else -> apply
       nothing, report.
    3. One NEVER-2 ledger entry (rollback: targeted apply of the pre-grant policy). Read back `iam get-role-policy`; re-plan
       targeted reads no changes. Report the applied time; dell2 then deploys its code.

    LEG 2 -- FENCED READ/DELETE (GO only when dell2 sends the keys FILE after its admit, relayed by 0.0.0_AB_MSTR):
    1. For each `irpt-requests` key in the file, and NO other: `get-item` (print ONLY whether it exists, and a sha256 prefix of
       `owner` and of `acting_principal_id` -- NEVER an email, name or raw id; CTO msg 107348 after the 2026-10-08 exposure), `delete-item`, `get-item` NOT FOUND.
    2. For the ONE S3 key in the file, and no other: `head-object`; `delete-object`; `head-object` 404. **Andrew approved this
       delete**, verbatim "Yes do it" (~19:3xZ, record
       `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_193xZ_E6_TEST_ADMIT_S3_DELETE_APPROVED.md`; CTO msg 107163):
       exactly the one key dell2's keys file names for the test admit, after the test. A file naming more than one S3 key, or a key
       outside the test admit, is a STOP: delete nothing and report.
    3. Result file to dell2 via 0.0.0_AB_MSTR.
  </the_act>

  <bounds>
    - One statement in one role policy; the named keys only; no other table, object, key policy or function.
    - No GetSecretValue. No read of any attribute beyond `owner` and `acting_principal_id`. No push of a shared branch.
  </bounds>

  <paths>
    infra/aws/terraform/investor-reporting/ycharts/generate.tf
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE three hand legs, each on its GO.
comp-iam: RUN by the applier at leg 1 (targeted plan diff and get-role-policy read-back); leg 0 measures the laptop identity's KMS reach on the table.
comp-adversary: RUN -- a wider grant than the pair's (exact plan shape and diff; demo excluded); a delete beyond the named keys (fenced to the file; conditional probe first); an S3 delete without Andrew's word (leg 2 step 2 holds it); BLIND: dell2's code deploy and admit (its own legs).
lane: the <paths> block names the one Terraform file, the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="IB-yr-671"><invocation>aws iam get-role-policy --role-name irpt-ycharts-generate-role --policy-name irpt-ycharts-generate --query PolicyDocument</invocation><expect>ReadPartnerProfileRowForOnBehalfAdvisor</expect></criterion>
</proof_of_spec>

  <report>
    Report per leg to 2.0.0_SA_COO~C (and the result files to dell2 via 0.0.0_AB_MSTR): leg 0 the key used and the exact
    response; leg 1 the plan, the applied time in UTC in the subject, the read-back, the ledger path and close; leg 2 each key's
    three reads, the S3 head-object result and whether the delete ran (with Andrew's word cited) or is held. Commit hashes and the
    measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
