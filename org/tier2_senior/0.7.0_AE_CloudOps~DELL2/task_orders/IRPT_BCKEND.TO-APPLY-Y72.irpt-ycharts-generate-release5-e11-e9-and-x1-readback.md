<task_order>
  <metadata>
    <id>IRPT_BCKEND.TO-APPLY-Y72.irpt-ycharts-generate-release5-e11-e9-and-x1-readback</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>IRPT_BCKEND</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<proof_of_spec>
Criterion ids: Y72-1-AC1, Y72-1-AC2, Y72-1-AC3. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y72/IRPT_BCKEND.TO-APPLY-Y72.proof_of_spec.json`, validated with `python .tools/proof-of-spec-check.py <instance> Y72-1-AC1,Y72-1-AC2,Y72-1-AC3`; AC2 is marked FAIL with reason PENDING-ISSUER until the laptop result lands. Shape: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~159/IRPT_BCKEND.TO-IB-yr-681.release3-a1-run-as-signed.proof_of_spec.json`.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP_R72_Y.md</decomp_doc> round 72, workstream ~Y, cell `APPLY-Y72`.
<owned_cells>APPLY-Y72</owned_cells>
</decomp_ref>

  <objective>
    Release 5 of `irpt-ycharts-generate` on dell2: E11 plus the E9 report modules (three changed members: `custody_submission.py`,
    `composition.py`, `repository.py`), built `4HEH1aDNa39+vwLFK24SldMOBit/hiBKF4aQjlsU1zk=`. It supersedes release 4, which rolled back on
    the E11 import gap (row IRPT_BCKEND-D2-S16). Live and rollback is `Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY=`.
    Then ONE template-lane on-behalf upload, whose read-back BEFORE any delete proves X-1's actor (CTO msg 1877).
  </objective>

  <context>
    Read the pair first: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release4_ycg/NEVER_WIDEN_PAIR_RELEASE5_E11.md`
    (blob 553de57d42). Then the CTO half, `.../deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_YCG_RELEASE5_E11_CTO_HALF.md` @79aa67ae5d. Its
    conditions bind: re-run the symbol closure against the UPLOADED zip before the apply; after-read 2 (import census) gates
    everything else; X-1 is graded on all three read-back booleans, taken before any
    delete; the S3 deletes are Andrew's act.

    Release 3's order is the model for every step shape below:
    `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-yr-681.release3-a1-run-as-signed.md`. That covers the ledger,
    upload, targeted plan from the shared tree's initialized `infra/aws/terraform/investor-reporting/ycharts` root, safe-apply, the
    test filer item, direct-invoke event shape and keys file. Its deliverables are in
    `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~159/`.
  </context>

  <steps>
    0. Pre-checks. STOP on any miss:
       - `git fetch origin` and `git merge-base --is-ancestor 2f3ee8c15b origin/box/dell2` rc 0;
       - `release-census.py irpt-ycharts-generate --pin HEAD` shows `changed_members=3` (`composition.py`, `custody_submission.py`, `repository.py`);
       - live CodeSha256 is `Un0wVZqj...`;
       - record the current S3 object version as the rollback source.
    1. Ledger `irpt-ycg-release5-20261009` (L1 verify / L2 s3-prefix / L3 activation / L4 verify). Open and commit it before any write.
    2. Upload: `build-and-upload.sh investor-reporting irpt-ycharts-generate`. The SHA256 must be `4HEH1aDN...`, or STOP. Then run
       `python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r71/symbol_closure.py <the uploaded zip>`
       (the BUILD_ONLY/upload artifact at /tmp/lambda-artifact-irpt-ycharts-generate.zip). It must print `missing=0` and `symbol_closure PASS`,
       or STOP before the apply (CTO condition).
    3. Targeted plan, 0/1/0, `s3_object_version` + `source_code_hash` only. Commit the plan text, then `safe-apply`.
    4. After-read 1: live == `4HEH1aDN...`, re-plan 0. After-read 2: import census `failed: {}` -- it GATES everything after it (CTO condition): on any failure, go
       straight to branch B.
    5. After-read 3 (E11 offline):
       - `python -m pytest -q -p no:cacheprovider infra/aws/lambda/investor-reporting/ycharts/generate/tests/test_custody_submission_revision.py`
         reads 3 passed;
       - the three custody suites read 66 passed, 2 skipped.
    6. After-read 4 (X-1 actor), as release 3's read 4:
       - put the test filer (synthetic `@opal.invalid`, OPAL_GLOBAL home opal-capital, `allowedFirmIds` = [F], no login identity);
       - make ONE direct-invoke template-lane upload with `advisor_email` = a verified advisor A of F;
       - re-POST the same token until NORMALIZED or NEEDS_CORRECTION (15 minutes max);
       - write `Y72-1_admit_keys.json`: `admit_keys`, `admit_tenant`, `upload_id`, `body_sha256` and the opaque `adv-` id of A. Its
         note asks the laptop to READ BACK FIRST and return `admit_readback` = {body_sha256_match, owner_is_advisor,
         acting_principal_is_filer} (all three, CTO condition), THEN delete, then return `results`.
    7. After-read 5: an unlisted-firm advisor is refused; a firm not on the list is refused; neither stores anything.
    8. Delete the test row on dell2; a consistent get-item reads NOT FOUND. Commit the keys file. The issuer relays it to the laptop.
    9. Branch B (any of 0-2, 4-7 fails): roll back to `Un0wVZqj...` the same session (re-promote the step-0 version, targeted apply),
       then step 8, then a BLOCKING row.
    10. Write `Y72-1_release5_after_reads.json` with the keys of release 3's after-reads file. Read 4's value is
        `"STORED-NEXT-STATE"`; set `admit_final_state`. Close the ledger and commit. Report.
  </steps>

  <acceptance>
    <criterion id="Y72-1-AC1"><invocation>python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r72/y72_cells.py . Y72-1-AC1</invocation><expect>Y72-1-AC1 PASS</expect></criterion>
    <criterion id="Y72-1-AC2"><invocation>python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r72/y72_cells.py . Y72-1-AC2</invocation><expect>Y72-1-AC2 PASS</expect></criterion>
    <criterion id="Y72-1-AC3"><invocation>python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r72/y72_cells.py . Y72-1-AC3</invocation><expect>Y72-1-AC3 PASS</expect></criterion>
    AC2 is graded by the issuer on the laptop's read-back + cleanup result. Leave the status for the issuer.
  </acceptance>

  <bounds>
    Write deliverables to `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y72/`. Use opaque ids only for real people.

    Live writes are exactly:
    - the artifact upload and the one targeted apply (in branch B, also the rollback);
    - ONE test row put + delete;
    - the one upload's records;
    - its one `resolve_upload` message and the resident's YCharts `securities_info` resolution for it (Andrew-direct ~21:1xZ).

    No IAM change, no other function, no other vendor call, no SendCommand.

    NEVER-2: ledger first, closed after. Never `update-function-code`. Edit byte-preserving; ASCII only.
  </bounds>

  <preflight>
comp-blast: RUN -- release-census at 2f3ee8c15b: 3 changed of 100 (composition, custody_submission, repository), one function; riders f60e6f1d2a (~G2, msg 2012) and b13bab7495 (~P2, msg 2011) confirmed; both halves sign this set.
comp-iam: DECLARED-NOT-APPLICABLE -- no permission is added or changed; the opal-partner GetItem grant is already live.
comp-routes: DECLARED-NOT-APPLICABLE -- no route or authorizer change; reads go by direct IAM invoke.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule is touched.
comp-adversary: RUN -- the symbol closure FAILed on release 4's exact defect before the repin and PASSes at 2f3ee8c15b; Y72-1-AC1/AC2/AC3 dry-run at base: FAIL (no file); AC2 refuses without all three read-back booleans true.
  </preflight>

  <report_to>2.0.0_SA_COO~Y2: commit hashes, built and live CodeSha256, the S3 versionIds, the apply line, the opaque F and A, `upload_id`, `admit_final_state`, the `admit_keys` count, row ids.</report_to>
</task_order>
