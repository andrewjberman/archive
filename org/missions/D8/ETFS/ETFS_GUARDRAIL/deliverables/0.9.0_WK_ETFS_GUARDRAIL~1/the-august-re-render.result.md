# ETFS_GUARDRAIL.TO-EG-s-14 -- THE AUGUST RE-RENDER: result

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` | **Branch:** `wk-etfs_guardrail-2-1` (cut from CLOUD @`93264db36c`)
**Ran:** 2026-09-09 23:01Z - 23:30Z | **Order:** `../../task-orders/ETFS_GUARDRAIL.TO-EG-s-14.the-august-re-render.md`
**Ledger:** `org/critical_paths/change_management/20260909T2312Z_etfs-guardrail-eg-s-14-august-rerender_deploy_completion.md` (HELD-SOVEREIGN-GATED)

## CONCLUSION

**The fire was MADE and the run FAILED on the box.** The same monthly orchestrator was invoked by hand with
the schedule's own payload (`{"mode":"run"}`, byte-equal to the live `Target.Input`); it started the reporter
box, the box's SSM render command **exited 1 at module import** -- `ModuleNotFoundError: No module named
'_orion_vendor_asof'` -- the orchestrator took its `status != "Success"` branch, alerted on SNS, and stopped
the box. **Nothing was rendered, nothing was published, no email was sent.**

The served August artifacts are **bit-identical to their pre-invoke state** (5 of 5 ETags and LastModified
unchanged), so the served-output move landed NOTHING and the rollback is a verified no-op. **No S3 object was
deleted at any point.**

`S14-AC1` **FAILS by output** (4 of 7 arms; the battery printed `EGS14-NOT-RERENDERED`, rc=1). The failing
arms are (d) publish, (e) the CloudTrail limb, (f) the send. **The order stays open.** The defect is in code
this order is explicitly forbidden to touch (`NO CODE CHANGE, NO DEPLOY`), so it is a BLOCKING row
(`ETFS_GUARDRAIL-W1-S11`), never a hot fix.

**The 10-01 scheduled fire takes the identical path and will fail identically** unless the renderer's
box-side import is repaired and re-uploaded. That is what this order was cut to find out.

## THE DEFECT, GROUNDED

`data/etfs/scripts/presentation/render_month_end.py:70-76` @`93264db36c` (deployed bytes are BYTE-EQUAL to
repo HEAD -- sha256 `6c3c963e693724be848d55511d81d374cb3fd455dca84513afb62603fd7893f7`, 61699 B, so this is a
SOURCE defect, not a stale deploy):

- module-level import, line 72: `from _orion_vendor_asof import orion_normalize_as_of` after inserting
  `<repo>/data/inf/scripts/silver` -- absent on the box.
- `ImportError` fallback, line 75: inserts `os.path.join(_ORION_HERE, "..", "coverage")` = **`/opt/coverage`**
  on the box, while the coverage package's own self-bootstrap (`:88-109`) pulls to
  `_ORION_HERE/coverage` = **`/opt/etfs-reports/coverage`** -- one directory level apart.
- and that bootstrap runs **after** line 72 anyway, so on a box with no pre-existing `/opt/coverage` the
  import raises before anything can repair it. The orchestrator's `_render_command`
  (`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:196-232`) copies only
  `render_month_end.py` to the box.

The vendored module itself is correct and present on the artifact prefix:
`s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/_orion_vendor_asof.py` sha256
`15d28dd8444455e5d4143dca4c62adea109aeb4b50a3ee4e99af0b54890e6f72` (6979 B) == `git show
HEAD:data/inf/scripts/silver/_orion_vendor_asof.py`. Only the box-side path and ordering are wrong.

**The invoke's own `StatusCode 200` / `{"ok": true}` is NOT a success oracle:** `_run()` returns `None` from
its refusal branch and `handler` returns `{"mode": "run", "ok": True}` regardless
(`lambda_function.py:405-424`, `:513`).

## WHAT WAS MEASURED

### The schedule, read LIVE

`.tools/aws scheduler get-schedule --name etfs-reports-monthly-run` (rc=0):

```
"ScheduleExpression": "cron(0 10 1 * ? *)",
"ScheduleExpressionTimezone": "America/New_York",
"State": "ENABLED",
"Target": { "Arn": "arn:aws:lambda:us-east-1:313476888478:function:etfs-reports-orchestrator",
            "Input": "{\"mode\":\"run\"}",
            "RoleArn": "arn:aws:iam::313476888478:role/etfs-reports-scheduler-role" }
```

### The archive (before the invoke), 5 of 5 byte-equal

`get-bucket-versioning` on `opal-data-etfs` returned an EMPTY document (rc=0) -> versioning NOT enabled ->
`copy-object` archive. Written to `platinum/reports/_archive/2026-08/20260909T230636Z/` (NOT the month
prefix -- row `ETFS_GUARDRAIL-W1-S12`, and the reason is in the ledger entry).

| served key (prior) | bytes | prior sha256 | archive sha256 | equal |
|---|---|---|---|---|
| `platinum/reports/2026-08/etf_ownership.html` | 62477 | `e6b16ef24ae6e997e2b85b3d393d6c60b089b47a4c04e021866ef839c3b3eee5` | same | YES |
| `platinum/reports/2026-08/etf_ownership.pdf` | 273857 | `e85fe6c5028ac860bb245c968f5e6047b50fc1ea0b7b26f71b8854f9383192e8` | same | YES |
| `platinum/reports/2026-08/opaletfs_49financial_202608.csv` | 1952 | `1fba75df7fe50e8b0287c96f2b6be36d9fa8d61ae2f5e0a4f59cbece3e35e3bc` | same | YES |
| `platinum/reports/2026-08/opaletfs_cottonwood_202608.csv` | 1828 | `98fb455c41a3958610a28bb9161ef9f111d012098f0f8862e3050babf6ebda6a` | same | YES |
| `platinum/reports/2026-08/opaletfs_inflection_202608.csv` | 1828 | `f19db318f79821c65144f2996cc2f670b4d47ffcda328c4054ceb666a8296221` | same | YES |

Denominator: 5 of 5 objects under the month prefix archived; 5 of 5 sha256-equal on both sides.

### The invoke

```
.tools/aws lambda invoke --function-name etfs-reports-orchestrator --payload '{"mode":"run"}' \
  --cli-read-timeout 0 --cli-connect-timeout 60 --debug .scratch/invoke_out.json
```

- caller: `arn:aws:iam::313476888478:user/Andrew_Berman` (`sts get-caller-identity`, UserId `AIDAUR7FNW6PEXHN2JIOH`)
- issued `2026-09-09T23:14:43Z`, returned `2026-09-09T23:15:24Z`, CLI rc=0
- response: `{"StatusCode": 200, "ExecutedVersion": "$LATEST"}`; payload `{"mode": "run", "ok": true}`
- `x-amzn-RequestId: 2be062b2-6642-4092-852a-7dc4c0b714b5`
- payload byte-equal to the schedule's `Target.Input`: YES

`--cli-read-timeout 0` was deliberate: the orchestrator is synchronous end to end and a default 60 s client
read timeout would have retried into a SECOND concurrent production run (row `ETFS_GUARDRAIL-W1-S14`).

### The run, on the box

- CloudTrail `StartInstances` `2026-09-09T23:14:48Z` (Username `etfs-reports-orchestrator`)
- SSM command `c935cadb-1e84-473a-a6ca-ab068f89f564`, Comment `ETFS month-end render 2026-08`, requested
  `23:15:09Z`, **Status `Failed`, ResponseCode 1**, output verbatim (tail):

```
Traceback (most recent call last):
  File "/opt/etfs-reports/render_month_end.py", line 72, in <module>
    from _orion_vendor_asof import orion_normalize_as_of
ModuleNotFoundError: No module named '_orion_vendor_asof'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/opt/etfs-reports/render_month_end.py", line 75, in <module>
    from _orion_vendor_asof import orion_normalize_as_of
ModuleNotFoundError: No module named '_orion_vendor_asof'
failed to run commands: exit status 1
```

- CloudTrail `StopInstances` `2026-09-09T23:15:24Z`; box `i-070477bf35fc54409` State.Name `stopped`
- orchestrator log stream `2026/09/09/[$LATEST]ee4d9f0f57b4424183ff917619bf011f`: only
  `INIT_START` / `START RequestId: 2be062b2-...` / `END` / `REPORT ... Duration: 37101.01 ms` -- 4 of 4
  events, zero application lines, zero `MessageId` lines.

### The served objects AFTER (UTC, via `s3api`)

| key | LastModified (UTC) | Size | ETag | changed by the run |
|---|---|---|---|---|
| `platinum/reports/2026-08/etf_ownership.html` | 2026-09-01T17:38:41Z | 62477 | `f3e43b3c72dc0d2753099d5e9c0181c4` | NO |
| `platinum/reports/2026-08/etf_ownership.pdf` | 2026-09-01T17:38:41Z | 273857 | `75989bf5f70e28f0ddae900a0a253ee3` | NO |
| `platinum/reports/2026-08/opaletfs_49financial_202608.csv` | 2026-09-01T17:38:42Z | 1952 | `1554f4a27e6959f291b3c3cf0470232c` | NO |
| `platinum/reports/2026-08/opaletfs_cottonwood_202608.csv` | 2026-09-01T17:38:42Z | 1828 | `175a3681daff17b0d5d1da7db680f4de` | NO |
| `platinum/reports/2026-08/opaletfs_inflection_202608.csv` | 2026-09-01T17:38:42Z | 1828 | `b6a2f9a1f31f1cb483b1b06315f2bd63` | NO |

Denominator: 5 of 5; no `coverage_verdict.json`, no `coverage_unresolved.json`, no `refused/` prefix was
written (the gate never ran -- the process died before `main()`).

### The SEND

0 SES `MessageId` lines in the run's log; 0 CloudTrail `SendRawEmail` events in the window. Reached-code
reason: `_email_report` is only called after `status == "Success"` and `_report_exists`. The JOIN itself is
deployed and correct -- live `EMAIL_RECIPIENT` = `aj@opalinvest.com,andrew@opalinvest.com`
(`get-function-configuration`), which `EMAIL_RECIPIENTS` splits for both envelopes.

### `_last_month()` on the invoke day

```
_last_month() (imported from infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py) = 2026-08
_report_keys(2026-08) = ('platinum/reports/2026-08/etf_ownership.pdf',
                         'platinum/reports/2026-08/etf_ownership.html')
```

Trading days in 2026-08 per `lib/trading_calendar.py` (NYSE/pandas_market_calendars): **21**
(2026-08-03 .. 2026-08-31). The denominator the coverage line would have carried.

### TOLD APART

CloudTrail `Invoke` in the run's window: **0 events** -- and that is an INSTRUMENT ABSENCE, not evidence:
`get-event-selectors` on both trails (2 of 2) shows **no `AWS::Lambda::Function` data resource**
(`opal-organization-trail`: management + S3 ReadOnly data on `opal-data-bd/`, `opal-data-inf/`;
`opal-served-key-write-trail`: S3 write data under `opal-data-{inf,bd,cot}/platinum/firm/`). Positive
control in the same window with the same command shape: `StartInstances` = 1 event, `StopInstances` = 1
event. Substitute oracle, printed but not scored as the named one: the client's `x-amzn-RequestId` from the
launching seat's user appears as the log's `START RequestId`, and the scheduler role cannot have fired it
(`cron(0 10 1 * ? *)`, next fire 2026-10-01). Row `ETFS_GUARDRAIL-W1-S13`.

`ARTIFACT-CARRIES-NO-TRIGGER-FIELD` -- printed by the battery; row `ETFS_GUARDRAIL-W1-S15`.

## CRITERIA

### S14-AC1 -- FAIL by output

`timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs14_august_rerender.py`
-> rc=1, deciding lines verbatim:

```
ARM a   PASS ledger .../20260909T2312Z_etfs-guardrail-eg-s-14-august-rerender_deploy_completion.md opened_at=2026-09-09T23:12:34.653323+00:00 < invoke 2026-09-09T23:14:43Z -> True; served keys named 5 of 5; prior sha256 named 5 of 5; rollback=True; signoffs COO 4155c85a1f + CTO 94775 -> True
ARM b   PASS State ENABLED=True; cron(0 10 1 * ? *)=True; America/New_York=True; Target.Arn == orchestrator=True; Target.Input {"mode":"run"}=True; payload byte-equal=True; StatusCode 200=True; request id present=True (8 of 8)
ARM c   PASS _last_month() ... = 2026-08
ARM d   FAIL published-after-invoke 0 of 5; CSV last row '# coverage:' 0 of 3; archive sha256 match 5 of 5
ARM e   FAIL CloudTrail Invoke events=0 (data-event selector on Lambda: none on either trail -- positive control StartInstances=1 proves the window is logged); recorded request id 2be062b2-6642-4092-852a-7dc4c0b714b5 present as START RequestId in /aws/lambda/etfs-reports-orchestrator -> True
ARM f   FAIL SES MessageId(s) in the orchestrator log for this run: 0; CloudTrail SendRawEmail in the run's minute: 0; Destinations must name aj@opalinvest.com + andrew@opalinvest.com
ARM g   PASS reporter box i-070477bf35fc54409 State.Name=stopped (describe-instances)
ARMS 4 of 7 PASS
EGS14-NOT-RERENDERED -- failing arms: d, e, f
```

Denominator: 7 of 7 arms evaluated, 4 PASS / 3 FAIL. The expected token `EGS14-AUGUST-RERENDERED` was NOT
printed.

### S14-AC2 -- JUDGMENT, graded by the CVO at L9. Evidence, no verdict.

- **FWD-6 alignment on the LIVE render:** NOT OBSERVABLE this turn -- no render occurred. The alignment code
  is present in the deployed renderer (`_align_inflection_series`, `ORION_ALIGNMENT_CUTOVER = "2026-09"`,
  `render_month_end.py:79` @`93264db36c`), and its cutover means 2026-08 renders exactly as before in any
  case (EG-s-13's forward-only qualifier). The import that crashed is the alignment module's own
  (`_orion_vendor_asof`), so the alignment is the very seam the failure sits on.
- **Served CSV before vs after:** identical. Both reads (23:06Z and 23:25Z) return 5-row CSVs ending on
  `PFOE,...` numeric rows; sha256 unchanged on all three. The coverage line was NOT added -- there is no
  diff to print, and that IS the finding.
- **What the run wrote beyond the three publish keys:** nothing. `coverage_verdict.json` and
  `coverage_unresolved.json` are absent from `platinum/reports/2026-08/` (5 of 5 objects listed, all
  pre-existing). The only new objects in the bucket this turn are the 5 archive copies written by this
  worker under `platinum/reports/_archive/2026-08/20260909T230636Z/`.
- **The one thing this order cannot see:** delivery at the two inboxes -- the issuer's read. There is
  nothing to read: 0 sends occurred. Any message in either inbox dated 2026-09-09 for month 2026-08 would
  NOT be from this run.
- **Vintage:** every path cited at `93264db36c`; every AWS read 2026-09-09 23:01Z-23:30Z.

### A note on the battery's four runs

The battery ran four times: 23:25:23Z and 23:25:51Z, then 23:35Z, then 23:39Z. Runs 1, 2 and 4 are identical
line for line. Run 3's arm (a) fell to FAIL (`served keys named 1 of 5; rollback=False`) because
`.tools/deploy_ledger.py` had REGENERATED the change-management entry from its sentinel during the
`close-leg`/`hold` calls, deleting the NEVER-2 section the criterion grades (`_write_entry` ->
`write_text(_render_entry(state))`, `deploy_ledger.py:239,289-291` @`93264db36c`). The section was
re-appended after the last ledger mutation and arm (a) reads PASS again. That is row
`ETFS_GUARDRAIL-W1-S16`, and the evidence quoted under S14-AC1 above is run 4.

## ROWS FILED

| id | class | hazard | subject |
|---|---|---|---|
| `ETFS_GUARDRAIL-W1-S11` | BLOCKING | ARMED (`2.0.0_SA_COO`) | the deployed renderer cannot import `_orion_vendor_asof` on the box; the 10-01 fire fails identically |
| `ETFS_GUARDRAIL-W1-S12` | OBSERVATION | ARMED (`2.0.0_SA_COO`) | the order's archive location sits inside the prefix the email enumerates; archive relocated |
| `ETFS_GUARDRAIL-W1-S13` | OBSERVATION | INERT | no trail captures Lambda data events, so AC1(e)'s CloudTrail limb cannot return a row |
| `ETFS_GUARDRAIL-W1-S14` | OBSERVATION | ARMED (`2.0.0_SA_COO`) | the invoke is synchronous, not "returns in seconds"; a default CLI timeout would double-fire |
| `ETFS_GUARDRAIL-W1-S15` | OBSERVATION | INERT | `ARTIFACT-CARRIES-NO-TRIGGER-FIELD` (the criterion's own required output) |
| `ETFS_GUARDRAIL-W1-S16` | OBSERVATION | ARMED (`2.0.0_SA_COO`) | `deploy_ledger.py` regenerates the entry from the sentinel on every `close-leg`/`hold`, silently deleting the hand-added NEVER-2 section arm (a) grades |

## WHAT WAS NOT DONE, AND WHY

- **No fix, no deploy, no `update-function-code`, no `terraform apply`** -- the order grants no code path and
  forbids both. The renderer repair belongs to the issuer's next cut.
- **No rollback executed** -- measured unnecessary: 5 of 5 served objects are bit-identical to their
  pre-invoke state. The rollback recipe stays written in the ledger entry.
- **Nothing deleted** -- no S3 delete of any kind (NEVER-AUTO-DELETE); the archive copies stay.
- **No re-invoke** -- a second fire would take the identical failing path and produce a second SNS alert; the
  discriminator (the box's import) is unchanged until a deploy lands.
- **No inbox read, no message sent** -- a worker holds no mailbox instrument and cannot send.
- **No trail, selector, alarm, topic or monitor created** -- moratorium, and out of `<paths>`.
- **No `<status>` flip** -- S14-AC1 FAILS by output, so the order stays open (a VALID instance is not a met
  order).
