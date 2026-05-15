<task_order>
  <metadata>
    <id>ADVI_INFFIN.023</id>
    <slug>rd-snapshot-median-percentile-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>RD 0.4.2 bench-clear post H3 FE patch close. Wave 1 RD batch.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Snapshot view percentile completeness; Andrew lean FE-first investigation</priority>
    <sla>~30-60min wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.4 (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ: "missing median values in the snapshot views from segment analytics, need to look into that, see if its a frontend or backend issue, id guess frontend as how would we have all the other items and somehow forget to do medians backend."</ref>
    <ref type="surface">Inflection portal → AdvisorIntelligence → Segment Analytics → Distribution → Snapshot → GEO cohort → AUA mode</ref>
  </references>

  <context>
    Segment Analytics Snapshot shows P10/P25/P75/P90 populated but Median = N/A. Andrew lean: FE-first investigation since "how would we have all the other items and somehow forget to do medians backend."

    FE-first then backend fallback if FE reads correctly but data shape lacks median.
  </context>

  <objective>
    Phase 1 FE-first: check if median field is read in snapshot percentile-band component but not rendered. Phase 2 fallback: if backend emit gap confirmed, cascade DE/DS TO authored.
  </objective>

  <scope>
    <files>
      <file action="readonly_reference">portal FE Snapshot percentile-band component</file>
      <file action="modify_conditional">FE component IF field exists but not rendered</file>
      <file action="readonly_reference">platinum artifact emit shape for distribution snapshot</file>
    </files>
  </scope>

  <phase id="1" when="FE-first investigation">
    <step>
      <run>grep portal FE for medianAccountSize / p50 / median field references in Snapshot component</run>
      <expect>Either: field read exists but not rendered (Path 1 FE fix) OR field not in current schema (Path 2 backend cascade).</expect>
    </step>
    <step>
      <run>S3 inspect platinum artifact: aws s3 cp s3://opal-data-inf/platinum/firm/{distribution snapshot artifact} - | head; check for median/p50 field</run>
      <expect>Backend emit shape verified.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>PATH 1 (FE field exists not rendered): wire median field into percentile-band display alongside P10/P25/P75/P90</run>
      <expect>Median renders correctly for GEO + ADV cohorts.</expect>
    </step>
    <step>
      <run>PATH 2 (backend gap): author cascade TO INFFIN.023b for DE/DS backend emit augment; close current TO with cascade routing note</run>
      <expect>Cascade routing clean; backend emit gap routed.</expect>
    </step>
    <step>
      <run>Path 1 verify: median value reconciles to mathematical median of account-size distribution (should match P50 if exists OR compute correctly)</run>
      <expect>Median value empirically valid; AUA mode + NNA mode both show median.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + RAVC">
    <step>
      <run>safe-commit.sh per Rule 14a + Author identity RD 0.4.2 (Path 1) OR cascade routing only (Path 2)</run>
      <expect>Commit clean.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4 + state which path executed</run>
      <expect>Evidence-bearing close + path attestation.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Phase 1 FE investigation findings documented (field exists OR not)
    AC2 (Path 1): Median value renders alongside P10/P25/P75/P90 for both GEO + ADV cohorts
    AC2 (Path 2): Cascade TO INFFIN.023b authored for backend emit
    AC3 (Path 1): Median value reconciles mathematically
    AC4 (Path 1): AUA mode + NNA mode both show median
    AC5: 49F regression smoke PASS
    AC6: No emoji per CLAUDE.md
    AC7: RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 grep + S3 inspect; Phase 2/3 safe-commit.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: RD H3 FE patch close.
    PARALLEL-OK: All other INFFIN.019-028 sibs.
    POTENTIAL CASCADE: Path 2 spawns INFFIN.023b for DE/DS lane.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE-only Path 1; Path 2 spawns backend cascade.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Phase 1 FE-first investigation findings
    2. Path 1 FE fix OR Path 2 cascade routing
    3. RAVC2 with path attestation
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO + CC CTO + DT 0.4 on AC1-7 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.

    **Andrew lean FE-first:** banked sister to `feedback_cdn_cache_staleness_masquerades_as_fe_bug.md` discipline; verify FE before backend.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
