<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R32R.resident-r32-aq2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-15</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed pair (packet section 2, by branch): the resident host gains one new root, the receipt, the unit's ExecStart and the kept library copy; the producer list moves to andrew and fwd1-staff-r41b; the Opal maps are selected per report variant; the commentary family irpt-anlreq-x10-v1 is registered; opal_pricing ships OFF. No IAM, Lambda, queue, table, schema or route moves; no vendor call.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM statement is added or changed; the host role holds GetObject on the keys and that is unchanged.
comp-adversary: RUN -- by reading the CTO half (msg 8693, six conditions) and the install scripts' guards against this cell; the lens: a running root that is not r31 (exit 34/40), a fetched script or sums file that is not the signed bytes (31/33), a key that already exists, a member outside the counted 15 changed and 11 added that differs, a queue that is not 0/0, a failed start (the install rolls itself back), an unsigned or changed packet blob. NOT seen (blind): the live host and S3 keys until steps 2 and 3; denominator: 310 members (15 changed, 11 added, 284 identical), 3 keys, 4 scripts.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R21_G.md</decomp_doc> round 21, workstream ~G: the apply of the release-32 resident (leg R only).
<owned_cells>AR-g-97</owned_cells>
</decomp_ref>

  <objective>
    Apply release 32 to the resident host, leg R and nothing else: upload the three staged artifacts, run the pre-read, run the signed install, read the running package back, write one record, close the ledger. Then report ONCE to 2.0.0_SA_COO~G2. If any step does not read green, STOP, leave the host as it was (the install rolls itself back on a failed start), and report. The Lambda leg (irpt-ycharts-generate) is a different order later; do not touch it.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R32_20261015.md (git hash-object 1c3023a9f163f0a19a7692e75641ead5fe74982c; sha256 fe3144daa06009e25e5b8b418e78b82598e6886bce0d5cf5507a91349ac94015; commit 8c4ecd6fc7) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RESIDENT_R32_CTO_HALF.md (CTO msg 8693, commit 803ea45ca3; you are named as the applier). A different COO blob voids both halves: STOP. The packet is the plan: section 2 (blast radius by branch), 3 (apply protocol), 4 (rollback per key). Both are LOCAL on box/dell2 (push state not read); you work on this box.
    THE BUILD (record: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~197/r32/RESIDENT_R32_BUILD.json; verified by the issuer: `python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_g92_checks.py verify C:/dev/irpt-release-r32 <record>` prints AR-G92-OK members=310 changed=15 added=11 removed=0). Stage folder, this box, outside the repository: file:///C:/dev/irpt-release-r32/ . Tar `irpt-resident-0485393f3a-r32.tar.gz` sha256 3338a5c73c8bf0bb050850507ba9707a079055e803858321c8864ee8bb3a3f1f, 1087615 bytes. Package sums `irpt-resident-0485393f3a-r32.package.SHA256SUMS` sha256 8a473acc405fb41dfba1af5d5bd9f2956aa38208aac43fa79d2f7fd96751afb5. Host script `scripts/resident_host_install_0485393f3a-r32.sh` sha256 5adc8d0b6ae1a6d04b182cda11d5d758b8549084f722b90e5990fc0b59d0d0d6. Run scripts: `scripts/pre_read_r32.sh` (sha256 9f6523cf84a8f3216ab312c2a7072b0fb468d89eec12a48e5cd9788ac4e1ccba), `scripts/install_r32.sh` (39f1326c96610d60d2a2a494ddc54e10d480df104f2df9bb747bd4994d871e53), `scripts/rollback_r32.sh` (a5b74ea1c35b29631f31a780240359a3d5d41891335bc754e3b726efd041c487; run ONLY if the issuer orders it).
    S3 (bucket opal-313476888478-lambda-artifacts, region us-east-1; the install script's own variables): tar key `ec2/investor-reporting-ycharts/resident/irpt-resident-0485393f3a-r32.tar.gz`; sums key `ec2/investor-reporting-ycharts/resident/irpt-resident-0485393f3a-r32.package.SHA256SUMS`; script key `ec2/investor-reporting-ycharts/resident/resident_host_install_0485393f3a-r32.sh`. The host reaches them by GetObject on the key (not GetObjectVersion).
    THE CTO'S CONDITIONS (msg 8693) BIND: (1) exactly the counted members against r31, 15 changed, 11 added, 0 removed, 284 identical; any member outside the packet's table that differs is a STOP before the install. (2) opal_pricing ships OFF; do not enable it. (3) the producer list is exactly ("andrew@opalinvest.com", "fwd1-staff-r41b@opal.invalid"); V1 prints the list line. (4) the commentary family irpt-anlreq-x10-v1 is registered; V1 imports resident_installed.py's registration. (5) the queue reads 0/0 at the before-read, or nothing installs. (6) rollback is the packet's section 4; the r31 root stays on the host; no delete.
  </context>

  <the_act>
    GO: both halves are signed. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~G2 and wait.
    1. Read the COO half and CTO half at HEAD; `git hash-object` of the COO half must print 1c3023a9f163f0a19a7692e75641ead5fe74982c. Verify in the stage folder the sha256 of the tar, the sums file, the host script and the three run scripts against the values in the context. Open the NEVER-2 ledger irpt-resident-r32-20261015 (legs P1 pre-read, D1 upload, D2 install, V1 after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the resident host, the irpt-analysis-resident unit or the ec2/investor-reporting-ycharts/resident keys is a STOP.
    2. P1, the before-read: send scripts/pre_read_r32.sh to the resident host by the channel you used for releases 29 and 31 and both FWD-1 windows (Systems Manager). It must print `P1 STOP-READ-0 PASS` (the running root is /opt/irpt-resident/0485393f3a-r31; otherwise it exits 40: STOP), every changed member at its r31 value, every added member ABSENT, the unit free of IRPT_ANALYSIS_READY_QUEUE_URL, and the queue 0 0. Any other state: STOP and report.
    3. D1, the upload: each of the three keys must read 404 first (a key that exists is a STOP). Upload the tar, the sums file and the host script to their keys from the stage folder; read each back and compare its sha256 to the value above; record each object's S3 VersionId.
    4. D2, the install: send scripts/install_r32.sh by the same channel. It fetches the host script and the sums BY KEY and refuses unless their sha256 equal WANT and WANTSUM (exits 31 and 33), refuses a running root that is not r31 (exit 34), stages the tar, checks the members, keeps the r31 root and the library, installs, polls, and rolls itself back to r31 on a failed start. Capture its full output.
    5. V1, the after-reads (the install prints most of them; read them, then add the census): (a) running root /opt/irpt-resident/0485393f3a-r32, unit active, restarts 0. (b) the install's P2b table: every one of the 25 changed or added members prints MATCH. (c) the package sums: 309 of 309 OK. (d) THE CENSUS (condition 1): on the host, list every file under the r31 root and the r32 root with its sha256 and diff the two lists: exactly 15 members differ and 11 exist only in r32, none only in r31; print the full lists' counts and the differing names. (e) the producer-list line from resident_worker.py, exactly as written. (f) the Opal imports (price_source, portfolio_series, tr_level, the adapters, layout_overview, opal_producer) and resident_installed.py's commentary registration for irpt-anlreq-x10-v1. (g) opal_pricing in reports/resident_bindings.json reads enabled false. (h) the queue 0 0 and no sign-in in the journal. Any failure: the install has rolled back or you run nothing further; report with the output.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r32/A_AFTER_R32R.txt with ONE line each, exactly: `P1 running root r31 queue 0 0`, `D1 three keys uploaded and read back equal`, `V1 running root r32 active`, `V1 members 25 of 25 MATCH`, `V1 sums 309 of 309`, `V1 census 15 changed 11 added 0 removed`, `V1 producer list andrew@opalinvest.com and fwd1-staff-r41b@opal.invalid`, `V1 commentary x10 registered pricing off`; then the three S3 VersionIds, and the install script's rc. A line that did not hold is written `<tag> FAIL <what was read>`.
    7. Close the ledger, and report ONCE to 2.0.0_SA_COO~G2: "leg R closed" with the three VersionIds, the V1 results, the output path and the ledger path. Report every Terraform apply (there is none in this order) to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway you made; do not delete the r31 root, the library copy or the receipt copies.
  </the_act>

  <bounds>
    One host root, three S3 objects, one receipt, one unit ExecStart, one kept library copy. No Terraform, IAM, queue, secret, Lambda, table or route change; no vendor call; no sign-in; no queue message received or purged. Not in this order: the irpt-ycharts-generate Lambda (r33), the portal, enabling opal_pricing, FWD-1 run 3. Rollback: the install's own failure branch, or scripts/rollback_r32.sh only on the issuer's order (the r31 root stays on the host).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r32/IRPT_ANLREQ.TO-APPLY-R32R.resident-r32-aq2.proof_of_spec.json`.
    <criterion id="R32R-AC1" cell_refs="AR-g-97">The record holds the eight lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(P1 running root r31 queue 0 0|D1 three keys uploaded and read back equal|V1 running root r32 active|V1 members 25 of 25 MATCH|V1 sums 309 of 309|V1 census 15 changed 11 added 0 removed|V1 producer list andrew@opalinvest\.com and fwd1-staff-r41b@opal\.invalid|V1 commentary x10 registered pricing off)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r32/A_AFTER_R32R.txt</invocation><expect>^8$</expect></criterion>
    <criterion id="R32R-AC2" cell_refs="AR-g-97">The ledger irpt-resident-r32-20261015 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-r32-20261015_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-g-97 is the issuer's, as for TO-APPLY-R31L.
