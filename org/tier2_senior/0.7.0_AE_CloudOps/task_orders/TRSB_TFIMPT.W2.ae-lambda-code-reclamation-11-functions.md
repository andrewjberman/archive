<task_order>
  <metadata>
    <id>TRSB_TFIMPT.W2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <reviewer>0.3.0_DT_TradingOperations (authorizer triplet security review on `trade-auth-handler` + `trade-authorizer` + `trade-recon-authorizer`)</reviewer>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>TRSB_TFIMPT</project_code>
    <priority>P1 (Rule 1 violation — 11 Lambdas with `filename=placeholder.zip` + `ignore_changes`; code is un-reproducible from repo)</priority>
    <sla>2 days (Day 1: pull + manifest + decide per-Lambda; Day 2: reclaim 7 non-authorizer Lambdas + authorizer triplet paired with DT 0.3)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRSB_TFIMPT.md (sections 1.G2, 3.Wave 2, 6.TO-2, 7, 8.Q2+Q4)</ref>
    <ref type="protocol">docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
    <ref type="protocol">infra/aws/lambda/ci/build-and-upload.sh (S3-backed deploy pattern)</ref>
    <ref type="protocol">infra/aws/lambda/ci/lambda-source-map.json (source of truth — all 11 trade Lambdas have `source_dir: EXTERNAL`)</ref>
    <ref type="precedent_pattern">yang-pipeline S3-backed migration (yang-v2.0.0, Phases 1-4) + news + bd + market-overview (2026-04-09) — parent pattern for `source_dir: EXTERNAL` → S3-backed deploy</ref>
    <ref type="precedent_pattern">ADVI_STAUDT.HLOT2 Phase 2 smoke-gate (ast.parse + importlib exec_module) — pre-commit defense against latent NameError/ImportError, PROOF-of-concept 2026-04-21 per CTO standardization note</ref>
    <ref type="project_json">org/projects/TRSB_TFIMPT.json</ref>
    <ref type="target_files">infra/aws/terraform/trade-pipeline/{main,lambdas}.tf + infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/ (new tree) + infra/aws/lambda/ci/lambda-source-map.json</ref>
  </references>

  <objective>
    Close G2: reclaim Lambda code for all 11 trade-pipeline functions from AWS console into repo + migrate from `filename=placeholder.zip` + `ignore_changes=[filename, source_code_hash]` to S3-backed deploy via `build-and-upload.sh`. Per-function decision: (a) reclaim to repo + S3-backed, or (b) formally document as `EXTERNAL` exception in the Known Issues table. Target tag `trade-pipeline-v1.4.0`.

    Closes the comp-iam blind spot: currently `comp-iam service &lt;fn&gt;` returns "No service matching" for every trade Lambda because the `source_dir: EXTERNAL` entry in lambda-source-map.json means the compiler has no Python AST to parse for boto3 calls. Post-W2, `comp-iam service` returns a real result for every reclaimed function and `comp-iam gaps` surfaces actual gap count (up from the misleadingly-clean 1 service scanned).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/ — 11 new source trees (one per Lambda, minus any ruled option-b-exception via §8 Q2)</file>
      <file action="create">infra/aws/lambda/trade-pipeline/&lt;fn&gt;/requirements.txt — per-function Python deps (if any)</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/lambdas.tf — remove `ignore_changes` per reclaimed Lambda; swap `filename=placeholder.zip` for `s3_bucket` + `s3_key` + `source_code_hash` matching S3-backed deploy</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/main.tf:7 — remove "deployed via console/legacy scripts" comment if all 11 reclaim; OR update to cite specific option-b exceptions by name</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json — update `source_dir` for each reclaimed Lambda from `EXTERNAL` to `infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/`</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/README.md — Known Issues table: close reclaimed rows; add formal exception rows for any option-b Lambdas</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/CHANGELOG.json</file>
    </files>
    <lambda_inventory>
      Per PRD §10 + lambda-source-map.json (11 functions):
      1. trade-auth-handler — **authorizer triplet, security-critical, DT 0.3 review required**
      2. trade-authorizer — **authorizer triplet, security-critical, DT 0.3 review required**
      3. trade-dashboard-api
      4. trade-identifier-cache
      5. trade-parquet-batch-export
      6. trade-submission-handler
      7. trade-workflow-handler
      8. trade-recon-api — **§8 Q2: still in use? If dead, option-b formal exception**
      9. trade-recon-auth — **§8 Q2: still in use?**
      10. trade-recon-authorizer — **authorizer triplet + §8 Q2 intersect. Security-critical IF still live.**
      11. trade-recon-processor — **§8 Q2: still in use?**
    </lambda_inventory>
  </scope>

  <deliverables>
    <deliverable id="pull-and-manifest-phase">
      Per Lambda (×11), independently:
      1. `aws lambda get-function --function-name &lt;fn&gt; --query 'Code.Location'` → signed S3 URL → `curl -o /tmp/&lt;fn&gt;.zip &lt;url&gt;` → `unzip -d /tmp/&lt;fn&gt;-src`.
      2. `aws lambda get-function-configuration --function-name &lt;fn&gt;` — capture Runtime, Handler, Memory, Timeout, EnvVars, Role ARN, Layers (if any), VPC config, arch.
      3. Diff captured config against `trade-pipeline/lambdas.tf` for that function. Document every field-level discrepancy in manifest table.
      4. For the authorizer triplet (fn #1, #2, #10): do NOT deploy any reclaimed code until DT 0.3 completes security review. Read-only pull + manifest is fine.
    </deliverable>
    <deliverable id="per-function-decision-phase">
      Per Lambda, classify option (a) reclaim or option (b) EXTERNAL exception:
      - (a) Default for all 7 non-recon Lambdas + authorizer triplet. Reclaim source, migrate to S3-backed, remove `ignore_changes`.
      - (b) For recon quartet (fn #8-11) IF §8 Q2 confirms they're dead-path: document as formal EXTERNAL exception in Known Issues table with ownership + deprecation rationale. Do NOT remove the `aws_lambda_function` resource — it stays TF-managed-as-exception for drift detection.
      - (b) Fallback trigger: compiled/obfuscated code, third-party dependency that can't be reproduced from zip, or source that doesn't `ast.parse` clean. Document rationale per-function.
    </deliverable>
    <deliverable id="reclaim-and-deploy-phase">
      For each option-(a) Lambda:
      1. Move reclaimed source to `infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/`. Preserve directory structure from the zip.
      2. Generate `requirements.txt` from any `site-packages/*` present in the zip — if none, skip (pure-stdlib function).
      3. Pre-commit smoke-gates per HLOT2 standardization pattern: `python -c "import ast; ast.parse('src/&lt;handler_file&gt;.py').read()"` exit 0 + `python -c "importlib.util.spec_from_file_location + exec_module"` exit 0 for every Python file.
      4. Build + upload via `bash infra/aws/lambda/ci/build-and-upload.sh trade-pipeline &lt;fn&gt;` (follow existing yang/news/bd pattern).
      5. Edit `lambdas.tf` — remove `ignore_changes = [filename, source_code_hash]` block; replace `filename = "placeholder.zip"` with `s3_bucket` + `s3_key` + `source_code_hash` (per CDRS_TFIMPT partner-firms-v1.0.0 pattern).
      6. Edit `lambda-source-map.json` — `source_dir` from `EXTERNAL` to `infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/`.
      7. `terraform plan` per Lambda → expect 0-diff on source_code_hash (live zip matches reclaimed src+uploaded zip). Any drift = missed Phase 1 config diff.
      8. `terraform apply`.
    </deliverable>
    <deliverable id="authorizer-triplet-review">
      1. DT 0.3 reads reclaimed source for `trade-auth-handler` + `trade-authorizer` + `trade-recon-authorizer` (if live).
      2. DT 0.3 signs off via MCP: no backdoors / no hardcoded secrets / no unexpected grants / JWT validation logic matches docs.
      3. Deploy reclaimed authorizer code via `aws lambda publish-version` + alias swap (NOT direct `$LATEST` overwrite per PRD §3 W2 risk mitigation). Single-Lambda rollback via alias revert if smoke test 403s.
    </deliverable>
    <deliverable id="tag-and-push">
      1. Pre-tag: `git tag -l "trade-pipeline-v*" | sort -V | tail -5` — confirm next version is `v1.4.0` (after W1 `v1.3.0`).
      2. `git commit --only --author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"` with explicit paths.
      3. `git tag -a trade-pipeline-v1.4.0 -m "W2 Lambda code reclamation: &lt;N&gt;/11 reclaimed, &lt;M&gt;/11 documented-as-exception"`.
      4. `git push origin CLOUD --follow-tags`.
    </deliverable>
  </deliverables>

  <wire_contract>
    Zero runtime behavior delta expected post-reclaim.
    - First `terraform apply` deploys reclaimed code; since the source was pulled from live, `source_code_hash` should match exactly. 0-diff is the evidence.
    - Authorizer triplet: alias-swap pattern means zero downtime if the reclaimed code matches live behavior byte-for-byte. If it doesn't (Phase 1 manifest diff caught any discrepancy), fix the source before publish — do NOT deploy divergent code.
    - Option-b exceptions: zero change (code stays on AWS console path). Documentation-only update.
  </wire_contract>

  <acceptance_criteria>
    1. 11 src/ folders populated (option-a) OR formal exception rows in README.md Known Issues table (option-b). Total = 11 entries somewhere.
    2. `comp-iam service &lt;fn&gt;` returns a real result (not "No service matching") for every option-(a) reclaimed Lambda.
    3. `comp-iam gaps` runs with ≥&lt;N_option_a&gt; services scanned (up from 1); any MISSING permissions flagged and patched in iam.tf before commit.
    4. `terraform plan` 0-diff on trade-pipeline post all W2 applies.
    5. End-to-end smoke test: single test trade submission through the UI (if §8 Q4 fixture available) writes to DDB + SES email sent + workflow transitions observed in CloudWatch. Document in session log.
    6. Every reclaimed Python file passes `ast.parse` + `importlib exec_module` smoke gates (HLOT2 standardization pattern).
    7. `lambda-source-map.json` `source_dir` updated per reclaimed Lambda; CI drift-detection pipeline accepts the change.
    8. Tag `trade-pipeline-v1.4.0` exists and pushed.
    9. Authorizer triplet (fn #1 + #2 + #10 if live) has DT 0.3 MCP-sign-off captured in session log pre-deploy. `aws lambda publish-version` + alias swap used, not direct `$LATEST` overwrite.
    10. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/{DATE}/trsb_tfimpt_w2_lambda_code_reclamation.md` reproducing every `<run>` + observed-result + pass/fail vs `<expect>`.
    11. MCP COMPLETE to COO with: per-Lambda decision table (option-a or option-b + rationale), commit hash, tag, smoke evidence, `comp-iam gaps` output, authorizer triplet DT 0.3 sign-off thread.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>For each of the 11 trade Lambdas: `aws lambda get-function --function-name &lt;fn&gt;` + `aws lambda get-function-configuration --function-name &lt;fn&gt;`</run>
        <expect>Code.Location S3 URL returned + full config captured. Diff captured config against `trade-pipeline/lambdas.tf` for each function — document every field discrepancy in a manifest table (Runtime/Handler/Memory/Timeout/EnvVars/Role/Layers/VPC/arch).</expect>
        <if_mismatch>If any function returns ResourceNotFoundException, the source map is stale — surface to COO before proceeding (may indicate a Lambda was deleted between PRD and execution).</if_mismatch>
      </step>
      <step>
        <run>For each Lambda: unzip Code.Location zip + `comp-iam service &lt;fn&gt;` (BEFORE reclamation)</run>
        <expect>Pre-reclaim baseline: "No service matching '&lt;fn&gt;'" for all 11 (per PRD §2 evidence). Unzipped source lives at `/tmp/&lt;fn&gt;-src/`.</expect>
        <if_mismatch>If comp-iam returns a real result for any Lambda pre-reclaim, the compiler graph has been updated out-of-band — audit order-of-operations with COO.</if_mismatch>
      </step>
      <step>
        <run>**DORMANCY MATRIX — all 11 trade Lambdas** (widened per TRSB_TFIMPT.W1 dormancy finding 2026-04-21, CTO concur 20260421T130116Z). Per function: `aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations --dimensions Name=FunctionName,Value=&lt;fn&gt; --start-time $(date -u -d '90 days ago' +%FT%T) --end-time $(date -u +%FT%T) --period 86400 --statistics Sum` + repeat with 30-day window + `aws logs filter-log-events --log-group-name /aws/lambda/&lt;fn&gt; --start-time $(date -d '30 days ago' +%s)000 --max-items 5` for invocation-content spot-check. **+ API GW method-level triangulation (CTO suggest 20260421T130453Z):** after W3 Phase 0 surfaces the trade REST API ID + method arns, pull `aws cloudwatch get-metric-statistics --namespace AWS/ApiGateway --metric-name Count --dimensions Name=ApiName,Value=&lt;api&gt; Name=Method,Value=POST Name=Resource,Value=/trades/submit Name=Stage,Value=&lt;stage&gt;` for matching time windows. Orphan-method signal: API GW method Count &gt; 0 AND Lambda Invocations = 0 = integration-error-before-Lambda (a 4th disposition bucket beyond the three-way bucketing). Low-cost one-shot CloudWatch call; high value for Andrew flag evidence.</run>
        <expect>§8 Q2 answer evidence widened from recon quartet to full 11. W1 already established trade-submission-handler has 0 invocations/30d — expect ≥1 more Lambda to show same (reality-matches-priors check). Surface full 11×2-window dormancy matrix: fn + 30d Sum + 90d Sum + last-invocation-ts + option-a-or-b recommendation per Lambda.</expect>
        <if_mismatch>If 5+/11 are dormant, flag to COO + CTO as PRD-framing question — option-b scaling from 4 to 8+ Lambdas is qualitatively different rollout (candidate for consolidated "TRSB deprecation assessment" TO as PRD amendment per CTO 20260421T130116Z). Do NOT self-amend PRD; surface + wait.</if_mismatch>
      </step>
      <step>
        <run>For test fixture (§8 Q4): `aws ses list-configuration-sets` + `aws ses list-identities` + grep repo for `trades@opalinvest.dev` sender</run>
        <expect>Either (a) a documented synthetic-trade test fixture route exists (likely under test/ or scripts/ or docs/), or (b) no such fixture exists — need to build one before W2 smoke-test acceptance can fire.</expect>
        <if_mismatch>If no fixture exists, surface to COO — W2 smoke test becomes blocked on fixture authoring. Andrew §8 Q4 answer drives scope.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>For every reclaimed Python file: `python -c "import ast; ast.parse(open(PATH).read())"` AND `python -c "import importlib.util; spec=importlib.util.spec_from_file_location(NAME, PATH); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)"` — both exit 0</run>
        <expect>HLOT2 standardization pattern (pattern established 2026-04-21 per CTO). Catches latent NameError / missing import / circular import / top-level ImportError before commit. Every reclaimed file passes both.</expect>
        <if_mismatch>STOP. Fix missing imports / syntax errors before commit. Do NOT upload to S3 with failed gates — same-class failure mode as 081223b5 / 048a6fa3.</if_mismatch>
      </step>
      <step>
        <run>For every option-(a) Lambda: `comp-iam service &lt;fn&gt;` (AFTER reclamation, BEFORE commit)</run>
        <expect>Now returns a real result — boto3 calls enumerated from the reclaimed source. Compare against `iam.tf` allow-list for that Lambda's role. MISSING flag = patch iam.tf before commit.</expect>
        <if_mismatch>If MISSING appears, do NOT commit Lambda reclamation without also committing the iam.tf patch — else production IAM becomes narrower than runtime needs on first deploy.</if_mismatch>
      </step>
      <step>
        <run>`comp-iam gaps`</run>
        <expect>Services-scanned count increases proportionally to option-(a) Lambdas reclaimed. Overall "No permission gaps detected" after any iam.tf patches land. This is the authoritative post-W2 gap-surface audit.</expect>
        <if_mismatch>Any gap surfacing = patch iam.tf before commit. Do NOT ship partial coverage.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>Per reclaimed Lambda: `source_code_hash` 0-diff (reclaimed zip matches live). `ignore_changes` block removed. `filename=placeholder.zip` replaced with `s3_bucket`+`s3_key`. Any drift = Phase 1 manifest diff was missed.</expect>
        <if_mismatch>If source_code_hash diffs, the reclaimed zip and live don't match — investigate before apply. Common causes: ZIP timestamp variance, .pyc files in live zip but not reclaimed, requirements install added vendored deps.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>terraform plan</run>
        <expect>0-diff across trade-pipeline state post-W2 apply(s).</expect>
        <if_mismatch>Post-apply drift = incomplete reclaim on at least one Lambda. STOP, capture, surface to COO; do NOT tag or mark complete.</if_mismatch>
      </step>
      <step>
        <run>End-to-end smoke test per §8 Q4 fixture decision</run>
        <expect>Single test trade submit → UI → trade-submission-handler → opal-trade-submissions DDB write → SES email → workflow state transitions (Approvals → Execution → History). CloudWatch trace captures authorizer + handler + DDB write. No 403s, no 500s.</expect>
        <if_mismatch>If authorizer triplet returns 403 post-alias-swap, revert the alias. If trade-submission-handler 500s, check for missing `requirements.txt` vendored deps in the reclaimed zip. Full rollback via `terraform apply` with prior `source_code_hash` if needed.</if_mismatch>
      </step>
      <step>
        <run>`comp-iam service` per option-(a) Lambda + `comp-iam gaps` (global)</run>
        <expect>All 11 option-(a) Lambdas indexed; `comp-iam gaps` clean with expected N_option_a services scanned. If N_option_b > 0, document the gap in Known Issues with explicit ownership.</expect>
        <if_mismatch>Gap surfacing post-apply = iam.tf is insufficient for real runtime usage. Open a fast-follow patch TO.</if_mismatch>
      </step>
      <step>
        <run>comp-routes trace trade-submission-handler</run>
        <expect>Still empty (W3 gap — API GW not yet in TF). This is expected; W3 closes it.</expect>
        <if_mismatch>If result appears, W3 may have shipped concurrently — reconcile.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>**Authorizer triplet (fn #1 + #2 + #10)** requires 0.3.0_DT_TradingOperations security review before deploy. Security-critical gate — mis-deploy means every trade request 403s. DT 0.3 must MCP-sign-off BEFORE `aws lambda publish-version` fires. Deploy pattern: `publish-version` + alias swap, NOT direct `$LATEST` overwrite.</item>
    <item>**Recon quartet (fn #8-11)** decision gates on Andrew §8 Q2 answer + Phase 1 log-activity probe. Until Q2 answered, work on the 7 non-recon Lambdas (fn #3-7) + authorizer triplet — recon stays parked.</item>
    <item>**Smoke test fixture** gates on Andrew §8 Q4 answer. If fixture exists, use it. If not, W2 closeout blocked until fixture built (may need separate TO or scope add).</item>
    <item>No AE 0.6 / BD pipeline conflict. W2 touches trade-pipeline state file + trade-pipeline Lambda src, fully orthogonal to BD pipeline work.</item>
    <item>No portal CF touch. W3 will add CF behaviors; W2 does not.</item>
    <item>Tag series: `trade-pipeline-v1.4.0` (after W1 `v1.3.0`). Verify via `git tag -l "trade-pipeline-v*" | sort -V | tail -5` pre-tag.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="W2 status flip staged→pending" status="pending">
      Gates on BOTH: (a) W1 completion (convention, not hard-technical), (b) Andrew §8 Q2 answer (recon quartet live-or-dead), (c) Andrew §8 Q4 answer (smoke-test fixture availability). COO collects all 3 before flipping.
    </dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="TRSB_TFIMPT.W1 complete" status="pending">
      W1 provides trade-pipeline-v1.3.0 baseline. W2 doesn't technically require W1's DDB import, but strict ordering per PRD §3.
    </dependency>
  </dependencies>

  <open_questions_gating_pending>
    <q id="§8-Q2-widened">**Widened 2026-04-21 per TRSB_TFIMPT.W1 dormancy finding (CTO 20260421T130116Z).** Originally scoped to recon quartet only (trade-recon-api/auth/authorizer/processor). W1 Phase 1 probe found trade-submission-handler is ALSO dormant (0 invocations/30d) — widens the question to "which of ALL 11 trade Lambdas have any invocations in 30/90d windows". Evidence-first: Phase 1 CloudWatch probe surfaces full 11×2-window dormancy matrix; Andrew's Q2 answer THEN decides reclamation (option-a) vs formal-exception (option-b) per Lambda. If 5+/11 dormant, PRD-framing revisit (consolidated "TRSB deprecation assessment" candidate).</q>
    <q id="§8-Q4">Smoke-test fixture for single synthetic trade — does one exist, or does W2 need to build one first? Blocks §acceptance_criteria L5. Note: widened Q2 may make this moot for option-b Lambdas; only option-a reclaim functions need fixture-based smoke.</q>
  </open_questions_gating_pending>

  <next>On §8 Q2+Q4 answered AND W1 complete: COO flips this TO staged→pending + dispatches GO MCP. On AE commit + tag + push: MCP COMPLETE to COO with per-Lambda decision table + Phase 1 probes + smoke evidence + authorizer triplet DT 0.3 sign-off. Then W3 unblocked (still gated on DT 0.4 CloudFront MCP).</next>
</task_order>
