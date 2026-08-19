# TO D3_MODELOVERLAY.TO-D3.5 — behavioral acceptance pass (EITHER -> LAPTOP)

<task_order id="D3_MODELOVERLAY.TO-D3.5" project="D3_ACCOUNT_MODEL_OVERLAY">
<issued_to>3.0.0_SA_CVO</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:50Z</issued>
<dated>on TO-D3.4</dated>
<status>staged -- GATED ON TO-D3.4; this row closes D3</status>
<priority>P1-program (the acceptance gate)</priority>
<authority>D3_ACCOUNT_MODEL_OVERLAY_PRD.md §6 item 5 at dispatch vintage @52a85baf08. Placement: EITHER -> LAPTOP by the standing default (read-only against DEV + served keys).</authority>
</task_order>

## Objective
Exercise the USER STORY, not the components: "what is this account in?" -> "seventy-thirty."

## Acceptance criteria
- D3.5-1 THE USER-STORY READ EXERCISED ON REAL ACCOUNTS — the question asked and answered end to
  end, on live data.
- D3.5-2 AT LEAST ONE UNRESOLVED-CLASS RENDER included in the exercised set. A pass measured only on
  accounts that resolve cleanly is measured on the easy half of the domain.
- D3.5-3 THE OVERLAP INVARIANT INDEPENDENTLY RE-DERIVED — not accepted from TO-D3.4's own report.
  A tie is evidence only when the legs differ in derivation.
- D3.5-4 proof instance VALID rc=0 positional: ids D3.5-1..D3.5-4. MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D3.5-1,D3.5-2,D3.5-3,D3.5-4</expected_criteria>
  <instance_path>org/tier1_exec/3.0.0_SA_CVO/deliverables/D3_MODELOVERLAY.TO-D3.5_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at verdict, cc CTO. Session log w/ Compiler Tools section.
