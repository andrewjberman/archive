<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-11.dell-identity-plan-1-secrets-deny-off-self-simulate-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain": a further apply leg of cell `CT-a-1` (the Dell identity root; its AMENDMENT 9 built this plan on Andrew's word lifting the Dells' limits).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <objective>
    Apply ONE untargeted plan of the Dell identity root: the Dell group gains a read of 66 named secrets, loses the Deny of
    resource-policy actions, and each Dell user may simulate its own user. Seats on dell1 and dell2 are stopped waiting on the
    secrets read. This order is SECOND in your queue, after NFRA_CTLPLN.TO-APPLY-10 (1.0.0_SA_CTO ruling 106726).
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`. Andrew-direct 2026-10-08 ~00:4xZ, "lets start with lifting 1 2 3 6" (record
    org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_004xZ_LIFT_FOUR_DELL_LIMITS_SECRETS_FIRM_DATA_RESOURCE_POLICIES_PUSH.md).
    The issuer planned it read-only on the trunk @35f5f12418 at ~04:5xZ (exit 2): `Plan: 2 to add, 1 to change, 2 to destroy.`
    This is PLAN 1 OF 2. It does not carry the Allow of the resource-policy actions or dell2's SSM public parameter read; do
    not add either, and do not wait for them.
    YOU READ NO SECRET VALUE at any step: no `get-secret-value`, by any route, for any reason.
  </context>

  <the_act>
    The apply runs only when BOTH never-widen halves are SIGNED. ONE go, no second message; the issuer's GO names the CTO half.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_PLAN_1_SECRETS_DENY_OFF_SELF_SIMULATE_20261008.md (@fa6d36f4a3)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_PLAN_1_SECRETS_DENY_OFF_SELF_SIMULATE_20261008.md (@8c4fe4be88)
    Read both in full first and carry every condition of both.

    THE COMMIT: the shared tree at its HEAD on CLOUD, which must contain 35f5f12418. Show `git status --porcelain --
    infra/aws/terraform/nfra-ctlpln-identity/` is empty.

    1. Load /cloud-ops. Immediately before the plan, run and record each last line:
       `python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py`
       (expect `selfsim_ok=9/9 ssm_ok=9/9 routes_ok=5/5 vendor_ok=235/235 all_ok=True`) and
       `python infra/aws/terraform/nfra-ctlpln-identity/tests/derive_vendor_secrets.py --from-file infra/aws/terraform/nfra-ctlpln-identity/tests/vendor_secrets_census.json`
       (expect `secrets=114 ... granted=66 ok=True blocked_by_key=1 platform_key=28 other=19`). ALWAYS with `--from-file`: the
       issuer ran it without the flag and it did not finish in 118 s (it re-takes the listing); with the flag it reads the saved
       census and leaves the root unmodified (measured). A failing line is a STOP.
    2. BEFORE: save the LIVE documents of `cloudops-dell-agent-create-policy` and `cloudops-dell-agent-respol-policy` (default
       versions) and the Dell agent group's attached-policy list, each with SHA-256.
    3. Plan, TARGETED at exactly the five resources named below (AMENDMENT 1 at the foot of this order): pass five
       `-target` flags, one per resource, and no other.
       - EXACTLY `2 to add, 1 to change, 2 to destroy`, these five and no other: `aws_iam_policy.dell_agent_vendor_secrets[0]`
         and its group attachment created; `aws_iam_policy.dell_agent_create` updated in place; `aws_iam_policy.dell_agent_respol`
         and its group attachment destroyed. The created policy holds exactly ONE action (`secretsmanager:GetSecretValue`) on
         exactly 66 secret ARNs, no wildcard. The in-place update ADDS exactly one statement, `SimulateOwnPolicyOnly`, and
         removes NO line. A grep of the plan for each of `jwt-private-key`, `admin-seed`, `jwt-secret`, `origin-verify`,
         `gateway/`, `otp-gateway-token`, `opal/mcp/`, `pseudonym`, `anonymization-key`, `ec2-credentials` reads ZERO hits
         (record each count) -> go to 4.
       - ANY other count, a sixth resource, an ARN count other than 66, a removed line in the create policy, a withheld name
         in the plan, a wildcard in the new statement -> apply NOTHING; report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the saved documents by path and hash, both halves, and the rollback
       per key as the COO half states it.
    5. ONE apply through `.tools/safe-apply.sh` with the SAME five `-target` flags.
    6. Read-back LIVE with `aws iam simulate-principal-policy` on EACH Dell user, each arm with its matched statement named:
       `secretsmanager:GetSecretValue` on the ARNs of `blackdiamond/49f/session`, `astn/kimi/api-key` and `openai-api-key`
       -> allowed; on `opal/auth/jwt-private-key`, `opalinvest/admin-seed`, `gateway/mail/bearer` and
       `blackdiamond/49f/otp-gateway-token` -> refused; `sqs:SetQueueAttributes` -> allowed; `s3:PutBucketPolicy` -> refused;
       one routes arm refused as before; `iam:SimulatePrincipalPolicy` on its own user allowed and on the other Dell's user
       refused (pass the context key `aws:username`). The group's attached-policy list read live. A re-plan WITH THE SAME FIVE TARGETS reads no changes (an
       untargeted re-plan will read plan 2's two resources as to-add: expected). Close the entry. APPLIED, not EXERCISED, until the Dells' own reads.
  </the_act>

  <bounds>
    - This root only, one apply. No edit to any `.tf`, policy document, census or test file.
    - `safe-apply` only. No push of a shared branch. No secret value read. No other root.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's simulation (235 secret arms over both users, nine self-simulate arms, the freed-action decisions, the routes and protected-function arms unchanged) and re-run by the applier immediately before the plan; step 6 repeats the named arms against the LIVE policies with matched statements.
comp-adversary: RUN -- a withheld platform key riding in the grant (the zero-hit grep of the plan over ten name stems; the live refused arms in step 6); a wildcard (the plan-shape check); the create policy losing a line (zero removed lines); the applier reading a value (forbidden in context and bounds); no way back (documents saved before the apply; the removed Deny document recoverable from git); BLIND: a real read from a Dell (its own, owed after), organization policies, and a secret created after the census time.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>vendor_ok=235/235 all_ok=True</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode -target='aws_iam_policy.dell_agent_vendor_secrets[0]' -target='aws_iam_group_policy_attachment.dell_agent_vendor_secrets[0]' -target=aws_iam_policy.dell_agent_create -target=aws_iam_policy.dell_agent_respol -target=aws_iam_group_policy_attachment.dell_agent_respol; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the two pre-plan lines; the saved
    documents' paths and hashes; the plan's count, the five resources, the ARN count, the ten grep counts; every live
    simulator arm per user with its decision and matched statement; the group's attached-policy list; the re-plan's exit;
    THE APPLIED TIME in UTC; the seat-gate WARN lines the wrapper printed; the ledger entry's path and close; the
    proof-of-spec instance path and its check result; commit hashes and the measured push state. Leave the status flip to
    the issuer.
  </report>

## AMENDMENT 1 (2.0.0_SA_COO~C, 2026-10-08 ~07:2xZ) -- the apply is TARGETED at the five signed resources (the applier's STOP of msg 106815 was right)

The issuer merged the cell's next pass (plan 2's Allow) into the trunk before this plan had applied, so an untargeted plan
read seven resources; `0.7.0_AE_CloudOps~E` stopped at step 3 and applied nothing. That was the correct reading of branch B
and the error is the issuer's. The act is now targeted at exactly:
`aws_iam_policy.dell_agent_vendor_secrets[0]`, `aws_iam_group_policy_attachment.dell_agent_vendor_secrets[0]`,
`aws_iam_policy.dell_agent_create`, `aws_iam_policy.dell_agent_respol`, `aws_iam_group_policy_attachment.dell_agent_respol`.
The issuer's targeted plan at ~07:1xZ: `2 to add, 1 to change, 2 to destroy`, 66 secret ARNs, zero occurrences of `respol_allow`.
Added to the STOP conditions of step 3: the string `respol_allow` anywhere in the plan, or any sixth resource. The COO half
carries CORRECTION 1 to the same effect; the GO for this amendment names the CTO's concurrence. Steps 3, 5 and 6 and criterion
AC2 are edited above accordingly. Gate limb: none graded this modification. Row NFRA_CTLPLN-S25 is disarmed by this amendment
and the correction: the unsigned Allow cannot ride a plan targeted at five other resources.
</task_order>
