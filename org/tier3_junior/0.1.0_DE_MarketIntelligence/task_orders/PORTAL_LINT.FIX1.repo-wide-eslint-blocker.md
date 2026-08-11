# PORTAL_LINT.FIX1 — unblock the repo-wide eslint gate (scoped cross-pod act)

<task_order>
<id>PORTAL_LINT.FIX1</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.1.0_DE_MarketIntelligence~Z</issued_to>
<date>2026-08-11</date>
<status>pending</status>
<priority>P2 — small, but it blocks every seat's lint gate</priority>

<scope>
`portal/src/pages/ModelPortfolios.tsx:873` fails `react-hooks/preserve-manual-memoization`. Because
`bun run lint` is `eslint .`, **the gate fails repo-wide for every seat regardless of the paths they
pass** — a seat that "ran lint and it failed" is reading a defect none of them introduced.

**CROSS-POD, DELIBERATELY AND ON THE RECORD:** this file is the PortfolioAnalytics pod's content, not
yours. The crossing is authorized because the fix is LINT-ONLY, the failure is infrastructure (a gate
down for everyone) rather than pod content, and you are live and portal-proven. **NAME the
PortfolioAnalytics pod owner in the commit message** so the crossing is recorded, never inferred.
</scope>

<requirements>
  <requirement id="1">**LINT-ONLY. ZERO BEHAVIOUR CHANGE.** If the violation cannot be resolved without altering behaviour — including memoization semantics that could change render timing — **STOP and tell me.** It then becomes 0.2.0_DE_PortfolioAnalytics~Z's, spawned properly. A behaviour change smuggled inside a lint fix is the worst version of a cross-pod act.</requirement>
  <requirement id="2">`bun run lint` clean repo-wide afterward — the gate's whole point is that it passes for everyone, so the verification is the REPO-WIDE run, not your file.</requirement>
  <requirement id="3">`tsc -b --noEmit` rc=0 (rc captured as the next statement).</requirement>
  <requirement id="4">DEV branch, no push, no PROD act.</requirement>
</requirements>

<acceptance_criteria>
  <criterion id="C1">`bun run lint` exits 0 REPO-WIDE — output cited, rc captured unpiped.</criterion>
  <criterion id="C2">Diff is lint-only; behaviour identical — state what the rule wanted and what you changed, so a reader can see no semantics moved.</criterion>
  <criterion id="C3">Commit message names the PortfolioAnalytics pod owner and cites this TO as the cross-pod authorization.</criterion>
  <criterion id="C4">Session-log line (no full log needed for a fix this size).</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4</expected_criteria>
  <instance_path>org/tier3_junior/0.1.0_DE_MarketIntelligence/deliverables/PORTAL_LINT.FIX1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<do_not>
  <rule>No behaviour change. No refactor beyond the rule's requirement. No touching anything else in the file.</rule>
  <rule>No push; DEV only.</rule>
  <rule>If it needs judgment about memoization semantics, STOP — that is pod-owner territory.</rule>
</do_not>
</task_order>
