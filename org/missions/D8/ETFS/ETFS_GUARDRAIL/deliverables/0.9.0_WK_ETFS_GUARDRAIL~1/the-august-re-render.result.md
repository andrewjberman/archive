# ETFS_GUARDRAIL.TO-EG-s-14 -- THE AUGUST RE-RENDER: result

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` | **Branch:** `wk-etfs_guardrail-2-1`
**Ran:** 2026-09-09 23:01Z - 2026-09-10 00:50Z (two fires: the failed first, then the amended re-run)
**Order:** `../../task-orders/ETFS_GUARDRAIL.TO-EG-s-14.the-august-re-render.md` @`5507841f04` (AMENDED)
**Ledger:** `org/critical_paths/change_management/20260909T2312Z_etfs-guardrail-eg-s-14-august-rerender_deploy_completion.md` -- **CLOSED, all 8 legs proven**

## CONCLUSION

**The August report IS re-published to the served key WITH the coverage line, and the report WAS
sent.** The manual fire of the monthly orchestrator now does end to end what the 10-01 schedule
will do: box up, render with `--gate`, publish PDF/HTML/CSV, SES-send to the joined recipients,
box down.

It took two fires. **Fire 1 (2026-09-09T23:14:43Z) FAILED on the box** -- `ModuleNotFoundError: No
module named '_orion_vendor_asof'` -- published nothing, and is kept below verbatim: that failure
is the manual-trigger rule doing its job, because the 10-01 fire would have failed identically.
The issuer's amendment granted one code change; it was made, gated, rehearsed against the box
layout, committed (`0c8bdbe`) and deployed (`00:16:35Z`, DEPLOYED == BUILT on two instruments).
**Fire 2 (2026-09-10T00:22:57Z -> 00:24:57Z) SUCCEEDED**: SSM `Success`, 5 of 5 served keys
rewritten, `# coverage: 21/21 trading days; 0 carried for missing data` on 3 of 3 CSVs, gate verdict
`PUBLISH`, box `stopped`.

**`S14-AC1` still FAILS by output -- 6 of 7 arms, `EGS14-NOT-RERENDERED`, rc=1 -- on arm (f) alone.**
Arm (f) names two instruments that cannot show a send in this estate: the deployed handler prints
NOTHING on the success path (no `MessageId` is ever logged) and no CloudTrail trail captures SES
calls -- the same COVERAGE-ABSENT class the amendment already ruled for `lambda:Invoke`. The send
itself is evidenced by two other instruments (SES's own counter, +2 delivery attempts = one message
to two destinations; and the alert topic at 0 publishes with a live positive control of 1 in the
failed fire's window). **The `<status>` is NOT flipped** -- a worker cannot re-cut its own criterion.
Row `ETFS_GUARDRAIL-W1-S18` carries the exact re-cut the issuer would need.

## FIRE 1 -- THE FAILED FIRST FIRE (kept verbatim)

- Invoke `2026-09-09T23:14:43Z -> 23:15:24Z`, `StatusCode 200`, request id
  `2be062b2-6642-4092-852a-7dc4c0b714b5`, payload out `{"mode": "run", "ok": true}`.
- SSM `c935cadb-1e84-473a-a6ca-ab068f89f564` ("ETFS month-end render 2026-08", 23:15:09Z)
  **Status `Failed`, ResponseCode 1**:

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

- Published NOTHING (5 of 5 served objects unchanged afterwards); box stopped 23:15:24Z; the
  `etfs-reports-alerts` topic published **1** message in that window (the fail-loud alert fired).
- **The invoke's own `StatusCode 200` / `{"ok": true}` is not a success oracle**: `_run()` returns
  `None` from its refusal branch and `handler` returns `ok: true` regardless
  (`lambda_function.py:405-424`, `:513`).

## THE ONE CODE CHANGE (row W1-S11), ITS PROOF AND ITS DEPLOY

`data/etfs/scripts/presentation/render_month_end.py`, `except ImportError` branch only -- commit
`0c8bdbe`, 20 insertions / 1 deletion against `4155c85a1f`:

- resolve `os.path.join(_ORION_HERE, "coverage")` (the SIBLING of the renderer) instead of `".."`;
- when `_orion_vendor_asof.py` is absent there, pull exactly
  `s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/_orion_vendor_asof.py` into it
  (`check=True`, the EG-s-6 self-bootstrap shape), then import.
- The primary repo-checkout import and `ORION_ALIGNMENT_CUTOVER` are untouched.

**Local proof, before the deploy.** `python -m py_compile` rc 0; `bash .tools/commit-gate.sh
data/etfs/scripts/presentation/render_month_end.py` rc 0 ("pre-commit gate clean for 1 of 1
file(s)"). Box-layout rehearsal (`.scratch/box_layout_rehearsal.py`, no network), verbatim:

```
BOX-LAYOUT REHEARSAL (no network; scratch only)
  renderer at        : ...\.scratch\rehearsal\root\x\y\etfs-reports\render_month_end.py
  coverage/ beside it: ...\coverage (5 file(s))
  computed repo root : C:\tmp\wk-etfs-2-1\.scratch\rehearsal
  data/inf above it  : False (must be False)
  PRIMARY import target absent: True
ARM-A (vendored file PRESENT, no stub on PATH) rc=0
  usage: render_month_end.py [-h] --month MONTH [--out OUT] ...
ARM-B setup: removed ...\coverage\_orion_vendor_asof.py (exists=False)
ARM-B (vendored file ABSENT, stub aws FIRST on PATH) rc=0
  STUB-AWS: copied fixture -> ...\coverage\_orion_vendor_asof.py
  RECORDED ARGV: aws s3 cp s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/_orion_vendor_asof.py ...\coverage\_orion_vendor_asof.py
  exact key in argv: True | destination is <renderer dir>/coverage/: True | file present after: True
REHEARSAL 2 of 2 arms PASS
EGS14-FIX-REHEARSAL-OK
```

**Negative control** (does the harness detect the defect?): the PRE-FIX file
(`git show 4155c85a1f:<path>`) in the SAME layout exits **rc=1** with the identical
`ModuleNotFoundError` -- so ARM-A's pass is a measurement, not a tautology.

**The deploy** (leg L6 of the same NEVER-2 entry; the README's own path,
`infra/aws/terraform/etfs-reports/README.md:99-105` -- "A RE-UPLOAD IS THE WHOLE DEPLOY"):

| | value |
|---|---|
| uploaded | `2026-09-10T00:16:35Z`, `.tools/aws s3 cp` rc 0 |
| head-object after | ContentLength **62880**, ETag `545afb2105518af0bc1c1b6bdb4c7ba5` |
| `aws s3 cp <key> -` \| sha256 | `55701125e86740f3bf51a715aba8f68e8441d3eb7bffc99a43b7d3ff29b973e9` |
| `s3api get-object` \| sha256 (2nd instrument) | the same |
| committed blob `git show HEAD:<path>` | the same -> **DEPLOYED == BUILT** |
| prior deployed (ROLLBACK target) | `6c3c963e693724be848d55511d81d374cb3fd455dca84513afb62603fd7893f7`, 61699 B, `2026-09-05T06:52:22Z` |

Byte checks on the deployed copy: it carries `os.path.join(_ORION_HERE, "coverage")` and no longer
carries `_ORION_HERE, "..", "coverage"`.

## FIRE 2 -- THE RE-INVOKE THAT LANDED

- `.tools/aws lambda invoke --function-name etfs-reports-orchestrator --payload '{"mode":"run"}'
  --cli-read-timeout 0 --cli-connect-timeout 60` (the flags are the amended bound, row W1-S14 --
  the call is synchronous end to end and a 60 s client timeout would retry into a second production
  run).
- Issued `2026-09-10T00:22:57Z` by `arn:aws:iam::313476888478:user/Andrew_Berman`, returned
  `00:24:57Z`, rc 0, `StatusCode 200`, `ExecutedVersion $LATEST`, request id
  `a027eeb0-e954-4dde-9c4f-1d91cad77f67`, Duration 113175.04 ms.
- SSM `faaae9a5-beb1-4214-8981-5d5d2858f0e0` **Status `Success`**.
- Box: CloudTrail `StartInstances` 00:23:06Z, `StopInstances` 00:24:57Z (both by
  `etfs-reports-orchestrator`); `describe-instances` -> `stopped`.

### The served objects AFTER (UTC via `s3api`), 6 of 6 listed

| key | LastModified (UTC) | Size | ETag |
|---|---|---|---|
| `coverage_verdict.json` (NEW key) | 2026-09-10T00:24:44Z | 1225 | `6d13a29621407b94c876b9a60677ea4b` |
| `etf_ownership.html` | 2026-09-10T00:24:47Z | 43376 | `5364844c7c743e46ead35b3630254845` |
| `etf_ownership.pdf` | 2026-09-10T00:24:48Z | 252393 | `d8d786db4be630c3f1d4bfb0420496f4` |
| `opaletfs_49financial_202608.csv` | 2026-09-10T00:24:48Z | 2012 | `d993f70bab48f40ada219a5f0e8c15a5` |
| `opaletfs_inflection_202608.csv` | 2026-09-10T00:24:49Z | 1888 | `3ff4a7dc9de75e0fc9ca0b540ba7fb74` |
| `opaletfs_cottonwood_202608.csv` | 2026-09-10T00:24:50Z | 1888 | `9662cb0d35de5d4baf4d56262c25f2b9` |

5 of 5 publish keys LastModified AFTER the invoke. No `coverage_unresolved.json`, no `refused/`.

### The coverage line, on the SERVED artifact (FWD-3)

3 of 3 CSVs end on `# coverage: 21/21 trading days; 0 carried for missing data`, and **21** is the
month's trading-day count from `lib/trading_calendar.py` (NYSE, 2026-08-03..2026-08-31).
`coverage_verdict.json`: verdict `PUBLISH`, holes 0, 21/21 for all three partners.

### The archives (both), 10 of 10 byte-equal

| prior served key | prior sha256 | archive 1 (23:06:36Z) | archive 2 (00:20:02Z) |
|---|---|---|---|
| `etf_ownership.html` | `e6b16ef24ae6e997e2b85b3d393d6c60b089b47a4c04e021866ef839c3b3eee5` | YES | YES |
| `etf_ownership.pdf` | `e85fe6c5028ac860bb245c968f5e6047b50fc1ea0b7b26f71b8854f9383192e8` | YES | YES |
| `opaletfs_49financial_202608.csv` | `1fba75df7fe50e8b0287c96f2b6be36d9fa8d61ae2f5e0a4f59cbece3e35e3bc` | YES | YES |
| `opaletfs_cottonwood_202608.csv` | `98fb455c41a3958610a28bb9161ef9f111d012098f0f8862e3050babf6ebda6a` | YES | YES |
| `opaletfs_inflection_202608.csv` | `f19db318f79821c65144f2996cc2f670b4d47ffcda328c4054ceb666a8296221` | YES | YES |

Archive 2 was taken immediately before the re-invoke; the served ETags matched the pre-archive-1
read 5 of 5 first, so both archives hold the same prior bytes. Nothing deleted, ever.

### TOLD APART (the amended arm (e))

- Log group read **BY TIME** (`filter-log-events`, 00:20:57Z -> 00:29:57Z): 4 events, and
  `START RequestId: a027eeb0-e954-4dde-9c4f-1d91cad77f67` appears **1 of 1** time -- the client's own
  request id, so the fire is the launching seat's by construction, and exactly one execution ran.
- `etfs-reports-scheduler-role` `AssumeRole` in the window: **0** of 28 AssumeRole events scanned --
  the rule did not fire (its next fire is 2026-10-01 10:00 ET).
- `COVERAGE-ABSENT: 0 of 2 trails select AWS::Lambda::Function` (CloudTrail `Invoke` returned 0 --
  neither a pass nor a fail), with the same-window positive control: management events = 2.
- `ARTIFACT-CARRIES-NO-TRIGGER-FIELD` (row `ETFS_GUARDRAIL-W1-S15`).

### The SEND -- what the named instruments show, and what actually measured it

| instrument | result |
|---|---|
| `MessageId` lines in the run's log | **0** -- and 0 of 0 possible: the handler prints nothing on the success path |
| CloudTrail `SendRawEmail` in the window | **0** -- no trail selects the SES data plane (COVERAGE-ABSENT) |
| SES `get-send-statistics` | total DeliveryAttempts **80 -> 82** across the run; the run's data point carries **attempts=2** -- one `send_raw_email` to TWO destinations |
| `etfs-reports-alerts` `NumberOfMessagesPublished` | **0** in the run window vs **1** in the FAILED fire's window (23:15:00Z) -- every failure branch publishes there, so 0 beside that positive control says the send did not fail |
| live `EMAIL_RECIPIENT` | `aj@opalinvest.com,andrew@opalinvest.com` (the JOIN, split into both envelopes by `EMAIL_RECIPIENTS`) |

**Stated limit:** `get-send-statistics` is account-wide, so +2 in a 15-minute bucket is consistent
with -- not exclusive to -- this send; the exclusive discriminator is the alert-absence with its
positive control plus the code path. Delivery AT the two inboxes stays the issuer's read.

## CRITERIA

### S14-AC1 -- FAIL by output (6 of 7 arms)

`timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs14_august_rerender.py`
-> rc=1:

```
ARM a   PASS ledger .../20260909T2312Z_etfs-guardrail-eg-s-14-august-rerender_deploy_completion.md opened_at=2026-09-09T23:12:34.653323+00:00 < invoke 2026-09-10T00:22:57Z -> True; served keys named 5 of 5; prior sha256 named 5 of 5; rollback=True; signoffs COO 4155c85a1f + 5507841f04 and CTO 94775 -> 3 of 3
ARM b   PASS State ENABLED=True; cron(0 10 1 * ? *)=True; America/New_York=True; Target.Arn == orchestrator=True; Target.Input {"mode":"run"}=True; payload byte-equal=True; StatusCode 200=True; request id present=True (8 of 8)
ARM c   PASS _last_month() ... = 2026-08
ARM d   PASS published-after-invoke 5 of 5; CSV last row '# coverage:' with the /21 denominator 3 of 3; archive sha256 match 10 of 10 (two archives)
ARM e   PASS manual fire pinned: START RequestId a027eeb0-... appears 1 of 1 time(s) in the log group read BY TIME; etfs-reports-scheduler-role AssumeRole in the window = 0 (rule did not fire); CloudTrail Invoke COVERAGE-ABSENT (0 of 2 trails select AWS::Lambda::Function); positive control management events in the window = 2
ARM f   FAIL SES MessageId(s) in the orchestrator log for this run: 0; CloudTrail SendRawEmail in the run's minute: 0; Destinations must name aj@opalinvest.com + andrew@opalinvest.com
ARM g   PASS reporter box i-070477bf35fc54409 State.Name=stopped (describe-instances)
ARMS 6 of 7 PASS
EGS14-NOT-RERENDERED -- failing arms: f
```

Denominator: 7 of 7 arms evaluated, 6 PASS / 1 FAIL. The token `EGS14-AUGUST-RERENDERED` was NOT
printed, so the order stays open (row `ETFS_GUARDRAIL-W1-S18`).

### S14-AC2 -- JUDGMENT, graded by the CVO at L9. Evidence, no verdict.

- **FWD-6, the alignment on the LIVE render.** The render ran on the box with the deployed
  alignment code (`_align_inflection_series`, `ORION_ALIGNMENT_CUTOVER = "2026-09"`,
  `render_month_end.py:60-79` @`93264db36c`) -- and the import that used to crash IS the alignment's
  own module, so this fire is the first time the alignment code has executed in production. Per
  EG-s-13's FORWARD-ONLY qualifier the 2026-08 month renders exactly as it always did (cutover is
  2026-09), and the numbers below confirm it: every numeric row is byte-identical to the pre-run
  artifact. The three partners' coverage lines all read `21/21 trading days; 0 carried`.
- **The served CSV before vs after -- the diff, printed:**

```
opaletfs_49financial_202608.csv    before rows=5 after rows=6 | identical rows 5 of 5 | changed rows none | added: ['# coverage: 21/21 trading days; 0 carried for missing data']
opaletfs_cottonwood_202608.csv     before rows=5 after rows=6 | identical rows 5 of 5 | changed rows none | added: ['# coverage: 21/21 trading days; 0 carried for missing data']
opaletfs_inflection_202608.csv     before rows=5 after rows=6 | identical rows 5 of 5 | changed rows none | added: ['# coverage: 21/21 trading days; 0 carried for missing data']
```

  Exactly FWD-3's shape: the numeric rows are untouched (so `AVERAGE()` in Excel still reproduces
  the deck's average) and the coverage row is appended.
- **What the run wrote beyond the three publish keys:** `coverage_verdict.json` (00:24:44Z, verdict
  `PUBLISH`, holes 0, per-partner 21/21). No `coverage_unresolved.json` (no unresolved days), no
  `refused/` prefix. The only other new objects in the bucket this turn are the 10 archive copies
  this worker wrote under `platinum/reports/_archive/2026-08/`.
- **A change in the served HTML that is NOT numeric:** the box render carries 4 `<svg>` blocks
  (charts) where the ad-hoc LOCAL render it replaced carried 9 -- the five inlined Opal logos
  (3868 B each, 19,044 chars) are gone, because `opal_logo_svg()` resolves
  `<repo root>/portal/public/logos/opal-logo-white.svg` and on the box that path is `/opt/portal/...`.
  Headings 4 of 4, table rows 31 of 31, slides 5 of 5, `PFOE` occurrences 8 of 8 -- identical. No
  data is missing; the brand bar is empty. Pre-existing and structural to every scheduled fire;
  filed as row `ETFS_GUARDRAIL-W1-S19`.
- **The one thing this order cannot see:** delivery at `aj@opalinvest.com` and
  `andrew@opalinvest.com`. The send is evidenced (table above) but the inboxes are the issuer's read.
- **Vintage:** repo citations @`93264db36c` / `5507841f04`; the fix at `0c8bdbe`; AWS reads
  2026-09-09 23:01Z - 2026-09-10 00:50Z.

## ROWS FILED

| id | class | hazard | subject |
|---|---|---|---|
| `ETFS_GUARDRAIL-W1-S11` | BLOCKING | ARMED (`2.0.0_SA_COO`) | the deployed renderer could not import `_orion_vendor_asof` on the box -- **RULED and FIXED this turn** (commit `0c8bdbe`, deployed 00:16:35Z, re-run Success) |
| `ETFS_GUARDRAIL-W1-S12` | OBSERVATION | ARMED (`2.0.0_SA_COO`) | the first-cut archive location sat inside the prefix the email enumerates -- **RULED**, both archives now outside it |
| `ETFS_GUARDRAIL-W1-S13` | OBSERVATION | INERT | no trail selects Lambda data events -- **RULED**, arm (e) re-cut and now PASSES |
| `ETFS_GUARDRAIL-W1-S14` | OBSERVATION | ARMED (`2.0.0_SA_COO`) | the invoke is synchronous -- **RULED**, the flags are cut into the bound and were used |
| `ETFS_GUARDRAIL-W1-S15` | OBSERVATION | INERT | `ARTIFACT-CARRIES-NO-TRIGGER-FIELD` |
| `ETFS_GUARDRAIL-W1-S16` | OBSERVATION | ARMED (`2.0.0_SA_COO`) | `deploy_ledger.py` regenerates the entry -- **RULED** as an ordering clause; honoured (appended after the CLOSE) |
| `ETFS_GUARDRAIL-W1-S17` | OBSERVATION | INERT | the tool has no `add-leg` verb and `open` refuses on an existing slug; the three new legs were appended to the sentinel |
| `ETFS_GUARDRAIL-W1-S18` | BLOCKING | INERT | arm (f)'s two named instruments cannot show any send; the send is evidenced by two others -- the only failing arm |
| `ETFS_GUARDRAIL-W1-S19` | OBSERVATION | ARMED (`2.0.0_SA_COO`) | the BOX render carries no Opal logo (`/opt/portal/...` absent); numbers identical |

## WHAT WAS NOT DONE, AND WHY

- **No second code change.** The amendment granted exactly one file; `lambda_function.py` stayed
  READ-only, so no `MessageId` print was added (that is what arm (f) would need -- row W1-S18).
- **No rollback executed.** Neither the served objects (the re-render is the intended state; every
  prior byte is held twice) nor the renderer deploy (DEPLOYED == BUILT). Both recipes are in the
  entry.
- **Nothing deleted** -- no S3 delete of any kind; both archives stand.
- **No third invoke.** Two fires happened, each recorded; a third would add nothing.
- **No trail, selector, alarm, topic, schedule or env var created** -- moratorium and out of
  `<paths>`; the SES/CloudTrail gaps are rows, not builds.
- **No inbox read and nothing sent by me** -- no mailbox instrument; the orchestrator's run is the
  one send.
- **No `<status>` flip** -- S14-AC1 FAILS by output on arm (f).
