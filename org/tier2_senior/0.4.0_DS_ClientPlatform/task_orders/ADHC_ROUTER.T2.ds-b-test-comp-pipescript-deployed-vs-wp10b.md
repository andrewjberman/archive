<task_order>
  <header>
    <id>ADHC_ROUTER.T2</id>
    <project>ADHC_ROUTER</project>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_at>2026-04-15</issued_at>
    <status>pending</status>
    <authorizing_directive>Andrew 2026-04-15 — corpus-driven compiler regression testing. Per-lane critical audit of the shipped compiler improvements against each agent's own recent work.</authorizing_directive>
  </header>

  <scope>
    Stress-test `comp-pipescript deployed` env-forwarding + explicit TIMEOUT behavior (shipped in `0324142a`) against your WP-10b gold-silver recon harness work. You had multiple comp-pipescript runs across that session; many succeeded after workarounds. Validate that the new env-forwarding actually fixes the AWS-subprocess-PATH bug end-to-end and that the TIMEOUT behavior is informative rather than confusing.

    Secondary scope: exercise `comp-pipescript deployed` across silver scripts (`bd_price_update.py`, `inject_scoped_overrides.py`) — the silver-scope extension shipped with AE CloudOps TO and is known to work, but validate it under the new env-forwarding conditions.

    You are authorized to ship direct compiler patches under `org/modules/graph/` if you find defects. Commit under your own agent author line; ship fixes inline, only message CTO for structural rewrites (>100 lines or cross-module).
  </scope>

  <acceptance_criteria>
    1. Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-15/adhc_router_t2_comp_pipescript_deployed_audit.md`.
    2. Compiler Tools section reproduces every `<run>` with observed output, AWS-environment state at time of run (credentials loaded? IMDS disabled?), pass/fail vs. `<expect>`. Rule 7 format.
    3. Explicit "Would this have helped WP-10b?" paragraph referencing specific points in your WP-10b session log where comp-pipescript runs succeeded only via workaround.
    4. If TIMEOUT behavior surfaces during testing: quote exactly what the tool printed. Is it actionable for an agent who doesn't know about the Windows WMI / IMDS fixes? If not, that's itself a defect worth patching.
    5. Critical lens required. "Doesn't crash" is not the bar. The bar is "an agent who had NEVER seen this tool before could diagnose a real deployed-parity failure from its output alone."
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>Clean MATCH/STALE/MISSING reporting, no "aws CLI not found" error. Should complete within 30 sec or emit explicit TIMEOUT with guidance.</expect>
        <if_mismatch>Record exact error. If still hanging or failing with PATH issues, env-forwarding is broken for the CI path. Diagnose in `pipeline_cli.py::cmd_deployed` subprocess dispatch and patch.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed bd_price_update.py</run>
        <expect>`[SILVER] bd_price_update.py: MATCH` or equivalent silver-layer parity output. If AWS is reachable, a real hash comparison; if not, a clear TIMEOUT message.</expect>
        <if_mismatch>Silver scope was supposed to land end-to-end. If it doesn't work under env-forwarding, there's a regression in the 0324142a integration.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed inject_scoped_overrides.py</run>
        <expect>Same shape as above.</expect>
        <if_mismatch>Same.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed (full sweep, no args)</run>
        <expect>All gold + silver scripts reported. Any STALE entries flagged. Any TIMEOUT entries include the runtime guidance the 0324142a changelog claimed.</expect>
        <if_mismatch>If the output is misleading (e.g. "No scripts matched filter" despite some scripts being deployed), that's the exact misleading-summary defect 0324142a was supposed to close.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="during analysis">
      <step>
        <run>Re-read your WP-10b session log. Find every `comp-pipescript` / AWS-adjacent run that succeeded via workaround (manual `aws s3api head-object`, manual `md5sum`, etc.).</run>
        <expect>For each workaround point, assess: under today's shipped env-forwarding, would that workaround still have been needed?</expect>
        <if_mismatch>If any workaround is still required with the new code, that's a real unclosed gap. Write it up explicitly.</if_mismatch>
      </step>
      <step>
        <run>Deliberately break your local AWS env (unset AWS_PROFILE or similar) and re-run `comp-pipescript deployed D_04`.</run>
        <expect>Tool emits explicit TIMEOUT with "AWS credentials not reachable" guidance rather than silently succeeding with empty output.</expect>
        <if_mismatch>If the tool fails silently or reports MATCH on an unreachable S3, that's a serious correctness defect — the tool is claiming parity it can't actually verify.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit (if you ship a patch)">
      <step>
        <run>Re-run all Phase 1 + Phase 2 runs against patched code.</run>
        <expect>Before/after evidence in the session log.</expect>
        <if_mismatch>Do not mark patch complete until the originally-failing run is clean.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <permitted_edits>
    - `org/modules/graph/pipeline_cli.py`
    - `org/modules/graph/extract_pipeline.py`
    - Any other `org/modules/graph/*.py` needed to fix a defect found.
    - Test files.
  </permitted_edits>

  <out_of_scope>
    - Do NOT touch gold/silver scripts during this TO (A→D rerun sensitivity).
    - Do NOT extend silver scope into `comp-pipescript io/feeds/consumers` — that is `COMPILER_SILVER_SCOPE_FULL.md` proposal scope.
    - Do NOT re-audit WP-10b itself.
  </out_of_scope>

  <deliverables>
    1. Session log with full Rule 7 audit.
    2. Zero-to-N patches with commit hashes.
    3. Critical-lens findings on TIMEOUT message quality.
  </deliverables>
</task_order>
