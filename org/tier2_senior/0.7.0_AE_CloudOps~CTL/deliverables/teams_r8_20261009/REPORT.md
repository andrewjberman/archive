# NFRA_CTLPLN.TO-APPLY-31 -- round 8, the drafting contract: applied report

**archetype:** DEPLOY
**seat:** 0.7.0_AE_CloudOps~CTL | **issuer:** 2.0.0_SA_COO~C | **risk:** WORLD | **cell:** CT-i-14
**halves:** COO @`082e0d865a` + CTO @`c2fa3eb0b4`, both read in full before acting

## THE HOUR: 2026-10-09T23:03Z

| event | time (UTC) |
|---|---|
| GO (msg 108145) | 22:38:59Z |
| NEVER-2 entry opened, before the act | 22:45Z |
| BEFORE references saved | 22:46:34Z |
| End of Day gate cleared | 22:47-22:48Z |
| build | 22:50Z |
| targeted plan (branch A verified) | 22:58Z |
| **apply returned** | **23:03:19Z** |
| handler live (`LastModified`, CloudTrail `UpdateFunctionCode`) | **23:03:08Z** |
| ingress live | **23:03:14Z** |
| **hour sent to the issuer** | **23:04:44Z -- before any proof work** |
| re-plan + read-back | 23:05-23:06Z |
| five-minute ingress window | 23:03:14Z - 23:08:14Z |
| ledger CLOSED | 23:09:22Z |

CloudTrail event ids: handler `b53e84c8-66f1-4dc0-bf53-f1ce6aa9db15`, ingress
`df95ca40-35db-4ccc-84fb-55d01b35cbf3`, both `UpdateFunctionCode20150331v2`.

## Packaged-path diff since `bde0c0fc90` (STOP 1)

**Zero files.** The packaged set was taken from `build.sh` itself rather than assumed:
`infra/aws/lambda/teams-chat-assist/handlers.py`, `infra/aws/terraform/modules/ldo` (which holds
`runtime/ldo.py`), `data/transcripts/scripts/teams_chat`, `daily_reports/eod/post_format.py`,
`daily_reports/eod/VOICE.md`, `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json`,
`infra/logic/registry`, plus the root `infra/aws/terraform/transcripts`.

`git diff --name-only bde0c0fc90 HEAD` over that set: **0**. No branch-B token
(`teams_chat/`, `ldo.py`, `handlers.py`, `daily_reports/eod/`) and no other file to name.

STOP 1 was run **twice**: once at HEAD `072a51a03c` and again at the build HEAD `75c918e031`,
because the shared tree moved twice under this seat mid-task. Both read 0. `git status` over the
same set also read **0 dirty**, so the bytes packaged are the bytes committed.

## AC1 at the build commit

`python data/transcripts/scripts/tests/test_draft_contract.py` ->
**`DRAFT-CONTRACT ok=True arms=9/9 base_leaked=True`** (rc=0), matching the COO half's own re-run.
Full output: `AC1-build.txt`.

## The package

32 files, 268,046 bytes, sha256 `485493181417debe3db766174ab37eeade84926cf536ba719235f4f551cb6443`,
base64 `SFSTGBQX3r49t2YXSrN+6t6Ekmz1NrpxkjX09VHLZEM=`, built at `75c918e031`. Both packages were
built so the root loads: `teams-chat-assist.zip` (32 files) and `transcripts-pull.zip` (89 files).
Record: `build.json`.

## BEFORE, saved with hashes (the rollback the CTO half names)

| reference | bytes | sha256 |
|---|---|---|
| `before-live-package.zip` | 261,942 | `a29f7680ceeb951f7de7ab627a7004a760ec732db385d0115775846d80c5a7f3` |
| `before-cursor.json` | 472 | `b8d734ea8f65665efddd4141c5b0df699540c197eccbb400faacf63f816ae623` |
| `before-metadata.json` | 997 | `a3beb880c11a4331145a468e841d04382188ed40ae1151cf314f3f5f71c58dbc` |
| `before-env-names.json` | 959 | `e7b5cadafb29514f7df80ff38c86835a92cb7b844752164c98c806530c52a8ff` |

Both functions were at `CodeSha256` **`op92gM7rlR9956tienAEp2Dscy2zhdARV3WEbYDFp/M=`** (handler
`LastModified` 18:33:43Z, ingress 18:33:37Z) -- equal to the `op92gM7r...` the order requires, so
**not** branch B. The downloaded live zip's own hash equals that `CodeSha256` (the reader asserts it),
so the rollback artifact is the running bytes, not a filename match. `cursor.json` was saved as bytes
and never printed. `MAIL_BEARER_SECRET` present on both functions, read **by name only** -- 13
environment variable names per function, zero values fetched.

## End of Day gate (STOP 3) -- the one place the default read was not good enough

Outside the 20:00Z-21:45Z window (read at 22:47Z). Queue
`ApproximateNumberOfMessagesNotVisible` = **0**.

The predecessor's 60-minute handler-log window returned **0 lines and a positive control of 0**. That
read cannot tell "no End of Day event in flight" from "this filter sees nothing" -- ABSENT is not
EXERCISED-AGAINST -- and the script's own `gate_clear` correctly refused rather than reading
`unmatched_eod=0` as clean. The window was widened on a ladder until the control fired:

| lookback | lines | REPORT control | EOD events | unmatched |
|---|---|---|---|---|
| 60 m | 0 | **0** | 0 | 0 |
| 180 m | 56 | **8** | 4 | **0** |

The in-flight question was then judged on the 180-minute window, which demonstrably sees lines: 4 End
of Day events, **0 unmatched**, so none in flight. `gate_clear = true`. Record: `eod-gate.json`, which
keeps the whole ladder, not just the passing rung.

## The targeted plan, as read

`Plan: 0 to add, 2 to change, 0 to destroy` -- branch A. `check_plan.py` (the predecessor's gate,
reused unchanged) asserts and passed:

- changed addresses are exactly `module.ldo_001.aws_lambda_function.handler` and
  `.ingress[0]`;
- actions `["update"]`;
- changed keys subset of `{source_code_hash, last_modified}` -- so **no environment change**, no
  policy line, nothing outside the module;
- `after.source_code_hash` equals the built package's base64;
- no unexpected computed values.

Verdict: `plan-verdict.json`. Fresh `TF_DATA_DIR` outside every git tree (confirmed by
`git rev-parse` failing in it); `init` without `-reconfigure`, no migration prompt; the saved plan was
applied with the same target and the same `TF_DATA_DIR`.

## ONE DEVIATION from the order's literal text, reported for the issuer to grade

The plan could not run at all: the shared root's `readers.tf` declares
`second_reader_trust_principal_arns` with **no default by design** -- its own comment says "WHO may
assume this role is NOT decided in this file ... a plan without it is refused by terraform". That file
did not exist at the r7 deploy (`a5fde91788`), which is why the predecessor's method never meets it; it
is present at the build commit.

I did not invent a value. I passed that **one** `-var` at its **live value read at the act** --
`["arn:aws:iam::313476888478:user/Opal_Terminal"]`, from
`aws iam get-role --role-name teams-global-transcripts-second-reader-role` (role CreateDate
09:55:13Z) -- which is the issuer's own **A3 ruling** on `COMM_ASSIST.TO-CA-d-2`, same root, same
reason, with "read it at the act; never type it from the order; never pass any other `-var`". No other
`-var` was passed.

A4 of that same order is why this needed checking rather than assuming: when `~CA` first passed the
var, the plan read `1 to add, 3 to change`, pulling in `aws_iam_role.silver_reader` (create) and
`aws_kms_key.transcripts` (policy update) as dependencies, and branch A was correctly not met. Both are
now applied -- silver reader role CreateDate **14:07:25Z** -- which is why this plan reads a clean
`0/2/0`.

**TO-31 names no `-var`, so this is the issuer's call to grade, not mine to assume away.** It widened
nothing: targeting plus the verdict gate bind the act to the two functions, and the applied result is
hash-only on both.

## AFTER, live

- both live `CodeSha256` = **`SFSTGBQX3r49t2YXSrN+6t6Ekmz1NrpxkjX09VHLZEM=`** = the built package
  (`after-metadata.json`, `matches: true`); new RevisionIds `fd7db701...` and `1b850b0a...`;
- targeted re-plan: **exit 0, "No changes. Your infrastructure matches the configuration."**;
- five minutes `23:03:14Z-23:08:14Z`, counts only: 27 lines, positive control REPORT **5**,
  `ingress_poll=5` with all 5 carrying the new fields, `failed_steps={}` so
  **`ingress_step_failed=0`**, `mail_poll=1`. `channel_poll=5` with the `failed` field set on all five
  -- the **pre-existing** condition both halves name. (The order writes "`channel_poll failed=1` is
  pre-existing"; that is the field's value per poll, not a count of one. The r7 predecessor recorded
  the same shape as "channel_poll failed=5 expected until gateway release". Naming the ambiguity so
  nobody later reads 5 as a regression.) Record: `after-ingress-counts.json`.

## Rules honoured

Neither function was invoked. No test event, text or bus line was sent. No chat, mail or message
content was read, and no secret value: the only secret-adjacent read was environment variable **names**.
No untargeted apply. Writes were confined to this deliverables folder, the ledger entry and its
sentinel.

## Ledger

`org/critical_paths/change_management/20261009T2245Z_teams-r8-draft-contract-laptop-20261009_deploy_completion.md`
-- opened 22:45Z before the act naming both function families, three legs each closed with proof,
entry **CLOSED** 23:09:22Z, sentinel removed.

## AC2

Not marked here. Per both halves, status is **APPLIED**, not EXERCISED: the exercise is the issuer's
first real drafting call and the first End of Day redraft. AC2 is the issuer's and the CVO's to grade.
