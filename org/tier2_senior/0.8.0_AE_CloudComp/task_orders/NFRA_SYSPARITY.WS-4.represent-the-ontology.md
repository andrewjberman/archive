<task_order>
<id>NFRA_SYSPARITY.WS-4.represent-the-ontology</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P2 -- follows WS-1 (feeds from its scope + ONTOCLARITY's clarified defs) but the grounding + representation-design start NOW. Context-reallocation of ~C (NFRA_ONTOLOGY lane, variance thread just closed CVO-PASS) per Andrew-direct idle-reallocation-by-context.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-4 = S3 fourth bullet)</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md</ref>
</references>

<objective>
Close the ontology's ~40% parity gap (the "0 files" absence) by REPRESENTING the ratified archetype layer in /system + the SDK:
(a) Bring the ratified 14 Roles / 10 Relations / 6 Variance vocabulary (LD-0311/0315, canonized in org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml + variance_dimensions.yaml) into /system -- a core doc OR a declared cross-reference that cites the rule-bank AS the authored governance artifact.
(b) Fold the ratified vocab into the SDK adapter: retire the v0.1 stub, wire binding_mode: vocabulary-bound (the adapter references the ratified taxonomy, not a hand-copy).
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>read org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml + variance_dimensions.yaml (the ratified vocab + canonical location/vintage) + the SDK adapter's current v0.1 stub + binding_mode</run>
      <expect>The authoritative 14/10/6 vocab + its canonical home; the SDK adapter's current binding state. The representation must CITE this canonical location, not re-copy the vocab (a copy immediately drifts -- the exact anti-pattern SYSPARITY exists to close).</expect>
      <if_mismatch>N/A -- grounding step.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>grep the /system representation for the CITATION of the ratified rule-bank (not just the terms)</run>
      <expect>The representation REFERENCES the ratified taxonomy AS the authored artifact (a citation of RULE_BANK.yaml / the LD-0311/0315 ratification), NOT prose that merely contains "Twin/Canonical/Fork-Shadow" (those are incidental homonyms; CVO fire-2 confirmed 0/8 citational -- a word-grep mis-verifies both ways). The "0 files" finding closes with a CITATION, not word-appearance.</expect>
      <if_mismatch>Rework -- word-presence is the wrong-axis error one layer in (verifying REPRESENTATION by word-presence). The acceptance is citational.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. The archetype layer (14/10/6) appears in /system as a CITATIONAL reference to the ratified rule-bank (references the taxonomy AS SUCH, grep-of-the-citation not grep-of-the-word) -- closes the "0 files" ontology-absence finding for real.
2. The SDK adapter is vocabulary-bound (binding_mode: vocabulary-bound; the v0.1 stub retired), referencing the canonical vocab not a hand-copy.
3. The SDK-incorporation half does NOT duplicate NESTEDABSTRACT's forward loop (~A) -- coordinate the boundary; WS-6 SLAs the incorporation debt.
4. LD-0318 CVO-VERIFIED GATE (load-bearing here): CVO verifies the presence is CITATIONAL, not word-appearance (per its fire-2 sharpening), per PRD S7 (cron 02d90dce). WS-4 is NOT done until CVO confirms citational. Ping CVO on land.
5. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- FEEDS FROM NFRA_ONTOCLARITY (charters on WS-1 land): its clarified ontology definitions (esp. the two-layers-one-word fog: CSE C0-C3 algebra vs the 14/10/6 archetype layer) sharpen WHAT is represented. Coordinate WS-4's final representation with ONTOCLARITY's definitions -- the grounding/design starts now, the final land aligns with ONTOCLARITY.
- SDK-incorporation half overlaps NESTEDABSTRACT (~A) -- do NOT duplicate its forward incorporation loop; represent the ratified vocab, ~A's loop handles forward enhancements. COO brokers the ~A/~C boundary if needed.
- CTO arch-gate + RAVC + CVO-verify to land.
</cross_domain_coordination>

<notes>
Context-reallocation of ~C per Andrew-direct (2026-07-19): ~C owns NFRA_ONTOLOGY (its variance thread just closed CVO-4-bar-PASS @68d728b90) -> representing that ratified ontology in /system is its exact continuation. ~C already grounding (@211436Z). The load-bearing acceptance is CVO's citational-not-word-grep sharpening -- design the representation as a real citation of the governance artifact from the start.
</notes>
</task_order>
