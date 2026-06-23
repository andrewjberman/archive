<to_id>ADVI_COTETL.AUAFIX-L3</to_id>
<project>ADVI_COTETL</project>
<title>firm_id fork-shadow cleanup: 3 cot platinum served JSONs mislabel firm_id="49financial" -> correct to cottonwood + sweep for siblings</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (AUAFIX PRD decomposition, 2026-06-18; CTO PRD ef04a08cc)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>staged</status>
<priority>MEDIUM -- independent cleanup (not gated on L1/L2). Bundles into DS's tomorrow-AM re-engagement (alongside L1-silver-side + the NNA value-gate decompose). A served-correctness bug (wrong firm_id on cottonwood's own served JSONs).</priority>

<references>
  <ref type="prd">docs/architecture/ADVI_COTETL_AUAFIX_PRD.md (ef04a08cc) -- §5 L3, §7 AC3</ref>
  <ref type="fork-shadow">memory/feedback_bd_cot_fork_validate_config_stale_shadow (the bd->cot fork silently copies bd content/labels dead/unwired -- same fork-shadow class).</ref>
  <ref type="canonical">memory/feedback_cottonwood_cot_canonical_abbreviation (cot/cottonwood canonical; firm_id=cottonwood is correct for cot served artifacts).</ref>
</references>

<scope>
3 cot platinum served JSONs (dashboard / mix / timeseries) mislabel `firm_id="49financial"` -- only header_metrics correctly says cottonwood. This is a fork-shadow from the bd->cot fork (the bd FIRM_ID literal carried into cot's served output). Fix:
1. Correct the 3 JSONs' firm_id to cottonwood AT THE GENERATION SOURCE (the cot gold/platinum generation script that hardcodes/passes firm_id) -- not a post-hoc patch of the served file (that re-drifts on next run).
2. SWEEP the cot gold/platinum generation for SIBLING fork-shadow mislabels (other 49financial/bd literals that should be cottonwood) -- the fork-shadow class is rarely a single instance.
3. Verify on the SERVED artifacts after the next gold-run (or a manual run if L1 needs one): all cot served JSONs carry firm_id=cottonwood, 0 residual.
DS commit cycle per Rule 13 (ds-commit-gate; comp-pipescript io on the touched gold script for column-gaps + consumers).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before editing the gold/platinum script">
    <step>
      <run>comp-pipescript io [the cot gold/platinum script that sets firm_id] -- COLUMN GAPS + portal consumers of the 3 JSONs (confirm who reads firm_id, so the correction doesn't break a consumer keying on '49financial')</run>
      <expect>The firm_id source identified; consumers mapped. A consumer keying on '49financial' for cot would itself be a fork-shadow bug to surface.</expect>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>ds-commit-gate (py_compile + ds-precommit + ruff FA) + grep the cot gold/platinum generation for residual '49financial'/bd literals (the sibling sweep)</run>
      <expect>0 residual 49financial/bd firm-literals in cot generation (except any legitimately-bd-shared utility). Clean gate.</expect>
    </step>
  </phase>
  <phase id="3" when="after the gold-run (served verify)">
    <step>
      <run>head-object / read the 3 served JSONs (dashboard/mix/timeseries) + header_metrics -> firm_id field</run>
      <expect>All cot served JSONs carry firm_id=cottonwood; 0 residual 49financial.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **Independent of L1/L2** -- pure served-correctness cleanup. But the served-verify (phase 3) wants a gold-run; if L1 confirms the chain fires on the 06-19 nightly, the firm_id fix lands on that run; if L1 needs a manual run, coordinate so L3's fix is in the manual run.
- **DS lane (Rule 13):** DS owns the cot gold/platinum generation script edit + commit + the served verify.
- **Bundles into DS tomorrow-AM** alongside L1-silver-side + the NNA value-gate decompose item.
</cross_domain_coordination>

<acceptance_criteria>
- AC3 (PRD): all cot served JSONs (dashboard, mix, timeseries, header_metrics) carry firm_id=cottonwood; 0 fork-shadow residual. Verified on the SERVED artifacts.
- The fix is at the GENERATION SOURCE (not a post-hoc served-file patch) so it doesn't re-drift on the next run.
- The sibling-sweep ran (0 residual 49financial/bd firm-literals in cot generation).
- Session log Compiler Tools section reproduces every `<run>` with pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>A firm_id label correction in the cot gold/platinum generation -- re-emits on the next scheduled gold-run (or the L1 manual run). No basis/data reprocessing; corrects a served-metadata label.</no_reprocess_needed></data_reprocess_scope>

---
**RECONCILED-COMPLETE 2026-06-23** (COO /drive 132528Z): firm-id fork-shadow cleaned; part of the $24M AUAFIX, CVO-certified 06-22. DONE.
