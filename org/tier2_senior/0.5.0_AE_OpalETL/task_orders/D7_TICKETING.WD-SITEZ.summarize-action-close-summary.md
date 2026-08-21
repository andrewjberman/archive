# TO D7_TICKETING.WD-SITEZ — Ticket Lifecycle v2 W-D: the SUMMARIZE action + BG's close-summary duty

<task_order id="D7_TICKETING.WD-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build: matrix row + API + serve-duty config; laptop apply leg via 0.0.0_AB_MSTR~Z ferry). BG (0.0.3_BG_BBGTerminal) = the serve-duty half at the close nudge — BG's G1 fence cannot write the repo; its duty lands as serve-loop behavior, config authored at this seat.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>**BOTH ACTIVATION CONDITIONS ARE NOW MET-OR-NEARLY. THE BINDING CONSTRAINTS ARE THE TWO HOLDS, NOT THE SEQUENCING.** (Corrected 23:31Z by 2.0.0_SA_COO~Z; superseded text preserved below.)
 ✅ CONDITION 2 — "once a nudge path exists" — **MET.** The scheduled backstop is LIVE and exercised: `OPAL_D7_ticket_intake`, `<Interval>PT5M</Interval>`, `State=Ready`, `exit 0` every pass through the 23:15:55Z credential boundary. **And this TO called it correctly in advance — "W-B stream not required" — which is why W-B's transport being DROPPED costs this lane NOTHING.**
 ◑ CONDITION 1 — "after W-A (shared Lambda file)" — **BUILD SIDE MET, APPLY SIDE PENDING.** W-A's build is complete and proof-validated (@81c502cff2, @9121a55330, @7e98926a41 `VALID rc=0`, @133b0f24b0). The shared-file collision risk this clause guards is a BUILD-TIME concern and is past; the laptop APPLY remains outstanding. **Name which one you mean before treating this as clear.**
 ⛔ WHAT ACTUALLY BINDS, and it is neither of the above: **limb (1)** thread-confirmation is HELD (it posts to Teams, and the prohibition reaches it); **limb (2)** SUMMARIZE is carded to Andrew. A hold inherits the scope of its reason — limb (2) writes a DDB field rendered in the client portal and never touches Teams.
 ⚠ SUPERSEDED TEXT: ~~staged — activates after W-A (shared Lambda file) and once a nudge path exists (the scheduled backstop suffices; W-B stream not required). 1.0.0_SA_CTO~Z sequencing: fourth of four.~~ — the sequencing remains TRUE and was satisfied.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ @942d4d885c — his C4 (AI Summary on Completed) + O8; 1.0.0_SA_CTO~Z ruling 4 (THE AI SUMMARY): a new scoped action SUMMARIZE granted ONLY to svc-analyst-intake — its first write beyond CREATE — one field, own matrix row, deny-by-default everywhere else; BG authors the summary at the close nudge: ONE nudge, TWO acts (thread confirmation per approved (b) + the SUMMARIZE write the client reads).</authority>
</task_order>

## ⛔ PARTIALLY HELD — LIMB (1) NOT BUILDABLE; LIMB (2) SCOPE-QUESTIONED. STOP BEFORE THE OBJECTIVE.
*(Gate spec-fact 21:39Z `1.0.0_SA_CTO~Z` @3149, NARROWED 21:4xZ on `3.0.0_SA_CVO~Z` @3153 — see the scope correction below. My first fold held this TO wholesale; that was over-broad.)*

**This is a SPEC FACT stated at the gate, not a gate and not a hold — nobody signs anything.**
Andrew's ~21:35Z ruling makes the "Opal Client Tickets" channel **CLIENT-ORIGINATED ONLY**, and on
the only coherent axis (**ORIGIN, NOT AUTHORSHIP** — no client has Teams access, so *every* post
there is agent-authored; if "client-originated" meant authorship the channel could never contain
anything, which is a contradiction rather than a reading):

| post | origin | status |
|---|---|---|
| runner's NEW-TICKET buzz | **client-caused** (a dashboard submission) | **SANCTIONED** — it is the channel's purpose |
| header / "now watching" | agent-caused | **PROHIBITED** |
| **closing-or-claim buzz + THIS TO's AI summary** | an **INTERNAL action on a CLIENT's ticket** | ⛔ **GENUINELY OPEN — ANDREW'S CALL** |

⚠ **AND THE COLLISION IS BETWEEN TWO OF HIS OWN RULINGS** — *"Rec approved on closing tickets"*
predates the client-originated ruling — **so the gate explicitly declines to adjudicate between a
sovereign's rulings in either direction.** Carded to him.

## ⛔ SCOPE CORRECTION 21:4xZ — **THIS TO IS TWO ACTS ON TWO SURFACES, AND THE PROHIBITION REACHES ONLY ONE**

*(`3.0.0_SA_CVO~Z` @3153, grounded at the v2 record's own O8 row — verbatim: **"one nudge, TWO ACTS
(the thread confirmation + the SUMMARIZE write)"**. My first fold above held the TO **wholesale**,
and that was my error.)*

| limb | surface | reached by the channel prohibition? |
|---|---|---|
| **(1)** thread confirmation at close | a **Teams post** in the client-tickets channel — **agent-caused** | ✅ **YES — HELD.** The interim covers it exactly |
| **(2)** the `SUMMARIZE` write | a `resolution_summary` **field on the DDB row**, rendered in the **CLIENT'S PORTAL** "Completed" view — **NEVER TOUCHES TEAMS** | ⛔ **NO — the prohibition does not reach this surface at all** |

⛔ **WHY HOLDING LIMB (2) WOULD BE ACTIVELY HARMFUL, not merely over-broad:** limb (2) is **Andrew's
own C4 requirement** (*"When ticket is closed, client sees ticket moved to 'Completed' with AI
Summary of its resolution"*) — **AND it is the mechanism behind the `superseded` exception** in the
adopted `closure_reason` record (a `closed` ticket must not carry an AI summary, **sole exception
`superseded`**, restored into W-C at 21:2xZ after a mis-ack nearly cost that clause). **Hold limb (2)
wholesale and that exception has no mechanism behind it — so the one ticket class whose client
legitimately GOT an answer is precisely the class that silently loses its answer.**

>> **THE GENERAL FORM, and it is this evening's own class again: A HOLD INHERITS THE SCOPE OF ITS
REASON.** W-D was decomposed as one workstream because the two acts fire on **one nudge** — a
**SEQUENCING** fact, not a **SURFACE** fact — and a prohibition scoped to one surface then reads as
scoped to the whole workstream. *Same shape as "row-scoped is not field-scoped": the bundling was
correct for the purpose it was made for, and wrong for the purpose it was then used for.*

⚠ **WHAT IS NOT CLAIMED, and either could overturn the split:** (a) **SEPARABILITY IS AN ENGINE
FACT I DO NOT HOLD** — if the `SUMMARIZE` write is inseparable from the nudge in the serve loop's
implementation, the wholesale hold is right; `0.5.0_AE_OpalETL~Z` confirms or refutes. (b) **Limb (2)
is NOT thereby cleared to build** — its Rule-24 matrix row, the deny-by-default scoping of
`SUMMARIZE` to `svc-analyst-intake`, and the client projection all still gate it, and W-C's tab
mapping is where the rendering lands. **The claim is only that the CHANNEL prohibition is not what
gates it, and a hold citing that prohibition must say WHICH LIMB it holds.**
**Scope confirmation requested from `1.0.0_SA_CTO~Z`: was the spec-fact wholesale, or limb-(1)-scoped?**

**W-A / W-B / W-C are UNTOUCHED and proceeding.** The `SUMMARIZE` action's *matrix/API* half is not
what is in question — **the CHANNEL POST at close is.** If he rules the closing buzz in, this TO
resumes unchanged; if out, the summary still lands on the row for the client's own view (W-C) and
only the thread post drops.

## Objective
- **API/matrix:** new action `SUMMARIZE` writing exactly one field, `resolution_summary`, on a
  COMPLETED row; granted ONLY to `svc-analyst-intake`; deny-by-default everywhere else. The
  Rule-24 matrix filing RIDES the change (the action set is a schema enumeration — four-postulate
  record with the declared layer, per the 08-20 widening).
- **BG duty:** at the close nudge, BG (a) confirms the close in the "Opal Client Tickets" thread
  (the approved (b)) and (b) composes a clean, client-readable resolution summary and lands it via
  SUMMARIZE under the svc-analyst-intake token. Serve rules bind (concise, id, deep link,
  identifier-beside-value; a permanent post promises only what is already true). Every gateway
  send handles confirm_on_irreversible.

## Acceptance criteria
- **WD-1** SUMMARIZE positive: under the svc-analyst-intake token, a completed row gains
  `resolution_summary`; exercised on a real row.
- **WD-2** DENY pairs (matrix mutants, both directions): svc-ticket-form → SUMMARIZE refused;
  svc-analyst-intake → claim/complete/other writes still refused; SUMMARIZE on a NON-completed
  row refused (state guard). Each mutant discriminates.
- **WD-3** One-nudge-two-acts exercised end-to-end: close → nudge → BG thread confirmation posted
  (before-read/after-read evidence, the dep-1 standard) + summary written; the client Completed
  view (W-C) and the internal board both render it.
- **WD-4** Rule-24 filing committed WITH the matrix change (action enum + outcome array re-tested
  against the declared layer).
- **WD-5** IAM/authz per 22a where any new resource appears; laptop apply ledger + tag; existing
  authz battery re-runs green.
- **WD-6** Proof instance VALID rc=0 positional, ids WD-1..WD-6.

<proof_of_spec>
  <expected_criteria>WD-1,WD-2,WD-3,WD-4,WD-5,WD-6</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WD_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<compiler_tools_mandate>
comp-blast on ticket_center lambda before write; comp-iam floor + live simulate for new grants;
commit-gate before commit.
</compiler_tools_mandate>

<cross_domain_coordination>
`infra/aws/lambda/ticket_center/lambda_function.py` SHARED with W-A (lands first) and W-C(b) —
rebase; MCP the other lane before commit if concurrent. BG serve-duty config: coordinate with the
BG relaunch/RELAUNCH.md state via 0.0.0_AB_MSTR~Z (identity pin + resident-schema rows). No portal files
(the render is W-C's).

⛔ **INHERITED OBLIGATION — THE UNMEASURED BLAST RADIUS ON THIS SHARED FILE**
(`1.0.0_SA_CTO~Z` amended ruling 21:59Z, on a residual I named at the W-A validation): W-A's
`comp-blast` on `lambda_function.py` **did not run before write** (timed out, backgrounded), and
**this file is shared across THREE W-lanes** — so it is not a late check on one lane's change,
it is an **unmeasured blast radius on a file three lanes touch.** **THE OBLIGATION TRANSFERS TO
WHICHEVER LANE TOUCHES THIS FILE NEXT.** Run it here if it has not run by the time this lane
starts, and say so either way.
⚠ **And do not discharge it with "risk is low because W-A lands first and we rebase"** — that is
**sequencing**, which this same evening demoted from load-bearing to convenience. Sequencing is
not a measurement.
</cross_domain_coordination>

## 3.0.0_SA_CVO~Z PRE-CUT NOTE FOLDED (2817 @3c29c35122) — two similar names, two audiences

The row already carries a deployed internal **`resolution`** close note (2000 chars). This TO adds
the client-facing **`resolution_summary`**. **One row, two similar names, two audiences** — and the
only thing standing between them is W-C's client projection allowlist. Therefore: name the
distinction explicitly in the Rule-24 filing (which field is internal, which is client-visible,
which principal writes each), and **WD-2's deny pairs must include a client-projection assertion
that `resolution` never reaches a client response** even once `resolution_summary` exists. If the
naming is judged too collision-prone at 1.0.0_SA_CTO~Z's gate, renaming is cheaper here than after either
field has consumers.

## Do not
SUMMARIZE never widens beyond the one field + one subject (deny-by-default is the design). BG's
summary is client-readable prose — no internal serials/jargon in the client-visible field. No
alert machinery.

## Reporting
Completion → 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance) + 0.0.0_AB_MSTR~Z (ferry + BG coordination). Surprise
channel: one line to 2.0.0_SA_COO~Z. Session log = deliverable.
