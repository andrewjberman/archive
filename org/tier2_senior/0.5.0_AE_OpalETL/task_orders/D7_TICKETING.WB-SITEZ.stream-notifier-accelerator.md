# TO D7_TICKETING.WB-SITEZ — Ticket Lifecycle v2 W-B: nudge SEMANTICS + a faster backstop — **THE STREAM IS DROPPED**

> ⛔ **RE-CUT 22:2xZ. DO NOT BUILD THE DDB STREAM. THE TRANSPORT IS DROPPED; THE LANE IS NOT.**
> *(`1.0.0_SA_CTO~Z` @3388 / @d7ca0bcd39, engineering recommendation on the numbers: **option (ii)**.
> Their words: **"W-B's AWS half stays held and on this recommendation SHOULD NOT BE BUILT AT ALL —
> which is a better outcome than building it correctly"**, and **"2.0.0_SA_COO~Z, that is a RE-CUT
> rather than a cancellation."**)*
>
> **EVERYTHING BELOW THE RE-CUT SECTION IS THE SUPERSEDED STREAM CUT, KEPT AS THE RECORD.** It is
> **NOT AN INSTRUCTION** and nothing in it is to be built. *It is retained rather than deleted
> because the reasoning that killed it is the deliverable — but a stale task order is an
> EXECUTABLE INSTRUCTION sitting in a live builder's lane, so the prohibition goes at the TOP,
> not in a footnote at the bottom.*

## ✅ THE RE-CUT — WHAT W-B IS NOW

**KEPT: the NUDGE SEMANTICS.** What a nudge means, what it carries, what the consumer does with it,
and the idempotency / one-digest discipline. That work was never about the transport and survives
it intact.

**DROPPED: the TRANSPORT.** No DynamoDB stream, no notifier Lambda, no new standing local consumer,
no new AWS-to-local hop. **Rung 1 of the build ladder is ANSWERED: the stream does not need to
exist for this requirement.**

**THE REPLACEMENT IS A SCHEDULE CHANGE ON THE EXISTING RUNNER** — no new surface at all.

✅ **SUPERSEDED BY EXERCISE 22:3xZ — 30s IS *REFUTED*, NOT UNESTABLISHED. THE FLOOR IS `PT1M`.**

*(Two seats, two independent test designs, converging. `0.5.0_AE_OpalETL~Z` @3444 ran the full
three-plane test with controls; `2.0.0_SA_COO~Z` ran a disabled far-future registration probe
chosen to read APPLIED without reaching EXERCISED. **Identical refusal: HRESULT `0x80041318`,
`(7,27):Interval:PT30S`, "incorrectly formatted or out of range".**)*

| plane | result | grounding |
|---|---|---|
| **DESIRED** — `New-ScheduledTaskTrigger -RepetitionInterval 30s` | **ACCEPTS**, returns `PT30S` | measured (CTO~Z, reproduced by AE~Z) |
| **APPLIED** — `Register-ScheduledTask` hands that object to the service | ⛔ **REFUSED, LOUDLY** | measured at **two seats, two designs** |
| **EXERCISED** at `PT30S` | unreachable **by construction** — nothing was ever stored to fire | — |
| **EXERCISED** at `PT1M` | fires **59.99s** apart, honoured to the tick | measured (AE~Z; **n=1 delta**, sufficient for "60s is honoured", **not** a jitter claim) |

**CONTROLS THAT MAKE IT A FLOOR RATHER THAN A FACT ABOUT `PT30S`** (AE~Z, each in isolation):
`PT59S` → **REFUSED, same element** (so: sub-minute floor). `PT1M` via the same two-step path →
**REGISTERS** (so the refusal is attributable to the VALUE, not the method). Hand-written XML via
`schtasks /Create /XML` → **REFUSED at different coordinates** `(30,27)` — **two genuinely different
documents hitting one validator, which attributes the constraint to the SERVICE rather than to
`schtasks.exe`.** Engine config mirrored the live task including `UseUnifiedSchedulingEngine`.

>> ✅ **AND THE FAILURE MODE IS THE ONE YOU WOULD DESIGN.** The worry this test was built on was a
**SILENT ROUND-UP** — a `PT30S` write quietly running at 60s, indistinguishable from success at the
call site. **IT DOES NOT DO THAT.** It refuses at registration and names both the element and the
value. Nobody can accidentally ship a 30s task that is secretly a 60s task. *Recorded as a property
of this box, because a mechanism that fails loudly on the exact axis you feared is rare enough to
write down.*

⛔ **CONSEQUENCE FOR THE CARD: THE 30s ROW LEAVES THE TABLE ENTIRELY** — it is not an option
carrying an asterisk, it is **not buildable**. And **"the stream's marginal benefit is approximately
equal to the wake hop it cannot touch" IS DEAD AND CANNOT BE REVIVED**: at the only reachable floor
the margin is **~28s against a ~14.13s hop**, twice over.

✅ **THE RECOMMENDATION IS UNCHANGED AT ~4:1, AND IS NOW THE BEST-SUPPORTED CLAIM IN THE LANE** —
it survived a pessimistic arrival model (BG), a pessimistic interval floor (COO~Z), the combined
worst corner (**~4.1:1**), *and* an exercised refutation of its own best-case row. **The honest
form: a schedule change buys ~120s for nothing; the stream buys ~28s for the estate's first
DynamoDB stream plus a new standing local process.**

---

*⬇ The original finding that opened this, kept because the reasoning is the deliverable: ⬇*

⛔ **~~BUT THE FLOOR IS UNESTABLISHED, AND THE QUOTED "~30s" MAY NOT BE REACHABLE ON THIS BOX.~~**
**MEASURED 2026-08-20 ~22:27Z** (positive control on the retrieval — the raw task query returned
1,570 chars; **two earlier greps came back EMPTY and were NOT read as answers**):

| fact | value | grounding |
|---|---|---|
| live `OPAL_D7_ticket_intake` repetition | `<Interval>PT5M</Interval>` | **MEASURED** (task XML) |
| `schtasks /Create /RI` unit | **"the repetition interval in MINUTES"** | **MEASURED** (help text) |
| whether the ENGINE honors a sub-minute `PT30S` | **UNMEASURED** | — |

>> **SO ONE MINUTE IS ESTABLISHED-REACHABLE AND THIRTY SECONDS IS UNESTABLISHED — NOT REFUTED.**
The XML schema is ISO-8601 and can *write* `PT30S`; whether Task Scheduler honors it is a different
question from whether the write succeeds.

**WB-R1 — SETTLE THE FLOOR ON THE REAL SURFACE BEFORE QUOTING A NUMBER.** Register a scratch task
carrying `<Interval>PT30S</Interval>`, then **READ THE REGISTERED TASK BACK.** ⛔ **THE WRITE
SUCCEEDING IS NOT THE ENGINE HONORING IT — a silent round-up to `PT1M` is indistinguishable from
success at the call site.** Minutes of work, no build, and it decides which number is real.

**WHY THE FLOOR IS NOT A DETAIL — it changes the SENTENCE, not just the digit:**

| floor | expected detect | + 14.13s wake | stream's marginal benefit |
|---|---|---|---|
| today, `PT5M` | ~150s | **~164s** | — |
| **`PT1M`** (established) | ~30s | **~44s** | **~28s — TWICE the wake hop** |
| `PT30S` (unestablished) | ~15s | **~29s** | ~13s — ≈ the wake hop |

>> ⛔ **"THE STREAM'S MARGINAL BENEFIT IS APPROXIMATELY EQUAL TO THE WAKE HOP IT CANNOT TOUCH" IS
TRUE AT 30s AND FALSE AT 1 MINUTE.** That sentence is the framing that makes the sovereign card
answerable in one word, and it is the single line that does not survive a 60s floor.
>> **THE ORDERING AND THE RECOMMENDATION HOLD EITHER WAY** — ~4:1 still favours the schedule change
decisively, and ~28s is still a thin return on the estate's first DDB stream plus a new standing
process. **What is fragile is a NUMBER and a SENTENCE, not the decision.**

⚠ **THE FOUR RATIFIED CONFIG DECISIONS WERE STREAM CONFIGURATION.** Their subject is dropped, so
they are **MOOT-BY-SUBJECT, not overturned** — recorded so nobody reads a surviving ratification as
a surviving instruction, and so they remain available intact if the stream is ever revisited.

**NOT FORECLOSED:** option (ii) does not prevent the stream later. If Andrew wants the last ~13–28
seconds, the cut is redone then — with the wake hop already measured underneath it.

---

# ⬇ SUPERSEDED — THE ORIGINAL STREAM CUT. RECORD ONLY. **NOT AN INSTRUCTION.** ⬇

# TO D7_TICKETING.WB-SITEZ — Ticket Lifecycle v2 W-B: DDB-Streams nudge ACCELERATOR on top of the scheduled backstop

<task_order id="D7_TICKETING.WB-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build: notifier + nudge contract; owns the runner/backstop substrate). Laptop apply leg (Terraform: stream + notifier Lambda) = EXECUTION PLACEMENT via 0.0.0_AB_MSTR~Z ferry.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>⛔ **RE-CUT: THE STREAM IS DROPPED. THIS FIELD'S ACTIVATION CONDITION IS BOTH *MET* AND *MOOT*.** (Corrected 23:31Z by 2.0.0_SA_COO~Z.) TAC-3 **DID** read schedule-landed — dep-3 ACCEPTED 19:59:41Z @399df8444a — so the trigger below fired ~3.5h ago. **AND IT NO LONGER MATTERS:** `1.0.0_SA_CTO~Z` @3388/@d7ca0bcd39 ruled option (ii) on the numbers and the DDB stream **is not to be built at all**. See the RE-CUT block at the top of this file — transport DROPPED, nudge SEMANTICS kept. **A field saying "staged, will activate" for a deleted transport is the exact stale-status class that cost two ticks on W-A today.** ⚠ SUPERSEDED TEXT: ~~staged — ACTIVATES when TAC-3 reads "schedule landed" (dep-3 registration + schedule-landed battery at this seat). 1.0.0_SA_CTO~Z @942d4d885c ruling 1: "dep-2/dep-3 land first, exactly as specified, and the stream is added ON TOP as W-B." This is CTO-ruled sequencing, not a COO-manufactured gate.~~ — the CTO sequencing quote remains TRUE OF ITS MOMENT and was SATISFIED, not violated.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ @942d4d885c — his O3 verbatim: "This write somehow triggers 0.0.3_BG that there is a new ticket..." ("somehow triggers" = his latitude); 1.0.0_SA_CTO~Z ruling 1 (NUDGE MODEL): DDB Streams → small notifier → BG nudge as the FAST path PLUS the 5-min Scheduled Task as the standing backstop — a production pipeline must have a SCHEDULE, event-driven is the accelerator (CLAUDE.md law). The nudge path is ANDREW-ASKED (his flow step O3/O7/O8) — not moratorium machinery.</authority>
</task_order>

## ✅ RULED 22:20Z — W-B's AWS HALF IS **HELD**, AND THE BUILD-LADDER QUESTION COMES FIRST

*(`1.0.0_SA_CTO~Z` @3341, reversing their own "build" of an hour earlier. **A SPEC FACT, not a
manufactured gate — nobody signs anything**, and the four ratified config decisions stand for
whenever it proceeds.)*

**(b) RUNG 1, AND NOBODY HAD ASKED IT: DOES THE STREAM NEED TO EXIST?**

| option | detection | delivery | cost |
|---|---|---|---|
| **shorten the schedule** | ~30s | **~30s** | **NO new surface** |
| stream + fast local consumer | sub-second | seconds | the estate's **FIRST DDB stream** + a **new standing local process** + a **new failure domain** |

>> **Whether ~30s → ~2s is worth that is a COST/BENEFIT CALL ON NEW INFRASTRUCTURE, not a technical
one — and option (ii) must be answered BEFORE option (i) is costed.**

✅ **(c) IS ALREADY SATISFIED — THE WAKE HOP WAS MEASURED AT 21:32Z, 48 MINUTES BEFORE THE RULING
THAT CALLS IT UNMEASURED.** (`0.0.3_BG_BBGTerminal` msg 3098, on **real traffic, by hand, three
independent clocks**: send 21:29:12.081Z → emit 21:29:24.564Z = **DETECT 12.48s** → ACK
21:29:38.692Z = **WAKE-AND-ACT 14.13s**; total 26.61s against ~128s for the same-shaped exchange that
morning.) *It arrived inside tonight's message volume and was only connected once the ruling named
the number to look for — so the decision the gate sequenced is available NOW, not after another pass.*

**APPLYING THE GATE'S OWN TEST.** ⚠ **MEASURED vs MODELLED, labelled:** the **14.13s wake floor is
MEASURED**; the expected-detect figures are **MODELLED on a uniform-arrival assumption — an
assumption, not an observation.**

| option | expected detect | + wake | expected total |
|---|---|---|---|
| today, 5-min backstop | ~150s (worst 300s) | +14s | **~164s** |
| **(ii) 30s schedule** | ~15s | +14s | **~29s** |
| (i) stream | ~1–2s | +14s | **~16s** |

>> ⛔ **THE FIRST STEP BUYS ~135 SECONDS; THE SECOND BUYS ~13.** The 5-min → 30s move is roughly
**TEN TIMES** the improvement of the 30s → stream move — **at NO new infrastructure, NO first-ever DDB
stream, NO new standing local process, and NO new failure domain.**
>> **THE STREAM'S MARGINAL BENEFIT IS APPROXIMATELY EQUAL TO THE WAKE HOP IT CANNOT TOUCH** — exactly
the disappearance the gate's step 2 existed to reveal, now with numbers instead of a prediction.

⛔ **AND THE STATED BOUND MAKES THE CONCLUSION STRONGER, NOT WEAKER:** 14.13s is a **WARM-SCHEMA**
figure; a cold session still pays the deferred-schema cost until S2 lands. **So the true wake floor is
14.13s OR MORE, and every second it is larger swallows more of the stream's marginal 13s. The
uncertainty runs TOWARD option (ii), not against it.**

⚠ **NOT CLAIMED** (the builder's own bounds, kept): this is a **cost/benefit input, not a ruling**;
the arrival-distribution model is theirs rather than measured, and **if tickets cluster at a known
hour the expected-value arithmetic shifts**. A 30s schedule also has an uncosted cost — **10× the
invocations** of a Lambda-free local task, cheap but not free, plus the box's own load tolerance.

**(c-original) THEN MEASURE THE WAKE HOP AND DECIDE ON NUMBERS, not architecture preference.** ⛔ **If the wake
hop is TENS OF SECONDS, the difference between the two options DISAPPEARS INTO IT** — which is
precisely what the measure-first step exists to reveal before anyone funds a build.

**(d) CARDED TO ANDREW.** He asked for exactly this; the answer is **POSSIBLE, AND THE LAST HOP INTO
THIS BOX IS THE PART THAT IS NOT.** The costs are his — and **the DL being authorized as the FIRST
LINE materially lowers what this accelerator has to buy.**

⚠ **TWO OF THE REASONS WERE THE GATE'S OWN, corrected by them rather than by anyone catching it:**
**(1)** their scoping claimed *"emit to the queue this box ALREADY long-polls — ZERO NEW
INFRASTRUCTURE"* — **FALSE: that queue is the agentbus, which is COORDINATION-ONLY by standing rule.**
Option (i) is a NEW queue **plus** a NEW standing consumer, not a reuse. *A cost claim based on a
resource's EXISTENCE without checking its CHARTER.* **(2)** they **cleared past their own sequencing
ruling** — *measure the wake hop before funding a transport build* — **and the wake hop is still
unmeasured.**

⛔ **NOT HELD:** W-A's apply, W-C, W-F, the channel leg, or anything else. **W-B's AWS half alone** —
stated so no adjacent lane infers a hold from this one.

## ⛔ THE FINDING THAT PRODUCED THE HOLD — THE LAST ARROW HAS NO MECHANISM (22:15Z)

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
