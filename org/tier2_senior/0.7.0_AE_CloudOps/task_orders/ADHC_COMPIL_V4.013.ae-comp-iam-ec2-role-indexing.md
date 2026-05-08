<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.013</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-iam service EC2 role indexing — extend resolver to handle EC2 role names alongside Lambda function names</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status><!-- Authored by CTO direct per Andrew 2026-05-08 PM "full 5-item, run it" post-retrospective. PRD v0.3 addendum §13.4 TO-13. -->
    <priority>normal</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §13.4 TO-13 (v0.3 addendum 2026-05-08 PM)</ref>
    <ref type="retrospective">docs/architecture/ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md §6.6 + §7 Item C</ref>
    <ref type="anchor_a">2026-04-16 AE 0.6 (dh3_dh7_dispatcher_hygiene): "comp-iam service for the gold runner EC2 returned 'No service matching' — gap-cross-reference focuses on Lambda; for EC2 role changes we rely on aws iam get-role-policy"</ref>
    <ref type="anchor_b">2026-05-08 AE 0.7 (INFETL.011 RAVC1): "comp-iam service inf-gold-trigger: tool catalog miss" — second incident</ref>
    <ref type="related_to">ADHC_COMPIL_V4.006 cross-firm subcommand reuses same IAM-role parse; this TO extends parse routing</ref>
  </references>

  <context>
    `comp-iam service <name>` resolves Lambda function names to IAM role + grants. EC2 role names (inf-bronze-runner-role, bd-gold-layer-runner-role, etc.) are not in the resolver — return "No service matching." Data exists in IAM-role parse (61 roles per current `comp-iam` default invocation); subcommand routing is the missing surface.

    Fix: extend resolver to handle EC2 role names. Reuse existing parse (no new index). Lookup order: Lambda function names → EC2 role names → unknown (with helpful error listing available services).
  </context>

  <scope>
    <step>
      <run>Read `comp-iam` source. Locate `service` subcommand resolver. Confirm Lambda-name lookup logic + IAM-role parse data.</run>
      <expect>Resolver function clearly identifiable; Lambda-name → role mapping is source-of-truth; can be extended.</expect>
    </step>
    <step>
      <run>Add EC2 role name resolver: when Lambda lookup fails, fall through to EC2 role names. EC2 role names sourced from existing IAM-role parse.</run>
      <expect>Two-stage lookup: Lambda first, EC2 second. No regression on Lambda case.</expect>
    </step>
    <step>
      <run>Update error message on unknown service: list both Lambda function names AND EC2 role names available; help agent disambiguate.</run>
      <expect>Improved UX on the "No service matching" failure mode.</expect>
    </step>
    <step>
      <run>Empirical test:
        - `comp-iam service inf-gold-trigger` (Lambda) — returns role + grants (existing behavior unchanged)
        - `comp-iam service inf-bronze-runner` (EC2 role) — returns role + grants (NEW behavior)
        - `comp-iam service bd-gold-layer-runner` (EC2 role) — returns role + grants (NEW behavior)
        - `comp-iam service nonexistent-thing` — returns improved error message with both lists</run>
      <expect>3 known cases work post-ship; error case helpful.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">`comp-iam service <ec2-role-name>` returns role + grants (matching existing Lambda case output format).</ac>
    <ac id="2">Lambda case unchanged — `comp-iam service <lambda-name>` produces same output as pre-ship.</ac>
    <ac id="3">Lookup order: Lambda first, EC2 fallback. Disambiguation if name collides (unlikely; document if encountered).</ac>
    <ac id="4">Improved error message on unknown name lists both Lambda + EC2 role candidates.</ac>
    <ac id="5">Empirical 4-case matrix validated (3 known-good + 1 unknown).</ac>
    <ac id="6">Reuses existing IAM-role parse (no new index, no new AWS API calls).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read comp-iam service resolver + IAM-role parse data.</phase>
    <phase id="2">Pre-commit: 4-case test matrix.</phase>
    <phase id="3">Post-commit empirical: rerun anchor cases (inf-gold-trigger Lambda + inf-bronze-runner EC2); append to compiler-tools-log.md.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>4-case test matrix + 2 anchor case re-runs</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Building new IAM index (reuse existing parse).</item>
    <item>EC2 instance-level introspection beyond role-level (out of scope; tool stays at role granularity).</item>
    <item>Cross-account IAM (single-account scope).</item>
  </out_of_scope>
</task_order>
