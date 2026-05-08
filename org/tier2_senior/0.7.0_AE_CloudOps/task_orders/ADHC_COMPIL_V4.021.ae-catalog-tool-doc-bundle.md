<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.021</id>
    <project>ADHC_COMPIL_V4</project>
    <title>Catalog + tool-doc bundle — flag/argument mismatches + stale catalog examples + semantic robustness (16 items from OPS Cat 3+4+5)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- Closed 2026-05-08T~PM by AE 0.7.0. 16 OPS items addressed via mix of doc-fixes + small CLI implementations. CLI ships: check-lambda-layer-deps --json (Cat 3.3); comp-constants check --lane (Cat 3.4); comp-trace --json multi-match disambiguation (Cat 3.5); comp-validate --list matcher tightened to exact-or-prefix-with-underscore + --lane filter (Cat 5.2); comp-validate --list emits ERROR + first-15 candidates on unknown script_id (Cat 5.3); comp-pipescript dag prints both named + detected-paths counts (Cat 5.4). Doc-fixes in comp-tools.yaml: comp-trace examples updated to canonical/working forms incl. INF gold + s3:platinum (Cat 4.4); comp-iam role example corrected (Cat 4.3); comp-platinum page example with non-existent components flagged (Cat 4.1/4.2); origins count 5→6 (Cat 5.6); inf-silver deployment caveat documented (Cat 5.5); --json/--lane added to relevant entries; getEmployeeLeaderboard→getFirmLeaderboard for working endpoint example (Cat 5.1). Out-of-scope: 5.4 INF named-key wiring (current detected-paths report covers; deeper s3_layout-style INF named keys = follow-on if needed). -->
    <priority>normal</priority>
    <estimated_effort>~1d (mostly doc updates + a few small CLI fixes)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md (V4 family)</ref>
    <ref type="ops_briefing">AE 0.7 OPS triage briefing 20260508T~PM Cat 3 (flag/argument mismatches; 6 items) + Cat 4 (stale catalog examples; 4 items) + Cat 5 (semantic robustness; 6 items)</ref>
    <ref type="ops_matrix">docs/architecture/ADHC_COMPIL_V4_017_TEST_MATRIX.md</ref>
  </references>

  <context>
    16 items from OPS triage Cat 3+4+5. Mostly doc fixes (catalog examples wrong, flag names drifted) with a few small CLI implementations (e.g., comp-validate input validation). AE picks per-item: pure doc-fix vs implement-missing-flag vs minor-semantic-fix.
  </context>

  <scope>
    <step>
      <run>**Cat 3 — Flag/argument mismatches (6 items):**
        - 3.1 `check-lambda-layer-deps`: catalog says positional arg; reality is `--function/--pipeline/--strict/--verbose` flags. Fix: update comp-tools.yaml + segment-scope reference card examples to use real flags.
        - 3.2 `check-lambda-layer-deps --all`: doesn't exist. Default (no-flag) is repo-wide. Fix: doc-update.
        - 3.3 `check-lambda-layer-deps --json`: doesn't exist. Either implement (useful for CI) or remove from docs. AE picks.
        - 3.4 `comp-constants check --lane bd`: rejected. Lane is config-metadata-driven. Fix: doc-update OR add `--lane` flag (low cost; per-lane filter is useful).
        - 3.5 `comp-trace --json D_04`: flag accepted but produces same text output. Fix: implement JSON output OR remove flag (AE picks).
        - 3.6 `comp-pipescript postdeps D_04`: returns "No dependencies declared." Catalog example over-promises. Fix: doc-update example.
      </run>
      <expect>Per-item fix landed (doc OR implementation per AE judgment); catalog examples accurate to actual CLI behavior post-ship.</expect>
    </step>
    <step>
      <run>**Cat 4 — Stale/incorrect catalog examples (4 items):**
        - 4.1 `comp-platinum page AdvisorIntelligence`: stale (directory not leaf). Fix: example to `PartnerAnalytics` or `ClientsTab`.
        - 4.2 `comp-platinum page BooksTab`: doesn't exist. Closest: `AdvisorBookView`. Fix: update example.
        - 4.3 `comp-iam role bd-gold-runner-role`: wrong name. Real: `bd-gold-layer-lambda-role` (Lambda) or `bd-gold-runner-ec2-role` (EC2). Fix: update example.
        - 4.4 `comp-trace D_04`: returns "Multiple matches" + 50 candidates. Fix: either (a) make script-level node match by default when ID is unambiguous prefix, OR (b) update example to use canonical form `gold:D_04.client_portal_summary`. AE picks; (a) is better UX.
      </run>
      <expect>All 4 catalog examples either work or are updated to working canonical form.</expect>
    </step>
    <step>
      <run>**Cat 5 — Semantic robustness (6 items):**
        - 5.1 `comp-trace getEmployeeLeaderboard`: stale registration; portal uses `getFirmLeaderboard`. Fix: graph-cleanup pass OR doc update.
        - 5.2 `comp-validate D_04 --list`: substring matches BD + INF + D_04_positions_output. Fix: tighten matcher to exact-or-prefix; add `--lane` filter.
        - 5.3 `comp-validate definitely_not_a_thing`: no error. Fix: validate script_id against config entry; emit error with first-15 candidates (mirror comp-iam service pattern).
        - 5.4 `comp-pipescript dag --pipeline inf-gold`: S3 keys 0 (BD shows 96 for 28). Fix: wire S3-key extraction for INF DAG.
        - 5.5 `comp-pipescript deployed --pipeline inf-silver`: all MISSING_ON_S3 (correct empirically; doc implies inf-silver works analogously). Fix: doc-update OR remove inf-silver from --pipeline choices until INF silver bucket goes live. AE picks.
        - 5.6 `comp-routes origins`: 6 origins; catalog says 5. Fix: update count comment.
      </run>
      <expect>Per-item fix landed; tools behave + document accurately.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with per-Cat summary of fixes (per-item: doc-only vs CLI vs hybrid).</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">All 6 Cat 3 items addressed (doc OR CLI fix per AE judgment; per-item rationale documented).</ac>
    <ac id="2">All 4 Cat 4 items addressed (catalog examples work or replaced with working examples).</ac>
    <ac id="3">All 6 Cat 5 items addressed.</ac>
    <ac id="4">Empirical: re-run each item's failing OPS test case; record PASS post-ship in compiler-tools-log.md (16 rows).</ac>
    <ac id="5">No regression: pick 5 random PASS cases from V4.017 matrix; verify still PASS post-ship.</ac>
    <ac id="6">comp-tools.yaml + comp-tools-segment-scope.md examples all use real, working command strings post-ship.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read affected CLI sources + comp-tools.yaml entries per item.</phase>
    <phase id="2">Pre-commit: rerun OPS test cases per item + 5-case regression sample.</phase>
    <phase id="3">Post-commit: 16 rows + 5 regression rows appended to compiler-tools-log.md.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Per-item PASS evidence + AE judgment rationale per fix-type (doc vs CLI)</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>BLOCKING bugs (Cat 1 — covered by V4.019).</item>
    <item>Cross-layer graph extension (Cat 2 — covered by V4.020).</item>
    <item>Coverage backfill + verdict validation (Cat 6+7 — covered by V4.022).</item>
    <item>DEFERRED items gated on V4.005/.015/.006/FIRMSEP.10.</item>
  </out_of_scope>
</task_order>
