# TO D7_TICKETING.WE-SITEZ — the EMAIL DL as the FIRST INSTANTANEOUS LINE (agent demoted to convenience layer)

<task_order id="D7_TICKETING.WE-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build). Laptop apply leg (ticket-api Lambda + any SES resource) = EXECUTION PLACEMENT via 0.0.0_AB_MSTR~Z ferry. **DL CREATION IS A TENANT-ADMIN ACT — actor named below, NOT assumed.**</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:4xZ</issued>
<status>staged — DESIGN GATE FIRST at 1.0.0_SA_CTO~Z (the transport fork below carries a standing law; do not build across it). Sequenced beside W-A..W-D, not ahead of the queue at the build seat.</status>
<priority>P2 — his stated ordering makes this the FIRST LINE for humans; it is not on the dep-2/dep-3 critical path.</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~20:45Z at the 0.0.0_AB_MSTR~Z console, record @11d274f8c2. VERBATIM: *"That is why the email needs to be the first instantaneous line of attack, the agent is just making it more convenient and teams-friendly."*
⛔ **MORATORIUM SATISFIED BY EXPLICIT ASK.** The 2026-07-28 standing moratorium bans BUILDING notification machinery unless Andrew explicitly asks. He asked. **His verbatim above IS the `# andrew-asked` marker text** — carry it inline on any commit that a notification lint would otherwise deny.</authority>
</task_order>

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

**(1) TRANSPORT — AND IT CARRIES A STANDING LAW, so it is not a detail.**
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
