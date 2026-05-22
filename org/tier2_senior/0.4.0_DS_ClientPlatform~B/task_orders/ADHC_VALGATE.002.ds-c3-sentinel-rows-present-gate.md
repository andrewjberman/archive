<task_order>
  <metadata>
    <id>ADHC_VALGATE.002</id>
    <slug>ds-c3-sentinel-rows-present-gate</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18 (re-routed ~C->~B 2026-05-20 by 2.0.0_SA_COO~B)</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-22 (stale-status correction, 2.0.0_SA_COO at Andrew direction): work shipped 2fd7415fb (0.4.0_DS_ClientPlatform~B -- C-3 sentinel-rows-present gate); RAVC2-accepted + closed by 2.0.0_SA_COO~B in b4d9836b5 ("close ADHC_VALGATE.002 -- C-3 sentinel-rows gate accepted"); follow-up cosmetic stale-echo fix cc56f8dfe. ADHC_VALGATE project closed 9/9 on 2026-05-21 (930bcc235). The TO <status> flag was simply never synced at close -- no work outstanding. -->
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GATE CLEARED + GO'd 2026-05-20 by 2.0.0_SA_COO~B -- VALGATE.001 is RAVC-accepted (gate machinery + chain-wire all shipped + verified). C-3 reuses .001's rolling-baseline read API (valgate_baseline.py) + the gate-fire surface (the non-fatal valgate_gate.py invocation in orion-gold-dispatch.sh's run_chain loop, pre-INF_09). SEQUENCING: DS~B's MDPF_ASSETS.029 Phase-0 dry-run is the MDPF critical path and takes precedence; .002 is next-in-queue after the .029 Phase-0 brief lands.</dispatch_unblock_condition>
    <project_code>ADHC_VALGATE</project_code>
    <priority>P1 -- VALGATE Phase 1. C-3 catches known-stable key identifiers silently dropping out of partitions -- the INFGRO/INFNNA rep_id drop-out class, which ties to the INF_C_02 perf-coverage gap (INFGRO PRD section 8.4 Finding B).</priority>
    <sla>1-1.5d wall (PRD section 6 sizing) -- thin once VALGATE.001's machinery exists; the work is the gate logic + the sentinel registry.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_VALGATE.md (v0.1) -- section 4.C C-3 spec, section 3.2 gate anatomy, section 7 Q1 verdict policy.</prd>
    <depends_on>ADHC_VALGATE.001 -- the rolling-baseline machinery + the gate-fire surface. C-3 is a consumer of .001's read API.</depends_on>
    <anchor>INFGRO / INFNNA rep_id drop-outs -- known-stable rep_ids silently absent from partitions; ties to the INF_C_02 perf-coverage gap (INFGRO Finding B, the ~$106M / managed-only-coverage class).</anchor>
  </references>

  <context>
    C-3 is the sentinel-rows-present gate. Reference: a small, declared set of KNOWN-STABLE sentinel identifiers (rep_ids, advisor keys, household keys) that must appear in every partition carrying material activity. Comparison: set difference -- a sentinel absent from a non-empty material partition is a WARN. It catches the failure mode where a partition is shape-clean and not row-count-anomalous (so C-1 passes) but a specific known-stable entity silently dropped out -- exactly the rep_id drop-out class.

    C-3 needs two pieces: (a) the gate logic (on a fresh partition, diff the present key set against the declared sentinel set), and (b) the declared sentinel-identifier REGISTRY -- the curated list of known-stable identifiers per artifact, with the basis for each (why this rep_id/advisor is known-stable).
  </context>

  <scope>
    <step>Phase 1 -- author the declared sentinel-identifier registry: a curated, version-controlled list of known-stable key identifiers per gated artifact (rep_ids / advisor keys / household keys), each with a one-line basis (why it is known-stable + material). Source the candidates empirically from recent stable partitions; do NOT pick arbitrarily.</step>
    <step>Phase 2 -- the C-3 gate: on a freshly-built partition, if the partition carries material activity (non-empty, above a minimal-activity floor), diff the present key set against the declared sentinel set; WARN on any sentinel absent. A sentinel legitimately absent (e.g. an advisor genuinely off-book) is registry maintenance -- the gate WARNs, the owner curates.</step>
    <step>Phase 3 -- wire C-3 at the same gate-fire surface VALGATE.001 chose (reuse, do not re-decide); reuse .001's baseline read API where the registry or activity-floor needs historical context. Fill the section-3.2 six-field gate table. Verify firing on a real chain run.</step>
  </scope>

  <gate_verdict_policy>C-3 ships WARN-not-BLOCK in v1 (PRD section 7 Q1). A missing sentinel WARNs + routes to the artifact owner; it does not fail the chain.</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io (each silver/gold script whose partition C-3 gates)</run>
        <expect>The artifact path + the key-identifier column (rep_id / advisor key / household key) C-3 reads -- confirms the gate reads the producer's actual output + the right key column.</expect>
        <if_mismatch>Reconcile the key column with the producer before building the registry.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed (the gate script, if chain-step-deployed)</run>
        <expect>MATCH before the verification chain run.</expect>
        <if_mismatch>Re-upload before verifying.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A read-only validation gate + a declared registry; no producer script modified, no data artifact content changed.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    C-3 reuses VALGATE.001's gate-fire surface (the orion-gold-dispatch.sh step or post-chain Lambda) -- so it inherits .001's coordination with the hot gold chain (RUNDATE-DISPATCH-IMPL, SYNC-COLLISION, INFGRO). No NEW orion-gold-dispatch.sh surface beyond what .001 established. The sentinel registry is new VALGATE-owned config -- no cross-domain file overlap.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A declared sentinel-identifier registry ships -- per-artifact known-stable key identifiers, each with an empirically-sourced basis. Version-controlled.</ac>
    <ac id="AC2">The C-3 gate fires on a freshly-built material-activity partition, WARNs on any declared sentinel absent from the present key set; the section-3.2 six-field table is filled.</ac>
    <ac id="AC3">The gate correctly SKIPS (no WARN) on a partition below the minimal-activity floor -- an empty/low partition legitimately has no sentinels and must not spuriously WARN.</ac>
    <ac id="AC4">C-3 is wired at VALGATE.001's gate-fire surface and verified firing on a real chain run with a WARN verdict; reuses .001's baseline read API where historical context is needed.</ac>
    <ac id="AC5">No emoji; Rule 15/16 as applicable; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The declared sentinel-identifier registry.
    - The C-3 gate, wired + verified, WARN verdict.
    - The section-3.2 six-field gate table for C-3.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
