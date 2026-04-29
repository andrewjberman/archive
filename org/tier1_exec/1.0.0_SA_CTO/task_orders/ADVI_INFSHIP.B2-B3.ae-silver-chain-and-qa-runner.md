<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-28-infship-b2b3-silver-chain-and-qa-runner</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL~B</issued_to>
    <date>2026-04-28</date>
    <status>complete</status><!-- AE 0.6.1~B 2026-04-28: shipped ab5ccadf (B2 inf-silver-chain Lambda + S3 EventBridge sentinel) + 5028c3ec + ed69c66a (B3 inf-gold-qa-runner EC2 c6a.2xlarge + IAM platinum-DENY, inf-pipeline-v1.6.1) + 48baf414 apply + B3-DEP-1/2 cascade (2e9bf29d + a7431486 + 28018d36 + 50d133c8); session log 5189492f. Reconciled 2026-04-29 startup. -->
    <project_code>ADVI_INFSHIP</project_code>
    <to_serial>B2-B3</to_serial>
    <priority>HIGH</priority>
    <prd>docs/architecture/ADVI_INFSHIP.md (Phase 1.5 Infrastructure formalization sub-wave)</prd>
    <note>Combined TO: B2 (silver chain) + B3 (gold-qa-runner) folded since same owner. Per Andrew pace push 12:50Z.</note>
  </metadata>

  <objective>
    Two paired infrastructure deliverables for inf-pipeline:

    **B2 — inf-silver-chain Lambda:** Triggered post-bronze (S3 ObjectCreated
    on `bronze/orion-api/{date}/` prefix OR sequenced by inf-bronze-runner
    boot script). Runs `data/orion/scripts/silver/build_*_dim.py` chain for
    all 9 dims, lands `silver/api_dims/{dim}/snapshot_date={date}/data.parquet`.
    Reuses DS~A's `_orion_api_silver_lib.py` envelope.

    **B3 — inf-gold-qa-runner formalization:** Separate EC2 instance (or
    mode of inf-gold-layer-runner) for QA-runner role. Same code path as
    PROD gold runner; outputs to `qa/` prefix instead of `platinum/`.
    Triggered manually by DS or post-silver via boot script. Resolves
    DS~B's pain point this session (had to local-exec for D2/D3 because
    inf-gold-qa-runner does not exist).

    Path X architecture: single low-volume design vs BD per-domain.
  </objective>

  <context>
    Andrew direct ~06:15Z (via COO): bronze/silver/QA runner formalization
    per BD pattern, manual API approach. Andrew direct ~12:50Z: pace push
    — AE 0.6.1~B waiting on B2/B3.

    **Existing infrastructure to reuse:**
    - inf-jwt-trigger Lambda (ORIAPI.003 v1.5.8) — dispatch primitive
    - inf-bronze-runner EC2 (B1, AE 0.7.0~B in flight) — bronze landing source
    - inf-gold-layer-runner EC2 (currently STOPPED; existing PROD instance)
    - bd-pipeline silver chain pattern (`bd_*_pipeline` Lambdas + cron)
    - DS~A's `_orion_api_silver_lib.py` shared envelope (consumed by all 9 silver builders)
    - DS pull scripts at `data/orion/scripts/silver/build_*_dim.py`

    **9 dims (per INFSHIP.B4 catalog ETA 1-2h, df4b3f86):**
    household / performance / activity / billing / tax_unrealized /
    tax_realized / assets (Path C) / accounts_v2 / transactions

    **DS~B local-exec pain point (this session):** had to bypass missing
    inf-gold-qa-runner by running publishers via workspace boto3. Worked
    for v1 ship but not sustainable for nightly cadence. B3 closes that gap.

    **JWT cache path:** AE 0.6.1~B is canonical owner; coordinate with B1
    AE 0.7.0~B on read path.
  </context>

  <files_to_modify>
    <file action="create">infra/aws/terraform/inf-pipeline/inf-silver-chain.tf</file>
    <file action="create">infra/aws/lambda/inf-silver-chain/handler.py</file>
    <file action="create">infra/aws/lambda/inf-silver-chain/requirements.txt</file>
    <file action="modify">infra/aws/lambda/ci/lambda-source-map.json (register inf-silver-chain per CLAUDE.md rule 4)</file>
    <file action="create">infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf (B3)</file>
    <file action="modify">infra/aws/ec2/EC2_MANIFEST.json (register inf-gold-qa-runner per CLAUDE.md rule 8)</file>
    <file action="create">infra/aws/ec2/inf-gold-qa-runner/userdata.sh (or extend layer-runner pattern)</file>
  </files_to_modify>

  <spec_summary>
    ## B2 — inf-silver-chain Lambda

    **Trigger (RATIFIED COO 14:05Z post AE 0.6.1~B catch):** S3 EventBridge
    rule on `s3://opal-data-inf/bronze/orion-api/{date}/_BRONZE_COMPLETE.json`
    ObjectCreated. inf-bronze-runner orchestrator writes the sentinel as
    its final step. Lambda fires once per cron run; reads `{date}` from
    sentinel content + bucket prefix. Single invocation runs all 9 silver
    builders sequentially.

    **Why sentinel pattern over direct invoke:** B1's IAM is scoped to
    bronze write only (no Lambda invoke). Sentinel pattern preserves B1
    IAM minimalism while giving B2 unambiguous chain-complete trigger.
    Per-dim ObjectCreated would fire 9 Lambdas; sentinel fires once.

    **Lambda runtime:** Python 3.12 (latest supported), 1024 MB memory,
    900s timeout (15 min). Sufficient for 9 sequential silver builds at
    ~30-60s each.

    **handler.py:**
    ```python
    def handler(event, context):
        date = event['date']
        for builder in SILVER_BUILDERS:  # ordered list per B4 §5
            try:
                run_silver_builder(builder, date)
            except Exception as e:
                log_error(builder, e)
                # continue to next builder; partial silver > no silver
        emit_completion_status(date, results)
    ```

    Each `run_silver_builder` invokes the corresponding
    `data/orion/scripts/silver/build_{dim}_dim.py` function in-process
    (script imports + main() call, not subprocess — keeps Lambda warm and
    avoids cold-start per builder).

    **IAM:**
    - s3:GetObject on bronze/orion-api/* (read bronze CSVs)
    - s3:PutObject on silver/api_dims/* (write silver parquets)
    - logs:* (CloudWatch)
    NO bronze write, NO platinum write, NO Lambda invoke.

    **Deps in Layer:** Existing or new layer with pandas + pyarrow + boto3 +
    s3fs. Reuse `news-trending-deps:2` if compatible (Python 3.12); else
    create `inf-silver-deps:1` per CLAUDE.md rule 3 (Lambda Layers, not
    inline pip).

    ## B3 — inf-gold-qa-runner

    **Sizing:** Same as inf-gold-layer-runner (mirror the existing PROD
    instance — t3.medium or whatever PROD uses). Spot OK.

    **Behavior:** Same orchestrator code as PROD layer-runner but with
    env var `OUTPUT_PREFIX=qa/` instead of `platinum/`. Identical compute,
    different write path. This guarantees QA = PROD parity.

    **Trigger:** Two paths:
    1. **Manual:** DS dispatches via `aws ssm send-command` with parameter
       `qa-run` and date arg. Lambda mode_marker `gold_qa_run` triggers
       the EC2 boot.
    2. **Post-silver auto:** B2 silver chain Lambda fires inf-jwt-trigger
       with mode_marker `gold_qa_run` after silver completes. Optional
       wiring; default to manual for v1 (per Andrew "ship simple first").

    **IAM:** Mirror layer-runner role + scope writes to `qa/` prefix only
    (cannot accidentally write to `platinum/`).

    **Manifest registration:** Add `inf-gold-qa-runner` row to
    EC2_MANIFEST.json.

    ## Sequence + dispatch

    1. B2 silver chain Lambda authored + deployed → standing ready
    2. B1 inf-bronze-runner ships (AE 0.7.0~B) → orchestrator.py adds
       silver-chain Lambda invoke at end of bronze chain → end-to-end test
       (bronze pull → silver build → all 9 silver parquets land)
    3. B3 inf-gold-qa-runner ships → manual dispatch test (DS triggers,
       gold runs against silver, qa/ prefix populated, validate matches
       prior platinum/) → DS QA-pass workflow formalized
    4. Production cutover: nightly cron triggers full chain (bronze →
       silver → optional gold-qa for spot-checks; platinum gold separately)

    ## Coordination flags

    - JWT cache path: confirm with AE 0.7.0~B (B1) before finalizing
    - L5 ORIAPI work (in flight, ~2-3h): the chained bronze pulls in L5
      may overlap with B1 orchestrator scope. Sync with AE 0.7.0~B to
      avoid duplicate work — L5 may BE the bronze runner code, in which
      case B1 just wraps it in EC2 + cron infra.
    - DS~B local-exec workaround: deprecate after B3 ships. DS~B should
      use inf-gold-qa-runner SSM dispatch instead of workspace boto3.
  </spec_summary>

  <acceptance_criteria>
    <ac>1. B2: Lambda deployed via TF (CLAUDE.md rule 1, no aws cli code
        push). Source-map registered (rule 4). Layer dep handled
        properly (rule 3). Memory + timeout sized for 9 builders (rule 5).</ac>
    <ac>2. B2: End-to-end test — invoke Lambda with `{'date': '2026-04-28'}`
        and verify all 9 silver parquets land at expected S3 keys with
        non-zero row counts.</ac>
    <ac>3. B2: Per-builder failure does NOT abort chain (validated via
        injected failure on one builder).</ac>
    <ac>4. B3: EC2 registered in EC2_MANIFEST.json. TF applied 0-diff
        (rule 1). Tag `inf-pipeline-vX.Y.Z` per pipeline tag rule.</ac>
    <ac>5. B3: Boot test — manual SSM dispatch fires Lambda, EC2 starts,
        gold runs against silver/api_dims/, writes to qa/ prefix only,
        self-shutdown.</ac>
    <ac>6. B3: QA output spot-check — qa/firm/header_metrics.json matches
        platinum/firm/header_metrics.json byte-for-byte (or with documented
        diff if PROD silver is older than QA silver).</ac>
    <ac>7. RAVC4 to CTO: Lambda ARN + layer ref, EC2 instance ID, both
        boot-test timestamps, S3 evidence, CloudWatch log samples, cost
        projection. CC COO + DS~A (B4 doc author) + AE 0.7.0~B (B1 partner).</ac>
  </acceptance_criteria>

  <gates_and_dependencies>
    <gates>
      INFSHIP.B4 (DS~A 9-dim spec doc) — provides authoritative SILVER_BUILDERS
      sequence. B2 can BEGIN with preliminary list (same order as B1's
      preliminary); SILVER_BUILDERS updates when B4 lands.

      INFSHIP.B1 (AE 0.7.0~B inf-bronze-runner EC2) — provides bronze landing.
      B2 silver chain Lambda technically can deploy + test before B1 ships
      (test invocations bypass the trigger), but END-TO-END test of trigger
      path requires B1 in place.

      L5 (your in-flight ORIAPI bronze ingestion) — coordinate with
      AE 0.7.0~B on B1 to avoid duplicate orchestrator code. L5 may
      simplify B1 if your code is reusable.
    </gates>
    <unblocks>
      DS~B's local-exec workaround deprecation (post-B3 ship).
      Nightly autonomous Inflection pipeline (post-B1+B2+B3 ship cycle).
      INFSHIP Phase 3 V1 RD smoke validation (uses qa/ outputs from B3).
    </unblocks>
  </gates_and_dependencies>

  <coordination>
    - AE 0.7.0~B (B1): JWT cache path + bronze chain sequencing + Lambda
      invoke handoff at end of orchestrator.py
    - DS~A: SILVER_BUILDERS sequence (per B4 doc, in flight)
    - DS~B: deprecate local-exec workaround once B3 ships (separate MCP
      after RAVC4)
    - DS~D: assets silver builder (Path C); confirm no special args needed
      for canonical-source mode
    - DT: TF deployment per CLAUDE.md rule 1; Lambda Layer per rule 3
  </coordination>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 single message covering both B2 + B3 ship — Lambda
        ARN + EC2 instance ID + both boot-test timestamps + S3 evidence +
        CloudWatch logs + cost projection. CC COO + DS~A + AE 0.7.0~B.</on_complete>
  </ravc_target>

  <estimated_effort>
    B2: 2-4 hours (Lambda + handler + layer + TF + tests)
    B3: 2-4 hours (EC2 + TF + boot script + manifest + boot test + QA spot-check)
    Total: 4-8 hours combined; can be 1 session if streamlined or 2 if
    blocked on L5 coordination.
  </estimated_effort>
</task_order>
