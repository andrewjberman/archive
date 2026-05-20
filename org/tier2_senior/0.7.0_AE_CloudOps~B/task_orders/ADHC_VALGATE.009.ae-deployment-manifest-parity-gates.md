<task_order>
  <metadata>
    <id>ADHC_VALGATE.009</id>
    <slug>ae-deployment-manifest-parity-gates</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-05-20 (authored on the CTO~B parity-follow-on ruling)</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO'd 2026-05-20 by 2.0.0_SA_COO~B. By-capacity (CTO~B ruling): deployment-manifest parity is independent of the Class-C/D gate machinery -- NO Phase-1 gate. Routed to 0.7.0_AE_CloudOps~B -- it authored the VALGATE.008 catalog that enumerated P6/P8/P9, it is the EC2/Lambda-infra lane, and it volunteered for the EC2-infra parity builds; idle, capacity available.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P2 -- VALGATE follow-on. Builds 3 of the 5 un-built declared-vs-empirical parity gates the VALGATE.008 catalog surfaced (org/modules/parity/PARITY_CLASS_CATALOG.md). Per CTO~B's ruling these 3 (P6/P9/P8) are bundled into ONE TO -- all small declared-vs-empirical parity checks, exactly VALGATE's mission, clean ~B AE-infra. P7 + P10 are documented-out (other-scope), not in this TO.</priority>
    <sla>~1-1.5d wall -- P6 + P9 are small aws-CLI-vs-JSON checks; P8 is a sweep wrapper over existing comp-pipescript logic.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 3.2 gate anatomy (six fields: Trigger/Input/Reference/Comparison/Verdict/Action); section 4.P parity-class; section 7 Q1 (v1 gates ship WARN-not-BLOCK).</prd>
    <origin>CTO~B parity-follow-on ruling 2026-05-20, on the ADHC_VALGATE.008 catalog (0.7~B). The catalog (org/modules/parity/PARITY_CLASS_CATALOG.md, canonical commit 418f1bd25) enumerated 10 declared-vs-empirical parity pairs; 5 un-built. CTO~B ruled P6+P9+P8 absorbed into VALGATE as this one bundled TO; P7 (comp-graph-vs-disk -> overlaps ADHC_COMPIL_V4.012, base) + P10 (gold_validate_config coverage -> comp-tooling scope) documented-out, NOT VALGATE TOs.</origin>
    <catalog>org/modules/parity/PARITY_CLASS_CATALOG.md -- the parity-pair registry; P6/P8/P9 rows carry the declared source / empirical source / comparison this TO builds.</catalog>
  </references>

  <context>
    A parity gate compares a `declared inventory` (a manifest / source-map / config) against the `empirical inventory` it claims to describe (the on-S3 / on-AWS / running-fleet reality). The VALGATE.008 catalog found 3 un-built deployment-manifest parity pairs that are clean ~B AE-infra: EC2_MANIFEST completeness (P6), Lambda source-map vs the deployed function set (P9), and repo-HEAD vs S3-deployed across the INF chain scripts (P8). This TO builds all three as WARN-mode v1 gates.
  </context>

  <scope>
    <step>P6 -- EC2_MANIFEST completeness gate. Compare infra/aws/ec2/EC2_MANIFEST.json's declared service set against the RUNNING EC2 fleet (+ each entry's source_path resolution). Per the .008 catalog refinement: the gate is manifest-completeness-vs-fleet, NOT folder-name matching (5 services have no infra/aws/ec2/<name>/ dir; verify-ec2.sh already covers registered-service code parity -- P6's gap is the manifest missing a running service, which verify-ec2.sh structurally can't see). Verdict: a running service absent from the manifest = WARN.</step>
    <step>P9 -- Lambda source-map vs deployed-function-set gate. Compare infra/aws/lambda/ci/lambda-source-map.json's function set against the deployed AWS Lambda set (aws lambda list-functions). Verdict: a deployed Lambda with no source-map entry (or a mapped function not deployed) = WARN. Bundles cleanly with P6 -- both are small declared-JSON-vs-live-AWS checks.</step>
    <step>P8 -- repo-HEAD vs S3-deployed sweep, across the ~56 INF chain scripts. THIN SCOPING per CTO~B: prefer a SWEEP WRAPPER over the existing `comp-pipescript deployed` per-script logic (which already does repo-HEAD-vs-S3 for one script) -- iterate it across the INF chain script set, collect the STALE/MISSING results. Do NOT pre-build a `--all` mode into comp-pipescript core blind. If a wrapper genuinely cannot do it without core comp-tool surgery, STOP -- split P8 out + flag it to the comp-tooling lane (surface to COO~B); do not do core surgery under this TO. Verdict: a script whose S3-deployed bytes != repo-HEAD = WARN (catches single-homed deploy-misses a collision census misses -- the AE 0.6.1 f39550d99 observation).</step>
    <step>Gate anatomy + verdict policy -- fill the PRD section-3.2 six-field gate table for each of P6/P9/P8. All three ship WARN-not-BLOCK in v1 (PRD section 7 Q1) -- surface the parity break, do not block anything. Where each gate FIRES (a scheduled check / a CI step / a comp-tool invocation) is the AE's placement call -- record it.</step>
    <step>Verify + RAVC2. Each gate verified: a clean state produces an empty/PASS report; a synthetic injected drift (a manifest entry removed / a stale S3 object) produces the expected WARN. RAVC2 to 2.0.0_SA_COO~B (CC 1.0.0_SA_CTO~B): the 3 gates, their placement, the six-field tables, the verification transcripts, any P8-split escalation.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">P6 EC2_MANIFEST-completeness-vs-running-fleet gate built; WARN on a running service absent from the manifest; six-field gate table filled.</ac>
    <ac id="AC2">P9 Lambda-source-map-vs-deployed-set gate built; WARN on a deployed Lambda with no source-map entry (or vice versa); six-field table filled.</ac>
    <ac id="AC3">P8 repo-HEAD-vs-S3-deployed sweep built as a wrapper over existing comp-pipescript-deployed logic (NOT a blind core --all mode); WARN on a script whose S3 bytes != repo-HEAD. If a wrapper is not feasible without comp-tool core surgery, P8 is split out + flagged to comp-tooling -- documented, not forced.</ac>
    <ac id="AC4">All three gates ship WARN-not-BLOCK v1 (PRD section 7 Q1) -- no gate blocks any deploy/chain/CI in v1.</ac>
    <ac id="AC5">Each gate verified: clean-state empty/PASS + synthetic-drift produces the expected WARN. No emoji. Session log with Compiler Tools section. RAVC2 to COO~B CC CTO~B.</ac>
  </acceptance_criteria>

  <out_of_scope>
    P7 (comp-graph node-set vs disk files) -- documented-out per CTO~B: overlaps ADHC_COMPIL_V4.012 (base project), which owns it; the catalog records P7 as covered-by/reconcile-with COMPIL_V4.012, NOT a VALGATE TO. P10 (gold_validate_config.yaml coverage vs gold scripts) -- documented-out: comp-tooling / gold-validate scope, not ~B. The DRIFTD-owned P4/P5 (EventBridge cron-maps + portal deploy manifest) -- DRIFTD v0.2, base-scope, referenced not duplicated. Core comp-pipescript surgery for P8 (split + flag if needed). Ratcheting any gate to BLOCK (v1 is WARN-only).
  </out_of_scope>

  <deliverables>
    - 3 deployment-manifest parity gates (P6 EC2_MANIFEST completeness, P9 source-map vs deployed Lambdas, P8 repo-HEAD vs S3 sweep), WARN-mode v1, six-field gate tables, verification transcripts; RAVC2 to COO~B CC CTO~B.
  </deliverables>
</task_order>
