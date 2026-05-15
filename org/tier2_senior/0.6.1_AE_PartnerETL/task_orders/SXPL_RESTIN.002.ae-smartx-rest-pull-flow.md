<task_order>
  <metadata>
    <id>SXPL_RESTIN.002</id>
    <slug>ae-smartx-rest-pull-flow</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-05-15</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>HELD pending Andrew's confirmation to engage AE 0.6.1 on this workstream. SmartX is the SXPL macro = PartnerETL domain, so AE 0.6.1 is the natural owner, and AE 0.6.1 is idle post-Eclipse with offered capacity. Andrew's 2026-05-15 directive scoped AE 0.6.1 to Eclipse-focus / off-TXNAMG; SmartX is a new non-TXNAMG Andrew-directed workstream so the directive's literal scope does not bind -- but COO will not re-engage AE 0.6.1 without Andrew's word. COO has surfaced this to Andrew. Released on Andrew's GO (or reassigned if Andrew routes TO-2 to a different AE).</dispatch_unblock_condition>
    <project_code>SXPL_RESTIN</project_code>
    <priority>P1 -- the whole SmartX pull flow; the first-data-goal deliverable (daily model value + holdings weights). Andrew brief section-9 "First AE TO -- the whole flow."</priority>
    <sla>~6-8h wall once unblocked.</sla>
  </metadata>

  <references>
    <brief>docs/briefs/smartx-rest-integration-design-20260515.md (commit 352ab4585) -- section-3 auth, section-4 token store, section-5 the proposed architecture + component table, section-6 endpoint manifest, section-7 modelId chaining, section-8 first-data-goal mapping, section-11 security.</brief>
    <directive>Andrew direct 2026-05-15; brief section-9 TO-2 "stand up the pull flow ... First AE TO -- the whole flow."</directive>
    <orion_pattern>The Orion parked-JWT pattern is the model: data/orion/manual_api/jwt_freshness.py (freshness-gated reader); orion/jwt/current (SM) + s3://opal-data-inf/orion/jwt/current.json. SmartX mirrors it -> smartx/jwt/current (SM) + s3://opal-data-bd/smartx/jwt/current.json.</orion_pattern>
  </references>

  <context>
    SmartX is a standards-compliant OIDC stack; a ROPC password grant works headless (brief section-2/3) -> the token refresh is a ~2-min Lambda, no EC2/browser. This TO stands up the whole pull flow per brief section-5: the smartx-jwt-refresher Lambda, the EventBridge 09:00-ET schedule, IAM, the smartx/jwt/current secret + S3 JSON, and the daily pull job that lands the first data goal (daily model value + holdings weights) to opal-data-bd. The old browser exporter (infra/aws/ec2/smartx-exporter) is NOT touched here -- its decommission is a later TO once REST parity is confirmed (brief section-5 / section-9 TO-3+).
  </context>

  <objective>
    A scheduled, headless SmartX pull: a 09:00-ET Lambda parks a fresh JWT, and a daily pull lands model value + holdings weights for the Opal models to opal-data-bd -- replacing the browser exporter's login + scrape with REST.
  </objective>

  <scope>
    <item>smartx-jwt-refresher Lambda: ROPC password grant (brief section-3) -> writes smartx/jwt/current (Secrets Manager, raw JWT) + s3://opal-data-bd/smartx/jwt/current.json (the Orion-shape JSON wrapper, brief section-4). Lambda CODE is DS-authored (brief section-5 component table: "DS writes code, AE deploys" -- coordinate with DS~B, the brief author / BD-domain owner); AE owns the Terraform deploy (CLAUDE.md Rule 1), the Lambda layer, sizing.</item>
    <item>EventBridge rule: 09:00 America/New_York daily (SmartX settles the day's data by ~9 AM ET).</item>
    <item>IAM (brief section-5): refresher role -- secretsmanager:GetSecretValue on smartx/credentials/*, Get/Put on smartx/jwt/current, s3:PutObject on opal-data-bd/smartx/jwt/*. Pull role -- s3:GetObject on opal-data-bd/smartx/jwt/*. Lock opal-data-bd/smartx/jwt/* to refresher(put)+pull(get) only (brief section-11).</item>
    <item>The JWT reader lib: generalize jwt_freshness.py to a pipeline param (orion/smartx) or a thin smartx sibling -- one real difference: SmartX uses Bearer, Orion uses Session (brief section-5). DS-authored.</item>
    <item>The daily pull job (DS-authored pull scripts, data/smartx/scripts/pull_*_rest.py, modeled on data/orion/manual_api/pull_inflection_*_rest.py): land the first data goal -- daily model value (/enterprises/aum -> performance[].closingEquity) + holdings weights (/reportedmodels/{reportedModelId}/holdings -> percentOfPortfolio), chaining modelId -> reportedModelId per brief section-7. Land raw + bronze tiers to opal-data-bd. Respect the rate limit (brief section-10 -- ~20 req/min; TO-1 confirms the exact ceiling).</item>
    <item>SCOPE BOUNDARY: this TO lands raw + bronze. Silver/gold MODELING is TO-3 (brief section-9, "scope TBD after TO-1"). Do not build silver/gold business logic here.</item>
    <item>Deploy: Terraform per CLAUDE.md Rule 1; lambda-source-map.json entry; tag; push --follow-tags. No emoji.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">smartx-jwt-refresher Lambda deployed via Terraform; on a 09:00-ET EventBridge schedule; parks a fresh JWT to smartx/jwt/current (SM) + s3://opal-data-bd/smartx/jwt/current.json (Orion-shape).</ac>
    <ac id="AC2">IAM scoped exactly per brief section-5; opal-data-bd/smartx/jwt/* locked to refresher(put)+pull(get). comp-iam after the iam.tf change.</ac>
    <ac id="AC3">The daily pull lands model value + holdings weights for the Opal models to opal-data-bd raw + bronze; JWT read via the freshness-gated reader lib; modelId->reportedModelId chained correctly; rate limit respected.</ac>
    <ac id="AC4">Credentials only from Secrets Manager -- never in code/env (brief section-11). No emoji in Lambda/pull code or logs.</ac>
    <ac id="AC5">Deployed via terraform apply to 0-diff; lambda-source-map.json updated; tagged; pushed --follow-tags. Silver/gold modeling NOT in scope (TO-3).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (before writing): comp-iam service on the new Lambda (the new IAM surface). Phase 2 (before commit): comp-iam gaps (iam.tf changed); ds-commit-gate.sh on any DS-authored .py. Phase 3 (after deploy): deployed-verify; confirm the 09:00-ET schedule fires + parks a JWT + the pull lands bronze.</compiler_tools_mandate>

  <cross_domain_coordination>
    DS-CODE COORDINATION: per brief section-5, DS authors the Lambda code + the pull scripts + the JWT reader lib; AE owns Terraform/IAM/EventBridge/deploy. Coordinate the code with DS~B (brief author, BD-domain / ModelPortfolios owner). AE 0.6.1 drives this TO end-to-end; DS~B is the code contributor. If AE 0.6.1 + DS~B prefer to split the code vs infra into sub-TOs operationally, surface to COO.
    RUNS PARALLEL to TO-1: TO-2's two first-data-goal endpoints (/enterprises/aum, /reportedmodels/{id}/holdings) are PROBE-confirmed in the brief (section-6.2) -- TO-2 does not block on TO-1. TO-1's full matrix refines TO-3 (silver/gold).
    The smartx-exporter EC2 is NOT touched -- decommission is a later TO (brief section-9 TO-3+) once REST parity is confirmed.
    opal-data-bd colocation: SmartX JWT + data land in opal-data-bd (Andrew 2026-05-15 -- SmartX feeds 49F/BD-domain work).
  </cross_domain_coordination>

  <deliverables>
    <item>smartx-jwt-refresher Lambda + EventBridge + IAM + the smartx/jwt/current secret -- Terraform-deployed, 0-diff, tagged, pushed.</item>
    <item>The daily pull landing model value + holdings weights to opal-data-bd raw+bronze; the JWT reader lib.</item>
    <item>Session log + RAVC2 to COO + CC CTO + DS~B.</item>
  </deliverables>

  <ravc>AE 0.6.1 RAVC2 to COO + CC CTO + DS~B on AC1-5.</ravc>

  <notes>
    STAGED -- do not start until COO releases dispatch_held on Andrew's word (see dispatch_unblock_condition). The brief (352ab4585) is the authoritative design -- section-5 is the architecture, do not re-derive. Andrew framed TO-2 as "the whole flow" in one TO; the DS-code / AE-infra split is internal to it -- coordinate with DS~B. Silver/gold modeling is explicitly TO-3, not this TO -- land raw+bronze and stop. The smartx/credentials/* secrets are a real Manager-role SmartX login -- Secrets-Manager-only, never in code (brief section-11).
  </notes>
</task_order>
