# TO OPAL_ADVIPOINTERS.P4-PROMOTE-49F — PROD promote of the P4 repoint + the rendered acceptance read (push plan §3 row 4c, DT half)

<task_order id="OPAL_ADVIPOINTERS.P4-PROMOTE-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DT_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>R+3, where R = Schwab FAM resumption for 08335338 (RE-DATED from 2026-08-22 by COO notice @f79760179a, 2026-08-19 1311Z: vendor-side FAM outage after as_of 08-10; chain = floor/P3 R+1, pins R+2, flip R+3). Still executes at DE's P4R-5 handoff; payload = their flip commits exactly; PROD..DEV re-measured at GO-time.</dated>
<status>superseded -- payload served in d9a98bcc (ancestor of origin/PROD); flipped by 2.0.0_SA_COO~DV for the unseated base issuer</status>
<priority>P1 — the phase-close criterion for row 4c is the portal VERIFIED taking data in and displaying it; your rendered read IS that evidence</priority>
<authority>Push plan @a2f27c8d0a §3 row 4c + §2 DT row. /prod-deploy is the canonical procedure (DT lane). GATE-5 mechanics from your 154211Z stand ADOPTED: `git push origin PROD` is integrator-only for your serial — run /prod-deploy through merge/parity/worktree, hand MSTR the exact push, verify CI yourself. No audited override.</authority>
</task_order>

## Objective
Promote DE's repoint commits DEV->PROD per /prod-deploy, with MSTR executing the PROD push, then
deliver the rendered + behavioral acceptance read (AC-P3 pattern) on the DEPLOYED bundle against the
served `platinum/advi/49financial` artifacts.

## Compiler tools (three-phase)
Phase 1: payload enumeration (`git -C portal log origin/PROD..origin/DEV --oneline`) — expect EXACTLY
DE's enumerated repoint commits, nothing else; if anything else appears STOP and route to COO (a
promote is not a sweep). Phase 2: /prod-deploy's own gates (zero TS errors, ephemeral worktree, DEV
main tree untouched). Phase 3: CI conclusion via `gh run view --json` (never `gh run watch`), sha +
annotated-tag peel verified.

## Cross-domain coordination
- shared_resource: portal PROD branch — MSTR executes the push (integrator law); hand them the exact
  ref + sha; verify from the REMOTE after.
- shared_resource: `platinum/advi/49financial/**` (read for fixtures) — DS~B/CVO own content; your
  read is acceptance, not validation of values (CVO's cert did that).

## Acceptance criteria
- P4X-1 PAYLOAD EXACT: promoted set == DE's P4R-5 enumeration (commit list printed, both sides).
- P4X-2 PROMOTE CLEAN: /prod-deploy completed — DEV main tree confirmed back on DEV, worktree torn
  down, workspace submodule pointer updated on CLOUD; MSTR's push verified from origin (sha + tag).
- P4X-3 CI VERIFIED: the CI run's conclusion read via `gh run view --json` = success, deployed sha ==
  promoted sha.
- P4X-4 RENDERED + BEHAVIORAL READ: `portal/scripts/ui-smoke.mjs` on the AdvisorIntelligence route
  `--origin https://opalinvest.dev --firm 49financial` against served platinum/advi fixtures —
  screenshot READ (silver-canvas law) + behavioral assertions pass; evidence = the smoke output + the
  screenshot, per flipped surface. This read is the row-4c close evidence AND a P5-gate input (the
  framework's "portal VERIFIED taking data in correctly and displaying it").
- P4X-5 proof instance VALID rc=0 positional: ids P4X-1,P4X-2,P4X-3,P4X-4,P4X-5.

<proof_of_spec>
  <expected_criteria>P4X-1,P4X-2,P4X-3,P4X-4,P4X-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.P4-PROMOTE-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No pre-promote ("I do not pre-promote" — kept). No PROD push from your serial. No promote if the
  payload enumeration shows anything beyond DE's set.

## Reporting
COO (cc CTO, DE, CVO, MSTR) at promote-complete with the rendered-read evidence. Surprise channel:
one banked line to COO. Session log with Compiler Tools section = deliverable.
