<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-33.estate-report-runner-blob-prefetch-upload-and-qa-run</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~NFRA1</issued_to>
    <date>2026-10-17</date>
    <status>complete -- CTcj1-AC1, AC2, AC3 met: upload 2026-10-17T14:53:25Z (VersionId LwDXDuLu9PZ.WHwKa.XV3Q4MQne9MR8i, sha256 equals the pin); ad-hoc QA run 14:54:45Z-15:13:56Z, log logs/2026-10-17T151354Z-i-0584e17d283fa7ef4.log compile_resources status=ok; manifest/2026-10-17.json status PENDING. Report: deliverables/TO-APPLY-33_REPORT.md</status>
    <project_code>NFRA_CTLPLN</project_code>
    <round>37</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round30.md</decomp_doc> (workstream OUTCOME, round 30, amendment 11): the apply leg of cell `CT-ci-1` (the built cell is `CT-ci-1`, merged @7a33c62148)
<owned_cells>CT-cj-1</owned_cells>
</decomp_ref>

  <preflight>
comp-schedule: RUN -- the scheduler `estate-report-0900et` (ENABLED, `cron(0 9 * * ? *)` America/New_York, target the orchestrator Lambda) is READ and not changed. The next scheduled fire is 2026-10-18 13:00Z. The window rule of step 3 keeps the upload and the QA start off 12:50Z-13:30Z and off an in-flight run.
comp-iam: DECLARED-NOT-APPLICABLE no IAM or policy change: one s3api put-object and one start of the existing instance by the seat's existing CloudOps role, as in ledger 20260909T1352Z and TO-APPLY-32. The seat reads its own grant first and stops if put-object or the start is refused.
comp-adversary: RUN -- the wrong bytes uploaded (read-back sha256 against `git show` at the pin, with a one-byte negative control); a stale rollback (the current object hashed and its VersionId recorded BEFORE the act); an upload while a run is in flight (the window rule and the instance state read first); a QA run that raises on the new code (the stop list: ROLLBACK to the recorded version); the QA run read from a log that is not its own (source file and start time named, the log object name carries the start time and the instance id); the QA run overwriting a manifest of the day (it replaces the FAILED manifest of 2026-10-17 on purpose: the CTO's criterion; the FAILED manifest and log are COPIED to the seat's deliverables folder first); an ad-hoc run read as production evidence (it is not: the CVO re-grades the next SCHEDULED day, 2026-10-18 13:00Z); cost (one full run: the same Kimi calls and about ten minutes of the t3.medium as a scheduled day); BLIND: the batched fetch has never run against GitHub from the runner host; the QA run is its first real exercise.
risk: WORLD -- a deploy of an object the instance pulls at every start, and a run on the runner host; no Terraform, policy or instance-configuration change.
lane: the seat is `0.7.0_AE_CloudOps~NFRA1` (rule 34, one lane per macro per box); NEVER-2 ledger opened first.
  </preflight>

  <precondition>
    The build cell `CT-ci-1` is merged on `box/laptop` @7a33c62148 (the file `infra/aws/ec2/estate-report-runner/estate_report_runner.py` there has sha256 `62b0d74c17fc4eaf24dcfbdce126964cf126d1e618ccd8538acb18bef453100d`; the issuer read it at the merge). Its tests: `ESTATE-PREFETCH arms=14/14 ok=True`, `FOLLOW-READERS arms=31/31 ok=True`, with the prefetch as the measured difference (a bare checkout on a fresh blobless clone failed rc 255). Cause and fix are the CTO's: `org/tier1_exec/1.0.0_SA_CTO/deliverables/RULINGS_PARKED_BUS_ITEMS_20261017_1350Z.md` item 1 (msg 109820). The folder `infra/aws/lambda/ci/function-map/` and `lib/opal_lambda_map.py` are on `origin/CLOUD` (read at the cut by the CTO's measurement; the seat re-reads in step 1).
    Prior state: the object `s3://opal-estate-report/code/estate_report_runner.py` already carries the CT-cg-1 file (uploaded under TO-APPLY-32 at ~00:46Z; its run of 2026-10-17 13:00Z FAILED at 13:03:55Z in `load_function_map`: log `s3://opal-estate-report/logs/2026-10-17T130355Z-i-0584e17d283fa7ef4.log`, manifest `s3://opal-estate-report/manifest/2026-10-17.json` status FAILED).
  </precondition>

  <objective>
    Make the S3 object `s3://opal-estate-report/code/estate_report_runner.py` carry the repo file at the pin `7a33c62148`, then run the runner ONCE on its host as a QA run, so the estate report writes a manifest with a status other than FAILED. This is criteria (b) and (c) of the CTO's ruling: the run's own fresh blobless clone is the clone on the runner host.
    WHY NOW: the report has failed since 13:03:55Z today and fails at every daily run until this lands. The scheduler's next fire is 2026-10-18 13:00Z.
  </objective>

  <context>
    The ONE consumer of the key: `estate-report.service` on the instance named `estate-report-runner` (CURRENT id `i-0584e17d283fa7ef4`, state `stopped` at the cut, read live by Name tag; the id in `EC2_MANIFEST.json` and in TO-APPLY-32 churns with the instance, so look it up by Name tag, never by a typed id). It pulls the key at EVERY service start (`ExecStartPre=/usr/bin/aws s3 cp s3://opal-estate-report/code/estate_report_runner.py ...`, `infra/aws/terraform/estate-report/instance.tf:233`), runs, and the instance self-stops (about 10 minutes on a normal day). `estate-report-orchestrator` (a Lambda) starts the instance on the schedule and never reads the key. ONE task family, no shared tag.
    Method: repeat TO-APPLY-32's steps and the ledger `org/critical_paths/change_management/20260909T1352Z_estate-report-runner-outset-seam-consumer_deploy_completion.md` (ONE `s3api put-object`, the entry committed OPEN before the upload, the legs verified, a comparator proven able to fail).
    What changed in the file (read the diff `git diff bfbdc20d40..7a33c62148 -- infra/aws/ec2/estate-report-runner/estate_report_runner.py`, +55/-6): a helper `checkout_paths` (and `prefetch_blobs`) lists the blob ids of the paths about to be checked out with `git ls-tree -r --object-only`, fetches them in ONE `git fetch --no-tags --filter=blob:none origin <ids>`, then runs the checkout; all three call sites use it. A failed prefetch logs a WARN and the checkout proceeds as before. Read it whole before the upload.
  </context>

  <steps>
    0. NEVER-2: open the ledger entry FIRST, `org/critical_paths/change_management/<UTC>_estate-report-runner-blob-prefetch_deploy_completion.md` plus the `org/critical_paths/.open_deploys/<slug>.json` sentinel, naming the ONE consumer above; commit it OPEN, then act. The entry names the QA run as part of the act.
    1. Pin and bytes: `git show 7a33c62148:infra/aws/ec2/estate-report-runner/estate_report_runner.py` -> a scratch file; its sha256 must read `62b0d74c17fc4eaf24dcfbdce126964cf126d1e618ccd8538acb18bef453100d` (say so if it does not and STOP). Re-read `git ls-tree` of `origin/CLOUD` for `infra/aws/lambda/ci/function-map` and `lib/opal_lambda_map.py` (positive control: a path that must be absent reads absent).
    2. ROLLBACK, recorded BEFORE the act: `s3api head-object` and `list-object-versions` for the key: the CURRENT object's `VersionId`, `LastModified` and sha256 (download the current object and hash it; it should equal the file at `bfbdc20d40`). Also COPY the FAILED `manifest/2026-10-17.json` and the failed run's log to `org/tier2_senior/0.7.0_AE_CloudOps~NFRA1/deliverables/` before the QA run replaces the manifest. The rollback is `put-object` of the recorded bytes (or copy-object of that version).
    3. WINDOW: read the scheduler state and the instance state (by Name tag). The instance must read `stopped`. Do NOT upload or start between 12:50Z and 13:30Z, and not while a run is in flight; say which window you used.
    4. The upload: ONE `s3api put-object` of the scratch file to the key.
    5. READ-BACK: download the object the act wrote; its sha256 must equal the sha256 of the file at the pin (step 1) and its `VersionId` must differ from the rollback's. A comparator proven able to fail: a one-byte-changed copy must read UNEQUAL.
    6. THE QA RUN: start the instance by the route the scheduler uses (read `infra/aws/lambda/estate-report-orchestrator/lambda_function.py` and the scheduler target's input first; invoke the orchestrator with that input, or `ec2 start-instances` on the instance found by Name tag if the orchestrator route is refused), once. Say it is an ad-hoc QA start. Follow the run to its end through `s3://opal-estate-report/logs/` (the newest log object whose name carries this start's UTC time and the instance id) and the instance's self-stop. Do not start a second run.
    7. READ: from that log, the line `STAGE compile_resources kind=deterministic status=<...>` and any `Traceback`/`CalledProcessError`; then `s3://opal-estate-report/manifest/<date>.json` (the date the run wrote): its `status`. Report each with its source object and time.
    8. Close the ledger entry; write a report in `deliverables/`; flip this order.
  </steps>

  <stops>
    STOP and report (do not improvise) if: the folder is absent on `origin/CLOUD`; the sha256 at the pin differs from the expected value; the current object's sha256 is neither the `bfbdc20d40` file's nor explained; an `estate-report` run is in flight or the instance is not `stopped`; the read-back differs; the QA run's log shows a Traceback, a `CalledProcessError`, or `compile_resources status` other than ok. ROLLBACK to the recorded version only if the failure is in the NEW code path (the helper); if the failure is elsewhere (a Kimi timeout, a GitHub error), do not roll back, report the log and the manifest as they stand. Do not start a second run without the issuer's word.
  </stops>

  <proof_of_spec>
    <criterion id="CTcj1-AC1" cell_refs="CT-cj-1"><invocation>aws s3api get-object of s3://opal-estate-report/code/estate_report_runner.py, sha256 of the downloaded bytes against `git show 7a33c62148:infra/aws/ec2/estate-report-runner/estate_report_runner.py`</invocation><expect>equal, with a one-byte-changed negative control reading unequal</expect></criterion>
    <criterion id="CTcj1-AC2" cell_refs="CT-cj-1"><invocation>the log object of the QA run under s3://opal-estate-report/logs/ (name and start time stated), the STAGE compile_resources lines</invocation><expect>STAGE compile_resources kind=deterministic status=ok, and no CalledProcessError in the log</expect></criterion>
    <criterion id="CTcj1-AC3" cell_refs="CT-cj-1"><invocation>aws s3 cp s3://opal-estate-report/manifest/2026-10-17.json - (the date the QA run wrote, stated), the status field</invocation><expect>a status other than FAILED</expect></criterion>
  </proof_of_spec>

  <expected_criteria>CTcj1-AC1,CTcj1-AC2,CTcj1-AC3</expected_criteria>
</task_order>
