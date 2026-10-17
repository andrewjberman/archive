<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-32.estate-report-runner-function-map-upload-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~NFRA1</issued_to>
    <date>2026-10-17</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round30.md</decomp_doc> (workstream OUTCOME, round 30): the apply leg of cell `CT-ch-1` (the built cell is `CT-cg-1`, merged @bfbdc20d40)
<owned_cells>CT-ch-1</owned_cells>
</decomp_ref>

  <preflight>
comp-schedule: RUN -- the scheduler `estate-report-0900et` (ENABLED, cron(0 9 * * ? *) America/New_York) is READ and not changed; the window rule of step 3 keeps the upload off an in-flight run and off 12:50Z-13:30Z.
comp-iam: DECLARED-NOT-APPLICABLE no IAM or policy change: one s3api put-object by the seat's existing CloudOps role to an object the seat has written before (ledger 20260909T1352Z); the seat reads its own grant first and stops if put-object is refused.
comp-adversary: RUN -- a RAISE at the next start fails that day's run (the new runner raises on a missing or empty folder: stop 1 checks the folder on origin/CLOUD; rollback is the recorded prior version); a run in flight read a half-replaced object (S3 PutObject is atomic per key; the window rule anyway); the wrong bytes uploaded (read-back sha256 against `git show` at the pin, with a one-byte negative control); a stale rollback (the current object hashed and its VersionId recorded BEFORE the act); the disarm read taken from a log that is not the next start's (source and time named); BLIND: the lambda hop of the new runner has never run against the live estate until the next start, which is the proof criterion.
risk: WORLD -- a deploy of an object the instance pulls at every start; no Terraform, policy or instance change.
lane: the seat is `0.7.0_AE_CloudOps~NFRA1` (rule 34, seated by 0.0.0_AB_MSTR at 00:33Z, msg 109778); NEVER-2 ledger opened first.
  </preflight>

  <precondition>
    CTO ruling, msg 109774 (1.0.0_SA_CTO, 2026-10-17 ~00:3xZ): YES, one CloudOps order for the PutObject of the CT-cg-1 `estate_report_runner.py`. This is a code-only upload of ONE object; there is NO Terraform change and NO policy change. MET at issue: `infra/aws/lambda/ci/function-map/` (241 files) and `lib/opal_lambda_map.py` are on `origin/CLOUD` (the branch the runner clones), and `lambda-source-map.json` is absent there (read at 00:3xZ: `git ls-tree` on `refs/remotes/origin/CLOUD`).
  </precondition>

  <objective>
    Make the S3 object `s3://opal-estate-report/code/estate_report_runner.py` carry the repo file `infra/aws/ec2/estate-report-runner/estate_report_runner.py` AT THE PIN `bfbdc20d40` (the CT-cg-1 merge), so the deployed runner reads the function folder instead of the retired map.
    WHY NOW: the folder is already on `origin/CLOUD` and the retired map is gone from it, so the DEPLOYED (old) runner's lambda hop reads the retired path, finds nothing and degrades with a WARN at its next start. The scheduler `estate-report-0900et` (ENABLED, `cron(0 9 * * ? *)` America/New_York) starts the run at 13:00Z; the upload should land BEFORE the next start and never while a run is in flight. This disarms row `NFRA_CTLPLN-W151-S2`.
  </objective>

  <context>
    Method: repeat the last estate-report-runner deploy step for step: ledger `org/critical_paths/change_management/20260909T1352Z_estate-report-runner-outset-seam-consumer_deploy_completion.md` (`0.7.0_AE_CloudOps~W`, order `NFRA_OUTSET.TO-OS-s-19`): ONE `s3api put-object`, the entry committed OPEN before the upload, the legs verified, a content diff, a comparator proven able to fail.
    The ONE consumer of the key: `estate-report.service` on `i-0512bd3cbaf602b7f`, which pulls the key at EVERY service start (`ExecStartPre=/usr/bin/aws s3 cp s3://opal-estate-report/code/estate_report_runner.py`, `instance.tf`). `estate-report-orchestrator` never reads the key. ONE task family, no shared tag.
    What changed in the file (read the diff `git diff <the pin of the last deploy>..bfbdc20d40 -- infra/aws/ec2/estate-report-runner/estate_report_runner.py`, 29 lines at CT-cg-1): `load_function_map(repo_dir)` checks out `infra/aws/lambda/ci/function-map` and `lib/opal_lambda_map.py` from the clone's own branch, imports `load_all`, and RAISES when the folder is missing or empty (it no longer degrades to an empty map). Read it whole before the upload: a RAISE at the next start fails that day's run, so the folder on CLOUD is the precondition above.
  </context>

  <steps>
    0. NEVER-2: open the ledger entry FIRST, `org/critical_paths/change_management/<UTC>_estate-report-runner-function-map_deploy_completion.md` plus the `.open_deploys` sentinel, naming the ONE consumer above; commit it OPEN, then upload.
    1. Pin and bytes: `git show bfbdc20d40:infra/aws/ec2/estate-report-runner/estate_report_runner.py` -> a scratch file; record its sha256. Re-read `git ls-tree` of `origin/CLOUD` for the folder and the lib (positive control: a path that must be absent reads absent).
    2. ROLLBACK, recorded BEFORE the act: `s3api head-object` and `list-object-versions` for the key: the CURRENT object's `VersionId`, `LastModified` and sha256 (download the current object and hash it). The rollback is `put-object` of those bytes (or copy-object of that version).
    3. WINDOW: read the scheduler state and the instance/service state; do NOT upload while an `estate-report` run is in flight or between 12:50Z and 13:30Z unless the service is stopped; say which window you used.
    4. The act: ONE `s3api put-object` of the scratch file to the key.
    5. READ-BACK: download the object the act wrote and require its sha256 equal the sha256 of the file at the pin (step 1), and its `VersionId` differs from the rollback's. A comparator proven able to fail (a one-byte-changed copy must read UNEQUAL).
    6. DISARM READ: at the next start of the service after the upload (the scheduled 13:00Z run, or a start by an authorized act if the issuer asks for one), read the run's log: the lambda hop must read `function-map/` with NO WARN about the retired map. That line is the proof that disarms W151-S2; report it with its source and time.
    7. Close the ledger entry; write a report; flip this order.
  </steps>

  <stops>
    STOP and report (do not improvise) if: the folder is absent on `origin/CLOUD`; the current object's sha256 is neither the last ledger's nor explained; an `estate-report` run is in flight; the read-back differs; the next start's log shows the retired path or a RAISE. A RAISE means ROLLBACK to the recorded version and report.
  </stops>

  <proof_of_spec>
    <criterion id="CTch1-AC1" cell_refs="CT-ch-1"><invocation>aws s3api head-object and get-object of s3://opal-estate-report/code/estate_report_runner.py, sha256 of the downloaded bytes against `git show bfbdc20d40:infra/aws/ec2/estate-report-runner/estate_report_runner.py`</invocation><expect>equal, with a one-byte-changed negative control reading unequal</expect></criterion>
    <criterion id="CTch1-AC2" cell_refs="CT-ch-1"><invocation>the run log of the next start of estate-report.service after the upload (source and time named)</invocation><expect>the lambda hop reads function-map/ and prints no WARN naming the retired map</expect></criterion>
  </proof_of_spec>

  <expected_criteria>CTch1-AC1,CTch1-AC2</expected_criteria>
</task_order>
