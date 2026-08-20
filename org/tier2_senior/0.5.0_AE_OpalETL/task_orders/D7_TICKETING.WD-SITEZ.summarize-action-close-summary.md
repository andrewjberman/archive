# TO D7_TICKETING.WD-SITEZ — Ticket Lifecycle v2 W-D: the SUMMARIZE action + BG's close-summary duty

<task_order id="D7_TICKETING.WD-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build: matrix row + API + serve-duty config; laptop apply leg via 0.0.0_AB_MSTR~Z ferry). BG (0.0.3_BG_BBGTerminal) = the serve-duty half at the close nudge — BG's G1 fence cannot write the repo; its duty lands as serve-loop behavior, config authored at this seat.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>staged — activates after W-A (shared Lambda file) and once a nudge path exists (the scheduled backstop suffices; W-B stream not required). 1.0.0_SA_CTO~Z sequencing: fourth of four.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ @942d4d885c — his C4 (AI Summary on Completed) + O8; 1.0.0_SA_CTO~Z ruling 4 (THE AI SUMMARY): a new scoped action SUMMARIZE granted ONLY to svc-analyst-intake — its first write beyond CREATE — one field, own matrix row, deny-by-default everywhere else; BG authors the summary at the close nudge: ONE nudge, TWO acts (thread confirmation per approved (b) + the SUMMARIZE write the client reads).</authority>
</task_order>

## ⛔ NOT BUILDABLE AS SPECIFIED — 21:39Z, `1.0.0_SA_CTO~Z` @3149. STOP BEFORE THE OBJECTIVE.

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

**W-D's specified behaviour IS exactly the behaviour whose legality is uncertain**, which is why the
TO cannot proceed as written. ⚠ **AND THE COLLISION IS BETWEEN TWO OF HIS OWN RULINGS** — *"Rec
approved on closing tickets"* predates the client-originated ruling — **so the gate explicitly
declines to adjudicate between a sovereign's rulings in either direction.** Carded to him.

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
