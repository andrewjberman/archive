<task_order>
  <metadata>
    <id>MDPF_STRATID.TO-APPLY-D2.mdpf-gold-lambda-targeted-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>MDPF_STRATID</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_STRATID/decompositions/MDPF_STRATID_DECOMP.md</decomp_doc>
<owned_cells>ST-t-3</owned_cells>
<decomp_context>dell1's decomposition (on origin box/dell1; reaches the laptop tree at the next box pass): ST-t-3, "deployed by the issuer at the drain under the C-GLOBAL-PAIR". Leg D2 of dell1's ledger mdpf-stratid-r1-global-pfde-fold. dell1 1.0.0_SA_CTO~DELL1 msg 1189, relay org/tier0_exec/0.0.0_AB_MSTR/deliverables/RELAY_DELL1_STRATID_D2_APPLY_ASK_2145Z.md; 1.0.0_SA_CTO msg 107370 (agreed).</decomp_context>
</decomp_ref>

  <objective>
    Apply D2 of dell1's MDPF_STRATID R1: move `mdpf-gold-lambda` to the package built from pin `148f715f8c`, by a targeted Terraform
    apply of `aws_lambda_function.mdpf_gold` in `infra/aws/terraform/mdpf-pipeline`. dell1 cannot plan the root (its user is denied
    `ssm:GetParameter` on `/mdpf/custody_source`).
  </objective>

  <context>
    Recipe and expected plan: `git show 3a7154fcbf:org/missions/D8/MDPF/MDPF_STRATID/deliverables/2.0.0_SA_COO~S1/D2_HANDOFF_20261008.md`
    (origin box/dell1). Pair: `NEVER_WIDEN_PAIR_R1_GLOBAL_PFDE_FOLD.md` on box/dell1, both halves SIGNED (laptop CTO half
    @c1484b8bb4). dell1's ledger `20261008T2137Z_mdpf-stratid-r1-global-pfde-fold` is OPEN on dell1, D1 landed 21:39:13Z; dell1
    rolled back its own partial D2 (the S3 zip restored; the function never moved: CodeSha256 `BZAtvS5mfjkkt9zi1zzkGm007DL21qwYsjM9K5XAypA=`).
    NEVER `aws lambda update-function-code` (CLAUDE.md NEVER-9): Terraform only.
  </context>

  <the_act>
    1. Load /cloud-ops. Read `get-function mdpf-gold-lambda` CodeSha256: expect `BZAtvS5mfjkkt9zi1zzkGm007DL21qwYsjM9K5XAypA=`
       (else STOP: the function moved since dell1's rollback). Record the current version id of
       `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip`.
    2. Build: `python infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py --pin 148f715f8c --out <zip>` -> exactly
       1,712,878 bytes, sha256 `d203dce7f914a3eb04f019ef84a839c0ef885e20c2078bd12b972fcb569cfb62`. Any other size or hash is a STOP.
    3. Open ONE NEVER-2 entry naming dell1's ledger and leg D2, the saved CodeSha256 and zip version id, both halves, and the rollback
       (re-promote the saved zip version and a targeted apply back to it; the function reads back `BZAtvS5m...`).
    4. `aws s3 cp <zip> s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip --metadata content-sha256=d203dce7...cfb62`.
    5. `terraform -chdir=infra/aws/terraform/mdpf-pipeline plan -target=aws_lambda_function.mdpf_gold` -> EXACTLY `0 to add, 1 to
       change, 0 to destroy`, the change `s3_object_version` and `source_code_hash` only -> `.tools/safe-apply.sh` with that plan.
       Anything else -> apply nothing, re-promote the saved zip version, report.
    6. Read back `get-function` CodeSha256 = `0gPc5/kUo+sE8BnvhKg5wO+IXiDCB4vRK5cvy1ac+2I=`; targeted re-plan no changes. Close your entry
       and send dell1 the applied time and CodeSha256 for its ledger leg L3, through 0.0.0_AB_MSTR.
  </the_act>

  <bounds>
    - One function, one S3 object, one targeted apply. No other resource in the root. No invoke of the function.
    - No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat inside dell1's ledger; the function's own schedule is unchanged.
comp-iam: DECLARED-NOT-APPLICABLE no identity change (dell1's missing ssm:GetParameter on /mdpf/custody_source is a separate NFRA_CTLPLN finding).
comp-adversary: RUN -- a moved function before the act (CodeSha256 must equal dell1's rollback read); a non-deterministic build (exact size and hash); a wider plan (targeted, exactly s3_object_version + source_code_hash); no way back (saved zip version, re-promote, targeted re-apply); BLIND: whether the EC2 MDPF daily runner reads code/scripts/gold/ (dell1's open question; inside the signed blast radius).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="ST-t-3"><invocation>aws lambda get-function --function-name mdpf-gold-lambda --query Configuration.CodeSha256 --output text</invocation><expect>0gPc5/kUo+sE8BnvhKg5wO+IXiDCB4vRK5cvy1ac+2I=</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C (and the applied time + CodeSha256 to dell1 via 0.0.0_AB_MSTR): the before CodeSha256 and zip
    version; the build's size and hash; the plan count and diff; the applied time in UTC in the subject; the read-back; the ledger
    entry; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
