<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.004</id>
    <project>ADVI_INFETL</project>
    <title>inf-portal-advisor-publisher Lambda — replace STUB with per-advisor drill-down implementation</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>normal</priority>
    <estimated_effort>~0.75d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFETL.md §3 (5-tier model, Tier 5b advisor drill), §4.6 (component spec), §6 Phase 1 TO-4</ref>
    <ref type="bd_pattern">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher (or analog) — BD per-advisor drill publisher (canonical reference; pattern parity expected)</ref>
    <ref type="target_file">infra/aws/lambda/inf-portal-advisor-publisher/lambda_function.py — currently STUB</ref>
    <ref type="ds_c_expertise">DS~C owns INF_D_05 (client_top_holdings) + INF_D_06 (client_timeseries) — per-client publisher logic. Per-advisor logic is a parallel concern (iterate advisors instead of clients). Per CTO RAVC2 routing concur.</ref>
    <ref type="paired_to">TO-3 (inf-portal-publisher) handler START fans out to this Lambda — TO-3 + TO-4 both ship for full Tier 5 chain</ref>
  </references>

  <context>
    INFETL §3 architecture mandates inf-portal-advisor-publisher Lambda as Tier 5b — per-advisor
    drill-down publisher. Iterates all reps from gold/dimensions/advisor_assignments;
    emits platinum/advisors/{rep_id}/{...}.json files for each advisor. 4 advisors at
    current Inflection scale (rep_ids 3, 6, 11, 12 per accounts_v2).

    Currently STUB. This TO replaces STUB with full implementation.

    Invocation: TO-3 inf-portal-publisher invokes this Lambda async at handler START
    (concurrent execution while firm publish runs). No fan-out from this Lambda.
    Iterates advisors sequentially within single Lambda invocation.
  </context>

  <scope>
    <step>
      Read BD analog: bd-portal-advisor-publisher (path varies; locate via
      `find infra/aws/lambda -name "*advisor-publisher*"` or similar). Identify:
      handler entry, advisor enumeration pattern, per-advisor data shaping, S3 write
      pattern, error handling for missing advisor data.
    </step>
    <step>
      Read existing inf-portal-advisor-publisher STUB. Confirm Lambda layer config
      requires pandas-pyarrow-layer (parquet reads).
    </step>
    <step>
      Map INF inputs/outputs per PRD §4.6:

      Inputs (from gold/):
        gold/dimensions/advisor_assignments/{date}.parquet (advisor enumeration source)
        gold/canonical/canonical_holdings/{date}.parquet
        gold/canonical/canonical_lots/{date}.parquet
        gold/canonical/canonical_nna/{date}.parquet
        gold/canonical/canonical_performance/{date}.parquet
        gold/views/* (advisor-scoped views)

      Outputs (to platinum/advisors/{rep_id}/):
        platinum/advisors/{rep_id}/summary.json           (header metrics for advisor)
        platinum/advisors/{rep_id}/timeseries.json        (per-advisor AUA timeseries)
        platinum/advisors/{rep_id}/clients.json           (per-advisor client list)
        platinum/advisors/{rep_id}/nna_clients.json       (per-advisor NNA breakdown)
        platinum/advisors/{rep_id}/holdings.json          (per-advisor top holdings)
        (full output list per BD analog enumeration)

      Phase 1 mandate: comp-pipescript io inf-portal-advisor-publisher post-implementation.
    </step>
    <step>
      Implementation skeleton:

      def lambda_handler(event, context):
          run_date = _extract_run_date(event)

          # Read advisor enumeration
          advisors_df = _read_parquet(f"gold/dimensions/advisor_assignments/{run_date}.parquet")
          rep_ids = advisors_df["rep_id"].unique()  # currently 4 for Inflection

          # Read shared inputs (read once, slice per advisor)
          shared = _read_shared_gold_inputs(run_date)

          # Iterate advisors
          for rep_id in rep_ids:
              advisor_data = _slice_for_advisor(shared, rep_id)
              _write_advisor_summary(rep_id, advisor_data)
              _write_advisor_timeseries(rep_id, advisor_data)
              _write_advisor_clients(rep_id, advisor_data)
              _write_advisor_nna_clients(rep_id, advisor_data)
              _write_advisor_holdings(rep_id, advisor_data)

          return {"statusCode": 200, "advisors_published": len(rep_ids), "run_date": run_date}

      Optimization note: read shared parquets once (canonical_holdings, canonical_nna)
      and slice in-memory per advisor. Avoid re-reading per advisor (4× wasted I/O).
    </step>
    <step>
      Schema parity check: validate per-advisor JSON shape against portal expected
      shape (Distribution tab ADV-NNA client drill, advisor summary tile). Run
      `comp-platinum reverse platinum/advisors/*` post-implementation.
    </step>
    <step>
      Lambda Terraform config: ensure infra/aws/terraform/inf-pipeline/lambdas.tf
      aws_lambda_function.inf_portal_advisor_publisher has:
        memory_size  = 6144
        timeout      = 900
        layers       = [aws_lambda_layer_version.pandas_pyarrow_layer.arn]
      (BD analog uses 6144 MB per PRD §4.6). Update if currently stub-defaults.
    </step>
    <step>
      Source map: per CLAUDE.md rule 4, infra/aws/lambda/ci/lambda-source-map.json must
      have entry. Confirm present; update if missing.
    </step>
    <step>
      Pre-commit gate: .tools/ds-commit-gate.sh on lambda_function.py — exit 0.
    </step>
    <step>
      Commit via .tools/safe-commit.sh with --author "0.4.0_DS_ClientPlatform~C &lt;0.4.0_DS_ClientPlatform~C@opal.agent&gt;"
      -m "feat(ADVI_INFETL.004): inf-portal-advisor-publisher Lambda full implementation (replace STUB)"
      -- infra/aws/lambda/inf-portal-advisor-publisher/lambda_function.py
      [+ requirements.txt + lambdas.tf as needed]
    </step>
    <step>git push origin CLOUD.</step>
    <step>
      Lambda deploy via Terraform: coordinate with AE 0.7 for terraform plan + apply.
      Verify 0-diff post-apply.
    </step>
    <step>
      Manual empirical: invoke Lambda directly with synthetic event:
        aws lambda invoke --function-name inf-portal-advisor-publisher \
          --payload '{"run_date":"2026-05-07"}' \
          --cli-binary-format raw-in-base64-out /tmp/advisor_publisher_response.json
      Verify:
        - StatusCode 200, advisors_published=4 (or current count)
        - All platinum/advisors/{rep_id}/*.json files written for all advisors
        - CW logs clean
    </step>
    <step>
      End-to-end test: trigger TO-3 inf-portal-publisher → verify it invokes this Lambda
      → both Lambdas complete → platinum/firm/* + platinum/advisors/*/*.json all fresh.
    </step>
    <step>
      RAVC to COO: commit hash + S3 lambda zip ETag + lambda-source-map confirmation +
      manual empirical evidence (StatusCode + per-advisor file timestamps + advisor count).
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-iam service inf-portal-advisor-publisher — IAM permissions for gold S3 reads + platinum/advisors/* writes</tool>
    <tool>comp-pipescript io inf-portal-advisor-publisher — canonical input/output enumeration</tool>
    <tool>comp-platinum reverse platinum/advisors/* — verify portal consumers see expected schema</tool>
    <tool>comp-pii audit — no cleartext PII leak</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Lambda emits per-advisor JSON for all 4 current Inflection advisors (rep_id 3, 6, 11, 12) + scales to N advisors via gold/dimensions/advisor_assignments enumeration (no hardcoded rep_id list).</criterion>
    <criterion id="AC2">Schema parity vs BD analog (per-advisor summary, timeseries, clients, NNA-clients, holdings).</criterion>
    <criterion id="AC3">comp-pii audit clean.</criterion>
    <criterion id="AC4">End-to-end test passes: TO-3 publisher invokes this Lambda; both complete; platinum/firm/* + platinum/advisors/*/*.json all fresh.</criterion>
    <criterion id="AC5">Manual empirical invoke produces StatusCode 200 + advisors_published=4.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>TO-3 (inf-portal-publisher) provides the invocation source. TO-3 + TO-4 ship in parallel — at TO-3 ship, this Lambda may still be a STUB and TO-3 invokes the stub (acceptable for TO-3 AC3). When TO-4 ships, real impl receives the invocation.</upstream>
    <downstream>None within Phase 1.</downstream>
  </gates_dependencies>

  <risks_failure_modes>
    <risk>
      Per-advisor data is small (4 advisors × maybe 700 accounts) — Lambda should
      complete in &lt;60s. If memory exceeded, profile and right-size; 6144 MB likely
      excessive for INF (BD's 6144 sized for 150+ advisors).
    </risk>
    <risk>
      Schema drift vs BD analog: portal Distribution tab + advisor summary tiles may
      expect specific shape. AC2 + AC4 verify; iterate if mismatch.
    </risk>
    <risk>
      Hardcoded rep_id list anti-pattern: do NOT hardcode {3,6,11,12} — read from
      gold/dimensions/advisor_assignments. Inflection adds advisors over time;
      hardcode would silently miss new ones (same class as INFNNA.001 root cause).
    </risk>
  </risks_failure_modes>

  <go_signal>
    <issued_at>pending Andrew confirmation of OQ1+OQ8+INFNNA-scope</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HOLD. TO authored pre-Andrew GO per CTO RAVC2 authorization. ~0.75d effort. Ships in parallel with TO-3.</message>
  </go_signal>
</task_order>
