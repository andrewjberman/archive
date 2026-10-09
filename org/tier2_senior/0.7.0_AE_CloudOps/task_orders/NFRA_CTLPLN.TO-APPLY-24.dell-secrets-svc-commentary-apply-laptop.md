<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-24.dell-secrets-svc-commentary-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>

  <closure>
    COMPLETE (issuer, ~02:1xZ). Applied 2026-10-09T02:03:17Z (policy default v3, plan 0/1/0, one ARN added). Issuer live read: both
    Dell users GetSecretValue on opal/ticketing/svc-commentary-pXsmuU allowed, on opal/ticketing/svc-commentary-other implicitDeny.
    Ledger closed (@3e3b61274f). dell2 V2 told via 0.0.0_AB_MSTR.
  </closure>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>The apply leg of AMENDMENT 23: one new secret, opal/ticketing/svc-commentary, joins the Dells' census-built platform-key read, to clear dell2's RED ledger tckt-vnext-f10-d1-mint-20261009 (dell2 2.0.0_SA_COO~V2 msg 2046).</decomp_context>
</decomp_ref>

  <objective>
    One ARN, `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/ticketing/svc-commentary-pXsmuU`, joins
    `aws_iam_policy.dell_agent_platform_secrets[0]`. `0 to add, 1 to change, 0 to destroy`.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`, trunk containing the AMENDMENT 23 merge. Measured by the issuer ~01:5xZ (read-only,
    untargeted, default variables; no window open): `Plan: 0 to add, 1 to change, 0 to destroy`, the one ARN added, nothing removed.
    Authority: dell2's pair, both halves signed (`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/F10_DEPLOY/NEVER_WIDEN_PAIR_SVC_COMMENTARY_MINT.md`
    @b70dd6fbad, origin box/dell2), and the laptop's step E pair, which granted the PLATFORM-KEY class this secret falls in (COO
    @9a8758bddf, CTO @ee3578d886). The laptop CTO is told in the GO. YOU READ NO SECRET VALUE. Use the shared TF_PLUGIN_CACHE_DIR.
  </context>

  <the_act>
    1. Load /cloud-ops. Save the policy's default version id.
    2. Plan (default variables): EXACTLY `0 to add, 1 to change, 0 to destroy` at `aws_iam_policy.dell_agent_platform_secrets[0]`, one
       secret ARN added, none removed. Anything else -> apply nothing, report.
    3. One NEVER-2 entry (rollback: re-apply at the merge's first parent).
    4. ONE `.tools/safe-apply.sh`.
    5. Read-back live (simulation only): both Dells `secretsmanager:GetSecretValue` on the ARN allowed; on
       `opal/ticketing/svc-commentary-other` refused. Re-plan reads no changes. Close the entry. Report the applied time to me and to dell2
       (2.0.0_SA_COO~V2) via 0.0.0_AB_MSTR at once: its RED ledger waits on it.
  </the_act>

  <bounds>
    - This root, this one address. No edit to any file. `safe-apply` only. No secret value read. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN -- denominator 1 policy address, 2 Dell users, 2 live arms per user (the ARN allowed, a sibling refused); BLIND to the secret's value (never read) and to other principals.
comp-adversary: RUN -- a wider grant (exact 0/1/0, one ARN); other census drift riding in (the worker kept every other grant as saved; the plan shows one ARN); a value read (forbidden); BLIND: dell2's use of the token (its ledger).
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
