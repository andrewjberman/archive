# TO D1_CATVIEWS.TO-D1d — portal global-view build, five category views (LAPTOP)

<task_order id="D1_CATVIEWS.TO-D1d" project="MDPF_CATVIEWS">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:35Z</issued>
<dated>on TO-D1c's served artifact</dated>
<status>staged -- GATED ON TO-D1c (the served block is this build's input)</status>
<priority>P1-program</priority>
<authority>D1_ASSET_CATEGORY_VIEWS_PRD.md §4.3 + §6 item 4, at dispatch vintage @3e589fa1eb. Acceptance amended per CVO @d476339293 (the invisible-fallback class). Placement: LAPTOP (portal dev-server + screenshot verification proven here).</authority>
</task_order>

## Objective
Render the five category views on the MDPF global view, **CONSUMED — not merely rendered.** The
whole acceptance shape exists because a page that renders identically from a fallback and from real
data proves nothing about consumption.

## Mandate (three-phase)
- **Phase 1:** `comp-transform schema-check ModelPortfolios` (MISSING = runtime undefined) +
  re-run `comp-cache` collisions. Rule 20(b): dependency graph BEFORE the frontend commit.
- **Phase 2:** portal main worktree stays on **DEV** (Rule 19) — `git -C portal branch --show-current`
  before you touch anything; if it reads PROD, `git -C portal checkout DEV` first.
- **Phase 3:** `/frontend-dev` screenshot verification — READ the screenshot (silver-canvas colour
  law; a grep cannot see contrast).

## Acceptance criteria
- **D1d-1 POSITIVE CONSUMPTION:** five views render with **NON-NULL member lists** for at least one
  firm. A rendered page is not evidence when the fallback renders the same page.
- **D1d-2 EMPTY-FALLBACK EXERCISED EXPLICITLY:** drive the empty-`category_views` case on purpose
  and show it is **distinguishable in the test record** from the consumed case. Both states
  captured; if you cannot tell them apart in the record, D1d-1 is not established either.
- **D1d-3 SUM INVARIANT DISPLAYED:** displayed five-node sum == total_aua; no double-count
  expressible in the UI.
- **D1d-4 SPLITS + EMPTY STATES:** Primary/Custom and Advised/Residual splits correct;
  Alternatives/Insurance render a proper empty-state (not a crash, not a silent omission).
- **D1d-5 SCREENSHOT READ + colour law checked** on the silver canvas.
- **D1d-6 proof instance VALID rc=0 positional: ids D1d-1..D1d-6.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D1d-1,D1d-2,D1d-3,D1d-4,D1d-5,D1d-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D1_CATVIEWS.TO-D1d_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No PROD promote — that is a DT lane (`/prod-deploy`). Stop at DEV.
- Do not treat a green render as consumption. D1d-2 is the discriminator; it is not optional.

## Reporting
COO at render-verified, cc DS (0.4.0_DS_ClientPlatform) so the projection owner sees the consumption
result. Distinguish success from silent fallback. Session log w/ Compiler Tools section.
