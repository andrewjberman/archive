# OPAL_ANALYST.TO4a — Model Portfolios artifact census + /draw (vertical 1 pilot)

<task_order>
<id>OPAL_ANALYST.TO4a</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-10</date>
<status>pending</status>
<!-- ACCEPTED-PENDING-REVIEW 2026-08-10 1815Z, 2.0.0_SA_COO~Z. Census @0c1dae3da
     (ARTIFACT_CENSUS_MP.yaml, 285 lines, COO spot-check: parse clean, header denominator
     482 keys itemized + scope-family dedup note, five-rule self-score with evidence);
     /draw of complete findings @fb2180c80 delivered to MSTR~Z for Andrew. Flip to complete
     on Andrew's structuring word (the Andrew-asked gate); that word also unlocks TO-4b.
     Registry-relevant finding (non-uniform vintage fields across the vertical -> per-artifact
     vintage_field in the 8.2 design) forwarded to CTO~Z. -->
<priority>P1</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §8.1 census grammar + §8.2 registry ruling (@7753e1caf)</ref>
  <ref type="charter">org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/ANDREW_DIRECT_20260810_TO4_VERTICAL_PLAN_BRIEFING.md @6c1161075 (Andrew verbatim — the plan)</ref>
</references>

<scope>
Vertical 1 pilot per Andrew's ruled order (MP → Pod-2 → Macro → News). TWO deliverables:

1. **MP artifact census** — one YAML at 0.0.3_BG agent home `refs/census/` per PRD §8.1's
   grammar (copy the worked skeleton): five levels, visual-first, page → location{header|tab}
   → panel → artifact → field. Every portal-served Model Portfolios artifact. The FIVE BINDING
   RULES are the scoring bar: (1) one-grain-per-level, no skips; (2) artifact dedup — one
   canonical entry + pointers, field lists never duplicated; (3) MECE with the DENOMINATOR
   printed in the file header (PORTAL_RETRIEVAL census + comp-estate thread); (4) state axis
   explicit (live|frozen|staged — frozen rows marked, never omitted); (5) per-row grounding
   evidence (portal_lookup ref for fields, screenshot/component file:line for panels).
2. **/draw of the COMPLETE findings** — the rendered census, house two-plane style, delivered
   to Andrew via MSTR~Z (his terminal channel).

**ANDREW'S STRUCTURING REVIEW GATES ALL FURTHER VERTICALS** (his design, verbatim: "if I like
the structuring, they can proceed to the other surfaces" — an Andrew-asked gate). Do NOT begin
Pod-2/Macro/News census work. Registry (DATA_CATALOG v0.2) additions are POST-review per §8.2 —
not in this TO. Inferential derivations are post-baseline — out entirely.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read PRD §8.1 (grammar + skeleton) @7753e1caf + the Andrew briefing @6c1161075 verbatim section</run>
      <expect>Census structure copied from the skeleton, not improvised; Andrew's page→location→panel→field hierarchy is the spine.</expect>
      <if_mismatch>STOP. A grammar deviation invalidates the pilot as the template for verticals 2-4; reconcile with CTO~Z first.</if_mismatch>
    </step>
    <step>
      <run>.tools/comp-estate for the MP/model-portfolios thread (--list first if the name needs resolving; read the provenance header, --refresh if the name snapshot is >14d)</run>
      <expect>The MP serving thread enumerated: produced artifacts + served keys + frontend consumers. This plus refs/PORTAL_RETRIEVAL.md's channel census IS the denominator for binding rule 3.</expect>
      <if_mismatch>STOP. A census whose denominator you cannot state fails MECE by construction; surface to COO~Z.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Validate the census YAML: parse clean (python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>), then self-score against the five binding rules, one line each in your log</run>
      <expect>Parse clean; 5/5 rules self-scored PASS with the evidence named (denominator line quoted, dedup pointer count, state-axis rows counted, grounding refs spot-checked).</expect>
      <if_mismatch>STOP. Do not commit a census that fails its own scoring bar.</if_mismatch>
    </step>
    <step>
      <run>Commit via safe-commit under the audited lane-override pattern you used for RELAUNCH.md (agent-home path, TIER0_UTILITY)</run>
      <expect>Commit lands with override audited; no push (LD-0367).</expect>
      <if_mismatch>STOP; surface the refusal verbatim to COO~Z, never --force.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>/draw the complete census findings (two-plane house style); deliver the rendered artifact to MSTR~Z for Andrew's structuring review, cc COO~Z</run>
      <expect>The /draw covers the COMPLETE findings (every censused page/panel/artifact — no top-N truncation; if anything is elided, the elision is printed on the drawing per no-silent-caps).</expect>
      <if_mismatch>Surface to COO~Z before delivery — an incomplete /draw corrupts the very structuring review that gates verticals 2-4.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
`refs/census/` is a NEW directory in the 0.0.3_BG agent home — no other open TO writes there
(MSTR~Z as integrator owns the home's steady-state; census authorship here is TO-scoped and
audited, same pattern as RELAUNCH.md). Read-only over portal/PORTAL_RETRIEVAL/comp-estate;
no serving path, no pipeline, no gateway change. The live 0.0.3_BG seat is unaffected until
it re-reads refs.
</cross_domain_coordination>

<acceptance_criteria>
1. Census YAML at agent-home refs/census/ passes ALL FIVE §8.1 binding rules (self-scored in
   log, each rule with named evidence; COO spot-checks).
2. Denominator printed in the file header and consistent with the Phase-1 enumeration.
3. /draw of the COMPLETE findings delivered to MSTR~Z for Andrew (cc COO~Z), no silent elision.
4. NO work begun on verticals 2-4 or registry v0.2 (gate held).
5. Session log Compiler Tools section reproduces every <run> with observed output vs <expect>.
</acceptance_criteria>

<notes>
GO accompanies this TO (status pending at issue). Completion = census committed + /draw
delivered; the TO then holds ACCEPTED-PENDING-REVIEW — Andrew's structuring word (via MSTR~Z)
closes the pilot and unlocks TO-4b (Pod-2). Effort: medium.
</notes>
</task_order>
