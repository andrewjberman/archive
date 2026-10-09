<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-Y1.irpt-status-release1-dell2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<proof_of_spec>
Criterion ids: APPLY1-AC1, APPLY1-AC2, APPLY1-AC3. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r1/IRPT_ANLREQ.TO-APPLY-Y1.proof_of_spec.json`, `to_id` the FULL id, validated with `python .tools/proof-of-spec-check.py <instance> APPLY1-AC1,APPLY1-AC2,APPLY1-AC3`. Shape: `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y75/IRPT_BCKEND.TO-APPLY-Y75.proof_of_spec.json`.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R2.md</decomp_doc> round 2, workstream ~Y, release 1 of cell `AR-y-21` (and `AR-y-22`, AMENDMENT 2).
<owned_cells>AR-y-21</owned_cells>
</decomp_ref>

  <objective>
    IRPT_ANLREQ release 1 on dell2. `irpt-status` code built `WTGCJPiSEWSack1XvAMRyTGSVLX84VSm+3eC3eSPgsQ=` at pin `3a6d021e4a` (on origin), plus ONE API route:
    `GET /api/scoped/investor-reporting/analysis/requests/{requestId}/original`. It ships:
    - the ticket binding's read side (AR-y-11);
    - the original-file reader (AR-y-22).
    Live and rollback is `E7VKvhg3E9D5euWO+S649/iyAJ05xUmFPqHEAKDTFxA=` (IB-pr-395).
  </objective>

  <context>
    Read the pair first: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_IRPT_STATUS.md`
    (blob ae6a278722; the COO half is signed by this issuance). Then the CTO half,
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RELEASE1_IRPT_STATUS_CTO_HALF.md` (msg 2940), GIVEN. Its conditions bind:
    - the after-reads run in order;
    - read 3 runs all three arms, and the signed link is NEVER logged or written to a file (record its sha256 and expiry only);
    - read 6's S3 deletes wait on Andrew's word;
    - the ledger is pinned (pin, built, rollback version);
    - the route census reads exactly ONE.
    Step shapes (ledger, upload, targeted plan, safe-apply, direct invoke) follow `TO-APPLY-Y75`. Build, plan and apply in a detached worktree at the
    pin (`git worktree add --detach /c/dev/anl-r1-pin 3a6d021e4a`), never at HEAD.
  </context>

  <steps>
    0. Pre-checks; STOP on any miss:
       - `git merge-base --is-ancestor 3a6d021e4a origin/box/dell2` returns rc 0;
       - at the pin, `release-census.py irpt-status --pin HEAD` reads `changed_members=5` (acceptance, entry, owned_report, pdf_link, submission);
       - live CodeSha256 is `E7VKvhg3...`;
       - record the current S3 object version as the rollback source.
    1. Ledger `irpt-anlreq-r1-irpt-status-20261009` (L1 verify / L2 s3-prefix / L3 activation + route / L4 verify), opened and committed before
       any write, with the pin, built sha and rollback version stated.
    2. Upload: `build-and-upload.sh investor-reporting irpt-status` from the pin worktree.
       - The SHA256 must be `WTGCJPiS...`, or STOP.
       - The symbol closure (the main tree's `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r71/symbol_closure.py`) on the uploaded
         zip, downloaded back by version, must read `missing=0`, or STOP.
    3. Plans in the pin worktree:
       - `investor-reporting/ops`, `-target=module.irpt_status`: the function's `s3_object_version` + `source_code_hash` only;
       - `investor-reporting/api`, untargeted: `1 to add`, the route above.
       Any other line is a STOP. Commit the plan texts, then `safe-apply` each, ops first.
    4. After-read 1: live == `WTGCJPiS...`; both re-plans read 0. After-read 2: the route exists ONCE (`get-routes`), and `GET .../analysis/requests` for
       the test filer answers 200.
    5. After-read 3, on ONE template-lane request of the test filer: either 6b's read-5 request, or one fresh template upload in the Y75 read-4
       shape. Its records and objects become `read3_objects`. Three arms:
       - (a) the owner receives a signed link whose sha256 equals the retained original's;
       - (b) a viewer at ANOTHER firm is refused;
       - (c) a custody-lane request refuses `ANALYSIS_ORIGINAL_NOT_APPLICABLE`.
       The link itself is never logged.
    6. After-read 4: `GET .../analysis/requests/{id}?include=composition` for a ticketed request returns its `ticket_id` and meets `OwnedAnalysisRequest`.
       After-read 5: `analysis-request-pdf` behaves as before for an existing READY request (it signs, or it refuses by the same name).
    7. Branch B (any of 0-2 or 5 fails, or read 3 or 4 fails):
       - re-promote the step-0 version the same session;
       - remove the route by a targeted revert of its `routes.json` entry, then apply;
       - then a BLOCKING row.
       Read the failing call's CloudWatch line before halting.
    8. Write `APPLY-Y1_after_reads.json`:
       - reads "0".."5" (each PASS/FAIL), `built_sha`, `live_sha`, `rolled_back`;
       - `read3_objects` [{key ("bucket/key"), version_id}], `deleted_on_andrews_word` false;
       - `ledger_closed`.
       Close the ledger and commit. Report.
    **AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~10:5xZ): REVISION 2 of the pair, on CTO msgs 3140/3163 (row IRPT_BCKEND-D2-S43). It SUPERSEDES the pin,
    built and census above.**
    - **Pair:** blob 0bb9a5a803 @ba918317c3; the COO half is signed by this amendment. CTO half AMENDMENT 2 (msg 3163), RE-SIGNED.
    - **Pin** `f23639ea21` (`git worktree add --detach /c/dev/anl-r1-pin f23639ea21`). **Built** `BjUZjt2oq8GPJSibq4vD/0m8/LfdN0GF3THwCaBMVOM=`.
    - **Step 0** adds: `merge-base --is-ancestor f23639ea21 origin/box/dell2` returns rc 0 (CTO condition: re-read before the upload; NOT on origin when this
      amendment was cut). The census at the pin reads `changed_members=6`: the five above plus `status_installed.py`.
    - **Step 0** also requires `python -m pytest -q -p no:cacheprovider infra/aws/lambda/investor-reporting/_authz/tests/test_unguarded_census.py` at the pin: 0 failed
      (CTO condition). The ledger names `BjUZjt2o`.
    - The checks `apply1_cells.py` are amended to `BjUZjt2o`. Everything else stands. Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii)
      on a modify.
  </steps>

  <acceptance>
    <criterion id="APPLY1-AC1" cell_refs="AR-y-21"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/apply1_cells.py . APPLY1-AC1</invocation><expect>APPLY1-AC1 PASS</expect></criterion>
    <criterion id="APPLY1-AC2" cell_refs="AR-y-21"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/apply1_cells.py . APPLY1-AC2</invocation><expect>APPLY1-AC2 PASS</expect></criterion>
    <criterion id="APPLY1-AC3" cell_refs="AR-y-21"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/apply1_cells.py . APPLY1-AC3</invocation><expect>APPLY1-AC3 PASS</expect></criterion>
  </acceptance>

  <bounds>
    Write deliverables to `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r1/`. Opaque ids only for real people; synthetic test data only.

    Live writes are exactly:
    - the artifact upload;
    - the two targeted applies (in branch B, also the rollback and revert);
    - read 3's one test request (only if 6b's is not available).

    No S3 delete: the deletes are Andrew's act. No IAM change, no other function or route, no vendor call beyond the existing resolve path of a
    fresh template upload, no SendCommand. NEVER-2: ledger first, closed after. Never `update-function-code`. Edit byte-preserving; ASCII only.
  </bounds>

  <preflight>
comp-blast: RUN -- release-census irpt-status at 3a6d021e4a: 5 changed of 49 vs live, all AR-y-11/AR-y-22; cochange split=0; symbol closure missing=0 (115 pairs); one function and one route.
comp-iam: RUN (by reading) -- no IAM change; irpt-status's role family list (ops/iam.tf:85) already holds ORIGINAL_HOLDINGS and ORIGINAL_CSV reads.
comp-routes: RUN -- api plan-only: exactly 1 to add (GET .../original), under the existing authorizer and integration; the CTO's census condition reads ONE.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger is touched.
comp-adversary: RUN -- APPLY1-AC1/AC2/AC3 dry-run at base: FAIL (no file); AC1 refuses a second route or a live sha other than the signed one; AC3 refuses a branch B that leaves the route.
  </preflight>

  <report_to>2.0.0_SA_COO~Y2: commit hashes, built and live CodeSha256, S3 versionIds, both apply lines, the route census, read 3's arm outcomes (no link), row ids.</report_to>
</task_order>
