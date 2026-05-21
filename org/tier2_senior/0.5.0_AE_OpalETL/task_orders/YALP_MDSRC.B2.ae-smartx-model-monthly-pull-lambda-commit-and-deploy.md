<task_order>
  <metadata>
    <id>YALP_MDSRC.B2</id>
    <slug>ae-smartx-model-monthly-pull-lambda-commit-and-deploy</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — COO routing ruling (B1 option (c), 2026-05-20). The SmartX-pull integration code lives in the SHARED_OPAL_ETL lane (data/smartx/scripts/) which is 0.5.0_AE_OpalETL's domain; the script is already built + verified by DS 0.4.0 and staged in the shared working tree. This TO is the AE-OpalETL commit + Lambda deploy of it. NOTE: 0.5.0_AE_OpalETL base is offline as of issue time; this TO sits in the base task_orders/ folder for pickup on boot. COO has flagged 2.0.0_SA_COO~B that if base stays offline the ~B exec may dispatch this to 0.5.0_AE_OpalETL~B (a ~B agent picking it up via the ~B exec chain is fine; a base-serial direct order to ~B is not).</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — the SmartX implementation segment. Sibling of YALP_MDSRC.B1 (DS 0.4.0). Not on a tight clock, but the verified script is sitting uncommitted in the shared working tree — commit it before it rots.</priority>
    <sla>~0.5-1 effort-day — the script is built + verified; this is the commit + Lambda packaging + terraform deploy + source-map entry. The substance is the deploy cycle, not authoring.</sla>
  </metadata>

  <references>
    <b1>YALP_MDSRC.B1 (0.4.0_DS_ClientPlatform) — the parent TO. DS 0.4.0 built + verified the SmartX-pull integration; B1 retains the yang dual-input producer modification + end-to-end verification + RAVC2. B2 is the AE-lane half: commit the pull code + deploy the Lambda.</b1>
    <sxpl>SXPL_RESTIN.002.ae-smartx-rest-pull-flow.md — the SmartX REST pull flow, your lane. B2's pull integrates against the same SmartX REST API; reuse the ROPC-JWT auth + the smartx/credentials secret. Decide (CTO-coordinate if needed) whether the monthly model-performance pull is a NEW standalone Lambda or an added endpoint in the SXPL_RESTIN pull surface — your architecture call as the lane owner.</sxpl>
    <standard>org/tier1_exec/2.0.0_SA_COO/drafts/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (306e394c0) — the Andrew-direct Third-Party Data Integration Standard. The pull is an INTEGRATION against the SmartX REST API; terminology "reverse engineer" / "integrate", never "scrape".</standard>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3.2 §5.3 (Model Portfolios seam). CTO v0.4 will consolidate.</prd>
  </references>

  <context>
    COO routing ruling, 2026-05-20: B1 (DS 0.4.0) built the SmartX model-monthly-performance pull integration. The script lands at data/smartx/scripts/ which is the SHARED_OPAL_ETL lane (0.5.0_AE_OpalETL + ~B) — the owned-paths hook correctly blocked DS 0.4.0's commit, and this is a genuine ownership boundary, not a YAML gap: data/smartx/ + the SmartX-pull flow (SXPL_RESTIN) are AE-OpalETL's domain, and AE owns the Lambda terraform deploy regardless. So the SmartX-pull CODE + Lambda is AE-OpalETL's; B1 stays DS 0.4.0's for the yang-side dual-input producer + the end-to-end verification. This TO is the AE-OpalETL half.

    The script is BUILT + VERIFIED by DS 0.4.0 — do not re-author it:
    - File: data/smartx/scripts/pull_smartx_model_monthly_performance.py (in the shared working tree; staged, uncommitted; 13592 bytes).
    - What it does: ROPC-JWT auth; integrates against performance.smartxadvisory.com/models/performance for the 5 portal models; computes the 7 monthly+ periods (1M / MTD / QTD / 1Q / YTD / 1Y / SI); emits the sidecar json/benchmarks/_smartx_model_monthly.json with per-period model_source='smartx_realized' labels (the mandatory Q8 cadence-source split).
    - DS 0.4.0 verification evidence: ds-commit-gate clean (py_compile + ds-precommit-check + ruff py39); live dry-run builds the sidecar for all 5 models; computed ST YTD 1.15% cross-checks SmartX's own precomputed ytd field 1.1517% to 0.002pp; empirically confirmed (Third-Party Data Standard discipline) the performance endpoint ignores date params -> no-param full-history pull.
  </context>

  <scope>
    <in_scope>
      - Review the DS-built script data/smartx/scripts/pull_smartx_model_monthly_performance.py — confirm it meets the SHARED_OPAL_ETL lane conventions (auth helper reuse, logging, error handling). Minor lane-convention adjustments are in scope; a re-architecture is not (it is built + verified).
      - Commit it to data/smartx/scripts/ via .tools/safe-commit.sh (you are the lane owner — the owned-paths hook will pass).
      - Package + deploy the SmartX model-monthly-performance pull as a Lambda: decide standalone-Lambda vs added-to-SXPL_RESTIN-pull (lane-owner call; CTO-coordinate if it touches the SXPL_RESTIN architecture). Set memory_size / timeout deliberately for the workload (CLAUDE.md Rule 5 — do not leave yang-lambda 256MB/30s defaults).
      - Update infra/aws/lambda/ci/lambda-source-map.json (Rule 4) + the source map for any new function.
      - Full deploy cycle per CLAUDE.md: write/confirm code -> write Terraform -> source map -> git commit -> terraform plan -> .tools/safe-apply.sh (HALTGT checkpoint) -> verify 0-diff -> git tag -> push --follow-tags.
      - Confirm the sidecar json/benchmarks/_smartx_model_monthly.json is produced to the expected S3 location for the B1 yang dual-input producer to consume.
    </in_scope>
    <out_of_scope>
      - The yang dual-input producer modification + the end-to-end model_portfolio_benchmarks.json verification — that is B1 (DS 0.4.0), running in parallel.
      - Re-authoring or re-verifying the pull logic — DS 0.4.0 built + verified it; B2 commits + deploys it.
      - Portal wiring of the SmartX-sourced columns — gated on Andrew Q8 (B1 Phase 2).
      - Any YCharts / FRED work.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the deploy">
      <step>
        <run>comp-pipescript io  on pull_smartx_model_monthly_performance.py (if it is a comp-graph node) + comp-iam service on the new/modified Lambda</run>
        <expect>COLUMN GAPS / portal-consumer check on the pull; comp-iam flags any missing S3/SSM/SecretsManager IAM permission before deploy (the ROPC-JWT pull needs SecretsManager read on smartx/credentials).</expect>
        <if_mismatch>If not a comp-graph node, source-read + document. Fix any IAM gap in iam.tf before deploy.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/smartx/scripts/pull_smartx_model_monthly_performance.py</run>
        <expect>All three checks exit 0 (py_compile + ds-precommit-check + ruff py39) — re-confirm DS 0.4.0's gate-clean result holds at commit time.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after deploy">
      <step>
        <run>comp-pipescript deployed pull_smartx_model_monthly_performance.py + verify the terraform plan is 0-diff</run>
        <expect>Runner has the committed code (MATCH); terraform apply reached 0-diff; the sidecar artifact is produced.</expect>
        <if_mismatch>STALE/MISSING -> redeploy; non-0-diff -> investigate before tagging.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    B1 (DS 0.4.0) is the sibling — DS 0.4.0 builds the yang dual-input producer that consumes this pull's sidecar (json/benchmarks/_smartx_model_monthly.json). Coordinate the sidecar's exact S3 path/shape with DS 0.4.0 so the producer reads what this pull writes. SXPL_RESTIN.002 is your own lane TO — the SmartX REST auth path is shared; reuse, do not duplicate. The smartx/credentials secret is the ROPC-JWT credential store. CTO writes PRD v0.4 — RAVC2 feeds it.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">data/smartx/scripts/pull_smartx_model_monthly_performance.py committed via safe-commit (lane-clean) on origin/CLOUD; ds-commit-gate re-confirmed exit 0.</ac>
    <ac id="AC2">The SmartX model-monthly-performance pull deployed as a Lambda (standalone or SXPL_RESTIN-integrated — the lane-owner call documented), memory/timeout sized deliberately, lambda-source-map.json updated, full deploy cycle complete: commit -> plan -> safe-apply -> 0-diff -> tag -> push --follow-tags.</ac>
    <ac id="AC3">The sidecar json/benchmarks/_smartx_model_monthly.json confirmed produced to the S3 location B1's yang dual-input producer expects; the path/shape coordinated with DS 0.4.0.</ac>
    <ac id="AC4">Phase-1 comp-iam + Phase-2 ds-commit-gate + Phase-3 comp-pipescript deployed + 0-diff plan reproduced in the session log Compiler Tools section.</ac>
    <ac id="AC5">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform (so B1 knows the pull is deployed and can run the end-to-end verify).</ac>
  </acceptance_criteria>

  <deliverables>
    - The committed + deployed SmartX model-monthly-performance pull Lambda; git tag; lambda-source-map entry.
    - Session log with Compiler Tools section + the standalone-vs-integrated Lambda architecture-call rationale.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform.
  </deliverables>

  <do_not>
    <rule>Do NOT re-author or re-verify the pull logic — DS 0.4.0 built + verified it; B2 is commit + deploy. Lane-convention adjustments only.</rule>
    <rule>Do NOT deploy the Lambda by any path other than terraform via .tools/safe-apply.sh (CLAUDE.md Rules 1 + 18). No aws lambda update-function-code.</rule>
    <rule>Do NOT handle the SmartX credentials in chat / MCP / git / logs — the secret is smartx/credentials; reference it by name only.</rule>
    <rule>Terminology: this is an INTEGRATION against the SmartX REST API — never "scrape" (Third-Party Data Integration Standard).</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
