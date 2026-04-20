<task_order>
  <metadata>
    <id>any-lane-2026-04-16-comp-learns-019-visualization-cli</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>any DS lane (first idle ~A / ~B / ~C / ~D after .017)</issued_to>
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P3 — optional; can slip to next wave without escalation</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ c963ced5 (v2)</ref>
    <ref type="prd_section">§12.2 TO .019 (optional visualization CLI)</ref>
  </references>

  <objective>
    Pretty-print helpers for scorecards + experiment_log. Optional QoL; no downstream dependency.

    Deliver:
    1. `comp-learns-run httpx --show-scorecard` — pretty-prints the latest scorecard JSON (tables for structural / behavioral / efficiency / per_selector / adversarial).
    2. `comp-learns-run httpx --show-log --last N` — tails the last N experiment_log entries in a human-readable format with verdict color-coding (plain ASCII: `KEEP` / `DISCARD` / `TIE` — NO emojis per CLAUDE.md code quality rules).
    3. `comp-learns-run httpx --show-diff A B` — prints GraphDiff between two scorecards' graphs (nodes added/removed, edges added/removed, kind deltas).

    Explicitly out of scope: interactive TUI, graph visualization (GraphViz, D3), scorecard dashboards, persistence beyond existing JSONL/JSON files.
  </objective>

  <scope>
    <files>
      <file action="create">comp/bin/show_scorecard.py</file>
      <file action="create">comp/bin/show_log.py</file>
      <file action="create">comp/bin/show_diff.py</file>
      <file action="modify">comp/bin/comp-learns-run.sh (wire --show-scorecard / --show-log / --show-diff subcommands)</file>
    </files>
  </scope>

  <wire_contract>
    **Output discipline — ASCII only (CLAUDE.md code quality rule 13).**
    No emoji. Use plain prefixes: `KEEP:`, `DISCARD:`, `TIE:`, `WARN:`, `ERROR:`.

    **--show-scorecard output format:**
    ```
    === Scorecard: httpx @ <sha> <ts> ===
    Primary metric: 0.123
    Structural:    p=0.95 r=0.91 f1=0.93 (1200 records)
    Behavioral:    88% pass (17/22)
    Efficiency:    extract=2.3s graph=45KB mem=82MB
    Downstream AB: best=centrality lift=+0.17 tokens_reduced=22%
      - random:     lift=+0.02  tokens_reduced=0%
      - keyword:    lift=+0.09  tokens_reduced=8%
      - centrality: lift=+0.17  tokens_reduced=22%
    Adversarial:   mutation_stability=0.89 (rename=0.91 reorder=0.88 noise=0.87)
    Conflict fraction: 0.000
    ```

    **--show-log output format:**
    ```
    iter=1 KEEP    primary=+0.08 delta=+0.08 loc=+142  [initial imports baseline]
    iter=2 DISCARD primary=+0.06 delta=-0.02 loc=+28   [regex fallback regressed F1]
    ```
  </wire_contract>

  <acceptance_criteria>
    1. `comp-learns-run httpx --show-scorecard` prints the latest scorecard in the format above.
    2. `comp-learns-run httpx --show-log --last 5` tails the last 5 experiment_log entries.
    3. `comp-learns-run httpx --show-diff &lt;scorecard_A.json&gt; &lt;scorecard_B.json&gt;` prints the GraphDiff summary.
    4. **No emoji characters in output** — `python -c "import sys; out = sys.stdin.read(); assert all(ord(c) &lt; 128 for c in out), 'non-ASCII found'"` passes when piped the output.
    5. Exit 0 on missing scorecard/log — print empty-state message.
    6. Session log `## Compiler Tools` reproduces every `<run>` below with observed output + pass/fail vs. `<expect>`.
    7. MCP COMPLETE to 2.0.0_SA_COO~Z with commit hash + sample outputs from each subcommand.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls comp/targets/httpx/scorecards/*.json comp/targets/httpx/experiment_log.jsonl</run>
        <expect>Both present — .017 landed scorecards + log for this CLI to read.</expect>
        <if_mismatch>STOP. .017 has not shipped; CLI has nothing to pretty-print. Defer this TO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash comp/bin/comp-learns-run.sh httpx --show-scorecard | head -30</run>
        <expect>Prints the formatted scorecard per wire_contract. No non-ASCII characters.</expect>
        <if_mismatch>Fix formatter.</if_mismatch>
      </step>
      <step>
        <run>bash comp/bin/comp-learns-run.sh httpx --show-scorecard | python -c "import sys; out = sys.stdin.read(); assert all(ord(c) &lt; 128 for c in out), f'non-ASCII found at {[i for i,c in enumerate(out) if ord(c)&gt;=128][:5]}'; print('ascii-ok')"</run>
        <expect>Prints `ascii-ok`. No emoji characters in output.</expect>
        <if_mismatch>Remove emoji. Per CLAUDE.md code quality rule 13.</if_mismatch>
      </step>
      <step>
        <run>bash comp/bin/comp-learns-run.sh httpx --show-log --last 2</run>
        <expect>Tails last 2 experiment_log entries in format above.</expect>
        <if_mismatch>Fix tail logic.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>bash comp/bin/comp-learns-run.sh httpx --show-scorecard &amp;&amp; echo "EXIT=$?"</run>
        <expect>Prints scorecard + `EXIT=0`.</expect>
        <if_mismatch>Fix exit code.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty. (Medium/Critical) Not applicable — CLI is read-only formatter. Does not mutate scorecards or gold.</risk>
    <risk id="R3">Subtype explosion. (High/High) Not applicable — CLI renders existing subtype_kinds; does not add new ones.</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **Three flags only. No TUI. No web dashboard. No graph visualization. If you reach for `curses` or `rich` beyond basic tables, STOP.**</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: `comp-learns-run.sh` gains three flags; existing `--once` behavior preserved.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.017" status="required">Scorecard + experiment_log data to format</dependency>
  </dependencies>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <next>Optional. If idle capacity after .017, any DS lane picks this up. If not done by end of wave, slip without escalation per §15.</next>
</task_order>
