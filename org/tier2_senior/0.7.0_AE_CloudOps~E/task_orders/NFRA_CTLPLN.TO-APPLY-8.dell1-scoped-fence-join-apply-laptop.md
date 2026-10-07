<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-8.dell1-scoped-fence-join-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-07</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain": the apply leg of cell `CT-d-2` as amended (dell1's read-only, prefix-scoped join; complete as a build, last merge @17b61b4124).
<owned_cells>CT-d-2</owned_cells>
</decomp_ref>

  <objective>
    Apply ONE targeted update of three firm bucket policies so the dell1 box user can READ one holdings prefix in each of the three
    firm buckets and nothing else there. It is a widening for one principal, bounded in the same apply by three Deny statements
    per bucket. You applied these same three resources for dell2 under TO-APPLY-4 and TO-APPLY-5.
  </objective>

  <context>
    Root `infra/aws/terraform/shared-infra/`. Three things landed in the order the CTO ruled: the renderer that turns a registry
    row carrying `actions` and `prefix` into three confining Deny statements (@3b6c321227); the three scoped rows in
    `infra/logic/registry/exemptions.json` (@d5516cb074, by `4.0.0_SA_CRO`); and the two checks made to hold on that registry
    (@17b61b4124). dell1's own identity policy allows get, put and list on the estate's bucket pattern, so plain admission would
    be whole-bucket read and write: the three `DenyScopedExemption1...` statements are what make this read-only and prefix-bound.
    The issuer planned it read-only at ~18:1xZ (exit 2): three in-place updates, 0 to add, 0 to destroy; 129 added lines, 0 removed.
    The cottonwood policy carries, applied today, three restricted-prefix statements of another project and the dell2 line: this
    act leaves them untouched.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and each binds on the plan shape below. ONE go, no second message.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL1_SCOPED_FENCE_JOIN_20261007.md (@ca90fc5303)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL1_SCOPED_FENCE_JOIN_20261007.md (@f4643f1530)
    Read both in full first and carry every condition of both (the COO half's six; the CTO half's seventh).

    THE COMMIT: the shared tree at its HEAD on CLOUD. Show that `infra/aws/terraform/shared-infra/s3-49financial.tf`,
    `s3-lgic-firm-buckets.tf`, `infra/aws/terraform/modules/opal_name/main.tf` and `infra/logic/registry/exemptions.json` are
    unmodified in the working tree and equal their bytes at `17b61b4124` (`git diff --stat 17b61b4124 HEAD -- <those four>` prints
    nothing). A difference is a STOP: another seat changed a fence input after the halves were signed.

    1. Load /cloud-ops. Run both checks IMMEDIATELY before the plan and record each last line:
       `python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py` (expect `cross_firm_leaks=0 ... scoped_rows=3 scoped_confined=3/3 ok=True`) and
       `python infra/aws/terraform/shared-infra/tests/check_fence_scoped_rows.py` (expect `unchanged_today=True scoped_rendered=9/9 sim_ok=30/30 refusals_ok=7/7 ... ok=True`).
       A failing check is a STOP.
    2. BEFORE: save each of the three buckets' LIVE policy documents with its SHA-256 (the rollback references; S3 keeps no prior
       version). Run the live fence census and record its last line (expected before: `dell1_admitted=21/24 gap_dell1=1`).
    3. Plan, targeted at exactly `aws_s3_bucket_policy.opal_data_49financial`, `'aws_s3_bucket_policy.lgic_firm["cottonwood"]'`
       and `'aws_s3_bucket_policy.lgic_firm["inflection"]'` (quote them; echo the arguments back).
       - EXACTLY `0 to add, 3 to change, 0 to destroy`, those three addresses. CLASSIFY every added line per bucket: the one dell1
         ARN in `DenyForeignFirmPrincipals`' admitted list, and three whole statements by Sid
         (`DenyScopedExemption1AnyOtherAction`, `...ObjectsOutsidePrefix`, `...ListingOutsidePrefix`), each naming the dell1 user
         and that bucket's own `irpt/<firm>/platinum/holdings/` prefix. ZERO removed lines; no other statement changed -> go to 4.
       - ANY removed line, any change in another statement, a prefix naming another firm, a fourth resource, a role, or another
         count -> apply NOTHING; report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the three saved documents by path and hash, both halves, and the rollback
       per bucket (put the saved document back; or the registry's lane removes that bucket's row and the same targeted apply).
    5. ONE apply through `.tools/safe-apply.sh` with the same three targets.
    6. Read-back LIVE, per bucket, by the simulator against the LIVE policy with dell1's live attached policies, each arm with its
       matched statement NAMED:
       - dell1 `s3:GetObject` under the prefix -> allowed; `s3:GetBucketLocation` -> allowed; `s3:ListBucket` with the prefix -> allowed;
       - dell1 `s3:GetObject` outside the prefix, `s3:PutObject` under the prefix, `s3:ListBucket` with NO prefix, and
         `s3:GetObjectVersion` under the prefix -> each explicitDeny by a `DenyScopedExemption1...` statement;
       - dell2 `s3:GetObject` outside the prefix -> still allowed; one unlisted, previously refused principal -> still refused;
       - on cottonwood: dell1 refused on the restricted prefix `commonwealth/cottonwood/bronze/crm/`;
       - the live document equals the saved one plus the planned additions (parsed, with a planted-mutant control);
       - a re-plan of the three targets reads no changes;
       - the live fence census: its `dell1_admitted` is expected to read 24/24 and is reported with the words "scoped, 3 of 24".
       Close the entry. You read NO object and list NO firm bucket. The exercised read is dell1's own, from dell1, by another
       route; until it runs the join is APPLIED, not EXERCISED: say so in those words.
  </the_act>

  <bounds>
    - These three resources only. No untargeted apply, no other root, no edit to any `.tf`, module, registry or test file.
    - `safe-apply` only. No push of a shared branch. No object read, no listing of any firm bucket.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's two checks (30 of 30 simulator arms on the saved policies plus the rendered statements, 7 of 7 planted refusals each from a valid control, scoped_confined 3 of 3; the issuer re-ran both before the merge) and re-run by the applier immediately before the plan; step 6 repeats the arms against the LIVE policies with matched statements.
comp-adversary: RUN -- admission without confinement (whole-bucket read and write for dell1: the plan must show the three Deny statements beside the admitted ARN in each bucket, or it is a stop); a prefix naming another firm (classified per bucket at the plan; the validator refuses it); a fence input changed after signing (the four-file byte check against 17b61b4124); another project's statements on cottonwood disturbed (zero removed lines; the restricted-prefix arm in step 6); no way back (three documents saved before the apply); a census that reads full admission (reported as scoped, 3 of 24); BLIND: a real read (dell1's own, owed after), organization policies, and whether a real list request sends the prefix the simulator was given.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py</invocation><expect>cross_firm_leaks=0</expect></criterion>
  <criterion id="AC2" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/check_fence_scoped_rows.py</invocation><expect>scoped_rendered=9/9 sim_ok=30/30 refusals_ok=7/7</expect></criterion>
  <criterion id="AC3" cell_refs="CT-d-2"><invocation>terraform -chdir=infra/aws/terraform/shared-infra plan -input=false -no-color -lock=false -detailed-exitcode -target=aws_s3_bucket_policy.opal_data_49financial -target='aws_s3_bucket_policy.lgic_firm["cottonwood"]' -target='aws_s3_bucket_policy.lgic_firm["inflection"]'; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the four-file byte check; both check lines;
    the three saved documents' paths and hashes; the census line before and after; the plan's count and the per-bucket
    classification of added lines; every simulator arm per bucket with its decision and matched statement; the re-plan's exit;
    the ledger entry's path and close; the proof-of-spec instance path (genre DEPLOY) and its check result; commit hashes and the
    measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
