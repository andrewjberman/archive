<task_order>
  <metadata>
    <id>SXPL_RESTIN.001</id>
    <slug>dsb-per-model-availability-assessment</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-15</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>SXPL_RESTIN</project_code>
    <priority>P1 -- the designated INITIAL TO (Andrew, brief section-9). Produces the ground-truth schemas + per-model availability matrix that TO-3+ (silver/gold modeling) is scoped against. Read-only investigation.</priority>
    <sla>~4-6h wall. Read-only API probing; no code ships beyond an optional probe harness + the deliverable matrix brief.</sla>
  </metadata>

  <references>
    <brief>docs/briefs/smartx-rest-integration-design-20260515.md (commit 352ab4585) -- the authoritative design brief. section-3 auth mechanics, section-6 endpoint manifest, section-7 modelId-vs-reportedModelId chaining, section-8 the first-data-goal mapping, section-10 open questions.</brief>
    <directive>Andrew direct 2026-05-15 -- the SmartX REST integration workstream; brief section-9 carries the directed TO structure (this is TO-1, the designated initial TO).</directive>
    <auth>ROPC password grant against identity.smartxadvisory.com/connect/token with client_id smartx-managerportal-webclient + the smartx/credentials/{username,password} Secrets Manager secrets -> 2h Bearer JWT (brief section-3). Read-only probing only.</auth>
  </references>

  <context>
    The SmartX HAR enumerated 7 modelIds but captured no response bodies for most endpoints. The brief section-6 manifest marks each endpoint HAR-observed vs PROBE-confirmed. TO-2 (the pull flow) and TO-3+ (silver/gold modeling) need the real per-model response schemas + a definitive availability matrix -- which endpoints carry daily-grain data vs current-snapshot, and which are populated for which of the 7 models. This TO produces that ground truth. Read-only: no production pull, no scheduled job -- ad-hoc authenticated probing.
  </context>

  <objective>
    A per-model x per-endpoint data-availability matrix for all 7 SmartX modelIds, with captured real response schemas, delivered as a brief for TO-2/TO-3 to build against.
  </objective>

  <scope>
    <item>Resolve all 7 modelIds: for each, GET /models/{modelId} -> capture id, name, shortName, status, reportedModelId, type, enterprise. Identify the 5 known Opal portfolios (UST/ST/INT/LTC/LTA per production.env) and characterize the 2 unidentified modelIds (brief section-7 / section-10 open question).</item>
    <item>For each of the 7 models, call every endpoint in brief section-6.2 (core api/3.1), section-6.3 (performance service), section-6.4 (legacy api/3.0) -- using the correct id space per brief section-7 (modelId vs reportedModelId; /reportedmodels/* needs the reportedModelId chained from /models/{modelId} -- calling it with a modelId returns HTTP 400). Capture the real response schema (the HAR has no bodies for HAR-status endpoints).</item>
    <item>For each endpoint, classify: daily-grain time series vs current snapshot vs static metadata; populated vs empty per model. Produce the per-model x per-endpoint availability matrix.</item>
    <item>Answer the brief section-10 open questions this probe can settle: does a historical-holdings endpoint exist (or is daily-weight history accrued only by daily snapshotting); the identity of the 2 unidentified modelIds; the rate-limit ceiling (the exporter asserts 20 req/min "per SmartX agreement" -- confirm + have the probe respect it).</item>
    <item>Read-only. A probe harness may be committed (a probe dir or data/smartx/) but NO scheduled job, NO production pull, NO Lambda. Credentials ONLY from Secrets Manager, never in code/env (brief section-11).</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">All 7 modelIds resolved -> name / shortName / reportedModelId / status; the 5 Opal portfolios identified, the 2 unidentified modelIds characterized.</ac>
    <ac id="AC2">Real response schemas captured for every section-6.2-6.4 endpoint reachable per model (the HAR body-n/a gap closed empirically).</ac>
    <ac id="AC3">Per-model x per-endpoint availability matrix delivered: daily-grain vs snapshot vs static, populated vs empty.</ac>
    <ac id="AC4">The probe-answerable brief section-10 open questions answered (historical-holdings existence; the 2 unknown models; the rate limit).</ac>
    <ac id="AC5">Deliverable is a brief (docs/briefs/) -- the matrix + schemas + answers. No scheduled job / production pull / Lambda shipped. No emoji. Credentials only from Secrets Manager.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Read-only investigation TO -- no gold/silver script edit, no deploy. If a probe harness is committed: ds-commit-gate.sh on any .py (py_compile + ds-precommit-check + ruff py39). No comp-pipescript (no pipeline script in scope). The deliverable is a brief, not code.</compiler_tools_mandate>

  <cross_domain_coordination>
    GATES TO-3+ (silver/gold modeling -- scope TBD after this TO per brief section-9 / Andrew). Runs PARALLEL to TO-2 (the AE pull flow) -- TO-2's first-data-goal endpoints (/enterprises/aum, /reportedmodels/{id}/holdings) are already PROBE-confirmed in the brief, so TO-2 does not block on this TO; this TO's full matrix refines TO-3. Additive to DS~B's ADVI_TXNAMG.002 (Phase C held) -- no file conflict (different pipeline: data/smartx/ vs data/orion/).
  </cross_domain_coordination>

  <deliverables>
    <item>The per-model availability matrix brief (docs/briefs/) -- schemas + matrix + open-question answers.</item>
    <item>Probe harness committed if useful (read-only; no scheduled job).</item>
    <item>Session log + RAVC2 to COO + CC CTO.</item>
  </deliverables>

  <ravc>DS~B RAVC2 to COO + CC CTO on AC1-5. The RAVC2 + matrix brief is the input COO uses to scope TO-3+.</ravc>

  <notes>
    Designated initial TO (Andrew). Read-only -- the value is the ground-truth matrix; resist scope-creeping into building the pull (that is TO-2) or the modeling (TO-3). Respect the rate limit once confirmed. The brief (352ab4585) is thorough -- section-6/7/8 give the endpoint map; this TO closes the empirical gaps the HAR left.
  </notes>
</task_order>
