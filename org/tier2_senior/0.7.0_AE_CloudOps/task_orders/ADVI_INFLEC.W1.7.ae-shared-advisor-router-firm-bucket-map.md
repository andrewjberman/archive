<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.7-shared-advisor-router-map</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Add `'inflection': 'inf'` entry to `FIRM_BUCKET_MAP` in `infra/aws/lambda-edge/shared-advisor-router/index.mjs` (around L175). Identical edit to W1.6 in a different file — both maps MUST stay in sync. Co-deploy with W1.6.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.2 row 4. Paired with W1.6. `shared-advisor-router` runs on origin-request for `/api/scoped/advisor-intelligence/*.json` behavior — rewrites S3 paths to the firm-scoped bucket based on FIRM_BUCKET_MAP. Without this edit, Inflection JWT would pass auth-validator-edge (W1.6) but shared-advisor-router couldn't route → 404 or incorrect-bucket read.

    Mechanically identical to W1.6; see W1.6 context for map-entry shape + CloudFront propagation notes.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>grep -n "FIRM_BUCKET_MAP" infra/aws/lambda-edge/shared-advisor-router/index.mjs</run>
    <expect>Map location confirmed (~L175 per PRD §4.2 row 4).</expect>

    <run>diff <(grep -A 20 "FIRM_BUCKET_MAP" infra/aws/lambda-edge/auth-validator-edge/index.mjs) <(grep -A 20 "FIRM_BUCKET_MAP" infra/aws/lambda-edge/shared-advisor-router/index.mjs)</run>
    <expect>Same set of firmId keys (may differ in ordering/formatting but same semantics). If the maps are already out of sync today, flag to CTO before making the inflection change.</expect>

    Phase 2 (during implementation):
    Same as W1.6 phase 2 (Terraform plan + apply).

    Phase 3 (after deploy):
    <run>comp-routes trace getPlatinumAccountSummary</run>
    <expect>Route map unchanged; shared-advisor-router Lambda version bumped.</expect>

    Integration test — paired with W1.6 test matrix. A single curl cycle validates both:
    1. Inflection JWT → advisor-intelligence S3 path → shared-advisor-router rewrites to opal-data-inf → 200.
    2. 49F JWT → same path → opal-data-bd → 200.
    3. Inflection JWT → endpoint needing advisor-scoping on {accountId} (W5.6 smoke cases 6-7) → 200 if own account, 403 if not. Confirms existing .004c logic unaffected.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: shared-advisor-router Lambda@Edge + existing ADVI_PROFIL.004c logic in same file.
    also_in_to: W1.6 (auth-validator-edge — co-deploy).
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "Co-commit with W1.6 (single commit, two file edits, one Terraform apply). After Lambda@Edge deploy, wait ≥15 min + run joint integration test. Do NOT edit shared-advisor-router in any other dimension in this TO — ADVI_PROFIL.004c logic is load-bearing."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `index.mjs` FIRM_BUCKET_MAP includes `'inflection': 'inf'`.
    2. Map is in sync with W1.6 (same firmId keyset).
    3. Lambda@Edge redeployed; CloudFront Status `Deployed`.
    4. Joint integration test with W1.6: Inflection + 49F + .004c advisor-scoping paths all pass.
    5. No refactor of `.004c` advisor-scoping logic. Additive only.
    6. Tag (co-deploy with W1.6 — likely single portal-auth-v{next}).
    7. Source map + session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/shared-advisor-router/index.mjs</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Map entry identical to W1.6: `'inflection': 'inf'`.</requirement>
    <requirement id="2">Preserve ADVI_PROFIL.004a/.004c advisor-scoping logic byte-for-byte. No refactor.</requirement>
    <requirement id="3">Co-commit + co-deploy with W1.6.</requirement>
    <requirement id="4">≥15 min propagation wait before integration test.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">index.mjs + source map. Co-commit with W1.6 (same commit or adjacent commit same Terraform apply).</deliverable>
    <deliverable type="tag">Joint with W1.6.</deliverable>
    <deliverable type="document">Session log (may be shared section with W1.6).</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT refactor ADVI_PROFIL.004c logic.</rule>
    <rule>Do NOT deploy independent of W1.6.</rule>
    <rule>Do NOT skip the sync check vs auth-validator-edge.</rule>
  </do_not>
</task_order>
