# OPAL_ANALYST.TO4b — Pod-2 Analytics artifact census + /draw (vertical 2)

<task_order>
<id>OPAL_ANALYST.TO4b</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-10</date>
<status>pending</status>
<priority>P1</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §8.1 grammar @7753e1caf (+ s.8 grammar-ratified note per @95b3e2852)</ref>
  <ref type="pilot">OPAL_ANALYST.TO4a complete — ARTIFACT_CENSUS_MP.yaml @0c1dae3da is the RATIFIED template</ref>
  <ref type="ruling">Andrew structuring approval + verticals-2-4 GO, record @95b3e2852; plan @6c1161075</ref>
</references>

<scope>
Vertical 2 per Andrew's ruled order. Same two deliverables as the pilot, same grammar, same
bar: (1) `refs/census/ARTIFACT_CENSUS_POD2.yaml` in the 0.0.3_BG agent home — every
portal-served Pod-2 Analytics artifact at page → location → panel → artifact → field grain,
five binding rules, RATIFIED pilot choices carried (residue plane in grammar, scope-family
dedup, per-artifact vintage_field, one-panel grain); (2) /draw of the COMPLETE findings to
MSTR~Z for Andrew (informational delivery per the persistence pattern — the structuring gate
is DISCHARGED for all remaining verticals; no hold on his reply), cc COO~Z.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Re-read ARTIFACT_CENSUS_MP.yaml (the ratified template) + .tools/comp-estate for the Pod-2 analytics thread(s) (--list to resolve names; read provenance headers, --refresh if stale >14d)</run>
      <expect>Pod-2 serving thread(s) enumerated: served keys + frontend consumers; denominator statable from comp-estate + PORTAL_RETRIEVAL before any row is written.</expect>
      <if_mismatch>STOP. No census without its frame; surface to COO~Z.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>YAML parse check + five-rule self-score (one line each, evidence named), as in the pilot</run>
      <expect>Parse clean; 5/5 PASS.</expect>
      <if_mismatch>STOP. Do not commit below the pilot's bar.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>/draw complete findings -> MSTR~Z (for Andrew) cc COO~Z; report to COO~Z with commit + denominator + delivery pointer</run>
      <expect>Complete coverage, elisions printed if any (no-silent-caps).</expect>
      <if_mismatch>Surface to COO~Z before delivery.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same as TO-4a: new file under `refs/census/` (audited lane-override commit, RELAUNCH.md
pattern); read-only over the estate; live seat unaffected until next refs re-read. No other
open TO touches these paths.
</cross_domain_coordination>

<acceptance_criteria>
1. ARTIFACT_CENSUS_POD2.yaml passes all five binding rules incl. the ratified pilot choices.
2. Denominator printed in header, consistent with Phase-1 enumeration.
3. /draw of complete findings delivered (MSTR~Z for Andrew, cc COO~Z).
4. No registry v0.2 rows, no inferential work, no pre-scoping of News.
5. Session log Compiler Tools section reproduces every <run> vs <expect>.
</acceptance_criteria>

<notes>
Part of the sequential batch GO b→c→d (Andrew's ruled order @95b3e2852): complete this, then
proceed DIRECTLY to TO-4c without a new GO (batch-GO protocol); COO validates each on report.
</notes>
</task_order>
