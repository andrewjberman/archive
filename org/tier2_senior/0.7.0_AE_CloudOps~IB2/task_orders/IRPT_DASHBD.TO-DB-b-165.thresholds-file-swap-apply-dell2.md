<task_order>
  <metadata>
    <id>IRPT_DASHBD.TO-DB-b-165.thresholds-file-swap-apply-dell2</id>
    <issued_by>2.0.0_SA_COO~D2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-13</date>
    <status>complete</status>
    <project_code>IRPT_DASHBD</project_code>
  </metadata>
<risk>WORLD</risk>
<round>87</round>
<workstream>B</workstream>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP.md</decomp_doc> section 89 (round 87), issuer cell `DB-b-165`, FWD-4.
<owned_cells>DB-b-165</owned_cells>
</decomp_ref>

  <objective>
    Apply the thresholds-file swap: ONE gold Lambda release of `irpt-49f-reporting-gold-lambda` over live `i2r7CbVr...` (CodeSha256
    `i2r7CbVr7ew/U0Ziwoi+Q3JnWLUZ0dBYjAv6XMrs8z8=`, MemorySize 3008; the REFRESH 4 build you applied), with EXACTLY ONE staged file re-pinned:
    the thresholds file, from the 24-key blob to the tracked six-key file. By ONE targeted `.tools/safe-apply.sh`; then ONE dry-run invoke,
    read against the 85 percent lines. You are the applier the pair names (its condition 6: an AE seat, not a worker).
  </objective>

  <context>
    READ ALL THREE FILES WHOLE BEFORE STEP 0, the files and not this restatement, and say so in the ledger's opening entry:
    - Packet (worker ~112, 2026-10-11): org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~112/NEVER_WIDEN_PACKET_GOLD_PACKAGE_THRESHOLDS_FILE.md,
      sha256 `2ed4e840ef5624707a144d5c79f8bf2d96cde67e929a790e908e01ec080cd662` (re-hash it; any other bytes are not covered: STOP).
    - COO half (SIGNED @7c9ad9d0f0): org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_GOLD_PACKAGE_THRESHOLDS_FILE_COO_HALF.md
      Its section 2 CORRECTS the packet's stale statements (the live state, the source-map lines, the rollback version): where the packet and that
      section differ, the half's section 2 governs and you re-read each value live anyway.
    - CTO half (SIGNED @c5e183273f): org/missions/D9/IRPT/IRPT_DASHBD/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_GOLD_PACKAGE_THRESHOLDS_FILE_CTO_HALF.md
    Your own REFRESH 4 apply is the precedent: org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_DASHBD.TO-DB-b-164.r45-refresh-4-apply-dell2.md and its record
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_dashbd_r45/R45_REFRESH4_APPLY_RECORD.json (same steps; the differences are below).

    The ONE member that changes (the packet's "The one member that changes", as the half states it today):
    - `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`: from the 24-key blob at `repo_path`
      `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json`, pin `6be02af162eaeff01ca19d2e5b228ffce6091cc7`, sha256
      `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` (live today), to the tracked file at `repo_path`
      `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`, pin `aaeb1866ff6e06b00af7987cfd5849c4fa0e4329`, sha256
      `69e0a889a7e639336d3c01105804e05173ab49528b5882d38cf6aa94a09bad0f` (top-level keys exactly `tolerance`, `large_flow_share`, `plausibility_band_low`,
      `plausibility_band_high`, `comparability_max_excluded_weight`, `threshold_claims`). `packaged_as` does not change.
    - The source-map entry you re-pin: `infra/aws/lambda/ci/lambda-source-map.json`, function `irpt-49f-reporting-gold-lambda`, `staged_from` element for the thresholds
      file; at trunk @67cadd141d its lines are 6091 (`repo_path`), 6092 (`pin`), 6093 (`packaged_as`, unchanged), 6094 (`sha256`). THREE fields change; re-find the lines at the
      base your tree is on.
    The four REFRESH 4 members stay at the pins you applied (recorded in your own REFRESH 4 record): handler.py @080dc90d92542d96817ae79f4f8a72a85dd9de09,
    account_return_daily.py @739dbb240f19b6dd2c08ce982c44c9b7c17ca322, account_activity_lots.py @19ba6fe341da80c906d0a1ff7a0db0253fdd2115, sources.json
    @f043506a7c3f5a7d997e6e4096ba094435e419a5. The criterion's check holds all five pins and compares your record to them.

    The pair's ordering condition is MET and is not yours to re-open: REFRESH 4 was applied 2026-10-12 13:58:42Z and its first scheduled fire (2026-10-13 11:41Z)
    was read CLEAN by the issuer at 12:14Z; ledger `irpt-dashbd-r45-refresh4-20261012` is closed (@db605d794c).
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry with `python .tools/deploy_ledger.py`, pinned to the packet's sha256, and COMMIT it at once (the entry and
       `org/critical_paths/.open_deploys/<slug>.json`), and again after each leg. Add a LEG that stays OPEN for the issuer: the scheduled call site read at the first
       fire after THIS release (the pair's condition 4: the six-key `thresholds` object and its claims `measured`, `measured`, `held`, `held`, `inferred`, with
       `threshold_claims_source` `stated`).
    1. BEFORE reads, each printed: (a) live `get-function-configuration`: CodeSha256 MUST read `i2r7CbVr...` and MemorySize 3008, else STOP; record
       `base_codesha256_before`. (b) Read EVERY live worktree's `.open_deploys/` (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD
       org/critical_paths/.open_deploys/`), union them, print the per-tree denominator; an open entry naming `irpt-49f-reporting-gold-lambda` is a STOP (your own open
       entries and orders on other functions are untouched; this order does not wait on them). (c) Re-read the rollback anchor: the S3 version id of
       `investor-reporting/irpt-reporting-gold-lambda.zip` in the lambda-artifacts bucket that the live function runs (the half read `8ELUDq_d2wRKI0kSXEuLXFm6iqgsiAyZ`,
       content-sha256 equal to the live CodeSha256, on 2026-10-13 12:19Z); record it as `rollback_version_id` as read NOW, and confirm its `content-sha256` metadata equals
       the live CodeSha256.
    2. Re-hash the packet and each of the FIVE pins with `git show <pin>:<path> | sha256sum`; each must equal the values above (record `pins_verified`: {file, pin, sha256,
       equal}, five entries). Any inequality is a STOP before the build.
    3. Build at the base your tree is on, from the pins and not from HEAD, with `infra/aws/lambda/ci/build-and-upload.sh`, BEFORE any upload (BUILD_ONLY first, as in
       REFRESH 4); re-pin the thresholds entry in `infra/aws/lambda/ci/lambda-source-map.json` (three fields). Download the live zip by its S3 version and compare members:
       `upload_member_diff` must be EXACTLY the one path `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json` and every other member must equal live's
       bytes. A second difference is a STOP before upload. Record `build_commit`, `built_codesha256`.
    4. Plan and apply. The targeted plan (`-target=module.irpt_reporting_gold.aws_lambda_function.this`) must read `0 to add, 1 to change, 0 to destroy`; record `plan`.
       Anything else is a STOP. Then ONE `.tools/safe-apply.sh` from the saved plan. Read back `live_codesha256_after`; it must equal `built_codesha256`. Stamp it with
       `record-deploy-scope.py`. A post-apply plan must read `No changes`: record `replan_no_changes`.
    5. THE ONE DRY-RUN INVOKE, immediately after the apply: `irpt-49f-reporting-gold-lambda` with event
       `{"backfill": {"start": "2026-10-08", "end": "2026-10-08"}, "accounts": "population", "dry_run": true}` (the sizing event REFRESH 4 used). Take the REPORT line from
       CloudWatch for the RequestId. Pass lines: Duration under 765,000 ms AND Max Memory Used under 2,556.8 MB. List `irpt/49financial/gold/` in `opal-data-49financial` for
       objects with LastModified at or after the invoke start: expect 0, with the denominator and a positive control as the REFRESH 4 record printed them. Record `dry_run`
       {event, invoke_status_code, invoke_function_error, request_id, report_line, duration_ms, max_memory_mb, written_objects}.
       OVER on either line, a function error, or any object written: ROLL BACK to the REFRESH 4 build the pair's way (copy-object of the recorded version onto the same key,
       re-record the source-map entry to pin `6be02af162` and sha256 `551920f0c364...`, targeted safe-apply; `aws lambda update-function-code` is barred), record `rollback`,
       close the ledger, report. A rollback needs no further word.
    6. Close the ledger's apply legs (the first-fire leg stays OPEN). Write the record and the proof-of-spec instance, validate it with
       `python .tools/proof-of-spec-check.py <instance> DB87-1-AC1` BEFORE you flip this order, then report ONCE to `2.0.0_SA_COO~D2`: the before reads, the pin table, the
       member diff, the plan, the readback, the dry-run REPORT line, the ledger entry, any row id.
  </steps>

  <bounds>
    ONE function, ONE release, ONE changed member. No invoke other than step 5's one. No run of the producer's `main()` with upload. No write of a method row, no rewrite or
    removal of a manifest already served, no S3 delete (the prior zip versions stay; the immediate prior version is the rollback target). No change to IAM, a bucket policy,
    a schedule, a route, memory or timeout (both stay 3008 and 900). No Bloomberg, vendor or Black Diamond call, no secret read. Deletes are Andrew's. No second release on
    this function until the first-fire read after this one closes. The opal-assets terraform hold is lifted (CTO msg 6890) and did not name this root. Safe-apply may print an
    APPLY-WHO line and a HALT-GATE notice: a HALT-GATE that lists notices on the issuer is read, and `HALT_ACK=1` is taken only after you read each notice and none names this
    function or carries a [STOP]. Any divergence the pair does not name is a STOP and a row, not a judgment call.
  </bounds>

  <write_surface>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_dashbd_thresholds/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    infra/aws/lambda/ci/lambda-source-map.json
    infra/aws/lambda/investor-reporting/reporting-gold/
    org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_DASHBD.TO-DB-b-165.thresholds-file-swap-apply-dell2.md
  </write_surface>

<proof_of_spec>
  <criterion id="DB87-1-AC1" cell_refs="DB-b-165"><invocation>python "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r87/p87_round87.py" . DB87-1-AC1</invocation><expect>DB87-1-AC1 PASS</expect></criterion>
</proof_of_spec>
DB87-1-AC1 -- the thresholds-file swap is live over i2r7CbVr with exactly ONE changed member at the packet's pin, plan 0/1/0, live equal to the build, a clean re-plan, and the one dry-run invoke under both 85 percent lines with 0 objects written. The record is `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_dashbd_thresholds/THRESHOLDS_SWAP_APPLY_RECORD.json` with keys packet_sha256, base_codesha256_before, rollback_version_id, pins_verified (five entries), build_commit, built_codesha256, upload_member_diff (exactly the one thresholds path), plan, live_codesha256_after, replan_no_changes, ledger_entry, dry_run, rollback. Base: FAIL (no record). The instance goes at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_dashbd_thresholds/IRPT_DASHBD.TO-DB-b-165.proof_of_spec.json`.

<preflight>
comp-blast: DECLARED-NOT-APPLICABLE the pair's radius names one function and one member; the targeted plan must read 0/1/0 or the act stops
comp-iam: DECLARED-NOT-APPLICABLE no grant, action or role statement changes; the pair reads none
comp-routes: DECLARED-NOT-APPLICABLE no route
comp-schedule: DECLARED-NOT-APPLICABLE the daily schedule is unchanged; the first fire after release is the open ledger leg
comp-cache: DECLARED-NOT-APPLICABLE no CloudFront or cache surface
comp-adversary: DECLARED-NOT-APPLICABLE at the cut; DB87-1-AC1 base: FAIL as expected (no record), the green arm PASS and eight failing arms (over memory, over duration, a two-member diff, a wrong plan, a rollback, a wrong base, a wrong packet, an object written) FAIL on synthetic records
</preflight>

# pipeline-override: an APPLY order to a dell2 cloud-ops seat for one issuer cell (DB-b-165: one targeted release under a signed never-widen pair, applier named by the pair's condition 6); not a worker cell.
</task_order>
