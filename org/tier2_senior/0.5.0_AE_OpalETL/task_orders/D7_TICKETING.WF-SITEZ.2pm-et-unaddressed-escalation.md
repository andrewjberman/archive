# TO D7_TICKETING.WF-SITEZ — the 2pm ET UNADDRESSED-REQUEST escalation on the thread

<task_order id="D7_TICKETING.WF-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (engine/runner owner — the build-ladder call below is YOURS as the seat that owns the live runner). Laptop apply leg if the definition rides a Lambda field = via 0.0.0_AB_MSTR~Z ferry.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:4xZ</issued>
<status>staged — **BOTH design forks RULED BY ANDREW ~20:50Z @0d82b6ce91 and BOTH SHRINK THIS CUT**: no trading-calendar limb, and ADDRESSED == ACCEPTED/CLAIMED (predicate `status == open`), so **ZERO W-A DEPENDENCY — this no longer sequences behind W-A**. **AND the remaining two are now RULED at the `1.0.0_SA_CTO~Z` gate @c9459dfa2f: WHICH THREAD = INTERNAL by default** (telling the CLIENT we were late is a product decision, carded to Andrew — which also dissolves the client-contradiction risk entirely), **and RE-ESCALATION = ONE DIGEST PER SWEEP**, not N messages. **NO DESIGN QUESTIONS REMAIN.** What is left is engineering: own state key, failure isolation, the cap assertion, one config.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~20:45Z, record @11d274f8c2. VERBATIM: *"we need the agent to be messaging on the thread if there is a service request that was issued prior to naive 2p ET, which has still not been addressed by 2p ET. THat is a feature that needs to be worked in."*
⛔ **MORATORIUM: SATISFIED BY EXPLICIT ASK — his verbatim above IS the `# andrew-asked` marker.** And note the shape is already correct by law: this is a **SCHEDULED CHECK**, which is what a production pipeline must be. It is a FEATURE he asked for, not detection machinery.</authority>
</task_order>

## Objective
At **naive 2p ET**, any service request **issued before 2p ET** that is **still not addressed**
gets an agent message on the "Opal Client Tickets" thread.

**"NAIVE 2p ET" matches the estate's existing scheduling grain.** The D7 runner is registered
`5-min RepetitionInterval, 24x7, naive-local`, and this box's local clock IS ET (measured: runner
`lastRun 15:59:45 local` == `19:59:45Z`). So "naive 2p" = **the box reading 14:00, no DST
arithmetic** — the same grain the schedule already uses.

**2p ET IS ALREADY THE PRODUCT'S CUTOFF.** The client ack renders *"after today's 2:00 PM ET
cutoff, so expect it on the next trading day"* (D7F-11, exercised on PROD in the water test).
**The escalation boundary and the cutoff are the same boundary and MUST NOT be allowed to drift
apart** — if one moves, both move, and the config that carries it should make that structural
rather than a convention.

## ✅ BOTH DESIGN FORKS **RULED BY ANDREW** ~20:50Z (record @0d82b6ce91) — THEY SHRINK THIS CUT

**VERBATIM:** *"No it is fine to escalate saturday tickets or sunday tickets, if we get a ticket and
we're delaying on it, we need to know about it. If a user has already accepted it, then we dont need
to buzz it again, the issue is simply making sure that tickets are not left open without anyone
accepting them"*

**RULING 1 — NO TRADING-CALENDAR QUALIFICATION.** The sweep is **wall-clock, every day, weekends
included.** `lib/trading_calendar.py` **does not enter this feature.**
⛔ **AND THE RECORD STATES WHY THIS IS NOT A NEVER#1 VIOLATION, so a future reader does not "fix"
it:** NEVER#1 governs calling a **DATA PIPELINE** stale on wall-clock age. This is an
**internal-awareness escalation about WORK SITTING UNACCEPTED** — and a client waiting across a
weekend is exactly what he wants surfaced, not suppressed. **The client-facing "expect it on the
next trading day" ack is a DIFFERENT AUDIENCE and is unaffected:** internal awareness of a delay
does not alter the client's stated SLA.

**RULING 2 — "ADDRESSED" MEANS ACCEPTED / CLAIMED, not replied-to.** The predicate is
**`status == open`** on TODAY's deployed row → **ZERO W-A DEPENDENCY; this feature ships on data
that exists now.**
⚠ **SUPERSEDED, AND RECORDED HONESTLY RATHER THAN SOFTENED:** the engine owner's finding (msg 2864
item 6) that a status predicate misses **claimed-but-unanswered** was **correct as analysis** — and
his word puts that population **explicitly OUT OF SCOPE** for this feature. The finding was right;
the scope call was his. `first_response_at` remains a valid W-A field for other purposes; it is
**not** this feature's definition. **The sequencing recommendation to place this after W-A is
therefore withdrawn — no W-A dependency remains.**

**RESIDUAL, NAMED SO IT IS DECIDED RATHER THAN EMERGENT:** his word settles ACCEPTED as the stop
condition but does not state the **re-escalation cadence** for a ticket still unaccepted across
successive days. `0.0.0_AB_MSTR~Z`'s lean, offered for correction: **escalate again each day it is
still unaccepted** — it is still the problem he described, and silence after day one would
re-create the invisibility this feature exists to remove. **`1.0.0_SA_CTO~Z` states the choice.**

## ⛔ SUPERSEDED — the pre-ruling fork text (preserved for provenance, NOT the spec)

**(1) THE TRADING-CALENDAR QUESTION — NEVER#1 CLASS, and it BITES IN TWO PLACES, not one**
(engine owner msg 2864 item 5; folded because the second place is easy to miss):
- **(i) WHETHER THE SWEEP RUNS AT ALL.** An unqualified 2p sweep on a Saturday escalates
  Friday-afternoon tickets **correctly waiting for Monday** — manufacturing an escalation about a
  system behaving exactly as designed, on the client-facing surface.
- **(ii) THE AGE PREDICATE ITSELF.** The product's own client ack promises *"expect it on the next
  trading day"* — so **lateness must count in TRADING DAYS, or the sweep contradicts the promise the
  client was already given.** A wall-clock age predicate can call a ticket late that the client was
  told to expect later.

`lib/trading_calendar.py` is the ONE frontier definition and carries what this needs —
`is_trading_day`, `expected_last_trading_day`, `trading_days_behind` (function list **read at HEAD**
by the engine owner, not assumed). **Answer both, then build. Never re-implement a calendar.**

**(2) "ADDRESSED" HAS NO FIELD TODAY — and the cheap answer has a hole exactly where it matters.**
On the **currently deployed** row the only signal is `status` (`open | in_progress | completed`).
W-A's day-one set adds **`first_response_at`** (plus `claimed_at`/`claimed_by`).

⛔ **THE FORK IS NOT MERELY EARLY-VS-LATE — THE EARLY VERSION UNDER-REPORTS BY CONSTRUCTION**
(engine-owner measurement, `0.5.0_AE_OpalETL~Z` msg 2864 item 6, folded here before build):
- **(i) SHIP ON `status` NOW** — zero W-A dependency, implementable immediately. **But "not
  addressed == still `open`" SILENTLY EXCLUDES CLAIMED-BUT-UNANSWERED**: a ticket someone claimed at
  9am and never replied to sits `in_progress`, so the sweep skips it — **and that is plausibly the
  exact case Andrew means by "not addressed."** The cheap definition misses precisely the population
  a human would consider the worst kind of late.
- **(ii) RIDE W-A for `first_response_at`** — catches that population; costs the W-A dependency.
**Whichever ships, the record states WHICH definition shipped AND WHAT IT DOES NOT COVER, in those
words** — otherwise the gap reads as coverage, which is the failure mode that makes an
under-reporting sweep worse than none.

**⚠ OPEN DESIGN INPUT — WHICH THREAD? (`0.5.0_AE_OpalETL~Z` cannot answer this from the engine, and
neither can I.)** *"An agent message on the thread"* — the client's own chat, or the "Opal Client
Tickets" channel? Different surfaces, different audiences, and **today different consumer
realities**: a channel post wakes nobody until the channel leg lands.

⛔ **AND THIS FORK GAINED A CONSEQUENCE IT DID NOT HAVE AN HOUR AGO** (`0.5.0_AE_OpalETL~Z` 2879,
folded ~20:53Z): **the weekend ruling's coherence DEPENDS ON THIS ANSWER.** Wall-clock
weekend escalation is fully coherent for an **INTERNAL** audience — it is exactly the delay Andrew
wants surfaced. But **if the escalation posts to the CLIENT's own chat, it collides with the ack the
product already gave that same client** — *"expect it on the next trading day"* — so on a Saturday
Opal would tell a client their request is overdue **after telling them to expect it Monday**: two
Opal surfaces contradicting each other to one person. **If it is the internal channel, no tension
exists at all.** The two rulings are independently correct and only interact here.

## BUILD LADDER — ANSWERED BY MEASUREMENT, not estimate (engine owner, msg 2864)

The runner's fetch is `GET /api/scoped/tickets?status=open&limit=500` — **it already returns EVERY
open ticket every pass**, and new-since-cursor is applied CLIENT-side inside `run_once`. So the
sweep is **a SECOND PREDICATE OVER DATA ALREADY IN HAND: no new API call, no new credential, no new
schedule, no new deploy surface.** That is rung 2 settled by measurement rather than plausibility.

⛔ **BUT TWO STRUCTURAL CONSTRAINTS COME WITH IT, and both are build-blocking:**

**(A) THE TWO DUTIES HAVE OPPOSITE STATE SHAPES — the cursor STRUCTURALLY CANNOT SERVE THE SWEEP.**
The cursor is a **forward-only high-water mark** ("what is new"). A sweep looks **BACKWARD** at rows
already behind that mark. Reusing the cursor would either re-buzz or find nothing. **The sweep needs
its OWN state key** — a `last_swept_date` attribute on the same config item is the cheap correct
form (same item, no second store). *Grain:* at a 5-min cadence, "at 2p" resolves to **the first pass
on or after 14:00 local that has not yet swept today.**

**(B) FAILURE ISOLATION — the load-bearing constraint, and the honest answer to the
"second-responsibility-on-live-production-infra" counterweight.** The buzz path is the
**client-facing SLA path**. Today `run_once` aborts the whole pass on a fetch failure and STOPS on
`SEND_FAILED` (ordered retry, deliberate). **If the sweep shares that control flow, a sweep bug can
silently stop new-ticket buzzes** — the expensive failure. **Therefore: the sweep runs STRICTLY
AFTER the buzz work, inside its OWN exception boundary, with its OWN distinct exit code that can
never mask or preempt the buzz path's.** A second duty is fine; **a shared failure domain is not.**

## ⛔ BINDING DESIGN RULINGS — `1.0.0_SA_CTO~Z` gate @c9459dfa2f / @21bd23d943 (folded ~20:56Z)

**(1) WHICH THREAD — RULED INTERNAL BY DEFAULT.** The escalation says *Opal has not answered* — it
is **addressed to Opal**. Telling the CLIENT we were late is a **product decision and Andrew's**;
carded, not assumed. ✅ **This also DISSOLVES the contradiction I flagged:** internal audience means
the weekend ruling and the client's "next trading day" ack never meet.

**(2) ONE CONFIG — the escalation reads the EXISTING `CUTOFF_ET`.** A second `14:00` literal means
the ack promises the client one boundary while the escalation enforces another. (This is WF-5,
now ruled rather than proposed.)

**(3) ⛔ THE `limit=500` IS A CAP, NOT A TOTAL — AND THE SWEEP MUST ASSERT IT DID NOT HIT IT.**
`1.0.0_SA_CTO~Z`'s own addition, and it is the sharpest one: at 501 open tickets the sweep
**silently stops seeing the OLDEST** — the truncated-page class landing on **the one mechanism whose
entire job is noticing what was missed.** A sweep that under-reads its own input fails exactly where
it is supposed to succeed.

**(4) RE-ESCALATION — ONE DIGEST PER SWEEP, NOT N MESSAGES.** A still-unaccepted ticket DOES escalate
again (silence after day one re-creates the invisibility the feature removes), **but as ONE digest**:
the ticket's own thread gets ONE marker; the DL gets a daily digest. **N-per-day escalations train
the reader to ignore them — which is how a backstop dies without anyone deciding to kill it** — and
a digest **carries its own denominator for free**, satisfying (3).

## ⛔ THE COUPLING THAT CHANGES WHAT THIS TO IS (gate §7 — read this before building either W-E or W-F)

**KEY THE CHECK ON THE WORK, NOT ON THE AGENT.** Two binding consequences:
- **(i) THE ESCALATION MUST RUN INDEPENDENT OF THE AGENT WHOSE DEAFNESS IT CATCHES.** As an agent
  duty it would inherit that deafness — **a check that fails in the same mode as the thing it checks
  is not a check.** It runs on the **SCHEDULED RUNNER**. *(Two independent routes reached this
  placement — engine economics and failure analysis — which is the strongest evidence it is right.)*
- **(ii) IT MUST DELIVER ON A PATH THAT IS NOT THE DEAF SURFACE.** Detection survives deafness;
  **delivery does not.** A channel-only escalation puts the backstop's output into the exact surface
  whose deafness it backstops.

>> **THEREFORE: THE ESCALATION DETECTS, THE EMAIL DL DELIVERS — the two mechanisms Andrew named in
one breath are ONE mechanism.** W-F and **W-E are coupled by design, not merely adjacent**: W-E is
not only the human first-line, it is the **deafness-independent delivery path** for W-F's output.
Neither should be scoped as if the other were optional.

## Acceptance criteria (D7F pattern)
- **WF-1** BUILT TO THE RULED DEFINITIONS: predicate is `status == open` (ACCEPTED/CLAIMED stops the
  escalation), **wall-clock daily, no calendar limb**, and the **re-escalation cadence** stated by
  `1.0.0_SA_CTO~Z` is implemented as stated. Evidence cites @0d82b6ce91.
- **WF-2** POSITIVE, EXERCISED: a ticket created before 2p ET and left unaddressed produces exactly
  one escalation message on the thread at the 2p boundary, carrying the ticket id + deep link per
  the serve rules (and `confirm=true` — the gateway's tool-wide irreversible-send fence).
- **WF-3** NEGATIVE CONTROLS, each exercised: a ticket created **after** 2p → no escalation; a
  ticket created before 2p and **ACCEPTED/CLAIMED** (`status != open`) → **no escalation** — his
  *"If a user has already accepted it, then we dont need to buzz it again"*, tested directly;
  already-escalated → **no duplicate within the day** (idempotency on the sweep's own state key,
  the discipline the buzz path already proved on real traffic).
- **WF-4** ⛔ **WEEKEND BEHAVIOR, EXERCISED IN THE DIRECTION HE RULED (inverted by @0d82b6ce91):** a
  simulated **Saturday** with an unaccepted pre-2p ticket **DOES escalate** — the sweep is wall-clock
  by his word. **The mutant is now the opposite one:** adding a calendar guard must make the test
  FAIL, which is what stops a future reader from "fixing" this into a NEVER#1-shaped suppression.
  Assert `lib/trading_calendar.py` is **not imported** by this path.
- **WF-5** BOUNDARY-COUPLING: the escalation boundary and the client-facing cutoff read from ONE
  source; a mutant changing the cutoff moves the escalation with it (they cannot drift).
- **WF-6** NO-REGRESSION: the 5-min buzz path, its cursor, and the exit contract behave unchanged;
  the escalation leg failing must NOT break the buzz leg (exercised, given the runner is live
  production infrastructure).
- **WF-7** Proof instance VALID rc=0 POSITIONAL, ids WF-1..WF-12 (rc unpiped).
- **WF-8** ⛔ **FAILURE ISOLATION, EXERCISED IN THE EXPENSIVE DIRECTION:** with the sweep leg forced
  to raise (scratch fault injection), **the buzz path still fetches, still buzzes, and still exits
  on its own contract** — the sweep's failure carries its OWN distinct exit code and neither masks
  nor preempts the client-facing SLA path. The mutant is the proof: share the exception boundary →
  a sweep fault stops the buzzes → the test FAILS.
- **WF-9** **OWN STATE KEY:** the sweep's `last_swept_date` (or equivalent) is separate from the
  forward-only buzz cursor, exercised across a day boundary; and the cursor's own value is
  **byte-unchanged** by a sweep pass (the two state shapes provably do not contaminate each other).
- **WF-10** ⛔ **THE CAP ASSERTION (gate ruling 3):** every sweep pass **asserts it did not hit the
  `limit=500` cap**, and says so in its output with the count beside the cap. Exercised in the
  failing direction: a fixture at/over the cap must make the sweep **declare the truncation
  loudly**, never silently sweep a partial set. *The mechanism whose job is noticing what was
  missed must not be able to miss silently.*
- **WF-12** ⛔ **THE SWEEP WRITES NO TERMINAL STATE, EXERCISED:** after a sweep pass over an
  unaccepted ticket, the row's `status` and `closure_reason` are **byte-unchanged** — the sweep
  escalated and disposed nothing. Mutant: have the sweep set any terminal value → the test
  FAILS. *(Opal-side ageout is not terminal, and closing on ageout would delete the very signal
  this feature raises.)*
- **WF-11** **ONE DIGEST PER SWEEP (gate ruling 4):** N unaccepted tickets produce **ONE** digest
  message carrying its own denominator, not N messages; the ticket's own thread gets ONE marker.
  Exercised with N>1. **Delivery follows the coupling above — the deafness-independent path (W-E),
  not the channel alone.**

<proof_of_spec>
  <expected_criteria>WF-1,WF-2,WF-3,WF-4,WF-5,WF-6,WF-7,WF-8,WF-9,WF-10,WF-11,WF-12</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WF_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<compiler_tools_mandate>
Before write: read `lib/trading_calendar.py` at source (the one frontier definition — never
re-implement a calendar); `comp-blast` on the runner before adding a responsibility to it.
Before commit: commit-gate. Exercise, never compile-and-assume — the runner execs live every 5 min.
</compiler_tools_mandate>

<cross_domain_coordination>
⛔ **THE DEPLOY FUSE IS A PROPERTY OF THE PATH, NOT OF THE WORK — `1.0.0_SA_CTO~Z` RULING 3a
@123071c5cd, which WIDENED its own earlier bar.** The Task's `Execute` is `run_intake.cmd` **in the
working tree**, so **EIGHT artifacts are live production, edited in place, with no deploy step**
(DENOMINATOR: 8) — `run_intake.cmd` · `runner.py` · `intake_pass.py` · `buzz.py` · `receipt.py` ·
`row_contract.py` · `runner_config.json` · `.claude/skills/teams-assist/teams-watch.py`.
**A5/A6/A7 BIND ON ANY EDIT TO ANY OF THEM, FOR ANY REASON** — a typo, a docstring, a comment, a
config value. *"The hazard is not a property of the work being done, it is a property of the file
being saved — and the next person to edit one of these will not be someone who read this ruling."*
⚠ **STATED BOUND, carried so nobody reads a clean result that was not obtained:** only
`OPAL_D7_ticket_intake` was fully resolved. Three other scheduled tasks execute through
`cmd.exe`/`wscript.exe` and their `Arguments` plane was NOT read — **their working-tree exposure is
UNMEASURED, NOT ABSENT.**

`integrations/ticketing/intake/` is this seat's own — BUT IT IS LIVE PRODUCTION INFRASTRUCTURE under
a 5-minute schedule, so every edit is effectively a deploy the moment it hits disk. **NO W-A
DEPENDENCY** (his ~20:50Z ruling: the predicate is `status == open` on the deployed row) — so this
touches the runner only, **no Lambda leg and no laptop apply**. Coordinate with the channel-leg P1
(same file family, ruled to build on TAC-2' close). *~~If the `addressed` definition rides
`first_response_at`, this TO is W-A-DEPENDENT and the Lambda leg is laptop-applied~~ — superseded
@0d82b6ce91.*
</cross_domain_coordination>

## ⛔ THE SWEEP NEVER WRITES A TERMINAL STATE (closure_reason record, ADOPTED @f834702451 21:14Z)

**The ruling names THIS SWEEP as the thing that would misuse the value**, so the guard belongs in
this TO rather than being discovered at the wiring: the value once called `expired` is **RENAMED
`requester_unresponsive`** precisely because its **definition is requester-bound** while its old name
invited *"whoever wires the sweep's terminal handling"* to reach for it as an **Opal-side ageout**.

>> **AND OPAL-SIDE AGEOUT IS NOT TERMINAL.** A ticket nobody has accepted is **not** closed, expired,
or disposed by the passage of time — **it is exactly the ticket this feature exists to make VISIBLE.**
**The sweep ESCALATES; it never closes, never sets `closure_reason`, and never writes any terminal
`status`.** Closing on ageout would delete the very signal the escalation is built to raise, and
would do it under a value whose definition describes the requester, not us.

## Do not
⛔ **The sweep writes NO terminal state and NO `closure_reason` — see above.**
⛔ **Do NOT add a trading-calendar limb — that is the "fix" his ruling exists to prevent** (WF-4's
mutant is now the guard against it). No alarm/monitor machinery — this is a scheduled FEATURE he
asked for. Do not let the escalation boundary and the client cutoff become two constants. Do not
re-scope toward claimed-but-unanswered: **ACCEPTED is the stop condition by his word**, and that
population is explicitly out of scope for this feature.

## Reporting
Completion → 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance) + 0.0.0_AB_MSTR~Z (ferry).
Surprise channel: one line to 2.0.0_SA_COO~Z. Session log = deliverable.
