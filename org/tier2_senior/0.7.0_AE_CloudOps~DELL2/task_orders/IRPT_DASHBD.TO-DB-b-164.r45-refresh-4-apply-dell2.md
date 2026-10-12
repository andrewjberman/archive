<task_order>
  <metadata>
    <id>IRPT_DASHBD.TO-DB-b-164.r45-refresh-4-apply-dell2</id>
    <issued_by>2.0.0_SA_COO~D2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>IRPT_DASHBD</project_code>
  </metadata>
<risk>WORLD</risk>
<round>86</round>
<workstream>B</workstream>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP.md</decomp_doc> section 88 (round 86), issuer cell `DB-b-164`, FWD-4.
<owned_cells>DB-b-164</owned_cells>
</decomp_ref>

  <objective>
    Apply R45 REFRESH 4: ONE gold Lambda release of `irpt-49f-reporting-gold-lambda` over live `oNgy4rnr` (CodeSha256
    `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=`, MemorySize 3008), built from the packet's FOUR pins, by ONE targeted
    `.tools/safe-apply.sh`; then ONE dry-run invoke, read against the 85 percent lines. You are the applier the pair names (its
    condition 6: an AE seat, not a worker).
  </objective>

  <context>
    READ ALL THREE FILES WHOLE BEFORE STEP 0, the files and not this restatement, and say so in the ledger's opening entry:
    - Packet: org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~110/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_4.md, sha256
      `04cf16cd48161a931f5e5da740e60562ec9505d58c154a467375d12c6415ad72` (re-hash it; any other bytes are not covered: STOP).
    - COO half (SIGNED @598347202e): org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_R45_RELEASE_REFRESH4_COO_HALF.md
    - CTO half (SIGNED @e969a090cc): org/missions/D9/IRPT/IRPT_DASHBD/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R45_RELEASE_REFRESH4_CTO_HALF.md
    The R44 apply is your procedure's precedent: org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-95.r44-release-apply.md and its
    record org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~70/R44_APPLY_RECORD.json (read steps 3 and 4 there).

    The four members (repo path, pin, sha256 at the pin) are the packet's "Members" table; the criterion's check holds the same four and
    compares your record to them:
    - infra/aws/lambda/investor-reporting/reporting-gold/handler.py @080dc90d92542d96817ae79f4f8a72a85dd9de09
    - data/assets/scripts/gold/irpt_reporting/account_return_daily.py @739dbb240f19b6dd2c08ce982c44c9b7c17ca322
    - data/assets/scripts/gold/irpt_reporting/account_activity_lots.py @19ba6fe341da80c906d0a1ff7a0db0253fdd2115
    - data/assets/scripts/gold/irpt_reporting/sources.json @f043506a7c3f5a7d997e6e4096ba094435e419a5
    The thresholds file in the package stays the PINNED blob (`551920f0c364...`, option A of the packet's question 5).

    The pair's condition 3 is MET and is not yours to re-open: Monday 2026-10-12's scheduled fire ran on `oNgy4rnr` at 11:41Z, 318.1 s
    (line 765 s) and 1,607 MB Max Memory Used (line 2,556.8 MB), CloudWatch REPORT in log stream `2026/10/12/[$LATEST]b6c1d562c86a4bf18a5b8f6b425d2927`,
    read by the issuer at 13:18Z (row IRPT_DASHBD-D2-W78-S1's acceptance read; the closing row is the issuer's).
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry with `python .tools/deploy_ledger.py`, pinned to the packet's sha256, and COMMIT it at once (the entry
       and `org/critical_paths/.open_deploys/<slug>.json`), and again after each leg. Add a LEG that stays OPEN for the issuer: the
       scheduled call site read at the first fire after release (the pair's condition 4).
    1. BEFORE reads, each printed: (a) live `get-function-configuration`: CodeSha256 MUST read `oNgy4rnr...` and MemorySize 3008, else STOP;
       record `base_codesha256_before`. (b) Read EVERY live worktree's `.open_deploys/` (`git worktree list --porcelain`, then
       `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator; an open
       entry naming `irpt-49f-reporting-gold-lambda` is a STOP. (c) Re-read the rollback anchor: the S3 version id of
       `investor-reporting/irpt-reporting-gold-lambda.zip` in the lambda-artifacts bucket that the live function runs (the packet's value,
       `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`, was last read 2026-10-11T15:10Z); record it as `rollback_version_id` as read NOW.
    2. Re-hash the packet and each of the four pins with `git show <pin>:<path> | sha256sum`; each must equal the table above (record
       `pins_verified`: {file, pin, sha256, equal}). Any inequality is a STOP before the build.
    3. Build at the base your tree is on, from the four pins and not from HEAD, with `infra/aws/lambda/ci/build-and-upload.sh`, BEFORE any
       upload; re-pin the three members in `infra/aws/lambda/ci/lambda-source-map.json` (handler.py rides at its source-map pin). Download
       the live zip by its S3 version and compare members: `upload_member_diff` must be EXACTLY the four member paths above and every
       other member must equal live's bytes. A fifth difference is a STOP before upload. Record `build_commit`, `built_codesha256`.
    4. Plan and apply. The targeted plan (`-target=module.irpt_reporting_gold.aws_lambda_function.this`) must read `0 to add, 1 to change,
       0 to destroy`; record `plan`. Anything else is a STOP. Then ONE `.tools/safe-apply.sh` from the saved plan. Read back
       `live_codesha256_after`; it must equal `built_codesha256`. Stamp it with `record-deploy-scope.py`. A post-apply plan must read
       `No changes`: record `replan_no_changes`.
    5. THE ONE DRY-RUN INVOKE, immediately after the apply: `irpt-49f-reporting-gold-lambda` with event
       `{"backfill": {"start": "2026-10-08", "end": "2026-10-08"}, "accounts": "population", "dry_run": true}` (the R44 sizing event,
       `0.9.0_WK_IRPT_DASHBD~78/R44_SIZING_DRYRUN.json`). Take the REPORT line from CloudWatch for the RequestId. Pass lines: Duration
       under 765,000 ms AND Max Memory Used under 2,556.8 MB. List `irpt/49financial/gold/` in `opal-data-49financial` for objects with
       LastModified at or after the invoke start: expect 0, with the denominator and a positive control as the R44 record printed them.
       Record `dry_run` {event, invoke_status_code, invoke_function_error, request_id, report_line, duration_ms, max_memory_mb,
       written_objects}.
       OVER on either line, a function error, or any object written: ROLL BACK to `oNgy4rnr` the pair's way (copy-object of the recorded
       version onto the same key, re-record the source-map entry, targeted safe-apply; `aws lambda update-function-code` is barred),
       record `rollback`, close the ledger, report. A rollback needs no further word.
    6. Close the ledger's apply legs (the first-fire leg stays OPEN). Write the record and the proof-of-spec instance, validate it with
       `python .tools/proof-of-spec-check.py <instance> DB86-1-AC1` BEFORE you flip this order, then report ONCE to `2.0.0_SA_COO~D2`:
       the before reads, the pin table, the member diff, the plan, the readback, the dry-run REPORT line, the ledger entry, any row id.
  </steps>

  <bounds>
    ONE function, ONE release. No invoke other than step 5's one. No run of the producer's `main()` with upload. No write of a method row,
    no rewrite or removal of a manifest already served, no S3 delete. No change to IAM, a bucket policy, a schedule, a route, memory or
    timeout (both stay 3008 and 900). No Bloomberg, vendor or Black Diamond call, no secret read. Deletes are Andrew's.
    Safe-apply may print an APPLY-WHO line and a HALT-GATE notice: a HALT-GATE that lists notices on the issuer is read, and
    `HALT_ACK=1` is taken only after you read each notice and none names this function or carries a [STOP] (row IRPT_DASHBD-D2-W87-S1).
    Any divergence the pair does not name is a STOP and a row, not a judgment call.
  </bounds>

  <write_surface>
    org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_dashbd_r45/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    infra/aws/lambda/ci/lambda-source-map.json
    infra/aws/lambda/investor-reporting/reporting-gold/
    org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md
    org/tier2_senior/0.7.0_AE_CloudOps~DELL2/task_orders/IRPT_DASHBD.TO-DB-b-164.r45-refresh-4-apply-dell2.md
  </write_surface>

<proof_of_spec>
  <criterion id="DB86-1-AC1" cell_refs="DB-b-164"><invocation>python "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r86/p86_round86.py" . DB86-1-AC1</invocation><expect>DB86-1-AC1 PASS</expect></criterion>
</proof_of_spec>
DB86-1-AC1 -- the R45 REFRESH 4 release is live over oNgy4rnr with exactly the four members at the packet's pins, plan 0/1/0, live equal to the build, a clean re-plan, and the one dry-run invoke under both 85 percent lines with 0 objects written. The record is `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_dashbd_r45/R45_REFRESH4_APPLY_RECORD.json` with keys packet_sha256, base_codesha256_before, rollback_version_id, pins_verified, build_commit, built_codesha256, upload_member_diff, plan, live_codesha256_after, replan_no_changes, ledger_entry, dry_run, rollback. Base: FAIL (no record). The instance goes at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_dashbd_r45/IRPT_DASHBD.TO-DB-b-164.proof_of_spec.json`.

<preflight>
comp-blast: DECLARED-NOT-APPLICABLE the pair's radius names one function and four members; the targeted plan must read 0/1/0 or the act stops
comp-iam: DECLARED-NOT-APPLICABLE no grant, action or role statement changes; the pair reads none
comp-routes: DECLARED-NOT-APPLICABLE no route
comp-schedule: DECLARED-NOT-APPLICABLE the daily schedule is unchanged; the first fire after release is the open ledger leg
comp-cache: DECLARED-NOT-APPLICABLE no CloudFront or cache surface
comp-adversary: DECLARED-NOT-APPLICABLE at the cut; DB86-1-AC1 base: FAIL as expected (no record), green arm PASS and over-memory arm FAIL on synthetic records
</preflight>

# pipeline-override: an APPLY order to the dell2 cloud-ops seat for one issuer cell (DB-b-164: one targeted release under a signed never-widen pair, applier named by the pair's condition 6); not a worker cell.
</task_order>
