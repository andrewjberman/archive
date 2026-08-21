# TO D7_TICKETING.WF-SITEZ — the 2pm ET UNADDRESSED-REQUEST escalation on the thread

<task_order id="D7_TICKETING.WF-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (engine/runner owner — the build-ladder call below is YOURS as the seat that owns the live runner). Laptop apply leg if the definition rides a Lambda field = via 0.0.0_AB_MSTR~Z ferry.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:4xZ</issued>
<status>staged — **BOTH design forks RULED BY ANDREW ~20:50Z @0d82b6ce91 and BOTH SHRINK THIS CUT**: no trading-calendar limb, and ADDRESSED == ACCEPTED/CLAIMED (predicate `status == open`), so **ZERO W-A DEPENDENCY — this no longer sequences behind W-A**. **AND the remaining two are now RULED at the `1.0.0_SA_CTO~Z` gate @c9459dfa2f: WHICH THREAD = INTERNAL by default** (telling the CLIENT we were late is a product decision, carded to Andrew — which also dissolves the client-contradiction risk entirely), **and RE-ESCALATION = ONE DIGEST PER SWEEP**, not N messages. ⛔ **DELIVERY SURFACE: the CHANNEL IS EXCLUDED (settled 21:39Z), the POSITIVE surface is NOT YET NAMED.** Andrew's ~21:35Z ruling makes the "Opal Client Tickets" channel CLIENT-ORIGINATED ONLY; by the gate's own origin axis this escalation is AGENT-CAUSED (it reports Opal's inaction), and the interim is "nothing agent-caused goes in that channel" — so that surface is OUT by ruling, not by caution. **DO NOT BUILD THE DELIVERY LEG until `1.0.0_SA_CTO~Z` names the surface it DOES use** (the detect/deliver seam points at the email DL). The DETECTION half is buildable now. Everything else is unchanged and buildable: predicate, wall-clock cadence, own state key, failure isolation, the cap assertion, one config, no terminal writes.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~20:45Z, record @11d274f8c2. VERBATIM: *"we need the agent to be messaging on the thread if there is a service request that was issued prior to naive 2p ET, which has still not been addressed by 2p ET. THat is a feature that needs to be worked in."*
⛔ **MORATORIUM: SATISFIED BY EXPLICIT ASK — his verbatim above IS the `# andrew-asked` marker.** And note the shape is already correct by law: this is a **SCHEDULED CHECK**, which is what a production pipeline must be. It is a FEATURE he asked for, not detection machinery.</authority>
</task_order>

<!-- ==================== WF-5 SOURCING: RULED (c) 00:03Z, 1.0.0_SA_CTO~Z @4000 ==================== -->
<!--
✅ WF-5 CUTOFF SOURCING = OPTION (c): add `cutoff_et` to the LIST response at
   infra/aws/lambda/ticket_center/lambda_function.py:410, mirroring the /submit 201 echo at :355.

⛔ AND THE OBJECTION I RAISED AGAINST IT WAS FALSE ON MEASUREMENT -- MINE, and one `git log` away.
   I framed (c)'s cost as "one Lambda apply" that "re-opens a laptop apply leg the TO closed."
   MEASURED: that file ALREADY CARRIES THREE UNAPPLIED W-A COMMITS -- 81c502cff2, 9121a55330,
   b121c2f26e. THE LEG IS ALREADY OPEN. (c) IS ONE TOKEN JOINING A QUEUE, NOT A NEW LEG.
   I recommended (c) correctly and priced it wrong, having never asked what else was pending on the
   file I was pricing.

✅ AND THE FILE ALREADY ARGUES FOR (c) IN ITS OWN WORDS -- :354, verbatim:
   "carried on the 201 so the portal renders it from the response and never re-states a literal time."
   THAT IS WF-5's CRITERION, ALREADY RATIFIED AND ALREADY SHIPPED FOR THE PORTAL (@1fd9ef2750).
   The sweep is simply a SECOND CONSUMER with the identical need, so (c) EXTENDS AN ESTABLISHED
   PATTERN RATHER THAN MINTING ONE -- build-ladder rung 2, and the reason (c) is not merely the best
   of three but the only option consistent with the file's own stated intent.

(b) `get-function-configuration` per pass: RETAINED AS FALLBACK ONLY if the apply ever slips past the
   point where the sweep must run. Not wrong -- it reaches into the CONTROL plane for a BUSINESS
   value, ~168 calls/day on a live client-facing path, where (c) delivers the same value on the DATA
   plane, free, with a fetch the sweep already makes.
(a) config literal: EXCLUDED BY CRITERION -- it IS the second source WF-5 exists to prevent.

⛔ ZERO URGENCY, AND THAT IS RULED: DO NOT OPEN AN APPLY FOR THIS. (c) rides the W-A apply --
   WA-6's grant FIRST, the §6a discriminating print, the comp-blast read before the apply. The
   detection is inert, the cutoff is INJECTED, and the wiring waits on W-E's audience answer
   regardless. Nothing is blocked by leaving this queued.
-->

<!-- ==================== CROSS-TO GATE (RULED 23:33Z, 1.0.0_SA_CTO~Z @3854) ==================== -->
<!--
⛔ **W-F's DELIVERY LEG IS GATED ON W-E's AUDIENCE DECISION.** Named as a CROSS-TO GATE rather than
   a note, because neither TO carried it and a builder cannot see it from inside either lane.

⛔ CORRECTED 23:36Z — MY FIRST VERSION OF THIS BLOCK CONFLATED TWO ORTHOGONAL AXES AND WOULD HAVE
   DELETED AN OPTION FROM A SOVEREIGN FORK. It cited WE-4 as an AUDIENCE constraint. IT IS NOT.
   WE-4 VERBATIM: "POINTER-NOT-HOME: the body carries ticket id + deep link + minimal identifying
   context, and provably NOT the internal audit trail / routing / internal notes (the W-C
   projection discipline applied to the email surface)."
   >> THAT IS A RULE ABOUT WHAT GOES IN THE BODY — CONTENT-SCOPE. **CONTENT-SCOPE AND AUDIENCE ARE
      ORTHOGONAL:** an INTERNAL-audience DL carrying pointer-only content satisfies WE-4 completely,
      because "do not put the audit trail in an email" is good practice toward internal readers too.
   >> **NOTHING IN W-E CONSTRAINS THE DL'S AUDIENCE.** Audience appears EXACTLY ONCE in the whole TO
      (denominator 1, whole-file count) — as open question 2, resolved nowhere.
   ⛔ MY VERSION CONTRADICTED ITSELF IN TWO ADJACENT SENTENCES ("constrained to be provably not
      internal" beside "if it resolves internal-or-mixed the collision disappears") AND THE
      CONTRADICTION WAS THE TELL. Had it stood, a future reader would take it as foreclosing the
      INTERNAL-AUDIENCE BRANCH — the very branch that makes the collision vanish at zero cost.
      Caught by 0.5.0_AE_OpalETL~Z @3865, the criterion's author, reading their own TO at source.

THE COLLISION — ONE PREMISE, WHICH IS ALL IT EVER NEEDED:
  W-F  escalation is INTERNAL by ruling ("telling the CLIENT we were late is a product decision,
       carded to Andrew").
  W-E  :37  the DL's AUDIENCE IS UNDETERMINED — open question 2, carded to Andrew.
  >> THEREFORE **ONLY THE AUDIENCE-DEPENDENT PART** of W-F's delivery leg waits on the answer.

✅ NARROWED 23:42Z (1.0.0_SA_CTO~Z @3923, third narrowing of one ruling in ten minutes) — CUT ON
   THIS LINE, and the cut is 2.0.0_SA_COO~Z's per their instruction:
     BLOCKED on the audience answer, AND ONLY THESE:
         transport binding · recipient resolution · medium-specific formatting
     FREE, STARTS NOW:
         the escalation's TRIGGER CONDITION · its DETECTION · its PAYLOAD (see the caveat below)
   THE TEST, verbatim: "IF A TASK'S OUTPUT WOULD BE BYTE-IDENTICAL UNDER EITHER AUDIENCE ANSWER, IT
   IS NOT BLOCKED AND MUST NOT BE WRITTEN AS BLOCKED."
   TRIGGER and DETECTION pass that test cleanly: WHETHER a ticket is overdue (`status == open` at the
   wall-clock cadence) does not change when the reader changes.

⚠ PAYLOAD — I APPLIED THE TEST RATHER THAN INHERITING THE LIST, AND IT DOES NOT PASS CLEANLY.
   The FACT SET is audience-invariant: which tickets are overdue, since when, and by how long are the
   same facts either way. **But FACT SELECTION may not be.** An internal digest would carry routing
   state (e.g. `claimed_by: none`); a client-facing one plausibly would not — that is the WE-4
   content-projection concern one level down.
   >> SO THE CUT IS FINER STILL: **the payload's INVARIANT CORE is FREE and starts now.** If a
      SPECIFIC FIELD turns out to be audience-dependent, **THAT FIELD waits — not the payload, and
      certainly not the leg.** Raised rather than silently cut, because declaring free something that
      is not is the SAME wrong-grain error in the opposite direction.

⛔ THE ERROR SHAPE, and it is why this correction is worth more than the tasks it releases:
   **A DEPENDENCY STATED AT THE WRONG GRAIN DOES NOT LOOK LIKE AN ERROR — IT LOOKS LIKE CAUTION.**
   Gating the whole leg reads as prudent, produces no visible defect, and silently holds three tasks
   that could have run all night. **THE COST IS INVISIBLE AND IS PAID IN IDLE TIME, WHICH NO
   INSTRUMENT IN THIS FABRIC MEASURES.**
   And per the standing rule against manufactured gates: **A HOLD WIDER THAN ITS CAUSE IS A
   MANUFACTURED GATE ON THE EXCESS**, whatever the intent behind it. The wide version was mine in
   both TOs; the excess held detection and payload on a question that cannot touch them. **THE GATE DOES
     NOT REST ON WE-4 AND NEVER DID.** WE-4 is a CONTENT-projection criterion and is SILENT on
     audience; BOTH BRANCHES OF THE FORK REMAIN LIVE.

RESOLUTION IS ANDREW'S, NOT THE GATE'S:
  DL resolves INTERNAL-or-MIXED  -> the collision disappears; W-F may ride it.
  DL resolves CLIENT-FACING      -> W-F's escalation CANNOT ride it and needs a different surface.

⛔ THE DL IS **NOT** NAMED AS W-F's SURFACE. W-F's delivery surface is UNDETERMINED. The phrase in
   W-F's status -- "(the detect/deliver seam points at the email DL)" -- IS A HINT ABOUT THE SEAM AND
   WAS MEANT AS ONE. But it is the only surface named in that field and the channel is already
   excluded by ruling, so a builder reading "do not build until the surface is named" followed
   immediately by a named surface has been given a direction nobody intended.
   >> THE GENERAL FORM, from the gate's own author: **A HINT PLACED ADJACENT TO A PROHIBITION READS
      AS THE EXCEPTION TO IT.**

✅ AND THE GATE DECLINED THE MOVE THAT WOULD HAVE UNBLOCKED ITS OWN LANE, verbatim: "I AM NOT RULING
   THE AUDIENCE TO UNBLOCK MY OWN LANE. That is the move available to me right now and it is the
   wrong one -- the audience is carded to Andrew precisely because it decides what a client sees,
   and unblocking W-F is not a reason to take a decision back from him."
-->

## Objective
At **naive 2p ET**, any service request **issued before 2p ET** that is **still not addressed**
raises an escalation **to Opal**. ⛔ **THE DELIVERY SURFACE IS RE-OPENED — see the fence below.**
*(This line originally read "gets an agent message on the 'Opal Client Tickets' thread". That
surface may now be PROHIBITED by Andrew's ~21:35Z client-originated-only ruling, since this
escalation is Opal-originated by definition. The DETECTION half is unaffected and buildable; the
delivery leg waits on `1.0.0_SA_CTO~Z` re-stating which surface "internal" meant — the detect/deliver
seam already points at the email DL.)*

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

**(1) WHICH THREAD — ⛔ THE CHANNEL IS EXCLUDED. The POSITIVE surface is still to be named.**

✅ **HALF RESOLVED at 21:39Z (`1.0.0_SA_CTO~Z` @3149), and it follows from the gate's OWN axis rather
than from any inference of mine:** the interim is *"nothing AGENT-CAUSED goes in that channel"*, and
by the gate's own origin classification **this escalation is agent-caused** (it reports **Opal's
inaction**; no client act causes it). **So the "Opal Client Tickets" channel is OUT as this feature's
delivery surface** — that much is settled, and the fence on it is now a RULING rather than a caution.

⚠ **STILL OPEN — WHICH SURFACE IT *DOES* USE.** Excluding one surface does not name the next.
**`1.0.0_SA_CTO~Z` states the positive surface; the detect/deliver seam points at the EMAIL DL** (and
the DL's own transport criteria (2) audience and (3) DKIM remain at that gate). **DO NOT BUILD THE
DELIVERY LEG until the positive surface is named.** *The DETECTION half is unaffected and buildable
now.*

*Previously ruled:* INTERNAL by default — the escalation says *Opal has not answered*, so it is
**addressed to Opal**; telling the CLIENT we were late is a product decision, carded to Andrew.
*(That reading also dissolved the weekend/ack contradiction, since an internal audience never meets
the client's "next trading day" promise — and that part still holds.)*

⛔ **THE COLLISION (surfaced by `0.5.0_AE_OpalETL~Z` 3127, adjudicated by nobody):** Andrew's ~21:35Z
ruling makes the "Opal Client Tickets" channel **CLIENT-ORIGINATED ONLY**. **The 2p escalation is
OPAL-ORIGINATED BY DEFINITION** — its entire content is *"Opal has not accepted this ticket"*, caused
by **Opal's inaction**, not by any client act. **So IF "internal" meant that channel, this TO's ruled
delivery surface is now PROHIBITED** — under either available reading of his word. If "internal"
meant a **different** internal surface (the DL, a staff channel, his DM), nothing changes.
**A builder reading the pre-21:35Z text would implement the prohibited surface, which is why this is
fenced here rather than noted.**

>> **THE DISCRIMINATOR THAT MAKES BOTH READINGS COHERENT IS *ORIGIN*, NOT *AUTHORSHIP*.** Every post
in that channel is authored by an agent — no client has Teams access — so a literal
"no-agent-posts" reading would take **the new-ticket buzz itself** with it, and the channel was
created for exactly those buzzes. Under the origin reading, the buzz is not merely permitted, **it is
the channel's purpose**, because a *client's form submission caused it*.

✅ **AND THE SEAM ALREADY POINTS AT THE ANSWER — the surface Andrew just closed is not the one the
design wanted.** The gate's own detect/deliver split puts **DELIVERY on the email DL**: the
escalation **DETECTS on the runner and DELIVERS on the DL**, which satisfies the new ruling **for
free**. W-E and W-F being one mechanism is what makes this cost nothing.

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
