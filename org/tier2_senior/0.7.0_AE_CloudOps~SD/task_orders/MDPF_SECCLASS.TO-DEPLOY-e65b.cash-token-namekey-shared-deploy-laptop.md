<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-DEPLOY-e65b.cash-token-namekey-shared-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SD</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R11.md</decomp_doc> (round 11), "Issuer acts": the release of cell `SC-e-65` amendment 3 (row S63; build 1fae201565, proof VALID d34adb6c2c). The CLOUD merge alone does not upload it.
<owned_cells>SC-e-65</owned_cells>
</decomp_ref>

  <objective>
    Upload `infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py` at the merged bytes of `q/dell1/secclass-r12-rel-e65b`
    (md5 40ffa3fac380551704637adc8a3b6ff3) to `code/gold/lib/_shared/etf_classification_scheduled.py` in `opal-data-bd` and
    `opal-data-cot`. The cash-token ticker leg then skips NAME:: keys.
  </objective>

  <context>
    BOTH halves are SIGNED. Read both in full first and carry every condition:
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_CASH_TOKEN_NAMEKEY_20261007.md (@86843a40fd).
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e65_AM3_NAMEKEY_DEPLOY_20261007.md (@7f68da7051).
    Its terms: the deploy runs only after the e65 ledger closes on its 23:00Z read, and outside any gold run. It uses the invocation the
    e65 ledger recorded, through the gold carriers; the literal _shared path deploys nothing (msg 499). A key left at 3f1e6be8 is a
    failed act.
  </context>

  <the_act>
    1. GATE: the ledger `secclass-e65-cash-token-deploy-s-20261007` reads CLOSED. No BD or COT gold run is in progress (bd-gold-trigger,
       and the cot gold schedule). Either unmet is a WAIT, never a skip.
    2. On CLOUD (a dell1 checkout of origin/CLOUD) after the merge, `git show HEAD:infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py | md5sum`
       reads 40ffa3fac380551704637adc8a3b6ff3. Any other value is a STOP.
    3. BEFORE: print ETag and VersionId for:
       - the two MOVING keys (expect ETag 3f1e6be8...; VersionIds bd `0aE1FGTSH.2rsPdoj.3mtrBuHmmByxAu`, cot
         `0e4OsubYyRdw4RnmCvfMYM0SZtLLM9z9`). These are the rollback versions; re-read them, never assume them.
       - the two CARRIERS (opal-data-bd `code/gold/E_18.detect_new_securities.py`, opal-data-cot `code/gold/A_00.accounts_dimension.py`)
         and the unchanged members (`etf_classification.py`, `etf_classifications_dynamodb.py` in both buckets). Each must equal the repo
         md5 at HEAD. Any that DIFFERS is a STOP.
    4. Open ONE NEVER-2 ledger entry, slug `secclass-e65b-namekey-deploy-s-20261007`, naming both moving keys with their before VersionIds
       and the rollback per key (copy that VersionId back).
    5. ONE run: `.tools/safe-deploy.sh data/black_diamond/scripts/gold/E_18.detect_new_securities.py data/cot/scripts/gold/A_00.accounts_dimension.py`.
       Expect DEPLOYED-SHIPPED for the moving member and MATCH for every other key. If it errors part-way, finish or roll back in-session.
    6. Prove it (AC1). Leave the entry OPEN on the next BD E_18 run's cash_token plan lines: no NAME:: key that is not a whole cash phrase
       is planned cash/Cash. Then close it, and flip this order complete with the proof instance in your deliverables.
  </the_act>

  <bounds>
    - These two moving keys only. No table write, no other script, no other bucket, no push of a shared branch.
    - `safe-deploy.sh` only; never a bare `aws s3 cp`. No package install or download of any kind.
    - A STOP in step 2 or 3 deploys nothing and is reported.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SD/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SD/logs/
  </paths>

<preflight>
comp-schedule: RUN -- after the e65 close on the 23:00Z E_18 run, outside any gold run; the next E_18 run is the verify reader.
comp-iam: DECLARED-NOT-APPLICABLE no grant changes; the seat deploys to these two code keys already (TO-DEPLOY-e65).
comp-adversary: RUN -- an unsigned body riding along (carriers and members byte-equal first); a half-landed deploy (one bucket of two: finish or roll back); no way back (both VersionIds named, re-read); the wrong invocation (the literal _shared path deploys nothing; AC1 reads 3f1e6be8 as FAIL).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the deploy writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-65"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e65_shipped_etag_check.py</invocation><expect>E65-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (head=40ffa3fa, bd and cot both read 3f1e6be8; control MATCH).

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes, or at a STOP, with:
    - step 2's md5 and the before reads;
    - the safe-deploy output lines and AC1's output;
    - the E_18 cash_token lines;
    - the ledger entry path and its close, and the proof instance;
    - the commit hashes with their measured push state.
  </report>
</task_order>
<!-- RE-ADDRESSED (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~00:3xZ): executor ~S (laptop) -> 0.7.0_AE_CloudOps~SD (dell1),
per 1.0.0_SA_CTO~DELL1 amend 914acafe20 (Andrew-direct ~00:0xZ: the Dells run the heavy jobs). Windows, ledger slug, reads, key list and
rollback are unchanged. Any AccessDenied the seat meets is reported the same hour as action and resource, and is never worked around. -->
