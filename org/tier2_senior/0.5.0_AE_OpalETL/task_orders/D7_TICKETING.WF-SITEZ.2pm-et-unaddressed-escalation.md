# TO D7_TICKETING.WF-SITEZ — the 2pm ET UNADDRESSED-REQUEST escalation on the thread

<task_order id="D7_TICKETING.WF-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (engine/runner owner — the build-ladder call below is YOURS as the seat that owns the live runner). Laptop apply leg if the definition rides a Lambda field = via 0.0.0_AB_MSTR~Z ferry.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:4xZ</issued>
<status>staged — TWO DESIGN ANSWERS REQUIRED BEFORE BUILD (trading-calendar behavior; the definition of ADDRESSED). Both are named below; neither is a build-time discovery.</status>
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

## ⛔ TWO ANSWERS REQUIRED BEFORE BUILD

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
realities**: a channel post wakes nobody until the channel leg lands. `1.0.0_SA_CTO~Z` rules it.

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

## Acceptance criteria (D7F pattern)
- **WF-1** BOTH DESIGN ANSWERS RECORDED FIRST: the trading-calendar behavior and the `addressed`
  definition, each stated in the record before the build lands.
- **WF-2** POSITIVE, EXERCISED: a ticket created before 2p ET and left unaddressed produces exactly
  one escalation message on the thread at the 2p boundary, carrying the ticket id + deep link per
  the serve rules (and `confirm=true` — the gateway's tool-wide irreversible-send fence).
- **WF-3** NEGATIVE CONTROLS, each exercised and each exiting distinctly: a ticket created **after**
  2p → no escalation; a ticket created before 2p and **addressed** → no escalation (the definition
  chosen in (2) is what this tests); already-escalated → **no duplicate** at the next pass
  (idempotency, the same cursor discipline the buzz path already proved on real traffic).
- **WF-4** ⛔ **THE TRADING-DAY CONTROL, RUN AS A CONTROL:** on a non-trading day the sweep behaves
  as ruled in (1) — **exercised against the calendar, not reasoned about.** If the ruling is "do not
  fire", a simulated Saturday must produce ZERO escalations for a ticket that a wall-clock sweep
  WOULD have escalated (the mutant: remove the calendar guard → it fires → the test fails).
- **WF-5** BOUNDARY-COUPLING: the escalation boundary and the client-facing cutoff read from ONE
  source; a mutant changing the cutoff moves the escalation with it (they cannot drift).
- **WF-6** NO-REGRESSION: the 5-min buzz path, its cursor, and the exit contract behave unchanged;
  the escalation leg failing must NOT break the buzz leg (exercised, given the runner is live
  production infrastructure).
- **WF-7** Proof instance VALID rc=0 POSITIONAL, ids WF-1..WF-9 (rc unpiped).
- **WF-8** ⛔ **FAILURE ISOLATION, EXERCISED IN THE EXPENSIVE DIRECTION:** with the sweep leg forced
  to raise (scratch fault injection), **the buzz path still fetches, still buzzes, and still exits
  on its own contract** — the sweep's failure carries its OWN distinct exit code and neither masks
  nor preempts the client-facing SLA path. The mutant is the proof: share the exception boundary →
  a sweep fault stops the buzzes → the test FAILS.
- **WF-9** **OWN STATE KEY:** the sweep's `last_swept_date` (or equivalent) is separate from the
  forward-only buzz cursor, exercised across a day boundary; and the cursor's own value is
  **byte-unchanged** by a sweep pass (the two state shapes provably do not contaminate each other).

<proof_of_spec>
  <expected_criteria>WF-1,WF-2,WF-3,WF-4,WF-5,WF-6,WF-7,WF-8,WF-9</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WF_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<compiler_tools_mandate>
Before write: read `lib/trading_calendar.py` at source (the one frontier definition — never
re-implement a calendar); `comp-blast` on the runner before adding a responsibility to it.
Before commit: commit-gate. Exercise, never compile-and-assume — the runner execs live every 5 min.
</compiler_tools_mandate>

<cross_domain_coordination>
`integrations/ticketing/intake/` is this seat's own — BUT IT IS LIVE PRODUCTION INFRASTRUCTURE under
a 5-minute schedule, so every edit is effectively a deploy the moment it hits disk. If the
`addressed` definition rides `first_response_at`, this TO is W-A-DEPENDENT and the Lambda leg is
laptop-applied. Coordinate with the channel-leg P1 (same file family, ruled to build on TAC-2' close).
</cross_domain_coordination>

## Do not
No wall-clock sweep without the trading-calendar answer. No alarm/monitor machinery — this is a
scheduled FEATURE he asked for. Do not let the escalation boundary and the client cutoff become two
constants. Do not ship a weaker definition of "addressed" silently — record which one shipped.

## Reporting
Completion → 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance) + 0.0.0_AB_MSTR~Z (ferry).
Surprise channel: one line to 2.0.0_SA_COO~Z. Session log = deliverable.
