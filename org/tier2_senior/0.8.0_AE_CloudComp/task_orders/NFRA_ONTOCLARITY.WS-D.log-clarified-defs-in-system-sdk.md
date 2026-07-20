<task_order>
<id>NFRA_ONTOCLARITY.WS-D.log-clarified-defs-in-system-sdk</id>
<project>NFRA_ONTOCLARITY</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<completed>2026-07-20T07:01Z -- CVO-PASS @0ee865ff9 (AC-3a seam-closer). ONTOCLARITY 4/4 COMPLETE (WS-A/B/C/D all CVO-verified). Landed @2799f8c49: 01_substrate.md role_priority cite (cite-not-copy), comp_ontolint self-test loads role_priority from bank (hardcode ELIMINATED -> zero ordering-copies outside RULE_BANK = AC-3a ideal), sdk no-op (vocabulary-bound). CVO exercised the seam by grep (sdk zero refs, RULE_BANK.yaml:56 sole home) + seed-guard fail-closed + system_parity 4/4 LIVE. Relayed to COO -> MSTR terminal ground-verify.</completed>
<progress>Grounding+design @48b239338 (COO GO 063241Z). BUILT @2799f8c49 (pushed CLOUD): (1) 01_substrate.md role_priority cite (cite-not-copy, WS-C spot-8); (2) comp_ontolint.py self-test LOADS role_priority from the bank (hardcode ELIMINATED -- folds CVO WS-C rec + AC-3a; zero ordering-copies outside RULE_BANK); (3) sdk no-op (already vocabulary-bound). Verify: self-test PASS, system_parity ontology 100% (4/4), ruff/py_compile/comp-manifest-check clean, seed-guard FAIL branch exercised. CVO verify requested 065155Z -> on PASS: WS-D DONE -> ONTOCLARITY 4/4.</progress>
<priority>P2 -- SEQUENCED LAST (logs the clarifications WS-A/B/C produce). RIDES SYSPARITY WS-4 (represent-the-ontology, COMPLETE) -- do NOT duplicate WS-4's representation; extend it with the clarified defs. Context-owner ~C (owns both seams).</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_ONTOCLARITY_PRD.md @b9b132933 (WS-D = S4 fourth bullet)</ref>
  <ref type="sibling">NFRA_SYSPARITY.WS-4.represent-the-ontology (COMPLETE -- ontology parity 40->100%; WS-D extends its representation with WS-A/B/C's clarified defs)</ref>
  <ref type="charter">org/tier0/ledger/LD-0320.md</ref>
</references>

<objective>
Ensure the CLARIFIED definitions/rules produced by WS-A (two-layer root + vocab authority + Observer truth + variance rename),
WS-B (layer crosswalk + Relation-vs-Role lint), and WS-C (process tie-breakers) are REPRESENTED in the system/sdk ontology
surface -- so the SDK's machine-readable ontology reflects the clarified truth, not the pre-clarity fog. This is the
definitions->representation seam CLOSED: WS-4 built the representation; WS-D keeps it coherent with the WS-A/B/C clarifications.
DO NOT re-do WS-4; extend/reconcile it.
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>diff the WS-4 representation (system/sdk ontology surface, as-shipped) against WS-A/B/C's clarified defs -- what changed that the representation must now reflect</run>
      <expect>The delta = only the clarifications WS-A/B/C introduced (two-layer split / one vocab authority / Observer single-truth / variance rename / crosswalk / tie-breakers). If a clarified def isn't yet represented, that's WS-D's work item. If WS-4 already covers it, WS-D is a no-op for that item -- record it, don't duplicate.</expect>
      <if_mismatch>N/A -- grounding the delta.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>re-run the SYSPARITY ontology parity metric (system_parity.py ontology domain) + drift-gate self-test over the ontology surface</run>
      <expect>Ontology parity stays 100% (4/4) with the clarified defs represented (not regressed); drift-gate self-test PASS. The clarified defs are now the represented truth.</expect>
      <if_mismatch>If parity regressed or a clarified def isn't represented, reconcile -- the seam is only closed when the SDK surface reflects the clarified ontology.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. Every clarified def from WS-A/B/C that belongs in the machine-readable ontology surface is represented there (extending WS-4, not duplicating) -- the definitions<->representation seam coherent in one head.
2. SYSPARITY ontology parity stays 100% (no regression) with the clarified defs represented; drift-gate self-test PASS over the ontology surface.
3. LD-0320/0318 CVO SEMANTIC-VERIFIED GATE: CVO confirms the represented ontology matches the clarified (post-WS-A/B/C) truth, not the pre-clarity fog. Ping CVO on land.
3a. **ROLE_PRIORITY PROPAGATION OBLIGATION (MSTR /govern @060101Z, LD-0090 discretion):** WS-C's role_priority ordering lands in NFRA_ONTOLOGY_RULE_BANK.yaml (the WS-A-declared SINGLE canonical source). WS-D MUST propagate it into infra/system + sdk so NO stale/partial copy of the role-resolution rule lingers (single-source / EVERY-ENFORCING-COPY discipline -- the exact drift-class this project audits). **CVO's WS-D semantic-verify CONFIRMS the sdk copy MATCHES the RULE_BANK ordering (total order, all 14, same sequence), not a stale/partial copy.** Same obligation applies to every WS-A/B/C clarified def, but the role_priority ordering is the named one.
4. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- RIDES SYSPARITY WS-4 (COMPLETE) -- ~C owns both, one head, no duplicate representation. Sequence LAST (after WS-A/B/C land their clarifications).
- The drift-gate ontology surface (~A's WS-3 widened it to RULE_BANK.yaml + variance_dimensions.yaml) is the coverage instrument -- if WS-A/B/C add a new canonical vocab source, that surface may need a WS-3-style add (coordinate with ~A + the COO cadence-sweep).
</cross_domain_coordination>

<notes>~C context-owner -- owns the WS-4 representation AND the WS-A/B/C clarifications, so the seam stays in one head (the whole reason ONTOCLARITY routed to ~C). WS-D is the seam-closer, not new representation. SEMANTIC-axis acceptance.</notes>
</task_order>
