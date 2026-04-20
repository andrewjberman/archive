<task_order>
  <header>
    <id>ADHC_ROUTER.T1</id>
    <project>ADHC_ROUTER</project>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_at>2026-04-15</issued_at>
    <status>complete</status><!-- COO flip 2026-04-16 per ADHC_ROUTER Phase 1 closeout. ~A shipped compiler patches d1d6920b (comp-blast function-level + dotted reverse-edge regression). Patch landed + REGISTRY reflects Phase 1 COMPLETE. -->
    <authorizing_directive>Andrew 2026-04-15 — route idle DS lanes to compiler regression testing on the 3 shipped compiler features (0324142a). Each lane is critical of the tools against their own recent work and is authorized to ship direct patches.</authorizing_directive>
  </header>

  <scope>
    Stress-test the function-level `comp-blast` + reverse caller edges feature shipped in `0324142a` against the RF01 session you completed earlier today (`advi_rollup_rf01_d04_window_nna_delta_fix.md`). Your retroactive triad run flagged three specific tool limitations in the "Compiler Graph Gaps Flagged" subsection. Feature 1 of 0324142a was built to close two of those. Validate that the claim holds end-to-end, not just in the engineer's smoke commands.

    Scope also covers the dotted-path `comp-platinum reverse` feature (shipped in the same commit) as it applies to the two `rfs.decomposition_*.nna` paths you audited.

    You are authorized to ship direct compiler patches under `org/modules/graph/` if you find defects. Commit any patches under your own agent author line; do NOT open a new TO for small fixes — just ship. If the defect requires a structural rewrite (>100 lines or cross-module), stop and message CTO with a proposal.
  </scope>

  <acceptance_criteria>
    1. Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-15/adhc_router_t1_comp_blast_audit.md` with standard sections.
    2. Compiler Tools section reproduces every `<run>` from this TO's mandate with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK per Rule 7.
    3. Explicit "Would this have helped RF01?" assessment paragraph for each of the 3 tested features (function blast + reverse caller edges + dotted platinum reverse). Be specific — reference the original gap entries from your earlier log.
    4. Any defects found: either patched inline (commit hash cited) or documented as a follow-up with proposed fix lift estimate.
    5. Critical lens required. "Passes the smoke commands the engineer wrote" is not the bar. The bar is "would have actually closed the gap the agent hit."
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-blast _compute_window_decomposition</run>
        <expect>Non-empty blast radius rooted at `gold:D_04.client_portal_summary:_compute_window_decomposition`. Caller-chain should surface `_window_nna_delta` (internal caller) and the script-level `D_04` node.</expect>
        <if_mismatch>Record exact output. If empty or terminates early, the feature is broken for the primary use case it was shipped for. Ship a patch if you can diagnose; otherwise log a concrete defect row.</if_mismatch>
      </step>
      <step>
        <run>comp-blast _compute_window_flows</run>
        <expect>Same shape as above; caller chain should reach D_04 top-level plus its called-by helpers.</expect>
        <if_mismatch>Same handling as above.</if_mismatch>
      </step>
      <step>
        <run>comp-blast _window_nna_delta</run>
        <expect>Reverse-caller edges should surface `_compute_window_decomposition` and `_compute_window_flows` as callers since the RF01 fix explicitly calls this helper from both of them.</expect>
        <if_mismatch>This is the canonical reverse-caller validation case. If it fails, reverse-caller edges are broken. Diagnose in `org/modules/graph/trace_graph.py` or `extract_s3.py` and patch.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse rfs.decomposition_max.nna</run>
        <expect>PRODUCER resolves to `D_04::_compute_window_decomposition` or the owning function; CONSUMED BY resolves to at least one portal component (DistributionTab per engineer smoke-test claim).</expect>
        <if_mismatch>If producer/consumer still empty: the dotted-path reverse feature isn't actually reaching the portal component via the platinum artifact chain. Diagnose `platinum_cli.py` reverse lookup + `extract_transforms` field usage walk.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse rfs.decomposition_ytd.nna</run>
        <expect>Symmetric to above.</expect>
        <if_mismatch>Same class of defect as above.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="during analysis">
      <step>
        <run>Compare the newly-working commands above against your original RF01 session log's "Compiler Graph Gaps Flagged" subsection.</run>
        <expect>Each of the three original gap flags (function-level blast, nested-key reverse, aws PATH subprocess) should either be CLOSED (tested green above) or still OPEN with a clear reason.</expect>
        <if_mismatch>If an originally-flagged gap is still open despite the engineer's claim, write a sharp critical finding. That is the signal Andrew wants.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit (if you ship a patch)">
      <step>
        <run>Re-run the 5 Phase 1 commands against the patched graph.</run>
        <expect>Any command that now passes after the patch should be cited in the session log with before/after evidence.</expect>
        <if_mismatch>Do not mark the patch complete until the originally-failing command passes.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <permitted_edits>
    - `org/modules/graph/trace_graph.py`
    - `org/modules/graph/extract_s3.py`
    - `org/modules/graph/platinum_cli.py`
    - `org/modules/graph/extract_transforms.py`
    - Any other `org/modules/graph/*.py` module if the defect localizes there.
    - New test file under `org/modules/graph/tests/` if appropriate.
  </permitted_edits>

  <out_of_scope>
    - Do NOT touch A→D rerun-sensitive gold scripts during this TO. Pure compiler-tooling work only.
    - Do NOT extend the shipped features' scope — that is what the proposal docs (A/B/C/D/E/N1 in `docs/architecture/COMPILER_*.md`) are for.
    - Do NOT re-audit RF01 itself. That TO is already complete.
  </out_of_scope>

  <deliverables>
    1. Session log with Compiler Tools audit section (Rule 7 format).
    2. Zero-to-N compiler patches, each cited with commit hash.
    3. List of residual defects flagged for the compiler engineer (if any).
  </deliverables>
</task_order>
