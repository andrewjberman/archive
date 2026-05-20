<task_order>
  <metadata>
    <id>ADHC_VALGATE.001</id>
    <slug>ds-c1-c2-rowcount-distribution-gate</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <coordinates_with>0.7.0_AE_CloudOps~B (chain-wire / gate placement)</coordinates_with>
    <date>2026-05-18 (re-routed ~C->~B + DISPATCHED 2026-05-20 by 2.0.0_SA_COO~B)</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RE-ROUTED + DISPATCHED 2026-05-20 by 2.0.0_SA_COO~B. ADHC_VALGATE execution ownership transferred to the ~B C-suite 2026-05-18 (Andrew); the original ~C issued_to + base-COO issued_by predate the ~B re-org and are stale -- re-routed to 0.4.0_DS_ClientPlatform~B (idle, capacity available). GO fired to DS~B 2026-05-20. The AE-side chain-wire/gate-placement coordination (originally AE 0.7) now coordinates with the ~B AE lane -- DS~B's Phase-0 placement step confirms the gate-fire surface; the actual chain-wire is sequenced with the ~B AE owner of the gold chain (0.5.0_AE_OpalETL~B / 0.7.0_AE_CloudOps~B per COO~B). VALGATE.002 + .003 stay staged -- they hard-gate on this TO's rolling-baseline machinery shipping + RAVC2-accept.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P1 -- VALGATE Phase 1, the foundation TO. It builds the rolling-baseline storage + read machinery that VALGATE.002 + .003 reuse; it MUST ship before them. Closes the highest-leverage gap (the DWSPLT chain-#27 class -- a 150x row swing + zero-NNA partition that passed every gate).</priority>
    <sla>2-3d wall (PRD section 6 sizing) -- the baseline machinery is the bulk; C-1 + C-2 are thin once it exists.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1, 1.0.0_SA_CTO) -- section 3 (four-class taxonomy), section 4.C (C-1 + C-2 specs), section 3.2 (gate anatomy: trigger/input/reference/comparison/verdict/action), section 7 Q2 (placement) + Q3 (baseline storage).</prd>
    <anchor>DWSPLT chain #27 (2026-05-13): a mode=full chain passed every A/B/C/D sentinel green while the silver/transactions partition carried 16,882 rows vs 115 the prior day (150x) with ZERO NNA-classified rows. No automated gate flagged it -- only Andrew's instinct. C-1 + C-2 are the gates that would have WARN'd.</anchor>
    <gate_anatomy>PRD section 3.2 -- each gate is six fields: Trigger, Input, Reference, Comparison, Verdict, Action. Fill the table for C-1 and C-2 in the deliverable.</gate_anatomy>
  </references>

  <context>
    A Class-C defect is shape-clean but content-regressed: the artifact has the right columns and a positive row count, so every Class-A/B shape check passes, but the content silently regressed (a 150x row swing, a classification bucket gone to zero). Catching it requires a reference the code does not contain -- a rolling N-day baseline of the artifact's own content statistics.

    VALGATE.001 builds (a) the rolling-baseline machinery and (b) the first two gates on top of it:
    - C-1 row-count stability -- current row count vs the rolling N-day median; WARN when current/median is outside [1/K, K] (K ~5, tunable per artifact).
    - C-2 classification-distribution stability -- per-bucket classification rate (NNA-rate / Internal-rate / Return-rate / any categorical) vs the rolling N-day rate; WARN when a bucket falls below an absolute floor (e.g. zero NNA in a material-activity partition) OR shifts beyond a distribution-distance threshold.
    The baseline machinery is the reusable foundation -- VALGATE.002 (C-3) and .003 (C-4) read it; .001 ships first.
  </context>

  <scope>
    <step>
      Phase 0 -- placement decision (PRD section 7 Q2). With AE 0.7.0, decide WHERE the Class-C gate fires: a step inside orion-gold-dispatch.sh (post silver/gold build, pre-platinum-emit -- fails the chain loudest) vs a post-chain Lambda keyed off pipeline-complete.json (least invasive). Record the decision + rationale. This is the first step -- the rest of the build targets the chosen surface.
    </step>
    <step>
      Phase 1 -- the rolling-baseline machinery (PRD section 7 Q3). Build the baseline store + reader:
      - Storage: gold/meta/valgate-baseline/{artifact}/ (PRD candidate -- confirm path with AE 0.7). Per-artifact rolling window of content statistics (row count, per-bucket classification rates) for the last N days.
      - N is per-artifact configurable (a config map -- artifact -> N, K, bucket-floors).
      - Bootstrap behaviour: until the baseline has >= N/2 samples, the gate runs in WARN-SUPPRESSED mode (computes + records the statistic, emits no verdict) -- so a gate never fires spuriously on a cold artifact.
      - The machinery has a clean read API that VALGATE.002 + .003 reuse.
    </step>
    <step>
      Phase 2 -- C-1 row-count-stability gate. On a freshly-built silver/gold partition: compute the row count, read the rolling median, WARN when current/median is outside [1/K, K]. Fill the section-3.2 six-field gate table.
    </step>
    <step>
      Phase 3 -- C-2 classification-distribution-stability gate. On the same partition: compute per-bucket classification rates, compare vs the rolling baseline; WARN on an absolute-floor breach (a material-activity partition with a zero-rate bucket) OR a distribution-distance breach. Fill the six-field table.
    </step>
    <step>
      Phase 4 -- chain-wire (with AE 0.7.0) at the Phase-0-chosen surface; verify the gate fires on a real chain run and emits a verdict to the session-log / chain-log surface. Verdict = WARN for both gates (PRD section 7 Q1 -- v1 ships WARN-not-BLOCK until the false-positive rate is known).
    </step>
  </scope>

  <gate_verdict_policy>Per PRD section 7 Q1 (COO decomposition ruling): C-1 and C-2 ship WARN-not-BLOCK in v1. A WARN surfaces in the chain-log + session-log and routes to the artifact owner; it does NOT fail the chain. After ~1-2 weeks of empirical false-positive data the gate may ratchet to BLOCK (a separate follow-on decision, same two-stage tolerance discipline as INFGRO epsilon + comp-validate sentinels).</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io convert_transactions_to_silver (and the other silver/gold scripts whose partitions C-1/C-2 will gate)</run>
        <expect>The S3-DYNAMIC / written-artifact path for each gated partition (e.g. silver/transactions/{*}.parquet) -- confirms the gate reads the SAME artifact the producer writes.</expect>
        <if_mismatch>If the producer writes a different path than the gate reads, reconcile before building -- a gate on the wrong artifact is worse than no gate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed (the gate script, if it deploys as a chain-step script)</run>
        <expect>MATCH -- the runner has the gate code before the verification chain run.</expect>
        <if_mismatch>Re-upload to S3 before the Phase-4 verification run.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>VALGATE.001 adds a read-only validation gate + a meta baseline-store; it does not modify any silver/bronze/gold producer script and does not change any data artifact's content. The baseline store under gold/meta/valgate-baseline/ is new derived metadata, not a reprocess of pipeline data.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    THE GOLD CHAIN IS HOT. orion-gold-dispatch.sh -- the likely Class-C gate fire-site -- is concurrently touched by: ADVI_INFETL.RUNDATE-DISPATCH-IMPL (AE 0.7.0, E1/E2 dispatcher edits), ADVI_INFETL.SYNC-COLLISION (AE 0.6.1, sync_scripts() fix), and is exercised by every INFGRO chain run. Before the Phase-4 chain-wire: confirm RUNDATE-DISPATCH-IMPL + SYNC-COLLISION have landed (or coordinate a clean rebase) so the gate-wire does not collide with their orion-gold-dispatch.sh edits. comp-blast does not model the shell dispatcher (verified empty 2026-05-18) -- the fire-site coordination is established by direct file identity, not the graph. AE 0.7.0 is the gate-placement + chain-wire coordinator (it owns the dispatcher lane).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The Phase-0 gate-placement decision (orion-gold-dispatch.sh step vs post-chain Lambda) is recorded with rationale, decided jointly with AE 0.7.0.</ac>
    <ac id="AC2">The rolling-baseline machinery ships: per-artifact N-day content-statistic store (gold/meta/valgate-baseline/{artifact}/ or the AE-confirmed path), a per-artifact config map (N, K, bucket-floors), a clean read API, and WARN-SUPPRESSED bootstrap behaviour until >= N/2 samples exist.</ac>
    <ac id="AC3">C-1 row-count-stability gate fires on a freshly-built partition, WARNs when current/median is outside [1/K, K]; the section-3.2 six-field gate table is filled. Demonstrated against the DWSPLT-#27-class case (a synthetic or replayed 150x swing WARNs).</ac>
    <ac id="AC4">C-2 classification-distribution-stability gate fires on the same partition, WARNs on an absolute-bucket-floor breach (zero-rate bucket in a material partition) or a distribution-distance breach; six-field table filled.</ac>
    <ac id="AC5">The gate is chain-wired at the Phase-0 surface and verified firing on a real chain run, emitting WARN verdicts to the chain-log/session-log (not BLOCK -- gate_verdict_policy).</ac>
    <ac id="AC6">No emoji; Rule 15 (if a gold-tier .py) / Rule 16 (if a local-runtime bash component); session log with the Compiler Tools section. RAVC2 to COO. The baseline read API is documented for VALGATE.002 + .003 reuse.</ac>
  </acceptance_criteria>

  <deliverables>
    - The rolling-baseline machinery (store + config + read API).
    - C-1 + C-2 gates, chain-wired, WARN verdict.
    - The section-3.2 six-field gate table for C-1 and C-2.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
