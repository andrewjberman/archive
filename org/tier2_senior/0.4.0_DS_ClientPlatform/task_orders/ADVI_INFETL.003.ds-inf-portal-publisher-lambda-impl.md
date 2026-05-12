<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.003</id>
    <project>ADVI_INFETL</project>
    <title>inf-portal-publisher Lambda — replace STUB with full implementation mirroring bd-portal-publisher</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_to_fallback>0.4.0_DS_ClientPlatform~D</issued_to_fallback>
    <fallback_after>1h post-dispatch with no DS~B pickup</fallback_after>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>pending_go</status>
    <priority>normal</priority>
    <estimated_effort>~1.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFETL.md §3 (5-tier model, Tier 5a publisher), §4.5 (component spec), §6 Phase 1 TO-3</ref>
    <ref type="bd_pattern">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py — ~2k lines, pandas-pyarrow-layer, 4096 MB / 900s. CANONICAL REFERENCE.</ref>
    <ref type="target_file">infra/aws/lambda/inf-portal-publisher/lambda_function.py — currently 25-line STUB returning {"status":"stub"}</ref>
    <ref type="terraform">infra/aws/terraform/inf-pipeline/lambdas.tf — existing aws_lambda_function.inf_portal_publisher resource (config update for memory/timeout if needed)</ref>
    <ref type="ds_b_expertise">DS~B has authored canonical_nna chain logic (INF_C_01) — publisher data-shaping is comparable concern (gold parquet reads → JSON shape transforms). Per CTO RAVC1 routing rationale.</ref>
  </references>

  <context>
    INFETL §3 architecture mandates inf-portal-publisher Lambda as Tier 5a — reads gold/
    parquets, writes platinum-canonical JSON to platinum/firm/. Currently a STUB
    (returns {"status":"stub","statusCode":200}); this TO replaces the STUB with full
    implementation.

    The publisher is the structural enforcement of Andrew's directive: "ONLY PLATINUM
    OUTPUTS ARE FED TO PORTAL, PERIOD." gold/ becomes a strict internal staging tier;
    only the publisher Lambdas may read from it. Portal API GW Lambdas read from
    platinum/* (per TO-7 audit + TO-8 migration).

    Pattern: this Lambda mirrors bd-portal-publisher with structural fidelity. The BD
    Lambda has been operating in production for ~12 months; pattern is proven.
    Departures from BD pattern allowed only where INF data shape genuinely differs
    (e.g., 4 advisors vs 150 in 49F, no role breakdowns, different lifecycle taxonomy).

    Fan-out: the publisher invokes inf-portal-advisor-publisher (TO-4) at handler
    START (concurrent execution while firm publish runs) and inf-capture-output-versions
    (TO-6, Phase 2) at handler END (after all platinum/firm/ writes complete). At
    Phase 1 ship without TO-6, the END invoke is a TODO with a clear placeholder.
  </context>

  <scope>
    <step>
      Read the BD canonical reference: infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py.
      Identify: handler entry, S3 read pattern (parquet via pandas + pyarrow), JSON shape
      build functions, S3 write pattern (boto3 put_object), Lambda-to-Lambda async invoke
      pattern (boto3 lambda.invoke InvocationType="Event"), CloudFront invalidation pattern.
    </step>
    <step>
      Read existing inf-portal-publisher STUB (infra/aws/lambda/inf-portal-publisher/lambda_function.py)
      and surrounding files (requirements.txt, tests/, etc.). Confirm Lambda layer config
      in Terraform: must use pandas-pyarrow-layer (per BD analog).
    </step>
    <step>
      Map INF gold inputs to platinum outputs per PRD §4.5:

      INF gold inputs (read from S3):
        gold/canonical/canonical_holdings/{date}.parquet     (INF_B_00 output)
        gold/canonical/canonical_lots/{date}.parquet         (INF_B_02 output)
        gold/canonical/canonical_nna/{date}.parquet          (INF_C_01 output)
        gold/canonical/canonical_performance/{date}.parquet  (INF_C_00 output)
        gold/dimensions/accounts_dim/{date}.parquet          (INF_A_00 output)
        gold/dimensions/advisor_assignments/{date}.parquet   (INF_A_01 output)
        gold/views/firm_mix_summary/{date}.parquet           (INF_D_02d output)
        gold/timeseries/{date}/*                             (INF_D_00b + INF_D_00d outputs)

      INF platinum outputs (write to S3):
        platinum/firm/header_metrics.json
        platinum/firm/leaderboard.json
        platinum/firm/timeseries_chart.json
        platinum/firm/clients_tab.json
        platinum/firm/filters/dimensions.json
        platinum/firm/snapshots/aua_by_architect.json
        platinum/firm/snapshots/aua_by_state.json
        platinum/firm/snapshots/aua_by_region.json
        platinum/firm/snapshots/aua_by_tax_status.json

      For each output, identify the BD analog file in gold/artifacts/ (BD writes there;
      INF writes to platinum/) — schema parity should be tight unless portal expects
      different shape. Phase 1 mandate `comp-pipescript io inf-portal-publisher`
      enumerates the canonical input-output map post-implementation.
    </step>
    <step>
      Implementation skeleton:

      def lambda_handler(event, context):
          # Determine target run_date from event (S3 ObjectCreated body)
          # OR read sentinel JSON metadata for run_date
          run_date = _extract_run_date(event)

          # Fan-out START: invoke advisor publisher concurrently
          _async_invoke("inf-portal-advisor-publisher", {"run_date": run_date})

          # Read gold inputs
          inputs = _read_gold_inputs(run_date)

          # Build platinum outputs
          header_metrics = _build_header_metrics(inputs)
          leaderboard = _build_leaderboard(inputs)
          timeseries_chart = _build_timeseries_chart(inputs)
          clients_tab = _build_clients_tab(inputs)
          filters_dim = _build_filters_dimensions(inputs)
          snapshots = _build_aua_snapshots(inputs)  # 4 cuts: architect/state/region/tax_status

          # Write platinum outputs
          _write_platinum_json(header_metrics, "platinum/firm/header_metrics.json")
          # ... etc

          # Cloudfront invalidate
          _invalidate_cf(["/api/scoped/advisor-intelligence/platinum/firm/*"])

          # Fan-out END: invoke capture-output-versions
          _async_invoke("inf-capture-output-versions", {"run_date": run_date})

          return {"statusCode": 200, "run_date": run_date, ...}

      Each _build_* function: Phase 1 references BD analog directly; INF-specific
      adjustments are documented inline.
    </step>
    <step>
      Schema parity check: for each platinum/firm/*.json output, validate against the
      shape currently consumed by the portal. Run `comp-platinum reverse platinum/firm/*`
      to enumerate consumers. Cross-check inferred schema vs portal API expectations.
      If schema differs from current ad-hoc gold reads (per TO-7 audit), flag in RAVC2.
    </step>
    <step>
      Fan-out invokes:
        - inf-portal-advisor-publisher: at handler start (concurrent). Implementation
          stubbed in TO-4; Phase 1 ship TO-3 may invoke a stub Lambda — that's OK;
          stub returns 200 fast. TO-4 ships full impl in parallel.
        - inf-capture-output-versions: at handler end (after all writes). Phase 2 TO-6.
          For Phase 1 ship, this invoke can be a TODO comment with a clear placeholder
          calling logger.info("TODO TO-6: invoke inf-capture-output-versions"). Do NOT
          remove the call site stub — TO-6 ship will fill it.
    </step>
    <step>
      CloudFront invalidation: identify CF distribution ID + path patterns. Per
      memory/inflec, CF distribution serves platinum at /api/scoped/advisor-intelligence/
      platinum/*. Distribution ID resolves via aws cloudfront list-distributions or
      from prior session notes (EVTSA9VEHNZVH per session60 INFLFE.006).
      Pattern: paths=["/api/scoped/advisor-intelligence/platinum/firm/*"] CallerReference=
      "publisher-{run_date}-{timestamp}".
    </step>
    <step>
      Lambda Terraform config: ensure infra/aws/terraform/inf-pipeline/lambdas.tf
      aws_lambda_function.inf_portal_publisher has:
        memory_size  = 4096
        timeout      = 900
        layers       = [aws_lambda_layer_version.pandas_pyarrow_layer.arn]  # or canonical name
      Update if currently stub-defaults (e.g., 256/30).
    </step>
    <step>
      Source map update: per CLAUDE.md rule 4, infra/aws/lambda/ci/lambda-source-map.json
      must have entry for inf-portal-publisher. Confirm present; update if missing or
      handler/entrypoint changed.
    </step>
    <step>
      Pre-commit gate: .tools/ds-commit-gate.sh on lambda_function.py — exit 0.
    </step>
    <step>
      Commit via .tools/safe-commit.sh with --author "0.4.0_DS_ClientPlatform~B &lt;0.4.0_DS_ClientPlatform~B@opal.agent&gt;"
      -m "feat(ADVI_INFETL.003): inf-portal-publisher Lambda full implementation (replace STUB)"
      -- infra/aws/lambda/inf-portal-publisher/lambda_function.py
      [+ requirements.txt if dependencies added; + lambdas.tf if config updated]
    </step>
    <step>
      git push origin CLOUD.
    </step>
    <step>
      Lambda deploy: per CLAUDE.md rule 1 — Terraform is the only Lambda deployment
      mechanism. Coordinate with AE 0.7 for terraform plan + apply against
      infra/aws/terraform/inf-pipeline/. AE 0.7 owns Lambda Terraform applies.
      Verify 0-diff plan post-apply.
    </step>
    <step>
      Manual empirical: invoke Lambda directly with synthetic event:
        aws lambda invoke --function-name inf-portal-publisher \
          --payload '{"Records":[{"s3":{"bucket":{"name":"opal-data-inf"},"object":{"key":"gold/meta/pipeline-complete.json"}}}]}' \
          --cli-binary-format raw-in-base64-out /tmp/publisher_response.json
      Verify:
        - StatusCode 200
        - All 9 platinum/firm/*.json files written with fresh data_as_of timestamp
        - CW logs show no errors
        - inf-portal-advisor-publisher invoked once (CW logs of that Lambda show entry)
    </step>
    <step>
      RAVC to COO: commit hash + S3 lambda zip ETag (post AE Terraform apply) +
      lambda-source-map confirmation + manual empirical evidence (StatusCode + platinum
      file timestamps) + comp-platinum reverse output (schema-parity confirmation).
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-iam service inf-portal-publisher — confirms IAM permissions sufficient for gold S3 reads + platinum S3 writes + lambda:InvokeFunction (advisor-publisher + capture-output-versions) + cloudfront:CreateInvalidation. Flag IAM gap as separate mini-TO if found.</tool>
    <tool>comp-pipescript io inf-portal-publisher — enumerate canonical inputs + outputs (post-implementation, evidence for §5 PRD ratchet)</tool>
    <tool>comp-platinum reverse platinum/firm/* — verify portal consumers see expected schema</tool>
    <tool>comp-pii audit — verify no cleartext PII leak introduced in platinum (BD analog has clean PII audit; INF parity expected)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Lambda reads gold/canonical/* + gold/dimensions/* + gold/views/* + gold/timeseries/* without IAM gap (comp-iam clean).</criterion>
    <criterion id="AC2">Lambda emits all 9 platinum/firm/*.json files per §4.5 (header_metrics, leaderboard, timeseries_chart, clients_tab, filters/dimensions, 4× snapshots/aua_by_*).</criterion>
    <criterion id="AC3">Lambda invokes inf-portal-advisor-publisher (handler start) + inf-capture-output-versions (handler end) — TO-4 + TO-6 stubs may receive the invocations; that's acceptable for Phase 1 ship.</criterion>
    <criterion id="AC4">Platinum JSON schema validates against existing portal expected shapes (Phase 1 mandate confirms via portal smoke test gate post AE Terraform apply).</criterion>
    <criterion id="AC5">comp-pii audit clean (no cleartext PII leak introduced).</criterion>
    <criterion id="AC6">Manual empirical invoke produces StatusCode 200 + all 9 outputs with fresh data_as_of + CW logs clean.</criterion>
    <criterion id="AC7">CloudFront invalidation issued post-write (CF logs show invalidation accepted).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — TO-3 is structurally independent. TO-1 (cron) preferred to ship first so cron-fired chain produces gold for Lambda to read; not strict — manual SSM dispatch suffices for empirical validation.</upstream>
    <downstream>
      TO-4 (advisor publisher) receives Lambda-to-Lambda invocation from this TO's handler.
      TO-5 (S3 ObjectCreated rule) wires sentinel → this Lambda; cannot empirically validate until both ship.
      TO-6 (capture-output-versions) receives Lambda-to-Lambda invocation at handler end (Phase 2).
      TO-011 (cron-flip-ack) requires this Lambda functional + emitting fresh platinum.
    </downstream>
  </gates_dependencies>

  <risks_failure_modes>
    <risk>
      Schema drift: platinum/firm/*.json shape inferred from BD analog may not match
      portal expectations. Mitigation: AC4 portal smoke test BEFORE AE Terraform apply
      to PROD. If schema drift detected, RAVC pause and adjust _build_* functions.
    </risk>
    <risk>
      Lambda timeout: BD analog runs 4-6 min for ~150 advisors / 1000s of accounts.
      INF runs much smaller (4 advisors / ~700 accounts). Should complete well under
      900s. If timeout occurs, profile and either increase to 1500s OR optimize hot
      paths (parquet read parallelism).
    </risk>
    <risk>
      CloudFront invalidation fails (insufficient permissions, wrong distribution ID).
      AC7 verifies; if fails, comp-iam audit on Lambda role + correct distribution ID
      pre-commit. Distribution ID per session60 evidence: EVTSA9VEHNZVH.
    </risk>
    <risk>
      DS~B session not registered (last seen this session: deregistered after INFNNA
      leap-day fix). DS~B must restart session + watcher before this TO can be
      processed. Per fallback metadata, COO reroutes to DS~D after 1h no-pickup.
    </risk>
  </risks_failure_modes>

  <go_signal>
    <issued_at>pending Andrew confirmation of OQ1+OQ8+INFNNA-scope</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HOLD. TO authored pre-Andrew GO per CTO RAVC2 authorization. Largest TO in Phase 1 (~1.5d). DS~B fallback to DS~D after 1h no-pickup. Stub fan-out invokes acceptable at Phase 1 ship — TO-4 + TO-6 ship the real targets in parallel/follow-on.</message>
  </go_signal>
</task_order>
