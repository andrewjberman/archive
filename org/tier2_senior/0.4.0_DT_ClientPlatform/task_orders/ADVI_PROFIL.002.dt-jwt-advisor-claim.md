<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-jwt-claim</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <co_owner>0.7.0_AE_CloudOps</co_owner>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Plumb an `advisorId` claim through the JWT issuance + validation + frontend Claims interface pipeline so non-admin advisors can reach their own `AdvisorPublicProfile` via Tab 3 of `/advisor-intelligence`. This is a multi-layer change: (a) token issuance at the auth source (`portal-auth` pipeline / login Lambda), (b) token validation at the edge (`auth-validator-edge` Lambda@Edge), (c) `Claims` interface update in the portal frontend (`portal/src/contexts/AuthContext.context.ts`), (d) user→advisor mapping at the auth source. After this TO lands, `const { claims } = useAuth(); claims.advisorId` resolves to the authenticated user's advisor id on non-admin accounts.
  </objective>

  <context>
    RD shipped the non-admin Tab 3 path in .001 but it currently renders an "Advisor Identity Unavailable" centered-panel fallback at runtime because `portal/src/contexts/AuthContext.context.ts` defines `Claims` with only `firmId: string | null` and `userType: 'Dev' | null` — no `advisorId` field. The fallback path auto-activates the moment `claims.advisorId` becomes non-null; all of the frontend infrastructure is already typed and wired.

    AdvisorIntelligence.tsx:153 currently reads the claim via a defensive cast:
    ```
    (claims as unknown as { advisorId?: string })?.advisorId ?? null
    ```
    That cast is expected to be removed in this TO once `Claims` is properly extended.

    Ownership split: DT owns the portal-side Claims interface update (frontend TypeScript) and the commit+push on portal DEV. AE owns the auth-validator-edge Lambda@Edge changes and the portal-auth login Lambda changes where user→advisor mapping and claim-set issuance happen. Both sides must coordinate on the claim NAME (`advisorId`), the claim VALUE TYPE (`string` — likely a UUID or a BD `advisor_id`), and the SOURCE OF TRUTH for user→advisor mapping (likely a DynamoDB lookup or a column in the existing portal-auth user table — AE's call after reading the portal-auth schema).

    Cross-layer dependency: .004 (ae-advisor-scoping-enforcement) blocks on .002. The Lambda@Edge scoping rule in .004 reads `jwt.advisorId` to enforce per-advisor scoping on the Lambda-served platinum endpoints. Until .002 lands, .004 has nothing to enforce.

    Cross-layer dependency: .007 (rd-admin-my-profile-toggle) also blocks on .002, because the toggle only appears when `claims.advisorId` is non-null (i.e., an admin user who is also an advisor).
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - Read the current JWT issuance chain: `infra/aws/lambda/portal-auth/**/lambda_function.py`. Identify where claims are assembled (likely a dict returned by the login handler, passed through to `jwt.encode`).
    - Read `auth-validator-edge` Lambda@Edge source (location: check `infra/aws/lambda/` or the Lambda source-map — `infra/aws/lambda/ci/lambda-source-map.json`). Identify where claims are extracted from the validated JWT and passed to downstream handlers.
    - Read `portal/src/contexts/AuthContext.context.ts` in full. Understand how `Claims` is currently consumed (`useAuth()` hook, `claims.firmId`, `claims.userType` call sites).
    - `comp-routes` on `/api/scoped/partners/books/advisor/*` and `platinum/advisors/*` — understand the full serving path so .004 (Wave 2) can reuse the edge changes you land here.
    - `comp-blast auth-validator-edge` — identify everything downstream of the edge Lambda that reads claims. Confirm nothing breaks when a new optional field is added.

    Phase 2 (during implementation):
    - DT side: extend `Claims` TypeScript interface additively: `advisorId?: string | null`. Do NOT make it required — it will be `null` for admin users who are not also advisors.
    - DT side: remove the `as unknown as { advisorId?: string }` cast in `AdvisorIntelligence.tsx:153` once the interface is live.
    - AE side: the claim value must come from a deterministic user→advisor mapping. Options: (a) add an `advisor_id` column to the `portal-auth` user table (if one exists), (b) join against the `bd-securities` / advisor-dimension table at login time, (c) lookup in a new DynamoDB table keyed by user email / cognito sub. AE picks and documents the decision.
    - AE side: add the advisorId claim to the JWT payload at issuance. Validate it survives through the edge Lambda verification path (JWT signature check should just pass through unknown fields).
    - Terraform/deploy: follow the standard Lambda deploy protocol (commit code → write Terraform if new resources → update source map → git commit → terraform plan → terraform apply → verify 0-diff → git tag → push --follow-tags). Tag: `portal-auth-v1.11.{next}` after running `git tag -l "portal-auth-v*" | sort -V | tail -5` to find the current version.

    Phase 3 (after deploy):
    - AE runs `comp-routes --update` to refresh the serving path graph.
    - Integration test: login as a known non-admin advisor account (Andrew provides the test account), decode the JWT (or inspect the claims propagated to a downstream Lambda via CloudWatch logs), verify `advisorId` is present and matches the expected value.
    - DT: deploy portal DEV with the Claims interface update, verify `claims.advisorId` resolves at runtime (non-admin test account). The "Advisor Identity Unavailable" fallback should be replaced by a rendered AdvisorPublicProfile.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/contexts/AuthContext.context.ts` — .002 (DT extends Claims), .007 (rd-admin-my-profile-toggle reads `claims.advisorId`). Ordering: .007 blocks on .002.
    shared_resource: `auth-validator-edge` Lambda@Edge (AE territory) — .002 (AE adds claim), .004 (AE enforces scoping using the claim). Ordering: .004 blocks on .002. Same Lambda, two separate passes.
    shared_resource: `infra/aws/lambda/portal-auth/` (portal-auth login Lambda) — AE owns. DT does not touch. Deployment tag: `portal-auth-v1.11.{next}`.
    shared_resource: JWT claim name `advisorId` — DT and AE must agree on the exact spelling (camelCase, matches existing `firmId`). Value type: `string` (nullable in TS, absent-or-null in JWT for non-advisor users).
    last_write_owner: AE 0.7.0 for auth-validator-edge + portal-auth Lambda and terraform. DT 0.4.0 for AuthContext.context.ts and portal DEV commit.
    required_action: "Coordinate with AE 0.7.0_AE_CloudOps before landing any changes. Agree on (a) claim name, (b) claim value type, (c) user→advisor mapping source of truth, (d) deploy ordering (AE deploys backend first, DT deploys frontend Claims interface second — otherwise the frontend type-checks against a claim the backend isn't issuing yet, and runtime falls back to null silently). Send message via MCP broker to 0.7.0_AE_CloudOps with the agreed spec before starting."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Claim name agreed:** `advisorId` (camelCase, matches existing `firmId`, `userType`). Documented in both the portal-auth Lambda source and the frontend Claims interface.
    2. **AE: portal-auth login Lambda issues `advisorId`:** The claim is present in the JWT payload for non-admin advisor accounts, absent or `null` for accounts that have no advisor mapping. User→advisor mapping source of truth documented in the session log with rationale.
    3. **AE: auth-validator-edge passes `advisorId` through:** The edge Lambda's JWT validation does not strip or reject the new claim. Unknown-claim passthrough is the default behavior, but verify explicitly.
    4. **AE: Terraform deployed:** `portal-auth` pipeline tag bumped (`portal-auth-v1.11.{next}` after checking `git tag -l "portal-auth-v*" | sort -V | tail -5`), 0-diff plan verified, source map updated, git tag pushed with `--follow-tags`.
    5. **DT: Claims interface extended:** `portal/src/contexts/AuthContext.context.ts` adds `advisorId: string | null` to the `Claims` type (optional or nullable — AE picks). Additive; no breaking change to existing `firmId`/`userType` readers.
    6. **DT: Defensive cast removed:** `AdvisorIntelligence.tsx:153` reads `claims.advisorId` directly (no `as unknown as` cast).
    7. **DT: Portal DEV commit + push:** Change committed with `--author=0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>`, pushed to portal DEV.
    8. **Runtime verification:** Non-admin test account (Andrew provides) logs in, reaches Tab 3 "Profile", sees their own AdvisorPublicProfile rendered (not the "Advisor Identity Unavailable" fallback). Admin account sees Tab 3 "Books" unchanged. Verification logged in the session log with screenshots or a browser-devtools snippet.
    9. **Integration test:** Decode JWT for a known non-admin account, verify `advisorId` is present and matches the expected BD advisor id. Logged in the session log.
    10. **Session log:** Documents the user→advisor mapping decision, the claim spec, the portal-auth tag + SHA, the portal DEV commit SHA, the DT+AE coordination message history, and the compiler tools output from Phases 1-3.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify" owner="AE">infra/aws/lambda/portal-auth/{login handler}/lambda_function.py</file>
      <file action="modify" owner="AE">infra/aws/lambda/{auth-validator-edge path}/lambda_function.py</file>
      <file action="modify" owner="AE">infra/aws/terraform/portal-auth/** (if a new Terraform resource is needed for the user→advisor mapping, e.g. a DynamoDB table)</file>
      <file action="reference" owner="AE">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify" owner="DT">portal/src/contexts/AuthContext.context.ts</file>
      <file action="modify" owner="DT">portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx (remove line 153 cast)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">AE and DT MUST coordinate via MCP broker BEFORE touching code. Agree on claim name (`advisorId`), value type (`string | null`), and user→advisor mapping source of truth. Document the agreement in both session logs.</requirement>
    <requirement id="2">Deploy ordering: AE ships backend first (Lambda + Terraform), then DT ships frontend Claims interface update. Rationale: if the frontend ships first, it type-checks against a claim the backend isn't issuing yet and runtime silently falls back to null, masking the real AE work.</requirement>
    <requirement id="3">Follow the standard Lambda deployment protocol (CLAUDE.md rule #1-6): Terraform-only, commit-before-apply, source map update, annotated tag, --follow-tags push. No `aws lambda update-function-code`.</requirement>
    <requirement id="4">Do NOT issue the `advisorId` claim for internal Opal admin users — they do not have an advisor identity. Claim should be `null` or absent for admin users. The frontend expects that (`isFirmAdmin` readers are unaffected).</requirement>
    <requirement id="5">Do NOT attempt to enforce scoping at this layer. Scoping is .004's job. .002 is claim-issuance only. The Lambda@Edge changes here are strictly about adding the claim to the verified JWT payload, not checking path matches.</requirement>
    <requirement id="6">The Claims interface update must be additive. Existing callers of `claims.firmId` and `claims.userType` must not break. Use `advisorId: string | null` (nullable) to match the existing convention on `firmId`.</requirement>
    <requirement id="7">If AE discovers the user→advisor mapping requires a new DynamoDB table or Terraform resource, the Terraform work lives in `infra/aws/terraform/portal-auth/` (or a new shared-infra module — AE's choice). Follow the sharded pipeline strategy in `infra/aws/TERRAFORM_PIPELINE_STRATEGY.md`.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="code" owner="AE">portal-auth login Lambda modified to issue `advisorId` claim. Terraform (if needed) for user→advisor mapping. Source map updated. Committed with `--author=0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>`.</deliverable>
    <deliverable type="code" owner="AE">auth-validator-edge Lambda verified to pass through the new claim. Modified only if passthrough is not automatic.</deliverable>
    <deliverable type="tag" owner="AE">`portal-auth-v1.11.{next}` annotated git tag pushed with `--follow-tags`.</deliverable>
    <deliverable type="code" owner="DT">portal/src/contexts/AuthContext.context.ts extended with `advisorId: string | null`. AdvisorIntelligence.tsx:153 cast removed. Committed with `--author=0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>`, pushed to portal DEV.</deliverable>
    <deliverable type="document" owner="AE">Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-10/advi_profil_002_jwt_claim.md` with the mapping decision, the deploy tag, the integration test output, and the compiler tools log.</deliverable>
    <deliverable type="document" owner="DT">Session log at `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-10/advi_profil_002_claims.md` with the interface update, the portal DEV commit SHA, the runtime verification screenshot/output, and the AE coordination message history.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start this TO until DT and AE have exchanged an MCP broker message agreeing on claim name, value type, and user→advisor mapping source.</rule>
    <rule>Do NOT enforce scoping in auth-validator-edge in this TO. That is .004's job. Keep this TO strictly additive to the claim set.</rule>
    <rule>Do NOT issue `advisorId` for internal Opal admin users.</rule>
    <rule>Do NOT use `aws lambda update-function-code` or bypass Terraform. All Lambda deploys go through the standard protocol.</rule>
    <rule>Do NOT ship frontend Claims interface update before AE has deployed the backend claim issuance. Ordering is backend-first.</rule>
    <rule>Do NOT commit frontend code under the AE author or vice-versa. Each side owns its own commit author.</rule>
  </do_not>
</task_order>
