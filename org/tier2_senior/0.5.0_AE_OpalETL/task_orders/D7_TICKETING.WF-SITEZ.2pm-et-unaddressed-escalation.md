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

**(1) THE TRADING-CALENDAR QUESTION — NEVER#1 CLASS, and it must be answered at design time, not
discovered on a Saturday.** The cutoff's own client-facing wording is **trading-day-shaped** ("the
next trading day"). Does the 2p sweep fire on a weekend or a market holiday? **An unqualified
wall-clock daily sweep will escalate Saturday tickets that are correctly waiting for Monday** —
manufacturing an escalation about a system behaving exactly as designed, on the client-facing
surface. `lib/trading_calendar.py` is the ONE frontier definition
(`expected_last_trading_day` / `trading_days_behind`). **Answer it, then build.**

**(2) "ADDRESSED" HAS NO FIELD TODAY — and the honest definition has a dependency.**
On the **currently deployed** row the only available signal is `status` still `open`. W-A's day-one
field set adds **`first_response_at`** (plus `claimed_at`/`claimed_by`), which is the richer and
more honest definition — *addressed* means someone responded, not merely that the row left `open`.
**THE FORK, stated so it is chosen rather than defaulted into:**
- **(i) SHIP ON `status` NOW** — available immediately; but it calls a ticket "addressed" the moment
  its status changes, which is a **weaker claim than the word means**.
- **(ii) RIDE W-A for `first_response_at`** — the honest definition; costs the W-A dependency.
**Whichever is chosen, the TO records WHICH definition shipped, in the record, in those words** —
so a future reader never has to infer what "addressed" meant on a given date.

## BUILD LADDER — this is plausibly a CONDITIONAL, not a new pipeline

The D7 runner **already fires every 5 minutes** and **already reads the board**. A 2p-window
evaluation is plausibly a conditional inside the existing pass — rung 2 (the estate already has it),
not rung 7 (new code). ⚖ **COUNTERWEIGHT, and it is real:** that runner is now **live production
infrastructure** carrying the client-facing buzz path; adding a second responsibility to it is a
coupling decision. **`0.5.0_AE_OpalETL~Z` owns this call as the engine owner** — either shape is
legitimate; what is not legitimate is drifting into one without naming it.

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
- **WF-7** Proof instance VALID rc=0 POSITIONAL, ids WF-1..WF-7 (rc unpiped).

<proof_of_spec>
  <expected_criteria>WF-1,WF-2,WF-3,WF-4,WF-5,WF-6,WF-7</expected_criteria>
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
