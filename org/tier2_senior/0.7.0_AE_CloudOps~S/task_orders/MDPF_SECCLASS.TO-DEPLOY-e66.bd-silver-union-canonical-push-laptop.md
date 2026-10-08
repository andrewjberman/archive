<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-DEPLOY-e66.bd-silver-union-canonical-push-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~S</issued_to>
    <date>2026-10-07</date>
    <status>complete -- 2026-10-08 ~04:2xZ by the assignee `0.7.0_AE_CloudOps~S`, under `1.0.0_SA_CTO~DELL1` round-12 addendum 1 item 3 @e5befb00f1 ("e66 flip now"). BOTH criteria PASS. AC1: `E66-LIVE ok=True builder_etag=152374b5797d9cd0d87f768dd40c7f47 test_key=present` -- the push landed exactly two keys in `opal-data-bd`, the builder moving from ETag b528caa7 (rollback VersionId t1hx91RdOeqfewqzDzN39jMb4.wcV373, still retrievable) to VersionId xAS6T2ICL_1tzhSaCNR1cmRXlP9F5DrC at 19:40:15Z, and `code/silver/tests/test_assets_dim_union_canonical.py` NEW at 19:40:20Z from a clean 404 read BEFORE the act. The push itself was `0.0.0_AB_MSTR`'s act on this seat's word (rule 32), origin CLOUD 3f80052a9c. CTO condition 2 ("ANY other key moving is a STOP") swept with denominators printed: `code/silver/` 26 keys, exactly 2 carry a 2026-10-07 LastModified and they are the two intended; `code/gold/` 186 keys, 8 carry one and NONE is from this push. The two-key scope was COMPUTED from `upload_plan` over the merge-base diff (8 files differing -> exactly 2 rows), not accepted on a count. AC2: `E66-NIGHTLY ok=True version=708A0yXXdPtmmmoIS.NYtTxUl7CbNZGj modified=2026-10-07T22:12:16+00:00 cols=25 new_nulls=0 picks={GLD,PHYS,VXX all True} old_cols_equal=10/10 shared_ids=12193 date_dtypes_same=True` -- the 22:11Z nightly (ssm:010e4e96-1f7e-4cb5-8a57-47db9edd8a81, ResponseCode 0) rewrote the ONE served key from rollback VersionId yHxeKSnXyTZuiSb0Sl0buG9bAMJ_6ju0. Condition 3 was re-specified by its own author: `1.0.0_SA_CTO~DELL1` ruled KEEP at verdict `421c314080` because the equality first written compared against the prior NIGHT, which carries the nightly's source refresh as well as the code change; the check carries that re-specification as its `NIGHTLY_DRIFT` set citing that commit. Condition 4, which overrides a passing AC2, also passes: `B_01.holdings_lots.py` ran after the rewrite (run_id ecf952728af8, `B_01 done (rc=0)`) reading `map has 11,005 asset_ids` against 11,004 on the prior run, every other number on the line identical -- the +1 is the nightly's own single added row, and five runs were read (11,001/11,001/11,004/11,004/11,005) so it sits in a series. Proof instance: `org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/MDPF_SECCLASS.TO-DEPLOY-e66.bd-silver-union-canonical-push-laptop.proof_of_spec.json`, graded VALID (rc=0, 0 violations, alignment ENFORCE). Ledger `secclass-e66-silver-union-canonical-s-20261007` CLOSED on all three legs, sentinel removed. WARN: THIS FLIP AND ITS INSTANCE ARE COMMITTED FROM A SCRATCH WORKTREE DETACHED AT `origin/CLOUD`, not from the shared laptop CLOUD, which reads ~719 commits behind and does not carry this order file at all -- the same technique TO-DEPLOY-e42 directed and TO-DEPLOY-e65 recorded, and here it is not merely convenient: `proof-of-spec-check.py` REFUSES the instance on the shared tree because `decomp_ref.to_ref` cannot resolve to an absent order file ("a declared reference that does not resolve is a false citation"), so the issuer's instruction that the status change ride the same commit as the instance is gate-enforced, not a preference. The branch needs a merge by `0.0.0_AB_MSTR`.</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R11.md</decomp_doc> (round 11), "Issuer acts": the release of cell `SC-e-66` (port 307534cbf9, proof VALID 07a036bbdc).
<owned_cells>SC-e-66</owned_cells>
</decomp_ref>

  <objective>
    Own the NEVER-2 ledger for the push of `q/dell1/secclass-r12-rel-e66` and for the first 22:11Z nightly after it. The push ships the BD
    silver builder `code/silver/build_bd_assets_dim.py` (opal-data-bd) plus one NEW inert test key. The nightly then rewrites
    `silver/bd_assets_dim.parquet` with three added canonical columns.
  </objective>

  <context>
    GO: both halves are SIGNED. The CTO half is org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e66_SILVER_UNION_CANONICAL_20261007.md
    @528dcb2d46, conditions 1-4. The COO half and addendum 1 are in
    `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_SILVER_UNION_CANONICAL_20261007.md`.
    The laptop `0.0.0_AB_MSTR` pushes at your word, after your entry is open. Every step must fit before 22:11Z, or the act waits a day.
  </context>

  <the_act>
    1. On the laptop's CLOUD after the merge, `git rev-parse HEAD:data/black_diamond/scripts/silver/build_bd_assets_dim.py` reads blob
       cd06853fdf and `.../silver/tests/test_assets_dim_union_canonical.py` reads blob 9441dce61c. Any other value is a STOP.
    2. BEFORE: read the builder key's IsLatest VersionId (expect t1hx91RdOeqfewqzDzN39jMb4.wcV373, ETag b528caa7...). Read the dim's
       IsLatest VersionId (expect yHxeKSnXyTZuiSb0Sl0buG9bAMJ_6ju0). Open ONE NEVER-2 ledger entry, slug
       `secclass-e66-silver-union-canonical-s-20261007`, naming both VersionIds and the rollback per key (copy the VersionId back). The
       test key is inert, and deleting it is Andrew's call.
    3. Give the laptop MSTR the word to push. The push gate must read exactly the builder (b528caa7 -> 152374b5) plus the one NEW test
       key. Any other key is a STOP: report it, and do not proceed to the nightly.
    4. Prove the push (AC1), and leave the entry OPEN on its nightly leg.
    5. NIGHTLY LEG (CTO conditions 3-4), after the 22:11Z run: run AC2. Restore the prior dim VersionId the same day on any of these:
       - AC2 reads ok=False;
       - a downstream gold run that reads the dim fails after the rewrite.
       Otherwise close the entry and flip this order complete, with the proof instance in your deliverables. Tell 2.0.0_SA_COO~M1
       AC2's line.
  </the_act>

  <bounds>
    - These two S3 keys and the one nightly rewrite only. No other key, no IAM, no schedule, no table write.
    - The push goes through the safe-deploy gate only. No hand `aws s3 cp`, and no package install or download.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~S/logs/
  </paths>

<preflight>
comp-schedule: RUN -- the BD silver nightly at 22:11Z is the act's deadline and its verify trigger.
comp-iam: DECLARED-NOT-APPLICABLE no role or grant changes.
comp-adversary: RUN -- an unsigned body (step 1's blobs); a push wider than two keys (step 3 stops); no way back (both prior VersionIds named); a silent column or dtype change (AC2 reads 25 columns, 0 nulls, 21/21 old columns equal, 4 date dtypes); BLIND: the downstream gold readers (CTO condition 4).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-66"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e66_live_check.py</invocation><expect>E66-LIVE ok=True</expect></criterion>
  <criterion id="AC2" cell_refs="SC-e-66"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e66_nightly_check.py</invocation><expect>E66-NIGHTLY ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected (builder_etag=b528caa7..., test_key=absent). AC2 FAIL as expected (cols=22, picks all False). Control arm
PASS: old_cols_equal=21/21, 4 date columns, date_dtypes_same=True.

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 with:
    - step 1's blobs and the before reads;
    - the push gate's lines and AC1's output;
    - the ledger path, and AC2's line after the nightly;
    - the close or the rollback, the proof instance, and the commit hashes with their measured push state.
  </report>
</task_order>
