<task_order>
  <metadata>
    <id>MDPF_ASSETS.011</id>
    <slug>dsbase-smartx-per-account-model-membership-probe</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-18</date>
    <status>cancelled</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>SUPERSEDED + CANCELLED 2026-05-18 (COO), before DS Base spent any effort. WS-B's own Phase-0 gate (MDPF_ASSETS.007, DS~A) resolved this TO's exact question concurrently and faster: SmartX `enterprises/allocations?modelid={modelId}` returns a per-allocation roster with per-account `value` -- account-grain 49F model membership IS feasible, PRD named-gap-2 closed. The mechanism + the verdict are in DS~A's Phase-0 brief docs/briefs/mdpf-assets-007-wsb-49f-smartx-phase0-feasibility-20260518.md (commit f5991b5bd). The SmartX↔BD join (this TO's Phase 2) is also moot -- SmartX carries per-account value directly, no BD join needed. Nothing for DS Base to do; this TO is closed unstarted. The de-risking instinct was right; WS-B simply self-resolved it faster than the dedicated probe could dispatch.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- Andrew-direct. WS-B (49F model AUA, Cohort 1a) cannot build account-grain without an account-to-model mechanism; this probe determines whether one exists. It de-risks the largest open question in MDPF Phase 2.</priority>
    <sla>1-1.5d wall -- a read-only backend probe ending in a finding brief. NOT a build.</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md (RATIFIED) -- §3.1: the model_aua_positions artifact is ACCOUNT-grain (one row per firm_id, model_key, account_id, as_of_date, with per-account model_value). WS-B for 49F must emit this. The contract REQUIRES account grain -- this probe determines whether 49F can meet it.</contract>
    <gated_to>org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/MDPF_ASSETS.007.dsa-wsb-49f-smartx-model-aua-feeder.md (WS-B, DS~A, in-progress). WS-B's Phase-0 step (a) -- "does a 49F per-account model-membership source exist" -- is OWNED BY THIS TO. WS-B's Phase 0 continues on parts (b) SXPL_RESTIN feeder state + (c) the data/smartx/ owned-paths blocker; WS-B's Phase-1 build gates on THIS TO's verdict.</gated_to>
    <prior_smartx_work>
      - docs/briefs/smartx-rest-integration-design-20260515.md (SXPL_RESTIN design brief, commit 352ab4585) -- the HAR analysis of a live SmartX manager-portal session + the ROPC token mechanism. The HAR is the starting point: it captured the manager portal's actual backend calls.
      - docs/briefs/smartx-per-model-availability-matrix-20260515.md (SXPL_RESTIN.001, commit bd5d7d068) -- the 13-endpoint x 7-model availability matrix. NOTE: that matrix is per-MODEL. This probe is per-ACCOUNT -- a different axis; the matrix is the inventory of known endpoints to start from, not the answer.
    </prior_smartx_work>
    <join_target>docs/briefs/mdpf-49f-nonmodel-custody-cutout-audit-20260518.md (MDPF_ASSETS.001) -- the 49F account_id space lives in Black Diamond silver (silver/allocations.account_id, the account_id->custodian crosswalk). BD has 49F account-grain market values but NO model tag. If SmartX supplies the model tag, the two must join on account identity -- this probe assesses that join.</join_target>
  </references>

  <context>
    Andrew (direct, 2026-05-18): "We want to see if there is a mechanism through the SmartX backend to start putting the pieces together on which 49 accounts are in what models."

    The MDPF WS-A contract requires 49F model AUA at ACCOUNT grain -- one row per (account, model, value). The 49F model data seen so far is a per-MODEL scalar (PRD named-gap-2: "model_aua is a SmartX scalar, not account-keyed to BD"). To build the contract's account-grain model_aua_positions, WS-B needs per-account model membership: which 49F account is assigned to which Opal model. SmartX is a managed-account (SMA/UMA) platform -- it manages individual accounts, so account-level model assignment EXISTS in its system; the open question is whether the SmartX backend (the REST API the manager portal uses) EXPOSES it.

    This is a read-only investigation. It probes the SmartX backend for an account-to-model mechanism, and assesses how an account-model assignment from SmartX would join to the 49F account market values that live in Black Diamond. It does NOT build the WS-B feeder -- it produces the finding that tells WS-B whether (and how) account-grain is buildable. The two probable outcomes: (1) a usable account-to-model mechanism exists -> WS-B Phase 1 proceeds account-grain; (2) it does not -> escalate to COO+CTO, a ratified-contract question (account-grain is contractual, not optional).
  </context>

  <scope>
    <step>Phase 0 -- absorb. Read the SXPL_RESTIN design brief (the HAR) + the .001 per-model availability matrix + the WS-A contract §3.1. Inventory the SmartX endpoint surface already known; identify which endpoints are account-scoped vs model-scoped.</step>
    <step>Phase 1 -- probe the SmartX backend for an account-to-model mechanism. Working from the HAR-captured manager-portal calls + the SmartX REST surface, determine whether the backend exposes, for 49 Financial:
      - an account inventory (the list of 49F accounts SmartX manages);
      - per-account model / sleeve / strategy assignment (which Opal model each account is in -- the core question);
      - per-account value / holdings (account market value, so model_aua can be summed at account grain).
      Probe live (read-only) where the briefs do not already answer it -- reuse the SXPL_RESTIN ROPC token / smartx JWT auth; provision no new auth. Record, per relevant endpoint: the resource, whether it is account-grain, what model-membership + value fields it carries, and the refresh cadence.</step>
    <step>Phase 2 -- assess the join. The likely shape is SmartX (account -> model assignment) joined to Black Diamond (account -> market value, the .001 silver/allocations space). Determine: can a SmartX account identifier be reconciled to a BD account_id? Is there a shared key (account number, registration, tax id), or is the join lossy? If SmartX itself carries per-account VALUE, the BD join may be unnecessary -- state which path is cleaner.</step>
    <step>Phase 3 -- the finding brief (docs/briefs/). A clear verdict: IS per-account 49F model membership obtainable -- YES (via which endpoint(s), at what cadence, with value in-hand or via the BD join) or NO. If YES: the concrete mechanism WS-B Phase 1 builds on. If NO: the escalation -- account-grain is a ratified-contract requirement, so a NO routes to COO+CTO as a contract question, not a silent model-grain downgrade. RAVC2 to COO; the brief feeds WS-B (MDPF_ASSETS.007).</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>No comp-* graph tool applies -- this is an external-backend feasibility probe (the .002 / .003 precedent), not a pipeline-graph trace. State N/A in one line. The empirical method is direct read-only SmartX REST calls + the HAR.</run>
        <expect>N/A -- documented.</expect>
        <if_mismatch>n/a</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-iam service / comp-iam gaps ONLY if the probe added a committed harness with a new AWS surface -- a read-only investigation should not. State N/A if so.</run>
        <expect>N/A -- a read-only probe, no new AWS surface.</expect>
        <if_mismatch>n/a</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A read-only backend probe ending in a finding brief. No pipeline producer touched, no data written, no reprocessing. Live SmartX REST calls are read-only GETs.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    This TO owns WS-B's (MDPF_ASSETS.007) Phase-0 question (a) -- coordinate with DS~A (the WS-B lane): DS~A's WS-B Phase 0 continues on parts (b) SXPL_RESTIN feeder state + (c) the data/smartx/ owned-paths blocker; WS-B's Phase-1 build gates on THIS TO's verdict. ALSO: data/smartx/ is owned-paths-registered to POD3 (not Pod-4 DS) -- a probe HARNESS, if committed, may be hook-blocked; keep the probe read-only and, if a harness must be committed, expect the owned-paths block and route to COO (do not force). Reuse the SXPL_RESTIN auth -- the SmartX EC2 browser-exporter (the proven canonical source) and the SXPL_RESTIN REST pull are untouched by a read-only probe.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A finding brief ships at docs/briefs/ with a clear verdict: is per-account 49F model membership obtainable through the SmartX backend -- YES or NO.</ac>
    <ac id="AC2">If YES: the concrete mechanism -- the endpoint(s), the account-to-model fields, the per-account value path (SmartX-native or via the BD join), and the refresh cadence -- specified so WS-B Phase 1 can build directly on it.</ac>
    <ac id="AC3">The SmartX-account-id to BD-account_id join is assessed -- shared key identified, or the join flagged lossy, or stated unnecessary if SmartX carries per-account value itself.</ac>
    <ac id="AC4">If NO: the finding is escalated to COO+CTO as a ratified-contract question (model_aua_positions is account-grain by contract) -- NOT presented as a routine model-grain fallback.</ac>
    <ac id="AC5">No emoji; session log with the Compiler Tools section. RAVC2 to COO; the brief feeds WS-B (MDPF_ASSETS.007).</ac>
  </acceptance_criteria>

  <deliverables>
    - The SmartX per-account-model-membership finding brief (docs/briefs/) -- the verdict + the mechanism (or the escalation).
    - The SmartX-to-BD account-join assessment.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
