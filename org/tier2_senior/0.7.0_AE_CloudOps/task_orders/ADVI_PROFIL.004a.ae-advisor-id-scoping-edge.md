<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-scoping-004a</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <co_owner>0.4.0_DT_ClientPlatform</co_owner>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
    <supersedes>ADVI_PROFIL.004.ae-advisor-scoping-enforcement.md (single-TO scoping, replaced after CTO comp-routes audit caught the two-behavior + ownership-map split)</supersedes>
  </metadata>

  <objective>
    Enforce non-admin advisor scoping at `shared-advisor-router` Lambda@Edge for the SIMPLE case: endpoints where the URL path parameter is literally `{advisorId}`. Rule: `if !isAdmin(jwt) and path[advisorId] != jwt.advisorId: return 403`. Admin bypass preserved. This is Wave 2a and unblocks the Profile + Timeseries serving path independently of .005. .004b/.004c handle the ownership-mapped account/relationship paths separately.
  </objective>

  <context>
    CTO `comp-routes` audit (logged in `org/compiler-tools-log.md` 2026-04-10) surfaced that the advisor-scoping work is NOT a single TO. The audit found:

    1. **Two CloudFront behaviors, two origins.** Not a stylistic choice — load-bearing.
       - `/api/scoped/partners/*` → `APIGateway-portal` origin (API GW can enforce, but we pick edge for single choke point)
       - `/api/scoped/advisor-intelligence/*.json` → `S3-opal-data-bd` direct origin (edge is the ONLY control point; API GW is not in the path)
    2. **Four advisor endpoints split by path-key type.** Two key by `{advisorId}` (simple compare — this TO), two key by `{accountId}` or `{relationshipId}` (require an advisor→{accounts, relationships} ownership map — .004b + .004c).
    3. **`getPlatinumAdvisorSummary` and `getPlatinumAdvisorDrilldownSummary` share a URL.** Two TS wrappers extracting different shapes from one backend response. One scoping rule covers both.

    Route map from `comp-routes trace` (PRD §5.1):

    | Endpoint | URL | CF Behavior | Origin | Path-key | In scope for |
    |---|---|---|---|---|---|
    | getPlatinumAdvisorSummary | `/api/scoped/partners/books/advisor/{advisorId}/platinum-summary?firmId=...` | `/api/scoped/partners/*` | `APIGateway-portal` | `{advisorId}` | **.004a** |
    | getPlatinumAdvisorDrilldownSummary | **same URL** (TS wrapper) | same | same | `{advisorId}` | **.004a** (covered by above) |
    | getPlatinumAdvisorTimeseries | `/api/scoped/advisor-intelligence/platinum/advisors/{advisorId}/timeseries.json` | `/api/scoped/advisor-intelligence/*.json` | `S3-opal-data-bd` (edge-only) | `{advisorId}` | **.004a** |
    | getPlatinumAccountSummary | `/api/scoped/advisor-intelligence/platinum/accounts/{accountId}/summary.json` | `/api/scoped/advisor-intelligence/*.json` | `S3-opal-data-bd` (edge-only) | `{accountId}` | .004c |
    | getPlatinumClientSummary | `/api/scoped/partners/books/relationship/{relationshipId}/platinum-summary?firmId=...` | `/api/scoped/partners/*` | `APIGateway-portal` | `{relationshipId}` | .004c |

    **.004a ships independently.** It unblocks the non-admin Profile+Timeseries surface — the core ADVI_PROFIL value — without waiting for the ownership map work. .004b+.004c block on .005 RD lift anyway (they only matter once non-admins can drill into their own clients/accounts from the Book view).
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - Verify .002 is fully deployed: `git tag -l "portal-auth-v*" | sort -V | tail -5`, confirm the bump that introduced `advisorId` to the JWT. Decode a non-admin test JWT and confirm `advisorId` is present.
    - `comp-routes trace getPlatinumAdvisorSummary` and `comp-routes trace getPlatinumAdvisorTimeseries` — re-run and confirm the CTO route map still holds. If CloudFront behavior or origin has drifted, escalate before starting.
    - `comp-blast shared-advisor-router` — identify every downstream consumer. Confirm the two path templates in scope (`{advisorId}` under `/api/scoped/partners/books/advisor/` and under `/api/scoped/advisor-intelligence/platinum/advisors/`) are the complete set.
    - Read `shared-advisor-router` Lambda source in full (the existing router; location via lambda-source-map.json). Understand the admin-check primitive and the existing firmId-scoping path you will parallel.
    - Read the existing path-pattern matching logic in the router. If none exists, design one that is reusable for .004c later.

    Phase 2 (during implementation):
    - Path pattern regexes (document in code comment):
      - `^/api/scoped/partners/books/advisor/([^/]+)/.*$` — API GW origin path
      - `^/api/scoped/advisor-intelligence/platinum/advisors/([^/]+)/.*\.json$` — S3-direct origin path
    - Enforcement rule placement: AFTER admin bypass, BEFORE any downstream forwarding. The new rule runs in addition to the existing firmId scoping, not instead.
    - Structured denial logging: `log.warn("advisor_scoping_denied", {userId: jwt.sub, requestedAdvisor: pathAdvisorId, jwtAdvisor: jwt.advisorId, path: request.path, rule: "004a"})`. Including the rule name makes CloudWatch filtering easier when .004c ships.
    - Non-admin with `jwt.advisorId == null` must be rejected (403). No advisor identity → no advisor endpoint access.
    - Design for .004c reuse: wrap the path-matching + advisor check in a helper that .004c can extend with ownership-map lookup rather than duplicating the pattern logic.

    Phase 3 (after deploy):
    - Integration test matrix (all curl commands logged in the session log with actual responses):
      1. Non-admin A (advisorId=A) → `/api/scoped/partners/books/advisor/A/platinum-summary` → expect 200
      2. Non-admin A → `/api/scoped/partners/books/advisor/OTHER/platinum-summary` → expect 403
      3. Admin → `/api/scoped/partners/books/advisor/ANY/platinum-summary` → expect 200
      4. Non-admin A → `/api/scoped/advisor-intelligence/platinum/advisors/A/timeseries.json` → expect 200
      5. Non-admin A → `/api/scoped/advisor-intelligence/platinum/advisors/OTHER/timeseries.json` → expect 403
      6. Admin → `/api/scoped/advisor-intelligence/platinum/advisors/ANY/timeseries.json` → expect 200
      7. Non-admin with `jwt.advisorId == null` → any of the above → expect 403
    - Verify the `getPlatinumAdvisorDrilldownSummary` TS wrapper works through case 1/2/3 — they hit the SAME URL so the single rule covers both wrappers.
    - `comp-routes --update` after deploy; `comp-blast shared-advisor-router` re-run to confirm no unexpected new downstream edges.
    - CloudWatch: confirm structured denial events for the 403 cases.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `shared-advisor-router` Lambda@Edge. .002 (AE adds `advisorId` to verified JWT claim set), .004a (AE consumes claim for enforcement), .004c (AE extends with ownership-map lookup). Ordering: .004a blocks on .002 full deploy; .004c blocks on .004a (shared helper) + .004b (ownership map artifact).
    shared_resource: Lambda deployment pipeline for shared-advisor-router. Tag bump via standard protocol. Current pipeline: check `git tag -l "shared-infra-v*" | sort -V | tail -5` — likely `shared-infra-v1.6.{next}` unless the router lives in its own pipeline.
    shared_resource: Path-matching helper introduced in .004a — .004c extends it. Design for reuse.
    last_write_owner: 0.7.0_AE_CloudOps for Lambda@Edge + Terraform. DT coordinates CloudFront invalidation.
    required_action: "Do NOT start until .002 is fully deployed AND the non-admin test JWT decodes to show `advisorId`. Verify first, then proceed. Coordinate CloudFront invalidation window with DT — Lambda@Edge changes propagate globally over 5-15 minutes and will start enforcing the moment they land."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Path patterns documented:** Two regex patterns in the router code, commented with the CF behavior and origin each matches.
    2. **Single rule covers both wrappers:** `getPlatinumAdvisorSummary` and `getPlatinumAdvisorDrilldownSummary` both pass/reject identically because they hit the same URL. Verified in the integration test.
    3. **Enforcement placement:** Rule runs AFTER admin bypass and BEFORE downstream forwarding. Existing firmId check and admin bypass unchanged.
    4. **Null `advisorId` rejected:** Non-admin with `jwt.advisorId == null` gets 403 on any scoped advisor endpoint.
    5. **Structured denial logging:** CloudWatch event emitted on every 403 with `userId`, `requestedAdvisor`, `jwtAdvisor`, `path`, `rule: "004a"`. Documented event shape in session log.
    6. **Helper designed for .004c reuse:** Path-matching + advisor-check logic is wrapped in a reusable helper, not inlined. .004c will extend it with an ownership-map lookup step.
    7. **Lambda deploy via standard protocol:** Terraform 0-diff verified, source map updated, `shared-infra-v1.6.{next}` (or equivalent) tag pushed with `--follow-tags`.
    8. **Integration test matrix (7 cases) passed:** All curls logged in session log with response codes and CloudWatch event excerpts.
    9. **Prerequisite verified:** .002 is fully deployed before .004a starts. Non-admin test JWT decodes with `advisorId`. Logged.
    10. **No backend Lambda changes:** The `opal-partners-data` Lambda (backing `getPlatinumAdvisorSummary`) and any S3 read path are unchanged. Router is the choke point.
    11. **Session log:** Includes the prerequisite verification, regex patterns, helper design, integration test matrix, deploy tag, CloudFront invalidation id, and compiler tools log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/{shared-advisor-router path}/lambda_function.py (or equivalent)</file>
      <file action="modify">infra/aws/terraform/{owning pipeline}/** (if any Terraform changes needed)</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="reference">auth-validator-edge (verify .002 claim is available)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT start until .002 is fully deployed. Verify by decoding a non-admin test JWT and confirming `advisorId` is present.</requirement>
    <requirement id="2">Cover BOTH path patterns in this single TO — API GW-origin `/api/scoped/partners/books/advisor/{advisorId}/...` AND S3-direct `/api/scoped/advisor-intelligence/platinum/advisors/{advisorId}/...`. Both have the same rule (simple advisorId compare), so one TO is sufficient.</requirement>
    <requirement id="3">Do NOT include account-id or relationship-id paths in this TO. Those are .004c and require the ownership map from .004b.</requirement>
    <requirement id="4">Design the path-matching + advisor-check as a reusable helper. .004c will extend it. Duplicating logic between .004a and .004c is a QA failure.</requirement>
    <requirement id="5">Follow the standard Lambda deployment protocol. No `aws lambda update-function-code`. Terraform-only.</requirement>
    <requirement id="6">Null `jwt.advisorId` for non-admin users must reject with 403. Do not fail-open.</requirement>
    <requirement id="7">Structured denial logging is mandatory. Include `rule: "004a"` in the event to enable filtering when .004c lands.</requirement>
    <requirement id="8">Preserve existing firmId scoping and admin bypass. .004a is strictly additive.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Router Lambda modified with .004a enforcement + reusable helper. Committed with `--author=0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>`.</deliverable>
    <deliverable type="tag">`shared-infra-v1.6.{next}` (or equivalent) annotated git tag pushed with `--follow-tags`.</deliverable>
    <deliverable type="source_map">`infra/aws/lambda/ci/lambda-source-map.json` entry updated.</deliverable>
    <deliverable type="test">Integration test matrix (7 cases) executed and logged.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_profil_004a_scoping.md` with prerequisite verification, regex patterns, helper design, integration test output, deploy tag, invalidation id, and compiler tools log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start before .002 is fully deployed. Verify first.</rule>
    <rule>Do NOT include account/relationship paths. Those are .004c.</rule>
    <rule>Do NOT modify backend Lambdas (opal-partners-data, etc.). Router is the choke point.</rule>
    <rule>Do NOT use `aws lambda update-function-code`. Terraform-only.</rule>
    <rule>Do NOT skip the structured denial logging.</rule>
    <rule>Do NOT inline the helper logic — design for .004c reuse.</rule>
    <rule>Do NOT weaken or remove existing firmId scoping.</rule>
  </do_not>
</task_order>
