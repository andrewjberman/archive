<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.022</id>
    <project>ADHC_COMPIL_V4</project>
    <title>Coverage backfill + verdict validation — BD Lambda IAM data backfill + comp-platinum reverse hybrid-merge fix + loop-quiescence false-positive (4 items from OPS Cat 6+7)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- Closed 2026-05-08T~PM by AE 0.7.0. 4 OPS items closed. Cat 6.1: built .tools/backfill-lambda-iam-mapping.py (parses TF for module->role mapping with locals + var.shared + inline-arn handling); 129 of 151 Lambdas backfilled (was 1); 22 unresolved are decommissioned/legacy/test functions. comp-iam gaps post-backfill surfaces 9 real permission gaps (queued separate remediation per out-of-scope). Cat 6.2: comp-platinum reverse '<key>#field' fallback2 directory-prefix speculatives suppressed when query has #field — was 18 SPECULATIVE; now 0. --strict regression-clean (exits 2 with N suppressed message preserved). Cat 7: loop-quiescence adds NO_PROJECT_FILE verdict separate from QUIESCENT_CLEAN; bare macro prefix returns NO_PROJECT_FILE + hint to use full project code; full project code path unchanged. Out-of-scope: 6.1 BD-Lambda permission-gap remediation (separate TO scope when needed). -->
    <priority>normal</priority>
    <estimated_effort>~1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md (V4 family)</ref>
    <ref type="ops_briefing">AE 0.7 OPS triage briefing 20260508T~PM Cat 6 (Coverage backfills; 2 items) + Cat 7 (Verdict validation; 2 items)</ref>
    <ref type="v4_010_ac5">V4.010 RAVC2 evidence — AC5 shipped against literal text; deeper "field-filter speculative" intent surfaced post-ship via OPS Cat 6.2. NOT a retro-reopen of V4.010; new work scope.</ref>
  </references>

  <context>
    4 items from OPS triage Cat 6+7. Two are coverage backfills (data + tool work); two are verdict-validation false positives in `loop-quiescence`.
  </context>

  <scope>
    <step>
      <run>**Cat 6.1 — BD Lambda IAM mapping backfill:** ~100 BD Lambdas show `comp-iam service <name>` returns role "(not mapped)" + ops `[UNKNOWN]`. INF Lambdas + EC2 roles work via V4.013 fallback; the gap is `infra/aws/lambda/ci/lambda-source-map.json` IAM mapping for BD Lambdas. Until backfilled, `comp-iam gaps` returns 0 because gap-detection requires role mapping; missing roles silently skipped.

        Fix: backfill `iam_role` field for all unmapped BD Lambdas in lambda-source-map.json. One-time data work. Post-backfill: `comp-iam gaps` becomes meaningful for BD Lambdas (may surface new permission gaps for follow-on remediation).</run>
      <expect>≥95 of ~100 unmapped BD Lambdas now have `iam_role` populated; remaining unmapped are explicitly documented (decommissioned / not deployed / etc.). `comp-iam gaps` re-run produces meaningful output.</expect>
    </step>
    <step>
      <run>**Cat 6.2 — comp-platinum reverse hybrid-merge fix (V4.010 follow-on):** `comp-platinum reverse "<key>#field"` triggers hybrid resolution but doesn't actually narrow — returns ALL artifact-reverse SPECULATIVE results regardless of `#field` filter. `--strict` correctly suppresses (works), but the `#field` hint alone doesn't tighten.

        AE diagnosis (in OPS briefing): "the artifact-reverse + field-reverse merge is unioning rather than intersecting. The `#field` should restrict CONSUMED BY to components that reference that specific field path; instead it returns all consumers of the parent artifact tagged SPECULATIVE."

        Fix: rework hybrid merge to use field-reverse as a filter on artifact-reverse, not a parallel branch. NOT a retro-reopen of V4.010 — that shipped against literal AC5 text; this is scope expansion.</run>
      <expect>`comp-platinum reverse "platinum/firm/header_metrics.json#radial_12m"` (no --strict) returns 0 results when no consumer references that specific field, instead of 18 SPECULATIVE results from parent-artifact prefix matching.</expect>
      <if_mismatch>If field-reverse index doesn't have field-level granularity for prefix-matched directories: scope is broader than refactor; RAVC1 to CTO; consider deferring.</if_mismatch>
    </step>
    <step>
      <run>**Cat 7.1+7.2 — loop-quiescence false-positive QUIESCENT_CLEAN:** `loop-quiescence ADHC --summary` and `loop-quiescence INFETL --summary` (macro prefix, not full project code) both return `Verdict: QUIESCENT_CLEAN / Project file present: False / Counts: total=0`. Tool conflates "project file not found" with "all TOs closed." Tier-1 SA reading this gets false positive.

        Fix: add `NO_PROJECT_FILE` verdict separately from `QUIESCENT_CLEAN`. Reject macro-prefix input OR scan all `org/projects/{MACRO}*.json` files when prefix-style input given. AE picks: cleaner is reject + helpful error (mirror comp-iam service unknown-name pattern).</run>
      <expect>`loop-quiescence ADHC --summary` returns `NO_PROJECT_FILE` verdict (or scans all ADHC_* projects + aggregates). NOT `QUIESCENT_CLEAN total=0`.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with empirical evidence per item.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">≥95 unmapped BD Lambdas backfilled with `iam_role` in lambda-source-map.json; remaining explicitly documented.</ac>
    <ac id="2">`comp-iam gaps` post-backfill produces meaningful output for BD Lambdas (may surface new gaps for follow-on remediation).</ac>
    <ac id="3">comp-platinum reverse `<key>#field` (no --strict) narrows results when field-level filtering is possible; returns empty when no consumer references the field.</ac>
    <ac id="4">comp-platinum reverse with --strict regression-clean (V4.010 behavior unchanged on the strict path).</ac>
    <ac id="5">loop-quiescence on macro prefix returns `NO_PROJECT_FILE` verdict OR scans all `{MACRO}*.json` projects.</ac>
    <ac id="6">loop-quiescence on full project code (e.g., ADHC_COMPIL_V4) regression-clean.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read lambda-source-map.json + comp-iam role-mapping logic + comp-platinum reverse hybrid-merge code + loop-quiescence verdict logic.</phase>
    <phase id="2">Pre-commit: per-item test (4-cell matrix).</phase>
    <phase id="3">Post-commit: 4 rows + 2 regression rows in compiler-tools-log.md.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Per-item pre/post evidence + BD Lambda backfill count + V4.010 strict regression test</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>V4.010 retro-reopen (this is scope expansion, not regression).</item>
    <item>EC2 role IAM backfill beyond what V4.013 already covers.</item>
    <item>Permission-gap REMEDIATION on the new BD Lambda gaps (this TO surfaces; remediation is separate scope).</item>
    <item>DEFERRED items gated on V4.005/.015/.006/FIRMSEP.10.</item>
  </out_of_scope>
</task_order>
