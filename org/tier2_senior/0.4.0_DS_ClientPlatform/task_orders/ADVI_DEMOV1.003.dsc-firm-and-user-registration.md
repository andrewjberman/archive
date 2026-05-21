<task_order>
  <metadata>
    <id>2.0.0_SA_COO~C-2026-05-21-demov1-to3-registration</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-21</date>
    <status>staged</status>
    <project_code>ADVI_DEMOV1</project_code>
  </metadata>

  <objective>
    Phase 3 of ADVI_DEMOV1 — register the demo tenant's identity: create the
    `FIRM#demo` record in the `opal-users-v2` DynamoDB table pointed at
    `opal-data-demo`, create a demo Cognito user scoped to the demo firm, and add
    the `demo` entry to the portal's `ROUTER_FIRM_SUFFIX` short<->long firm map.
    End state: a demo login exists and resolves end-to-end to the demo bucket on
    both serving paths.
  </objective>

  <context>
    ADVI_DEMOV1 PRD: docs/architecture/ADVI_DEMOV1.md (v0.1, 2e1321f79). Read §3,
    §4, §6 TO-3. Auth design of record: docs/architecture/ADVI_49PUSH_AUTH_ARCHITECTURE.md.
    Firm-record template: infra/aws/auth/migration/003_create_firms.py.

    The dynamic serving Lambda `opal-partners-data` is firm-agnostic — it resolves
    a firm's bucket from DynamoDB `opal-users-v2` `PK=FIRM#{firmId}`, `SK=META`,
    attribute `s3Bucket`. Creating `FIRM#demo` with `s3Bucket=opal-data-demo`
    serves every DYNAMIC route with no Lambda code change.

    DUAL SERVING PATH (TO-0 §3.2 verdict): the static-platinum path resolves via
    the edge `FIRM_CONFIG` map (TO-1's scope); the dynamic path resolves via this
    DynamoDB `FIRM#demo` record (this TO). The demo needs BOTH — TO-1 wires the
    edge map, TO-3 wires DynamoDB. Cross-check the `firmId` token: it must be
    identical (`demo`) across the Cognito user claim, the DynamoDB FIRM# key, the
    edge FIRM_CONFIG entry, and the portal ROUTER_FIRM_SUFFIX entry — a mismatch
    breaks one serving path silently.

    GATING — this TO is staged. It sequences AFTER TO-1 (infra: bucket + routing
    live) and TO-2 (transform engine built). The registration records can be
    written before the bucket is populated, but a demo login is only meaningfully
    verifiable once TO-4 has populated data — so the end-to-end login check in
    this TO confirms ROUTING resolves (correct bucket, no 403/401), not data
    richness. COO~C issues the GO when TO-1 + TO-2 are RAVC-closed.

    Precedent: `mockadv` is an existing non-real test firm — its FIRM# record,
    Cognito user, and routing follow the same shape; use it + the FIRMSEP.10
    Cottonwood onboarding as the working templates. The PRD ADVI_FIRMSEP
    onboarding playbook is the documented path.

    Auth-domain coordination: this TO writes to opal-users-v2 (auth-owned) and
    creates a Cognito user. If a dedicated auth owner / DE/RD is required for the
    Cognito or DynamoDB write, coordinate via COO~C — flag it rather than
    proceeding outside your grant.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-routes auth-map</run>
      <expect>The JWT-claim path for a partner firm — confirms the claim shape
      (`firmId`, `allowedFirmIds`, `role`, ...) the demo Cognito user must carry,
      mirroring mockadv.</expect>
      <if_mismatch>If the auth-map does not resolve the demo claim path, inspect
      ADVI_49PUSH_AUTH_ARCHITECTURE.md + the mockadv user directly.</if_mismatch>

      <run>comp-transform schema-check {portal component touched by ROUTER_FIRM_SUFFIX}</run>
      <expect>0 MISSING fields — the ROUTER_FIRM_SUFFIX entry is an additive map
      key; no rendered field changes.</expect>
      <if_mismatch>If schema-check flags drift, the portal change is broader than
      a map entry — stop and flag to COO~C.</if_mismatch>

    Phase 2 — before commit:
      <run>bun run build (or bunx tsc -b) on the portal change</run>
      <expect>Zero TypeScript errors — the ROUTER_FIRM_SUFFIX entry is type-clean.</expect>
      <if_mismatch>Fix all TS errors before commit.</if_mismatch>

    Phase 3 — after committing + records created:
      <run>comp-routes trace getPlatinumFirmDashboard (demo firm)</run>
      <expect>An end-to-end demo request resolves: static path -> opal-data-demo
      via the edge FIRM_CONFIG; dynamic path -> opal-data-demo via the DynamoDB
      FIRM#demo s3Bucket attribute. No 403 (OAI) / 401 (router-block) errors on
      the routing.</expect>
      <if_mismatch>A routing failure means the firmId token mismatches across one
      of the four wiring points, or TO-1 infra is incomplete — diagnose and flag
      to COO~C.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: portal/src/api/endpoints/advisor-intelligence.ts — the
      ROUTER_FIRM_SUFFIX map. This file is high-traffic across ADVI TOs.
    - required_action: before committing, re-confirm via get_live_agents / broker
      that no other agent is editing advisor-intelligence.ts; pull latest
      (origin/CLOUD after a fresh fetch — local HEAD goes stale fast). The `demo`
      entry is additive only — do not alter existing firm-suffix entries.
    - shared_resource: opal-users-v2 DynamoDB (auth domain). The FIRM#demo write
      is additive — a new partition key, no mutation of existing firm records.
    - The portal submodule commits to its own DEV branch, not CLOUD — follow the
      portal submodule git convention.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `FIRM#demo` record exists in `opal-users-v2` (`PK=FIRM#demo`, `SK=META`)
       with `s3Bucket=opal-data-demo`, plus `name`, `tier`, `domain`, `status`
       set per the 003_create_firms.py template / the mockadv precedent.
    2. A demo Cognito user exists with JWT claims `firmId=demo`,
       `allowedFirmIds=demo` (or `[demo]`), and the role/tier claims a partner
       user carries — mirroring mockadv.
    3. The portal `ROUTER_FIRM_SUFFIX` map in advisor-intelligence.ts has a
       `demo -> demo` entry; `bucketSuffix()` resolves `demo` correctly. Additive
       only — existing entries unchanged.
    4. The `firmId` token `demo` is verified IDENTICAL across all four wiring
       points: Cognito claim, DynamoDB FIRM# key, edge FIRM_CONFIG entry (TO-1),
       portal ROUTER_FIRM_SUFFIX entry. Documented in the session log.
    5. `bun run build` / `bunx tsc -b` on the portal change: zero TypeScript
       errors.
    6. Phase-3 `comp-routes trace` confirms a demo request resolves end-to-end on
       BOTH serving paths to opal-data-demo with no 403/401 routing error.
    7. A demo login authenticates and the Advisor Intelligence portal loads for
       the demo firm (data may be empty/sparse until TO-4 populates — routing +
       auth resolution is what this criterion verifies).
    8. Session log with Compiler Tools section committed.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">the FIRM#demo DynamoDB record (via a migration script in the 003_create_firms.py family, or the documented onboarding mechanism)</file>
      <file action="create">the demo Cognito user (via the documented user-creation mechanism)</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts — ROUTER_FIRM_SUFFIX `demo` entry</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-21/advi_demov1_to3_registration~C.md</file>
      <file action="reference">infra/aws/auth/migration/003_create_firms.py; docs/architecture/ADVI_49PUSH_AUTH_ARCHITECTURE.md</file>
      <file action="reference">the mockadv firm record + the FIRMSEP.10 Cottonwood onboarding (templates)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Create FIRM#demo per the 003_create_firms.py template /
    mockadv precedent — s3Bucket=opal-data-demo is the binding attribute.</requirement>
    <requirement id="2">Create the demo Cognito user scoped to firmId=demo,
    allowedFirmIds=demo — it must NOT carry allowedFirmIds for any real firm.</requirement>
    <requirement id="3">Add the additive ROUTER_FIRM_SUFFIX `demo` entry; do not
    disturb existing firm-suffix mappings.</requirement>
    <requirement id="4">Verify the `demo` firmId token is identical across all
    four wiring points (criterion 4) — the #1 silent-failure mode.</requirement>
    <requirement id="5">If a Cognito or DynamoDB write requires a dedicated auth
    owner / DE/RD outside your grant, coordinate via COO~C — do not proceed
    outside lane.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Portal ROUTER_FIRM_SUFFIX change committed to the portal submodule DEV branch</deliverable>
    <deliverable type="commit | document">FIRM#demo record + demo Cognito user created; the creation mechanism (script/commit) recorded</deliverable>
    <deliverable type="document">Session log with Compiler Tools section + the four-point firmId-token consistency check</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT give the demo Cognito user `allowedFirmIds` containing any real
    firm (49financial / inflection / opal-capital) — the demo user must see ONLY
    the demo firm.</rule>
    <rule>Do NOT mutate existing FIRM# records, ROUTER_FIRM_SUFFIX entries, or the
    edge FIRM_CONFIG — every change in this TO is additive.</rule>
    <rule>Do NOT skip the four-point firmId-token consistency check — a mismatch
    breaks one serving path silently.</rule>
    <rule>Do NOT begin before COO~C issues the GO (gated on TO-1 + TO-2 close).
    This TO is staged.</rule>
  </do_not>
</task_order>
