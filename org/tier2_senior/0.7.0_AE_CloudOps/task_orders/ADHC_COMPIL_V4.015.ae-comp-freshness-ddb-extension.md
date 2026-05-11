<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.015</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-freshness DynamoDB extension — `ddb &lt;table&gt;` subcommand + cadence config DDB target support</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_commit>6becc77e5</completed_commit><!-- Authored by CTO direct per Andrew 2026-05-08 PM "full 5-item, run it" post-retrospective. PRD v0.3 addendum §13.4 TO-15. v3 explicit "v4 candidate" finally landing. -->
    <priority>normal</priority>
    <estimated_effort>~1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §13.4 TO-15 (v0.3 addendum 2026-05-08 PM)</ref>
    <ref type="retrospective">docs/architecture/ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md §6.2 + §7 Item D</ref>
    <ref type="v3_deferred">ADHC_COMPIL_V3.md §1 out-of-scope: "DynamoDB freshness checks — v3's comp-freshness is S3-only; DynamoDB freshness is a v4 candidate."</ref>
    <ref type="cottonwood_driver">FIRMSEP.10 Cottonwood onboarding (gated on credentials + bucket creation) — multi-firm scope makes DDB-backed firm-config state freshness more important; FIRM_BUCKET_MAP / opal-users-v2 / opal-routing-config are DDB-state surfaces.</ref>
  </references>

  <context>
    v3 `comp-freshness` checks S3 artifact mtime against cadence config (e.g., `silver/canonical_prices/latest.parquet` < N hours old). v3 PRD §1 explicitly listed DynamoDB freshness as "v4 candidate" — V4 v0.1/v0.2 didn't include it. With Cottonwood onboarding scaling firm-config DDB state (FIRM_BUCKET_MAP entries, partner-firm META rows, route-config items), DDB freshness gap means firm-config drift would not be caught by current `comp-freshness`.

    Fix: add `ddb &lt;table&gt;` subcommand mirroring S3 mode semantics. Cadence config extended to support DDB targets alongside S3 prefixes.
  </context>

  <scope>
    <step>
      <run>Read `comp-freshness` source + existing cadence config (`freshness_config.yaml`). Confirm S3-mode logic structure.</run>
      <expect>S3 mode is `target → mtime check → cadence threshold → MATCH/STALE/MISSING`; DDB mirror should follow same flow.</expect>
    </step>
    <step>
      <run>Extend cadence config schema to support DDB targets:
```yaml
ddb:
  - table: opal-users-v2
    item_pattern: "FIRM#*"
    max_age_hours: 168
    cadence_note: "Firm config; updates only on partner onboarding"
  - table: opal-routing-config
    item_pattern: "ROUTE#*"
    max_age_hours: 24
    cadence_note: "Updated daily by route-sync Lambda"
```</run>
      <expect>Schema extension is backwards-compatible (existing S3 entries unchanged).</expect>
    </step>
    <step>
      <run>Add `comp-freshness ddb &lt;table&gt;` subcommand: scan DDB table items matching `item_pattern`; check item-mtime (or last-modified attribute) against `max_age_hours`; emit MATCH/STALE/MISSING per item.</run>
      <expect>DDB subcommand works empirically against opal-users-v2.</expect>
      <if_mismatch>If DDB items don't have a standard mtime attribute, document the convention (e.g., expect `updated_at` field or use `dynamodb-streams` if needed; defer streams-mode if complex).</if_mismatch>
    </step>
    <step>
      <run>Add `comp-freshness all` (or `comp-freshness chain &lt;target&gt;`) to support running both S3 + DDB checks in one pass per cadence config.</run>
      <expect>Combined output; one command runs full freshness sweep.</expect>
    </step>
    <step>
      <run>Empirical test:
        - `comp-freshness ddb opal-users-v2 --pattern "FIRM#*"` — should return MATCH for FIRM#inflection, FIRM#cottonwood, FIRM#49financial (all recently updated)
        - Synthetic stale-fixture: set max_age=1h on a slowly-changing test item → STALE
        - Existing S3 mode regression — `comp-freshness chain bd` produces same output as pre-ship</run>
      <expect>3 cases pass; S3 regression-clean.</expect>
    </step>
    <step>
      <run>Update `org/modules/graph/comp-tools.yaml` comp-freshness entry: document DDB subcommand + extended cadence config schema.</run>
      <expect>Catalog reflects new capability.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with empirical evidence + integration with FIRMSEP scope.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">`comp-freshness ddb &lt;table&gt;` subcommand exists + works empirically against opal-users-v2.</ac>
    <ac id="2">Cadence config schema extended to support DDB targets (backward-compatible with S3-only configs).</ac>
    <ac id="3">DDB freshness check returns MATCH/STALE/MISSING semantics (same as S3 mode).</ac>
    <ac id="4">`comp-freshness all` runs combined S3 + DDB sweep per cadence config.</ac>
    <ac id="5">Synthetic stale-fixture test fires STALE empirically.</ac>
    <ac id="6">S3 mode regression-clean (existing `comp-freshness chain bd` produces same output as pre-ship).</ac>
    <ac id="7">comp-tools.yaml entry updated.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read comp-freshness source + cadence config + DDB table schemas (opal-users-v2, opal-routing-config).</phase>
    <phase id="2">Pre-commit: 6-cell test matrix — 3 DDB cases + 1 synthetic stale + 1 S3 regression + 1 combined-mode.</phase>
    <phase id="3">Post-commit empirical: rerun all 6 cases; append to compiler-tools-log.md with new convention column for synthetic-vs-real (TO-016).</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>6-cell test matrix + cadence config schema + sample output</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>DynamoDB Streams integration (defer until use-case emerges).</item>
    <item>Cross-region DDB checks (single-region scope; us-east-1).</item>
    <item>RDS/Aurora freshness (separate scope; not biting).</item>
    <item>DDB item-write traffic introspection (just mtime/last-modified attribute).</item>
  </out_of_scope>
</task_order>
