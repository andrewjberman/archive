# TO D7_TICKETING.WB-SITEZ — Ticket Lifecycle v2 W-B: DDB-Streams nudge ACCELERATOR on top of the scheduled backstop

<task_order id="D7_TICKETING.WB-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build: notifier + nudge contract; owns the runner/backstop substrate). Laptop apply leg (Terraform: stream + notifier Lambda) = EXECUTION PLACEMENT via 0.0.0_AB_MSTR~Z ferry.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>staged — ACTIVATES when TAC-3 reads "schedule landed" (dep-3 registration + schedule-landed battery at this seat). 1.0.0_SA_CTO~Z @942d4d885c ruling 1: "dep-2/dep-3 land first, exactly as specified, and the stream is added ON TOP as W-B." This is CTO-ruled sequencing, not a COO-manufactured gate.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ @942d4d885c — his O3 verbatim: "This write somehow triggers 0.0.3_BG that there is a new ticket..." ("somehow triggers" = his latitude); 1.0.0_SA_CTO~Z ruling 1 (NUDGE MODEL): DDB Streams → small notifier → BG nudge as the FAST path PLUS the 5-min Scheduled Task as the standing backstop — a production pipeline must have a SCHEDULE, event-driven is the accelerator (CLAUDE.md law). The nudge path is ANDREW-ASKED (his flow step O3/O7/O8) — not moratorium machinery.</authority>
</task_order>

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
