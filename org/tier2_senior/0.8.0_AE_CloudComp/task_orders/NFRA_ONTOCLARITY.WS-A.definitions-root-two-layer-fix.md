<task_order>
<id>NFRA_ONTOCLARITY.WS-A.definitions-root-two-layer-fix</id>
<project>NFRA_ONTOCLARITY</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>P1 -- DO FIRST (contains the ROOT fix everything downstream inherits). Sequenced AFTER ~C's SYSPARITY WS-4 (same ontology lane; WS-A's clarified defs then feed WS-4's representation -- one head, no seam). GO on WS-4 land. Context-owner reallocation of ~C per Andrew-direct.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_ONTOCLARITY_PRD.md @b9b132933 (WS-A = S4 first bullet)</ref>
  <ref type="brief">docs/briefs/NFRA_ONTOCLARITY_BRIEF_20260719.md (MSTR, 10 fog-spots)</ref>
  <ref type="charter">org/tier0/ledger/LD-0320.md (Andrew-direct via MSTR)</ref>
</references>

<objective>
Resolve the ROOT ontology fog + its definitional tail (everything downstream inherits WS-A):
(a) DISAMBIGUATE THE TWO "ontology" LAYERS IN ONE AUTHORITATIVE PLACE -- "ontology" is one word for two distinct layers: the
    CSE C0-C3 ALGEBRA (the compiled-system ladder) vs the 14 Roles / 10 Relations / 6 Variance ARCHETYPE LAYER above it. State
    the two-layer relationship ONCE, unambiguously, at a canonical source; everything else references it. THIS IS THE ROOT FIX.
(b) SINGLE canonical SOURCE-OF-RECORD + version scheme for the ratified vocab -- retire the split / `v0.1`-pin fog (one authority
    that every consumer cites, not multiple copies that drift).
(c) RESOLVE the Observer DoR-vs-rulebank CONTRADICTION -- a record can hold only ONE truth (reconcile which is authoritative).
(d) PURGE the retired Fork-Shadow=debt copies to closure (the LD-0315 tail -- zero LIVE Fork-Shadow=debt assertion remains).
(e) RENAME/ANNOTATE variance_dimensions so the axis-NAMES aren't mis-read as the verdict VOCABULARY.
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-which "where is the ontology two-layer distinction defined" + grep the ratified vocab sources (RULE_BANK.yaml / canon-patterns / DoR / variance_dimensions) + the Fork-Shadow=debt occurrences</run>
      <expect>Enumerate the current STATE of each fog: where (if anywhere) the two-layer split is stated, the multiple vocab copies, the Observer DoR-vs-rulebank two-truths, the live Fork-Shadow=debt copies, the variance_dimensions mis-read. This is the denominator of what WS-A resolves.</expect>
      <if_mismatch>N/A -- grounding the fog inventory.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>re-grep each fog: two-layer statement present-and-single / one canonical vocab source / Observer single-truth / zero live Fork-Shadow=debt / variance name</run>
      <expect>Each fog measurably RESOLVED at source (not reworded): the two-layer split stated ONCE; one vocab authority; one Observer truth; zero live Fork-Shadow=debt; variance name no longer mis-reads.</expect>
      <if_mismatch>The fog persists -- rework. A reworded ambiguity is NOT a resolved one (the load-bearing acceptance).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. The two-layer relationship (CSE C0-C3 algebra vs 14/10/6 archetype layer) is stated ONCE, unambiguously, at a canonical source; downstream references it (the ROOT fix).
2. ONE canonical vocab source-of-record + version scheme; the split/v0.1-pin fog retired; every consumer cites the one authority.
3. Zero LIVE Observer DoR-vs-rulebank contradiction (one authoritative truth).
4. Zero LIVE Fork-Shadow=debt assertion (LD-0315 tail purged).
5. variance_dimensions renamed/annotated so axis-names don't read as the verdict vocabulary.
6. LD-0320/LD-0318 CVO SEMANTIC-VERIFIED GATE (load-bearing): CVO confirms -- SEMANTICALLY, NOT a word-grep -- each fog class is GONE (the ambiguity resolved, not reworded). WS-A is NOT done until CVO semantic-verifies. Ping CVO on land.
7. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- WS-A/B/C are definitional -- INDEPENDENT of the SYSPARITY scope contract; start after ~C's WS-4 (same lane, one head).
- WS-A's clarified DEFINITIONS FEED SYSPARITY WS-4 (represent the ontology) + ONTOCLARITY WS-D (log them) -- keep the definitions<->representation seam coherent (~C owns both). WS-D RIDES WS-4; do not duplicate.
- ANY arch-decision (which record is the Observer authority, the canonical vocab source, the variance rename) -> ping CTO (he arch-gates the ontology rulings) via COO.
</cross_domain_coordination>

<notes>
Context-owner reallocation of ~C per Andrew-direct (2026-07-19): ~C owns NFRA_ONTOLOGY; ONTOCLARITY is the CLARITY audit OF that
ontology, and its clarified defs feed ~C's own SYSPARITY WS-4 representation -- so ~C owning both keeps the definitions<->representation
seam in one head (MSTR + COO concurred the fit). WS-A is the root; B/C follow (I file them), D rides WS-4. The SEMANTIC-axis acceptance
(ambiguity GONE not reworded) is the whole point -- a fog you can still word-grep both ways is not resolved.
</notes>
</task_order>
