<task_order>
<to_id>NFRA_COMPSIMILAR.PH2</to_id>
<title>comp-similar engine — BM25 over the summary corpus (copy-reuse dup_scan.py) + the superseded-twin supersede mode + comp-tool registration</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-17</date>
<status>complete</status>
<!-- 2026-07-19 ~D: GO'd under COO PROCEED-ALL-NFRA @180112Z (Andrew-direct via CTO). Engine comp_similar.py
     LANDED @b63b18853 (self-test 7/7, live-exercised); .tools/comp-similar wrapper + comp-tools.yaml +
     coverage-map staged. Two external gates pending, both submitted: CTO arch-gate @184502Z (PRD-4.3
     departure + gate-scoping + heat-plumbing call); COO registration SoD @184511Z (graph-call-manifest
     tools_index/entries/comp-which -- registration invariant blocks the wrapper commit without it). NOT
     complete until both clear. Dogfood: offline C4 mutant PASS; monolith live pair PH3-gated
     (opal-data-assets UNKNOWN-thin). -->
<!-- 2026-07-19 UPDATE: BOTH gates CLEARED. CTO arch-gate GO @185343Z (departure approved, read/scan
     scoping confirmed, heat-cadence deferred, dogfood correct). COO landed graph-call-manifest routing +
     wrapper atomically @e58a1bcd6 (rank-1 2.00, no theft, routing-test PASS, baseline regression-free);
     AE-SoD half (comp-tools.yaml + coverage-map) committed @2956c2751; comp-manifest-check
     registration-invariant PASS. ENGINE+REGISTRATION LANDED. Sole remaining = CVO held supersede-path
     exercised verify (pinged @192357Z) -> that CLOSES PH2 (COO). Flip to complete on CVO PASS.
     Deferred/separate (CTO-ruled, not PH2 blockers): heat-source cadence follow-on (data-production, not a
     monitor) + PH3 authored summaries. -->

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

<completion>
COMPLETE 2026-07-19 (0.8.0_AE_CloudComp~D, under Andrew-direct PROCEED-ALL-NFRA via CTO/COO). All
acceptance criteria met; CVO closing verify PASS (2/3 primary wave land CLOSED).

DELIVERED (all on origin):
- ENGINE comp_similar.py @b63b18853 (538 lines): BM25 SUMMARY similarity (reuses summary_corpus
  build_corpus/SimilarityIndex which reuse dup_scan.BM25) + --supersede (summary-twin x heat-DIVERGENCE
  x designed-parallel/held suppressors, confidence-graded HIGH both-cold/MEDIUM one-cold) + cluster +
  pairwise. ZERO summary_corpus.py edits (~C _position_key seam held clean throughout).
- WRAPPER .tools/comp-similar + graph-call-manifest tools_index + entries cloud.similar.resource +
  comp-which rule = COO-SoD atomic land @e58a1bcd6 (manifest-check requires a registered tool be
  git-tracked). AE-SoD half (comp-tools.yaml + coverage-map meta_tools home) @2956c2751.
- comp-manifest-check registration-invariant PASS (79 tracked comp-* all accounted, comp-similar in).

GATES CLEARED:
- CTO arch-gate GO @185343Z (exercised): PRD-4.3 departure APPROVED (summary-first candidate-gen, since
  the headline monolith cutover is name-DIFFERENT; DoR updated); read/scan gate-scoping CONFIRMED (no
  store-writer/apply/TF/IAM this leg; no plan-gate/22a); heat-decoupling APPROVED.
- COO registration RAVC-confirmed clean @2956c2751.
- CVO supersede-path PASS @193302Z: (1) self-test 7/7; (2) LIVE displacement on the real corpus (CVO's
  own heat-json pair, superseding HOT displaces superseded COLD); (3) C1 LIVE discrimination (same pair
  both-HOT -> 0 candidates -- keys on heat-divergence not similarity); (4) registration rank-1 2.00, NO
  theft, gibberish abstains.

ACCEPTANCE CRITERIA: 1 engine+--supersede DONE; 2 dogfood -- offline C4 mutant PASS + live --heat-json
displacement PASS (monolith pair PH3-gated: opal-data-assets UNKNOWN-thin, C3 correctly excludes --
CTO-ruled correct, not a defect); 3 registered + routing PASS; 4 the 5 PRD controls documented + self-
test-discriminating (7/7); 5 session logs (laneD_ph2_comp_similar_engine.md + this close).

DEFERRED (CTO-ruled non-blockers, NOT this TO):
- Heat-source CADENCE follow-on (real live-heat end-to-end): a DATA-PRODUCTION step (not an alert/monitor
  -- respects the consolidation alert-suspension). comp-debris live >2min/partial-for-S3, comp-heat
  repo-scoped -- v1 decouples via --heat-json. Separate follow-on.
- PH3 authored summaries (~549 targets) -- enriches the corpus so PH3-gated pairs (e.g. the monolith
  dogfood) surface. Separate TO (CTO §9-4).

RESIDUAL SURFACED (not this TO, surfaced to COO): CVO's light aside -- comp-which "describe one specific
AWS resource" routes rank-1 to comp-tooltip not comp-describe (pre-existing comp-which routing nuance,
comp-similar did NOT cause it). AE-eye-worth, out of PH2 scope.
</completion>
</task_order>
