<task_order>
  <metadata>
    <id>YALP_MDSRC.B2</id>
    <slug>ae-b1-lambda-artifacts-commit-and-deploy</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~A</issued_to>
    <reassigned_from>0.5.0_AE_OpalETL</reassigned_from>
    <!-- REASSIGNED 2026-05-21 by COO (stimulus-scan): the entire OpalETL lane (0.5.0_AE_OpalETL base + ~B) is offline (NOT_REGISTERED). B1 is e2e-verified + staged and 0.4.0_DS is blocked on this deploy; B2 cannot sit indefinitely on an offline lane. Reassigned to 0.7.0_AE_CloudOps~A — a live, idle, AE-capable CloudOps-lane agent (consistent with the original dispatch_unblock_condition's anticipation that ~A may take it). One known friction: if the SHARED_OPAL_ETL-lane B1 artifact trips the owned-paths pre-commit hook for ~A's serial, ~A surfaces to COO and COO does the one-line .owned-paths.yaml permitted_agents add (the documented tilde-lane owned-paths-gap pattern) — fast, not a blocker. The CLOUD_OPS_OR_ETL (any-AE) artifact commits clean. -->
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — COO routing ruling (B1, 2026-05-20). BOTH B1 build artifacts are AE-lane infra/aws/lambda code; DS 0.4.0 authored + verified them but cannot commit them (correct lane discipline — DS did not --force). This TO is the AE commit + Lambda deploy of both. NOTE: 0.5.0_AE_OpalETL base is offline as of issue time; this TO sits in the base task_orders/ folder for pickup on boot. COO has flagged 2.0.0_SA_COO~B that if base stays offline the ~B exec may dispatch this to 0.5.0_AE_OpalETL~B (a ~B agent via the ~B exec chain — fine; a base-serial direct order to ~B — not). 0.5.0_AE_OpalETL is the correct owner: it can commit BOTH lanes — SHARED_OPAL_ETL (its lane) and CLOUD_OPS_OR_ETL (any-AE).</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — the SmartX implementation segment. The AE-lane deploy half of YALP_MDSRC.B1 (DS 0.4.0). B1's end-to-end verification cannot run until both these Lambdas are deployed — B2 is on B1's completion path.</priority>
    <sla>~1 effort-day — both artifacts are built + verified by DS 0.4.0; B2 is the review + commit + Lambda packaging + 2x terraform deploy + source-map. The substance is the deploy cycle, not authoring.</sla>
  </metadata>

  <references>
    <b1>YALP_MDSRC.B1 (0.4.0_DS_ClientPlatform) — the parent TO. DS 0.4.0 authored + verified BOTH B1 build artifacts (gate-clean, dual-source override logic tested). B1 retains: coordinate the sidecar path/shape, run the end-to-end model_portfolio_benchmarks.json verification once both Lambdas deploy, RAVC2. B2 is the AE-lane half: commit both files + deploy both Lambdas.</b1>
    <handoff>docs/briefs/ae-handoff-yalp-mdsrc-b1-lambda-artifacts-20260521.md (8caacbadc, on origin/CLOUD) — DS 0.4.0's AE hand-off brief. CONSUME THIS AS THE BUILD INPUT: both files (path/purpose/lane), the DS verification evidence marked do-not-re-run, the sidecar S3 path/shape contract (s3://opal-data-portal-v2/json/benchmarks/_smartx_model_monthly.json + the full JSON schema both Lambdas are coded to), the deploy-order note (Artifact 1 first / run once so the sidecar exists; graceful all-yang fallback makes strict ordering optional), the IAM deltas (Artifact 1 needs Secrets Manager + egress; Artifact 2 needs nothing new), and the documented Path-A consequences for v0.4 awareness.
    <sxpl>SXPL_RESTIN.002.ae-smartx-rest-pull-flow.md — the SmartX REST pull flow, your lane. The SmartX pull integrates against the same SmartX REST API; reuse the ROPC-JWT auth + the smartx/credentials secret.</sxpl>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED, 73e4da697) — the SmartX pull is an INTEGRATION against the SmartX REST API; terminology "reverse engineer" / "integrate", never "scrape". §3 step 2 — credential handling binds to AWS Secrets Manager (smartx/credentials); §3 step 6 — contract-drift detection (fail loud if the SmartX response shape changes).</standard>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3.2 §5.3 (Model Portfolios seam). CTO v0.4 consolidates.</prd>
  </references>

  <context>
    COO routing ruling, 2026-05-20: B1 (DS 0.4.0) was issued to build the SmartX model-monthly-performance pull + the yang dual-input producer. BOTH deliverables turn out to be AE-lane infra code — DS can author + verify Lambda code but the commit + terraform deploy is AE's (CLAUDE.md Rule 1; the DS commit carve-out, Rule 13, is `data/*/scripts/{gold,silver,bronze}/*.py` only — it does NOT cover `data/smartx/scripts/` pull code or `infra/aws/lambda/` function code). The owned-paths hook correctly blocked DS 0.4.0 on both; DS did not --force (correct). So the SmartX-pull code + the yang Lambda mod + both deploys are AE-OpalETL's; B1 stays DS 0.4.0's for the final end-to-end verification. This TO is the AE-OpalETL half — both artifacts.

    THE TWO ARTIFACTS — both BUILT + VERIFIED by DS 0.4.0, do not re-author:

    ARTIFACT 1 — the SmartX pull. File: data/smartx/scripts/pull_smartx_model_monthly_performance.py (in the shared working tree; uncommitted; ~13.6 KB; SHARED_OPAL_ETL lane). ROPC-JWT auth; integrates against performance.smartxadvisory.com/models/performance for the 5 portal models; computes the 7 monthly+ periods (1M / MTD / QTD / 1Q / YTD / 1Y / SI); emits the sidecar json/benchmarks/_smartx_model_monthly.json with per-period model_source='smartx_realized' labels (the Q8 cadence-source split). DS verification: ds-commit-gate clean; live dry-run builds the sidecar for all 5 models; computed ST YTD 1.15% cross-checks SmartX's own precomputed ytd field 1.1517% to 0.002pp; the performance endpoint empirically ignores date params (no-param full-history pull).

    ARTIFACT 2 — the yang dual-input producer. File: infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py (in the shared working tree; uncommitted; CLOUD_OPS_OR_ETL lane). The dual-input modification: the 7 monthly+ periods of model_portfolio_benchmarks.json's model field source from the SmartX sidecar (model_source='smartx_realized'); 1D/WTD stay yang (model_source='yang_design'); explicit per-period model_source label + a top-level model_source_note (the mandatory Q8 split); legacy benchmark_returns.json inherits the label; graceful all-yang fallback if the sidecar is absent. DS verification: ds-commit-gate clean; the dual-source override logic tested against a synthetic sidecar (monthly periods route to smartx_realized, 1D/WTD to yang_design, sidecar-absent degrades to all-yang); no new IAM.
  </context>

  <scope>
    <in_scope>
      ARTIFACT 1 — the SmartX pull (SHARED_OPAL_ETL lane):
      - Review pull_smartx_model_monthly_performance.py against SHARED_OPAL_ETL lane conventions (auth helper reuse, logging, error handling) — minor lane-convention adjustments in scope; re-architecture is not (built + verified).
      - Commit it to data/smartx/scripts/ via .tools/safe-commit.sh.
      - Package + deploy it as a Lambda: standalone vs added-to-SXPL_RESTIN-pull is your lane-owner architecture call (CTO-coordinate if it touches SXPL_RESTIN architecture). Size memory/timeout deliberately (Rule 5).
      - Confirm the sidecar json/benchmarks/_smartx_model_monthly.json is produced to the S3 location Artifact 2 expects.

      ARTIFACT 2 — the yang dual-input producer (CLOUD_OPS_OR_ETL lane):
      - Review the yang-model-portfolio-benchmarks lambda_function.py dual-input modification — confirm it is a clean diff against the deployed function; built + verified, do not re-author.
      - Commit it via .tools/safe-commit.sh.
      - Redeploy the yang-model-portfolio-benchmarks Lambda via the yang-pipeline terraform.

      BOTH:
      - Update infra/aws/lambda/ci/lambda-source-map.json (Rule 4) for any new/changed function.
      - Full deploy cycle per CLAUDE.md for each: code -> Terraform -> source map -> git commit -> terraform plan -> .tools/safe-apply.sh (HALTGT checkpoint) -> 0-diff -> git tag -> push --follow-tags.
      - DEPLOY ORDER: the yang producer has a graceful all-yang fallback if the sidecar is absent, so strict ordering is not required — but prefer deploying the SmartX pull first (or running it once) so the sidecar exists before the yang producer's first post-deploy run, to avoid a transient all-yang window. Document the order used.
      - Coordinate the exact sidecar S3 path/shape with DS 0.4.0 (B1) so Artifact 2 reads what Artifact 1 writes.
    </in_scope>
    <out_of_scope>
      - The end-to-end model_portfolio_benchmarks.json verification — that is B1 (DS 0.4.0), run once both Lambdas deploy.
      - Re-authoring or re-verifying either artifact's logic — DS 0.4.0 built + verified both; B2 commits + deploys. Lane-convention adjustments only.
      - Portal wiring of the SmartX-sourced columns — gated on Andrew Q8 (B1 Phase 2).
      - Any YCharts / FRED work.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before each deploy">
      <step>
        <run>comp-pipescript io on each artifact (if a comp-graph node) + comp-iam service on each Lambda + comp-pipescript io yang-model-portfolio-benchmarks for the COLUMN GAPS / portal-consumer check on the modified producer</run>
        <expect>COLUMN GAPS / portal-consumer check; comp-iam confirms no missing S3/SSM/SecretsManager IAM (the SmartX pull needs SecretsManager read on smartx/credentials; DS reports the yang mod needs no new IAM — confirm).</expect>
        <if_mismatch>If not a comp-graph node, source-read + document. Fix any IAM gap in iam.tf before deploy.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before each commit">
      <step>
        <run>.tools/ds-commit-gate.sh on each file (the .py pull + the yang lambda_function.py)</run>
        <expect>All three checks exit 0 (py_compile + ds-precommit-check + ruff py39) — re-confirm DS 0.4.0's gate-clean result holds at commit time.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after each deploy">
      <step>
        <run>comp-pipescript deployed on each artifact + verify each terraform plan is 0-diff</run>
        <expect>Runner has the committed code (MATCH); each apply reached 0-diff; the sidecar artifact is produced.</expect>
        <if_mismatch>STALE/MISSING -> redeploy; non-0-diff -> investigate before tagging.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    B1 (DS 0.4.0) is the sibling — DS authored + verified both artifacts and runs the end-to-end verification once both deploy. Consume DS 0.4.0's AE hand-off brief. Coordinate the sidecar S3 path/shape with DS 0.4.0 so Artifact 2 reads what Artifact 1 writes. SXPL_RESTIN.002 is your own lane TO — the SmartX REST auth path is shared; reuse. CTO writes PRD v0.4 — RAVC2 feeds it.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Artifact 1: data/smartx/scripts/pull_smartx_model_monthly_performance.py committed via safe-commit on origin/CLOUD; ds-commit-gate re-confirmed exit 0; deployed as a Lambda (standalone vs SXPL_RESTIN-integrated documented), memory/timeout sized deliberately.</ac>
    <ac id="AC2">Artifact 2: the yang-model-portfolio-benchmarks lambda_function.py dual-input modification committed via safe-commit on origin/CLOUD; ds-commit-gate exit 0; the Lambda redeployed via the yang-pipeline terraform.</ac>
    <ac id="AC3">Both: lambda-source-map.json updated; full deploy cycle complete for each (commit -> plan -> safe-apply -> 0-diff -> tag -> push --follow-tags); deploy order documented.</ac>
    <ac id="AC4">The sidecar json/benchmarks/_smartx_model_monthly.json confirmed produced to the S3 location Artifact 2 expects; the path/shape coordinated with DS 0.4.0.</ac>
    <ac id="AC5">Phase-1 comp-iam + Phase-2 ds-commit-gate + Phase-3 comp-pipescript deployed + 0-diff plans reproduced in the session log Compiler Tools section.</ac>
    <ac id="AC6">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform (so B1 can run the end-to-end verify).</ac>
  </acceptance_criteria>

  <deliverables>
    - Both B1 Lambda artifacts committed + deployed (the SmartX pull Lambda + the modified yang-model-portfolio-benchmarks Lambda); git tags; lambda-source-map entries.
    - Session log with the Compiler Tools section + the deploy-order + the standalone-vs-integrated Lambda architecture-call rationale.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform.
  </deliverables>

  <do_not>
    <rule>Do NOT re-author or re-verify either artifact's logic — DS 0.4.0 built + verified both; B2 is review + commit + deploy. Lane-convention adjustments only.</rule>
    <rule>Do NOT deploy either Lambda by any path other than terraform via .tools/safe-apply.sh (CLAUDE.md Rules 1 + 18). No aws lambda update-function-code.</rule>
    <rule>Do NOT handle the SmartX credentials in chat / MCP / git / logs — the secret is smartx/credentials; reference it by name only.</rule>
    <rule>Terminology: the SmartX pull is an INTEGRATION against the SmartX REST API — never "scrape" (Third-Party Data Integration Standard).</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
