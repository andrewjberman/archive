# TO D4_ETFPOS.TO-D4e — the Positioning page Models/ETFs flip UI (LAPTOP)

<task_order id="D4_ETFPOS.TO-D4e" project="ETFS_POSITIONING">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:55Z</issued>
<dated>on TO-D4c artifacts live + D1's TO-D1b registry</dated>
<status>superseded -- **SUPERSEDED-BY-DELIVERY, marked 2026-08-28 ~18:5xZ by `2.0.0_SA_COO~Z` (issuer)**. The Models/ETFs flip shipped as **`ETFS_POSITIONING.TO-3`, cell `ETFS-f-1`**, named in `Positioning.tsx`'s own header. **NO proof-of-spec instance for this TO** -- the discriminator, again. ⛔ **NOT "staged, never started".** ~~staged -- GATED ON TO-D4c artifacts + D1 TO-D1b~~</status>
<priority>P2</priority>
<authority>D4_ETF_POSITIONING_VARIANT_PRD.md §4.3 + §6 item 5 at dispatch vintage @2ecc24d0c8. Placement: LAPTOP (portal dev + screenshot law).</authority>
</task_order>

## Objective
Flip the Positioning page between **Models (unchanged)** and **ETFs**.

## THE D1 DEPENDENCY IS SCOPED TO THE REGISTRY, NOT TO D1
The PRD's "behind Item 1" dependency is **the category registry (D1's TO-D1b) for category
labeling — and nothing else.** You are NOT waiting on D1's projection, portal build, or acceptance
chain. Consume the registry for labels; do not re-coin category names locally (a vocabulary
re-coined beside a ratified one is a build-ladder duplicate).

## Mandate
`comp-transform schema-check` (MISSING = runtime undefined) + `comp-cache` collisions +
`comp-routes` where the new keys are fetched. **Rule 19: portal main worktree stays on DEV** — check
`git -C portal branch --show-current` first. Phase 3: `/frontend-dev` screenshot verification, and
READ the screenshot (silver-canvas colour law; a grep cannot see contrast).

## Acceptance criteria
- **D4e-1 FLIP RENDERS 4 ETFs** with holdings + allocation.
- **D4e-2 MODELS MODE BYTE-IDENTICAL BEHAVIOR** — the existing mode is a live surface and must be
  provably untouched. Show the comparison; "it looked the same" is not the criterion.
- **D4e-3 CATEGORY LABELS SOURCED FROM THE D1 REGISTRY**, not local strings.
- **D4e-4 SCREENSHOT READ + colour law checked.**
- **D4e-5 proof instance VALID rc=0 positional: ids D4e-1..D4e-5.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D4e-1,D4e-2,D4e-3,D4e-4,D4e-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D4_ETFPOS.TO-D4e_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## OPEN QUESTION ON THE FACE (Q2, at Andrew -- does NOT block you)
Does v1 of the flip require ATTRIBUTION parity (a holdings_attribution equivalent, which needs a
style/factor source), or ship allocation+holdings+summary first? **Proposed: allocation+holdings
first, attribution as v1.1.** Decision by TO-D4c's design freeze. Build to the proposed shape unless
the answer lands otherwise.

## Do not
- No PROD promote (DT lane). Stop at DEV.

## Reporting
COO at render-verified. Session log w/ Compiler Tools section.
