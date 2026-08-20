# OPAL_ANALYST.W4b — atom_decomp `/advisor-intelligence` (larger than the whole decomposed corpus)

<task_order>
<id>OPAL_ANALYST.W4b</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-12</date>
<status>closed-terminal -- DECLARED TERMINAL at the project close 2026-08-20 (CTO~Z 2533, simultaneous with the OPAL_ANALYST 2-step): NOT CONVERGED, 20 cells governance-held under @e56e9e2d4c, NO successor TO. Closed-as-declared, not completed. Flipped by 2.0.0_SA_COO~Z.</status>
<priority>P1</priority>
<!-- Sequenced AFTER W4a deliberately: W4a is the cheap census-less unit, this is the expensive one.
     Meeting census-lessness and 60 accessors in the same run confounds two hard things. -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §9 — **§9.2.1 (why this page is its own wave) + §9.8.1-V (dual-plane enumeration)**; full A–V regime binds.</ref>
  <ref type="prior-art">**NONE — census-less.** Plus W4a's reconciliation method, which you will have just built.</ref>
</references>

<scope>
`/advisor-intelligence`, page grain, one run: `runs/portal-page-advisor-intelligence/<stamp>/`.

**Measured at portal `ce98e334` (§9.2.1): 51 files · 24,905 lines · 60 `useQuery` · 0 `useMutation` ·
`src/api/endpoints/advisor-intelligence.ts` 1,500 lines, 0 writes.**

>> **THIS ONE PAGE EXCEEDS THE ENTIRE DECOMPOSED CORPUS: 24,905 lines against 16,303 for all eight
prior pages, and 60 accessors against 25.** It is pure-read, so today's axis fits — **the difficulty
here is SCALE, not kind.** <<

⚠ **Those are MY prior-claim counts under test. Re-derive them; a disagreement is a finding.**
</scope>

<requirements>
  <requirement id="1">**STATE THE SUB-GRAIN RULE IN THE AXIS DECLARATION, BEFORE MEASURING.** 60 accessors will tempt a collapse (families, tabs, panels) — a collapse is legitimate (W2's 79-slug family precedent) but only when **membership is verified per Rule 10, never asserted from a name**, and the rule is committed BEFORE it is convenient. **A collapse decided mid-run to make the rectangle finish is the failure this requirement exists to prevent.**</requirement>
  <requirement id="2">**Dual-plane enumeration (§9.8.1-V)** as in W4a — independent planes, both committed before reconciliation, disagreements are findings.</requirement>
  <requirement id="3">**Size is the risk; say so out loud in the domain bar.** State what you will NOT measure and why, BEFORE measuring (14b). **A declared exclusion is a result; a silent one is a hole**, and at 60 accessors silent holes are cheap to create and invisible afterwards.</requirement>
  <requirement id="4">Full §9.8.1 regime: evidence triples, validator-merged patches, lens-diverse DRY with at least one non-page-rooted lens, K-derivation, K.1 packet (c1/c2 excluded), K.2 attestation, sealed plant, denominators beside every count, rc captured as the next statement.</requirement>
  <requirement id="5">Findings only — no fixes, no deletions, nothing notification-shaped; residue gets Rule-9 disposition rows.</requirement>
  <requirement id="6">**If the run does not converge to DRY within your honest working window, STOP AND SAY SO rather than declaring DRY.** §9.4.1 already says DRY is not done; the inverse binds here — **an un-converged run reported as converged is the one outcome this page can produce that nothing downstream would catch.** A partial run with a stated frontier is a legitimate deliverable and I will take it.</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` for searches; `comp-estate` for the non-page plane; **`comp-cache collisions`** — at 60 accessors on one page, colliding/shared query keys are a live hazard and this is the deterministic instrument for it.</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py`.</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8   # POSITIONAL argv[2]; CHECK THE RC</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — semantics + certification with K.2 attestation. Hand off at DRY. **Flag the volume early** so the certifier's clock is not surprised.
- **1.0.0_SA_CTO~Z** — PRD owner; method findings + surprise channel to me.
- Lane commits only; no push.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">Axis + domain bar committed BEFORE measurement, **including the sub-grain/collapse rule (req 1) and the declared exclusions (req 3)**.</criterion>
  <criterion id="C2">Both enumerations committed independently before reconciliation; independence argued; disagreements named.</criterion>
  <criterion id="C3">Any family/panel collapse is **membership-verified per Rule 10** — membership, never the total, never the name.</criterion>
  <criterion id="C4">Rectangle schema-valid; declared/deployed/serving separated; SERVED limb grounded live or exercised.</criterion>
  <criterion id="C5">DRY by convergence, lens-diverse, ≥1 non-page-rooted lens — **or an honestly-declared non-convergence with its frontier (req 6)**.</criterion>
  <criterion id="C6">CVO~Z certification with reconstruction attestation; plant caught or attempt VOIDed and retained.</criterion>
  <criterion id="C7">Consumable derived from dry (K); K.1 packet exact, c1/c2 excluded.</criterion>
  <criterion id="C8">Session log + exclusions + surprises; semantics staged for W5.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/OPAL_ANALYST.W4b_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">Run package at `runs/portal-page-advisor-intelligence/<stamp>/`, full K-regime set</deliverable>
  <deliverable type="document">The collapse/sub-grain rule with its membership verification</deliverable>
  <deliverable type="document">Proof-of-spec, validator-clean before any flip; session log</deliverable>
</deliverables>

<do_not>
  <rule>No monitors/alerts · no fixes/deletions · no push · no mid-run collapse-of-convenience · no single-plane enumeration · **never report DRY you did not reach.**</rule>
</do_not>
</task_order>
