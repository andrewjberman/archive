<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-DELL-1.dell-identity-apply-site-z</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~RV</issued_to>
    <date>2026-10-07</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round2.md</decomp_doc> (round 2), cell `CT-b-1`: this order is that cell's site-Z apply leg.
<owned_cells>CT-b-1</owned_cells>
</decomp_ref>
# pipeline-override: the site-Z apply leg of the laptop's NFRA_CTLPLN round 2 (cell CT-b-1, issuer 2.0.0_SA_COO~C, order complete as a build); routed to site Z by 0.0.0_AB_MSTR~Z msgs 30561 and 30565 on Andrew's word "Where is the Dell Keys? i want that issued"; a seat act bounded by a never-widen pair, not a round of this lane

  <objective>
    Create the Dell agent identities at site Z by applying ONE Terraform root, so the two Dell machines can be issued their keys.
    Andrew, verbatim, relayed from the laptop CTO terminal ~04:2xZ on 2026-10-07: "Where is the Dell Keys? i want that issued".
    This is URGENT. It is an IAM-creating apply, so the plan's exact shape gates the apply.
  </objective>

  <context>
    The root is `infra/aws/terraform/nfra-ctlpln-identity/` (8 files), built and proven statically by the laptop's cell CT-b-1
    (`org/missions/D0/NFRA/NFRA_CTLPLN/task-orders/NFRA_CTLPLN.TO-CT-b-1.dell-identities.md`, complete; read it for the design).
    It is on origin CLOUD 0ae63f9dbf; the shared tree may not hold it yet, which is why you work from a detached worktree at
    that exact commit.
    Measured on origin at the cut, `iam.tf` declares ten resources: one group `cloudops-dell-agents-group`, two users
    `cloudops-dell1-agent-user` and `cloudops-dell2-agent-user`, one group membership, three policies
    (`cloudops-dell-agent-deploy-policy`, `cloudops-dell1-agent-bus-policy`, `cloudops-dell2-agent-bus-policy`), one group policy
    attachment and two user policy attachments. No `aws_iam_access_key`. The laptop CTO measured NoSuchEntity for both users.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED AHEAD OF THE PLAN, and each binds ONLY on the plan shape below. So there is ONE go and no
    second message: you grade the plan yourself, and the plan's shape decides whether you apply.
    - COO half: org/tier1_exec/2.0.0_SA_COO~Z/deliverables/NEVER_WIDEN_HALF_COO_NFRA_CTLPLN_DELL_IDENTITY_SITEZ_APPLY_20261007.md
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_SITEZ_APPLY_20261007.md @bbca23131f
    Read both in full first. The CTO half's section 2 lists six conditions; carry all six.

    THE COMMIT: a DETACHED worktree at EXACTLY origin CLOUD `0ef817adb0` (git fetch origin CLOUD first). It carries BOTH roots
    and the laptop's own pair; the identity root's bytes are unchanged since 0ae63f9dbf (measured: an empty diff). Never "at or after" it. This order file and the halves live in the shared tree, not in that
    worktree; that is expected.

    1. Load /cloud-ops. Run the root's two checks at that commit: `tests/check_identity.py` and `tests/simulate_policy.py`.
       A failing check is a STOP.
    2. Read live that neither user and not the group exists (the negative arm of AC2).
    3. Plan the root through `safe-apply`'s plan path, UNTARGETED.
       - The plan reads EXACTLY `10 to add, 0 to change, 0 to destroy`, the ten resources are the ones the context lists, and
         no resource is an access key -> go to 4.
       - ANY other plan -> apply NOTHING. Report the plan as read to 2.0.0_SA_COO~Z and stop.
    4. Open ONE NEVER-2 entry naming the rollback (a `safe-apply` destroy of this root; clean only while neither user holds a key).
    5. ONE `safe-apply` of the root at the same commit.
    6. Prove it (the criteria below), compare each of the three policies' live documents to the JSON files' bytes, run
       `comp-iam gaps`, and close the entry.

    THEN LEG B, THE DELL INBOUND QUEUES (only after leg A has applied and proved): the root
    `infra/aws/terraform/nfra-ctlpln-agentbus/` at the SAME commit. Its pair is the project's own, both on origin at that
    commit: the laptop CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_AND_QUEUES_APPLY_20261007.md` (@4ab68e2c3f, covering both roots) and the laptop COO half
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_CT_b_1_DELL_IDENTITIES_20261007.md` with its addendum
    for act 2 (@0ef817adb0). 1.0.0_SA_CTO~Z concurs in its ADDENDUM 1 (@b02f8a2f74, in the shared tree). Read them in your worktree
    and carry their conditions: an UNTARGETED plan of EXACTLY `2 to add, 0 to change, 0 to destroy` (two FIFO queues,
    `agentbus-global-dell1-queue.fifo` and `agentbus-global-dell2-queue.fifo`); an EMPTY diff in that root between the commit the
    laptop COO half names and the commit you apply; the identity apply first. Any other plan -> apply nothing and report.
    Its own NEVER-2 entry, its own `safe-apply`, then read both queues live (they exist, FIFO) and close the entry.
    If leg B stops, leg A stands: the two legs do not roll back together.
  </the_act>

  <bounds>
    - NO access key is created by this order, by any means. The keys are a later act by 0.0.0_AB_MSTR~Z.
    - These two roots only, in that order. No other Terraform root, no edit to either root's files, no IAM write outside leg A's apply.
    - `safe-apply` only; never a bare `terraform apply`. No push of a shared branch.
    - A plan that differs from the expected ten, or an apply that errors part-way, is a STOP with a report: finish or roll back
      in-session per the entry, and say which.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~RV/logs/
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="DELL-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/check_identity.py; echo "exit=$?"</invocation><expect>the root's own static check passes at the GO's commit; and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="DELL-1"><invocation>.tools/aws iam get-group --group-name cloudops-dell-agents-group --query "sort(Users[].UserName)" --output json</invocation><expect>exactly ["cloudops-dell1-agent-user", "cloudops-dell2-agent-user"] after the apply (before it: NoSuchEntity, the negative arm, recorded in step 1)</expect></criterion>
  <criterion id="AC3" cell_refs="DELL-1"><invocation>for u in cloudops-dell1-agent-user cloudops-dell2-agent-user; do .tools/aws iam list-access-keys --user-name $u --query "length(AccessKeyMetadata)" --output text; done</invocation><expect>0 and 0: this order leaves no access key on either user</expect></criterion>
</proof_of_spec>

  <report>
    Report to 2.0.0_SA_COO~Z AS SOON AS LEG A IS PROVEN (0.0.0_AB_MSTR~Z issues the keys the moment the users exist), and again when leg B closes (or at a STOP): the plan's counts and addresses, each criterion's output, the attached policy
    ARNs per user and for the group, `simulate_policy.py`'s result against the live identities, `comp-iam gaps`, the NEVER-2 entry
    path and its close, commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
