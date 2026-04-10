<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-ownership-map</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <co_owner>0.7.0_AE_CloudOps</co_owner>
    <date>2026-04-10</date>
    <status>complete</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Publish an advisor→{accounts, relationships} ownership map as a small JSON artifact at an edge-accessible location (S3 key under the existing platinum layout, served via CloudFront). The map is the source of truth for .004c's per-path enforcement of account/client endpoints. Refreshed on every D_00/D_04 run so edge state tracks the platinum layer. This is Wave 2b and can run in parallel with .004a; both are prerequisites for .004c.
  </objective>

  <context>
    CTO's comp-routes audit identified two advisor endpoints that cannot be scoped by a simple `jwt.advisorId == path[id]` rule because the path parameter is NOT an advisor id:

    - `getPlatinumAccountSummary` — path `{accountId}`, S3-direct origin, edge-only enforcement
    - `getPlatinumClientSummary` — path `{relationshipId}`, API GW origin

    Enforcement of these requires the edge Lambda to look up "does this advisor own this account/relationship?" at request time. That means an ownership map must exist on the edge path.

    Options considered (CTO PRD §5.5):
    - (a) DynamoDB lookup at edge — too slow at Lambda@Edge scale (50ms+ per request).
    - (b) S3 JSON blob read at edge — acceptable if the map is small (<1 MB) and CloudFront-cached.
    - (c) Lambda@Edge KV store — not supported on our current stack.

    **Recommended: Option (b).** Publish `platinum/shared/advisor_ownership.json` (or similar path under the existing platinum layout) with the shape:

    ```json
    {
      "generated_at": "2026-04-10T22:05:00Z",
      "advisors": {
        "A001": {
          "accounts": ["ACC_0001", "ACC_0002", ...],
          "relationships": ["REL_0001", ...]
        },
        "A002": { ... }
      }
    }
    ```

    At edge enforcement time (.004c), `shared-advisor-router` reads the blob (CloudFront-cached, so ~1 read per minute globally), looks up `advisors[jwt.advisorId]`, and checks if the path's `{accountId}` or `{relationshipId}` is in the appropriate set.

    Scale estimate: ~200 advisors × ~50 accounts + ~20 relationships per advisor = ~14k ids total. At ~20 bytes per id (JSON overhead), ~300 KB uncompressed, ~100 KB gzip. Comfortably within CloudFront edge-cache size limits.

    Refresh cadence: DS adds a step at the end of D_00 (or D_04) that writes the ownership map after the underlying platinum dimension tables are updated. No separate trigger, no new cron. If D_00 runs daily, the map refreshes daily; if D_00 runs on incremental mode multiple times per day, the map refreshes each time.

    Contract with .004c: the JSON shape is FROZEN after .004b ships. Any future schema change requires a coordinated .004c + frontend review.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - `comp-pipescript io D_00` and `comp-pipescript io D_04` — identify which gold script is the right home for the ownership map writer. D_00 (accounts/advisors dimension) is the primary candidate since it already loads advisor_assignments and accounts_dimension; D_04 (platinum publisher) is secondary.
    - `comp-blast` on the selected gold script — confirm adding a new writer does not disrupt existing consumers.
    - `comp-blast advisor_assignments_history` — understand the shape of the source data. Confirm the join keys (advisor_id, relationship_id, account_id) are available.
    - Read `data/black_diamond/scripts/gold/D_00*.py` to locate the right insertion point for the ownership map builder. Prefer a late step after all dimension loads are complete so you have advisor_assignments, accounts_dimension, and relationships in memory.
    - `comp-routes` on a platinum JSON path — understand the existing CloudFront behavior for `platinum/**`. Confirm `platinum/shared/advisor_ownership.json` will be served through the same behavior as other platinum artifacts (or pick a different key if the behavior routing is ambiguous).

    Phase 2 (during implementation):
    - Add an `_build_advisor_ownership_map()` helper in the selected gold script. Joins advisor_assignments_history (current version) against accounts_dimension (for account ids) and relationships (for relationship ids). Returns the nested dict.
    - Filter to ACTIVE advisors only — do not include retired or inactive advisors. `active` definition: whatever D_00 already uses for the leaderboard population.
    - Exclude admin users who are ALSO advisors from special treatment — the map is purely about advisor→account mapping. Admin bypass is handled in the router, not here.
    - Write to S3 at `platinum/shared/advisor_ownership.json` (or whatever path .004c AE confirms is CloudFront-reachable — agree before shipping).
    - Include `generated_at` ISO timestamp for debuggability.
    - Include a `schema_version: 1` field so .004c can reject stale maps after a schema bump.
    - Log the write: rows written, advisor count, account count, relationship count, S3 etag.

    Phase 3 (after committing, before gold run):
    - `py_compile` on all modified Python files.
    - Dry-run: invoke `_build_advisor_ownership_map()` locally against a dev snapshot if available, verify the shape is correct and the three counts (advisors/accounts/relationships) match expectations.
    - Upload to `s3://opal-data-bd/code/gold/` with etag parity scan.
    - Broker message to 0.6.0_AE_PartnerETL: the map will start populating on the next gold run.
    - Broker message to 0.7.0_AE_CloudOps: the ownership map S3 key is `platinum/shared/advisor_ownership.json` (or agreed key), the shape is frozen at schema_version 1, .004c can proceed once the first map lands after the next gold run.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `data/black_diamond/scripts/gold/D_00*.py` (or D_04) — DS owns. New step appended to the dimension-build phase.
    shared_resource: `platinum/shared/advisor_ownership.json` (new S3 artifact) — DS writes, AE reads at edge.
    shared_resource: `shared-advisor-router` Lambda@Edge — AE reads the artifact in .004c. No dependency on .004b code, only on the artifact existing.
    shared_resource: CloudFront behavior for `platinum/**` — existing, no Terraform change expected. Verify the new key is reachable via the existing behavior; if a new behavior is required, escalate.
    last_write_owner: 0.4.0_DS_ClientPlatform for the gold script; 0.6.0_AE_PartnerETL for gold-runner orchestration.
    required_action: "DS and AE 0.7.0 must agree on the S3 key BEFORE DS writes the gold script. Exchange via broker message. Default recommendation: `platinum/shared/advisor_ownership.json`. If AE identifies a CloudFront behavior problem with `/shared/*`, pick an alternative and update both sides before shipping."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **S3 key agreed:** DS + AE exchange broker message agreeing on the exact S3 key. Default: `platinum/shared/advisor_ownership.json`. Logged in both session logs.
    2. **Gold script modified:** `_build_advisor_ownership_map()` added to D_00 (or D_04 per comp-pipescript analysis). Runs after advisor_assignments + accounts_dimension + relationships are loaded.
    3. **Schema frozen:**
       ```json
       {
         "schema_version": 1,
         "generated_at": "ISO8601",
         "advisors": {
           "{advisor_id}": {
             "accounts": ["{account_id}", ...],
             "relationships": ["{relationship_id}", ...]
           }
         }
       }
       ```
       Documented in the session log. Any future schema change requires a coordinated .004c update.
    4. **Active advisors only:** Retired/inactive advisors excluded using whatever definition D_00 currently uses for the leaderboard population. Documented.
    5. **Size sanity:** Total size <1 MB uncompressed. Log the actual size and counts (advisors/accounts/relationships).
    6. **py_compile + diff-before-ship:** Modified gold script compiles clean. Local dry run produces a sane map (non-zero advisors, non-zero accounts, non-zero relationships).
    7. **Commit + push + S3 upload:** DS-authored commit, push to CLOUD, upload to `s3://opal-data-bd/code/gold/`. Etag parity verified.
    8. **Runner pickup:** Broker message to AE 0.6.0 announces staging. Do NOT trigger the runner directly — let the next scheduled run pick it up.
    9. **AE handoff message:** Broker message to AE 0.7.0 announcing: map S3 key, shape frozen at schema_version 1, first population date (after next gold run), acceptance check to verify the artifact is CloudFront-reachable.
    10. **First map population verified:** After the next gold run lands, verify the artifact at the agreed S3 key: `aws s3 ls s3://opal-data-bd/platinum/shared/advisor_ownership.json`, cat the JSON, spot-check 3 known advisors' account lists. Log in the session.
    11. **Compiler Tools section:** comp-pipescript, comp-blast, comp-routes outputs logged in the session.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_00*.py (or D_04 per comp-pipescript analysis)</file>
      <file action="reference">data/black_diamond/scripts/gold/lib/** (shared helpers for parquet reads)</file>
      <file action="create">platinum/shared/advisor_ownership.json (S3 artifact, NOT a repo file)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Agree on the S3 key with AE 0.7.0 BEFORE writing code. Broker message exchange required.</requirement>
    <requirement id="2">Schema is frozen at schema_version 1 once this TO ships. Future changes require coordinated .004c + frontend review.</requirement>
    <requirement id="3">Filter to active advisors only. Use D_00's existing active-advisor definition.</requirement>
    <requirement id="4">Keep the map small. Target <1 MB uncompressed. If it grows beyond that, escalate — CloudFront edge-cache has size limits.</requirement>
    <requirement id="5">Do NOT trigger the gold runner. Ship the code, let the next scheduled run pick it up.</requirement>
    <requirement id="6">Do NOT write the ownership map to any silver/gold S3 key that is also a consumer target — `platinum/shared/` is a new namespace for this purpose.</requirement>
    <requirement id="7">py_compile + diff-before-ship are mandatory gates per existing DS protocol.</requirement>
    <requirement id="8">Include `schema_version` in the artifact. This is the contract surface with .004c.</requirement>
    <requirement id="9">Do NOT include PII in the ownership map. advisor_id, account_id, relationship_id are ok; names, emails, balances are NOT in scope.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Gold script modified. Committed with `--author=0.4.0_DS_ClientPlatform`.</deliverable>
    <deliverable type="s3_upload">Modified script uploaded to `s3://opal-data-bd/code/gold/`. Etag parity verified.</deliverable>
    <deliverable type="s3_artifact">After next gold run: `platinum/shared/advisor_ownership.json` populated.</deliverable>
    <deliverable type="message">Broker messages to 0.6.0_AE_PartnerETL (runner pickup) and 0.7.0_AE_CloudOps (edge consumption handoff with schema contract).</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-{NN}/advi_profil_004b_ownership_map.md` with S3 key decision, script change, dry-run output, commit SHA, S3 etag, and Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT ship without AE 0.7.0 agreement on the S3 key.</rule>
    <rule>Do NOT trigger the gold runner. Let the next scheduled run pick it up.</rule>
    <rule>Do NOT include PII fields. IDs only.</rule>
    <rule>Do NOT ship a map larger than 1 MB without flagging the size issue first.</rule>
    <rule>Do NOT change the schema after shipping without coordinating with .004c.</rule>
    <rule>Do NOT skip py_compile or diff-before-ship.</rule>
  </do_not>
</task_order>
