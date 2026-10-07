<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-4.dell2-fence-join-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain" act 1: the apply leg of cell `CT-d-2`, complete as a build.
<owned_cells>CT-d-2</owned_cells>
</decomp_ref>

  <objective>
    Apply THREE bucket-policy updates so the dell2 box can read the firm data its own projects are placed on. Today the three fenced
    firm data buckets refuse `cloudops-dell2-agent-user`; five projects placed on dell2 read them and dell2 is asking the laptop to
    proxy reads. This is the first-priority act of round 4 (CTO msg 106089). It is a cross-firm access change, so the plan's exact
    shape gates the apply.
  </objective>

  <context>
    The three fences are `aws_s3_bucket_policy.opal_data_49financial` (`infra/aws/terraform/shared-infra/s3-49financial.tf`) and
    `aws_s3_bucket_policy.lgic_firm` (`s3-lgic-firm-buckets.tf`, a `for_each` that builds exactly two buckets, cottonwood and
    inflection). Each policy's admitted list is rendered by `module.opal_name.fence_exemption_arns` from
    `infra/logic/registry/exemptions.json`. `4.0.0_SA_CRO` landed three rows there @e7ac51a04c, one per bucket, for
    `arn:aws:iam::313476888478:user/cloudops-dell2-agent-user`. NO `.tf` file changed. dell1 is admitted to nothing.
    NOT measured by the issuer: the plan. A read-only plan from the issuer's session stopped at "Backend initialization required";
    the issuer did not initialise the root. Whether `terraform init` of this root needs a provider that is not already on this box is
    your first read: if init would have to FETCH a provider from the registry, STOP and report (do not fetch).
    The CRO also measured that `modules/opal_name/generated_locals.tf` differs from a fresh regenerate in its header registry mark
    only; a header comment should not reach a plan.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and bind on the plan shape below. ONE go, no second message: you grade the plan yourself.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL2_FENCE_JOIN_20261007.md
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL2_FENCE_JOIN_20261007.md (@91f1667810)
    Read both in full first and carry every condition of both.

    THE COMMIT: the shared tree at its HEAD on CLOUD. First show that the three inputs are what the halves read:
    `git log -1 --format=%H -- infra/logic/registry/exemptions.json` is e7ac51a04c (or a later commit that leaves the three dell2 rows
    byte-identical: show it), and `git diff 3ec42c56bf HEAD -- infra/aws/terraform/shared-infra/s3-49financial.tf infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf`
    prints nothing, and neither file is modified in the working tree.

    1. Load /cloud-ops. Run `python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py` (expect
       `rows=3/3 typed_in_tf=0 cross_firm_leaks=0 ... validator=ok ok=True`). A failing check is a STOP.
    2. BEFORE: save each of the three LIVE bucket policy documents into your deliverables folder (`s3api get-bucket-policy`), with
       its SHA-256. These are the rollback reference: S3 keeps no prior version.
    3. Plan the root with terraform directly, TARGETED:
       `-target=aws_s3_bucket_policy.opal_data_49financial -target=aws_s3_bucket_policy.lgic_firm`.
       - The plan reads EXACTLY 3 to change, 0 to add, 0 to destroy (the two targets expand to three resources), and in each policy's
         diff the ONLY change is the one added string `arn:aws:iam::313476888478:user/cloudops-dell2-agent-user` inside the
         `ArnNotLike` list of `DenyForeignFirmPrincipals` -> go to 4.
       - ANY other plan (another resource, another statement, another changed value, a target dragging in a dependency that changes)
         -> apply NOTHING. Report the plan as read to 2.0.0_SA_COO~C and stop.
    4. Open ONE NEVER-2 ledger entry, slug `nfra-ctlpln-dell2-fence-join-laptop-20261007` (the registry rows' `signoff_ref` cites this
       slug), naming the laptop as the box, the three saved prior documents by path and hash, and the rollback per key as the COO
       half states it.
    5. ONE apply through the wrapper, with the same two targets: `.tools/safe-apply.sh -chdir=infra/aws/terraform/shared-infra apply ...`.
       If it errors part-way (one or two of three applied): finish or roll back in-session per the entry, and say which.
    6. Prove it (the criteria below), then: each of the three LIVE policies equals its saved prior document plus the one added
       principal (parsed comparison, and a planted-mutant control); `iam simulate-principal-policy` with each LIVE policy as the
       resource policy -- `cloudops-dell2-agent-user` on `s3:GetObject`: allowed x3; `cloudops-dell1-agent-user`: NOT allowed x3; one
       principal that was refused before and has no row (pick it from `tests/dell_fence_census.json`, name it): still NOT allowed x3;
       and one principal the fence admitted before (the control): still allowed. Close the entry.
       You do NOT read any object in any firm bucket: the box arm (dell2 reads one object per bucket) is run from dell2 by another route.
  </the_act>

  <bounds>
    - These three resources only. No untargeted apply of this root, no other root, no edit to any `.tf` or registry file.
    - `safe-apply` only; never a bare `terraform apply`. No push of a shared branch. No object read in any firm bucket.
    - No provider fetch from the registry: if init needs one, that is a STOP with a report.
    - A plan that differs from the expected three is a STOP with a report.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the built cell's evaluator arms (check_dell_fence_join.py: dell2 allowed x3 on the edited documents, dell1 denied on the live one); the order's step 6 repeats them against the LIVE policies after the apply.
comp-adversary: RUN -- a cross-firm leak (rows keyed by bucket, dell1 admitted to none, the census re-read of all 24 buckets after the apply); a plan that carries more than the three fences (targeted, exact shape, any other line is a stop); no way back (S3 keeps no prior policy: the three documents are saved before the apply and named in the ledger entry); a half-landed apply (finish or roll back in-session); BLIND: an access path outside the bucket policy -- the dell2 box read is the test, run by another route.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/check_dell_fence_join.py</invocation><expect>rows=3/3 typed_in_tf=0 cross_firm_leaks=0</expect></criterion>
  <criterion id="AC2" cell_refs="CT-d-2"><invocation>python infra/aws/terraform/shared-infra/tests/dell_fence_census.py --live</invocation><expect>gap_dell2=0</expect></criterion>
  <criterion id="AC3" cell_refs="CT-d-2"><invocation>terraform -chdir=infra/aws/terraform/shared-infra plan -input=false -no-color -lock=false -detailed-exitcode -target=aws_s3_bucket_policy.opal_data_49financial -target=aws_s3_bucket_policy.lgic_firm; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes (or at a STOP): the plan's counts, addresses and the three diffs as read; the
    three prior documents' paths and hashes; the live-versus-prior comparison per bucket; every simulator arm with its decision; the
    census's live last line after the apply (AC2: it re-reads all 24 buckets; `dell1_admitted` must be unchanged from 21/24 and
    `gap_dell1` still 0); the ledger entry's path and its close; the proof-of-spec instance path (genre DEPLOY) and its check result;
    commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
  <amendment id="1" by="2.0.0_SA_COO~C" date="2026-10-07">
    YOUR STOP AT THE PLAN GATE WAS RIGHT (msg 106147): the cottonwood fence carries another project's unapplied statements, and both
    halves voided on it. Both halves are now AMENDED AND SIGNED for a narrower act:
    - COO half, AMENDMENT 1: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL2_FENCE_JOIN_20261007.md
    - CTO half, AMENDMENT 1 (@341eeb04bd): org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL2_FENCE_JOIN_20261007.md
    Read both amendments in full. WHERE THIS AMENDMENT AND THE ORDER ABOVE DIFFER, THIS AMENDMENT GOVERNS.

    THE ACT NOW: ONE targeted apply of exactly TWO resources,
    `-target=aws_s3_bucket_policy.opal_data_49financial -target='aws_s3_bucket_policy.lgic_firm["inflection"]'`
    (quote the second target so the shell passes the brackets and quotes through; echo the argument back to confirm).
    - Step 2: save all THREE live policy documents as before (the cottonwood one is the proof it was not touched); the ledger entry
      names the two that the apply changes as the rollback reference.
    - Step 3: the plan reads EXACTLY 2 to change, 0 to add, 0 to destroy; each diff is the one added dell2 principal;
      `lgic_firm["cottonwood"]` does not appear. Any other plan: apply nothing, report.
    - Step 4: the same ledger slug, `nfra-ctlpln-dell2-fence-join-laptop-20261007`; the entry says two buckets and names the cottonwood
      fence as deliberately NOT applied, with the reason.
    - Step 6, read-back: the two live policies equal prior plus one principal; the cottonwood live policy is byte-equal to the
      document saved in step 2; simulator with each LIVE policy: dell2 allowed x2; dell2 NOT allowed on the cottonwood bucket; dell1
      not allowed x2; one unlisted, previously refused principal still refused; one previously admitted principal still allowed.
      Then a re-plan of the two targets reads no changes. Also run, and report as EXPECTED and not as drift, a plan of
      `lgic_firm["cottonwood"]` alone: it still shows the dell2 principal and the three rider statements pending.
    - Criteria: AC1 unchanged. AC2 (the live census) now expects `gap_dell2=1` (the cottonwood bucket remains) with `dell1_admitted`
      unchanged at 21/24 and `dell2_admitted` 23/24. AC3's invocation uses the two targets of this amendment and expects `exit=0`.
  </amendment>
</task_order>
