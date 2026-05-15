<task_order>
  <metadata>
    <id>ADVI_ECLDAT.001</id>
    <slug>ae-jwt-extension-eclipse-dual-track</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <completed_at>2026-05-15T02:55Z</completed_at>
    <deploy_commit>8ff9ee1ff</deploy_commit>
    <deploy_tag>inf-pipeline-v1.7.60</deploy_tag>
    <project_code>ADVI_ECLDAT</project_code>
    <priority>P1 — Andrew dashboard tomorrow gate; Eclipse JWT capture + dual-track freshness validation</priority>
    <sla>~2-3h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="feasibility_brief">docs/briefs/data-scientist-eclipse-ingestion-feasibility-20260514.md (DS~A `23d2e2c54`)</ref>
    <ref type="cto_ratify">CTO 5-Q ratify 2026-05-14 ~20:5XZ — Q5 dual-track JWT freshness extension; HS256 float exp (Orion) vs HS512 int exp (Eclipse)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~21:0XZ: "set up the same jwt refresher that we did for orion for eclipse as well as figuring out bronze and silver ingestion, gold layers can wait for now"</ref>
    <ref type="sibling_pattern">inf-jwt-trigger Lambda + jwt_freshness.py (Orion JWT capture + freshness validation pattern source)</ref>
    <ref type="dependency_phase2">ADVI_ECLDAT.002 DS~A bronze puller runs stop-gap on Andrew JWT direct pre-Phase-1; supersedes to Lambda-managed JWT post-Phase-1 ship</ref>
  </references>

  <context>
    DS~A feasibility brief proves Eclipse data ingestion via JWT bearer auth. Eclipse JWT distinct from Orion JWT in 3 ways:
    - Auth endpoint: GET https://www.orioneclipse.com/v1/admin/Token (vs Orion equivalent)
    - JWT signing key: HS512 int `exp` (Eclipse) vs HS256 float `exp` (Orion)
    - User ID: separate `eclipse_user_id` SM metadata vs `orion_user_id`

    Per Andrew Q3 hybrid audit trail ratify: Andrew identity stop-gap ships now; mechanical SM secret swap when Orion provisions service-user (multi-week ops cycle). TO scope authorized this phase = Andrew identity capture; Phase 6 stretch covers service-user flip migration when provisioning completes.
  </context>

  <objective>
    Extend `inf-jwt-trigger` Lambda to capture Eclipse JWT via Eclipse admin Token endpoint; store in SM at `orion/eclipse_jwt/current` (sibling-namespace to existing Orion JWT). Extend `jwt_freshness.py` to dual-track Orion + Eclipse JWT validation. Emit CW metrics matching Orion pattern.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/inf-jwt-trigger/index.py (or sibling) — add Eclipse JWT capture path</file>
      <file action="modify">infra/aws/lambda/{lambda-dir}/jwt_freshness.py — extend `_decode_jwt_exp` for HS256 float + HS512 int</file>
      <file action="modify">infra/aws/terraform/{path}/iam.tf — add SM read/write on `orion/eclipse_jwt/current`</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json — entry for extended Lambda</file>
      <file action="readonly_reference">DS~A feasibility brief §JWT-mechanics + Eclipse auth endpoint scope</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io inf-jwt-trigger (or sibling JWT Lambda)</run>
      <expect>Surface existing Orion JWT capture path + freshness validation. Pattern source for Eclipse extension.</expect>
    </step>
    <step>
      <run>aws secretsmanager list-secrets --filters Key=name,Values=orion/ — verify SM namespace clean for orion/eclipse_jwt/current</run>
      <expect>No conflict on sibling-namespace SM secret name.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Add Eclipse JWT capture path: GET https://www.orioneclipse.com/v1/admin/Token with Andrew identity bearer; write to SM orion/eclipse_jwt/current with metadata {eclipse_user_id, orion_user_id, expires_at, captured_at}</run>
      <expect>Sibling-pattern to Orion JWT capture; structurally consistent.</expect>
    </step>
    <step>
      <run>Extend jwt_freshness.py: `_decode_jwt_exp` supports HS256 float exp (Orion) + HS512 int exp (Eclipse); auto-detect via JWT header alg field</run>
      <expect>Dual-track validation; no Orion regression.</expect>
    </step>
    <step>
      <run>Add CW metrics: EclipseJwtExpired / EclipseJwtNearExpiry / EclipseJwtUnreadable (matching Orion pattern; same namespace)</run>
      <expect>3 new metrics emitted; alarms configurable post-deploy.</expect>
    </step>
    <step>
      <run>IAM policy extension: secretsmanager:GetSecretValue + PutSecretValue on orion/eclipse_jwt/current ARN</run>
      <expect>Lambda execution role scoped narrow; no broader perms.</expect>
    </step>
    <step>
      <run>Update lambda-source-map.json entry for inf-jwt-trigger (Eclipse-JWT files added)</run>
      <expect>Source-map current per CI drift detection contract.</expect>
    </step>
  </phase>

  <phase id="3" when="deploy">
    <step>
      <run>safe-deploy.sh per Lambda Deployment Protocol</run>
      <expect>Terraform apply 0-diff. Tag `inf-pipeline-v{X.Y.Z+1}` per current series.</expect>
    </step>
    <step>
      <run>Empirical post-deploy: invoke Lambda; verify orion/eclipse_jwt/current populated with valid Eclipse JWT; verify jwt_freshness.py validates both Orion + Eclipse JWTs without regression</run>
      <expect>Both JWTs valid; freshness metrics emitting.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `inf-jwt-trigger` Lambda captures Eclipse JWT via admin Token endpoint with Andrew identity bearer auth
    AC2: SM secret `orion/eclipse_jwt/current` populated with valid JWT + metadata {eclipse_user_id, orion_user_id, expires_at, captured_at}
    AC3: `jwt_freshness.py` `_decode_jwt_exp` supports HS256 float exp (Orion) + HS512 int exp (Eclipse); auto-detect via header alg
    AC4: Orion JWT validation regression-free post-deploy
    AC5: CW metrics emitting: EclipseJwtExpired / EclipseJwtNearExpiry / EclipseJwtUnreadable
    AC6: IAM policy scoped narrow (SM ARN-specific; no wildcard)
    AC7: lambda-source-map.json current
    AC8: safe-deploy.sh PASS + Terraform 0-diff + tag pushed per protocol
    AC9: RAVC2 to COO + CC CTO + DS~A (Phase 2 consumer of SM Eclipse JWT)
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (comp-pipescript io) before write; safe-deploy.sh per Phase 3.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: None — independent Lambda extension.
    PARALLEL-OK: ADVI_ECLDAT.002 DS~A bronze puller (stop-gap uses Andrew JWT direct pre-Phase-1; supersedes to Lambda-managed JWT post-Phase-1 ship).
    NO PORTAL CHANGES.
    SISTER-NAMESPACE: orion/eclipse_jwt/current under existing orion/* SM namespace; no new namespace.
    PHASE 6 STRETCH: service-user flip migration when Orion provisions Eclipse service-user (multi-week ops cycle; NOT in this TO scope).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Lambda + IAM + Terraform only. Activates JWT capture immediately on Lambda fire cadence.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Lambda code extension (Eclipse JWT capture)
    2. jwt_freshness.py dual-track extension
    3. CW metrics 3 new (matches Orion pattern)
    4. IAM policy extension
    5. lambda-source-map.json updated
    6. safe-deploy.sh PASS + tag pushed
    7. RAVC2 with deploy evidence
  </deliverables>

  <ravc>AE 0.6.1 RAVC2 to COO + CC CTO + DS~A on AC1-9 PASS.</ravc>

  <notes>
    **Andrew identity stop-gap:** per CTO Q3 hybrid audit trail ratify, Andrew identity bearer ships now. Service-user flip is Phase 6 stretch (NOT in this TO scope). SM metadata `{eclipse_user_id, orion_user_id}` preserves audit trail for future flip.

    **Author identity:** `--author="0.6.1_AE_PartnerETL <0.6.1_AE_PartnerETL@opal.agent>"`.

    **Sister-pattern ref:** Orion JWT capture path in `inf-jwt-trigger` is the canonical structural reference. Eclipse extension mirrors structure; differs only in auth endpoint + alg + user_id metadata.

    **No emoji per CLAUDE.md.** No production code emoji; CW metric names plain ASCII.
  </notes>
</task_order>
