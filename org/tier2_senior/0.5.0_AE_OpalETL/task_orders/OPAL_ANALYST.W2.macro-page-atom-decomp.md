# OPAL_ANALYST.W2 — atom_decomp `/macro` (page 8 of 16; the wave's learnings bound)

<task_order>
<id>OPAL_ANALYST.W2</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-11</date>
<status>pending</status>
<priority>P1</priority>
<!-- W1 closed 6/6 certified @1927Z; this GO is immediate — same method, one page, everything W1
     paid for bound below rather than remembered. -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §9 (v-current @81a18881a2) — §9.8.1 A-L + K/K.1/K.2/K.2e, §9.9 item 5 incl. the CADENCE-HOMOGENEITY PREDICATE</ref>
  <ref type="prior-art">ARTIFACT_CENSUS_MACRO.yaml @5efce36b7 — 84 keys: 5 top-level + the 79-slug timeseries FAMILY; 4 rendered types; 2 unrendered; frozen adjacent (market-metrics.json.gz); borrowed manifest pointer. INPUT, never evidence (§9.0).</ref>
  <ref type="method">your own W1 emitter + K.1 packet + K.2 attestation regime; CVO's W5 lift constraints @f28e15d4b5 (L-1 full-key rows, L-3 no footer fallback bind your rows too)</ref>
</references>

<scope>
`/macro`, page grain, one run: `workflows/atom_decomposition/runs/portal-page-macro/<stamp>/`.
**The slug-parameterized timeseries family (79 keys) is ONE entity with family grammar** — the
census's own collapse rule, membership-verified (Rule 10), never 79 rows. Modal lazy-load per
indicator click is a consumer-set property to MEASURE (K8 call-site grain), not assume.

**Packaging fix bound here (CVO's third-page note): the verifier packet carries K.1's EXACT set —
c0 + pre-dry patches + final + run.json + constraints + seal. `rectangle.c1/c2` are NOT packet
members.** No capability cost today; it does not carry into a third wave.
</scope>

<requirements>
  <requirement id="1">Full §9.8.1 regime: axis + domain bar committed BEFORE measurement; evidence triples; validator-merged patches; lens-diverse DRY; K-derivation (consumable from dry); K.1 packet (corrected composition); K.2 attestation at certification; fresh sealed plant, coordinates never in-object.</requirement>
  <requirement id="2">**Run the CADENCE-HOMOGENEITY PREDICATE explicitly (new instrument, first deliberate application):** classify every artifact's cadence, state whether the page's set is homogeneous, and PREDICT the footer-binding verdict BEFORE measuring it — /macro mixes a daily FRED chain, an unrendered staging twin, a superseded VIX artifact and a frozen legacy adjacent, so it is a strong test. A pre-filed prediction that fails is a FINDING about the predicate and goes to the register either way.</requirement>
  <requirement id="3">Enumerator v2 grain (distinct artifacts vs real accessors, call-site counts); type imports are not consumers; denominators printed beside every count; rc captured as the next statement.</requirement>
  <requirement id="4">Census as input; every run-vs-census disagreement NAMED (the MACRO census's unrendered/frozen claims are prior claims to re-ground).</requirement>
  <requirement id="5">Findings land as findings — no fixes, no deletion, nothing notification-shaped; residue gets dispositions (the frozen `market-metrics.json.gz` and superseded `vix_data.json` are Rule-9 disposition rows, never acts).</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-estate` macroeconomics thread (9 chains, 6 in-scope per the census — verify that frame); `comp-which` for searches.</before_write>
  <before_commit>`.tools/commit-gate.sh` on any `.py`.</before_commit>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7,C8,C9   # POSITIONAL argv[2]; CHECK THE RC</after_commit>
</compiler_tools_mandate>

<cross_domain_coordination>
- **3.0.0_SA_CVO~Z** — semantics (Plane B/C only, evidence as objects) + certification with K.2 attestation + register extension. Hand off at DRY.
- **1.0.0_SA_CTO~Z** — PRD owner; method findings to me; surprise channel to me.
- **0.8.0_AE_CloudComp~Z** — running the instruments decomposition in parallel from now; comp-* tools you both touch are THEIR entities and YOUR instruments — if your run surfaces a comp-tool defect, it routes to their run as a prior claim, not into your rectangle.
- Lane commits only; no push.
</cross_domain_coordination>

<acceptance_criteria>
  <criterion id="C1">Axis + domain bar committed verifiably before first measurement.</criterion>
  <criterion id="C2">Rectangle schema-valid; family entity membership-verified (79 slugs, Rule 10 — membership, never the total).</criterion>
  <criterion id="C3">Declared/deployed/serving separated per artifact; SERVED limb grounded live or exercised.</criterion>
  <criterion id="C4">DRY by convergence, lens-diverse, evidenced in run.json.</criterion>
  <criterion id="C5">**Predicate row delivered: cadence classification per artifact + homogeneity verdict + the PRE-FILED footer-binding prediction and its outcome.**</criterion>
  <criterion id="C6">Census reconciliation stated; disagreements named; zero-disagreement stated explicitly if so.</criterion>
  <criterion id="C7">`certification.json` signed by CVO~Z with reconstruction attestation; plant caught or attempt VOIDed and retained.</criterion>
  <criterion id="C8">Consumable derived from dry (K); packet = K.1 exact set, c1/c2 EXCLUDED, composition stated in the handoff.</criterion>
  <criterion id="C9">Session log + declared exclusions + surprises; semantics staged for W5 per the lift constraints.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8,C9</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/OPAL_ANALYST.W2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">Run package at `runs/portal-page-macro/<stamp>/`, full K-regime artifact set</deliverable>
  <deliverable type="document">Predicate row (C5) — the register's first deliberate pre-ship application</deliverable>
  <deliverable type="document">`OPAL_ANALYST.W2_PROOF_OF_SPEC.json`, validator-clean</deliverable>
  <deliverable type="document">Session log</deliverable>
</deliverables>

<do_not>
  <rule>No monitors/alerts (moratorium) · no fixes/deletions (Rule 9) · no panel-grain decomposition · no push · census never cited as run evidence · c1/c2 never in the verifier packet.</rule>
</do_not>
</task_order>
