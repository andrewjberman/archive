<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-DEPLOY-e21.shared-module-explicit-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~S</issued_to>
    <date>2026-10-07</date>
    <status>superseded</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R8.md</decomp_doc> (round 8), "Issuer acts this round creates or inherits": the deploy of cell `SC-e-21`'s six-class module (TO-SC-e21, proof VALID), which the trunk push did not carry (row MDPF_SECCLASS-S50).
<owned_cells>SC-e-21</owned_cells>
</decomp_ref>

  <objective>
    Upload `infra/aws/lambda/v2_portal/_shared/etf_classification.py` at the trunk's bytes (md5 3a033c04678f1c96d116b641545b17bb) to
    `code/gold/lib/_shared/etf_classification.py` in `opal-data-bd` and `opal-data-cot`, through `.tools/safe-deploy.sh`, so that S3
    equals the trunk. The laptop's hold on CLOUD pushes that deploy a bd or cot gold script lifts on the issuer's read-back after this.
  </objective>

  <context>
    The module merged to origin CLOUD at a96edec2d7 (q/dell1/secclass-e21/r1); the pre-push gate printed "no deploy-scope script files
    detected, nothing to do", because `safe_deploy_core.shipped_artifacts_for()` returns the `lib/_shared` members only beside a gold
    script of the tree (probed: the module alone returns []). Measured by the issuer ~10:1xZ: both keys ETag 05c924d53ed51a09911198a6a384a74f.
    Full order with the carrier rationale: `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/DEPLOY_ORDER_SECCLASS_E21_SHARED_MODULE_20261007.md`.
    You run it because the firm buckets deny dell1's principal (row W25-S1); 1.0.0_SA_CTO~DELL1 msg 144 and laptop 1.0.0_SA_CTO msg 106143.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED for exactly this upload; read both in full first and carry every condition:
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_SEED_SIX_CLASS_20261007.md (@59cfbf169b)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e21_SEED_SIX_CLASS_20261007.md (@b39e54dc9e; msg 140: it covers this explicit upload)
    NO seed run. Nothing else is written.

    1. On the laptop's CLOUD at or after a96edec2d7, show `git show HEAD:infra/aws/lambda/v2_portal/_shared/etf_classification.py | md5sum`
       reads 3a033c04678f1c96d116b641545b17bb. Any other value is a STOP with a report.
    2. BEFORE: for each of these six keys print ETag and VersionId, and compare to the repo's md5 at HEAD:
       - the two MOVING keys: `code/gold/lib/_shared/etf_classification.py` in opal-data-bd and opal-data-cot -- expect ETag 05c924d5...,
         VersionIds 9abtPgnVDEDVovysMOqLo_cIw3fSZ6hQ (bd) and HCv30DsdLF9wgJGrAu4H78zeGKGcgNd6 (cot): the rollback versions;
       - the two CARRIERS, which must be byte-equal (ETag = repo md5) so they do not move: opal-data-bd `code/gold/E_18.detect_new_securities.py`
         (a7820a20...) and opal-data-cot `code/gold/A_00.accounts_dimension.py` (cb10e3cd...);
       - the two unchanged members in both buckets: `code/gold/lib/_shared/etf_classifications_dynamodb.py` and
         `code/gold/lib/_shared/etf_classification_scheduled.py` (ETag = repo md5).
       Any carrier or unchanged member that DIFFERS is a STOP: the deploy would move an unsigned body. Report it.
    3. Open ONE NEVER-2 ledger entry, slug `secclass-e21-shared-module-deploy-s-20261007`, naming the laptop as the box, the two moving
       keys with their before VersionIds, and the rollback per key (copy that VersionId back over the key).
    4. ONE run: `.tools/safe-deploy.sh data/black_diamond/scripts/gold/E_18.detect_new_securities.py data/cot/scripts/gold/A_00.accounts_dimension.py`.
       Expect `DEPLOYED-SHIPPED` for the shipped members and MATCH for the carriers. If it errors part-way, finish or roll back in-session
       per the entry, and say which.
    5. Prove it (the criteria below) and close the entry.
  </the_act>

  <bounds>
    - These two moving keys only. No seed run, no table write, no other script deployed, no other bucket. No push of a shared branch.
    - `safe-deploy.sh` only; never a bare `aws s3 cp` of the module.
    - A STOP in step 1 or 2 deploys nothing and is reported.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~S/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one deploy by a seat.
comp-iam: DECLARED-NOT-APPLICABLE no grant changes; the seat's own principal writes two code keys it already deploys to.
comp-adversary: RUN -- an unsigned body riding along (the carriers and unchanged members are read byte-equal before the act, a DIFF is a stop); a half-landed deploy (one bucket of two: finish or roll back per the entry); no way back (both before VersionIds named; versioning is on); the E_18 vocabulary change (the halves read E_18's reader rule: the admitted set becomes six classes; the table holds 0 multi_asset rows); BLIND: an in-flight gold run keeps the body it loaded.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the deploy writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-21"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R10_CHECKS/e21_shipped_etag_check.py</invocation><expect>E21-SHIPPED ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (`ok=False trunk=3a033c04... bd=05c924d5... cot=05c924d5... control=MATCH`).

  <report>
    Report ONCE to 2.0.0_SA_COO~M1 when the entry closes (or at a STOP): step 1's md5; the six before reads; the safe-deploy output lines;
    AC1's output; the ledger entry path and its close; the proof-of-spec instance path (genre DEPLOY); commit hashes and the measured push
    state. The issuer runs its own read-back and flips the status.
  </report>
</task_order>

### AMENDMENT -- CLOSED SUPERSEDED (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~12:3xZ; answers laptop ~S via laptop CTO msg 106920 / MSTR msg 886)

This order's act was never taken as this order. Its outcome was delivered by the TO-DEPLOY-e65 deploy:
code/gold/lib/_shared/etf_classification.py reads ETag 3a033c04678f1c96d116b641545b17bb, 73,461 bytes, in both opal-data-bd and
opal-data-cot, equal to trunk (~S's measurement). So this order closes SUPERSEDED by TO-DEPLOY-e65, not complete, and no proof
instance is owed. No gate limb grades the status change of an existing order to a terminal word.
