<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-10.dell1-full-fence-admission-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain": a further apply leg of cell `CT-d-2` (dell1's join to the three fences, now in full by Andrew's word; the cell's AMENDMENT 7 repaired its two checks for this registry).
<owned_cells>CT-d-2</owned_cells>
</decomp_ref>

  <objective>
    Apply ONE targeted update of the same three firm bucket policies you applied under TO-APPLY-8, this time REMOVING the three
    confining Deny statements from each, so the dell1 box user is admitted in full, as dell2 is. Andrew lifted this limit at
    ~00:4xZ; dell1's seats are waiting on it.
  </objective>

  <context>
    Root `infra/aws/terraform/shared-infra/`. Andrew-direct ~00:4xZ, "lets start with lifting 1 2 3 6" (record
    org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_004xZ_LIFT_FOUR_DELL_LIMITS_SECRETS_FIRM_DATA_RESOURCE_POLICIES_PUSH.md);
    `1.0.0_SA_CTO` msg 106669 ruling 2. `4.0.0_SA_CRO` made the three `cloudops-dell1-agent-user` rows full rows @173f98f24b.
    The issuer planned it read-only at ~01:0xZ (exit 2): three in-place updates; 126 removed lines, 0 added; in each policy the
    three `DenyScopedExemption1...` statements leave and the dell1 user stays in the admitted list.
    FULL WIDTH, as both halves state it: dell1's own policy allows put on the estate's buckets, so after this act dell1 can read
    AND write any object in the three firm buckets, as dell2 can today.
    Since TO-APPLY-9 the two apply wrappers print WARN lines from two new seat-gate checks (cell CT-s-3). They are in WARN mode:
    they print and do not stop anything. Report the lines they print for this apply.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and each binds on the plan shape below. ONE go, no second message.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL1_FULL_FENCE_ADMISSION_20261008.md (@d4310763b7)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL1_FULL_FENCE_ADMISSION_20261008.md (@31538ec99d)
    Read both in full first and carry every condition of both (seven, and the CTO's added one on the checks).

    THE COMMIT: the shared tree at its HEAD on CLOUD, which must contain the merge of cell CT-d-2 AMENDMENT 7 (the issuer's GO
    message names that merge commit). Show the registry file's three dell1 rows carry no `actions` and no `prefix`, and that the
    two fence `.tf` files and `infra/aws/terraform/modules/opal_name/main.tf` are unmodified in the working tree.

    1. Load /cloud-ops. Run both checks IMMEDIATELY before the plan and record each last line:
       `python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py` (expect `pairs=6 rows=6/6 ... cross_firm_leaks=0 ... ok=True`)
       and `python infra/aws/terraform/shared-infra/tests/check_fence_scoped_rows.py` (expect `refusals_ok=7/7 ... ok=True`).
       CTO's added condition: confirm from the join check's output that the arm "an unlisted principal is still refused" is
       PRESENT with its denominator. A failing check, or that arm missing, is a STOP.
    2. BEFORE: save each of the three buckets' LIVE policy documents with its SHA-256. Run the live fence census and record its
       last line (expected before: `dell1_admitted=21/24 dell1_scoped=3 ... disagree=0 ok=True`).
    3. Plan, targeted at exactly `aws_s3_bucket_policy.opal_data_49financial`, `'aws_s3_bucket_policy.lgic_firm["cottonwood"]'`
       and `'aws_s3_bucket_policy.lgic_firm["inflection"]'`.
       - EXACTLY `0 to add, 3 to change, 0 to destroy`; in each policy exactly the three statements
         `DenyScopedExemption1AnyOtherAction`, `DenyScopedExemption1ObjectsOutsidePrefix` and
         `DenyScopedExemption1ListingOutsidePrefix` removed whole; ZERO added lines; the admitted list unchanged; no other
         statement touched -> go to 4.
       - ANY added line, any other statement touched, an admitted list changed, a fourth resource, another count -> apply
         NOTHING; report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the three saved documents by path and hash, both halves, and the
       rollback per bucket (put the saved document back; or the registry's lane restores that bucket's scoped row and the same
       targeted apply).
    5. ONE apply through `.tools/safe-apply.sh` with the same three targets.
    6. Read-back LIVE, per bucket, by the simulator against the LIVE policy with dell1's live attached policies, each arm with
       its matched statement named: dell1 `s3:GetObject` and `s3:PutObject` OUTSIDE the old holdings prefix -> now allowed;
       dell1 `s3:ListBucket` with no prefix -> allowed; on cottonwood, dell1 still refused on the restricted prefix
       `commonwealth/cottonwood/bronze/crm/`; dell2 unchanged; one unlisted, previously refused principal still refused. The
       live document equals the saved one minus the three statements (parsed, with a planted-mutant control). A re-plan of the
       three targets reads no changes. The live fence census, expected `dell1_admitted=24/24 dell1_scoped=0 disagree=0 ok=True`.
       Close the entry. You read NO object and list NO firm bucket. APPLIED, not EXERCISED, until dell1's own reads.
  </the_act>

  <bounds>
    - These three resources only. No untargeted apply, no other root, no edit to any `.tf`, module, registry or test file.
    - `safe-apply` only. No push of a shared branch. No object read, no listing of any firm bucket.
    - The cross-box deploy notice on `infra/aws/terraform/opal-assets` (until 06:20Z) does not concern this root.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's two repaired checks (the six expected unscoped pairs as data; an unlisted principal still refused; seven planted refusals) and re-run by the applier immediately before the plan; step 6 repeats the arms against the LIVE policies with matched statements.
comp-adversary: RUN -- a plan that admits more than dell1 (zero added lines; the admitted lists unchanged; exact statements removed); another project's statements on cottonwood disturbed (the restricted-prefix arm in step 6); a check made to pass by losing an arm (the CTO's added condition, read by the applier from the check's own output); no way back (three documents saved before the apply); BLIND: a real read or write from dell1 (its own, owed after), and organization policies.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py</invocation><expect>cross_firm_leaks=0</expect></criterion>
  <criterion id="AC2" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/dell_fence_census.py --live</invocation><expect>dell1_admitted=24/24 dell1_scoped=0</expect></criterion>
  <criterion id="AC3" cell_refs="CT-d-2"><invocation>terraform -chdir=infra/aws/terraform/shared-infra plan -input=false -no-color -lock=false -detailed-exitcode -target=aws_s3_bucket_policy.opal_data_49financial -target='aws_s3_bucket_policy.lgic_firm["cottonwood"]' -target='aws_s3_bucket_policy.lgic_firm["inflection"]'; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): both check lines and the unlisted-principal
    arm as read; the three saved documents' paths and hashes; the census line before and after; the plan's count and the
    per-bucket classification of removed lines; every simulator arm per bucket with its decision and matched statement; the
    re-plan's exit; the seat-gate WARN lines the wrapper printed; THE APPLIED TIME in UTC (the CTO passes it to dell1); the
    ledger entry's path and close; the proof-of-spec instance path and its check result; commit hashes and the measured push
    state. Leave the status flip to the issuer.
  </report>
</task_order>
