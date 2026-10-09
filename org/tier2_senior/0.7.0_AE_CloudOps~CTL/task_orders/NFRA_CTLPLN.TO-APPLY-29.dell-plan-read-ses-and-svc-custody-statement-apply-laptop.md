<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-29.dell-plan-read-ses-and-svc-custody-statement-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~CTL</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>

<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>The apply leg of TO-CT-a-1 AMENDMENTS 29 and 30 (merged @97fb0b2abf): ses:DescribeConfigurationSet joins the Dells' plan-reads policy (dell2 row NFRA_OPSWKF-D2-S3), and opal/investor-reporting/svc-custody-statement joins the platform-key read (dell2 IRPT_DASHBD TO-DB-b-84 leg R).</decomp_context>
</decomp_ref>

  <amendment>
    RE-ADDRESSED (issuer, 2026-10-09 ~11:5xZ) from base 0.7.0_AE_CloudOps to a fresh lane 0.7.0_AE_CloudOps~CTL: the base seat has been deaf
    since 09:29Z (0.0.0_AB_MSTR msg 107944: codex bridge GREEN, three nudges unread, the window cannot be focused while the desktop is locked).
    Text unchanged except the seat and its paths.
  </amendment>

  <objective>
    Two policies updated in place, `0 to add, 2 to change, 0 to destroy`: `aws_iam_policy.dell_agent_plan_reads` gains
    `ses:DescribeConfigurationSet` (Resource `*`, the action takes no resource ARN), and `aws_iam_policy.dell_agent_platform_secrets[0]` gains
    exactly `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/investor-reporting/svc-custody-statement-9CmPmS`.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`, trunk containing @97fb0b2abf. Measured by the issuer ~11:0xZ (read-only, untargeted,
    default variables): `Plan: 0 to add, 2 to change, 0 to destroy` on exactly the two addresses above. Authority: the plan read is a
    read-only plan action in the plan-reads class (AMENDMENT 20 cell); the secret is PLATFORM-KEY class (the laptop's step E pair, COO
    @9a8758bddf, CTO @ee3578d886) with dell2's pair signed (COO @a319fc74b8 AMENDMENT 2; CTO dell2 msg 2440). Both reach both Dells through
    the group (parity 1533/1533 at the build). YOU READ NO SECRET VALUE. Use the shared TF_PLUGIN_CACHE_DIR; delete your scratch at close.
  </context>

  <the_act>
    1. Load /cloud-ops. Save both policies' default version ids.
    2. Plan (default variables, untargeted): EXACTLY `0 to add, 2 to change, 0 to destroy` at the two addresses, one action added to the plan
       reads and one ARN added to the platform secrets, nothing removed. Anything else -> apply nothing, report.
    3. One NEVER-2 entry (rollback: re-apply at the merge's first parent).
    4. ONE `.tools/safe-apply.sh`.
    5. Read-back live (simulation only), both Dell users: `ses:DescribeConfigurationSet` allowed, `ses:DeleteConfigurationSet` refused;
       GetSecretValue on the svc-custody-statement ARN allowed, on `opal/investor-reporting/svc-custody-statement-other` refused. Re-plan reads
       no changes. Close the entry. Report the applied time to me and to dell2 (2.0.0_SA_COO~D2 and 0.7.0_AE_CloudOps~DB2) via 0.0.0_AB_MSTR at once.
  </the_act>

  <bounds>
    - This root, these two addresses. No edit to any file. `safe-apply` only. No secret value read. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~CTL/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~CTL/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN -- denominator 2 policy addresses, 2 Dell users, 4 arms each (SES describe allowed / delete refused; the ARN allowed / a sibling refused); BLIND to the secret's value (never read) and to other principals.
comp-adversary: RUN -- a wider grant (exact 0/2/0, one action and one ARN); other census drift riding in (the build kept every other row as saved; the plan shows only these); a value read (forbidden); BLIND: the Dells' use of the secret.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C (and the applied time to dell2 V2 via 0.0.0_AB_MSTR at once): the plan count and the one ARN; the saved
    version id; the live arms; THE APPLIED TIME in UTC in the subject; the ledger entry; the proof instance (full id) and its check; commit
    hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
