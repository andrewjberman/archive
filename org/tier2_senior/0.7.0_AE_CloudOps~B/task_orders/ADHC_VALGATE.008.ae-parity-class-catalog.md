<task_order>
  <metadata>
    <id>ADHC_VALGATE.008</id>
    <slug>ae-parity-class-catalog</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-05-18 (re-routed ~base->~B + DISPATCHED 2026-05-20 by 2.0.0_SA_COO~B)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RE-ROUTED + GO'd 2026-05-20 by 2.0.0_SA_COO~B. ADHC_VALGATE execution ownership is the ~B C-suite; the original base issued_to/issued_by predate the re-org. PULLED FORWARD: per the TO's own statement this Phase-3 catalog has NO hard dependency on Phase 1/2 (it's a declared-vs-empirical parity-pair catalog, independent of the Class-C gate machinery) -- so it is dispatched NOW in parallel with the .029/.002/.003 critical path, using the idle ~B AE capacity, rather than waiting for Phase 1 to finish. Routed to 0.7.0_AE_CloudOps~B (idle watchdog standby; the original base lane was 0.7.0_AE_CloudOps -- natural ~B successor). Sibling .007 (Class-B chainrun pre/post diff) is NOT pulled forward -- its own TO explicitly gates it on VALGATE Phase 1 (.001-.003) shipping (the chain-gate surface + verdict conventions), and wiring it concurrent with .002/.003's Class-C gate edits to orion-gold-dispatch.sh is a shared-file collision risk; .007 re-routes + GOs when .002/.003 complete.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P2 -- VALGATE Phase 3. The parity gate SHAPE (declared inventory vs empirical inventory) recurs; only one instance is built. Catalog the sites + route the un-built ones.</priority>
    <sla>1d wall (PRD section 6 sizing) -- a catalog deliverable, not a build.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 4.P (parity-class catalog, N8), section 2 (the parity row -- one built instance), section 3.4 (DRIFTD owns the source-map parity check; VALGATE catalogs, does not duplicate).</prd>
    <built_instance>ADHC_DRIFTD.002 -- the Lambda source-map files-array vs source_dir parity check. DRIFTD v0.2 also extends to EventBridge cron resource-maps + a portal deployment manifest -- DRIFTD-owned.</built_instance>
    <field_observation>AE 0.6.1, 2026-05-18 (INFINC.006 chain-validation + SYNC-COLLISION): a deploy-miss can hit SINGLE-homed scripts, not just collision-prone multi-homed ones -- pull_inflection_performance_rest.py shipped a commit (f39550d99) that never reached any S3 code/ prefix. A full repo-HEAD-vs-S3-deployed parity audit across all ~56 INF chain scripts would catch single-homed deploy-misses that a collision census cannot. AE 0.6.1 recommended this as a VALGATE.008 catalog candidate.</field_observation>
  </references>

  <context>
    The parity gate is not a class -- it is a recurring gate SHAPE: a `declared inventory` (a manifest, a files-array, a graph node-set, a source map) compared against the `empirical inventory` it claims to describe (an on-disk / on-S3 / on-runtime scan). One instance is built (ADHC_DRIFTD.002 source-map parity). Several sites are un-built.

    VALGATE.008's deliverable is the CATALOG itself -- a single registry of every declared-vs-empirical parity pair, its current gate status (built / un-built), and its owner. Building each missing parity check is a follow-on TO routed to the relevant infra owner; VALGATE.008 does NOT build the checks (except where one is trivial enough to fold in -- AE's call, noted per site).
  </context>

  <scope>
    <step>Phase 1 -- enumerate every declared-vs-empirical parity pair. Seed set (PRD section 4.P + the AE 0.6.1 field observation):
      - Lambda source-map files-array vs source_dir -- BUILT (ADHC_DRIFTD.002).
      - EventBridge cron resource-maps + portal deployment manifest -- DRIFTD v0.2 (owned by DRIFTD).
      - EC2_MANIFEST.json vs infra/aws/ec2/ -- un-built.
      - comp-graph nodes vs actual .py / .tsx files on disk -- un-built.
      - repo-HEAD vs S3-deployed code, across all ~56 INF chain scripts (the AE 0.6.1 deploy-miss observation) -- un-built; this catches single-homed deploy-misses a collision census misses.
      - any other declared-vs-empirical pair the enumeration surfaces.
    </step>
    <step>Phase 2 -- build the catalog: org/modules/parity/ (a catalog file, or a comp-tools.yaml parity subsection -- AE's call). For each pair: the declared source, the empirical source, the comparison, the current gate status (built / un-built), and the owner.</step>
    <step>Phase 3 -- route the un-built sites: for each un-built pair, name the owning lane (EC2_MANIFEST parity -> AE infra; comp-graph-vs-disk -> the comp-tooling lane; repo-HEAD-vs-S3 deploy parity -> AE pipeline). Surface the routing to COO -- COO authors the follow-on build TOs. Do NOT duplicate DRIFTD-owned checks; the catalog references them, DRIFTD owns them.</step>
  </scope>

  <gate_verdict_policy>VALGATE.008 ships a CATALOG, not a gate -- no verdict policy. The follow-on build TOs (one per un-built site) carry their own verdict policy when authored, defaulting WARN-not-BLOCK per PRD section 7 Q1.</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat org/modules/graph/comp-tools.yaml | head -60 (and inspect the ADHC_DRIFTD parity check structure)</run>
        <expect>The existing catalog/registry conventions + the DRIFTD-built parity instance -- so the new catalog matches house structure and correctly references (not duplicates) DRIFTD's checks.</expect>
        <if_mismatch>Use the DRIFTD project JSON + .002 TO as the source of truth for the built instance.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-iam gaps (only if VALGATE.008 itself adds an AWS-touching check -- it should not; the catalog is documentation)</run>
        <expect>N/A -- VALGATE.008 is a catalog deliverable, no new AWS surface. State so in one line.</expect>
        <if_mismatch>n/a</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A catalog/documentation deliverable; no code, no data, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    VALGATE.008 catalogs; ADHC_DRIFTD owns the source-map + cron + portal-manifest parity CHECKS -- the catalog references them, does not re-author or duplicate them (PRD section 3.4 + 4.P). No file overlap if the catalog stays in org/modules/parity/. The follow-on build TOs route to infra owners via COO -- not authored in this TO.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A parity catalog ships at org/modules/parity/ (or a comp-tools.yaml parity subsection) -- every declared-vs-empirical parity pair listed with: declared source, empirical source, comparison, gate status (built/un-built), owner.</ac>
    <ac id="AC2">The catalog includes the seed set: the DRIFTD-built source-map instance (referenced, not duplicated), EC2_MANIFEST-vs-infra/aws/ec2/, comp-graph-nodes-vs-disk, and the repo-HEAD-vs-S3-deployed parity across the ~56 INF chain scripts (the AE 0.6.1 deploy-miss observation).</ac>
    <ac id="AC3">Each un-built site has a named owning lane; the routing is surfaced to COO for follow-on build-TO authoring. DRIFTD-owned checks are referenced, not duplicated.</ac>
    <ac id="AC4">No emoji; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The parity-class catalog (org/modules/parity/).
    - A routing list of un-built parity sites + owning lanes, surfaced to COO.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
