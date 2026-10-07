<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-6.dell-denies-and-dell2-grant-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain": the apply leg of cell `CT-d-5` (complete as a build); the same one plan carries workstream ACCESS cell `CT-a-1` (decomposition `NFRA_CTLPLN_DECOMP.access1.md`, complete as a build), by the CTO's ruling of one half request for both (msg 106190).
<owned_cells>CT-d-5</owned_cells>
</decomp_ref>

  <objective>
    Apply ONE Terraform root on the laptop so the two Dell machines are refused three things and one of them gains one thing.
    Refused, both Dells: writing any resource policy (74 actions); updating any function, command document or downloaded artifact
    prefix that leads to a role able to write IAM or delete production data (33 functions, 12 documents, 5 prefixes, built by
    Terraform from a role census). Gained, dell2 only: sending two named command documents to one named host and reading command
    results. It is an IAM-changing apply, so the plan's exact shape gates the apply.
  </objective>

  <context>
    The root is `infra/aws/terraform/nfra-ctlpln-identity/`, the same root you applied under TO-APPLY-3. Since then two cells merged
    into it: CT-d-5 (`dell_respol_policy.json`, one policy and one group attachment in `iam.tf`) and CT-a-1 (`dell2_ssm_policy.json`
    with one policy and one user attachment in `iam.tf`; `routes.tf` and `modules/routes_policy/`, which build two Deny documents
    from `tests/reached_roles_census.json`). Last commit to the root: `109a410fe7`, merged to the trunk @47a20c88e4.
    The issuer planned it read-only on the laptop at ~12:3xZ (exit 2): eight resources created, nothing changed, nothing destroyed.
    Both resident command documents take a free-text parameter, so the dell2 grant lets dell2 run a command of its choosing on that
    host as the host's role; both halves say so and the CTO signed it at that width because the census reads that role NO.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and each binds on the plan shape below. There is ONE go and no second message: you grade the
    plan yourself, and the plan's shape decides whether you apply.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_DENIES_AND_DELL2_GRANT_20261007.md (@14774dd9ff)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_DENIES_AND_DELL2_GRANT_20261007.md (@eb74cfb2d2)
    Read both in full first and carry every condition of both (the COO half's six; the CTO half's 7 and 8).

    THE COMMIT: work in the shared tree at its HEAD on branch CLOUD. Before anything else show that the root's bytes at HEAD equal
    its bytes at `47a20c88e4`: `git diff --stat 47a20c88e4 HEAD -- infra/aws/terraform/nfra-ctlpln-identity/` prints nothing, and
    `git status --porcelain -- infra/aws/terraform/nfra-ctlpln-identity/` shows no tracked change. Either one non-empty is a STOP.

    1. Load /cloud-ops. Run the root's checks and record each last line: `tests/check_identity.py`, `tests/simulate_policy.py`,
       `tests/render_routes_policy.py`, `tests/render_passrole.py --check`, `tests/derive_protected_functions.py --check`,
       `tests/derive_ssm_documents.py --check`. A failing check is a STOP.
    2. THE FRESHNESS READ, before the plan: `python infra/aws/terraform/nfra-ctlpln-identity/tests/derive_reached_roles.py --check-fresh`
       (read-only, about 9 minutes, it retries on throttling; do not bound it at 120 seconds). `fresh=True` -> go on.
       `fresh=False` -> apply NOTHING; report its differences; the census is re-taken by the issuer's cell, not by you.
    3. Read live, BEFORE, and save in your deliverables folder (the rollback's reference): the policies attached to
       `cloudops-dell-agents-group` and to each of the two Dell users; that none of the four new policy names exists
       (`cloudops-dell-agent-respol-policy`, `cloudops-dell-agent-routes-fn-policy`, `cloudops-dell-agent-routes-host-policy`,
       `cloudops-dell2-agent-ssm-policy`). One that already exists is a STOP.
    4. Plan the root UNTARGETED with terraform directly:
       `terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color`.
       - EXACTLY `8 to add, 0 to change, 0 to destroy`, and the eight addresses are:
         `aws_iam_policy.dell_agent_respol`, `aws_iam_group_policy_attachment.dell_agent_respol`,
         `aws_iam_policy.dell_agent_routes_fn[0]`, `aws_iam_group_policy_attachment.dell_agent_routes_fn[0]`,
         `aws_iam_policy.dell_agent_routes_host[0]`, `aws_iam_group_policy_attachment.dell_agent_routes_host[0]`,
         `aws_iam_policy.dell2_ssm`, `aws_iam_user_policy_attachment.dell2_ssm` -> go to 5.
       - ANY other plan (a different count, a change, a destroy, a ninth address, a refused precondition) -> apply NOTHING.
         Report the plan as read to 2.0.0_SA_COO~C and stop.
    5. Open ONE NEVER-2 ledger entry naming the laptop as the box, the eight objects, and the rollback per pair as the COO half
       states it (the four pairs are independent).
    6. ONE apply of the root through `.tools/safe-apply.sh`, as under TO-APPLY-3.
    7. Read-back, LIVE, each arm ATTRIBUTED (matched statement), by the simulator against the ATTACHED policies, not the repo files:
       - the four live documents equal the rendered ones (parsed comparison, with a planted-mutant control); the group carries 5
         managed policies and the dell2 user 2;
       - the nine arms of the simulation's sixth block (dell2: each resident document to the instance allowed; a resident document
         to another instance refused; `AWS-RunShellScript` explicitDeny; the export render document explicitDeny; a document nothing
         grants refused; `ssm:GetCommandInvocation` allowed; dell1: the send refused, `GetCommandInvocation` refused);
       - the five arms of its seventh block (three explicitDeny, one per route kind; two allowed on NO roles);
       - for the resource-policy Deny: one refused `s3:PutBucketPolicy` for a Dell user, and one create the create policy allows
         still allowed as the control;
       - a re-plan reads no changes.
       Close the entry. You send NO command to any host: the exercised send is dell2's own, from dell2, by another route, and
       until it runs the grant is APPLIED, not EXERCISED. Say that in your report in those words.
  </the_act>

  <bounds>
    - This one root only. No other root, no edit to any `.tf`, `.json` or census file, no `ssm send-command`, no session.
    - `safe-apply` only. No push of a shared branch.
    - TO-APPLY-5 (the cottonwood fence) stays open and separate; this order does not wait on it and does not touch that resource.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the built cells' evaluator arms (tests/simulate_policy.py: 22 allowed, 19 denied, 5 pass-role, 8 protected, 11 resource-policy, 9 command, 5 routes; the issuer re-ran it before the merge) and re-run by the applier before the plan; step 7 repeats the command and routes arms against the LIVE attached policies with matched statements.
comp-adversary: RUN -- a census gone stale between the read and the apply (step 2's live freshness read; a difference is a stop); a plan that carries a ninth line (exact shape, eight named addresses); a Deny that locks a Dell out of work it does today (named in both halves as the design; the two NO-role arms are the control); the one widening, a free-text command as the host's role (stated in both halves at its full width; CTO condition 8 detaches on any wider send); a policy name already taken (step 3); BLIND: resource policies and organization policies, which the census did not evaluate (row NFRA_CTLPLN-W8-S2), and whether an existing command's output holds a secret that the new read actions would show dell2 (an open row the issuer files).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-d-5"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>respol_ok=11/11 ssm_ok=9/9 routes_ok=5/5 all_ok=True</expect></criterion>
  <criterion id="AC2" cell_refs="CT-d-5"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
  <criterion id="AC3" cell_refs="CT-d-5"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/check_identity.py</invocation><expect>names_from_builder=11/11 policy_size_ok=True ok=True</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the six check lines; the freshness line; the
    before-state file paths; the plan's count and eight addresses as read; each read-back arm with its decision and matched
    statement, grouped by block; the group's and the dell2 user's attached policies after; the re-plan's exit; the ledger entry's
    path and close; the proof-of-spec instance path (genre DEPLOY) and its check result; commit hashes and the measured push state.
    Leave the status flip to the issuer.
  </report>
</task_order>
