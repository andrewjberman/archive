# TO D7_TICKETING.WE-SITEZ — the EMAIL DL as the FIRST INSTANTANEOUS LINE (agent demoted to convenience layer)

<task_order id="D7_TICKETING.WE-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build). Laptop apply leg (ticket-api Lambda + any SES resource) = EXECUTION PLACEMENT via 0.0.0_AB_MSTR~Z ferry. **DL CREATION IS A TENANT-ADMIN ACT — actor named below, NOT assumed.**</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:4xZ</issued>
<status>BUILT, NOT APPLIED — updated 2026-08-21 ~0630Z by 2.0.0_SA_COO~Z; the prior "staged — DESIGN GATE FIRST" line was stale by FOUR movements, not three. **(1) DESIGN GATE HALF-DISCHARGED 0212Z @c3e7fc73ac** — transport (SES from the CREATE Lambda write path) + sender (opalinvest.dev) RULED; the "DL address exists and its creating actor is named" limb is **NOT** discharged and remains a tenant-admin act. **(2) SES SANDBOX BLOCKER CLEARED ~0305Z @9c73a31b8d** — production access GRANTED, case 178727932800843, 200 -> 50,000/day; a DL on @opalinvest.com needs no per-address verification. **(3) AUDIENCE RULED INTERNAL ONLY ~0450Z** (Andrew-direct, plan @c1cb35d3aa sec. 0) — this releases the AUDIENCE-DEFERRED set (title, requester.{email,name,firm}) and does NOT touch the WE-4-PROHIBITED set. ⚠ "body text" is a **NEW** field, neither prohibited nor deferred, and needs its own gate ruling rather than a silent release under cover of the audience answer. **(4) BUILD LANDED 0515Z @4d5a92f4d7** — 4 PASS / 3 UNCOMPUTABLE-BY-CONSTRUCTION, VALID rc=0, independently re-derived by 2.0.0_SA_COO~Z (checker discrimination confirmed on THIS instance, not a sibling). **REMAINING:** DL creation (tenant-admin, not the build seat) · TICKET_DL + TICKET_DEEP_LINK_BASE set · laptop apply. ⛔ **THE APPLY CARRIES W-A's QUEUE** — the module-level region is diverged, so it is NOT a clean single-change apply (81c502cff2 + 9121a55330 + b121c2f26e ride with it); it must be REQUESTED as such, not corrected afterwards. **WE-2/WE-3 remain the exercised proof and nothing built substitutes for them.**</status>
<priority>P2 — his stated ordering makes this the FIRST LINE for humans; it is not on the dep-2/dep-3 critical path.</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~20:45Z at the 0.0.0_AB_MSTR~Z console, record @11d274f8c2. VERBATIM: *"That is why the email needs to be the first instantaneous line of attack, the agent is just making it more convenient and teams-friendly."*
⛔ **MORATORIUM SATISFIED BY EXPLICIT ASK.** The 2026-07-28 standing moratorium bans BUILDING notification machinery unless Andrew explicitly asks. He asked. **His verbatim above IS the `# andrew-asked` marker text** — carry it inline on any commit that a notification lint would otherwise deny.</authority>
</task_order>

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
An **email distribution group** receives a notification the instant a client service request is
created. The agent's Teams buzz is **convenience + Teams-friendliness on top**, not the critical
path.

**THE ORDERING FALLS OUT OF THE ARCHITECTURE — name it, do not assert it.** "First INSTANTANEOUS
line" and "the agent is just making it more convenient" map exactly onto what already exists:
the CREATE Lambda write is the instantaneous moment; the agent buzz rides the 5-minute scheduled
runner (≤5 min, measured 99.6s in the water test). So an email sent from the **Lambda write path**
is instantaneous by construction, and the agent stays the convenience layer by construction.
⚠ **This is the decomposition's READ, not a ruling — 1.0.0_SA_CTO~Z owns the design word.**

**THE EMAIL IS A POINTER + LINK, NEVER A SECOND HOME for ticket state** (the tickets-class
discipline already in the memory contract). Ticket state has one home; the email points at it.

## ⛔ TWO DECISIONS THAT MUST PRECEDE THE BUILD (named here so neither is a build-time discovery)

**(1) TRANSPORT — CRITERIA RE-ORDERED BY THE GATE @21bd23d943→ (1.0.0_SA_CTO~Z 2980, on the measured
credential finding). The gate's own sender ruling was settled on AUTH POSTURE and it says that was
INCOMPLETE. THE ORDER IS NOW:**
1. ⛔ **DOES THE SEND PATH DEPEND ON AN AGENT-SESSION-REFRESHED CREDENTIAL? If YES → DISQUALIFIED
   for the DL, regardless of auth posture.** The DL exists precisely to work **when no agent is
   awake**; a path carrying the ~1h dependency would reproduce the exact failure it is meant to
   backstop, **at the exact moment it is meant to work**.
2. The DL's **audience**.
3. **DKIM state** — meaningful only after 1 and 2.
✅ **CRITERION (1) IS NOW SETTLED AT SOURCE — and the answer is STRUCTURAL, not probabilistic**
(`0.5.0_AE_OpalETL~Z` 2988, gateway app read at HEAD). *The conditional above resolved to YES, and
it resolved without needing a `sendMail` test at all:*

**THE DEPENDENCY LIVES AT THE TRANSPORT LAYER, NOT AT THE TOOL LAYER.** `server.py:15` — the gateway
Bearer is **fully validated before any tool name is dispatched** (`:92-98`). So **a call that cannot
present a live bearer never reaches a tool.** Therefore **EVERY gateway-mediated send —
`send_channel_message`, `send_email`, Graph `sendMail`, anything added later — inherits the ~1h
agent-session dependency BY CONSTRUCTION, and NO PER-TOOL EXCEPTION IS POSSIBLE.** *(A `sendMail`
probe would only have sampled one tool of a class that shares one gate — the structural read is the
stronger result.)*

⛔ **RETRACTED BY ITS AUTHOR (3021), AND THE REPLACEMENT IS THE HONEST ARGUMENT — DO NOT CARRY THE
OLD ONE.** This clause previously read that the refresh *"is an INTERACTIVE OAuth challenge"* and
that a Scheduled Task *"structurally cannot self-heal."* **TOO STRONG.** Measured (field-name census
over the credential store, 4 of 4 records, no values printed): **every record carries `refreshToken`
+ `clientId` + `redirectUri` + `scope`** — the complete material for a standard **`refresh_token`
grant, which is a server-to-server POST needing no human and no browser.** The 401 +
`WWW-Authenticate` path grounded at `server.py:81-87` is **the INTERACTIVE path — correct for a
FIRST authorization or an already-failed refresh. It is ONE path, not THE only one.**

>> **WHY THE RUNNER STILL DOES NOT REFRESH IS A DESIGN CHOICE, stated in the engine's own docstring:
*"Claude Code owns the refresh (rotating tokens), so this never refreshes itself → no refresh-token
fight."* THE TOKENS ROTATE — two independent refreshers would invalidate each other.**

✅ **THE DISQUALIFICATION SURVIVES, ON A BETTER ARGUMENT: ENTANGLEMENT, NOT IMPOSSIBILITY.** Making a
gateway-mediated DL work unattended would require **a SECOND REFRESHER RACING CLAUDE CODE ON ROTATING
TOKENS** — trading a *predictable hourly gap* for **unpredictable mutual invalidation that would take
down the agent's own connectivity.** That is **the backstop damaging the thing it backstops.**
>> **THE PRINCIPLE, and it is the durable half: A BACKSTOP MUST NOT BE ENTANGLED WITH THE CREDENTIAL
OF THE SYSTEM IT COVERS.** Criterion (1) still disqualifies the gateway; SES still survives.

⚠ **AND A DELIBERATE NON-MEASUREMENT, recorded with its reason rather than left as a gap:** the
refresh grant was **NOT attempted**. A successful refresh **ROTATES** the token, and the artefacts
live on that exact credential right now are **the production intake's send leg and another seat's
armed monitor** — so the experiment's failure mode is invalidating a client-facing path and a peer's
reachability to confirm a claim already corrected on stronger evidence. If the DL design ever needs
it measured, it wants **a scratch OAuth client or Andrew's word, never a live-credential probe.**

>> **RULING INPUT: the gateway is DISQUALIFIED for the DL on criterion (1), definitively rather than
probably** — a gateway-mediated DL would reproduce the exact failure it exists to backstop, at the
exact hour it is meant to cover, and **SILENTLY from the DL's own point of view** (a 401 is a clean,
well-formed refusal). **SES survives (1):** AWS-native, authenticates with the box's own credentials,
no interactive-client dependency — with **NEVER#23 then binding its sender to `opalinvest.dev` at
criterion (3)**, exactly where the gate placed it.

⚠ **TWO HONEST BOUNDS, carried from the author:** the gateway's **server-side** Graph token
(`_user_token()`, its own MSAL lifecycle) was **NOT measured** — irrelevant here because the client
never gets that far, but silence is not converted into a finding. And **SES has NOT been exercised
from this box**; its suitability rests on **architecture, not an exercised send**. WE-2/WE-3 remain
the exercised proof.

>> **AND THE "DETECTION IS AGENT-INDEPENDENT; DELIVERY KEEPS TURNING OUT NOT TO BE" PATTERN NOW HAS
ITS MECHANISM RATHER THAN ITS THIRD COINCIDENCE: every delivery surface reached for routes through
an interactive-OAuth gateway, and detection does not. ONE ROOT, not three findings.**
>> **THE PATTERN THE GATE NAMES, worth carrying beyond this TO: this is the THIRD independent
discovery in one evening that something called "independent of the agent" is not. DETECTION IS
AGENT-INDEPENDENT; DELIVERY KEEPS TURNING OUT NOT TO BE.**

**(1a) THE UNDERLYING AUTH FACTS — AND IT CARRIES A STANDING LAW, so it is not a detail.**
The two candidates **send as DIFFERENT DOMAINS**:
- **SES** → NEVER#23 binds it absolutely: `Source`/`EMAIL_FROM` on **`opalinvest.dev`** (DKIM-signed,
  DMARC-aligned). `opalinvest.com` is address-verified only and gets **nondeterministically**
  quarantined — a silent coin-flip, not a clean fail.
- **Graph `sendMail` as the gateway identity** → sends as **`opalbloomberg@opalinvest.com`** — a
  different domain with a different authentication posture.
**Pick the transport WITH its sender identity, at 1.0.0_SA_CTO~Z's design gate.** A "first
instantaneous line" that lands in quarantine is worse than no first line, because it reads as sent.

⛔ **A MEASURED FINDING NOW BEARS ON THIS FORK, AND IT MAY DECIDE IT (`0.5.0_AE_OpalETL~Z` 2955,
measured end-to-end 21:04–21:06Z).** The `opal-gateway-bbg` OAuth credential carries a **~1 HOUR
TTL and is refreshed ONLY as a side effect of an agent MCP call to that server.** Measured live: the
21:04:46Z scheduled fire **exited 2** ("pinned gateway token expired"); one legitimate agent read at
~21:06 moved expiry to 22:06:05Z and the runner immediately returned `INTAKE PASS OK`. **So the
production buzz leg stops within the hour whenever no session touches the gateway** — behaviour is
correct (it refuses before fetching, the cursor never advances, tickets are **DELAYED, NEVER
DROPPED**), but **a ticket filed overnight sits unbuzzed until a seat wakes.**

**THE CONSEQUENCE FOR THIS FORK:** the whole point of W-E is a **first INSTANTANEOUS line** that
does not depend on the agent. **SES from the Lambda write path uses the Lambda's own IAM role and
has NO agent-session dependency at all.** ⚠ **INFERENCE, NOT MEASURED BY ME — verify at the gate:**
a Graph `sendMail` **as the gateway identity** would plausibly draw on that same gateway credential
and therefore **inherit the identical ~1h session dependency** — which would make the "first
instantaneous line" fail in exactly the same window as the agent path it exists to backstop,
**defeating its purpose**. If that inference holds, the fork is close to decided; if it does not
(a distinct app-only credential, say), it does not bind. **Read the credential path before ruling.**

**(2) THE DL ITSELF IS A TENANT-ADMIN ACT — NAME THE ACTOR EARLY.**
Creating an Exchange distribution group is the same shape as the "Opal Client Tickets" channel
Andrew created by hand at ~19:22Z: **no tool in the gateway creates it.** The chain must name who
creates it (Andrew, or a tenant admin) and who reports the resulting address, exactly as the
channel's ids were reported. **Do not let the build discover this.** The DL address is CONFIG,
refuse-if-unset, never a baked default — the channel-ids precedent.

## Acceptance criteria (D7F pattern)
- **WE-1** DESIGN GATE DISCHARGED: transport + sender identity ruled by 1.0.0_SA_CTO~Z, recorded
  before any build act; the DL address exists and its creating actor is named in the record.
- **WE-2** INSTANTANEOUS, EXERCISED: one real ticket creation produces the email, with the
  **latency measured** from the row's `created_at` to the send — and stated beside the agent buzz's
  own latency on the same ticket, so "first line" is a **measured ordering**, not a claim.
- **WE-3** SENDER VERIFIED ON THE WIRE (not from config): the delivered message's From/authentication
  headers read the ruled domain. A config value proving itself is not evidence.
- **WE-4** POINTER-NOT-HOME: the body carries ticket id + deep link + minimal identifying context,
  and **provably NOT** the internal audit trail / routing / internal notes (the W-C projection
  discipline applied to the email surface — asserted on a row where those fields are populated).
- **WE-5** REFUSE-IF-UNSET: with the DL address absent, the path refuses **loudly** (distinct exit /
  named error) and **does not** fall back to a baked address; exercised.
- **WE-6** NO-REGRESSION on the live path: the CREATE write, the 201 contract, the client ack frame
  and the 5-min runner's buzz all behave unchanged; the existing batteries re-run green. ⚠ **The
  runner and the CREATE Lambda are LIVE PRODUCTION INFRASTRUCTURE now** — a failure in the email leg
  must not fail the ticket creation. Exercised: the email leg erroring still yields a 201 and a
  buzz.
- **WE-7** Proof instance VALID rc=0 POSITIONAL, ids WE-1..WE-7 (rc unpiped; the flagged form exits
  2 and the 2-arg fallback prints VALID while checking coverage nothing).

<proof_of_spec>
  <expected_criteria>WE-1,WE-2,WE-3,WE-4,WE-5,WE-6,WE-7</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WE_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<compiler_tools_mandate>
Before write: `comp-estate --layers` for an existing notification/SES pattern (Build Ladder rung 2 —
the estate may already carry one); `comp-iam service` (floor) on the sending principal.
Before commit: commit-gate. After apply: the live IAM primitive per Rule 22a for any new SES/Graph
grant (ONE `--resource-arns`, separate positive control).
</compiler_tools_mandate>

<cross_domain_coordination>
`infra/aws/lambda/ticket_center/lambda_function.py` is SHARED with W-A (lands first), W-C(b) and
W-D — rebase and MCP the concurrent lane before commit. Any SES identity/resource is
NEVER#23-governed and laptop-applied. The DL is a tenant surface, not a repo surface.
</cross_domain_coordination>

## Do not
No second home for ticket state in the email. No fallback sender, ever. No monitoring/alarm
machinery — he authorized a NOTIFICATION FEATURE, and the moratorium is untouched for everything
else. Do not build across the transport fork before 1.0.0_SA_CTO~Z rules it.

## Reporting
Completion → 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance) + 0.0.0_AB_MSTR~Z (ferry).
Surprise channel: one line to 2.0.0_SA_COO~Z. Session log = deliverable.
