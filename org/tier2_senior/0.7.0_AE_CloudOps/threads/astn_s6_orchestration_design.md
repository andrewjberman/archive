# ASTN_WSJFT S6 -- 3am-ET orchestration design (AE -> CTO arch-gate)

**Lane:** 0.7.0_AE_CloudOps~C | **Status:** DESIGN for arch-gate | **2026-06-24**
**Guardrail (CTO 210519Z + 214107Z):** create the schedule DISABLED; enabling = Andrew's go-live.

## Constraint
- ONE EC2 (LOCKED), TRANSIENT: STOPPED between runs (cost + surface). At 3am it's stopped -> a
  single EventBridge->SSM SendCommand can't run on a stopped box. Need start -> run -> stop.
- DST-aware 3am ET: EventBridge **Scheduler** `schedule_expression_timezone="America/New_York"` (native).
- FAIL-LOUD: a broken run (0 fetched / 0 survive / send error) ALARMS, never silent. run.py already
  exits non-zero on the FATALs; the orchestrator surfaces that + a missed-run (silent-absence) alarm.

## Flow (start -> run -> stop), all in a small orchestrator Lambda (boto3)
```
EventBridge Scheduler (cron(0 3 * * ? *), TZ America/New_York, STATE=DISABLED until go-live)
  -> astn-wsjft-orchestrator Lambda:
       1. ec2:StartInstances(i-0c8b110af37486ecc)
       2. poll until SSM PingStatus=Online (agent re-registers on boot; ~60-90s)
       3. ssm:SendCommand AWS-RunShellScript -> deploy.sh (idempotent pull) ; python3 run.py
       4. poll GetCommandInvocation until terminal; capture exit code + tail
       5. ec2:StopInstances(...)  -- ALWAYS (finally), even on failure (cost)
       6. on non-zero run.py exit / step-timeout -> sns:Publish FAIL-LOUD to the alerts topic
       7. (silent-absence guard) verify s3 digest/{today}/digest.json exists post-run; absent -> alarm
```
Lambda over Scheduler->SSM-direct: the start->wait-online->run->stop is multi-step + conditional
(must wait for SSM online before SendCommand); Scheduler's universal target is single-call. (SSM
Automation doc is the alt; Lambda is simpler to fail-loud + log. CTO pick -- lean Lambda.)

## Two SEPARATE roles (CTO 210519Z -- never the scraper instance-role)
- **Scheduler role** (assumed by scheduler.amazonaws.com): `lambda:InvokeFunction` on the orchestrator only.
- **Orchestrator Lambda role**: `ec2:StartInstances|StopInstances|DescribeInstances` (Condition: the
  astn instance / its tag), `ssm:SendCommand` (Resource: the instance + the AWS-RunShellScript doc) +
  `ssm:GetCommandInvocation`, `sns:Publish` (the alerts topic), CW Logs, `s3:GetObject` on
  digest/* (the silent-absence check). NOT secrets, NOT the SES/scraper grants (the scraper role keeps those).

## Fail-loud surface
- CW alarm on orchestrator Lambda Errors>=1 -> SNS.
- run.py non-zero captured -> SNS "ASTN digest run FAILED <reason>".
- Silent-absence: no digest/{today}/ object by ~4am ET -> SNS (absence is the dangerous mode).

## FT self-healing reharvest (CTO 224329Z -- app-layer, noted here for the orchestration contract)
- run.py FT-leg: on a fetch CF-challenge -> a plain fetch-RETRY first (transient hiccup); only on
  CONFIRMED session-expiry -> trigger the Kimi reharvest-through-proxy. CAP = 1-2 reharvests then
  FAIL-LOUD-alert + STOP (no captcha-hammer loop -- ROE). WSJ proceeds regardless (FT WARN-degrades).
- Orchestrator just runs run.py; the cap/retry logic lives in run.py (CTO lane). The SNS fail-loud
  topic carries the "FT reharvest exhausted" alert.

## IaC
- Terraform (astn-pipeline module): aws_scheduler_schedule (state=DISABLED) + aws_lambda_function
  (orchestrator, TF-only per Rule 1) + the 2 roles + aws_sns_topic + the CW alarms. Source-map entry.
- Tag astn-pipeline-v0.3.0 on apply. EC2_MANIFEST unchanged (instance already registered).

## Open (decide at arch-gate)
1. Lambda orchestrator vs SSM Automation doc (lean Lambda).
2. SNS recipient: a new astn-alerts topic -> who? (Andrew? COO? -- ask). Reuse an existing ops topic?
3. Go-live flip = (a) set the schedule ENABLED + (b) flip run.py recipient digest->austin@ (Andrew's word).
