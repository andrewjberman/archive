# INBOUND_CLOUD_DEPLOY_NOTES -- TO-CT-i-1 (0.9.0_WK_NFRA_CTLPLN~31)

What the deploy after the drain must carry. Nothing here was applied; no Terraform file was edited.

## 1. The two policy statements the function's role needs

The Teams agent (`teams-global-chat-assist-role`) now offers a job to every box of `org/devices/DEVICES.json`: four boxes,
two of them new (`dell1`, `dell2`). `infra/aws/terraform/transcripts/chat_assist.tf` `extra_statements` holds the two
existing statements (`TellTheLaptopMstrOnTheBus`, `TellTheSiteZMstrOnTheBus`); two more are needed, one per queue,
because `extra_statements` is `list(any)` and every element's Resource must share one type (the comment above the existing
pair). Account id from `data.aws_caller_identity.current.account_id`, as the existing two:

```
{ Sid = "TellDell1OnTheBus", Effect = "Allow", Action = ["sqs:GetQueueUrl", "sqs:SendMessage"],
  Resource = "arn:aws:sqs:us-east-1:${data.aws_caller_identity.current.account_id}:agentbus-global-dell1-queue.fifo" },
{ Sid = "TellDell2OnTheBus", Effect = "Allow", Action = ["sqs:GetQueueUrl", "sqs:SendMessage"],
  Resource = "arn:aws:sqs:us-east-1:${data.aws_caller_identity.current.account_id}:agentbus-global-dell2-queue.fifo" },
```

Without them the first `#dev` fails at `sqs.get_queue_url` for `dell1` (AccessDenied) inside `on_job_open`, after the brief
is written and before any offer is sent to that box. The queue names are the register's `inbound_queue` values
(`agentbus-global-dell1-queue.fifo`, `agentbus-global-dell2-queue.fifo`); the Dell side's own receive policies
(`infra/aws/terraform/nfra-ctlpln-identity/dell1_bus_policy.json`, `dell2_bus_policy.json`) are the receiving half and
already exist.

## 2. Package step

- The function's package carries `NAMES.json`, not the register. `data/transcripts/scripts/teams_chat/NAMES.json` now
  holds `bus_devices` (four boxes). Before building the zip, run
  `python data/transcripts/scripts/teams_chat/gen_bus_devices.py --check`; it must print `BUS-DEVICES ok=True`. If it prints
  `ok=False` (a box was added to the register), run `--write` and commit `NAMES.json`.
- `gen_bus_devices.py` is a build-time tool and need not be in the zip.

## 3. Behaviour changes that the deploy makes live

- One extra model call per waiting chat message (`assist.work_request`, system prompt `WORK_SYSTEM`) on the same Kimi
  path, in the same event as the reply draft. Worst case the two calls take 2 x `KIMI_TIMEOUT_S` (240 s); check the worker
  Lambda's timeout and the LDO event visibility against about 480 s plus the draft before deploy. A failure of this call
  is swallowed (the text is today's text).
- A job in flight at deploy time has no `offered_to` in its state; the early award then waits for all four boxes (the
  award alarm at the 120 s deadline still awards). Deploy with no job in `bidding`, or accept the alarm path.
- `job.complete` without a good grade no longer reaches `verify`: it leaves the job `working` and texts one line.
  The box tool (`.tools/remote-job.py`, another worker's cell) must send `coo` and `grade` {`by`, `verdict`, `record`, `at`}
  on `complete`, `reviewer` / `unavailable_reason` on `bid`, `brief_sha256` on `accepted`, or every completion is refused.
  Deploy the box half first or together.

## 4. Open items found while building (rows in the investigation file)

- `NFRA_CTLPLN-W31-S1`, `-W31-S2`: three tests in `data/transcripts/scripts/tests/test_teams_chat_jobs.py` fail by design of
  this change (four-box offer; completion without a grade). They need an order that carries that file in its `<paths>`;
  the deploy gate that runs the suite will stop on them until then.
- `NFRA_CTLPLN-W31-S3`: the seam's additions to `REMOTE_JOBS_PROTOCOL_20261002.md` are not written in the protocol file.
