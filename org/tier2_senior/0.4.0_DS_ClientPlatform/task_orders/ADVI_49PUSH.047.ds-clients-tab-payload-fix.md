<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-047-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <phase>Books Tab Performance</phase>
    <priority>HIGH</priority>
  </metadata>

  <objective>
    Eliminate the 7-second clients-tab Lambda call. Pre-build a slim clients-tab
    artifact in D_04 that the Lambda serves directly from S3, replacing on-demand
    computation with a fast S3 passthrough.
  </objective>

  <context>
    Prior investigation (ADVI_REBORN.W5-003, 2026-04-08) identified getClientsTab()
    as the Books tab bottleneck and proposed payload reduction. Never implemented.

    Network trace evidence (Andrew, 2026-04-09):
      clients-tab?firmId=49financial   200   81.8 kB   7.71 s   (first call)
      clients-tab?firmId=49financial   200   81.9 kB   6.97 s   (second call -- warm Lambda)

    Key observations:
    1. Both calls take ~7s. This is NOT cold start -- the warm Lambda invocation
       is equally slow. The Lambda is doing heavy compute per request.
    2. 81.8 kB for a firm client list. W5-003 confirmed: Lambda returns every client
       with headline, tax, income_fees, portfolio, engagement sections all at once.
    3. Compare: leaderboard.json (284ms) and fee_efficiency.json (283ms) are pre-built
       S3 files. clients-tab goes through Lambda compute. That gap (7s vs 284ms) is
       the architecture mismatch.
    4. The component also double-fetches (clients-tab fires twice per page load due to
       remounting -- a separate DE fix). Every second of Lambda processing time is
       paid twice until that is resolved.
  </context>

  <step_1_diagnose label="Read the Lambda to confirm root cause">
    Before building anything, confirm what the clients-tab endpoint actually does.
    Read: infra/aws/lambda/opal-partners-data/lambda_function.py
    Find the handler for the clients-tab route. Answer:

    A. Is it serving a single pre-built S3 file (fast path)?
       OR doing per-client DynamoDB reads / per-advisor S3 reads (slow path)?

    B. Does it pseudonymize at serve time (inline) or is the S3 data already pseudonymized?

    C. How many S3 get_object or DynamoDB get_item calls does it make per request?

    Run comp-pipescript to check D_04 output keys:
      comp-pipescript io D_04

    Check whether D_04 already writes any S3 key that looks like clients-tab.
    If it does, the Lambda may not be using it -- that is a routing fix, not a D_04 fix.
    If it does not, D_04 needs to be extended.

    Document your findings before writing any code.
  </step_1_diagnose>

  <step_2_build label="Pre-build slim clients-tab artifact in D_04">
    Based on step 1 findings, extend D_04 to write a pre-built, pre-pseudonymized
    slim clients-tab JSON artifact to S3 at gold run time.

    Artifact key: platinum/firm/{firm_id}/clients-tab-slim.json
    (or platinum/firm/{firm_id}/clients-tab.json if that key does not already exist)

    Slim payload -- include ONLY what the Books tab N1 view renders:
      - relationship_id          (internal join key, not rendered)
      - display_name             (pseudonymized at write time -- HMAC via pseudonymizer)
      - account_count            (integer, not PII)
      - aua_current              (dollar amount)
      - nna_ytd                  (dollar amount)
      - advisor_id               (for grouping by advisor)
      - advisor_display_name     (pseudonymized -- which advisor owns this relationship)

    Do NOT include in this artifact:
      - tax_exposure, income_fees, portfolio_composition, engagement_metrics
      Those belong in platinum/clients/{id}/summary.json (L3 drill, fetched on demand).

    Pre-pseudonymize at write time:
      Apply the existing pseudonymizer to display_name and advisor_display_name
      before writing to S3. The Lambda must NOT need to pseudonymize at serve time.
      The file on S3 is already safe to serve.

    Size target: under 15 kB for a typical firm (vs current 81.8 kB).
    If 49Financial has an unusually large client count, document the actual count
    and flag if pagination is needed even for the slim version.
  </step_2_build>

  <step_3_route label="Wire Lambda to serve the pre-built file">
    The Lambda clients-tab handler should become a pure S3 passthrough:
      1. Resolve firm bucket (get_firm_bucket -- note: this already has a DynamoDB
         round trip that should be cached per ADVI_49PUSH analysis, but that is a
         separate Lambda fix for AE/DT)
      2. S3 get_object: platinum/firm/{firm_id}/clients-tab-slim.json
      3. Return response directly -- no pseudonymization, no aggregation, no per-client reads

    If the Lambda change requires a deploy, note it clearly in your session log as a
    DT/AE handoff. Do not deploy Lambda yourself.

    If the current Lambda route already points at an S3 file (from step 1 finding A),
    you may only need to update the S3 key it reads and confirm D_04 writes there.
  </step_3_route>

  <pii_note>
    Pre-pseudonymizing at D_04 write time (not Lambda serve time) is the correct
    pattern. It means:
    - The S3 file is safe at rest (no cleartext names)
    - The Lambda is a dumb passthrough (no PII processing per request)
    - Pseudonymization errors are caught at gold run time, not at serve time

    The L3 per-client detail (platinum/clients/{id}/summary.json) remains Lambda-routed
    with per-request pseudonymization because it is fetched on demand for one client at a
    time and the volume is small. Do not change that path.

    The clients-tab-slim artifact must NOT contain cleartext relationship_name or
    client_name fields under any key. Only display_name (already HMAC-hashed).
  </pii_note>

  <acceptance_criteria>
    1. comp-pipescript io D_04 shows a clients-tab or clients-tab-slim write edge
    2. platinum/firm/{firm_id}/clients-tab-slim.json exists on S3 after a gold run
    3. Payload size is under 15 kB for 49Financial (target: 5-10x reduction from 81.8 kB)
    4. Lambda clients-tab route returns in under 500ms on a warm invocation (vs 7s)
    5. No cleartext client names in the artifact (verified by grep on the S3 file)
    6. L3 per-client drill (platinum/clients/{id}/summary.json) behavior unchanged
    7. Session log documents: root cause finding from step 1, S3 key written,
       payload size before/after, Lambda timing before/after (use curl or network tab)
  </acceptance_criteria>

  <compiler_tools_mandate>
    REQUIRED before writing any code:
      comp-pipescript io D_04       -- confirm which S3 keys D_04 currently writes
      comp-routes trace clients-tab -- confirm Lambda route for this endpoint
      comp-blast D_04               -- blast radius of any D_04 changes

    REQUIRED before marking complete:
      comp-pii scan ClientsTab      -- confirm no cleartext PII fields in rendered output
                                       after DE wires the new slim artifact
  </compiler_tools_mandate>

  <handoff_note>
    If Lambda code changes are required (step 3), leave lambda_function.py uncommitted
    and write a handoff table in your session log for AE/DT:

      | File | Change | Deploy required |
      |------|--------|----------------|
      | infra/aws/lambda/opal-partners-data/lambda_function.py | clients-tab route now serves pre-built S3 slim file | partners-api deploy |

    If only D_04 changes (step 2 only, Lambda already reads from the right S3 key),
    a gold re-run is sufficient -- no Lambda deploy needed. Confirm with AE that
    the runner is available before triggering.
  </handoff_note>

</task_order>
