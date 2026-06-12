<to_id>NFRA_COT_TOOLING</to_id>
<project>NFRA_GRAPHS (tool-coverage fill; no D-scope collision)</project>
<title>Cot tooling coverage — gold_validate_config.yaml registration + comp-pipescript opal-data-cot extension</title>
<assigned_to>0.6.0_AE_PartnerETL</assigned_to>
<issued_by>2.0.0_SA_COO (CTO cleared no-scoping 141911Z; COT-FIX coverage gap surfaced 141659Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>pending</status>
<priority>Low — tooling coverage fill; no gate on cot cutovers; GO at capacity</priority>

<references>
  <ref type="gap">COT-FIX AE RAVC2 141659Z: cot has no comp-validate config (registry = BD+INF only) + comp-pipescript io/deployed is bd-only/blind to cot; shadow battery substituted for comp-validate in COT-FIX</ref>
  <ref type="cto-clearance">CTO 141911Z: no CTO architectural scoping needed; fill within ALREADY-RATIFIED architecture (Rule-13 PIPELINE_MAP, per-pipeline gold_validate_config pattern, same per-bucket blindness class as mdpf/backfill gap)</ref>
  <ref type="constraints">CTO 141911Z constraints (a)(b)(c) — firm separation, fail-closed, catalog completeness</ref>
</references>

<scope>
Two tool-coverage additions for the cot (Cottonwood) pipeline:

**1. comp-validate: cot gold_validate_config.yaml**
Register cot gold scripts with the comp-validate framework. Create `data/cot/scripts/gold/gold_validate_config.yaml` following the established per-pipeline pattern (see `data/black_diamond/scripts/gold/gold_validate_config.yaml` as the reference). The registration must use fail-closed semantics per COMP_VALIDATE_PROTOCOL §10.1 / §10.1b: NO_CONFIG and ZERO_CHECKS both return exit-2 UNVALIDATED (absence != PASS). The point is to make cot gold scripts stop being structurally NO_CONFIG on comp-validate runs.

**2. comp-pipescript: extend to opal-data-cot**
Extend comp-pipescript's deployed-check (PIPELINE_MAP or equivalent) to recognize `data/cot/scripts/gold/*.py` and check `opal-data-cot/code/gold/`. This should make `comp-pipescript deployed data/cot/scripts/gold/A_01.advisor_assignments.py` return MATCH/STALE/MISSING rather than silently skipping cot scripts. The md5 MATCH pattern from DS's Rule-13 deploy confirmed the correct S3 path is `opal-data-cot/code/gold/`.

**3. graph-call-manifest.yaml + comp-tools.yaml updates**
If the comp-pipescript or comp-validate surface/flags change, update both `org/modules/graph/graph-call-manifest.yaml` and `org/modules/graph/comp-tools.yaml` entries for the affected tools in the same commit (Rule 20 catalog completeness). graph-call-manifest.yaml is ANY_EXEC-owned — land under COO/CTO/CVO author line; flag the patch in RAVC2 for COO to commit (same handoff pattern as TO-F1).

**FIRM SEPARATION (MANDATORY):**
- comp-pipescript cot extension reads `opal-data-cot/code` ONLY — no cross-bucket fallback to opal-data-bd
- gold_validate_config.yaml is cot-scoped; no bd artifacts referenced
- Cross-firm guard class applies to tooling reads as much as script code
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>Read data/black_diamond/scripts/gold/gold_validate_config.yaml (reference pattern) + read comp-pipescript PIPELINE_MAP section (understand the extension point)</run>
      <expect>Pattern understood; PIPELINE_MAP extension point identified; fail-closed semantics clear.</expect>
      <if_mismatch>Surface structural surprises to COO before proceeding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-validate data/cot/scripts/gold/A_01.advisor_assignments.py (one spot-check on a known-deployed script)</run>
      <expect>Exit 0 PASS or WAIVED (not NO_CONFIG or UNVALIDATED). If exit-2 NO_CONFIG: registration is incomplete.</expect>
      <if_mismatch>Fix the registration before commit.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript deployed data/cot/scripts/gold/A_01.advisor_assignments.py</run>
      <expect>MATCH (it was just deployed by DS at 812200e5). If MISSING or blind-skip: extension is incomplete.</expect>
      <if_mismatch>Fix the PIPELINE_MAP extension before commit.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- graph-call-manifest.yaml is ANY_EXEC-owned (COO/CTO/CVO author line required). Flag the patch in RAVC2 and COO will land it (same pattern as TO-F1 manifest handoff 08475dbeb).
- This TO does NOT touch NFRA_GRAPHS D-scope (portal/pipeline trace graph is separate from per-bucket deployed-check tooling).
- DS Rule-13 deploy: no cot gold script changes in this TO; the tooling reads the already-deployed S3 artifacts.
</cross_domain_coordination>

<acceptance_criteria>
- comp-validate exits PASS/WAIVED (not NO_CONFIG) on spot-check cot gold script.
- comp-pipescript deployed returns MATCH/STALE/MISSING (not blind-skip) for cot gold scripts.
- Firm separation: opal-data-cot reads only, no opal-data-bd references in cot tooling paths.
- graph-call-manifest.yaml + comp-tools.yaml updated if surface changes (ANY_EXEC handoff patch in RAVC2).
- RAVC2 to COO: commit hash + spot-check comp-validate output + comp-pipescript deployed output.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Tooling-coverage only; no data-path or script changes.</no_reprocess_needed></data_reprocess_scope>
