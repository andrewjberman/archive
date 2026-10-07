<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-5.cottonwood-fence-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain" act 1: the THIRD fence of cell `CT-d-2`, complete as a build; the first two fences were applied under TO-APPLY-4.
<owned_cells>CT-d-2</owned_cells>
</decomp_ref>

  <objective>
    Apply ONE bucket-policy update: the cottonwood firm bucket's fence. It carries two things in one in-place update, because the
    resource can only be applied whole: (1) this project's line, the dell2 box user added to the fence's admitted list, so dell2's
    placed projects can read that firm's data; (2) ADVI_COTBKF's three Deny statements on the restricted CRM prefix, which arrive
    with that project's own two halves. You stopped the first attempt at exactly this rider (msg 106147); it now has its pair.
  </objective>

  <context>
    The resource is `aws_s3_bucket_policy.lgic_firm["cottonwood"]` in `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf`.
    You measured its pending diff under TO-APPLY-4: the dell2 principal plus three whole statements
    (`DenyRestrictedReadExceptReaders`, `DenyRestrictedListExceptReaders`, `DenyRestrictedWriteExceptBreakglass`), and after the
    two-bucket apply you reported it still pending, as expected. The registry row for this bucket landed @e7ac51a04c (`4.0.0_SA_CRO`).
    The issuer writes no ADVI_COTBKF artifact and rules nothing of that project (Andrew-direct ~06:1xZ keeps this seat off the
    Cottonwood backfill project; `1.0.0_SA_CTO` ruled, msg 106172, that joining dell2 to this fence is NFRA_CTLPLN's work and the
    policy applies whole). The three statements are signed by that project's seats, not by the issuer.
  </context>

  <the_act>
    FOUR halves bear on this one apply. Read ALL FOUR in full first, at the trunk HEAD you apply from:
    - NFRA_CTLPLN COO half, AMENDMENT 2 (the dell2 line only): org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL2_FENCE_JOIN_20261007.md
    - NFRA_CTLPLN CTO half, AMENDMENT 2 (@2714b7df72): org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL2_FENCE_JOIN_20261007.md
    - ADVI_COTBKF COO half with its AMENDMENT 1 (@f9150f248a): org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_C_RESTRICTED_STATEMENTS_COO_HALF.md
    - ADVI_COTBKF CTO half, amended (@b4073b7bf2): org/missions/D8/ADVI/ADVI_COTBKF/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_CB_d_4_RESTRICTED_PREFIX_STATEMENTS_CTO_HALF.md

    STEP 0, THE CONFLICT READ, BEFORE ANY AWS CALL: list every condition of the four halves in one table (which half, the condition,
    how you will measure it). If two halves ask for things that cannot both hold on one plan, STOP and report the pair to
    2.0.0_SA_COO~C: do not choose between them. One the issuer already sees and does NOT resolve: the NFRA_CTLPLN CTO half voids on
    any role or role-policy line in the plan ("the break-glass role is a separate act"), while the ADVI_COTBKF COO half's Branch A
    describes a plan in which the break-glass role and its inline policy are created. Your TO-APPLY-4 plan read 0 to add for this
    resource. Read both texts as amended and say plainly whether a plan with NO role line satisfies the ADVI_COTBKF pair as written.
    If it does not, STOP at step 0.

    THE COMMIT: the shared tree at its HEAD on CLOUD. Show `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` is unmodified
    in the working tree and print the commit that last changed it; show the registry row for this bucket is present.

    1. Load /cloud-ops. Run `python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py` (it pins the two `.tf` files to
       commit 3ec42c56bf: if another project has since changed `s3-lgic-firm-buckets.tf`, it will FAIL on that; then report the diff
       and stop -- the issuer amends the pin) and, IMMEDIATELY before the apply as the ADVI_COTBKF COO half requires (its CB4d4-AC1),
       `python infra/aws/terraform/shared-infra/tests/check_restricted_prefix.py`. Record both last lines. A failing check is a STOP.
    2. BEFORE: save the cottonwood bucket's LIVE policy document with its SHA-256 (the rollback reference: S3 keeps no prior
       version); and the listing the ADVI_COTBKF halves require: `commonwealth/cottonwood/bronze/crm/` in that bucket holds 0 objects
       (a key COUNT only, auto-paginated, counted client-side; you read no object). A non-zero count is a STOP.
    3. Plan, targeted at `'aws_s3_bucket_policy.lgic_firm["cottonwood"]'` alone (quote it; echo the argument back).
       - EXACTLY 1 to change, 0 to add, 0 to destroy; the diff is the dell2 principal
         `arn:aws:iam::313476888478:user/cloudops-dell2-agent-user` added to `DenyForeignFirmPrincipals`' list and the three
         statements named above, by Sid, and nothing else -> go to 4.
       - ANY other line (a role, a role policy, another bucket's row, another statement, another changed value) -> apply NOTHING;
         report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry, naming the laptop, the saved prior document by path and hash, all four halves, and the
       rollback per half (this project's line: the registry row removed and the same targeted apply; the three statements: as the
       ADVI_COTBKF halves state).
    5. ONE apply through `.tools/safe-apply.sh` with the same single target.
    6. Read-back, each arm ATTRIBUTED (matched statements) as you did before:
       - the LIVE policy equals the saved prior document plus the one principal plus the three statements (parsed comparison, with a
         planted-mutant control);
       - this project's arms: dell2 `allowed` on `s3:GetObject` for a key OUTSIDE the restricted prefix; dell1 NOT allowed on the
         bucket; one unlisted, previously refused principal still refused; one previously admitted principal still allowed outside
         the prefix;
       - the ADVI_COTBKF halves' arms, run and reported under THEIR conditions as they state them (the agents' user denied on the
         prefix and admitted elsewhere in the bucket; the console user's arm as their text gives it; and the NFRA_CTLPLN CTO half's
         condition 3: dell2 refused read, list and put ON the prefix; `user/Andrew_Berman` refused the same three on the prefix and
         still reading outside it);
       - a re-plan of the same target reads no changes;
       - the live fence census: `python infra/aws/terraform/shared-infra/tests/dell_fence_census.py --live`.
       Close the entry. You read no object in any firm bucket; the box arm (dell2 reads one object from dell2) is another route's.
  </the_act>

  <bounds>
    - This one resource only. No untargeted apply, no other root, no edit to any `.tf` or registry file, no role created by you.
    - `safe-apply` only. No push of a shared branch. No object read in any firm bucket; the prefix listing is a key count only.
    - Named so it is not a surprise: after this apply the laptop's own identity is refused read, list and put on the restricted
      prefix. That is ADVI_COTBKF's stated intent. Do not try to read that prefix afterwards except through the simulator.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the built cell's evaluator arms (check_dell_fence_join.py) and, for the rider, by ADVI_COTBKF's own check (check_restricted_prefix.py), both re-run by the applier immediately before the apply; step 6 repeats every arm against the LIVE policy with matched statements.
comp-adversary: RUN -- two projects' changes in one resource with four halves (step 0's conflict read; a stop, never a choice); a plan that drags in a role (exact shape; a role line is a stop); no way back (the prior document saved before the apply); a rider applied on a prefix that holds data (the key count must read 0); the laptop locking itself out of a prefix it needs (named in bounds; the prefix is empty and is ADVI_COTBKF's by design); BLIND: an access path outside the bucket policy -- the dell2 box read is the test, by another route.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py</invocation><expect>rows=3/3 typed_in_tf=0 cross_firm_leaks=0</expect></criterion>
  <criterion id="AC2" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/dell_fence_census.py --live</invocation><expect>dell2_admitted=24/24</expect></criterion>
  <criterion id="AC3" cell_refs="CT-d-2"><invocation>terraform -chdir=infra/aws/terraform/shared-infra plan -input=false -no-color -lock=false -detailed-exitcode -target='aws_s3_bucket_policy.lgic_firm["cottonwood"]'; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): step 0's condition table and your reading of
    the role question; both check lines; the prior document's path and hash and the prefix key count; the plan's counts and the diff
    as read; every simulator arm with its decision and matched statement, grouped by the half whose condition it serves; the live
    census last line (`dell2_admitted`, `dell1_admitted`, `gap_dell1`, `gap_dell2`); the ledger entry's path and close; the
    proof-of-spec instance path (genre DEPLOY) and its check result; commit hashes and the measured push state. Leave the status flip
    to the issuer.
  </report>
</task_order>
