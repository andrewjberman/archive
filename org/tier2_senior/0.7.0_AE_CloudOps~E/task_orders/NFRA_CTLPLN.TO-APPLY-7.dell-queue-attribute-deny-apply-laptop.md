<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-7.dell-queue-attribute-deny-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain": the apply leg of cell `CT-d-5` as amended (the queue-attribute action added to its Deny; complete as a build, merged @aa6b587487).
<owned_cells>CT-d-5</owned_cells>
</decomp_ref>

  <objective>
    Apply ONE Terraform root on the laptop so the two Dell machines can no longer change a queue's attributes after it is created,
    its access policy included. You found this gap yourself under TO-APPLY-6 (msg 106271). It narrows only.
  </objective>

  <context>
    The root is `infra/aws/terraform/nfra-ctlpln-identity/`, as under TO-APPLY-6. One file changed since: `dell_respol_policy.json`
    gained `sqs:SetQueueAttributes` in `DenyResourcePolicyWrites` (74 -> 75 actions), with its tests. Merged to the trunk
    @aa6b587487. The issuer planned it read-only at ~14:4xZ (exit 2): `aws_iam_policy.dell_agent_respol` updated in place, one
    added action; 0 to add, 1 to change, 0 to destroy.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and each binds on the plan shape below. ONE go, no second message.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_QUEUE_ATTRIBUTE_DENY_20261007.md (@f9858d0ab1)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_QUEUE_ATTRIBUTE_DENY_20261007.md (@2792d4cf57)
    Read both in full first and carry every condition of both.

    CTO CONDITION 5, BEFORE THE APPLY: both Dells are told the refusal in one line. `1.0.0_SA_CTO` asked `0.0.0_AB_MSTR` to relay it
    (msg 106310). You do not message a Dell. Before step 4, read the fabric manager's relay record under
    `org/tier0_exec/0.0.0_AB_MSTR/deliverables/` or ask `0.0.0_AB_MSTR` once whether the line went to both Dells; if you cannot show
    it went, STOP before the apply and report that to 2.0.0_SA_COO~C.

    THE COMMIT: the shared tree at its HEAD on CLOUD. `git diff --stat aa6b587487 HEAD -- infra/aws/terraform/nfra-ctlpln-identity/`
    prints nothing and `git status --porcelain` on the root shows no tracked change. Either one non-empty is a STOP.

    1. Load /cloud-ops. Run and record each last line: `tests/check_identity.py`, `tests/simulate_policy.py` (expect
       `respol_ok=13/13 ... all_ok=True`), `tests/derive_respol_actions.py` (expect `actions=75 covered=75/75 ... ok=True`). A
       failing check is a STOP.
    2. Read live, BEFORE, and save: the default version id and document of `cloudops-dell-agent-respol-policy` (the rollback's
       reference) and how many versions it holds (a managed policy holds at most five; at five the apply fails: report, do not
       delete a version yourself).
    3. Plan the root UNTARGETED: `terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color`.
       - EXACTLY `0 to add, 1 to change, 0 to destroy`; the one address is `aws_iam_policy.dell_agent_respol`; its diff is the one
         added action `sqs:SetQueueAttributes` and nothing else -> go to 4.
       - ANY other plan -> apply NOTHING, report the plan as read, stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the prior version id, and the rollback (set the prior version as default).
    5. ONE apply through `.tools/safe-apply.sh`, as under TO-APPLY-6.
    6. Read-back LIVE against the ATTACHED policies, each arm with its matched statement: a Dell user `sqs:SetQueueAttributes` ->
       explicitDeny in `DenyResourcePolicyWrites`; `sqs:CreateQueue` -> allowed; `sqs:TagQueue` -> allowed; the live document equals
       the repo file (parsed, with a planted-mutant control); the new default version id; a re-plan reads no changes. Close the entry.
       You create and change no queue.
  </the_act>

  <bounds>
    - This one root only. No edit to any `.tf`, `.json` or test file. `safe-apply` only. No push of a shared branch.
    - TO-APPLY-5 (the cottonwood fence) stays separate; this order does not wait on it.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's evaluator arms (tests/simulate_policy.py resource-policy block 13 of 13, with the action's removal caught as a mutant; the issuer re-ran it before the merge) and re-run by the applier; step 6 repeats the three arms against the LIVE attached policies.
comp-adversary: RUN -- a Deny that stops a Dell from creating a queue at all (the cell's first read: 18 of 18 Terraform creates carried attributes inside the create call; the weak point is stated in both halves and COO condition 4 restores the prior version the same window); a plan with a second line (exact shape); the policy at its five-version limit (step 2); a Dell seat surprised by the refusal (CTO condition 5, read before the apply); BLIND: regions other than us-east-1 in the audit read; whether a Dell-placed project owns one of the six roots that declare a separate queue-policy resource (the issuer's read, owed to the CTO).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-d-5"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>respol_ok=13/13 ssm_ok=9/9 routes_ok=5/5 all_ok=True</expect></criterion>
  <criterion id="AC2" cell_refs="CT-d-5"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): how condition 5 was shown; the three check
    lines; the prior and new default version ids and the version count; the plan's count and diff as read; the three live arms
    with decision and matched statement; the re-plan's exit; the ledger entry's path and close; the proof-of-spec instance path
    (genre DEPLOY) and its check result; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
