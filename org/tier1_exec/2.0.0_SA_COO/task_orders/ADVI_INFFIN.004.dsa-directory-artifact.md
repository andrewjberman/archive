<task_order>
  <metadata>
    <id>ADVI_INFFIN.004</id>
    <slug>dsa-directory-artifact</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P2 — small isolated emit; contingent dependency for Surface #4 if RD-B (.002) routes to backend approach vs FE-iteration. Ships in parallel with .002 investigation; either approach works for Surface #4 ship</priority>
    <sla>~1-2h wall; ships standalone; small isolated scope</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief §Surface #4 + §Open Questions #2)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough 2026-05-13 — DS~A/~B/~C/~D all 4 sub-lanes available; this TO uses DS~A explicitly per Andrew greenlight</ref>
    <ref type="cross_link">Sibling: .002 RD advisor-context wiring (Surface #4 FE side; RD-B investigates FE-iteration first; if backend needed, consumes this artifact)</ref>
  </references>

  <context>
    Surface #4 (L3 ClientDetailPage missing advisor context via BI deeplink) requires HH → advisor reverse lookup at L3 mount. DE brief identifies two viable approaches:

    **(a) FE-side iteration:** RD-B (.002) iterates 4 advisor `book.json` files on L3 mount to build a reverse index. Cheap — 4 advisors only. No backend emit needed.

    **(b) DS-side directory artifact:** DS~A emits `s3://opal-data-inf/platinum/firm/client_directory.json` containing `hh_id → {advisor_id, advisor_name, display_name}` for O(1) lookup at L3 mount.

    .002 RD-B picks approach at investigation time (Phase 1 step 3 of .002). If FE-iteration suffices, .004 still ships as standalone deliverable for future-use (cleaner cache + faster L3 mount on cold load) but RD-B doesn't gate on it. If FE-iteration latency unacceptable, RD-B routes to consume .004.

    Andrew authorized DS~A explicitly for this TO (per DE alternative-lane-split recommendation). DS~A's INFGRO Stage 1 work shipped earlier today (Path B SmartX reconcile); current capacity available for this small isolated emit.

    Per Andrew session-scope: DS~A/~B/~C/~D all 4 sub-lanes authorized for INFFIN scope (overrides "base DS only" session-scope directive).
  </context>

  <objective>
    Emit `s3://opal-data-inf/platinum/firm/client_directory.json` as gold-tier sibling to existing per-advisor book.json files.

    Schema:
    ```json
    {
      "snapshot_date": "2026-05-13",
      "source_system": "orion-api",
      "households": {
        "338": {
          "advisor_id": "peter_lee",
          "advisor_key": "peter_lee",
          "advisor_name": "Peter Lee",
          "display_name": "NOEL SODERBLOM",
          "client_count": 1,
          "primary_account_id": "..."
        },
        ...
      }
    }
    ```

    Source: aggregate over 4 advisor book.json files (peter_lee + patrick_scanlan + joe_brandenburg + inflection_wealth_management) — for each `clients[].hh_id`, capture advisor attribution + display_name.

    Path A.2 cache-reader pattern OR direct sibling emit in INF_D_02 (or INF_D_03) per architectural preference. Single emit, single file.
  </objective>

  <scope>
    <surfaces>
      <surface id="4">Contingent backend emit for L3 ClientDetailPage HH → advisor reverse lookup</surface>
    </surfaces>
    <files>
      <file action="investigate">data/orion/scripts/gold/INF_D_02.advisor_client_detail.py — current advisor book.json emit shape; identify natural sibling location for client_directory.json emit</file>
      <file action="create_or_modify">data/orion/scripts/gold/INF_D_02b.client_directory.py (NEW script — recommended) OR extend INF_D_02 to additionally emit client_directory.json as sibling output</file>
      <file action="output">s3://opal-data-inf/platinum/firm/client_directory.json (NEW artifact)</file>
    </files>
  </scope>

  <phase id="1" when="investigation">
    <step>
      <description>Investigate INF_D_02.advisor_client_detail.py current emit. Where does it materialize per-advisor book.json? What's the in-memory advisor-keyed dict before serialization? That dict has the source data for client_directory.json (just inverse-indexed).</description>
      <expect>Source data + serialization pattern identified.</expect>
    </step>
    <step>
      <description>Decide: new sibling script INF_D_02b.client_directory.py OR extend INF_D_02 to emit a second artifact? Recommendation: new sibling script for separation of concerns + cleaner blast-radius. INF_D_02 stays focused on per-advisor book; INF_D_02b emits firm-level directory.</description>
      <expect>Sibling-script approach decided OR extension justified.</expect>
    </step>
    <step>
      <description>Verify .002 RD-B routing decision (consume .004 vs FE-iterate). Coordinate via COO — if RD-B's Phase 1 step 3 of .002 surfaces that FE-iteration is sufficient, this artifact still ships (future-use cache) but RD-B doesn't gate on it.</description>
      <expect>Coordination acknowledged; ship regardless of RD-B routing.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Author INF_D_02b.client_directory.py (or extend INF_D_02). Read 4 advisor book.json files from gold output (or in-memory dict pre-serialization if extending). For each `clients[].hh_id`, emit entry in `households` dict with advisor attribution + display_name + client_count.</description>
      <expect>Script generates valid client_directory.json with all Inflection HHs covered.</expect>
    </step>
    <step>
      <description>Handle multi-advisor HHs (if any exist — likely rare or zero for Inflection's flat structure). If multiple advisors share a HH, capture both advisors with primary/secondary attribution. Document in sentinel field.</description>
      <expect>Multi-advisor case handled OR documented as not-applicable for Inflection structure.</expect>
    </step>
    <step>
      <description>Emit to `s3://opal-data-inf/platinum/firm/client_directory.json`. Path follows `platinum/firm/` convention for firm-level (vs per-advisor) artifacts.</description>
      <expect>S3 emit successful; permissions correct.</expect>
    </step>
  </phase>

  <phase id="3" when="empirical-validation">
    <step>
      <description>Empirical: download client_directory.json from S3 + inspect. Verify all 4 advisors' HHs covered. Pick 3 known HHs (e.g., 338 from BI deeplink test case) + verify advisor + display_name resolve correctly.</description>
      <expect>All HHs covered; spot-check passes.</expect>
    </step>
    <step>
      <description>Coverage check: total HHs in directory should match sum of clients[] across all 4 advisor book.json files (minus any multi-advisor dedup).</description>
      <expect>Count consistent.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: New artifact `s3://opal-data-inf/platinum/firm/client_directory.json` exists post-chain.
    AC2: Schema: `{snapshot_date, source_system, households: {hh_id: {advisor_id, advisor_key, advisor_name, display_name, client_count}}}` with all Inflection HHs covered.
    AC3: All 4 Inflection advisors' HHs present (peter_lee + patrick_scanlan + joe_brandenburg + inflection_wealth_management).
    AC4: Spot-check 3 known HHs → advisor + display_name resolve correctly.
    AC5: ds-commit-gate PASS (py_compile + AST + ruff py39 + Rule 15 `from __future__ import annotations`).
    AC6: safe-deploy SHA-MATCH post-push.
    AC7: Sibling script approach (recommended) — INF_D_02 untouched OR extended cleanly with isolated client_directory emit.
    AC8: MCP RAVC2 to COO post-AC1-7 PASS.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-pipescript io (existing INF_D_02 + new INF_D_02b); comp-blast new script (zero existing consumers expected; future RD-B consumption only if .002 routes here)</phase_1>
    <phase_2>ds-commit-gate.sh on the new Python file; py_compile + AST + ruff py39 + Rule 15</phase_2>
    <phase_3>safe-deploy SHA-MATCH; post-chain empirical S3 inspection</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    NO UPSTREAM DEPS: independent of .001/.002/.003/.005.

    DOWNSTREAM CONSUMER (contingent):
    - .002 RD-B Surface #4 — RD investigates FE-iteration first; if backend needed, consumes this artifact. Either approach works for Surface #4 ship; this artifact is the future-proof O(1) lookup.

    NO PORTAL CONFLICT: this is pure gold-tier emit; no FE-side change.

    CHAIN-FIRE GATE: if you write the sibling script, .007 AE 0.6.1 chain fire materializes the new artifact. If you patch existing INF_D_02 in-place, same chain fire materializes via existing path.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <chain_fire_required>
      Gold-emit changes; chain fire materializes new artifact via .007 AE 0.6.1 dispatch.
    </chain_fire_required>
    <no_backfill_needed>
      Firm-level directory is point-in-time per snapshot_date; no historical backfill needed (FE consumes current snapshot only).
    </no_backfill_needed>
  </data_reprocess_scope>

  <deliverables>
    1. New artifact at `s3://opal-data-inf/platinum/firm/client_directory.json`
    2. New gold script (INF_D_02b.client_directory.py recommended) OR INF_D_02 extension
    3. Single commit under 0.4.0_DS_ClientPlatform~A author
    4. ds-commit-gate PASS + safe-deploy SHA-MATCH
    5. Session log with empirical spot-check evidence
    6. MCP RAVC2 to COO post-AC1-8 PASS
  </deliverables>

  <ravc>
    DS~A RAVC2 to COO post-AC1-8 PASS. .002 RD-B consumes if their Phase 1 step 3 routing decision picked backend approach; otherwise artifact is future-proof cache for L3 cold-load optimization. Either way, ship is structurally clean + standalone.
  </ravc>

  <notes>
    **Per Andrew session-scope override:** DS~A is explicitly authorized for INFFIN scope. This is a small isolated emit ideal for parallel-take alongside DS~C critical-path work (.003) + DS~B 49F audit (.005).

    **Architectural note:** this is firm-level artifact (`platinum/firm/`) vs per-advisor (`platinum/advisors/{id}/`). Path convention: firm-level artifacts under `platinum/firm/` per existing precedent.

    **Surface #4 routing flexibility:** RD-B picks FE-iteration OR this artifact. Both work. This TO ships regardless — gives the org a clean reverse-lookup primitive for future use.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~A <0.4.0_DS_ClientPlatform~A@opal.agent>"` per agent commit identity protocol.
  </notes>
</task_order>
