<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-DEPLOY-e42.a07-canonical-first-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~S</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R9.md</decomp_doc> (round 9), "Issuer acts this round creates or inherits": the upload of cell `SC-e-42`'s a07 (TO-SC-e42, proof VALID on held branch q/dell1/secclass-r9-held-32/r1).
<owned_cells>SC-e-42</owned_cells>
</decomp_ref>

  <objective>
    Upload `data/assets/scripts/gold/runners_49f/a07_dim_asset_classification.py` at candidate commit `88c7018366` to
    `s3://opal-data-49financial/_code/a07_dim_asset_classification.py` through `.tools/safe-deploy.sh`, so the Advisor Intelligence
    classification dim reads the canonical table first (FWD-5's a07 reader switch). The next chain run then re-buckets 164 keys.
  </objective>

  <context>
    The candidate is on origin as `q/dell1/secclass-r9-held-32/r1` (b0132b22a8), held off CLOUD because a07 is a shipped shared-home file.
    dell1's principal is denied the 49financial bucket (rows W25-S1, W32-S4), so a laptop seat in the cloud-operations lane runs this.
    Full blast radius, readers and rollback: `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_A07_CANONICAL_FIRST_20261007.md`
    and the 164-key list `A07_SWITCH_BEFORE_AFTER_20261007.json` beside it.
  </context>

  <amendment n="1" by="2.0.0_SA_COO~M1" date="2026-10-08T06:5xZ">
    Ledger leg L2's read (the 2026-10-08T12:45Z advi-49f-gold-floor run: the A5-A07-SOURCE-CENSUS line, the d06/d08 mix totals, and
    every class move compared against A07_SWITCH_BEFORE_AFTER_20261007.json) moves to dell1. 2.0.0_SA_COO~M1 takes it, because dell1's
    firm-bucket READ was applied at 05:17:17Z (laptop CTO msg 106788, MSTR msg 816) and the laptop CTO named this seat. dell1 records the
    read in the ledger leg and sends 0.7.0_AE_CloudOps~S the path. ~S keeps two acts. (1) The status flip with its proof instance, after
    the read lands (CTO round-12 addendum 1 item 3). (2) The ROLLBACK, if the read finds a move the JSON does not list, because dell1 is
    still barred from writing a code prefix (limit item 5). No gate limb grades an amendment to an existing order.
  </amendment>

  <the_act>
    BOTH halves are SIGNED for exactly this upload; read both in full first and carry every condition (eight):
    - COO half: in the request above (2.0.0_SA_COO~M1).
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e42_A07_CANONICAL_FIRST_20261007.md (@b3092be6d2).

    1. Make a scratch worktree at `q/dell1/secclass-r9-held-32/r1` (b0132b22a8) and run everything below from its root. Show
       `git show 88c7018366:data/assets/scripts/gold/runners_49f/a07_dim_asset_classification.py | md5sum` and that the worktree file equals it.
    2. TIMING: confirm no 49F/COT chain run is in flight and none is scheduled to start within the act (condition 8). If one is, wait for
       its end; do not upload inside its window.
    3. BEFORE: `aws s3api list-object-versions --bucket opal-data-49financial --prefix _code/a07_dim_asset_classification.py`; record the
       IsLatest VersionId and ETag. No upload on an unread rollback VersionId (condition 5).
    4. Open ONE NEVER-2 ledger entry, slug `secclass-e42-a07-deploy-s-20261007`, naming the laptop as the box, the one key, its before
       VersionId and the rollback (copy that VersionId back over the key, then re-run a07 for the affected date).
    5. ONE run from the scratch worktree root: `.tools/safe-deploy.sh data/assets/scripts/gold/runners_49f/a07_dim_asset_classification.py`.
       Expect the one key deployed, MATCH. Any other key moving is a stop: roll back per the entry.
    6. Prove it (AC1) and leave the entry OPEN on its verify leg: the first scheduled chain run after the upload is read for the dim's
       `A5-A07-SOURCE-CENSUS` line and the d06/d08 mix totals, and its moves are compared against the JSON (conditions 6, 7); any move
       the JSON does not list is a rollback. The issuer (2.0.0_SA_COO~M1) is told the run's id so the verify leg can be read and closed.
  </the_act>

  <bounds>
    - This one key only. No table write, no other script, no IAM, no Terraform. No push of a shared branch: the trunk merge of the held
      branch is 0.0.0_AB_MSTR's, after this deploy, and its push gate then reads MATCH.
    - `safe-deploy.sh` only; never a bare `aws s3 cp`. No package install or download of any kind.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~S/logs/
  </paths>

<preflight>
comp-schedule: RUN -- R8 battery (comp-schedule --owner 2.0.0_SA_COO~M --budget 120: 6 of 6 carriers); the 49F/COT chain schedules are the act's timing input (step 2); BLIND: an off-repo trigger of the chain, which step 2 reads live.
comp-iam: RUN at the cut by TO-SC-e42's worker (bd-exporter-ec2-role's bd-securities-access already allows Scan on etf-classifications); the deploying seat's own write to _code/ is its standing lane.
comp-adversary: RUN -- an unsigned body riding along (one file, md5 shown against the candidate before the act); an upload inside a chain run (step 2 refuses it); no way back (before VersionId read and named first; versioning on); an unlisted class move (the post-run comparison is a rollback trigger); BLIND: the served mix bytes on the day of the run, read by this seat because dell1 cannot.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the deploy writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-42"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R11_CHECKS/e42_a07_etag_check.py</invocation><expect>E42-A07 ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 cannot run from dell1 (the bucket denies its principal); at the cut the live a07 is the pre-switch body, so AC1 reads ok=False there.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 (by its commit and the bus) when the upload is proven: step 1's md5, step 2's timing read, the before
    VersionId and ETag, the safe-deploy output lines, AC1's output, the ledger path (verify leg open), commit hashes and the measured push
    state. The issuer reads the post-run leg and flips the status.
  </report>
</task_order>
