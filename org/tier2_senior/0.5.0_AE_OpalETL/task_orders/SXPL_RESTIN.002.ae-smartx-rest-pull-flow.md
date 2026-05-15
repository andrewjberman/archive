<task_order>
  <metadata>
    <id>SXPL_RESTIN.002</id>
    <slug>ae-smartx-rest-pull-flow</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-15</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RELEASED + RE-ADDRESSED 2026-05-15. This TO was briefly staged pending Andrew's word on the AE assignment. Andrew directed (2026-05-15, via DS~B): "send this work to the 0.5.0_AE_OpalETL agent ... it makes more sense to do these kind of operations with the Opal agent rather than a partner agent because it's shared resources." TO-2 re-addressed from 0.6.1_AE_PartnerETL to 0.5.0_AE_OpalETL and dispatched GO. NOTE: TO-2's DS-authored data/smartx/ pull-script commits gate on the separate data/smartx/ .owned-paths lane decision (routed to CTO) -- the AE Terraform/IAM/EventBridge work has no such gate; sequence accordingly.</dispatch_unblock_condition>
    <project_code>SXPL_RESTIN</project_code>
    <priority>P1 -- the whole SmartX pull flow; the first-data-goal deliverable (daily model value + holdings weights). Andrew brief section-9 "First AE TO -- the whole flow."</priority>
    <sla>~6-8h wall.</sla>
  </metadata>

  <references>
    <brief>docs/briefs/smartx-rest-integration-design-20260515.md (commit 352ab4585) -- section-3 auth, section-4 token store, section-5 the proposed architecture + component table, section-6 endpoint manifest, section-7 modelId chaining, section-8 first-data-goal mapping, section-11 security.</brief>
    <to1_deliverable>docs/briefs/smartx-per-model-availability-matrix-20260515.md (TO-1, commit bd5d7d068, COO-validated) -- the 7-model x 13-endpoint availability matrix + the confirmed first-data-goal mapping + the 7-pair modelId/reportedModelId table. Use it: TO-1 confirmed the daily-value + holdings endpoints, dropped legacy api/3.0 from scope, and confirmed no historical-holdings endpoint (daily-snapshot model).</to1_deliverable>
    <directive>Andrew direct 2026-05-15; brief section-9 TO-2 "stand up the pull flow ... First AE TO -- the whole flow." Andrew 2026-05-15 also directed the receiver: 0.5.0_AE_OpalETL (SmartX = shared Opal resources -> the Opal ETL agent).</directive>
    <orion_pattern>The Orion parked-JWT pattern is the model: data/orion/manual_api/jwt_freshness.py (freshness-gated reader); orion/jwt/current (SM) + s3://opal-data-inf/orion/jwt/current.json. SmartX mirrors it -> smartx/jwt/current (SM) + s3://opal-data-bd/smartx/jwt/current.json.</orion_pattern>
  </references>

  <context>
    SmartX is a standards-compliant OIDC stack; a ROPC password grant works headless (brief section-2/3) -> the token refresh is a ~2-min Lambda, no EC2/browser. This TO stands up the whole pull flow per brief section-5: the smartx-jwt-refresher Lambda, the EventBridge 09:00-ET schedule, IAM, the smartx/jwt/current secret + S3 JSON, and the daily pull job that lands the first data goal (daily model value + holdings weights) to opal-data-bd. The old browser exporter (infra/aws/ec2/smartx-exporter) is NOT touched here -- its decommission is a later TO once REST parity is confirmed (brief section-5 / section-9 TO-3+). TO-1 is complete: its per-model availability matrix confirms the endpoints + the modelId/reportedModelId pairs this TO pulls.
  </context>

  <objective>
    A scheduled, headless SmartX pull: a 09:00-ET Lambda parks a fresh JWT, and a daily pull lands model value + holdings weights for the Opal models to opal-data-bd -- replacing the browser exporter's login + scrape with REST.
  </objective>

  <scope>
    <item>smartx-jwt-refresher Lambda: ROPC password grant (brief section-3) -> writes smartx/jwt/current (Secrets Manager, raw JWT) + s3://opal-data-bd/smartx/jwt/current.json (the Orion-shape JSON wrapper, brief section-4). Lambda CODE is DS-authored (brief section-5 component table: "DS writes code, AE deploys" -- coordinate with DS~B, the brief author / BD-domain owner); 0.5.0_AE_OpalETL owns the Terraform deploy (CLAUDE.md Rule 1), the Lambda layer, sizing.</item>
    <item>EventBridge rule: 09:00 America/New_York daily (SmartX settles the day's data by ~9 AM ET).</item>
    <item>IAM (brief section-5): refresher role -- secretsmanager:GetSecretValue on smartx/credentials/*, Get/Put on smartx/jwt/current, s3:PutObject on opal-data-bd/smartx/jwt/*. Pull role -- s3:GetObject on opal-data-bd/smartx/jwt/*. Lock opal-data-bd/smartx/jwt/* to refresher(put)+pull(get) only (brief section-11).</item>
    <item>The JWT reader lib: generalize jwt_freshness.py to a pipeline param (orion/smartx) or a thin smartx sibling -- one real difference: SmartX uses Bearer, Orion uses Session (brief section-5). DS-authored.</item>
    <item>The daily pull job (DS-authored pull scripts, data/smartx/scripts/pull_*_rest.py, modeled on data/orion/manual_api/pull_inflection_*_rest.py): land the first data goal -- daily model value (/enterprises/aum -> performance[].closingEquity) + holdings weights (/reportedmodels/{reportedModelId}/holdings -> percentOfPortfolio), chaining modelId -> reportedModelId per brief section-7 + the TO-1 7-pair table. Land raw + bronze tiers to opal-data-bd. Respect the rate limit (TO-1: ~17/min clean, 20/min safe planning ceiling).</item>
    <item>SCOPE BOUNDARY: this TO lands raw + bronze. Silver/gold MODELING is TO-3 (brief section-9, scoped after TO-1). Do not build silver/gold business logic here.</item>
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
    DS-CODE COORDINATION: per brief section-5, DS authors the Lambda code + the pull scripts + the JWT reader lib; the AE owns Terraform/IAM/EventBridge/deploy. Coordinate the code with DS~B (brief author, BD-domain / ModelPortfolios owner). 0.5.0_AE_OpalETL drives this TO end-to-end; DS~B is the code contributor. If 0.5.0_AE_OpalETL + DS~B prefer to split the code vs infra into sub-TOs operationally, surface to COO.
    LANE DEPENDENCY: the DS-authored data/smartx/ pull scripts hit the data/smartx/ .owned-paths lane registration (currently POD3). COO has routed the lane decision to CTO. The AE Terraform/IAM/EventBridge work (infra/) has no lane gate -- proceed; the data/smartx/ DS-code commits gate on CTO's lane ruling. Surface to COO if the lane is unresolved when the code is ready to commit.
    RUNS PARALLEL to / AFTER TO-1: TO-1 is complete (matrix brief bd5d7d068) -- its first-data-goal endpoints are confirmed; this TO builds against them.
    The smartx-exporter EC2 is NOT touched -- decommission is a later TO (brief section-9 TO-3+) once REST parity is confirmed.
    opal-data-bd colocation: SmartX JWT + data land in opal-data-bd (Andrew 2026-05-15 -- SmartX feeds 49F/BD-domain work; SmartX is shared Opal resources).
  </cross_domain_coordination>

  <deliverables>
    <item>smartx-jwt-refresher Lambda + EventBridge + IAM + the smartx/jwt/current secret -- Terraform-deployed, 0-diff, tagged, pushed.</item>
    <item>The daily pull landing model value + holdings weights to opal-data-bd raw+bronze; the JWT reader lib.</item>
    <item>Session log + RAVC2 to COO + CC CTO + DS~B.</item>
  </deliverables>

  <ravc>0.5.0_AE_OpalETL RAVC2 to COO + CC CTO + DS~B on AC1-5.</ravc>

  <notes>
    Andrew directed the receiver: 0.5.0_AE_OpalETL ("the Opal agent ... shared resources"), not a partner-specific ETL agent. The brief (352ab4585) + the TO-1 matrix (bd5d7d068) are the authoritative inputs -- brief section-5 is the architecture, do not re-derive. Andrew framed TO-2 as "the whole flow" in one TO; the DS-code / AE-infra split is internal to it -- coordinate with DS~B. Silver/gold modeling is explicitly TO-3, not this TO -- land raw+bronze and stop. The smartx/credentials/* secrets are a real Manager-role SmartX login -- Secrets-Manager-only, never in code (brief section-11). The data/smartx/ code-home lane is with CTO -- the AE infra work does not wait on it; the DS-code commits do.
  </notes>
</task_order>
