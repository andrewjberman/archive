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
    **AMENDMENT 2 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~12:2xZ): a SECOND apply, REVISION 3, on top of live revision 2.** CTO msgs 3245/3262, ~G2 msg 3241,
    row IRPT_YCDGEN-D2-S20.
    - **Why:** live `BjUZjt2o` refuses the Opal 49financial report `REQ-5e4149d2...` with `RetentionRefused 'invalid retention reference'`, because its
      packaged `reporting_policies.json` lists research firms `[cottonwood]`.
    - **Pair:** REVISION 3 @1d9154f3ce (blob ac59c753eb); the COO half is signed by this amendment, and the CTO RE-SIGNED it (msg 3262).
    - **Pin** `5240156380`: `git worktree add --detach /c/dev/anl-r1c-pin 5240156380`; every step runs there. Step 0 adds
      `merge-base --is-ancestor 5240156380 origin/box/dell2` rc 0. **Built** `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=`. **Rollback** `BjUZjt2o...`
      (revision 2; record its S3 version at step 0).
    - **CTO condition (STOP rule):** print each packaged member's sha256, uploaded against live. EXACTLY `reporting_policies.json` may differ; a second
      differing member is a STOP before the apply. Record it as read "7" (PASS when exactly one differs).
    - **Plan:** `investor-reporting/ops -target=module.irpt_status`, the code only. No API change; the `/original` route stays exactly ONE.
    - **Read "6":** `REQ-5e4149d2`'s owned read through irpt-status no longer refuses `RetentionRefused` (served, or a different typed refusal quoted).
      Reads "0"-"2" are re-run for revision 3, with live `t6OJTCcm`. Reads "3"-"5" stay with the laptop spec @66b6d08b9c; they are unaffected
      by a registry-only change.
    - Write the result into the same `APPLY-Y1_after_reads.json` with `built_sha` `t6OJTCcm` and `revision` 3. On branch B, re-promote revision 2's
      version. Copy `2.0.0_SA_COO~G2` on read "6" (YCDGEN FWD-1 grade).
    - The checks `apply1_cells.py` are amended to these values (@e47eb94fa9). Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii)
      on a modify.
    **AMENDMENT 3 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~13:4xZ): reads 3a, 4 (route) and 5 are RE-RUN on ONE FRESH synthetic request.** Laptop result
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/Y1_laptop_reads_3_5_result.json`: 3b TRUE, 4_record TRUE, 3c null (0 custody
    requests). 3a, 4_route and 5 refused upstream on a content-addressed retention row the Y75 cleanup deleted; it is shared by Y77's three test requests
    (row IRPT_BCKEND-D2-S51). Ruling: NO restore, because only test requests are affected.
    - **This seat (dell2) creates the request:** ONE template-lane on-behalf upload in the TO-APPLY-Y75 read-4 shape. Use the same verified 49financial
      advisor, a fresh synthetic test filer, and NEW file bytes (one holding changed), so no retention row is shared with any earlier request. Re-POST
      until NORMALIZED. Then ONE prospect submission with a NEW ticket id: file a fresh Ticket Center ticket of type analysis_request as the filer, or
      use the existing synthetic TCK if the filer cannot file. Record `fresh_request_id`, `fresh_ticket_id`, and its admit keys PLUS a principal-free
      retention dependency walk proving none of its rows is shared.
    - **Then the laptop** (relayed by the issuer) runs 3a, 4 (route) and 5 on `fresh_request_id`, read-only, with booleans only.
    - **Cleanup** (the fresh request plus Y77's three broken requests) goes on a list for Andrew's word, built ONLY after a dependency walk (row D2-S51 rule).
    - Write `fresh_request_id`, `fresh_ticket_id` and the walk into `APPLY-Y1_after_reads.json`. Gate limb that graded this amendment: `to-pipeline-gate.py`
      GATE (viii) on a modify.
    **AMENDMENT 4 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~15:3xZ): a THIRD apply, REVISION 4, on top of live rev 3.** The reader registers the research revision
    (derived from the packaged registry, fail closed); CTO ruling AMENDMENTS 2-3, msgs 3514/3548.
    - **Pair:** `release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV4_IRPT_STATUS.md` @86685d4180 (blob 142e1e6d2d); the COO half is signed by this amendment. CTO half
      AMENDMENT 4 @080347139a (msg 3569), GIVEN.
    - **Pin** `287b105600` (ON origin): `git worktree add --detach /c/dev/anl-r1d-pin 287b105600`. **Built** `VC/r14kaXm6FqaZOOFm3fT+8qngsyGI5Yr7U+DgYx64=`.
      **Rollback** `t6OJTCcm` (record its S3 version at step 0). The ledger STATES the pin and the built sha.
    - **R0 (CTO condition):** the per-member diff of the UPLOADED zip against live is EXACTLY `status_installed.py`; anything else is a STOP. The SHARED-ROOT STOP
      applies: if another seat holds an open ledger or plan on the `investor-reporting/ops` root, STOP and report.
    - **R1:** closure on the uploaded zip, missing=0. **R2:** live == `VC/r14ka`, re-plan 0, `_authz` census 22 of 22. **Only an R2 failure rolls back** (re-promote
      rev 3's version).
    - **R3** is `2.0.0_SA_COO~G2`'s owner read of REQ-5e4149d2 in a NEW sr1 window: codes and section names only, and a refusal is recorded with its code. Record ~G2's
      result as read "6".
    - Write the same after-reads file with `revision` 4 and `built_sha` VC/r14ka; checks `apply1_cells.py` are amended. Gate limb that graded this amendment:
      `to-pipeline-gate.py` GATE (viii) on a modify.
    **AMENDMENT 5 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~16:2xZ): EXECUTE BRANCH B NOW -- roll irpt-status back to rev 3.** CTO ruling msg 3681 (~G2 msg 3675):
    live rev 4 `VC/r14ka` raises `TypeError: build_retained_repositories() got an unexpected keyword argument 'additional_policy_revisions'` at
    `status_installed.py:137` on EVERY call (52 events since 15:43Z, issuer re-read). The packaged `composition.py` predates the kwarg. A regression to all callers
    is Branch B, superseding AMENDMENT 4's "only an R2 failure rolls back".
    - **Act:** re-promote rev 3's S3 version `mkD1gV_CByQfMVGbNzf6E7EKsUUlKdXb` (the `rollback_source_version` you recorded) through the same Terraform path
      (`safe-apply`; never `update-function-code`). Open and close a ledger entry.
    - **After-reads:** (a) live CodeSha256 == `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=`; (b) one real GET answers 200 for a non-49F caller; (c) the
      CloudWatch count of `additional_policy_revisions` errors stays flat for 5 minutes after the promote. Write `rolled_back` true and the three reads into
      the after-reads file.
    - Rev 4 is re-cut by the issuer with `composition.py` co-staged and a live-call arm. Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii)
      on a modify.
    **AMENDMENT 6 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~17:2xZ): a FOURTH apply, REVISION 5 (the rev 4 re-cut).** Pair
    `release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV5_IRPT_STATUS.md` @778f5097f0 (COO half signed). CTO half AMENDMENT 6 @84b912d229 (msg 3780), GIVEN.
    Its condition 1 holds: IB-pr-419 reads irpt-status's profile_reader as LATENT (@7364c85e16, CTO msg 3784).
    - **Pin** `54ed3aa8f6` (ON origin, box/dell2 @13e4164cf1): `git worktree add --detach /c/dev/anl-r1f-pin 54ed3aa8f6`. **Built**
      `DZOdwUOG/+EQe4mxW65GoDSoa4fckLXDXQDfExm3fTk=`. **Rollback** rev 3 `t6OJTCcm`: record the object version you replace at step 0. The ledger STATES the
      pin and the built sha.
    - **R0:** live at start == `t6OJTCcm`. The per-member diff of the UPLOADED zip against LIVE (read via `get_function`) is EXACTLY `status_installed.py`,
      `composition.py` and `repository.py`; anything else is a STOP. The shared-root STOP applies.
    - **R1:** on the UPLOADED zip, symbol closure missing=0, and `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/signature_closure.py`
      prints exactly one mismatch, the tolerated `served:1006 ... ['profile_reader']`.
    - **R2:** live == `DZOdwUOG`, re-plan 0, the `/original` route count is 1.
    - **R3 (live-call arm; the ledger does NOT close before it):** irpt-status 5xx count and `TypeError` count both 0 over 5 minutes, with START lines
      printed as the traffic denominator. AND `2.0.0_SA_COO~G2`'s authorized owner GET answers 200 (its sr1 window). **Either one failing is Branch B:**
      re-promote rev 3's object version.
    - **R4:** `2.0.0_SA_COO~G2`'s owner read of `REQ-5e4149d2` (status-job and analysis-report). If it fails ALONE, record it with its code; no rollback.
    - Write the same after-reads file with `revision` 5. Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii) on a modify.
    **AMENDMENT 7 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~18:0xZ): rev 5 Branch B executed; release 1's irpt-status line moves into ONE-TREE build IB-pr-416.**
    Rev 5 `DZOdwUOG` went live at 17:42Z. At 17:57:56Z it raised TypeError `RetentionPolicy.reference() takes 3 positional arguments but 4 were given`
    (staged `retention.py` @80a79a7462 is older than `repository.py` @2aa217ec58). Branch B ordered at 17:59Z; live reads rev 3 `t6OJTCcm` again at
    18:02:55Z (issuer re-read). ~G2: R3 authorized 200 (cottonwood history); R4 `REQ-5e4149d2` ok:false with the same TypeError (row IRPT_YCDGEN-D2-S24).
    CTO ruling msg 3856 (AMENDMENT 7 @e7c8cf880a): no more member re-pins. The next irpt-status release takes every investor-reporting member from ONE commit,
    graded by a per-route replay plus the live-call arm, inside `2.0.0_SA_COO~P2`'s IB-pr-416. **This order stays OPEN.** Its reads 5-6 (the ticket-bound
    READY and `REQ-5e4149d2` served) are graded on that release. No further apply is cut here. Close the rev 5 ledger as Branch B. Gate limb that graded this
    amendment: `to-pipeline-gate.py` GATE (viii) on a modify.
    **AMENDMENT 8 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~03:4xZ): a FIFTH apply, REVISION 6 -- irpt-status from ONE commit (IB-pr-416's build).**
    Pair `release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV6_IRPT_STATUS.md` @7ce505dc5a (blob 1d38417741; COO half signed). CTO half: section A3 of
    `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_416_THREE_FUNCTIONS_ONE_TREE_CTO_HALF.md` @81cba68056 (msg 3962),
    SIGNED against that blob. Read both before any act. Conditions 1, 2, 3, 5, 6, 8 and 9 of that half bind and are placed below.
    - **Pin** `5c35a6f9f9` (the source-map landing, TO-IB-pr-420 step 1; condition 2): `git worktree add --detach /c/dev/anl-r1g-pin 5c35a6f9f9`; build,
      plan and apply there, never at HEAD. Step 0: `git fetch origin`, then `git merge-base --is-ancestor 5c35a6f9f9 origin/box/dell2` rc 0 (NOT on origin
      when this amendment was cut), with `origin/CLOUD` beside it as the control. **Built** `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=` (the issuer built
      it at the pin from the real map, BUILD_ONLY, and read this digest). **Rollback** rev 3 `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=`, object version
      `iDIQPfNUQM8EH4pjrG.codFMMaR071yi`: re-read both at step 0 and record the version you replace.
    - **Start (condition 3; shared-root STOP):** do not start until `2.0.0_SA_COO~P2`'s adapter apply has read its live-call arm clean and the issuer has
      relayed that. If ledger `irpt-bckend-ib420-adapter-narrative-20261011`, or any other entry or plan, is open on `investor-reporting/ops`, STOP and report.
    - **Ledger** `irpt-anlreq-r1-irpt-status-rev6-20261011`, opened and committed BEFORE the first upload, stating the pin, the built sha and the rollback
      version (condition 6). A live CodeSha256 other than `t6OJTCcm` at the precheck is a STOP and a row.
    - **Condition 1 (digest control):** `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status` at the pin prints
      `6idtFvAm...`, or ABORT. Then the same without BUILD_ONLY.
    - **R0:** the per-member diff of the UPLOADED zip against LIVE (read via `get_function`, never the S3 key) is EXACTLY these 13: `composition.py`,
      `data/custodian_key_seam.json`, `durable_job.py`, `entry.py`, `ids.py`, `interactive_access.py`, `loaders.py`, `owned_report.py`, `repository.py`,
      `resident_installed.py`, `retention.py`, `served.py`, `status_installed.py`; 0 added, 0 removed. Anything else is a STOP. Record it as read "7".
    - **R1,** on the UPLOADED zip downloaded back by version: symbol closure missing=0; `checks/r2/signature_closure.py`, IB-pr-416's
      `signature_closure_attr.py` and `method_call_limb_416.py` each 0 mismatches (the `profile_reader` mismatch is no longer tolerated: it is closed).
    - **Condition 8 (reach read),** on the same UPLOADED zip:
      `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/reach_read.py <zip>` ends `count=0 verdict=PROCEED` with 7 routes read.
      The issuer's own run on its build reads that (@e1e037b14e, `release1/REV6_REACH_READ_IRPT_STATUS.json`). A count above 0 is a STOP to the CTO.
    - **Plan:** `investor-reporting/ops`, `-target=module.irpt_status`: `s3_object_version` + `source_code_hash` only; any other line is a STOP. Commit the
      plan text, then ONE `safe-apply`. No API, IAM, layer or environment change.
    - **R2:** live == `6idtFvAm`, re-plan 0, the `/original` route count is 1.
    - **R3 (live-call arm; the ledger does NOT close before it):** within a minute of the promote, one GET `/api/scoped/investor-reporting/status` for a
      non-49F caller: a typed answer, never a 500. Then irpt-status 5xx and `TypeError` counts both 0, counted from the promote UNTIL
      `2.0.0_SA_COO~G2`'s reads below have finished, with START lines printed PER TENANT (49financial and cottonwood). A window that closes earlier, or a
      one-tenant denominator, is not R3.
    - **R4 (`2.0.0_SA_COO~G2`, sr1 window):** `REQ-5e4149d2`'s owner read (status-job and analysis-report) answers with no `RetentionRefused` and no
      `TypeError`. Record it as read "6". **R5 (same window):** one GET `.../analysis/requests/{id}/original` answers and the object count stays 1.
    - **Condition 5 (the IB-pr-405 widening, both arms, same window):** as `svc-custody-statement`, one `analysis-request-read` of a request owned by its
      own firm answers; one of a request owned by another firm is refused `NOT_AUTHORIZED`. If the subject cannot be driven in the window, the ledger
      records that widening as APPLIED, UNEXERCISED, in those words.
    - **Branch B:** R2 failing, OR any 5xx or any `TypeError` in the log group at any time inside the R3 window (a 200 beside a logged `TypeError` is
      still Branch B), OR R5's count moving: re-promote rev 3's object version through the same Terraform path at once, then read live == `t6OJTCcm` and
      probe BOTH tenants. R4 answering a typed refusal that is neither is recorded with its code and routed to the issuer; no rollback.
    - **Condition 9:** the ledger close states both A1 widenings (`svc-commentary` on `reserve`; `svc-irpt-packager` reading `ANALYSIS_COMMENTARY`) as
      APPLIED, UNEXERCISED on irpt-status.
    - Write the same `APPLY-Y1_after_reads.json` with `revision` 6, `built_sha` `6idtFvAm...`, reads "0".."7", plus `r3` (5xx, TypeError, START per tenant,
      window start and end), `r5_original_count`, `condition5` (both arms, or APPLIED, UNEXERCISED) and `condition9`. The checks `apply1_cells.py` are
      amended to `6idtFvAm`. Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii) on a modify.
    **AMENDMENT 9 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~04:3xZ): CORRECTION of R5 in AMENDMENT 8 -- the count that stays 1 is the ROUTE count, not an object count.**
    The source is this issuer's own msg 3866 of 2026-10-09: "one GET .../analysis/requests/{id}/original route answers (count stays 1)". The IB-pr-416
    packet glossed it as "(the read does not write)", and the REVISION 6 pair section 5 and AMENDMENT 8 then wrote "the object count stays 1". No object
    was ever named, so that read could not be run (`2.0.0_SA_COO~G2` msg 4052 asked which object). The issuer's error.
    - **R5 as corrected:** `2.0.0_SA_COO~G2` makes ONE GET `.../analysis/requests/{id}/original` and reports its code; the APPLIER re-reads the
      `/original` route count after it (`get-routes`): exactly 1. That is the same census as R2, read a second time after the call.
    - **Branch B as corrected:** "R5's count moving" means that route count reading other than 1. A 5xx or a `TypeError` on the GET is already Branch B
      under R3.
    - **Condition 5** cannot be driven in the window (`2.0.0_SA_COO~G2` msg 4052: its grant covers the analysis service credential only). The ledger
      records the IB-pr-405 widening as APPLIED, UNEXERCISED, in those words, as the CTO half's condition 5 provides.
    - **CTO msg 4062 (corrected R5 ACCEPTED, no stop):** the ledger close states `the read does not write: NOT MEASURED`, in those words; it is
      not inferred from the route count. The three widenings (IB-pr-405 and the two of A1) close APPLIED, UNEXERCISED on irpt-status.
    - The signed pair file is NOT edited (the CTO half binds its blob 1d38417741); this amendment is the correction's carrier, sent to
      `1.0.0_SA_CTO~DELL2`. Everything else in AMENDMENT 8 stands. Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii) on a modify.
    **AMENDMENT 10 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~05:2xZ): REVISION 6 is APPLIED and its ledger CLOSED, Branch A; APPLY1-AC1 stays FAIL on read "5", and that is the world, not the check.**
    Applier msg 4146, re-read by the issuer: live `6idtFvAm` (LastModified 04:44:47Z), ledger `irpt-anlreq-r1-irpt-status-rev6-20261011` absent from
    `.open_deploys` at HEAD, APPLY1-AC2 PASS and APPLY1-AC3 PASS run by the issuer; APPLY1-AC1 FAIL with reads 0-4, 6, 7 PASS and "5" `DEFERRED-RELEASE4`.
    - **The slot map (the issuer's omission in AMENDMENT 8, which said "reads 0..7" and named only "6" and "7"):** read "5" keeps the meaning it has had
      since step 6 and decomposition R2 AMENDMENT 3: one TICKET-BOUND request reaching READY, with `analysis-request-pdf` behaving as before on it. It is
      graded on release 4's run (the resident release, `2.0.0_SA_COO~G2`'s `AR-g-23` packet), "not before". AMENDMENT 7's sentence that reads 5-6 are graded
      on this release was wrong for read 5: nothing in window 6 was a ticket-bound READY request. The check `apply1_cells.py` is NOT amended to pass it.
    - **AMENDMENT 8's R5** (one GET `.../original`, route census 1) is a different read. The applier filed it under key "5" of the after-reads file, a
      mapping it stated in `read_map`. It is asked to move that result to its own key `r5_original_get` and to write `"5": "DEFERRED-RELEASE4"`, so the
      file and the check agree without the overlay.
    - **Reads "3" and "4"** in the check still come from the laptop re-run of 2026-10-09 on revision 2 (`BjUZjt2o`): MEASURED THEN, not on revision 6.
      On revision 6 the `/original` reader answered 200 once (`2.0.0_SA_COO~G2`, HELD); arms 3b and 3c were not re-run.
    - **Read "6"** is PASS on R4's written terms (no `RetentionRefused`, no `TypeError`; the report served 257 sections). The status-job read is NOT
      READY: `ANALYSIS_STATUS_DATE_BASIS_UNAVAILABLE`, row `IRPT_ANLREQ-D2-S19`.
    - **This order stays `pending`** on read "5" alone. No further apply is owed under it; the applier owes only the key move above.
    Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii) on a modify.
    **AMENDMENT 11 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~06:1xZ): read "5" is RE-HOMED to release 4's apply order. Its text and its check are unchanged.**
    Ruling: 1.0.0_SA_CTO~DELL2 msg 4240. Decomposition R2 AMENDMENT 3 already defers read 5 to release 4 (the resident release, `2.0.0_SA_COO~G2`'s
    `AR-g-23` packet), so this order carried a check its own act cannot run, and the round could not close.
    - **This is not the amendment AMENDMENT 10 refused.** That would have changed a check so it passed. This changes WHICH ORDER OWES the read; the read
      still has to pass, and it reads FAIL today.
    - **The criterion, verbatim, now owed by release 4's apply order:** `python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/apply1_cells.py . REL4-READ5`,
      expecting `REL4-READ5 PASS`. It is the same statement the check has always made for slot "5": one TICKET-BOUND request reaches READY and
      `analysis-request-pdf` behaves as before on it. Run by the issuer at this amendment: `REL4-READ5 FAIL` (read 5 is `DEFERRED-RELEASE4`).
    - **Release 4's apply order does not exist yet** (searched: no IRPT_ANLREQ task order names release 4 or `AR-g-23`). Until `2.0.0_SA_COO~G2` cuts
      it, the read is PARKED on row `IRPT_ANLREQ-D2-S25`: owner `2.0.0_SA_COO~G2`; un-parks when that order is cut carrying the criterion above.
    - **APPLY1-AC1 is now graded on reads 0-4, 6 and 7,** the reads this order's act made. Run by the issuer after the change: APPLY1-AC1 PASS,
      APPLY1-AC2 PASS, APPLY1-AC3 PASS. Reads "3" and "4" remain the 2026-10-09 laptop re-run on revision 2, as AMENDMENT 10 states.
    - The applier updates its proof instance's AC1 row to this amendment; the status flip follows from the issuer.
    Gate limb that graded this amendment: none named in the gate's output on this lane's modifications tonight (`to-pipeline-gate` printed only its
    newly-added-order line); stated here as the CTO asked.
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
