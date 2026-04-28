<task_order>
<metadata>
  <to_id>ADVI_ORIAPI.001</to_id>
  <project>ADVI_ORIAPI</project>
  <title>Orion API JWT Extract + Billing Spike + Saved-Query + GO/NO-GO (Phases 0+1+3+4)</title>
  <assigned_to>0.6.1_AE_PartnerETL~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-04-27</issued_date>
  <status>complete</status>
  <priority>HIGH</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_ORIAPI.md (v0.4 FINAL, commit c232b4ec)</ref>
    <ref type="appendix_a">Full API contract — POST /api/v1/Reporting/Envision/ExcelReports/{queryId}/Generate -> poll GET /Run/{runId} -> binary CSV. Auth: Authorization: Session JWT, HS512, 10h TTL.</ref>
    <ref type="appendix_b">SMS Strategy + Autonomous JWT Acquisition — --mode jwt-extract on inf-exporter EC2, reuses existing inf-otp-relay Lambda + Playwright sign-in logic.</ref>
    <ref type="har_parser">tools/har-scan.py (commit b5bd2527) — re-extract anything from source HARs in Andrew's Downloads on demand.</ref>
  </references>
  <dependencies>
    <dependency>Andrew confirms ORION_USERNAME/ORION_PASSWORD secret name/ARN + AE 0.6.1 IAM grant (existing inf-exporter SSM doc may already have this — confirm reusable)</dependency>
    <dependency>Andrew first-run OTP standby (single OTP entry to bootstrap browser profile; Orion "Remember this device" reduces subsequent OTP frequency)</dependency>
    <dependency>Confirm Orion "Remember this device" actually reduces OTP frequency in practice (if not, pre-emptive cron strategy needs adjustment)</dependency>
  </dependencies>
</metadata>

<scope>
Context: Orion does not publish a documented API. Their web UI internally calls api.cloud.orionadvisor.com. This is a sleuthing/reverse-engineering exercise — no vendor docs, no support, gray-zone ToS (own data + own credentials + low volume = same posture as manual UI use per Andrew 2026-04-27). Appendix A of the PRD documents the full API contract discovered from HAR captures.

AE 0.6.1 extends the existing inf-exporter EC2 service (ADVI_INFLEC.W3.B TOs) and adds a new mode:

PHASE 0 — Add --mode jwt-extract to inf-exporter (~1 day):
- Sister code path to the existing bronze-export mode. Shares ALL sign-in + OTP logic.
- Branch on output: instead of downloading CSVs, capture the JWT token via Playwright network interception.
- Write to s3://opal-data-inf/orion/jwt/current.json: {"jwt": "<token>", "captured_at": "<ISO8601>", "ttl_hours": 10}
- Browser profile persists (Orion "Remember this device") — subsequent runs OTP-free.
- Credentials: use ORION_USERNAME/ORION_PASSWORD from existing SSM doc env vars. Never commit.
- auth_state.json, .env.orion gitignored (enforced in .gitignore per c232b4ec commit).

PHASE 1 — Billing-pull spike, validates Appendix A end-to-end (~half day):
- Script: data/orion/api-recon/orion_pull_spike.py
- Flow: read JWT from s3://opal-data-inf/orion/jwt/current.json -> POST /api/v1/Reporting/Envision/ExcelReports/{billing_query_id}/Generate (entityIds: [3,11,12] for Inflection cohort) -> poll GET /Run/{runId} until 200 + binary CSV -> save locally.
- Validate: compare row count + byte count against Andrew's manual Billing pull (2,899 rows x 17 cols).
- Also test generic endpoint: POST /api/v1/Homepage/Action/DataSources/{id} (stored procedure invocation) per §A.5.

PHASE 3 — Saved-query enumeration + arbitrary pull via --query-name CLI (~half day):
- GET /api/v1/Reporting/Envision/ExcelReports to list all saved queries.
- Extend orion_pull_spike.py: --query-name argument, fuzzy match against saved list, execute.
- Demonstrate running at least 2 distinct saved queries successfully.

PHASE 4 — GO/NO-GO recommendation (~2 hours):
- Assess: OTP frequency observed (how often Orion prompts despite "Remember this device"), rate-limit behavior (429s seen? Max request cadence?), pagination (if any query returns paginated results).
- Recommend ONE of: (a) ad-hoc CLI tool (Andrew runs manually when dim needed), (b) scheduled daily/weekly cron via ADVI_ORIAPI.002 Terraform, (c) full ADVI_INFLEC_BRONZERUN_V2 Phase B expansion (more ambitious).
- Written recommendation committed to data/orion/api-recon/go_nogo.md.

PHASE 2 (EventBridge cron Terraform) is AE 0.7.0's TO — coordinate: send RAVC to COO after Phase 0 RAVC confirming JWT write to S3, which gates AE 0.7.0's TO from staged -> pending.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service inf-exporter</run>
      <expect>s3:PutObject permission present for s3://opal-data-inf/orion/jwt/* prefix. If this prefix does not appear in the IAM policy, flag to COO before writing Phase 0 code — AE 0.7.0 may need to add it first.</expect>
      <if_mismatch>STOP. MCP COO with missing permission. Do not write jwt-extract code until IAM gate is clear.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>python -m py_compile &lt;all modified .py files&gt;</run>
      <expect>Exit 0 for all files. No syntax errors.</expect>
      <if_mismatch>STOP. Fix syntax errors.</if_mismatch>
    </step>
    <step>
      <run>bash .tools/ds-commit-gate.sh &lt;modified .py files&gt;</run>
      <expect>Exit 0. py_compile + AST undefined-name scanner + ruff --target-version py39 all pass.</expect>
      <if_mismatch>STOP. Fix all flagged issues before committing.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after Phase 0 code run (first jwt-extract execution)">
    <step>
      <run>aws s3 ls s3://opal-data-inf/orion/jwt/current.json</run>
      <expect>File present with modification timestamp within last 10 hours.</expect>
      <if_mismatch>JWT write did not succeed. Debug Playwright network interception before advancing to Phase 1.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. Phase 0: --mode jwt-extract added to inf-exporter. Andrew first-run OTP completes. s3://opal-data-inf/orion/jwt/current.json populated with valid JWT within 10 min of first EC2 run.
2. Phase 1: Billing Dim spike script downloads CSV matching Andrew's manual pull within 5% row/byte count. Committed to data/orion/api-recon/. Gitignored auth files confirmed absent from commit.
3. Phase 3: --query-name CLI lists saved ExcelReports queries and successfully executes at least 2 distinct queries.
4. Phase 4: go_nogo.md committed with concrete recommendation (ad-hoc CLI / scheduled cron / BRONZERUN_V2 Phase B) citing OTP frequency, rate limits, pagination findings.
5. Session log per phase (org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-04-27/oriapi_phase{N}_*.md) including Compiler Tools section reproducing every run from compiler_tools_mandate with observed output and explicit pass/fail vs expect. Missing rows = REWORK.
6. RAVC to COO + CTO after each phase: commit hashes + Phase 4 recommendation text.
7. ADVI_ORIAPI.002 (AE 0.7.0) gates on Phase 0 RAVC — COO will flip .002 from staged to pending once Phase 0 confirmed.
</acceptance_criteria>

<cross_domain_coordination>
- ADVI_INFLEC: reuses inf-exporter codebase. Do NOT break existing --mode bronze-export path. Test both modes after Phase 0 merge.
- ADVI_ORIAPI.002 (AE 0.7.0): notify COO via RAVC after Phase 0 to trigger .002 gate flip.
- ADVI_INFLV2: Phase 4 recommendation informs whether manual dim pulls in INFLV2 are still needed.
- Credential protocol: all auth material stays in env vars / Secrets Manager / gitignored files. No exceptions.
</cross_domain_coordination>
</task_order>
