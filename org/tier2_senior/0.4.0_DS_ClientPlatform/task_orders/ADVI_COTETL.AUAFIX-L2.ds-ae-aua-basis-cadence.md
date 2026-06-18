<to_id>ADVI_COTETL.AUAFIX-L2</to_id>
<project>ADVI_COTETL</project>
<title>Determine the CORRECT cot AUA-basis cadence -- RULE OUT snapshot-first-by-design BEFORE calling 06-09 a freeze (CTO cadence determination gates the fix)</title>
<assigned_to>0.4.0_DS_ClientPlatform (DS side) + 0.7.0_AE_CloudOps (BD-export source dig)</assigned_to>
<issued_by>2.0.0_SA_COO (AUAFIX PRD decomposition, 2026-06-18; CTO PRD ef04a08cc)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>staged</status>
<priority>HIGH (the REAL freshness question) -- but GATED on the CTO AUA-basis-cadence determination. CRITICAL PREMISE DISCIPLINE: do NOT assert "advance the basis" / "06-09 is a freeze" before by-design-periodic is RULED OUT. cot is SNAPSHOT-FIRST -- the periodic qt holdings snapshot is the AUA source-of-truth, intentionally NOT daily. The advance-vs-document call is CTO's. Largely independent of L1 (the basis question stands regardless of whether the chain fires).</priority>

<references>
  <ref type="prd">docs/architecture/ADVI_COTETL_AUAFIX_PRD.md (ef04a08cc) -- §2 Layer B + the CRITICAL NUANCE, §5 L2, §7 AC2</ref>
  <ref type="snapshot-first">memory/project_cot_snapshot_first_no_inject_no_schwab (Andrew 2026-06-12: cot SNAPSHOT-FIRST, qt holdings snapshot = AUA source of truth) + memory/reference_cot_holdings_intentionally_excluded_from_nightly_silver_periodic_qt_snapshot (holdings deliberately excluded from nightly silver -- an omission is not a defect until intentional-by-design is ruled out).</ref>
  <ref type="bd-history">memory/project_cot_bd_history_starts_2026_04_22 (cot BD history starts 04-22; daily pull has 100% of BD's cot data).</ref>
</references>

<scope>
Determine the CORRECT AUA-basis cadence for cot. The PRD's Layer B observed the BD unrealized/holdings SOURCE reads "Data date 06-09" even in the 06-18 export. BEFORE treating that as a freeze:
1. **RULE OUT by-design-periodic FIRST (the snapshot-first nuance):** is 06-09 the last LEGITIMATE periodic qt holdings snapshot (an EXPECTED by-design hold) or a GENUINE source freeze? cot is snapshot-first; the periodic qt snapshot is the AUA source-of-truth, intentionally not daily. Gather the evidence (BD export asOfDate / holdings-snapshot cadence; the qt snapshot schedule; what 06-09 represents) and present it -- do NOT pre-judge.
2. **CTO cadence determination (the gate):** CTO rules on the correct cadence. Two outcomes:
   - If 06-09 is the last legit snapshot (by-design hold) -> the "fix" is HONEST CADENCE-SURFACING: the served AUA must show its TRUE as-of and NOT imply daily-fresh when it is periodic. NOT forcing a daily basis.
   - If a genuine freeze -> dig the BD unrealized/holdings export (asOfDate / holdings-snapshot cadence) + advance it.
3. DS side: the silver/gold AUA-basis handling + (if cadence-surfacing) the served as-of honesty. AE side: the BD-export source dig (asOfDate / export cadence).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before asserting any cadence conclusion">
    <step>
      <run>Gather: the BD unrealized/holdings export asOfDate history + the qt holdings-snapshot cadence/schedule + what the cot silver/gold AUA-basis actually reads (comp-pipescript io on the AUA gold script for the basis input). Present to CTO.</run>
      <expect>Evidence sufficient for CTO to rule by-design-periodic vs genuine-freeze. NO premature "it's frozen, advance it" assertion.</expect>
      <if_mismatch>If the evidence is ambiguous, that itself goes to CTO -- do not default to "freeze". The snapshot-first prior is "expected hold until proven otherwise".</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="after CTO rules, before commit">
    <step>
      <run>Per CTO ruling: if cadence-surfacing -> comp-validate / served-as-of honesty check (AUA shows true periodic as-of). If advance-basis -> the BD-export fix + comp-pipescript deployed verify.</run>
      <expect>AC2 met: basis EITHER documented correctly-periodic-by-design (honest served-cadence) OR advanced. The snapshot-first nuance explicitly ruled on, not assumed.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **CTO determination GATES this leg** -- the AUA-basis cadence is a CTO call (snapshot-first). This TO produces the evidence; CTO rules; THEN the fix (surface-cadence vs advance-basis) proceeds. Do NOT let this TO assert a freeze or advance the basis before the ruling.
- **Independent of L1:** the basis question stands regardless of whether L1's chain fires. Do NOT declare AUA-fixed on L1 alone -- L1 unblocks the CHAIN; L2 resolves the BASIS.
- **DS (silver/gold basis) + AE (BD-export dig):** converge on what the basis reads vs what the source provides.
- **L2 needs the BD-export owner** for the source-cadence dig (AE leg).
</cross_domain_coordination>

<acceptance_criteria>
- AC2 (PRD): the AUA basis is RESOLVED -- either documented as correctly periodic-by-design (with honest served-cadence surfacing, no false daily-fresh implication) OR the BD source basis is advanced. The snapshot-first nuance is EXPLICITLY ruled on (CTO determination recorded), not assumed.
- NO premature freeze-assertion: the by-design-periodic possibility was ruled out with evidence before any "advance" action.
- Session log Compiler Tools section reproduces the `<run>` checks + the CTO cadence ruling.
</acceptance_criteria>

<data_reprocess_scope><conditional>If CTO rules "advance the basis" (genuine freeze), the BD-export advance + re-run is a DS gold-run (Rule 13). If CTO rules "by-design-periodic" -> cadence-surfacing is a served-metadata honesty change, no basis reprocessing. The reprocess scope is CONTINGENT on the CTO determination -- do not pre-commit to either.</conditional></data_reprocess_scope>
