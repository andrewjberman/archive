<task_order>
  <metadata>
    <id>TRSB_TFIMPT.W2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <co_owner>0.5.0_AE_OpalETL (joint Phase 0 discovery + SES packet — both AEs required, see §rescope_2026-04-21)</co_owner>
    <reviewer>0.3.0_DT_TradingOperations (authorizer triplet security review on `trade-auth-handler` + `trade-authorizer` + `trade-recon-authorizer` IF Phase 0 classifies any as active)</reviewer>
    <date>2026-04-21</date>
    <rescoped>2026-04-21 (was: single-AE binary Q2/Q4 gate)</rescoped>
    <status>complete</status><!-- 2026-04-24: W2 Phase 0 + Phase 1 BOTH SHIPPED. Joint COO+CTO Option X signoff (CTO 20260424T150159Z + 150240Z; COO 20260424T150221Z + 150436Z + 152740Z RAVC4 ACK). Phase 0 docs: 54efb540 brief + 521b8c26 SES packet. Phase 1 ship: AE 0.7 abfed84d source + 71be8a7e lambdas.tf + e11151d5 smoke/README + 14b3b501 log. SES infra: AE 0.5 15a048e6 (config set + bounce/complaint SNS). Tag trade-pipeline-v1.4.0 pushed. 9 option-(b) exceptions in trade-pipeline/README.md Known Issues. Carry-forward (non-blocking): Andrew SES Console prod-access submission, 9-COLD deprecation assessment standing-backlog (CTO-flagged), EMAIL_FROM source/env mismatch on trade-submission-handler, 4 failed SES identities. Phase 0 Section A "missing layers block" was a false-positive — layers always present at lambdas.tf:136-138; CTO Condition #1 moot, Phase 1 still landed clean. -->
    <project_code>TRSB_TFIMPT</project_code>
    <priority>P1 (Rule 1 violation — 11 Lambdas with `filename=placeholder.zip` + `ignore_changes`; code is un-reproducible from repo) — plus SES sandbox→prod readiness folded in (trade pipeline depends on SES for client notifications; same operational cluster)</priority>
    <sla>2 days — Day 1 Phase 0 joint discovery (both AEs) + SES packet, Day 2 actionable outcome based on Phase 0 findings (reclaim vs formal exception) + authorizer triplet paired with DT 0.3 if any triplet member is live</sla>
  </metadata>

  <rescope_2026-04-21>
    Per Andrew 5-item walkthrough 2026-04-21 PM (CTO session log `org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md` §3, commit `0a37d545`):

    **Old scope (REMOVED):** binary gate on Andrew answering §8 Q2 (recon quartet live-or-dead) + §8 Q4 (smoke-test fixture availability) before W2 could flip staged→pending.

    **New scope (THIS REVISION):** joint 0.5.0_AE_OpalETL + 0.7.0_AE_CloudOps Phase 0 discovery. Andrew's rationale: "hard to say what is best approach without a better understanding of what is there." AEs walk the 11-Lambda surface themselves, inventory what's there, and return with an informed W2 proposal. SES sandbox→prod readiness packet folded into the same segment (same operational cluster — trade pipeline depends on SES for client notifications; item #5 from the 5-item list rolled in).

    **Why joint AE:** Neither 0.5.0 (OpalETL) nor 0.7.0 (CloudOps) alone has full context. 0.7 owns infra (Terraform, IAM, API GW); 0.5 owns the broader ETL pattern library (SES identity verification came up during partner-etl work).

    **Un-gate the staged→pending flip:** no longer gated on Andrew answers. COO flips staged→pending as soon as both AEs ACK joint engagement.
  </rescope_2026-04-21>

  <references>
    <ref type="prd">docs/architecture/TRSB_TFIMPT.md (sections 1.G2, 3.Wave 2, 6.TO-2, 7)</ref>
    <ref type="decision_record">org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md §3 (+ §5 SES folded in)</ref>
    <ref type="protocol">docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
    <ref type="protocol">infra/aws/lambda/ci/build-and-upload.sh (S3-backed deploy pattern)</ref>
    <ref type="protocol">infra/aws/lambda/ci/lambda-source-map.json (source of truth — all 11 trade Lambdas currently have `source_dir: EXTERNAL`)</ref>
    <ref type="precedent_pattern">yang-pipeline S3-backed migration (yang-v2.0.0, Phases 1-4) + news + bd + market-overview (2026-04-09) — parent pattern for `source_dir: EXTERNAL` → S3-backed deploy</ref>
    <ref type="precedent_pattern">ADVI_STAUDT.HLOT2 Phase 2 smoke-gate (ast.parse + importlib exec_module) — pre-commit defense against latent NameError/ImportError, standardized 2026-04-21</ref>
    <ref type="project_json">org/projects/TRSB_TFIMPT.json (rescope captured `0a37d545`)</ref>
    <ref type="target_files">infra/aws/terraform/trade-pipeline/{main,lambdas}.tf + infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/ (new tree, per reclaimed Lambda) + infra/aws/lambda/ci/lambda-source-map.json</ref>
  </references>

  <objective>
    **Phase 0 (joint AE discovery — both AEs, combined deliverable):**
    Walk the 11-Lambda trade-pipeline surface + SES sandbox→prod readiness in one discovery segment. Produce a single combined report: (a) per-Lambda fixture/invocation/dormancy inventory, (b) smoke-test build-vs-skip recommendation with evidence, (c) Console-ready SES packet Andrew can copy-paste into AWS Console.

    **Phase 1 (on AE+CTO signoff of Phase 0 report):**
    Execute the per-Lambda decision plan produced by Phase 0 — option (a) reclaim source + migrate to S3-backed, or option (b) formal EXTERNAL exception. Closes G2. Target tag `trade-pipeline-v1.4.0`.

    Closes the comp-iam blind spot: currently `comp-iam service &lt;fn&gt;` returns "No service matching" for every trade Lambda because `source_dir: EXTERNAL` means the compiler has no Python AST to parse for boto3 calls. Post-W2, `comp-iam service` returns a real result for every option-(a) reclaimed function and `comp-iam gaps` surfaces the actual gap count.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/ — per-Lambda source trees for every option-(a) reclaim (decided in Phase 0)</file>
      <file action="create">infra/aws/lambda/trade-pipeline/&lt;fn&gt;/requirements.txt — per-function Python deps (if any)</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/lambdas.tf — remove `ignore_changes` + swap `filename=placeholder.zip` for `s3_bucket` + `s3_key` + `source_code_hash` per reclaim</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/main.tf:7 — remove "deployed via console/legacy scripts" comment if all 11 reclaim; OR update to cite specific option-b exceptions by name</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json — update `source_dir` for each reclaimed Lambda from `EXTERNAL` to `infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/`</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/README.md — Known Issues table: close reclaimed rows; add formal exception rows for any option-(b) Lambdas</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/CHANGELOG.json</file>
      <file action="create">infra/aws/ses/trade-pipeline-prod-access-request.md — Console-ready SES packet (use-case, daily volume, compliance language, DKIM/SPF status per identity) for Andrew to paste into AWS Console</file>
    </files>
    <lambda_inventory>
      Per PRD §10 + lambda-source-map.json (11 functions):
      1. trade-auth-handler — authorizer triplet, security-critical if active
      2. trade-authorizer — authorizer triplet, security-critical if active
      3. trade-dashboard-api
      4. trade-identifier-cache
      5. trade-parquet-batch-export
      6. trade-submission-handler — W1 Phase 1 already established 0 invocations/30d (dormant candidate)
      7. trade-workflow-handler
      8. trade-recon-api
      9. trade-recon-auth
      10. trade-recon-authorizer — authorizer triplet + recon-quartet intersect
      11. trade-recon-processor
    </lambda_inventory>
  </scope>

  <deliverables>
    <deliverable id="phase-0-joint-discovery">
      **Joint 0.5.0_AE_OpalETL + 0.7.0_AE_CloudOps** produce ONE combined Phase 0 report:

      **A. Per-Lambda surface walk (11 functions):**
        1. `aws lambda get-function --function-name &lt;fn&gt; --query 'Code.Location'` → signed S3 URL → `curl -o /tmp/&lt;fn&gt;.zip &lt;url&gt;` → `unzip -d /tmp/&lt;fn&gt;-src`.
        2. `aws lambda get-function-configuration --function-name &lt;fn&gt;` — capture Runtime, Handler, Memory, Timeout, EnvVars, Role ARN, Layers, VPC, arch.
        3. Diff captured config against `trade-pipeline/lambdas.tf` for that function. Document every field-level discrepancy.
        4. Spot-check reclaimed source for obvious red flags (hardcoded secrets, compiled/obfuscated, missing top-level imports).

      **B. Dormancy matrix (full 11 × 2 windows):**
        Per function: `aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations --dimensions Name=FunctionName,Value=&lt;fn&gt; --start-time $(date -u -d '90 days ago' +%FT%T) --end-time $(date -u +%FT%T) --period 86400 --statistics Sum` + repeat with 30-day window + last-invocation timestamp via `aws logs filter-log-events` spot-check. Classify: ACTIVE (non-zero 30d invocations), DORMANT (0 invocations in 30d but non-zero in 90d), COLD (0 invocations in 90d).

      **C. API Gateway method-level triangulation:**
        For the trade REST API: `aws cloudwatch get-metric-statistics --namespace AWS/ApiGateway --metric-name Count --dimensions Name=ApiName,Value=&lt;api&gt; Name=Method,Value=POST Name=Resource,Value=/trades/submit Name=Stage,Value=&lt;stage&gt;` for 30d + 90d windows. Orphan-method signal: API GW method Count > 0 AND matching Lambda Invocations = 0 = integration-error-before-Lambda (a 4th disposition bucket).

      **D. Smoke-test build-vs-skip recommendation:**
        Inventory existing synthetic-trade fixture: check `tests/`, partner docs, prod submission samples for existing golden-path trade JSON. Grep repo for `trades@opalinvest.dev` or similar test-trade sender. Recommend:
        - If fixture exists → smoke-test is feasible in Phase 1; use it for acceptance.
        - If no fixture AND ≥1 option-(a) Lambda is active → recommend building a minimal fixture as part of Phase 1 (or as a micro-follow-up TO).
        - If no fixture AND all option-(a) Lambdas are dormant → smoke-test is moot; acceptance shifts to `terraform plan` 0-diff + smoke gates only.

      **E. Per-Lambda option recommendation:**
        For each of the 11 Lambdas, recommend option-(a) reclaim or option-(b) formal EXTERNAL exception based on dormancy + code-reclaim-feasibility. If 5+/11 recommend option-(b), FLAG to COO + CTO as candidate for consolidated "TRSB deprecation assessment" PRD amendment (qualitatively different rollout).

      **F. Combined report lives at:** `infra/aws/ses/trade-pipeline-prod-access-request.md` for the SES packet AND `docs/briefs/trsb_tfimpt_w2_phase0_discovery.md` for the dormancy/reclamation plan. AEs MCP COO with both report paths + option-disposition table.
    </deliverable>

    <deliverable id="ses-sandbox-to-prod-packet">
      **Single file: `infra/aws/ses/trade-pipeline-prod-access-request.md`** — Console-ready for Andrew to copy-paste into the AWS SES production-access-request form:

      - **Use-case description (1-2 paragraphs):** who we are, what trade-pipeline notifications do, why production access is needed (sandbox limits outbound to verified identities, blocks real client notification flow).
      - **Daily volume estimate:** per-trade-notification transactional email count (best-available estimate based on current or projected trade throughput). Break down by notification type (submission ack, approval, execution, rejection) if meaningful.
      - **Compliance attestation language:**
        - Bounce rate mitigation (suppression list handling, invalid-address scrubbing pre-send)
        - Complaint rate handling (unsubscribe flow, complaint feedback loop subscription)
        - Unsubscribe handling (link in every transactional email? only where required by jurisdiction? per trade-pipeline design)
      - **DKIM/SPF verification status per SES identity:** `aws ses list-identities` + `aws ses get-identity-verification-attributes` + `aws ses get-identity-dkim-attributes`. Report per-identity status (Verified / Pending / Failed).
      - **Identity list requested for production:** specific SES identities the request covers (likely `trades@opalinvest.com` or similar — AEs identify from `aws ses list-identities`).
      - **Content readiness:** packet is in plain markdown, Console-form-ready. Andrew pastes directly; no reformatting.
    </deliverable>

    <deliverable id="phase-1-reclaim-and-deploy">
      **Gated on AE+CTO signoff of Phase 0 report.**

      Per option-(a) Lambda:
      1. Move reclaimed source to `infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/`. Preserve directory structure from the zip.
      2. Generate `requirements.txt` from any `site-packages/*` present in the zip — if none, skip (pure-stdlib function).
      3. Pre-commit smoke-gates per HLOT2 standardization: `python -c "import ast; ast.parse('src/&lt;handler_file&gt;.py').read()"` exit 0 + `python -c "importlib.util.spec_from_file_location + exec_module"` exit 0 for every Python file.
      4. Build + upload via `bash infra/aws/lambda/ci/build-and-upload.sh trade-pipeline &lt;fn&gt;` (follow existing yang/news/bd pattern).
      5. Edit `lambdas.tf` — remove `ignore_changes = [filename, source_code_hash]`; replace `filename = "placeholder.zip"` with `s3_bucket` + `s3_key` + `source_code_hash` (CDRS_TFIMPT partner-firms-v1.0.0 pattern).
      6. Edit `lambda-source-map.json` — `source_dir` EXTERNAL → `infra/aws/lambda/trade-pipeline/&lt;fn&gt;/src/`.
      7. `terraform plan` per Lambda → expect 0-diff on source_code_hash. Drift = missed Phase 0 config diff.
      8. `terraform apply`.

      Per option-(b) Lambda: document as formal EXTERNAL exception in `infra/aws/terraform/trade-pipeline/README.md` Known Issues table. Retain `aws_lambda_function` resource as TF-managed-exception (not removed). Document ownership + deprecation rationale per function.
    </deliverable>

    <deliverable id="authorizer-triplet-review">
      IF Phase 0 classifies any of {trade-auth-handler, trade-authorizer, trade-recon-authorizer} as ACTIVE:
      1. DT 0.3 reads reclaimed source for each active authorizer.
      2. DT 0.3 signs off via MCP: no backdoors / no hardcoded secrets / no unexpected grants / JWT validation logic matches docs.
      3. Deploy reclaimed authorizer code via `aws lambda publish-version` + alias swap (NOT direct `$LATEST` overwrite per PRD §3 W2 risk mitigation). Single-Lambda rollback via alias revert if smoke test 403s.

      IF all three authorizers are DORMANT/COLD: option-(b) formal exception for all three; DT 0.3 security review SKIPPED with rationale documented.
    </deliverable>

    <deliverable id="tag-and-push">
      1. Pre-tag: `git tag -l "trade-pipeline-v*" | sort -V | tail -5` — confirm next version is `v1.4.0` (after W1 `v1.3.0`).
      2. `git commit --only --author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"` with explicit paths. (0.5.0 may author separate commits for SES packet or share the W2 commit; AEs coordinate.)
      3. `git tag -a trade-pipeline-v1.4.0 -m "W2 Lambda code reclamation: &lt;N&gt;/11 reclaimed, &lt;M&gt;/11 documented-as-exception + SES prod-access packet"`.
      4. `git push origin CLOUD --follow-tags`.
    </deliverable>
  </deliverables>

  <wire_contract>
    - Zero runtime behavior delta expected post-reclaim per option-(a) Lambda.
    - First `terraform apply` deploys reclaimed code; since source was pulled from live, `source_code_hash` should match exactly. 0-diff is the evidence.
    - Authorizer triplet (if any active): alias-swap pattern means zero downtime if reclaimed code matches live byte-for-byte. If not (Phase 0 manifest diff caught any discrepancy), fix the source before publish — do NOT deploy divergent code.
    - Option-(b) exceptions: zero runtime change. Documentation-only update + Known Issues row.
    - SES packet: zero runtime change. Documentation-only. Andrew's manual Console submission is the production-access flip.
  </wire_contract>

  <acceptance_criteria>
    1. **Phase 0 combined report delivered** at `docs/briefs/trsb_tfimpt_w2_phase0_discovery.md` with: 11-Lambda fixture/invocation/config manifest + dormancy matrix (30d + 90d) + API GW method-level triangulation + per-Lambda option-(a)/option-(b) recommendation + smoke-test build-vs-skip recommendation.
    2. **SES packet delivered** at `infra/aws/ses/trade-pipeline-prod-access-request.md` — Console-ready, plain markdown, all six required fields (use-case, volume estimate, compliance language, DKIM/SPF status, identity list, content readiness note).
    3. Phase 0 signoff from CTO + COO before Phase 1 fires. If 5+/11 are option-(b), COO surfaces to CTO for potential PRD amendment (deprecation assessment).
    4. Per option-(a) Lambda: src/ folder populated + lambdas.tf updated + lambda-source-map.json updated + `terraform plan` 0-diff + `comp-iam service &lt;fn&gt;` returns real result.
    5. `comp-iam gaps` runs with ≥N_option_a services scanned (up from 1); any MISSING permissions flagged and patched in iam.tf before commit.
    6. Every reclaimed Python file passes `ast.parse` + `importlib exec_module` smoke gates (HLOT2 standardization pattern).
    7. End-to-end smoke test: IF fixture exists, single test trade submit → UI → trade-submission-handler → DDB write → SES email → workflow state transitions. Document in session log. Skipped if Phase 0 recommended skip.
    8. `lambda-source-map.json` `source_dir` updated per reclaimed Lambda; CI drift-detection accepts the change.
    9. Tag `trade-pipeline-v1.4.0` exists and pushed.
    10. Authorizer triplet (if any active): DT 0.3 MCP-sign-off captured in session log pre-deploy. `aws lambda publish-version` + alias swap used, not direct `$LATEST`.
    11. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/{DATE}/trsb_tfimpt_w2_lambda_code_reclamation.md` (and optional 0.5.0_AE_OpalETL parallel log for SES packet authorship) reproducing every `<run>` + observed-result + pass/fail vs `<expect>`.
    12. MCP COMPLETE to COO with: per-Lambda decision table, commit hash(es), tag, smoke evidence, `comp-iam gaps` output, authorizer triplet DT 0.3 sign-off thread (if applicable), SES packet path.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="joint discovery (both AEs, Day 1)">
      <step>
        <run>For each of the 11 trade Lambdas: `aws lambda get-function --function-name &lt;fn&gt;` + `aws lambda get-function-configuration --function-name &lt;fn&gt;`</run>
        <expect>Code.Location S3 URL returned + full config captured per Lambda. Diff captured config against `trade-pipeline/lambdas.tf` for each function — document every field discrepancy in a manifest table (Runtime/Handler/Memory/Timeout/EnvVars/Role/Layers/VPC/arch).</expect>
        <if_mismatch>If any function returns ResourceNotFoundException, the source map is stale — surface to COO before proceeding (may indicate a Lambda was deleted between PRD and execution).</if_mismatch>
      </step>
      <step>
        <run>For each Lambda: unzip Code.Location zip + `comp-iam service &lt;fn&gt;` (BEFORE reclamation)</run>
        <expect>Pre-reclaim baseline: "No service matching '&lt;fn&gt;'" for all 11 (per PRD §2 evidence). Unzipped source lives at `/tmp/&lt;fn&gt;-src/`.</expect>
        <if_mismatch>If comp-iam returns a real result for any Lambda pre-reclaim, the compiler graph has been updated out-of-band — audit order-of-operations with COO.</if_mismatch>
      </step>
      <step>
        <run>**DORMANCY MATRIX — all 11 trade Lambdas.** Per function: CloudWatch invocations 30d + 90d + last-invocation-ts. Classify ACTIVE / DORMANT / COLD. Plus API GW method-level triangulation on the trade REST API (30d + 90d method Count vs matching Lambda Invocations).</run>
        <expect>Full 11 × 2-window dormancy matrix surfaced. Per-Lambda option-(a)/option-(b) recommendation derived from dormancy + code-reclaim-feasibility. If 5+/11 are DORMANT or COLD, flag as candidate for consolidated deprecation assessment.</expect>
        <if_mismatch>If 5+/11 are dormant, flag to COO + CTO as PRD-framing question — option-(b) scaling from ~4 to 8+ Lambdas is qualitatively different rollout. Do NOT self-amend PRD; surface + wait.</if_mismatch>
      </step>
      <step>
        <run>Fixture probe: `aws ses list-configuration-sets` + `aws ses list-identities` + grep repo for `trades@opalinvest.dev` sender + check `tests/` / partner docs / prod submission samples.</run>
        <expect>Either (a) a documented synthetic-trade fixture route exists (likely under tests/ / scripts/ / docs/), or (b) no fixture exists. Build-vs-skip recommendation derived from fixture availability AND dormancy outcome.</expect>
        <if_mismatch>If no fixture AND at least one option-(a) Lambda is active, recommend building minimal fixture in Phase 1 (or as a micro-follow-up TO). Document in Phase 0 report.</if_mismatch>
      </step>
      <step>
        <run>SES packet research: `aws ses list-identities` + `aws ses get-identity-verification-attributes --identities &lt;...&gt;` + `aws ses get-identity-dkim-attributes --identities &lt;...&gt;` + `aws ses get-send-quota` (current sandbox limits) + `aws ses list-configuration-sets`.</run>
        <expect>Per-identity verification + DKIM status captured. Sandbox quota + current send volume captured. All six SES packet required fields documented.</expect>
        <if_mismatch>If no SES identities exist under account 313476888478, surface to COO — either identities need to be created first (Phase 1 deliverable) or scope changes (SES not yet applicable; defer to future TO).</if_mismatch>
      </step>
      <step>
        <run>Joint AE MCP to COO with Phase 0 report path + per-Lambda option-disposition table + SES packet path + Phase 1 scope proposal</run>
        <expect>COO + CTO review + signoff. CTO may redline option recommendations; iterate.</expect>
        <if_mismatch>Signoff blocked on ambiguity → clarify iteratively. Do NOT start Phase 1 without signoff.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before reclaim-and-deploy commits (Day 2)">
      <step>
        <run>For every reclaimed Python file: `python -c "import ast; ast.parse(open(PATH).read())"` AND `python -c "import importlib.util; spec=importlib.util.spec_from_file_location(NAME, PATH); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)"` — both exit 0</run>
        <expect>HLOT2 standardization pattern. Catches latent NameError / missing import / circular import / top-level ImportError before commit. Every reclaimed file passes both.</expect>
        <if_mismatch>STOP. Fix missing imports / syntax errors before commit. Do NOT upload to S3 with failed gates — same-class failure mode as 081223b5 / 048a6fa3.</if_mismatch>
      </step>
      <step>
        <run>For every option-(a) Lambda: `comp-iam service &lt;fn&gt;` (AFTER reclamation, BEFORE commit)</run>
        <expect>Now returns a real result — boto3 calls enumerated from the reclaimed source. Compare against `iam.tf` allow-list for that Lambda's role. MISSING flag = patch iam.tf before commit.</expect>
        <if_mismatch>If MISSING appears, do NOT commit Lambda reclamation without also committing the iam.tf patch.</if_mismatch>
      </step>
      <step>
        <run>`comp-iam gaps`</run>
        <expect>Services-scanned count increases proportionally to option-(a) Lambdas reclaimed. Overall "No permission gaps detected" after any iam.tf patches land.</expect>
        <if_mismatch>Any gap surfacing = patch iam.tf before commit. Do NOT ship partial coverage.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>Per reclaimed Lambda: `source_code_hash` 0-diff (reclaimed zip matches live). `ignore_changes` block removed. `filename=placeholder.zip` replaced with `s3_bucket`+`s3_key`. Any drift = Phase 0 manifest diff was missed.</expect>
        <if_mismatch>If source_code_hash diffs, reclaimed zip and live don't match — investigate before apply. Common causes: ZIP timestamp variance, .pyc files in live zip but not reclaimed, requirements install added vendored deps.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="after commit">
      <step>
        <run>terraform plan</run>
        <expect>0-diff across trade-pipeline state post-W2 apply(s).</expect>
        <if_mismatch>Post-apply drift = incomplete reclaim on at least one Lambda. STOP, capture, surface to COO; do NOT tag or mark complete.</if_mismatch>
      </step>
      <step>
        <run>End-to-end smoke test per Phase 0 fixture decision (if applicable)</run>
        <expect>Single test trade submit → UI → trade-submission-handler → opal-trade-submissions DDB write → SES email (if SES prod-access granted by then) → workflow state transitions. CloudWatch trace captures authorizer + handler + DDB write. No 403s, no 500s.</expect>
        <if_mismatch>If authorizer triplet returns 403 post-alias-swap, revert the alias. If trade-submission-handler 500s, check for missing `requirements.txt` vendored deps. Full rollback via `terraform apply` with prior `source_code_hash` if needed.</if_mismatch>
      </step>
      <step>
        <run>`comp-iam service` per option-(a) Lambda + `comp-iam gaps` (global)</run>
        <expect>All option-(a) Lambdas indexed; `comp-iam gaps` clean with expected N_option_a services scanned. If N_option_b > 0, document gap in Known Issues with explicit ownership.</expect>
        <if_mismatch>Gap surfacing post-apply = iam.tf is insufficient for real runtime usage. Open a fast-follow patch TO.</if_mismatch>
      </step>
      <step>
        <run>comp-routes trace trade-submission-handler</run>
        <expect>Still empty (W3 gap — API GW not yet in TF). Expected; W3 closes it.</expect>
        <if_mismatch>If result appears, W3 may have shipped concurrently — reconcile.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>**Joint AE engagement:** 0.5.0_AE_OpalETL + 0.7.0_AE_CloudOps co-own Phase 0. Either can author the combined report or they split (SES packet likely 0.5.0 as ETL-identity-verification experience; dormancy matrix + code reclaim likely 0.7.0 as CloudOps infrastructure experience). Both MUST MCP-ACK COO on the combined report before Phase 1 fires.</item>
    <item>**Authorizer triplet** requires 0.3.0_DT_TradingOperations security review before deploy IF Phase 0 classifies any as active. Security-critical gate. DT 0.3 MCP-sign-off BEFORE `aws lambda publish-version`. Deploy pattern: `publish-version` + alias swap, NOT direct `$LATEST`.</item>
    <item>**Smoke test fixture** — Phase 0 build-vs-skip recommendation determines Phase 1 smoke scope. No external Andrew answer required; AEs decide from evidence.</item>
    <item>**SES prod-access Console submission** — Andrew performs this manually AFTER W2 commits the packet. Not a Phase 1 deliverable; a post-W2 Andrew action. W2 ships the packet; Andrew's form submission is outside the TO.</item>
    <item>No AE 0.6 / BD pipeline conflict. W2 touches trade-pipeline state file + trade-pipeline Lambda src + SES identities, fully orthogonal to BD pipeline work.</item>
    <item>No portal CF touch. W3 will add CF behaviors; W2 does not.</item>
    <item>Tag series: `trade-pipeline-v1.4.0` (after W1 `v1.3.0`). Verify via `git tag -l "trade-pipeline-v*" | sort -V | tail -5` pre-tag.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="TRSB_TFIMPT.W1" status="complete">
      W1 shipped trade-pipeline-v1.3.0 (commit `d1e27dfb` + `62847274`) 2026-04-21. Baseline established. W2 doesn't technically require W1's DDB import; strict ordering per PRD §3.
    </dependency>
    <dependency agent="2.0.0_SA_COO" task="W2 staged→pending flip" status="pending">
      No longer gated on Andrew §8 Q2+Q4 (rescope 2026-04-21). Gates only on both AEs ACKing joint engagement. COO flips after joint ACK.
    </dependency>
  </dependencies>

  <next>
    On joint AE ACK of this TO: COO flips staged→pending + dispatches GO MCP (both AEs addressed). Day 1: joint Phase 0 discovery → combined report + SES packet → MCP COO + CTO for signoff. Day 2: Phase 1 reclaim per option-disposition plan → authorizer triplet DT 0.3 review if applicable → commit + tag + push → MCP COMPLETE to COO with full evidence bundle + SES packet path (Andrew performs Console submission manually post-commit).
  </next>
</task_order>
