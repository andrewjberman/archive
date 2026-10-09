<task_order>
  <metadata>
    <id>IRPT_BCKEND.TO-APPLY-Y77.irpt-ycharts-generate-release6-custody</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>IRPT_BCKEND</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<proof_of_spec>
Criterion ids: Y77-1-AC1, Y77-1-AC2, Y77-1-AC3. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y77/IRPT_BCKEND.TO-APPLY-Y77.proof_of_spec.json`, validated with `python .tools/proof-of-spec-check.py <instance> Y77-1-AC1,Y77-1-AC2,Y77-1-AC3`. Shape: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~159/IRPT_BCKEND.TO-IB-yr-681.release3-a1-run-as-signed.proof_of_spec.json`.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP_R77_Y.md</decomp_doc> round 77, workstream ~Y, cell `IB-ya-771` (was `APPLY-Y77`).
<owned_cells>IB-ya-771</owned_cells>
</decomp_ref>

  <objective>
    Release 6 of `irpt-ycharts-generate` on dell2. It installs the custody factory: a Performance client statement submission (no
    `input_id`) reaches `build_accepted_custody_entry` instead of raising `CUSTODY_FACTORY_REQUIRED`.
    - Code built `V6EiBNcJ2267Ox2cZAj7VZC+rlv+XrmpW5y6aCr/YOM=` at pin `bea2a2ceb3`.
    - New inline policy `irpt-ycharts-generate-custody-factory-policy` with 11 ARNs.
    - Layer `AWSSDKPandas-Python312:16` added.
    Rollback is release 5b, `5FRkux2oSNN1jB4xJEibio+F9F2ofl9mgcuH9jN/JrY=`.
  </objective>

  <context>
    Run this AFTER `TO-APPLY-Y75` (release 5b) is terminal with live `5FRkux2o...`. If 5b rolled back, this order does not start; report and wait for the issuer.

    Read the pair first: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release6_custody/NEVER_WIDEN_PAIR_RELEASE6_CUSTODY.md`
    (blob a3c54ba263). Its section 3 prints the 11 ARNs. Then the CTO half, `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_YCG_RELEASE6_CUSTODY_CTO_HALF.md`
    @96e03f8ba1. Its conditions bind:
    - 5b live first;
    - the symbol closure is re-run on the uploaded zip;
    - the policy reads back with exactly the 11 ARNs;
    - the read-3 objects are listed for Andrew's delete word;
    - the IAM write is reported via `0.0.0_AB_MSTR~DELL2`.

    Every step shape (ledger, upload, targeted plan from the initialized `infra/aws/terraform/investor-reporting/ycharts` root,
    safe-apply, direct invoke) follows `TO-APPLY-Y75` and release 3's `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-yr-681.release3-a1-run-as-signed.md`.
  </context>

  <steps>
    0. Pre-checks. STOP on any miss:
       - `git fetch origin` and `git merge-base --is-ancestor bea2a2ceb3 origin/box/dell2`, rc 0;
       - `python infra/aws/lambda/ci/release-census.py irpt-ycharts-generate --pin HEAD` shows `changed_members=11` against release 3. Against 5b, only
         `generate_installed` and the 4 added members (custody_interpreter, custody_ports, holdings_publication,
         holdings_publication_port) are new;
       - `python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r73/cochange_closure.py irpt-ycharts-generate` reads `split=0`;
       - live CodeSha256 is `5FRkux2o...`;
       - record the current S3 object version as the rollback source;
       - record every object version under `s3://opal-data-irpt/irpt/cottonwood/platinum/custody_reports/` as `custody_reports_before`
         (`list-object-versions`, auto-paginated, count printed).
    1. Ledger `irpt-ycg-release6-20261009` (L1 verify / L2 s3-prefix / L3 activation + IAM / L4 verify). Open and commit it before any write.
    2. Upload: `build-and-upload.sh investor-reporting irpt-ycharts-generate`. The SHA256 must be `V6EiBNcJ...`, or STOP. Then run
       `python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r71/symbol_closure.py <the uploaded zip>`.
       It must print `missing=0` and `symbol_closure PASS`, or STOP before the apply.
    3. Targeted plan with `-target=aws_iam_role_policy.generate_custody_factory -target=module.irpt_ycharts_generate`. Expect 1 to add, 1 to change, 0 to destroy:
       - the add is the policy;
       - the change is `s3_object_version` + `source_code_hash` + the layers list only.
       Any other attribute -> STOP. Commit the plan text, then `safe-apply`.
    4. After-read 0 is step 0. After-read 1: live == `V6EiBNcJ...`; layers read `irpt-common` + `AWSSDKPandas-Python312:16`; the
       policy reads back (`aws iam get-role-policy`) with exactly the 11 ARNs of pair section 3; re-plan 0. After-read 2: import
       census `failed: {}`. It GATES the rest; on failure go straight to branch B.
    5. After-read 3: ONE direct-invoke Performance client statement submission for cottonwood with no `input_id` (the
       test_generate_installed_custody.py shape, synthetic statement, no real-person data). PASS when the CloudWatch line shows no
       `CUSTODY_FACTORY_REQUIRED` and no ImportError, and the outcome is either an accepted custody entry or a typed refusal from
       the factory's own validation. Quote the outcome line in `read3_outcome`. List every object version it wrote under the
       custody_reports prefix as `read3_objects` [{key, version_id}].
    6. After-read 4: one `input_id` submission still reaches the prospect factory (release 3's shape).
    7. Branch B (any of 0-2, 4, 6 fails, or read 3 raises CUSTODY_FACTORY_REQUIRED or an ImportError):
       - the same session, re-promote the step-0 version;
       - revert the policy and the layer by a targeted apply at the parent of `2ae4d86e00` for `ycharts/generate.tf`, plan 0/1/1;
       - live reads `5FRkux2o...`, the policy is absent and the pandas layer is detached;
       - then a BLOCKING row.
    8. Write `Y77-1_release6_after_reads.json`: reads "0".."4" each PASS/FAIL, `built_sha`, `live_sha`, `rolled_back`,
       `custody_reports_before`, `read3_outcome`, `read3_objects`, `deleted_on_andrews_word` false, `ledger_closed`. Close the
       ledger and commit. Report the IAM change to `0.0.0_AB_MSTR~DELL2` (policy name, role, 11 ARNs, commit). Report.
    **AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~06:3xZ): build, census, plan and apply at the PIN, never at HEAD (as Y75's AMENDMENT 1).**
    - **Why:** the function's `source_dir` packages unpinned members straight from HEAD, and HEAD has moved past `bea2a2ceb3` (IRPT_ANLREQ
      drains among others). Issuer read: a BUILD_ONLY at HEAD yields `teYpLltujx29hTC4EutL73C07Cy421MitP389zV/FLw=`; a detached worktree at
      `bea2a2ceb3` rebuilds the signed `V6EiBNcJ...` exactly.
    - **Step 0:** `git worktree add --detach /c/dev/y77-pin bea2a2ceb3`. Run the census and `cochange_closure.py` INSIDE it (expect 11 and
      `split=0`). The ancestor check against origin is unchanged.
    - **Steps 2-3 and branch B:** the build, the symbol closure (the main tree's `checks/r71/symbol_closure.py` on that zip), `terraform
      init`, the targeted plan and `safe-apply` all run in the worktree's `infra/aws/terraform/investor-reporting/ycharts`.
    - After the ledger closes, `git worktree remove /c/dev/y77-pin`. Every deliverable is still written and committed in the shared tree.
    - Gate limb that graded this amendment: `to-pipeline-gate.py` GATE (viii) on a modify; criteria unchanged.
    **AMENDMENT 2 (issuer `2.0.0_SA_COO~Y2`, 2026-10-09 ~08:4xZ): this order now applies RELEASE 6b. It SUPERSEDES the pin, built, rollback and
    reads named above and in AMENDMENT 1.**
    - **Why:** IB-pr-390 went live at 07:49Z as `ZA0QJ5Wt...` (via IB-pr-395, CTO msgs 2833/2855). The CTO ruled that release 6's `V6EiBNcJ` must
      NOT be applied, because it would revert 390's served.py.
    - **Pair:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release6_custody/NEVER_WIDEN_PAIR_RELEASE6B_CUSTODY.md` @ba6fcb1c14
      (blob 768db03070; the COO half is signed by this amendment). CTO half
      `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RELEASE6B_CUSTODY_CTO_HALF.md` (msg 2888), GIVEN.
    - **Pin** `66207bce7d` (on origin): `git worktree add --detach /c/dev/y77-pin 66207bce7d`; every build, census, plan and apply step runs there.
      **Built** `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=`.
    - **Step 0:** live is `ZA0QJ5Wt/7JcwmuzVfHOeNAdFk6th4H5IEeqQStDYm8=`, and the rollback source is S3 version `8rOI5aDff8mlWQQ6YNVy7Is11Pfh8jcn`;
      otherwise STOP. The census at the pin, against live, reads exactly 3 changed members (`acceptance.py`, `submission.py`,
      `contracts/AnalysisSubmissionRequest.schema.json`).
    - **Step 3, the plan:** 1 add (the policy) plus the function's `s3_object_version` + `source_code_hash`. There is NO layer diff (390 attached it).
      ANY other line is a STOP (CTO condition).
    - **Reads:** "0"..."5" per the 6b pair, section 4. Read 5 is the ticket binding live: one `input_id` submission with a valid `ticket_id` is
      accepted and its record carries it; a malformed one refuses `TICKET_REFERENCE`. Record reads 4 and 5's S3 objects as `prospect_objects`
      [{key, version_id}]. Their deletes wait on Andrew's word (CTO condition); do not delete them.
    - **Branch B:** re-promote `8rOI5aDf` and remove the policy. The layer STAYS, because it is 390's.
    - **The ledger is pinned** (CTO condition): it names pin, built, rollback and version. After the apply, re-read the census row (CTO condition).
    - The checks `checks/r77/y77_cells.py` are amended to these values (AMENDMENT 2). Gate limb that graded this amendment: `to-pipeline-gate.py`
      GATE (viii) on a modify.
  </steps>

  <acceptance>
    <criterion id="Y77-1-AC1" cell_refs="IB-ya-771"><invocation>python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r77/y77_cells.py . Y77-1-AC1</invocation><expect>Y77-1-AC1 PASS</expect></criterion>
    <criterion id="Y77-1-AC2" cell_refs="IB-ya-771"><invocation>python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r77/y77_cells.py . Y77-1-AC2</invocation><expect>Y77-1-AC2 PASS</expect></criterion>
    <criterion id="Y77-1-AC3" cell_refs="IB-ya-771"><invocation>python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/checks/r77/y77_cells.py . Y77-1-AC3</invocation><expect>Y77-1-AC3 PASS</expect></criterion>
  </acceptance>

  <bounds>
    Write deliverables to `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y77/`. Use opaque ids only for real people. Synthetic statement
    only.

    Live writes are exactly:
    - the artifact upload;
    - the one targeted apply (policy + function);
    - in branch B, the rollback and revert;
    - read 3's custody_reports objects;
    - read 4's prospect records.

    No S3 delete: the deletes are Andrew's act. No other function, no other policy, no vendor call beyond read 4's existing resolve
    path, no SendCommand. NEVER-2: ledger first, closed after. Never `update-function-code`. Edit byte-preserving; ASCII only.
  </bounds>

  <preflight>
comp-blast: RUN -- release-census at bea2a2ceb3: 11 changed of 104 vs release 3 (5 new vs 5b), one function; cochange_closure split=0; symbol_closure missing=0 on the BUILT zip; plan-only 1/1/0.
comp-iam: RUN -- one new inline policy, 3 statements over 11 ARNs, each printed beside its owner's read set (pair section 3); CTO half GIVEN @96e03f8ba1.
comp-routes: DECLARED-NOT-APPLICABLE -- no route or authorizer change; reads go by direct IAM invoke.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule is touched.
comp-adversary: RUN -- Y77-1-AC1/AC2/AC3 dry-run at base: FAIL (no file); AC1 refuses a policy with any ARN beyond the signed 11; AC3 refuses a branch B that leaves the policy or layer behind.
  </preflight>

  <report_to>2.0.0_SA_COO~Y2: commit hashes, built and live CodeSha256, the S3 versionIds, the apply line, the policy read-back count, read 3's outcome line and object count, row ids.</report_to>
</task_order>
