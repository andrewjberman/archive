# OPAL_SQSCHAT.T1 -- Adopt the live Port-2 FIFO queue-pair into Terraform (import, 0-diff, no redesign)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>1.0.0_SA_CTO~Z (arch-gate LD-0347; charter item 2 from 0.0.0_AB_MSTR~Z 20260729T134838Z)</issued_by>
<date>2026-07-29</date>
<status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "OPAL_SQSCHAT (transport) / NFRA_AGENTBUS Port 2 (owning PRD," to OPAL_SQSCHAT, which is closed. Closed as a record act, not a work verdict. Prior status: pending</status>
<go>GO IS LIVE -- flip to `pending` and take it when your slots allow. It is small (an import + a 0-diff plan), and it is the item MSTR least wanted deferred: two queues are LIVE, COSTING, and invisible to `terraform plan`. NOTE ON ADDRESSING: I am the site-Z CTO lane and CANNOT reach you over MCP -- opal-agent-comms is a localhost broker and liveness.json is gitignored, so the fabric is device-local (that is the defect OPAL_SQSCHAT exists to fix). This GO reaches you over the SQS delivery tier + the git history tier. Per Rule 22b I have NOT recorded it delivered: ACK it by MCP to 1.0.0_SA_CTO (base, on your device) and/or `agentbus-sqs.sh send sitez 0.7.0_AE_CloudOps <ack>`, naming this TO.</go>
<project>OPAL_SQSCHAT</project>

## WHAT EXISTS AND WHY IT IS NOT IN STATE

Two FIFO queues were created **by CLI** on Andrew's explicit frontrun instruction 2026-07-29, by
`0.0.0_AB_MSTR~Z`, outside the normal chain because the Tier-1 chain is structurally unreachable
from site Z over MCP. That was sovereign and is settled. What is NOT settled is that they are live
infra outside Terraform, which CLAUDE.md makes the only deploy mechanism.

**MEASURED LIVE 2026-07-29T~1355Z (`313476888478` / `us-east-1`) -- write your TF to match THIS, not to an idealized shape:**

| attribute | BOTH queues |
|---|---|
| names | `agentbus-ajbdev-sitez-to-laptop.fifo`, `agentbus-ajbdev-laptop-to-sitez.fifo` |
| `fifo_queue` | `true` |
| `content_based_deduplication` | `true` |
| encryption | **`sqs_managed_sse_enabled = true`** -- SSE-SQS managed. **`kms_master_key_id` is NULL. There is no CMK.** |
| `message_retention_seconds` | **`1209600`** (14 days) |
| `receive_wait_time_seconds` | **`20`** (long-poll) |
| `visibility_timeout_seconds` | `30` |
| `max_message_size` | `1048576` (1 MiB, the AWS default) |
| `delay_seconds` | `0` |
| queue policy | **NONE. Do not add one.** (see the DO-NOT section) |

Convention (mirrors the module's own): `<sender>-to-<receiver>` is the RECEIVER's inbound queue.
`sitez-to-laptop` = the laptop's inbound; `laptop-to-sitez` = site Z's inbound.

## THE ARCHITECTURAL TRAP IN THIS TO -- READ BEFORE YOU OPEN THE MODULE

`infra/aws/terraform/nfra-agentbus/` already contains an SQS queue-pair (`q_a_to_b` / `q_b_to_a`,
the `agentbus-sim01` fleets) and it is a **PORT 1** artifact: per-collaboration KMS CMK
(`kms.tf`), two-principal `aws_sqs_queue_policy` read partitions (`sqs.tf:34-82`), and
per-fleet IAM roles + partition policies (`iam.tf`).

**DO NOT MIRROR THAT PATTERN. It is the 5-control cross-distrust model, and
`NFRA_AGENTBUS_PRD.md` A.2 excludes every one of those controls from Port 2 BY CONSTRUCTION** --
same principal owns both machines, so there is no colleague boundary to partition, no
cross-read to deny, no DLP boundary. Copying the neighbouring resource because it is adjacent and
looks canonical would be applying Port 1's security model to Port 2. **The two ports do not blur;
A.2 says so explicitly and Amendment B B.5 restates it.**

Concretely, the sim01 block would also silently CHANGE live state if copied: it sets
`message_retention_seconds = 345600` (4 days) against the live **14 days**, and a
`kms_master_key_id` against live **SSE-SQS managed**. **An import followed by a copied-neighbour
config is not adoption -- it is an undeclared reconfiguration of a live channel on the first apply.**

## THE RULED SHAPE (build to this)

1. **A SEPARATE MODULE: `infra/aws/terraform/nfra-agentbus-port2/`.** Not a second queue-pair
   inside `nfra-agentbus/`. Rationale, and it is an arch call not a preference: one module = one
   state = one apply blast radius. Port 1 and Port 2 have **different trust models and different
   security postures**, and co-locating them means a Port-1 apply can touch Port-2's live channel
   and vice versa. The ports are separated by trust model and queue identity -- keep the state
   boundary on the same seam.
2. **Two `aws_sqs_queue` resources ONLY**, attributes exactly as measured above.
   `sqs_managed_sse_enabled = true`; **no `kms_master_key_id`**, no `aws_kms_key`.
3. **No `aws_sqs_queue_policy`.** Access is the account-level principal (`user/Andrew_Berman`,
   both devices, two independently-revocable access keys -- verified live under LD-0347 B.4).
   Adding a policy here does not harden anything and would be the Port-1 pattern leaking in.
4. **No IAM roles, no partition policies, no DLQ, no `redrive_policy`** -- none is in live state
   and none is called for by Port 2's design. **A DLQ in particular is NOT an omission to fix:**
   Port 2's delivery oracle is an agent-side ACK on the git history tier (Amendment B B.3), and a
   DLQ would introduce a second, weaker place a message can sit while looking handled.
5. **`terraform import` both queues, then `plan` must be EXACTLY `0 to add, 0 to change, 0 to destroy`.**
   That 0-diff IS the acceptance test: it proves the TF you wrote describes the queues that exist,
   which is the only thing adoption means. A non-zero plan means your config diverges from live --
   **fix the CONFIG to match live; do NOT apply the diff to make the plan clean.** If you believe
   live is wrong (e.g. 14d retention should be shorter), that is a SEPARATE, deliberate change
   after a clean 0-diff -- surface it, do not fold it in.
6. **Tags:** whatever `default_tags` the module inherits, verified not to produce a diff. If
   default_tags would introduce a tag change against live, report it rather than applying -- the
   `partner-etl-ops-alerts` in-place tag drift (`NFRA_TERRAFORM_P2_batchC_residuals.md:134`) is the
   known instance of that class in this estate.
7. **Register the module** wherever `nfra-agentbus` is registered for CI/drift detection, so a
   future drift sweep sees it. An adopted resource nobody sweeps is only half adopted.
8. **Apply via `.tools/safe-apply.sh`. Never bare `terraform apply`** (CLAUDE.md NEVER#3). An
   import + 0-diff needs no never-widen hold (DELTA=0), but the wrapper is still the only path.

## DO NOT (each of these would be a rule violation, not a style choice)

- **No alarm, alert, SNS topic, SES send, freshness checker, monitor, or CloudWatch metric alarm
  on these queues or this module.** The 2026-07-28 moratorium is STANDING and Andrew named it an
  anti-pattern. MSTR flagged in the charter that this channel is "adjacent enough to tempt it,"
  and a new transport with an unproven leg is exactly where an alarm feels like the cheapest
  deliverable. **A queue-depth alarm here would also be measuring the wrong thing precisely:**
  depth is producer-side and cannot distinguish read from discarded (Rule 22b).
- **Do not delete, purge, or drain either queue.** `sitez-to-laptop` currently holds
  `MessageId b02b96d8-a455-4cb0-80e1-5e0f773b1fca` -- an UNCONSUMED message that is the pending
  cross-device delivery proof. **Purging it destroys the evidence the project's verification bar
  depends on.** An import does not touch messages; keep it that way.
- **Do not "fix" the 1 MiB `max_message_size`.** It is the AWS default and live. The 8KB body cap
  is an application-layer AC (`AC-2`), enforced by the sender-side lint per Amendment B, not by
  the queue.
- Do not rename the queues to a taxonomy you prefer. They are live and in use; a rename is a
  destroy+create of the channel MSTR's unproven message is sitting in.

## <compiler_tools_mandate>
<phase id="1" when="before write">
  <step>
    <run>comp-blast on infra/aws/terraform/nfra-agentbus (and any registry the new module joins)</run>
    <expect>Confirms the new module is NOT coupled into the Port-1 module's state or apply path. Any shared node = a cross-domain resource; flag it before writing.</expect>
    <if_mismatch>STOP and surface to 1.0.0_SA_CTO (base, relay to ~Z). If Port 1 and Port 2 cannot be state-separated, that is an arch question, not an AE workaround.</if_mismatch>
  </step>
  <step>
    <run>aws sqs get-queue-attributes --attribute-names All, per queue, re-read at write time</run>
    <expect>Matches the measured table above. If it does NOT, live changed since 2026-07-29T~1355Z -- write TF to what you measure, and report the delta.</expect>
    <if_mismatch>Report the delta in your ACK. Do not silently adopt a different shape than this TO describes.</if_mismatch>
  </step>
</phase>
<phase id="2" when="before commit">
  <step>
    <run>.tools/terraform.exe plan (post-import) in the new module</run>
    <expect>EXACTLY "No changes." / 0 to add, 0 to change, 0 to destroy. Paste the literal line.</expect>
    <if_mismatch>Fix the CONFIG to match live. Do NOT apply a diff to make the plan clean, and do NOT commit a non-zero-diff adoption.</if_mismatch>
  </step>
  <step>
    <run>comp-iam gaps (iam.tf unchanged is the expectation -- run it to prove you added no grant)</run>
    <expect>No new grants attributable to this module. Port 2 adds no IAM per LD-0347 B.4.</expect>
    <if_mismatch>If you found yourself needing a role, STOP -- you are building Port 1's model. Surface it.</if_mismatch>
  </step>
</phase>
<phase id="3" when="after commit">
  <step>
    <run>terraform state list | grep aws_sqs_queue  AND  aws sqs get-queue-attributes on both queues</run>
    <expect>Both queues present in STATE (desired) AND unchanged in LIVE (applied) -- Rule 22a: cite both layers, a state-read alone cannot tell landed from planned.</expect>
    <if_mismatch>Roll back the state change and escalate; a half-adopted queue-pair is worse than an untracked one (two records, one of them wrong).</if_mismatch>
  </step>
  <step>
    <run>aws sqs get-queue-attributes --attribute-names ApproximateNumberOfMessages on agentbus-ajbdev-sitez-to-laptop.fifo</run>
    <expect>Still >= 1 -- MessageId b02b96d8-... survived the adoption. This is a positive control that the import touched infrastructure, not messages.</expect>
    <if_mismatch>The pending delivery proof was destroyed. Report immediately to 1.0.0_SA_CTO + 0.0.0_AB_MSTR; the project's verification bar has to be re-established.</if_mismatch>
  </step>
</phase>

## <cross_domain_coordination>
- **`0.0.0_AB_MSTR` / `0.0.0_AB_MSTR~Z`** -- created the queues; owns the unconsumed message that must
  survive your import; owns the missing `PROP-AGENTBUS-P2-SQS-20260729.md` citation (LD-0347 B.6).
- **`1.0.0_SA_CTO` (base, YOUR device) / `~Z` (me, site Z)** -- arch-gate. Route anything that looks
  like a design decision to CTO rather than resolving it in the module. **I am not MCP-reachable from
  your device**; base CTO is, and the SQS + git tiers reach me.
- **`infra/aws/terraform/nfra-agentbus/`** -- SHARED-ADJACENT, deliberately NOT shared: do not modify
  the Port-1 module in this TO. If you find yourself editing it, the state-separation ruling (item 1)
  is being violated.
- **`docs/architecture/NFRA_AGENTBUS_PRD.md` Amendment B** -- the authority for every "do not" above.
  If it and this TO disagree, the PRD wins and you tell me.

## <acceptance_criteria>
1. `infra/aws/terraform/nfra-agentbus-port2/` exists, declares exactly two `aws_sqs_queue`
   resources, ZERO `aws_kms_key`, ZERO `aws_sqs_queue_policy`, ZERO IAM resources.
   *(Machine-checkable: `grep -c` per resource type.)*
2. Both queues in `terraform state list`, and `terraform plan` output contains the literal
   `No changes.` (or `0 to add, 0 to change, 0 to destroy`) -- **pasted verbatim into your log**.
3. Live attributes byte-identical to the measured table (post-adoption re-read, per queue).
4. `ApproximateNumberOfMessages >= 1` on `agentbus-ajbdev-sitez-to-laptop.fifo` after adoption
   (the pending proof survived).
5. ZERO new `aws_cloudwatch_metric_alarm`, `aws_sns_topic`, `aws_sns_topic_subscription`, or SES
   resource anywhere in the change. *(Machine-checkable: `grep -c` over the diff.)*
6. Module registered for CI drift detection.
7. A session log with a **Compiler Tools** section, plus the `org/compiler-tools-log.md` line.
8. An ACK naming this TO, delivered to CTO by a path that crosses the device boundary
   (MCP to base CTO on your device, and/or `agentbus-sqs.sh send sitez`).

## NOT IN SCOPE
Envelope/typed-kinds/validation (WS-1), the MCP bus tools (WS-2), breach surfacing (WS-3), the
sender-side 8KB lint, ACK records on the git tier, and anything about `bus_claim` (FENCED --
Amendment B B.3). **This TO is adoption of existing infrastructure into state. Nothing more.**
