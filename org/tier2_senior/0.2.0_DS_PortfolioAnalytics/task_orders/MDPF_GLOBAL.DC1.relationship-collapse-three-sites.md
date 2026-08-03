<task_order>
<to_id>MDPF_GLOBAL.DC1.relationship-collapse-three-sites</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-03</date>
<status>staged</status>
<priority>P1 (CTO ruled 230622Z: BUILD NOW, gate granted for the collapse scope at all three sites. >> THE SERVE-CHANGE HOLDS FOR ANDREW: DELTA != 0 on a served client-facing value -- the corrected number must NOT reach the served surface until his disclosure call. <<)</priority>

<title>DC1: collapse to (AccountID, AssetID) before aggregating -- the three naive summers over BD relationship grain; BUILT + EXERCISED + HELD, never served without Andrew's word</title>

<context>
0.4.0_DS's consumer enumeration @387fa87c90: BD relationship-grain rows double-count under naive
sums (account z0927448821, two LP assets under two relationships, equal values doubled). Served
impact: cottonwood Total-AUA +$205,070.77 (~0.045% of firm total) on every value-carrying
dual-relationship day (07-22, 07-28..current 07-31). Three confirmed sites, all yours (the
slice/dim/pair family you deployed tonight):
1. build_cottonwood_mdpf_slice holdings_total_by_date (whole-column SUM -> the SERVED cottonwood
   Total-AUA series)
2. build_dim_model_portfolio account_values (per-account groupby does NOT save it -- the
   dual-relationship rows sit INSIDE one account group)
3. build_cottonwood_mdpf_pair firm_total (inherits)
Possible fourth: the emitter's cot_total :446 whole-sum -- YOUR check in flight; if it shares
the class its collapse rides AE's C1 implementation, NOT this TO.

CTO GATE GRANTED (230622Z) for the collapse scope at these three sites only.

>> THE SERVE-HOLD, VERBATIM CTO: "This is a DELTA != 0 change to a SERVED client-facing value,
so the never-move-served-output rule binds and the 'verified DELTA=0 needs no hold' carve-out
does NOT apply. Land the code + the measured before/after; do NOT let the corrected value reach
the served surface until Andrew has made the disclosure call." MECHANICALLY: commit + exercise
in scratch with the DO-NOT-DEPLOY marker (your own T1.C row-4 pattern); production keeps running
the current code -- tonight's cycle serving the same number as yesterday IS the status quo Andrew
adjudicates. Deploy leg fires on Andrew's word relayed through CTO/COO, not before. <<
</context>

<scope>
1. Implement the collapse at all three sites (collapse to (AccountID, AssetID) before any
   aggregation; the RELATIONSHIP dimension remains in the data -- this changes SUMS, not grain).
   WITH THE EQUALITY ASSERT (your own 230639Z spec rider, now binding here too): assert
   dollar-equality across the dual rows per (AccountID, AssetID) -- if dual-relationship rows
   ever carry DIFFERENT values, that is a DATA question: refuse loudly, never silently
   keep-first (your slice's own :240-253 precedent). Note: your 230639Z "fifth summer"
   (holdings_total_by_date) IS site 1 of this TO -- independently re-derived, convergent,
   covered; total distinct sites = these three + the emitter (AE's C1 window).
2. EXERCISE in scratch: (a) the measured before/after on a value-carrying dual day (07-31
   expected delta: -$205,070.77 exactly -- tie it to 0.4.0's measured figure); (b) a clean-day
   control (no dual rows -> before==after byte-identical); (c) the 07-22 anchor date reproducing
   the collapsed truth $457,984,488.00.
3. COMMIT with DO-NOT-DEPLOY marker; evidence package to CTO + COO (Andrew's disclosure call
   rides it). NO deploy, NO production writes, NO serve change under this TO.
4. Pre-register the deploy leg's cycle interpretation now (for when Andrew clears): first
   post-deploy cycle's cottonwood series steps DOWN by the dual-day delta -- expected, correct,
   not a regression.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read all three sites at pinned commit; comp-blast on the three fns (hand-derive where assets-tree-blind, labeled)</run>
      <expect>Three sites confirmed at vintage; consumers enumerated; no fourth site in THIS family (the emitter is separately owned).</expect>
      <if_mismatch>STOP. A moved site or an unexpected consumer re-grounds first.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="exercise, before commit">
    <step>
      <run>scratch exercises (a)/(b)/(c) per scope 2</run>
      <expect>Delta ties to the measured figure exactly; clean-day byte-identical; 07-22 reproduces the collapsed truth.</expect>
      <if_mismatch>STOP. A delta that does not tie to 0.4.0's measurement means one of the two derivations is wrong -- route to CTO before committing either.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit (deploy HELD)">
    <step>
      <run>evidence package to CTO + COO (before/after + controls + the DO-NOT-DEPLOY state); deploy leg ONLY on Andrew's cleared word</run>
      <expect>Package lands; TO stays open at HELD-FOR-ANDREW until the word; then deploy + MATCH + ledger closes it.</expect>
      <if_mismatch>Serving the corrected value without the word is a NEVER-rule violation -- there is no override path here.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same file family as your T1.C deploy -- the collapse composes with the (b+) rider (both change
the slice; commit atomically or sequence explicitly). The emitter site is EXCLUDED (rides C1/AE).
0.4.0's anchor-correction TO annotates the 07-22 tie records in parallel -- your exercise (c)
supplies the collapsed-truth figure their annotations cite; cross-reference commits.
</cross_domain_coordination>

<acceptance_criteria>
1. Three sites collapsed, one logical change each, CTO grant 230622Z cited.
2. Exercises (a)/(b)/(c) verbatim: delta ties EXACTLY to the measured +$205,070.77; clean-day
   byte-identical; 07-22 collapsed truth reproduced.
3. DO-NOT-DEPLOY held until Andrew's word; the serve-hold is an acceptance item, not a courtesy.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260803T230622Z (fix-now + serve-hold + gate grant)</ref>
  <ref type="finding">0.4.0_DS @387fa87c90 (three summers + measured impact + the blind parity tie)</ref>
  <ref type="never">CLAUDE.md NEVER: never move served output without never-widen sign-off (DELTA!=0 -- the carve-out does not apply)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
