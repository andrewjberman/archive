# TO D7_TICKETING.WC-SITEZ — Ticket Lifecycle v2 W-C: client READ-OWN matrix + the portal "My Requests" view (JOINT, TO-F precedent)

<task_order id="D7_TICKETING.WC-SITEZ" project="OPAL_TICKET">
<issued_to>JOINT (the TO-F-SITEZ two-half pattern): half (b) MATRIX = 0.5.0_AE_OpalETL~Z (build; laptop apply leg via MSTR~Z ferry). Half (a) PORTAL VIEW = DE-class hands AT THE NEXT SEAT WINDOW (MSTR~Z spawn call — no DE~Z live at issuance); ship via the DT~Z promote pattern (portal-v2.1.164 precedent).</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>staged — half (b) activates after W-A lands (shared Lambda file, sequenced); half (a) activates at the DE-class seat window. CTO~Z sequencing: third of four.</status>
<priority>P2</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ @942d4d885c — his C2/C3/C4 client experience verbatim; CTO~Z ruling 2 (CLIENT VISIBILITY): client-human gains READ-OWN — list/get filtered SERVER-SIDE to the session identity's own rows (never a client parameter); the matrix widening is authorized by his word, scoped to this step. Tenant axis stays absolute.</authority>
</task_order>

## Objective
- **Half (b) — matrix:** `client-human` gains **READ-OWN**: list/get scoped server-side to rows
  where the requester matches the SESSION identity (filter derives from the token — never a client
  parameter). Tenant axis absolute: a client sees ONLY their own firm's own rows. Deny-by-default
  preserved everywhere else (svc subjects untouched; internal READ unchanged). PRD §7.3 matrix
  amendment rides CTO~Z's gate.
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
- **WC-3** CROSS-FIRM negative: a client token of firm X sees ZERO rows of firm Y (both
  directions); an internal token's board view unchanged (positive control).
- **WC-4** SVC-subject regression: svc-ticket-form stays CREATE-only, svc-analyst-intake stays
  CREATE + scoped-list; the existing 12/12 authz battery re-runs green.
- **WC-5** Portal view renders all three tabs against DEV with a client identity; claimed rows
  show claimer name+email; Completed shows the summary when present; screenshots READ; color law
  compliant.
- **WC-6** Ship via the promote pattern (DT lane, /prod-deploy, freeze window declared to COO~Z);
  exercised on PROD both directions post-promote (the TO-F B-row pattern).
- **WC-7** Proof instance VALID rc=0 positional, ids WC-1..WC-7 (halves may file jointly; one
  instance).

<proof_of_spec>
  <expected_criteria>WC-1,WC-2,WC-3,WC-4,WC-5,WC-6,WC-7</expected_criteria>
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
live portal work via COO~Z census; promote freeze window binds all portal/DEV pushes.
</cross_domain_coordination>

## Do not
No client parameter may influence the filter (the mutant is the proof). No external-firm
visibility widening beyond READ-OWN (P3 scope stays parked). The main portal tree never leaves
DEV; promote via the skill only.

## Reporting
Each half reports to COO~Z (validation) cc CTO~Z (acceptance); MSTR~Z coordinates the DE-class
seat window + ferry. Surprise channel: one line to COO~Z. Session logs = deliverables.
