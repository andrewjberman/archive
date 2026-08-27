# TO D7_TICKETING.WC-SITEZ — Ticket Lifecycle v2 W-C: client READ-OWN matrix + the portal "My Requests" view (JOINT, TO-F precedent)

<task_order id="D7_TICKETING.WC-SITEZ" project="OPAL_TICKET">
<issued_to>JOINT (the TO-F-SITEZ two-half pattern): half (b) MATRIX = 0.5.0_AE_OpalETL~Z (build; laptop apply leg via 0.0.0_AB_MSTR~Z ferry). Half (a) PORTAL VIEW = **0.4.0_DE_ClientPlatform~Z** at the next seat window ⛔ **[MEASURED 22:10Z: THAT SERIAL HAS NEVER REGISTERED THIS SESSION — it has no entry in `liveness.json` at all, stale or otherwise (6 seats present, denominator stated). So this half's assignee is a NAMED-BUT-UNSEATED serial. `0.0.0_AB_MSTR~Z` carries a drafted spawn queued on slot availability, which makes this CAPACITY-BLOCKED rather than owner-blocked — a different state taking a different answer. Do not read the assignee line as a live seat until it registers. **CONFIRMED 22:11Z by `0.0.0_AB_MSTR~Z` FROM PROCESS TRUTH, not recollection: 7 live serials = SIX ~Z working seats + the BG utility seat (Andrew-scheduled, not a working-slot consumer). DE~Z would be a SEVENTH ~Z spawn against a 6-CEILING, and Accept-7 was already ruled NO. THEREFORE THE PATH IS A SWAP, AND NAMING THE SEAT TO RELEASE IS `2.0.0_SA_COO~Z`'s ALLOCATION CALL — `0.0.0_AB_MSTR~Z` executes on a handoff-save / no-in-flight signal and deliberately nominates nobody. NOT exercised today: nothing is hot enough to justify releasing a working seat, and this half is staged behind W-A regardless. WHEN W-C GOES HOT, THE NAMING IS THE FIRST ACT — not a discovery.**]** (0.0.0_AB_MSTR~Z spawn call — that serial was not live at issuance); ship via the 0.4.0_DT_ClientPlatform~Z promote pattern (portal-v2.1.164 precedent).
⚠ **ADDRESSING NOTE (Andrew-direct 2026-08-20 ~2036Z, record @9e1e94c4f4 — agents refer to other agents by FULL SERIAL):** this line previously read "DE-class hands", which is not an address at all. **And the hazard is sharper here than the general rule:** `0.4.0_DE_ClientPlatform~Z` and `0.4.0_DT_ClientPlatform~Z` differ by ONE LETTER and BOTH are real registered seats — so a one-character slip delivers to a live wrong seat and `send_message` returns DELIVERED. Half (a) is the DE seat (portal build); the promote is the DT seat.</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_TICKET, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: ⚡ **HALF (b): ACTIVATION CONDITION MET 2026-08-21T1610Z -- VERIFIED AT THE ISSUING SEAT, NOT RELAYED.** The condition was *"after W-A lands (shared Lambda file)"*; the chain is measured end to end: **(1)** W-A `81c502cff2` **IS an ancestor of HEAD**; **(2)** the DEPLOYED `lambda_function.py` is **byte-identical to HEAD** (sha256 `96bd2df561b6...`, negative control HEAD~20 differs, confirmed at three independent seats); **(3)** W-A's diff touches that exact shared file (+178). **W-A is therefore IN the deployed artifact and half (b) is ACTIVE by the TO's own terms** -- no new dispatch, and `1.0.0_SA_CTO~Z` correctly neither activated nor held it.
    ⛔ **TWO ANDREW-DIRECT RULINGS ~1600Z NOW BIND THE WORK DOWNSTREAM OF THIS TO (spec @f1c66559bc): (A) NO FIRM SEES THE MERGED TICKET CENTER UNTIL ROLLOUT** -- `/ticket-center` stays double-gated (`requireInternal` AND absent from all four firm allowlists) and **both gates already hold, so honouring this costs one line of discipline -- DO NOT EDIT `firmAccess.ts` -- and requires building nothing**; **(B) T1 IS THE BUILD TARGET** (tab 1 = NOT-YET-ACCEPTED; client sees submit + own pending, labelled *Submit*; internal sees the same tab as *Open*).
    ⛔⛔ **THE ORDERING TRAP BELOW IS *MOOT* -- ANDREW-DIRECT ~1610Z, VERBATIM: *"No firms file tickets anyway we have never even explained this to them so its moot"*.** The hazard rested on an **UNMEASURED USAGE PREMISE** -- that three firms file through `/submit-request` today -- and the sovereign falsified it: **nobody files, because nobody was ever told the route exists.** Retiring `/submit-request` at merge therefore strands no one, and **the consumers-first ordering is now a FREE DESIGN CHOICE, not a safety requirement** -- if it is still wanted it must be argued on other grounds. **I recorded it at 1610Z and it was false when I wrote it; struck by the same seat 10 minutes later, text preserved below rather than deleted.**
    ⛔ **WHAT THIS DOES *NOT* CLEAR, AND THE DISTINCTION IS THE WHOLE POINT: RULING A STANDS** (no firm allowlist gains `/ticket-center` until he rolls it -- he called the TRAP moot, not the RULING), **AND THE CLIENT-VIEW-UNEXERCISED GAP STANDS UNTOUCHED.** That gap is about **RENDERING, NOT USAGE**: *"no firm files tickets"* says nothing about whether the client view **draws correctly for a client principal**. It still needs a client-principal fixture or a seeded test tenant, and **deploying still does not discharge it.** *Do not let a moot usage premise carry an unrelated acceptance gap out with it.*
    ~~**SUPERSEDED, retained as the record of what was believed: THE ORDERING TRAP, RECORDED HERE BECAUSE THIS TO STARTS THE CHAIN THE WHOLE IA CHANGE SITS ON: `/submit-request` NOW RETIRES AT ROLLOUT, NOT AT MERGE.** Three firms (49financial, cottonwood, demo -- NOT inflection) file through it today. **Retiring it when the merged page lands, while that page is still firm-invisible, leaves those three firms with NO way to file a ticket at all.** The route retirement is the **LAST** act of the rollout, **AFTER** the allowlist flip. *Consumers first was already good practice; Ruling A makes the ordering load-bearing.*~~
    ⚠ **AND THE CLIENT VIEW SHIPS UNEXERCISED BY CONSTRUCTION:** if no firm can reach the page, **no real client session renders the client view before rollout.** DEPLOYING DOES NOT DISCHARGE IT -- acceptance needs a client-principal fixture or a seeded test tenant. Same discipline as D-3 and WF-2/WF-11; **named now so it is not discovered at the flip.**
    Q2 needs no new word -- READ-OWN (`'own'`) is already authorized Andrew-direct @942d4d885c. **Prior status, superseded, retained verbatim:** staged — half (b) activates after W-A lands (shared Lambda file, sequenced); half (a) activates at the 0.4.0_DE_ClientPlatform~Z seat window (**unchanged -- still capacity-blocked on that seat**). 1.0.0_SA_CTO~Z sequencing: third of four.</status>
<priority>P2</priority>

<!-- ================================================================================ -->
<!-- COO~Z CONSTRAINT CORRECTION 23:15Z -- CAPACITY IS NOT THE BINDING GATE           -->
<!-- ================================================================================ -->
<!--
⛔ THIS TO HAS BEEN CARRIED (BY ME, IN MY OWN DRIVE LOGS, FOR SEVERAL TICKS) AS
"W-C CAPACITY-BLOCKED BEHIND THE 6-SEAT CEILING." THAT NAMES THE WRONG CONSTRAINT, and the
error is not cosmetic: it implies FREEING A SEAT WOULD UNBLOCK THIS LANE. IT WOULD NOT.

MEASURED 23:15Z, from the TOs themselves:
  W-C half (b)  staged BEHIND W-A            (shared Lambda file, CTO~Z-sequenced)
  W-A           <status>pending</status>     GO rides a commit's MCP, QUEUED BEHIND dep-3
                                             registration (CTO~Z @942d4d885c: "the current
                                             dep-2/dep-3 chain is UNCHANGED and remains the
                                             critical path")
>> SO W-C IS TWO LINKS BACK: dep-3 -> W-A -> W-C(b). CAPACITY IS A THIRD CONSTRAINT THAT DOES
   NOT BIND UNTIL THE FIRST TWO RELEASE.

⛔⛔ CORRECTED AGAIN 23:22Z, BY THE SAME SEAT, ONE TICK LATER — THE TWO-LINK CHAIN ABOVE IS
   ITSELF WRONG, AND IT IS WRONG BECAUSE I READ W-A's <status> AS CURRENT STATE.
   MEASURED:
     dep-3   CLOSED ~20:12Z — "dep-3 ACCEPTED: TAC-3 SCHEDULE-LANDED" @399df8444a
     W-A     BUILD COMPLETE + PROOF-VALIDATED — @81c502cff2, @9121a55330, @7e98926a41
             (WA-1..WA-10, VALID rc=0 positional), @133b0f24b0; COO-validated deliverable
             laneZ_VALIDATION_20260820_WA_build_leg.md
     W-A's <status> field   AUTHORED 20:04:32Z (@9eeb173dc5) -- FIVE MINUTES AFTER the dep-3
             feat commit (19:59:41Z), ~6 min BEFORE its accept/validate. ACCURATE WHEN WRITTEN,
             STALE WITHIN SIX MINUTES; the file was then edited three more times (21:45:50Z,
             21:48:11Z, 21:53:17Z) WITHOUT THE STATUS LINE BEING REVISITED.
             ⛔ MY FIRST VERSION SAID "LAST TOUCHED 17:53Z ... BEFORE dep-3 closed." BOTH HALVES
             WRONG: 17:53 was LOCAL (-04:00) = 21:53Z, and a FILE's last touch is not a LINE's
             last change. I rendered local time with no marker and read it as UTC.
>> THE REAL CHAIN IS ONE LINK, NOT TWO: **THE W-A APPLY -> W-C(b)**. dep-3 is discharged and
   W-A's build is done; what remains is the laptop-side apply (WA-6 grant first, then the
   deployed WA-1/2/8 exercises). Capacity remains a further constraint behind that.
>> I CORRECTED A WRONG CONSTRAINT BY CITING A STALE FIELD AND PRODUCED A DIFFERENTLY WRONG
   CONSTRAINT, WITH MORE CONFIDENCE, AND BROADCAST IT TO THREE SEATS TELLING THEM TO UPDATE
   THEIR BOARDS. The first correction was right about capacity not binding and wrong about what
   does. Both errors have the same root: I TREATED A <status> FIELD AS A MEASUREMENT.
   A CLOSED DEPENDENCY DOES NOT GO BACK AND EDIT THE FIELDS THAT NAMED IT — and the evidence
   that dep-3 had closed was sitting in MY OWN TICK-20 DRIVE LOG the whole time.
   W-A's status field is corrected at HEAD; this block is kept because the retraction is the
   record. The TO's own text already said "this half is staged
   behind W-A regardless" -- the sequencing clause was here the whole time, sitting beside the
   capacity paragraph, and the capacity paragraph is the one that got carried forward because
   it is the one that sounds actionable.

⛔ AND THE DRIVE IMPERATIVE PUSHED ME AT THE WRONG ACT. "Resolve gates, don't attest them"
   plus a drained seat (0.4.0_DT_ClientPlatform~Z closed with 0 TOs) reads as: MAKE THE
   ALLOCATION CALL NOW. That would have RELEASED A WORKING SEAT FOR A LANE THAT CANNOT START
   FOR TWO MORE LINKS. A gate that is real but NOT THE BINDING ONE still refuses to open, and
   the effort spent opening it is spent.
   THE ALLOCATION CALL IS UNCHANGED AND REMAINS MINE -- MSTR~Z's swap path stands and the
   naming is still the first act WHEN W-C GOES HOT. What is corrected is WHEN "hot" arrives:
   not when a seat frees, but when W-A lands.

⚠ SECOND CORRECTION, SAME PARAGRAPH: "THAT SERIAL HAS NEVER REGISTERED THIS SESSION" is
   true of liveness.json and reads as "this serial has never existed." IT HAS.
   MEASURED: org/mcp/agent_telemetry/0.4.0_DE_ClientPlatform~Z.jsonl carries 289 ROWS, last
   work-call 2026-08-20T16:18:43Z -- ~6.9 HOURS before this note.
>> 0.4.0_DE_ClientPlatform~Z IS A LAPSED SEAT, NOT A NEVER-SPAWNED SERIAL. That matters to
   whoever seats it: a lapsed seat may carry in-flight state, partial work, or a handoff that
   a fresh spawn would not inherit. Check before assuming a clean start.
⚠ AND NOTE THE INSTRUMENT TRAP THIS EXPOSES: THE TELEMETRY FILE'S EXISTENCE IS NOT A
   LIVENESS SIGNAL. DE~Z has a file; it is 6.9h stale. An age filter is what separates them,
   and a census keyed on file-presence alone would have read this seat as live.
-->
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
  client's rows or **states its own bound** — no silent truncation.
  ⛔ **THIS CRITERION IS NOW THE OBLIGATION-HOLDER FOR THE GSI DECISION (W-A DECIDED 21:4xZ
  @81c502cff2: NO INDEX IN W-A).** The reasoning is sound and worth carrying: **the requester-keyed
  access pattern's correct key depends on W-C's query shape, which is unsettled — and a guessed index
  is a second home for an unspecified pattern.** So the decision was not deferred vaguely; it was
  **transferred with a named obligation: if this view lists client tickets by SCAN, it MUST PRINT ITS
  BOUND.** Deciding the index here (once the query shape is real) is in scope; shipping a silent
  scan is not. See the GSI decision routed to
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

## Do not
No client parameter may influence the filter (the mutant is the proof). No external-firm
visibility widening beyond READ-OWN (P3 scope stays parked). The main portal tree never leaves
DEV; promote via the skill only.

## Reporting
Each half reports to 2.0.0_SA_COO~Z (validation) cc 1.0.0_SA_CTO~Z (acceptance); 0.0.0_AB_MSTR~Z coordinates the 0.4.0_DE_ClientPlatform~Z
seat window + ferry. Surprise channel: one line to 2.0.0_SA_COO~Z. Session logs = deliverables.
