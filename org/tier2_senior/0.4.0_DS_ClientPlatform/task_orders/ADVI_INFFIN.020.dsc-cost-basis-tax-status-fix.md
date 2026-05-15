<task_order>
  <metadata>
    <id>ADVI_INFFIN.020</id>
    <slug>dsc-cost-basis-tax-status-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>Cascade unblock post ADVI_INFFIN.019 RAVC2. Scope of this TO determined by investigation brief recommendation (gold-script fix? FE tooltip? schema rename?).</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Andrew empirical reconciliation gap fix</priority>
    <sla>~1-3h wall (scope-dependent on investigation finding)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.1</ref>
    <ref type="parent_investigation">ADVI_INFFIN.019 RAVC2 + docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md</ref>
  </references>

  <context>
    Fix scope determined by INFFIN.019 investigation outcome. Possible scopes:
    - Gold script lot-level → account-level dedupe fix
    - Tax-status filter scope alignment
    - Date-window scope correction
    - Unit-scale conversion fix
    - FE tooltip wording clarification (semantic not data fix)
    - Schema rename for cross-script consistency

    Per CLAUDE.md Rule 13+14+15: DS owns the full commit→QA-deploy cycle; ds-commit-gate.sh + `from __future__ import annotations` first import for any gold/silver/bronze script edit.
  </context>

  <objective>
    Implement the fix recommended by INFFIN.019 investigation brief. Reconciliation verified empirically post-fix: CBBY total reconciles to AUA-by-Tax-Status OR documented divergence with tooltip clarification.
  </objective>

  <scope>
    <files>
      <file action="determined_by_investigation">Files scoped post-INFFIN.019 RAVC2</file>
    </files>
  </scope>

  <phase id="1" when="implementation">
    <step>
      <run>Apply fix per investigation brief recommendation</run>
      <expect>Fix implemented; ds-commit-gate.sh PASS if .py changes; FE-only changes go via separate cascade TO if needed.</expect>
    </step>
    <step>
      <run>Empirical verification: re-emit affected platinum artifacts; verify CBBY total reconciles per AC2</run>
      <expect>Post-fix CBBY ≤ firm AUA OR documented + tooltip explained.</expect>
    </step>
  </phase>

  <phase id="2" when="commit + deploy">
    <step>
      <run>safe-deploy.sh per Rule 13 if gold/silver/bronze edit; comp-pipescript deployed MATCH</run>
      <expect>SHA-MATCH; deploy clean.</expect>
    </step>
    <step>
      <run>SSM dispatch to re-run affected scripts; verify Andrew empirical reconciliation post-deploy</run>
      <expect>Reconciliation confirmed empirically on Inflection portal Books tab.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4 (PROD promote candidate)</run>
      <expect>Evidence-bearing close with reconciliation table post-fix.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Fix scope matches INFFIN.019 brief recommendation
    AC2: Post-fix CBBY total reconciles to AUA-by-Tax-Status OR documented + tooltip explained
    AC3: Capital Gains (TTM) value validated post-fix
    AC4: 2026 partial-year vs 2025 plausibility resolved
    AC5: 49F regression smoke PASS (per investigation risk assessment)
    AC6: ds-commit-gate.sh PASS (if .py)
    AC7: safe-deploy.sh PASS + S3 upload + comp-pipescript deployed MATCH (if .py)
    AC8: SSM re-run + empirical verification post-deploy
    AC9: RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>ds-commit-gate.sh + safe-deploy.sh per CLAUDE.md Rule 13+14.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: ADVI_INFFIN.019 RAVC2 (scope-determining).
    PARALLEL-OK: All other INFFIN.021-028 TOs.
    POTENTIAL FE-CASCADE: if investigation determines FE-only fix (tooltip wording), this TO transfers to RD 0.4.2 lane.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_scope>Affected platinum artifacts re-emit after gold fix; current-date forward + 1-day backfill recommended.</reprocess_scope>
  </data_reprocess_scope>

  <deliverables>
    1. Fix implementation per .019 brief
    2. ds-commit-gate + safe-deploy + S3 SHA-MATCH
    3. Reconciliation post-fix evidence
    4. RAVC2
  </deliverables>

  <ravc>DS~C RAVC2 to COO + CC CTO + DT 0.4 on AC1-9 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"`.

    **Scope-conditional:** if investigation surfaces FE-only fix, this TO transfers to RD 0.4.2 lane with renumbering note. COO routing-discretion on transfer.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
