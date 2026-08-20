# TO D7_TICKETING.WB-SITEZ — Ticket Lifecycle v2 W-B: DDB-Streams nudge ACCELERATOR on top of the scheduled backstop

<task_order id="D7_TICKETING.WB-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build: notifier + nudge contract; owns the runner/backstop substrate). Laptop apply leg (Terraform: stream + notifier Lambda) = EXECUTION PLACEMENT via 0.0.0_AB_MSTR~Z ferry.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>staged — ACTIVATES when TAC-3 reads "schedule landed" (dep-3 registration + schedule-landed battery at this seat). 1.0.0_SA_CTO~Z @942d4d885c ruling 1: "dep-2/dep-3 land first, exactly as specified, and the stream is added ON TOP as W-B." This is CTO-ruled sequencing, not a COO-manufactured gate.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ @942d4d885c — his O3 verbatim: "This write somehow triggers 0.0.3_BG that there is a new ticket..." ("somehow triggers" = his latitude); 1.0.0_SA_CTO~Z ruling 1 (NUDGE MODEL): DDB Streams → small notifier → BG nudge as the FAST path PLUS the 5-min Scheduled Task as the standing backstop — a production pipeline must have a SCHEDULE, event-driven is the accelerator (CLAUDE.md law). The nudge path is ANDREW-ASKED (his flow step O3/O7/O8) — not moratorium machinery.</authority>
</task_order>

## ⛔ BUILD-BLOCKING HOLE IN THIS CUT — THE LAST ARROW HAS NO MECHANISM (22:15Z)

*(`0.5.0_AE_OpalETL~Z` @3318, found on the pre-write check and surfaced BEFORE writing. The defect is
mine: I cut the chain with a hop that does not exist.)*

**AS CUT:** DDB stream → notifier Lambda → *"BG's nudge (writes the nudge/buzz payload for the serve
loop / fabric inbox file to the BG seat)"*. **THAT LAST ARROW HAS NO MECHANISM.**

| grounded fact | consequence |
|---|---|
| The notifier is a **Lambda in AWS**; BG's nudge target is a **filesystem inbox on the BBG box** | **A Lambda cannot write a local file.** No bridge exists in the cut |
| The notifier **cannot send the buzz itself either** — the gateway bearer is validated at the transport layer and its refresh is an **INTERACTIVE OAuth challenge answered by the Claude Code client** | **A LAMBDA CAN NEVER BE THAT CLIENT.** The one delivery surface that works for the runner is **structurally closed** to a Lambda |
| The estate's only live AWS→local channel is the **agentbus FIFO device pairs** | **MSTR-scoped coordination, one consumer per device, "the bus is coordination-only" is standing.** Not a ticket bus |
| So the notifier can write an AWS-side store, but **something LOCAL must consume it** | **the only thing already running locally on a schedule is the 5-min runner** |

>> ⛔ **THE CONSEQUENCE, which WB-1 would otherwise surface at test time as "the nudge is not
faster": IF THE LOCAL CONSUMER IS THE 5-MIN RUNNER, THE ACCELERATOR DELIVERS AT BACKSTOP LATENCY AND
ACCELERATES NOTHING.** WB-1 asks for the stream path's measured latency — **as cut, that number would
be the backstop's.** *An event-driven accelerator whose last hop is a five-minute poll is not an
accelerator; it is a second detector feeding the same delivery clock.*

>> **AND IT IS THE DETECT/DELIVER SEAM, THIRD SURFACE.** The stream is the purest instance yet: **a
genuinely agent-independent DETECTOR whose DELIVERY terminates at an agent-shaped boundary it cannot
cross.** Same root as the DL and the escalation — every delivery surface reached for so far routes
through something only a live interactive session can drive.

**OPTION SET (design is `1.0.0_SA_CTO~Z`'s; neither the builder nor I choose):**
**(i)** a **fast local consumer** — a long-poll SQS reader on the box, reusing the agentbus consumer's
existing shape; costs a second standing local process. **(ii)** ⛔ **SHORTEN THE BACKSTOP AND DROP THE
STREAM** — if the requirement is "faster than 5 minutes", a **1-minute schedule with NO new AWS
surface** may be the honest answer. **This is rung 1: does the stream need to exist at all?**
**(iii)** notifier → a nudge flag on the ticket row, runner reads it — no new transport, but inherits
the 5-min clock. **(iv)** something laptop-side not visible from this box.

⚠ **BUILD IS HELD ON THIS ONE QUESTION ONLY.** The four ratified pre-build decisions still hold
whichever way it goes — they concern the stream's CONFIGURATION, not its DELIVERY. **Rule the hop and
the build proceeds the same hour.** *If the answer is (ii), W-B as cut may not need to exist — which
is a better outcome than building the estate's first DynamoDB stream to feed a five-minute poll.*

## Objective
Add the FAST path on top of the (already-landed) scheduled backstop, same runner substrate:

- DynamoDB Streams enabled on `opal-tickets` → a SMALL notifier Lambda → BG's nudge (writes the
  nudge/buzz payload for the serve loop / fabric inbox file to the BG seat) on create, claim, and
  close transition writes (his O3 + O7 + O8; the approved (b): claim AND complete confirmations).
- The 5-min Scheduled Task REMAINS the schedule — the same runner, now catching only what the
  stream missed. The runner's cursor makes double-delivery idempotent BY CONSTRUCTION; dedupe key
  = (ticket id, event).
- The buzz content = the §12 serve discipline (concise, id, deep link `/ticket-center?ticket=<id>`,
  identifier-beside-value). Every gateway send handles `confirm_on_irreversible` (confirm=true or
  two-step — the fence is TOOL-WIDE, SCHEDULE_DECISION.md send row @56cd2208e1).
- **COMPLEMENTS, NOT SUBSTITUTES (1.0.0_SA_CTO~Z ruling 2762/2768, folded at the cut):** this stream-nudge
  accelerator wakes BG for NEW TICKETS; user QUESTIONS in the channel are heard ONLY by the
  teams-watch CHANNEL-LEG P1 (separate ruled build, owner 0.5.0_AE_OpalETL~Z, sequenced ON TAC-2' close, design
  blessed in 2768: direct bounded read / per-channel cursor own file / watched-ids config). Neither
  covers the other; W-B's acceptance never claims the consumer limb. Note: TAC-3 = SCHEDULE LANDED
  (2026-08-20 ~20:0xZ) — this TO's staging condition is MET; sequencing vs the channel-leg P1 and
  W-A is the seat's queue under 1.0.0_SA_CTO~Z's ruled priorities.

## Acceptance criteria
- **WB-1** Stream path exercised: a transition write (create / claim / close) produces the nudge
  via the notifier, latency measured and quoted with its denominator (n events).
- **WB-2** BACKSTOP-ALONE negative control: with the stream/notifier disabled (scratch,
  run-and-read — nothing standing), the next scheduled pass delivers the same event. The schedule
  is the pipeline; the stream is provably only an accelerator.
- **WB-3** DEDUPE exercised: stream AND schedule both deliver one event → exactly ONE buzz
  (idempotency on (ticket id, event) shown on real payloads).
- **WB-4** Notifier failure loses nothing: notifier erroring (scratch fault injection) → the
  scheduled pass still delivers; the failure is visible in the runner's exit contract, not
  swallowed.
- **WB-5** IAM per 22a: stream-consumer role verified on the LIVE primitive (one --resource-arns
  per call + separate positive control; comp-iam = floor). TF apply via safe-apply; ledger + tag;
  0-diff.
- **WB-6** Proof instance VALID rc=0 positional, ids WB-1..WB-6.

<proof_of_spec>
  <expected_criteria>WB-1,WB-2,WB-3,WB-4,WB-5,WB-6</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WB_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<compiler_tools_mandate>
Before write: `comp-blast` on opal-tickets + ticket_center infra; `comp-iam service` (floor) +
`comp-estate` layer check for an existing stream/notifier pattern (Build Ladder rung 2 — reuse
before build). Before commit: commit-gate. After apply: live simulate per WB-5.
</compiler_tools_mandate>

<cross_domain_coordination>
Terraform tree `infra/aws/terraform/` (ticket-center module) — coordinate with any laptop-side
ticket-center TF in flight via 0.0.0_AB_MSTR~Z ferry BEFORE apply. The runner
(`integrations/ticketing/intake/`) is this seat's own. No portal files. NOT an
aws_cloudwatch_metric_alarm / SNS / SES resource — if any lint pattern-matches, the inline marker
cites the Andrew flow step O3 verbatim (# andrew-asked).
</cross_domain_coordination>

## Do not
No SNS/SES/alarm/monitor resources — the nudge is a Lambda→serve-loop delivery, not notification
machinery. Do not remove or bypass the scheduled backstop — trigger-only-on-stream is the defect
class the law names. Do not start before TAC-3 = schedule-landed.

## Reporting
Completion → 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance) + 0.0.0_AB_MSTR~Z (ferry). Surprise channel: one line
to 2.0.0_SA_COO~Z. Session log = deliverable.
