<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.SHAPE-VERIFY</id>
    <project>ADVI_INFETL</project>
    <title>Per-dim daily-pull shape verification — rep_id filter, INFGRD scope, schema parity</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>active</status>
    <priority>medium</priority>
    <estimated_effort>~1d cumulative across 9 dims; ~1h per dim post-Lambda-deploy</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_prd">docs/architecture/ADVI_INFETL.md</ref>
    <ref type="incident">INFNNA.001 root cause was rep_id filter misalignment — pull script hardcoded "3,11,12" while gold script filtered {3,6,11,12}. Years of stale silver+canonical_nna under wrong attribution. This TO ensures that class of bug is caught at deploy time, not 6 months later via portal symptoms.</ref>
    <ref type="upstream_TOs">INFETL.LAMBDA-DIMS (Lambdas to verify); INFETL.DAILY-AUDIT (matrix that defines expected shape)</ref>
    <ref type="output_target">docs/architecture/INFETL_PULL_SHAPE_VERIFY.md (NEW)</ref>
  </references>

  <context>
    Per-dim daily Lambdas must produce output matching a documented shape spec.
    Verification is post-deploy + recurring (e.g., weekly), so any drift
    (e.g., a future Orion attribution change like Joe's) surfaces fast.

    Per-dim verification covers:
      - Bronze pull rep_id filter set (must be {3, 6, 11, 12} for INFLECTION-scoped dims)
      - Silver INFGRD scope filter (custodian + rep_id intersection)
      - Schema field set vs portal-expected shape
      - Row count + AUA totals within Guard B bounds (per INFNNA.GUARDS-AUDIT thresholds)
      - Sentinel JSON metadata correctly populated
  </context>

  <scope>
    <step>
      Define per-dim shape spec template. Captured in
      docs/architecture/INFETL_PULL_SHAPE_VERIFY.md:
        | dim | bronze rep_id filter | silver scope filter | schema fields | row count band | AUA band |
    </step>
    <step>
      For each of 9 dims (post each LAMBDA-DIMS ship), run shape check:
        - Pull bronze sample for snapshot_date
        - Pull silver sample for snapshot_date
        - Diff against spec; flag any deviation
        - Empirical: run actual Lambda invocation and verify output shape
    </step>
    <step>
      Build a daily verification script (data/orion/scripts/verify/shape_check.py):
        - Reads spec from INFETL_PULL_SHAPE_VERIFY.md (or YAML companion)
        - Iterates dims; runs check; emits PASS/FAIL summary
        - Wired to weekly EventBridge cron (06:00 UTC Sunday — same as parity check)
        - Alarm on FAIL → SNS opal-infrastructure-alerts
    </step>
    <step>
      Pre-commit gate on the verify script + commit + S3 upload + Terraform integration.
    </step>
    <step>
      Per-dim RAVC: spec landed + empirical sample passes + dim added to weekly verify.
    </step>
    <step>
      Final RAVC: all 9 dims wired into weekly shape check + alarm firing on synthetic FAIL test.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-pipescript io inf-{dim}-daily — used as ground truth for canonical shape</tool>
    <tool>comp-pii audit — sanity check no cleartext leak</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">INFETL_PULL_SHAPE_VERIFY.md spec doc landed with all 9 dims documented.</criterion>
    <criterion id="AC2">Verification script ships + runs cleanly against current state.</criterion>
    <criterion id="AC3">Weekly EventBridge cron + alarm wired.</criterion>
    <criterion id="AC4">Synthetic FAIL test (e.g., rep_id filter set to {3,11,12}) is caught + alarmed.</criterion>
    <criterion id="AC5">All 9 dims pass current-state shape check.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>INFETL.LAMBDA-DIMS — at least subset of Lambdas live to verify against.</upstream>
    <downstream>None.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Ships in parallel with LAMBDA-DIMS — incremental: as each dim's Lambda lands, add to spec + check. No need to wait for all 9.</message>
  </go_signal>
</task_order>
