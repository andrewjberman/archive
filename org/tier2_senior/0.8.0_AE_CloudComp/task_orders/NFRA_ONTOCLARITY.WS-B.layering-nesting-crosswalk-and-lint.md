<task_order>
<id>NFRA_ONTOCLARITY.WS-B.layering-nesting-crosswalk-and-lint</id>
<project>NFRA_ONTOCLARITY</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_ONTOCLARITY is complete; this TO was last touched 2026-07-19, predating the project close 2026-07-20. Closed as a record act, not a work verdict. Prior status: staged</status>
<priority>P2 -- definitional, startable after WS-A (inherits WS-A's two-layer root fix). The 5-scheme crosswalk is the highest-leverage clarity artifact (CTO). Context-owner ~C.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_ONTOCLARITY_PRD.md @b9b132933 (WS-B = S4)</ref>
  <ref type="charter">org/tier0/ledger/LD-0320.md</ref>
</references>

<objective>
Resolve the LAYERING + NESTING fog:
(a) Build ONE crosswalk table reconciling the 5 layer/plane numbering schemes (the highest-leverage clarity artifact -- a reader
    sees how the schemes map in one place instead of inferring across docs). Inherits WS-A's two-layer root distinction.
(b) ENFORCE the Relation-vs-Role exception as a LINT (a machine check), NOT prose -- an exception stated only in prose is re-drifted
    the next time someone reads past it (Rule-20 "cannot block = not a gate", applied to the definitional exception).
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>enumerate the 5 layer/plane numbering schemes across the ontology/CSE docs (grounded, cite each source) + the Relation-vs-Role exception's current statement</run>
      <expect>The 5 schemes + where each is defined; the Relation-vs-Role exception (currently prose). The crosswalk's denominator = these 5 schemes reconciled.</expect>
      <if_mismatch>N/A -- grounding.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>run the Relation-vs-Role LINT (seed a violation -> it flags) + grep the crosswalk table present</run>
      <expect>The crosswalk table reconciles the 5 schemes (one place); the LINT FIRES on a seeded Relation-vs-Role violation (EXERCISED, not prose).</expect>
      <if_mismatch>A prose-only exception is not enforced -- build the lint to actually flag.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. ONE crosswalk table reconciles the 5 layer/plane numbering schemes (grep-provable, one canonical place), inheriting WS-A's two-layer distinction.
2. The Relation-vs-Role exception is a LINT that FIRES on a seeded violation (EXERCISED), not prose.
3. LD-0320/0318 CVO SEMANTIC-VERIFIED GATE: CVO confirms -- semantically -- the layering/nesting ambiguity is GONE (not reworded). Ping CVO on land.
4. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- Inherits WS-A's two-layer root fix -- start after WS-A. Feeds WS-D (logged in system/sdk).
- Arch-decisions (which scheme is canonical) -> ping CTO via COO.
</cross_domain_coordination>

<notes>~C context-owner (ONTOCLARITY = the clarity audit of ~C's ontology). WS-B is the highest-leverage clarity artifact. SEMANTIC-axis acceptance (ambiguity GONE not reworded).</notes>
</task_order>
