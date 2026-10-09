<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-21.dell-identity-step-g-step-f-followups-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>The apply leg of AMENDMENT 21 (merged @83326afe6f): the CTO's three follow-ups on step F (msg 107457).</decomp_context>
</decomp_ref>

  <objective>
    Apply STEP G on the Dell identity root: one secret ARN (a public key) joins the platform-secrets read; one Deny refuses writes to the
    bd-to-schwab cutover parameter. `0 to add, 2 to change, 0 to destroy`.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`, trunk containing merge 83326afe6f. Measured by the issuer ~00:0xZ (read-only):
    `Plan: 0 to add, 2 to change, 0 to destroy.` Halves: COO
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_G_STEP_F_FOLLOWUPS_20261008.md`; CTO
    `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_STEP_G_AND_PARTNER_ROSTER_20261009.md` section 1 (@21a5ceab0f, SIGNED). Set TF_PLUGIN_CACHE_DIR to the shared cache (MSTR msg 107482). YOU READ NO SECRET VALUE.
  </context>

  <the_act>
    1. Load /cloud-ops. `git status --porcelain -- infra/aws/terraform/nfra-ctlpln-identity/` empty; the simulation's last line contains
       `cutover_ok=23/23` and ends `all_ok=True`.
    2. Save both policies' default version ids.
    3. Plan (default variables): EXACTLY `0 to add, 1 to change` twice = `0 to add, 2 to change, 0 to destroy`, addresses
       `aws_iam_policy.dell_agent_platform_secrets[0]` and `aws_iam_policy.dell_agent_deploy`; added lines carry one secret ARN and one
       statement `DenyCutoverParameterWrites`. Anything else -> apply nothing, report.
    4. One NEVER-2 entry (rollback: re-apply the root at the merge's first parent).
    5. ONE `.tools/safe-apply.sh`.
    6. Read-back live per the COO half's condition 3; re-plan no changes. Close the entry. Report the applied time to me and to both Dells
       via 0.0.0_AB_MSTR.
  </the_act>

  <bounds>
    - This root only, one apply. No edit to any file. `safe-apply` only. No secret value read. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN -- denominator 2 policy addresses, 2 Dell users, 6 live arms per user (two cutover writes/reads, two secret reads, plus the re-plan); BLIND to what a Dell does with IAM write afterwards (it can remove this Deny itself; stated in the COO half).
comp-adversary: RUN -- a wider plan (exact 0/2/0, two addresses, one ARN, one statement); a secret value read (forbidden; simulation only); the cutover Deny reaching other parameters (exact ARN; other-parameter arms unchanged in the cell's simulation); BLIND: organization policies.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>cutover_ok=23/23</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the pre-plan line; the plan count and added lines' summary; the saved version ids; every live arm with
    decision and matched statement; THE APPLIED TIME in UTC in the subject; the ledger path and close; the proof instance (full id) and
    its check; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
