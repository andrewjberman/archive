<task_order>
  <metadata>
    <id>ADVI_STAUDT.OPB</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-20</date>
    <status>held</status><!-- DISPATCHED 20260420T16:48Z then HELD 20260420T17:18Z by Andrew (relayed via CTO 20260420T172121Z). HOLD reason: this TO frames the question as A-vs-B internal-universe binary (canonical/nna/ 5,984 vs canonical/nna_atomic/ 9,592), which is a FALSE BINARY without anchoring to BD's authoritative active-account set (~6,554 accts at 2026-04-20). DS~A is on ad-hoc BD-anchored investigation per Andrew. Memory ref: project_bd_is_ground_truth.md. The "Penfield $400M-vs-$434M = universe truncation" framing in §bug_reference + §decision_authority was theory carried forward as conclusion (memory ref: feedback_no_unverified_theories_as_conclusions.md) and is not factually established. This TO will likely be REWRITTEN or REPLACED end-to-end after DS~A's investigation produces evidence — do NOT execute as-written. AE: do not pursue Phase 0 of this TO; await new TO. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — SCOPING ONLY (no code changes in this TO). Accelerated by CTO post-FIX3B-cancellation; FIX3B's failure made clear that interim D-script reverts can no longer paper over the universe asymmetry. Option B is now the architectural blocker for full identity restoration. Output: scoping document defining surfaces, sequencing, risks, and ETA for the implementation TOs that will follow.</priority>
    <lane>AE 0.6.0 primary (owns C-layer + canonical/ ingestion + S3 schema decisions). DS ~A supporting (D-script consumer perspective + post-FIX3A/FIX3B-cancel context).</lane>
    <bug_reference>Three converging issues that interim D-script fixes cannot resolve: (1) Penfield $400M-vs-$434M = universe truncation gap (5,984 nna/ accts vs 9,592 nna_atomic/ accts, 3,608 acct delta); (2) D_01 firm NNA $19.4M delta vs D_00c = D_01 sources silver views (NNA_AUA_BY_ADVISOR/GEOGRAPHY) instead of canonical/nna/, methodology fork; (3) Bug 4 role_aua/ cum_* P1 SHADOW state still active, blocks RA-P3/RA-P5 override re-enablement (currently disabled by FIX1+FIX7).</bug_reference>
    <decision_authority>CTO 20260420T164454Z accelerated authorization. Andrew session 2026-04-20.</decision_authority>
  </metadata>

  <references>
    <ref type="cto-acceleration">CTO 20260420T164454Z — "Option B: ACCELERATE. This is now blocking on the identity fix. Authorize AE 0.6.0 to start scoping immediately — do not wait for FIX1 prod close."</ref>
    <ref type="parquet-evidence">COO 20260420T163959Z — direct parquet schema inspection: nna/ (14 cols, 5,984 rows) HAS aua_current/growth/client_state; nna_atomic/ (22 cols, 9,592 rows) DOES NOT — has cum_* + multi-advisor roles + office instead</ref>
    <ref type="schema-doc">data/black_diamond/diagnostics/STAUDT/layer_C/c01_nna_schema_diff.md (verified accurate per parquet inspection)</ref>
    <ref type="inv1">data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md (firm-level universe asymmetry — 441 flow-only accts at 2020-12-31)</ref>
    <ref type="cancelled-fix">FIX3B (8a469bca) — CANCELLED 20260420T164454Z. Kept in repo as historical record of the wrong direction; do NOT revive.</ref>
    <ref type="related-interim">FIX1 (2fa1f2be), FIX7 (~A in flight), FIX6 (b7a75374) — all interim. FIX1 + FIX7 RA-P3/RA-P5 disables can be re-enabled when role_aua/ canonical state is correct (Bug 4 hygiene = part of Option B).</ref>
  </references>

  <objective>
    Produce a scoping document that defines the architectural Option B work to permanently resolve the canonical/nna/ universe asymmetry + D_01 methodology fork + role_aua/ P1 shadow state. Output is a written scoping document with surfaces, sequencing, risk register, and ETA for the implementation TOs that will follow. NO code changes in this TO. Implementation is gated on COO+CTO sign-off of the scoping doc.
  </objective>

  <scope>
    **Three convergent problem areas to scope:**

    **(a) canonical/nna/ ↔ nna_atomic/ universe + schema unification.**
    - Current state: nna/ (14 cols, 5,984 acct narrow universe) HAS aua_current/growth/client_state. nna_atomic/ (22 cols, 9,592 broader universe) HAS cum_*, multi-advisor roles, office, billable, is_excluded, is_ghost — but LACKS aua_current/growth/client_state.
    - Two viable directions to evaluate (decide which, in scoping doc):
      - **Direction 1: extend nna/ universe to 9,592 accts** (broaden to flow-only accts that lack holdings_lots coverage; assign default aua_current/client_state values for those accts)
      - **Direction 2: extend nna_atomic/ schema with aua_current/growth/client_state** (add columns from a join with holdings_lots-derived sources; preserve broader universe)
    - Trade-offs to evaluate: ingestion complexity, downstream consumer impact (D_00b/D_01/C_08 + FIX3A-deployed D_00c/D_02), historical backfill cost, data quality.
    - C_01 ingestion logic owns nna_atomic/; C-layer (C_03? C_07? AE confirms) owns nna/. Confirm in scoping doc.

    **(b) D_01 silver-view methodology fork.**
    - D_01 header_metrics.quarterly sources from silver views (NNA_AUA_BY_ADVISOR, NNA_AUA_BY_GEOGRAPHY) — different aggregation than D_00c/D_00b/D_04 which read canonical/nna/.
    - Result: $19.4M firm-level NNA delta D_01 vs D_00c (per ~A FIX3A close MCP 20260420T160534Z).
    - Scope: flip D_01 to canonical/nna/ source (or whatever the unified canonical lands at post-(a)). Identify D_01 line surface, evaluate dependencies on silver views (do other consumers need them?).

    **(c) role_aua/ Bug 4 hygiene (cum_* refresh).**
    - role_aua/ canonical is in P1 SHADOW state — not authoritative for downstream consumers.
    - This blocks re-enabling FIX1's RA-P3 override (D_00c L971-987) and FIX7's RA-P5 override (D_00b L788-798); both are currently guard-claused (`if False and ...`).
    - Scope: define what "P1 to canonical" looks like — schema validation, backfill plan, switchover criteria. Coordinate with prior ADVI_ROLLUP RA-P1/P2/P3/P5 work (~D and ~A already touched this surface).

    **Scoping deliverables (the output of THIS TO):**

    1. **Scoping document** at `data/black_diamond/diagnostics/STAUDT/OPB/option_b_scoping.md`:
       - (a) Universe + schema unification: chosen direction (1 or 2) with rationale, surface map (which scripts), sequencing (which fixes go first), ingestion changes
       - (b) D_01 methodology unification: surface, plan
       - (c) role_aua/ canonical promotion: schema, backfill, switchover criteria
       - Risk register: rollback plan, partial-deploy hazards, validation strategy
       - ETA + lane assignments for the implementation TOs that will follow (do NOT issue them in this TO — just propose them)

    2. **Compiler-tools evidence** (per CLAUDE.md mandate before any cross-domain TO):
       - `comp-pipescript io C_01.canonical_nna` + any other C-script touching canonical/nna_atomic/
       - `comp-blast canonical/nna/` + `comp-blast canonical/nna_atomic/` (full consumer maps)
       - `comp-pipescript io D_01.partner_analytics` (or whatever its actual filename is — confirm)
       - `comp-blast` on each D-script that consumes role_aua/

    3. **Backfill cost estimate:** if Option B requires re-backfilling ~2,297 partitions of canonical/nna/ OR canonical/nna_atomic/, estimate compute time + S3 cost + risk window. Coordinate with EC2 capacity.

    **OUT OF SCOPE for this TO:**
    - NO code changes (scoping only)
    - NO ingestion changes
    - NO schema migrations
    - NO implementation TO authoring (those follow after COO+CTO sign-off on this scoping doc)
    - NO interim fixes — all interim work is in FIX1/FIX3A/FIX6/FIX7 already-deployed surfaces
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="surface mapping (mandatory before drafting scoping doc)">
      <step>
        <run>comp-pipescript io C_01.canonical_nna + comp-pipescript io on every C-script writing to canonical/nna/ or canonical/nna_atomic/</run>
        <expect>Full producer map. Confirm C_01 ownership; identify any other writers.</expect>
        <if_mismatch>If multiple C-scripts write either prefix, scoping must address coordination.</if_mismatch>
      </step>
      <step>
        <run>comp-blast canonical/nna/ + comp-blast canonical/nna_atomic/</run>
        <expect>Full consumer chain. Should match: D_00b, D_00c, D_01, D_02, D_04, C_08 — confirm no surprise consumers.</expect>
        <if_mismatch>Surprise consumers = scope must include them.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_01 (whichever its filename is) — confirm silver-view dependencies (NNA_AUA_BY_ADVISOR, NNA_AUA_BY_GEOGRAPHY)</run>
        <expect>Identify silver-view source path + computation logic. Determine if other consumers depend on those silver views.</expect>
        <if_mismatch>If silver views are widely consumed, deprecation has wider blast radius.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io on every script reading role_aua/ canonical (likely D_00b L306-356 + D_00c L971-987 (currently disabled) + D_00b L788-798 (currently disabled))</run>
        <expect>Full role_aua/ consumer map. Confirm Bug 4 P1 SHADOW state by inspecting current canonical/role_aua/ partition timestamps + schema.</expect>
        <if_mismatch>If role_aua/ has additional consumers, scoping must address re-enable cascade.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="scoping doc draft">
      <step>
        <run>Author scoping doc with all sections enumerated in scope</run>
        <expect>Document is implementation-ready: each downstream TO can be authored from the scoping doc without further investigation.</expect>
        <if_mismatch>If any section is "TBD" at this stage, surface to COO before submission.</if_mismatch>
      </step>
      <step>
        <run>MCP COO + CTO with scoping doc location + 1-paragraph executive summary covering chosen direction (a-1 vs a-2), D_01 plan summary, role_aua/ promotion summary, ETA, risk headlines</run>
        <expect>Executive summary is decision-ready; full doc is reference</expect>
        <if_mismatch>If COO or CTO requests revisions, iterate scoping doc before any implementation TO authoring</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/OPB/option_b_scoping.md</path>
      <description>Full scoping document covering (a) universe+schema unification (with chosen direction + rationale), (b) D_01 methodology unification, (c) role_aua/ canonical promotion. Includes surface maps, sequencing, risk register, ETA, and proposed implementation TO list (NOT the TOs themselves).</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/OPB/comp_evidence.md</path>
      <description>Per-script comp-pipescript io output, comp-blast output for canonical/nna/ + nna_atomic/ + role_aua/. Required by CLAUDE.md compiler-tools mandate before cross-domain TO authoring.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Phase 0 compiler-tools evidence file complete + filed at data/black_diamond/diagnostics/STAUDT/OPB/comp_evidence.md
    - [ ] Scoping doc enumerates direction choice (a-1 broaden nna/ universe vs a-2 extend nna_atomic/ schema) with rationale
    - [ ] D_01 methodology unification surface + plan documented
    - [ ] role_aua/ canonical promotion criteria + backfill plan documented
    - [ ] Risk register addresses rollback, partial-deploy hazards, validation strategy
    - [ ] Backfill cost + window estimate (compute time, S3 cost) documented
    - [ ] ETA + lane assignments proposed for implementation TOs
    - [ ] Executive summary MCP'd to COO + CTO
    - [ ] COO+CTO sign-off received before any implementation TO is authored from this scoping
  </acceptance_criteria>

  <guardrails>
    - **SCOPING ONLY** — no code, no schema migrations, no implementation TOs in this TO
    - **No interim-fix scope creep** — FIX1/FIX3A/FIX6/FIX7 are the interim layer; Option B is architectural, not patches
    - **Coordinate with DS ~A (supporting lane)** — they have the FIX3A/FIX3B-cancel context + D-script consumer perspective; pull them in for scoping doc review before submission
    - **Compiler-tools evidence is mandatory per CLAUDE.md cross-domain rule** — do NOT submit scoping doc without comp-pipescript io + comp-blast outputs filed
    - **Coordinate with prior ADVI_ROLLUP RA work** — the RA-P1/P2/P3/P5 wave touched role_aua/; pull existing canonical promotion docs into scoping rather than re-investigating
    - **Universe truncation is the user-visible blocker** — Penfield $400M-vs-$434M is documented as known limitation pending Option B; Andrew is monitoring this surface, so scoping doc should explicitly address how Option B closes the Penfield gap
    - **No emojis, selective staging, agent commit identity**
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - CTO MCP 20260420T164454Z (in your inbox or via get_agent_status broker)
       - data/black_diamond/diagnostics/STAUDT/layer_C/c01_nna_schema_diff.md (verified accurate)
       - data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md (firm-level universe asymmetry)
       - data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md + bug_attribution.md
       - C_01.canonical_nna.py (current ingestion logic, including --backfill-nna-atomic-only flag from FIX5)
       - prior ADVI_ROLLUP RA-P1/P2/P3/P5 PRDs/TOs (role_aua/ canonical promotion context)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min: "ACK STAUDT.OPB scoping — starting Phase 0 compiler-tools surface mapping"
    - Phase 0 gate: MCP COO with comp evidence filed, ready to draft scoping
    - Phase 1 gate: MCP COO + CTO with scoping doc + executive summary
    - RAVC step 4: COO+CTO sign-off cited; implementation TOs queued (separate authoring follows)
  </completion_protocol>
</task_order>
