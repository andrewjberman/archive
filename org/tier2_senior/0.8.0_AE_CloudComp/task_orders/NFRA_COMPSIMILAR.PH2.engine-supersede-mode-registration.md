<task_order>
<to_id>NFRA_COMPSIMILAR.PH2</to_id>
<title>comp-similar engine — BM25 over the summary corpus (copy-reuse dup_scan.py) + the superseded-twin supersede mode + comp-tool registration</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-17</date>
<status>pending</status>
<!-- 2026-07-19 ~D: GO'd under COO PROCEED-ALL-NFRA @180112Z (Andrew-direct via CTO). Engine comp_similar.py
     LANDED @b63b18853 (self-test 7/7, live-exercised); .tools/comp-similar wrapper + comp-tools.yaml +
     coverage-map staged. Two external gates pending, both submitted: CTO arch-gate @184502Z (PRD-4.3
     departure + gate-scoping + heat-plumbing call); COO registration SoD @184511Z (graph-call-manifest
     tools_index/entries/comp-which -- registration invariant blocks the wrapper commit without it). NOT
     complete until both clear. Dogfood: offline C4 mutant PASS; monolith live pair PH3-gated
     (opal-data-assets UNKNOWN-thin). -->

<priority>P2 (Andrew batch 2026-07-17). GATE: NFRA_COMPSIMILAR.PH1 landed (resource_summaries corpus live) + CTO arch-gate on the PRD's engine/registration decisions.</priority>

<authority>
Andrew-direct (recorded @dc4207c7c/1d81e760b/3d326af47): comp-similar scores BM25 over a resource's SUMMARY
(what it DOES) where comp-dups scores over name/body (what it IS). Headline = the superseded-twin fast-scan:
decommission candidate = similar-name cluster + VERY HIGH summary similarity + LARGE hot-vs-cold heat
divergence (old version quietly replaced, left running). Engine = the existing dup_scan.py BM25 class (Andrew:
copy-reuse, not reimplement).
</authority>

<gate>
DO NOT GO until: PH1 landed (resource_summaries table + Kuzu projection queryable) AND CTO's arch-gate rulings
on the engine-shape decisions (own-tool vs a comp-dups mode; the heat source for the supersede divergence;
the registration shape). COO fires GO when both clear.
</gate>

<scope>
  1. The engine: comp-similar scores BM25 (dup_scan.py's proven BM25 class, copy-reuse) over the
     resource_summaries corpus — the functional-overlap axis. Query = a resource; result = summary-similar peers.
  2. SUPERSEDE MODE (the headline): comp-similar --supersede = the joint-signal scan — intersect (name-similar
     cluster) × (very-high summary similarity) × (large hot/cold heat divergence via comp-heat). Output = ranked
     superseded-twin candidates (old-left-running-beside-hot-replacement), the decommission-candidate feed.
  3. REGISTRATION (COMPCLOSE invariant): tools_index + a curated comp-which rule + a routing-test +
     comp-manifest-check — so comp-similar is discoverable + the manifest invariant passes.
  Ship WITH the 5 pre-registered failure-modes-it-must-not-have + the dogfood (the monolith-cutover superseded
  pairs are the known-answer test set). This is a READ/scan tool — no alert leg.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-manifest-check (baseline) + read dup_scan.py's BM25 class</run>
      <expect>BM25 class located for copy-reuse (not reimplement, per Andrew); manifest baseline green so the new executable's registration is the only delta.</expect>
      <if_mismatch>STOP. If BM25 isn't cleanly reusable, surface to CTO before reimplementing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>DOGFOOD exercise: run comp-similar --supersede against the monolith-cutover known superseded pairs (old bucket/lambda left beside its hot replacement)</run>
      <expect>The known superseded twins rank at/near the top (high summary-sim + high heat-divergence). A --supersede that MISSES the known-answer pairs is a broken instrument — this is the discriminating test, not a vacuous pass.</expect>
      <if_mismatch>STOP. Tune/fix before shipping; a decommission scanner that misses known superseded twins would greenlight leaving them running.</if_mismatch>
    </step>
    <step>
      <run>comp-manifest-check + the routing-test after registering comp-similar</run>
      <expect>comp-similar REGISTERED (tools_index + comp-tools.yaml + comp-which rule); routing-test resolves a "what overlaps / is superseded / decommission candidate" question to comp-similar.</expect>
      <if_mismatch>STOP. Register + add the comp-which rule before commit (COMPCLOSE invariant).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Composes with OPAL_TAXONOMY P3-CENSUS: comp-similar --supersede's heat-divergence output IS the census's
"unused-by-heat" column (~C/~B). Feeds OPAL_LCLRPO (the disposal pipeline) — the candidate feed is LCLRPO's
input, NOT an auto-delete (deletion stays per-batch Andrew-word per LCLRPO/LD-0300). Reads comp-heat for the
divergence signal — coordinate the heat source with CTO's PH1 ruling.
</cross_domain_coordination>

<acceptance_criteria>
1. comp-similar engine scores BM25 over resource_summaries; --supersede emits ranked superseded-twin candidates.
2. DOGFOOD: the known monolith-cutover superseded pairs rank top (exercised, discriminating — not a vacuous pass).
3. Registered (comp-manifest-check green + comp-which routes + routing-test passes).
4. The 5 pre-registered failure-modes documented as not-present with evidence.
5. Session log reproduces each mandate run + observed vs expect.
PH3 (the authored ~549-target summary pass that populates the corpus for real coverage) is the follow-on TO.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPSIMILAR_PRD.md</ref>
  <ref type="depends">NFRA_COMPSIMILAR.PH1 (corpus must land first)</ref>
</references>
</task_order>
