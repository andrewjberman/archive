# TO D3_MODELOVERLAY.TO-D3.4 — Advisor Intelligence portal overlay UI (LAPTOP-ONLY)

<task_order id="D3_MODELOVERLAY.TO-D3.4" project="D3_ACCOUNT_MODEL_OVERLAY">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:50Z</issued>
<dated>on TO-D3.3's served key</dated>
<status>staged -- GATED ON TO-D3.3 + D1 registry (display names) + the D2-threaded dim_portfolio_group/bridge_group_account artifact</status>
<priority>P1-program</priority>
<authority>D3_ACCOUNT_MODEL_OVERLAY_PRD.md §4.4 + §6 item 4 at dispatch vintage @52a85baf08. Placement: LAPTOP-ONLY (portal dev/deploy chain).</authority>
</task_order>

## Objective
Render the account-level model overlay on Advisor Intelligence. The overlay components are absent
from portal/src/pages/AdvisorIntelligence/ today (run #7) — this is a build, not an edit.

## THE INVARIANT THIS UI MUST NOT BE ABLE TO BREAK
CVO's D3 verdict calls the overlap invariant the thing D3 CARRIES that D1 asserted away:
NO FIGURE MAY SUM AN ACCOUNT INTO TWO OR MORE BOOKS. Exercise it — do not reason about it.

## Mandate
- comp-routes trace (BOTH firm scopes when INF binds), comp-cache collisions,
  comp-transform schema-check (MISSING = runtime undefined). Rule 20(b): graph BEFORE the commit.
- Rule 19: the portal main worktree stays on DEV. Check git -C portal branch --show-current first;
  if it reads PROD, git -C portal checkout DEV before touching anything.
- Consume the D1 registry for display names — do not re-coin category labels here (a vocabulary
  re-coined beside a ratified one is the build-ladder duplicate, one layer up).

## Acceptance criteria
- D3.4-1 RENDERED OVERLAY ON DEV DIFFED VS THE SERVED JSON — the render matches the served key.
- D3.4-2 SCOPING VERIFIED ADMIN-VS-ADVISOR — an advisor sees their scope, an admin sees the whole;
  exercise BOTH, since a scope bug renders identically to correct behavior for whichever role you
  happen to test.
- D3.4-3 OVERLAP INVARIANT EXERCISED — construct or find the case where an account belongs to
  multiple groups and show no figure double-counts it.
- D3.4-4 UNRESOLVED-CLASS RENDER handled explicitly (it is a real state from TO-D3.1's residual
  enum, not an error).
- D3.4-5 /frontend-dev SCREENSHOT READ + silver-canvas colour law checked (a grep cannot see
  contrast).
- D3.4-6 proof instance VALID rc=0 positional: ids D3.4-1..D3.4-6. MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D3.4-1,D3.4-2,D3.4-3,D3.4-4,D3.4-5,D3.4-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D3_MODELOVERLAY.TO-D3.4_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No PROD promote (DT lane, /prod-deploy). Stop at DEV.

## Reporting
COO at render-verified, cc DS~B (served-key owner). Session log w/ Compiler Tools section.
