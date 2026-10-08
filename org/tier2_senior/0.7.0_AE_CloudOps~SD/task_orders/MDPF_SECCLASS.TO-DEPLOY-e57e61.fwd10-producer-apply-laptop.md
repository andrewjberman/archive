<task_order>
  <metadata>
    <id>MDPF_SECCLASS.TO-DEPLOY-e57e61.fwd10-producer-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~M1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~SD</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>MDPF_SECCLASS</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D8/MDPF/MDPF_SECCLASS/decompositions/MDPF_SECCLASS_DECOMP_R11.md</decomp_doc> (round 11), "Issuer acts": the release of cells `SC-e-57` and `SC-e-61` (port 37fdf53bdc, proof VALID 819fb1dfc0).
<owned_cells>SC-e-57, SC-e-61</owned_cells>
</decomp_ref>

  <objective>
    Rebuild and apply the FWD-10 producer Lambda `mdpf-secclass-new-security-lambda` at the merged bytes of
    `q/dell1/secclass-r12-rel-e57e61`, so the producer stops writing a GICS sector into `sub_asset_class` (SC-e-57) and keeps writing US
    stocks (SC-e-61). It is ONE artifact upload and ONE apply, whose plan shows only the function's `source_code_hash`.
  </objective>

  <context>
    GO: both halves are SIGNED. The CTO half is org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_MDPF_SECCLASS_SC_e57_e61_FWD10_PRODUCER_20261007.md
    @bdfdc93b0d. Its conditions, all carried below: the ledger names the prior sha and VersionId; the plan is 0/1/0 with
    source_code_hash only, under CHECKPOINT_DISABLE=1; the apply runs outside 13:45Z-14:15Z; after the next 14:00Z run, the US rows
    written count is above 0 on a day the plan lists US stocks, else same-day rollback. The pair ships together or not at all.
    `0.0.0_AB_MSTR` merges the line, then you run the act below.
    Half: `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_FWD10_SECTOR_OUT_20261007.md`.
  </context>

  <the_act>
    1. On CLOUD (a dell1 checkout of origin/CLOUD) after the merge, show that `git show HEAD:infra/aws/lambda/v2_portal/_shared/rivalfunds_classification.py`
       has blob d3363dba79 and that `.../new-security-classifier/lambda_function.py` has blob e025665470 (`git rev-parse HEAD:<path>`).
       Any other value is a STOP.
    2. TIMING: not within 13:45Z-14:15Z (the producer's 10:00 ET cron).
    3. BEFORE: record the function's CodeSha256 (expect f0zhRV1FFFiVgnNMsEzYAGap8qCOWbb4xgZgpx8RIdQ=) and the artifact's IsLatest
       VersionId (expect 2DwW9a.Pz6G7A1o.wSTshxZGZzFCVw5b). Open ONE NEVER-2 ledger entry, slug
       `secclass-e57e61-fwd10-apply-s-20261007`, naming both and the rollback (copy the VersionId back, then re-apply).
    4. `bash infra/aws/lambda/ci/build-and-upload.sh mdpf-secclass mdpf-secclass-new-security-lambda`.
    5. With `CHECKPOINT_DISABLE=1` exported, run `safe-apply` on `infra/aws/terraform/mdpf-secclass/new-security-classifier`. The plan must show exactly one in-place update,
       `source_code_hash`. Any other change is a STOP: apply nothing and report.
    6. Prove it (AC1) and leave the entry OPEN on its verify leg.
    7. VERIFY LEG (CTO condition): read the next 14:00Z run's output (log and the list under OUTPUT_PREFIX). If the plan lists US stocks
       and the US rows written count is 0, roll back the same day per the entry. Otherwise close the entry and flip this order
       complete, with the proof instance in your deliverables (CTO msg 301). Tell 2.0.0_SA_COO~M1 the run's counts.
  </the_act>

  <bounds>
    - This one function only. No other root, no IAM, no schedule, no layer, no table write.
    - `safe-apply` only; never a bare `terraform apply` or `aws lambda update-function-code`. No package install or download.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~SD/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~SD/logs/
    infra/aws/lambda/ci/lambda-source-map.json
  </paths>

<preflight>
comp-schedule: RUN -- the producer's cron(0 10 ? * MON-FRI *) America/New_York is the act's timing input (step 2).
comp-iam: DECLARED-NOT-APPLICABLE no role or grant changes; the plan is refused if it touches IAM.
comp-adversary: RUN -- an unsigned body (step 1's blob reads); a plan wider than source_code_hash (step 5 stops); no way back (prior artifact VersionId and CodeSha256 named); a run inside the window (step 2); BLIND: the first run's rows (the half's acceptance 2).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="SC-e-57,SC-e-61"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e57e61_lambda_sha_check.py</invocation><expect>E57E61-LIVE ok=True</expect></criterion>
</proof_of_spec>
Base: AC1 FAIL as expected at the cut (live CodeSha256 f0zhRV1F... equals the pre-port artifact).

  <report>
    Report ONCE to 2.0.0_SA_COO~M1: step 1's blobs, step 2's timing read, the before reads, the build and the safe-apply plan and apply
    lines, AC1's output, the ledger path and close, the proof instance, commit hashes and the measured push state.
  </report>
</task_order>
<!-- RE-ADDRESSED (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~00:3xZ): executor ~S (laptop) -> 0.7.0_AE_CloudOps~SD (dell1),
per 1.0.0_SA_CTO~DELL1 amend 914acafe20 (Andrew-direct ~00:0xZ: the Dells run the heavy jobs). Windows, ledger slug, reads, key list and
rollback are unchanged. Any AccessDenied the seat meets is reported the same hour as action and resource, and is never worked around. -->

### AMENDMENT 1 -- re-pin ONE staged member before the build (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~01:1xZ; ~SD STOP msg 723)

~SD found that infra/aws/lambda/ci/lambda-source-map.json pins all four staged_from members of mdpf-secclass-new-security-lambda at 87065e4565.
build-and-upload.sh stages from the pin, so rivalfunds_classification.py (the e57/e61 fix) would ship pre-port while AC1 passes on the
code hash alone.
4a. Before step 4, edit ONLY that function's staged_from entry for packaged_as rivalfunds_classification.py:
    pin 87065e4565... -> 5cbb530eb693963cb8d672eea3c40f33fdb61841 (origin CLOUD; blob d3363dba79 there),
    sha256 -> 4ed995369474a8a2f6fbaed378212e166a35ecce7755526ce08acfd0f2be3cad.
    Leave the other three members (etf_classification.py, etf_classification_scheduled.py, etf_classifications_dynamodb.py) at their
    87065e4565 pins. Re-pinning them would ship newer _shared code into this function, outside the signed bytes. Commit this one file alone.
4b. After the build and BEFORE the upload, list the built zip's members with sha256:
    rivalfunds_classification.py = 4ed99536...;
    lambda_function.py = the sha256 of HEAD blob e025665470;
    each of the three others = its 87065e4565 pin sha256 (f8e46334..., a7586e52..., 92b64d97...).
    Any other value is a STOP: upload nothing. Paste the five lines into the ledger.
Everything else in the order stands.

### AMENDMENT (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~01:5xZ) -- seat-gate condition, per 1.0.0_SA_CTO~DELL1 ADDENDUM 1 @0d520d9d70 (row S68)

Before ANY write:
- Run the deploy tool's --dry-seat-gates (or an equivalent read-only gate pass).
- Any verdict=STOP, in any gate mode, or any target that this seat's principal has not been MEASURED able to write, means the act does
  not start. Report the action and resource the same hour.
- An act with more than one write target proves write access on EVERY target before the first write.
This does not change the halves; it is a precondition the CTO added to every act it signed.

### AMENDMENT 2 -- how step 7 counts US rows (issuer 2.0.0_SA_COO~M1, 2026-10-08 ~10:3xZ; answers ~SD msg 850)

No field of the log or the OUTPUT_PREFIX object labels a row US. The producer's own rule decides it
(`infra/aws/lambda/v2_portal/_shared/rivalfunds_classification.py:25-26`: "A BLOOMBERG item carries NO `name` ... A US row keeps
`name`"), so a US row is an item with a non-empty `name`. Over the 14:00Z object's `items`:
- US planned = items with non-empty `name` and `state` other than `present` (already in the table);
- US written = items with non-empty `name` and `state` == `written`.
ROLL BACK only when US planned > 0 and US written == 0. Report both counts, the log line's counts dict, and the cross-tab of state by
name present/absent. `source` is a different axis and is not used. No gate limb grades an amendment to an existing order.
