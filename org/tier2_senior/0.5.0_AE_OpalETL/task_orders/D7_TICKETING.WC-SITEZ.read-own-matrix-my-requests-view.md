# TO D7_TICKETING.WC-SITEZ — Ticket Lifecycle v2 W-C: client READ-OWN matrix + the portal "My Requests" view (JOINT, TO-F precedent)

<task_order id="D7_TICKETING.WC-SITEZ" project="OPAL_TICKET">
<issued_to>JOINT (the TO-F-SITEZ two-half pattern): half (b) MATRIX = 0.5.0_AE_OpalETL~Z (build; laptop apply leg via 0.0.0_AB_MSTR~Z ferry). Half (a) PORTAL VIEW = **0.4.0_DE_ClientPlatform~Z** at the next seat window (0.0.0_AB_MSTR~Z spawn call — that serial was not live at issuance); ship via the 0.4.0_DT_ClientPlatform~Z promote pattern (portal-v2.1.164 precedent).
⚠ **ADDRESSING NOTE (Andrew-direct 2026-08-20 ~2036Z, record @9e1e94c4f4 — agents refer to other agents by FULL SERIAL):** this line previously read "DE-class hands", which is not an address at all. **And the hazard is sharper here than the general rule:** `0.4.0_DE_ClientPlatform~Z` and `0.4.0_DT_ClientPlatform~Z` differ by ONE LETTER and BOTH are real registered seats — so a one-character slip delivers to a live wrong seat and `send_message` returns DELIVERED. Half (a) is the DE seat (portal build); the promote is the DT seat.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>staged — half (b) activates after W-A lands (shared Lambda file, sequenced); half (a) activates at the 0.4.0_DE_ClientPlatform~Z seat window. 1.0.0_SA_CTO~Z sequencing: third of four.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ @942d4d885c — his C2/C3/C4 client experience verbatim; 1.0.0_SA_CTO~Z ruling 2 (CLIENT VISIBILITY): client-human gains READ-OWN — list/get filtered SERVER-SIDE to the session identity's own rows (never a client parameter); the matrix widening is authorized by his word, scoped to this step. Tenant axis stays absolute.</authority>
</task_order>

## ⛔ P0 AMENDMENT — ROW-SCOPED IS NOT FIELD-SCOPED (3.0.0_SA_CVO~Z pre-cut read 2817 @3c29c35122, folded ~20:33Z)

**The cut below originally specified only the ROW filter. That is one control where TWO are needed,
and the missing one leaks internal data to clients.** `get_ticket`/`list_tickets` return
**UNPROJECTED WHOLE ROWS** — so the day `client-human` joins LIST/GET, a client fetching *their own*
ticket also receives `events[]` (the full internal audit trail: every internal actor's email,
action, from/to, free-text notes), `routing{primary,secondary,visibility}`, and the internal
`resolution` close note.

**REQUIRED, and it is a build-blocking part of this TO:** an explicit **client PROJECTION ALLOWLIST
at the RESPONSE BOUNDARY** — server-side, never left to the frontend. *A UI that does not render a
field still shipped it over the wire.* The allowlist is derived from **Andrew's own C2/C3/C4
enumeration** (their ticket in Open/In Progress/Completed, the claimer's name+email, the AI summary,
plus the ticket's own identity/title/description/timestamps) — **everything not enumerated is
internal by his framing**, so this is faithful implementation, not a narrowing.

**AND the mutants must be symmetric:** the D7F-4 class asserts a client response **LACKS**
`events[]` / `routing` / `resolution` **as positively as** it asserts it HAS the claimer identity.
An absence that is never asserted is not tested.

## Objective
- **Half (b) — matrix + projection:** `client-human` gains **READ-OWN**: list/get scoped server-side
  to rows where the requester matches the SESSION identity (filter derives from the token — never a
  client parameter), **AND every client-bound response passes the projection allowlist above.**
  Tenant axis absolute: a client sees ONLY their own firm's own rows. Deny-by-default preserved
  everywhere else (svc subjects untouched; internal READ unchanged). PRD §7.3 matrix amendment rides
  1.0.0_SA_CTO~Z's gate.
  ⚠ **ARCHITECTURAL FINDING TO RESOLVE AT DESIGN, NOT DISCOVER AT BUILD (3.0.0_SA_CVO~Z P1-3):** `MATRIX` is
  `action -> {principal_class}` with **no scope channel**, and `authorize()` returns `(allowed, pc)`.
  Every grant today is unscoped, so action-only modeling has been faithful — **CLIENT READ-OWN is
  the estate's FIRST SCOPED GRANT and the matrix cannot express it**, which would strand "own only"
  in handler code *beside* the authorization surface instead of *in* it. That is Rule 22a's
  `(action)` vs `(action, resource)` defect one layer up. **The return-contract change is far
  cheaper here than after.** Decide it with 1.0.0_SA_CTO~Z before writing the handler.
- **Half (a) — portal:** client "My Requests" view: Open / In Progress / Completed tabs; renders
  `claimed_by` name+email (W-A enrichment) on claimed rows and `resolution_summary` (W-D) on
  Completed. Client-facing surface: color law + /frontend-dev render-check BINDING. Route stays
  client-legal (`/ticket-center` remains internal — the redirect discriminates identity, the
  TO-F B2/B3 pattern).

## Acceptance criteria (D7F pattern; the D7F-4 mutant class EXTENDS to READ-OWN)
- **WC-1** READ-OWN positive: a client token lists/gets ITS OWN rows (all three states), exercised
  on real rows.
- **WC-2** MUTANT (forged filter): a client request carrying another requester's
  id/email/firm as a parameter or body field returns ONLY the session identity's rows — the forged
  input is inert (filter from token). Mutant discriminates both directions.
- **WC-2b** **PROJECTION, ASSERTED IN BOTH DIRECTIONS (the P0):** a client-bound `get` and `list`
  response **CONTAINS** the enumerated client fields **AND PROVABLY LACKS** `events[]`, `routing`,
  and `resolution` — on a row where those fields are populated (an absence asserted against an empty
  row proves nothing). Mutant: remove the projection → the internal fields appear → the test FAILS.
  Exercised over the wire (the response body), never by reading the frontend.
- **WC-2c** **COMPLETENESS OF THE CLIENT LIST:** the "My Requests" view either returns ALL of the
  client's rows or **states its own bound** — no silent truncation. See the GSI decision routed to
  W-A (3.0.0_SA_CVO~Z P1-1): without a requester-keyed index this view rides a Limit-bounded scan plus
  in-memory filter, which is the estate's truncated-page class turned into a **client-facing
  completeness claim** (a client who filed 12 shown 8, with nothing saying so). If the index is not
  in place, this criterion requires the printed bound.
- **WC-3** CROSS-FIRM negative: a client token of firm X sees ZERO rows of firm Y (both
  directions); an internal token's board view unchanged (positive control).
- **WC-4** SVC-subject regression: svc-ticket-form stays CREATE-only, svc-analyst-intake stays
  CREATE + scoped-list; the existing 12/12 authz battery re-runs green.
- **WC-5** Portal view renders all three tabs against DEV with a client identity; claimed rows
  show claimer name+email; Completed shows the summary when present; screenshots READ; color law
  compliant.
- **WC-5b** ⛔ **A TERMINAL VALUE THAT IS NOT "COMPLETED" MUST NOT RENDER AS COMPLETED**
  (`3.0.0_SA_CVO~Z` CE finding 5 @97e58b0c14 — *the P0's shape one layer over*). The client tabs are
  Open / In Progress / Completed, and **a second terminal `status` value has NO TAB.** Rendered under
  "Completed", a **withdrawn / out-of-scope / duplicate** ticket **still reads to the client as
  resolved** — the original defect intact, now with better internal data behind it. **Internal-
  recorded is not client-rendered.** ⚠ **The per-value TAB MAPPING (and which values show NO AI
  summary) belongs to the closure-reason ruling at `1.0.0_SA_CTO~Z`, NOT to this TO** — this
  criterion exists to make the omission FAIL here rather than ship. Exercised per terminal value.
  ✅ **THE HOLD IS LIFTED — the `closure_reason` record was ADOPTED 21:14Z (@f834702451) and it
  covers what this criterion deferred.** Two halves, and the split matters for what W-C may decide:
  **RULED (correctness, the gate's):** a `status=closed` ticket **MUST NOT render under Completed**
  and **MUST NOT** carry the AI resolution summary — ⛔ **SOLE EXCEPTION `superseded`, where an
  outcome genuinely WAS delivered** (just not through this ticket). *Corrected 21:2xZ: my first fold
  of this ruling omitted that exception, and omitting it would have suppressed the summary on the
  one terminal value whose client legitimately received an answer — and on live-beta traffic, where
  one analyst answers in-thread and on the board, that is plausibly the COMMON ending.* The gate's
  own framing: **it rules that a closed ticket must not read as RESOLVED; it does not rule what it
  reads as.** **CARDED (product, Andrew's):** the client-facing
  **tab LABEL**, and **whether a client sees `closure_reason` at all.** ⛔ **So W-C builds the
  correctness half NOW and must NOT invent the label or the disclosure decision** — those are his.
  Adopted values carry MANDATORY POINTERS that the **client projection must carry**: `superseded`
  (name what met the need) · `duplicate` (the canonical ticket id) · `disputed` (the rejection
  message/event id) · `requester_unresponsive` (renamed from `expired`, because the definition was
  requester-bound while the name invited the sweep to reach for it as an **Opal-side ageout** — and
  **Opal-side ageout is NOT terminal**).
  Related: any reason carrying a POINTER (e.g. `duplicate` → the canonical ticket) must carry it
  into the client projection — *a terminal status without its pointer is the rot with a tidier
  label*, and a client told "duplicate" with no path to where their request actually lives is that
  rot made client-facing.
- **WC-6** Ship via the promote pattern (DT lane, /prod-deploy, freeze window declared to 2.0.0_SA_COO~Z);
  exercised on PROD both directions post-promote (the TO-F B-row pattern).
- **WC-7** Proof instance VALID rc=0 positional, ids WC-1..WC-7 (halves may file jointly; one
  instance).

<proof_of_spec>
  <expected_criteria>WC-1,WC-2,WC-2b,WC-2c,WC-3,WC-4,WC-5,WC-5b,WC-6,WC-7</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WC_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<compiler_tools_mandate>
Half (b): comp-blast on ticket_center lambda; comp-iam floor + live simulate for any new resource.
Half (a): comp-transform schema-check on the new view component (+ --feature for the new cohort);
/frontend-dev render loop before commit. Both: commit-gate.
</compiler_tools_mandate>

<cross_domain_coordination>
`infra/aws/lambda/ticket_center/lambda_function.py` SHARED with W-A (first) and W-D — rebase on
W-A; MCP before commit if W-D is concurrently editing. Portal tree: half (a) coordinates with any
live portal work via 2.0.0_SA_COO~Z census; promote freeze window binds all portal/DEV pushes.
</cross_domain_coordination>

## Do not
No client parameter may influence the filter (the mutant is the proof). No external-firm
visibility widening beyond READ-OWN (P3 scope stays parked). The main portal tree never leaves
DEV; promote via the skill only.

## Reporting
Each half reports to 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance); 0.0.0_AB_MSTR~Z coordinates the 0.4.0_DE_ClientPlatform~Z
seat window + ferry. Surprise channel: one line to 2.0.0_SA_COO~Z. Session logs = deliverables.
