<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-DEPLOY-e65.cash-token-shared-module-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~S</issued_to>
    <date>2026-10-07</date>
    <status>complete -- 2026-10-07 ~17:0xZ by the assignee `0.7.0_AE_CloudOps~S` (CTO msg 301: the assignee flips). AC1 PASS: `E65-SHIPPED ok=True head=3f1e6be8910952f33c88bf100c610ab6 bd=3f1e6be8910952f33c88bf100c610ab6 cot=3f1e6be8910952f33c88bf100c610ab6 control=MATCH`. Step 1 read 3f1e6be8910952f33c88bf100c610ab6 at three independent places (the scratch worktree's file on disk, origin/CLOUD, and the shared laptop CLOUD HEAD after the level-set). Step 2: 8 of 8 keys read BEFORE the act, ZERO STOPs; both rollback VersionIds read first and still retrievable after. ONE safe-deploy run moved exactly the two keys by content; the six byte-identical re-uploads all returned their pre-act ETags (0 of 8 off expectation). Proof instance: `org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/MDPF_SECCLASS.TO-DEPLOY-e65.cash-token-shared-module-deploy-laptop.proof_of_spec.json`. Ledger `secclass-e65-cash-token-deploy-s-20261007` opened before the act @e0b3189735; L1/L2/L3 CLOSED on proof. ⛔ **THE ENTRY IS NOT CLOSED -- it is HELD-SOVEREIGN-GATED on leg L4**, the 23:00Z BD E_18 read (CTO half af8fa774f3 condition 3), against a named external gate with a re-read event; `deploy_ledger list` prints "apply legs proven, only verify open; tracked-not-stranded". The CTO's sequencing rule gates TO-DEPLOY-e57e61 on this entry being CLOSED, and HELD is not CLOSED: that call is the CTO's and the issuer's, not this seat's. ⚠ The act ran from a scratch worktree detached at origin/CLOUD `efc2e63467` because the shared laptop CLOUD was then 459 commits behind and did not carry the merge; the level-set landed afterwards and the shared HEAD now reads the same md5, so the deviation is moot in hindsight but is recorded rather than dropped.</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R11.md</decomp_doc> (round 11), "Issuer acts": the release of cell `SC-e-65` (TO-SC-e65, proof VALID @858c1d3b5d), which the CLOUD merge alone does not upload (CTO half, msg 362).
<owned_cells>SC-e-65</owned_cells>
</decomp_ref>

  <objective>
    Upload `infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py` at the merged bytes (md5 3f1e6be8910952f33c88bf100c610ab6,
    commit 16092a4806) to `code/gold/lib/_shared/etf_classification_scheduled.py` in `opal-data-bd` and `opal-data-cot`, through
    `.tools/safe-deploy.sh`, in the same window as `0.0.0_AB_MSTR`'s merge of `q/dell1/secclass-r11-held-e65`. No BD or COT gold push
    lands between the merge and this read-back.
  </objective>

  <context>
    `safe_deploy_core.py` ~:1042 ships the `lib/_shared` members only beside a gold script of the tree. The merge alone prints "nothing to
    do", as TO-DEPLOY-e21 showed. So this order carries the module on two byte-equal carriers, exactly as TO-DEPLOY-e21 did.
    Measured by the issuer 2026-10-07T15:2xZ (head-object ETag vs `git show CLOUD:` md5): both carriers and all four unchanged members
    MATCH, and both moving keys read cfe898d1b8677c0765a7f5ee8026761c, the pre-merge bytes.
  </context>

  <the_act>
    BOTH halves are SIGNED for this upload; read both in full first and carry every condition:
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_CASH_TOKEN_20261007.md (@00e7bf2cb5)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e65_CASH_TOKEN_20261007.md (msg 362: merge + explicit
      safe-deploy in one window, read back 3f1e6be8, no BD/COT gold push until that read, then the 23:00Z E_18 cash_token read)

    1. On the laptop's CLOUD AFTER the merge of q/dell1/secclass-r11-held-e65, show that
       `git show HEAD:infra/aws/lambda/v2_portal/_shared/etf_classification_scheduled.py | md5sum` reads 3f1e6be8910952f33c88bf100c610ab6.
       Any other value is a STOP.
    2. BEFORE: print ETag and VersionId for:
       - the two MOVING keys: `code/gold/lib/_shared/etf_classification_scheduled.py` in opal-data-bd (VersionId
         P9g4.GzldooFjJgeyMTfk2YlTzT5sQUg) and opal-data-cot (893RBl4.9fYgJGC7j0qjLTXzVkCQaPX1). Both expect ETag cfe898d1..., and these are
         the rollback versions;
       - the two CARRIERS, which must equal the repo md5 at HEAD: opal-data-bd `code/gold/E_18.detect_new_securities.py` (a7820a20...) and
         opal-data-cot `code/gold/A_00.accounts_dimension.py` (cb10e3cd...);
       - the unchanged members in both buckets: `code/gold/lib/_shared/etf_classification.py` (3a033c04...) and
         `code/gold/lib/_shared/etf_classifications_dynamodb.py` (4cc11d3e...).
       Any carrier or unchanged member that DIFFERS is a STOP.
    3. Open ONE NEVER-2 ledger entry, slug `secclass-e65-cash-token-deploy-s-20261007`. It names the laptop, the two moving keys with their
       before VersionIds, and the rollback per key (copy that VersionId back).
    4. ONE run: `.tools/safe-deploy.sh data/black_diamond/scripts/gold/E_18.detect_new_securities.py data/cot/scripts/gold/A_00.accounts_dimension.py`.
       Expect DEPLOYED-SHIPPED for the members and MATCH for the carriers. If it errors part-way, finish or roll back in-session.
    5. Prove it (AC1) and close the entry.
  </the_act>

  <bounds>
    - These two moving keys only. No table write, no other script, no other bucket, no push of a shared branch.
    - `safe-deploy.sh` only; never a bare `aws s3 cp`. No package install or download of any kind.
    - A STOP in step 1 or 2 deploys nothing and is reported.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~S/logs/
  </paths>

<preflight>
comp-schedule: RUN -- the BD 23:00Z E_18 run is the first reader; the deploy lands before it, and no BD/COT gold push lands between the merge and the read-back.
comp-iam: DECLARED-NOT-APPLICABLE no grant changes; the seat's principal writes two code keys it already deploys to (TO-DEPLOY-e21).
comp-adversary: RUN -- an unsigned body riding along (carriers and unchanged members read byte-equal first; a DIFF is a stop); a half-landed deploy (one bucket of two: finish or roll back); no way back (both before VersionIds named; versioning on); BLIND: an in-flight gold run keeps the body it loaded.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the deploy writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-65"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e65_shipped_etag_check.py</invocation><expect>E65-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (head is the CLOUD base, not the candidate; both keys read cfe898d1...; control MATCH).

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes (or at a STOP): step 1's md5; the before reads; the safe-deploy output lines;
    AC1's output; the ledger entry path and its close; the proof-of-spec instance at
    org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/MDPF_SECCLASS.TO-DEPLOY-e65.cash-token-shared-module-deploy-laptop.proof_of_spec.json;
    and, in the same commit, this order's status flipped to complete (CTO msg 301: the assignee flips). Name the commit hashes and the
    measured push state.
  </report>
</task_order>
