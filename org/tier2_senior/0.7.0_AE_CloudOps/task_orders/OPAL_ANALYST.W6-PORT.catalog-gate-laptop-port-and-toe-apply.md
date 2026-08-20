<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-20-w6-laptop-port-toe-apply</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-20</date>
    <status>pending</status>
    <project_code>OPAL_ANALYST</project_code>
  </metadata>

  <objective>
    OPAL_ANALYST.W6 close-gate (b): the 0-diff laptop-lane port of the certified W6 package
    (catalog_gate.py + the staged W5 catalog), then the TO-E mechanical apply (the v0
    partner-query plumbing endpoint on opal-gateway). Program close is declared at CTO~Z on
    (a) the CVO~Z co-sign (site Z, in flight) + (b) this TO.
    CADENCE RE-FRAMED 2026-08-20 ~1429Z (supersedes the dispatch-time "not urgent"):
    Andrew's fresh word at the site-Z CTO terminal (~142xZ, relayed @e2c8e55dab) put the
    site-Z D-family (D6/D7/D8/D9) under a sovereign-backed COO~Z /drive loop "to
    completion" -- and D6's laptop dependency IS this TO. Treat it as your NEXT item
    after in-flight work; do not park it behind discretionary queue items.
  </objective>

  <context>
    W6 is CERTIFIED-ON-STAGED at CTO~Z @bf0a2c30f9, on CLOUD at parity. Cert:
    org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_OPAL_ANALYST_W6_CERTIFICATION_20260820.md
    (PROOF_OF_SPEC validator rc=0; 13/13 author-time battery).

    Governing spec (READ FIRST -- the apply checklist at the bottom is the procedure):
    infra/aws/ec2/opal-gateway/app/graphql_plumbing/DESIGN.md (author package,
    site-Z 0.5.0_AE_OpalETL~Z). Package files, already in-tree at parity:
    infra/aws/ec2/opal-gateway/app/graphql_plumbing/catalog_gate.py +
    exercise_catalog_gate.py. Staged catalog:
    workflows/atom_decomposition/catalog_v02/DATA_CATALOG.v0.2.staged.yaml.

    LOAD-BEARING PINS (routed by 0.0.0_AB_MSTR 20260820T125049Z; each cites its source --
    do not widen any of them):
    1. THE PORT PRECEDES THE APPLY. The gate reads the live refs/DATA_CATALOG.yaml (v0.2)
       path at runtime, passed by the endpoint at startup; the staged path is author-time
       only (DESIGN.md checklist 3).
    2. EC2 deploy via safe-ec2-deploy.sh per EC2_MANIFEST -- code, not TF (D6-5: sitez
       does not apply; every apply of this package is a laptop-lane act).
    3. identity_scope key mint: ZERO-MINT IS NOW RULED, not merely default. Andrew-direct
       at the CTO terminal 2026-08-20 ~1425Z, VERBATIM: "zero-mint W6" (record:
       org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260820_OPENCALLS_THREE_WORDS.md).
       DESIGN.md checklist item 4 executes as explicit zero-mint; partner naming is a
       FUTURE Andrew act at first-real-consumer, outside this TO's life. This TO mints
       ZERO keys. (CTO messaged you this directly 1425Z; this pin cites the same ruling.)
    4. v0 is PLUMBING-ONLY (@1e0ec3b079, Andrew-ruled 2026-08-19 ~20:12Z): no GraphQL
       parsing, no schema exposure, no parquet resolver (D6-3), resolver floor enforced
       (@7ea13aa4ed -- structurally absent from the catalog + belt-checked in
       catalog_gate.FLOOR_PATTERNS).
    5. CTO REVIEW SLOT -- EXERCISED AND AMENDED 2026-08-20 ~1456Z (CTO 63158, by the
       issuing authority): the applied numbers are rows &lt;= 1000/response, 10s/request,
       **4 MB/response** (raised from the proposed 2 MB after the R1 apply-time size
       census found two CERTIFIED catalog rows over-cap -- "a limit that permanently
       vetoes a certified catalog row is a content policy wearing an ops bound's
       clothes"), 30 req/min/key sliding-window-log. R1 (head-object size census) is
       now STANDING at EVERY catalog version port; any legitimate over-cap key routes
       to CTO before the cap moves. Over-cap named-refusal behavior unchanged above 4MB.
    6. O-1 rider at port (cert, from mutant P7): ONE battery case asserting every {scope}
       family row carries firm: per-scope. OWNER IS 0.5.0_AE_OpalETL~Z (their authorship)
       -- coordinate via MCP; do NOT author the case yourself. A test assertion; no gate,
       no monitor (the alert moratorium binds).
    7. O-2 rider (cert): T-3 = the MCP service restart that activates max_data_points in
       the live tool signature -- verified by a CAPPED CALL at the laptop's next gateway
       touch, NEVER a config read. THIS APPLY IS THAT TOUCH: discharge O-2 here.

    Caller-signature note from the cert seat (DESIGN.md checklist 0): the TO-G consumer
    entity_resolution/disposition_contract.load_contract(repo_root) takes the REPO ROOT --
    passing a full contract path doubles it.
  </context>

  <compiler_tools_mandate>
    Phase 1 -- before writing:
      <run>./infra/aws/ec2/verify-ec2.sh</run>
      <expect>EC2 parity clean (Rule 11: verify parity before EC2 work)</expect>
      <if_mismatch>Resolve parity before any deploy step; a deploy onto a drifted box is the half-landed class.</if_mismatch>

      <run>comp-blast catalog_gate</run>
      <expect>Thin/absent radius -- the package is new (issuer's dispatch-time run launched 1337Z; re-run at your seat). No unexpected existing consumers.</expect>
      <if_mismatch>Unexpected consumers = a shared surface this TO did not plan for -- flag to COO before writing.</if_mismatch>

      <run>comp-find "identity_scope" infra/aws/ec2/opal-gateway</run>
      <expect>The EXISTING identity_scope machinery localized -- the endpoint EXTENDS it (build ladder rung 2), never rebuilds it. Server-side firm claim, never from the request body (trade-workflow-handler reference pattern).</expect>
      <if_mismatch>If the machinery is not found where expected, read the gateway app source before scaffolding anything.</if_mismatch>

    Phase 2 -- before committing:
      <run>python infra/aws/ec2/opal-gateway/app/graphql_plumbing/exercise_catalog_gate.py</run>
      <expect>13/13 against the PORTED live catalog, rows 4 and 7 explicitly re-exercised (the port-time-delta pair)</expect>
      <if_mismatch>A failing row after the port = the port changed semantics -- stop, diff staged vs ported, do not deploy.</if_mismatch>

    Phase 3 -- after committing / deploying:
      <run>on-box battery per DESIGN.md checklist 5 (SSM execution or the runner's own exit-log -- Rule 22a APPLIED evidence, never a staged-file read)</run>
      <expect>13/13 on-instance -- same file, same catalog</expect>
      <if_mismatch>Staged-vs-executing divergence: the EC2 S3 pull may be first-boot-only -- verify the on-instance bytes, then redeploy; escalate to COO if the box executes a baked copy.</if_mismatch>

      <run>comp-iam service opal-gateway (ONLY if the apply adds any new boto3 call)</run>
      <expect>No new gaps -- the audit line rides the EXISTING audit.py to s3://opal-mcp-audit, no new sink, so no new grant expected. For any genuinely new (action, resource): aws iam simulate-principal-policy, ONE --resource-arns per call, positive control as a separate invocation (Rule 22a).</expect>
      <if_mismatch>A new grant requirement means the apply widened beyond the spec -- stop and re-read pin 4.</if_mismatch>

    Results go in your session-log Compiler Tools table. A TO with no compiler check logged
    is NOT accepted as complete.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: infra/aws/ec2/opal-gateway/app/graphql_plumbing/exercise_catalog_gate.py
      also_in_to: O-1 rider (cert) -- case authorship belongs to 0.5.0_AE_OpalETL~Z (site Z)
      last_write_owner: 0.5.0_AE_OpalETL~Z for the O-1 case
      required_action: MCP 0.5.0_AE_OpalETL~Z before any edit to this file; coordinate the O-1 case landing, do not author it.
    - shared_resource: the proposed limits numbers (endpoint config)
      also_in_to: 1.0.0_SA_CTO's W6 limits-review leg (live on their queue 2026-08-20)
      required_action: MCP 1.0.0_SA_CTO at apply with the PROPOSED numbers; their review verdict does not gate the deploy (numbers ship as PROPOSED) but must be on record.
    - shared_resource: infra/aws/ec2/EC2_MANIFEST.json
      required_action: pull latest before deploy; it is the CI/CD source of truth shared by every EC2 TO.
  </cross_domain_coordination>

  <acceptance_criteria>
    C1  PORT-CATALOG: the staged catalog lands at the live runtime refs/DATA_CATALOG.yaml
        path under the gateway app (per DESIGN.md checklist 3); version reads v0.2; diff vs
        workflows/atom_decomposition/catalog_v02/DATA_CATALOG.v0.2.staged.yaml is ZERO, or
        every port-time delta is named line-by-line in the PROOF_OF_SPEC instance.
    C2  BATTERY-AT-PORT: full 13-case exercise_catalog_gate.py run from this seat against
        the PORTED catalog: 13/13, rows 4 and 7 quoted in the instance.
    C3  ENDPOINT: POST /query/v0 accepts {key, params} (NOT GraphQL); principal resolved
        via the EXISTING identity_scope machinery (firm claim server-side, never the body);
        catalog_gate.gate() called; ALLOW fetches via the catalog row's own tool: path.
        Evidence = one exercised ALLOW + one exercised DENY at the DEPLOYED endpoint.
    C4  DEPLOY: safe-ec2-deploy.sh per EC2_MANIFEST (code, not TF); deploy output + manifest
        entry cited.
    C5  ON-BOX BATTERY: 13/13 post-deploy ON-INSTANCE (checklist 5; Rule 22a APPLIED
        evidence -- SSM execution or runner exit-log, never a staged-file read).
    C6  LIMITS: rows&lt;=1000 / 10s / 2MB / 30 per min per key enforced at the endpoint,
        labeled PROPOSED; at least ONE limit exercised behaviorally (a request that trips
        it); the numbers routed to 1.0.0_SA_CTO with their verdict-or-pending on record.
    C7  ZERO-MINT: identity_scope key census shows ZERO new partner keys; the instance
        cites the RULED zero-mint (Andrew-direct ~1425Z "zero-mint W6", pin 3) -- partner
        naming deferred to first-real-consumer, a future Andrew act.
    C8  AUDIT: one exercised request's audit line {ts, principal, firm, key, verdict,
        reason, bytes} present in s3://opal-mcp-audit via the existing audit.py -- object
        key cited.
    C9  SCOPE-HOLDS: no GraphQL parsing, no parquet resolver anywhere in the apply; a
        FLOOR_PATTERNS key request returns DENY at the deployed endpoint (exercised).
    C10 O-1-COORDINATED: the {scope}-family firm:per-scope battery case is landed by
        0.5.0_AE_OpalETL~Z, or their ACK of the routed ask is on record in the instance.
    C11 O-2-DISCHARGED: a CAPPED CALL at the deployed gateway exercises max_data_points in
        the live tool signature post-restart -- call output cited, not a config read.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ANALYST.W6-PORT_PROOF_OF_SPEC.json</instance_path>
    <!-- Validate BEFORE the complete flip, positional id set, CHECK THE RC:
         python .tools/proof-of-spec-check.py org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ANALYST.W6-PORT_PROOF_OF_SPEC.json C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11 -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="reference">infra/aws/ec2/opal-gateway/app/graphql_plumbing/DESIGN.md</file>
      <file action="reference">infra/aws/ec2/opal-gateway/app/graphql_plumbing/catalog_gate.py</file>
      <file action="create">infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml (confirm exact live path against DESIGN.md checklist 3 -- the endpoint passes it at startup)</file>
      <file action="create">the POST /query/v0 endpoint scaffold on the existing opal-gateway app (extend, not rebuild)</file>
      <file action="modify">infra/aws/ec2/EC2_MANIFEST.json (only if the service entry needs updating)</file>
      <file action="reference">infra/aws/ec2/opal-gateway/app/graphql_plumbing/exercise_catalog_gate.py (O-1 edit is 0.5.0_AE_OpalETL~Z's -- coordinate, never author)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Sequencing: the port (C1-C2) strictly precedes the apply (C3-C9). Surprise channel: anything outside this scope = one line to 2.0.0_SA_COO, no action, keep working.</requirement>
    <requirement id="2">Deliverables: the PROOF_OF_SPEC instance (validated rc=0) + a session log with the Compiler Tools table + an RAVC close to 2.0.0_SA_COO with evidence (commits, deploy output, exercised-call outputs).</requirement>
  </requirements>
</task_order>
