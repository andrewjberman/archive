<task_order>
  <header>
    <id>ADHC_ROUTER.T3</id>
    <project>ADHC_ROUTER</project>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_at>2026-04-15</issued_at>
    <status>pending</status>
    <authorizing_directive>Andrew 2026-04-15 — corpus-driven compiler regression testing.</authorizing_directive>
  </header>

  <scope>
    Stress-test dotted-path `comp-platinum reverse` (shipped in `0324142a`) against the RA-P0 role_aua canonical schema work you completed earlier today, plus the B9-DS small_account_count work. Both involved new or modified platinum field paths. Validate that the reverse lookup correctly resolves payload field paths for fields that currently exist in consumer code and correctly returns the new-field PASS for fields that don't exist yet (expected empty for new canonical convergence work).

    Also exercise function-level `comp-blast` against C_08 helpers you touched in B9-DS.

    You are authorized to ship direct compiler patches. Commit under your own author line; CTO escalation only for structural rewrites.
  </scope>

  <acceptance_criteria>
    1. Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-15/adhc_router_t3_comp_platinum_reverse_audit.md`.
    2. Rule 7 format Compiler Tools section.
    3. Explicit "Would this have helped RA-P0?" and "Would this have helped B9-DS?" assessment paragraphs, referencing specific points in your earlier session logs.
    4. Particular attention to the new-platinum-field auto-rule case — RA-P0 used `comp-platinum reverse role_aua` and expected empty (new field, no consumers yet). Validate that case is correctly distinguished from "tool broken" today.
    5. Critical lens: any false-positive (tool claims producer/consumer for a field that actually has none) is more serious than a false-negative, because it misleads agents into thinking the graph is more complete than it is.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-platinum reverse role_aua</run>
        <expect>Empty PRODUCER + CONSUMED BY. This is a NEW canonical field from RA-P0; no shadow write, no portal consumer yet. Tool should correctly report "no matches" without crashing.</expect>
        <if_mismatch>If tool crashes or reports spurious matches, that's a defect. If it reports empty but in a way that's indistinguishable from "tool failed," that's a UX defect worth fixing.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse advisor_fee_efficiency</run>
        <expect>PRODUCER resolves to `gold:C_08.advisor_fee_efficiency` (writes `gold/artifacts/advisor_fee_efficiency.json`); CONSUMED BY resolves to `FeeEfficiencyPanel` via D_04 platinum mirror.</expect>
        <if_mismatch>If producer or consumer is empty, the reverse lookup isn't reaching the existing graph even for known-populated fields. Diagnose `platinum_cli.py` reverse logic + `extract_transforms` / `extract_api` indexing.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse small_account_count</run>
        <expect>PRODUCER resolves to C_08 (your B9-DS edit adds this field); CONSUMED BY resolves to FeeEfficiencyPanel column (DE added in B9-DE commit a2d8f83).</expect>
        <if_mismatch>If either is empty, the tool isn't picking up the just-shipped field. Ask: is the graph stale? Does `comp-build` need to re-run to pick up the new field? If yes, document that as a usability issue.</if_mismatch>
      </step>
      <step>
        <run>comp-blast C_08</run>
        <expect>Script-level blast — this is where the graph is currently weakest (see `COMPILER_BLAST_SCRIPT_ARTIFACT_EDGES.md` proposal). Likely returns "no downstream consumers found" today.</expect>
        <if_mismatch>If the command does return meaningful downstream, that's unexpected good news — the proposal may already be moot. If empty as expected, note that and move to function-level test below.</if_mismatch>
      </step>
      <step>
        <run>comp-blast C_08.build_scorecard</run>
        <expect>Function-level blast works post-0324142a — should return at minimum the advisor_fee_efficiency artifact reachability and any helper call chain.</expect>
        <if_mismatch>If empty, function-level indexing isn't catching C_08's helpers. Diagnose in the AST walk that extracts function nodes.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="during analysis">
      <step>
        <run>Compare your RA-P0 session log (`comp-platinum reverse role_aua` expected PASS because new field) against current tool output.</run>
        <expect>Your prior PASS reasoning was "exactly matches expect — new platinum field, no existing producer or consumer." Today's behavior should preserve that PASS semantic.</expect>
        <if_mismatch>If the new-field empty case is indistinguishable from a broken lookup, write a sharp critical finding. "It says empty" isn't audit signal if the agent can't tell whether the graph is complete-but-empty or just broken.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit (if you ship a patch)">
      <step>
        <run>Re-run all Phase 1 commands.</run>
        <expect>Before/after evidence in the log.</expect>
        <if_mismatch>Do not mark complete until originally-failing runs pass.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <permitted_edits>
    - `org/modules/graph/platinum_cli.py`
    - `org/modules/graph/extract_transforms.py`
    - `org/modules/graph/extract_api.py`
    - `org/modules/graph/trace_graph.py`
    - Test files.
  </permitted_edits>

  <out_of_scope>
    - No gold script edits (A→D rerun sensitivity).
    - No new-feature work — stick to audit + fix of 0324142a scope.
  </out_of_scope>

  <deliverables>
    1. Session log with Rule 7 audit.
    2. Zero-to-N patches with commit hashes.
    3. Specific critical finding on empty-vs-broken disambiguation in reverse lookup output.
  </deliverables>
</task_order>
