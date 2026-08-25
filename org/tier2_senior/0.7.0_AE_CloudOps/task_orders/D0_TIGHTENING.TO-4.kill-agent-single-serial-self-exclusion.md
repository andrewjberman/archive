# TO D0_TIGHTENING.TO-4 — kill-agent.ps1 single-serial self-exclusion (LAPTOP, small)

<task_order id="D0_TIGHTENING.TO-4" project="D0_INFRA_TIGHTENING">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:45Z</issued>
<dated>any window -- small, no gate</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "D0_TIGHTENING" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged -- GO paired; UNGATED, take it whenever a window opens</status>
<priority>P3 (small), but it is a self-inflicted-outage class -- a seat that kills itself while reaping is an expensive small bug</priority>
<authority>D0_INFRA_TIGHTENING_PRD.md §4c + §6 row 4 at dispatch vintage @4bf291b26c. Placement: LAPTOP (CTO ruling FINAL); exercise on BOTH devices per §7.</authority>
</task_order>

## Objective
`kill-agent.ps1` must exclude the CALLER's own serial from a single-serial match.

## Acceptance criteria
- **K-1 SELF-MATCH EXCLUDED, POSITIVE-CONTROLLED:** `needle == own serial` kills **nothing** and
  **prints the exclusion**. Both limbs — a silent no-kill is indistinguishable from a broken matcher.
- **K-2 `-All` BEHAVIOR UNCHANGED** (regression check, exercised not asserted).
- **K-3 EXERCISED ON BOTH DEVICES** (§7: repo + powershell, both fabrics). A one-device green is
  partial and reported as partial.
- **K-4 proof instance VALID rc=0 positional: ids K-1..K-4.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>K-1,K-2,K-3,K-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D0_TIGHTENING.TO-4_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No device-specific logic (device-agnostic law): resolve the workspace root via
  `git rev-parse --show-toplevel`, never a baked `C:\Users\<name>` path or drive prefix.

## Reporting
COO. Session log w/ Compiler Tools section.
