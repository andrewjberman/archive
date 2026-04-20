<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform~C-2026-04-15-comp-learns-006-iter-prompt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- commit d8ab1372 2026-04-16 -->
    <evidence>
      Shipped: commit d8ab1372 — comp/prompts/iter.md per-iteration agent prompt.
      Artifacts: comp/prompts/iter.md.
      Validation: comp/bin/comp-learns-run.sh (engine at commit 2cb83eb6) invokes the per-iter agent via python -m comp.framework.run referencing this prompt.
      Session log: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-16/.
    </evidence>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — engine runs but agent needs the prompt</priority>
  </metadata>

  <references>
    <ref type="cto_directive">CTO msg 19:55Z punchlist #006 — "Sibling to autoresearch's program.md but per-iteration scope"</ref>
    <ref type="source">/tmp/autoresearch_inspect/autoresearch-master/program.md (reference pattern: prose-procedural per-iter instructions)</ref>
    <ref type="engine">comp/bin/comp-learns-run.sh (commit 2cb83eb6) — invokes the per-iter agent via python -m comp.framework.run</ref>
    <ref type="framework">comp/framework/run.py (~C e657c232) — per-iter Python entry; agent prompt is what it TELLS the agent to do</ref>
  </references>

  <objective>
    Author `comp/prompts/iter.md` — the per-iteration agent prompt. Sparse, procedural, LLM-readable.
    Covers one iteration's mechanics only (NOT the loop-forever meta — that's the bash driver's job).

    Per-iter agent reads: branch state + results.tsv (authoritative history) + current iteration
    inputs. Picks one failing query from the harness. Proposes one edit to `compiler.py`. Commits.
    Re-runs harness. Logs result row to tsv. Returns.

    Does NOT tell agent to "loop forever" or "never stop" — the driver owns termination. Does NOT
    schedule next iteration — that's the driver. Agent's job is one iteration's transformation:
    current-state + one-target-failing-query → proposed-edit → committed-code → measured-result.
  </objective>

  <scope>
    <files>
      <file action="create">comp/prompts/iter.md</file>
      <file action="create">comp/prompts/README.md (brief index of prompt files + their invocation paths)</file>
    </files>
  </scope>

  <wire_contract>
    `iter.md` is LLM-readable Markdown. Driver invokes headless Claude (or equivalent) with this
    file as the prompt + environment variables: `COMP_LEARNS_TARGET`, `COMP_LEARNS_ITER`,
    `COMP_LEARNS_WORKTREE` (for branch context). Agent works within the worktree's checkout.

    Required sections in iter.md:
    1. Context — target + iter + branch (from env vars)
    2. Read the state — `git log --oneline -5` on the branch + `tail -20 results.tsv`
    3. Pick one failing query — read harness output from last iter's `logs/iter_{N-1}.log` if present
    4. Propose one edit — scope: `compiler.py` in the target dir only
    5. Commit the edit — use DS ~C's author line convention
    6. Re-run harness — invoke `python -m comp.framework.run {target} --iter {N}` which handles
       compiler subprocess + tsv append + state.json cache
    7. Return — do NOT ask the human for direction; do NOT loop

    Honest about what the agent is NOT authorized to do: modify framework files, modify harness.py,
    modify queries.yaml, modify `_repo/` (target source under vendored clone).
  </wire_contract>

  <acceptance_criteria>
    1. `comp/prompts/iter.md` exists; ≤120 lines; procedural, no prose bloat; LLM-readable.
    2. 7 sections per wire contract; each has a concrete action + explicit scope.
    3. Authority boundaries explicit — what agent CAN and CANNOT touch.
    4. `comp/prompts/README.md` indexes this + any future prompts; mentions the driver invocation contract.
    5. Dry-run: point a headless Claude at iter.md + `_stub` target; observe agent follows the 7 steps without looping/escalating.
    6. Session log Compiler Tools section reproduces each step (CTO Rule 7).
    7. MCP COMPLETE to COO with commit hash + dry-run trace.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat /tmp/autoresearch_inspect/autoresearch-master/program.md | head -60</run>
        <expect>Karpathy's pattern: procedural, sparse, "do X, then Y" — our iter.md is the per-iter analog of his loop-forever instructions.</expect>
        <if_mismatch>Re-read before authoring.</if_mismatch>
      </step>
      <step>
        <run>cat comp/bin/comp-learns-run.sh | grep -n "python -m comp.framework.run"</run>
        <expect>Confirm driver invokes `python -m comp.framework.run $TARGET --iter $ITER`. iter.md step 6 must match this exactly.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>wc -l comp/prompts/iter.md</run>
        <expect>≤120 lines.</expect>
        <if_mismatch>Tighten.</if_mismatch>
      </step>
      <step>
        <run>Dry-run headless-agent against iter.md + _stub target (either simulated or actual headless Claude invocation)</run>
        <expect>Agent reads state, picks query, edits compiler.py, commits, invokes run.py, returns.</expect>
        <if_mismatch>Iterate prompt until agent follows.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp/prompts/README.md lists iter.md + invocation contract</run>
        <expect>Present.</expect>
        <if_mismatch>Add.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~C" task="COMP_LEARNS.004" status="complete" description="run.py invocation contract locked (e657c232)"/>
    <dependency agent="2.0.0_SA_COO" task="Track B engine worktree migration" status="complete" description="worktree-based invocation env (23de5edf + 2cb83eb6)"/>
  </dependencies>

  <next>On commit: engine is fully armed to run against a real target — iter.md wired to driver + run.py + harness + compiler baseline. First real iteration on httpx can fire once PRD #2 (CTO) + PRD #3 (~B) ship.</next>
</task_order>
