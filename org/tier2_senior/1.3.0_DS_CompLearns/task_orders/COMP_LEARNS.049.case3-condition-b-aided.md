<task_order>
  <metadata>
    <id>1.3.0_DS_CompLearns-2026-04-22-comp-learns-049-case3-condition-b-aided</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- commit 6ac6352f, pushed CLOUD 2026-04-22 --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3 Lane B first formal aided run (condition_b); establishes aided baseline before .050 unaided dispatches (non-contamination rule §4)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §3 (Case 3 lane) + §3.3 (aided = condition_b) + §3.5 (nav_log.jsonl format) + §4 (non-contamination) + §8 — commit 30971db1 (patched per Option B ruling)</ref>
    <ref type="packet">comp/tasks/case-003-sphinx-autodoc-typehints/packet.yaml — fa1d5eb8, condition_b = aided_full</ref>
    <ref type="backlog">comp/backlog/benchmark/bl-sweb-002.yaml — Case 3 entry, baseline 36367765</ref>
    <ref type="harness">comp/targets/sphinx/ — cc13a7a4, required for aided run</ref>
    <ref type="runner">comp/bin/comp-wave-runner.py (5a44ac87) — Stage 2 eval mode, will dispatch you via wave config in a later pass; FIRST run is COO-manual-inspected per AUTOMATION_V1 §6 (new task family)</ref>
  </references>

  <objective>
    Execute Case 3 aided (condition_b) run on sphinx-doc__sphinx-10449 as Wave 3 Lane B's
    aided baseline. Produce full eval-mode bundle + nav_log.jsonl. Your run establishes
    the aided baseline; .050 unaided runs AFTER your ship for non-contamination.

    Note: this is the FIRST Case 3 event (new task family per AUTOMATION_V1 §6). COO
    will manually inspect your bundle before SC dispatch. After first clean pass,
    Wave 3b reruns proceed under standard Stage 2 automation.

    Explicitly in scope:

    1. Set up aided working environment per packet.yaml condition_b.artifacts_allowed:
       - Full repo source tree at baseline 36367765fe780f962bba861bf368a765380bbc68
       - Full comp/ apparatus: compiler.py, scorecards, graph outputs, selector, ab_cache,
         champion_json, all comp-* tools
       - comp/targets/sphinx/ harness (from .046)

    2. Read packet.yaml acceptance_criteria. The decisive FAIL_TO_PASS test is:
       `tests/test_ext_autodoc_configs.py::test_autodoc_typehints_description_with_documented_init`
       (plus regression guards ac-2 + ac-3).

    3. Use the compiler apparatus to navigate sphinx structurally. Expected cross-module
       traversal path (PRD §3.2): autoclass documenter (sphinx/ext/autodoc/__init__.py)
       → typehints processor (sphinx/ext/autodoc/typehints.py) via event registration.

    4. Produce nav_log.jsonl per §3.5 — REQUIRED bundle artifact. Every session action
       logged:
       - `file_open` events in chronological order, with `compiler_assisted` flag
       - `comp_call` events for every comp/ tool invocation with tool + args
       - `hypothesis` events; AT LEAST the first hypothesis where you believe the root
         cause is identified, with `correct: true|false` flag (post-hoc assignment OK
         but must be settled before bundle commit)
       - `token_count` events with cumulative count at hypothesis time (and periodically
         if useful)

       MANDATORY events:
       - All file_open events (no gaps)
       - All comp_call events
       - First correct hypothesis
       - Cumulative token_count at first correct hypothesis

       Example format per §3.5:
       ```jsonl
       {"ts": "2026-04-22T...", "event": "file_open", "path": "sphinx/ext/autodoc/__init__.py", "compiler_assisted": false}
       {"ts": "...", "event": "comp_call", "tool": "comp-trace", "args": "record_typehints_desc --direction both"}
       {"ts": "...", "event": "file_open", "path": "sphinx/ext/autodoc/typehints.py", "compiler_assisted": true}
       {"ts": "...", "event": "hypothesis", "text": "root cause is in typehints.py class vs method discrimination", "correct": true}
       {"ts": "...", "event": "token_count", "cumulative": 14200}
       ```

       Noise detection (§3.5): if your nav_log has ZERO `comp_call` events, the aided run
       is invalid — COO will flag for re-run. You MUST use comp/ tools; that's the point
       of the aided condition.

    5. Implement the fix + make the FAIL_TO_PASS test pass. Regression guards must not
       break. Fix is yours to author (this is a DS task, not a patch-copy exercise).

    6. Produce standard eval-mode bundle at
       `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/`:
       - `changes.patch` (git diff of your fix against baseline)
       - `test_output.txt` (pytest output showing FAIL_TO_PASS test passing + regression guards clean)
       - `reasoning.md` (your post-fix reasoning; excluded from Phase 1 verdict scoring per eval-mode doctrine, included in SC records)
       - `nav_log.jsonl` (per §3.5 — NOT subject to reasoning.md exclusion; Phase 2 metric audit input)

    7. MCP COMPLETE to 2.1.0_SA_COO with commit SHA + bundle path + nav_log summary
       (first-correct-hypothesis time + token count + comp_call count). COO does manual
       inspection per §7 (first-event-new-task-family rule) before SC dispatch.

    Explicitly out of scope:
    - Unaided condition (that is .050, 1.4.0_DS).
    - SC scoring (.051, 2.1.0_SC_CompLearns — two-phase Phase 1 + Phase 2).
    - Modifying packet.yaml (fa1d5eb8 is authoritative).
    - Coordinating compiler changes with dev-4 loop (.048, 1.1.0_DS) — §4 non-contamination
      rule; the compiler apparatus you use is the CURRENT champion at dispatch time, not
      any mid-flight dev-4 improvement.
    - Cross-model variation — Wave 3 uses pinned judge_model_id; cross-model deferred to
      Wave 4.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before run">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Baseline clean (9 pre-existing reds accepted).</expect>
        <if_mismatch>Rebase / fix before starting.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/sphinx/ && cat comp/targets/sphinx/repo_pin.txt</run>
        <expect>Sphinx harness present; repo_pin = 36367765fe780f962bba861bf368a765380bbc68.</expect>
        <if_mismatch>STOP. MCP COO — sphinx harness missing or pin mismatched.</if_mismatch>
      </step>
      <step>
        <run>cat comp/tasks/case-003-sphinx-autodoc-typehints/packet.yaml | grep -E "(condition_b|baseline_commit|swe_bench_id)"</run>
        <expect>condition_b.label: aided_full; baseline_commit: 36367765; swe_bench_id: sphinx-doc__sphinx-10449.</expect>
        <if_mismatch>STOP. Packet mismatch with PRD.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile {any python files in bundle if patch touches them}</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>ls comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/</run>
        <expect>changes.patch + test_output.txt + reasoning.md + nav_log.jsonl all present.</expect>
        <if_mismatch>Add missing artifacts before commit. nav_log.jsonl is the NEW required artifact — don't ship without it.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; [json.loads(l) for l in open('comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/nav_log.jsonl')]; print('nav_log valid jsonl')"</run>
        <expect>Prints "nav_log valid jsonl" — all lines parseable.</expect>
        <if_mismatch>Fix malformed jsonl.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows = [json.loads(l) for l in open('comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/nav_log.jsonl')]; assert any(r['event']=='comp_call' for r in rows), 'MUST have comp_call events in aided mode'; assert any(r['event']=='hypothesis' and r.get('correct')==True for r in rows), 'MUST have first correct hypothesis'; print('nav_log semantics ok')"</run>
        <expect>Prints "nav_log semantics ok".</expect>
        <if_mismatch>nav_log is incomplete. Add missing events. Aided run with no comp_call is invalid per §3.5 noise detection.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/*.patch</run>
        <expect>Exit 0 (patch is stdlib-parseable).</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Clean rebuild.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.050 (1.4.0_DS condition_a unaided) GATES ON your ship for non-contamination (§4). Do not discuss your fix approach, reasoning, or nav_log with 1.4.0_DS during their run. After .050 ships, .051 SC scores both together. Your nav_log is the AIDED side of the efficiency delta.</note>
    <shared_artifacts>comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/** (created by this TO)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Aided environment assembled per packet.yaml condition_b: repo + full comp/ apparatus + sphinx harness.
    2. Fix authored and committed; FAIL_TO_PASS test passes (tests/test_ext_autodoc_configs.py::test_autodoc_typehints_description_with_documented_init).
    3. Regression guards pass: ac-2 + ac-3 per packet.
    4. Bundle complete: changes.patch + test_output.txt + reasoning.md + nav_log.jsonl.
    5. nav_log.jsonl: valid JSONL; contains file_open + comp_call + first correct hypothesis + token_count events per §3.5; at least one comp_call event (aided run hygiene).
    6. Commit --only --author=1.3.0_DS_CompLearns@opal.agent pathspec scoped to comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/**.
    7. Pushed to CLOUD.
    8. Session log with Compiler Tools section + run timing + tools used + hypothesis evolution.
    9. MCP COMPLETE to 2.1.0_SA_COO with: commit sha, bundle path, first-correct-hypothesis time + token count, total comp_call count, wall-clock duration.
  </acceptance_criteria>

  <dependencies>
    - Gate: Wave 3 PRD 30971db1 (patched, locked).
    - Parallel: .048 dev-4 (1.1.0_DS) — non-contamination: do NOT coordinate compiler changes mid-flight.
    - Blocks: .050 (non-contamination — .050 gates on your ship).
    - Blocks: .051 (SC scoring gates on your bundle + .050 bundle).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - FIRST Case 3 event = new task family. I will manually inspect your bundle before SC dispatch (AUTOMATION_V1 §6). Expect a brief back-and-forth on bundle shape before SC hands off.
    - nav_log.jsonl is NEW for Wave 3 (no prior DS has written one). Reference §3.5 format spec; if uncertain, MCP COO before committing.
    - Use compiler tools honestly — the aided advantage is genuine graph traversal, not cherry-picked tool calls. Noise-detection gate will catch zero-comp_call runs.
    - reasoning.md content: describe your path, which compiler calls helped, what hypotheses you rejected. This is excluded from Phase 1 verdict but SC uses it in Phase 2 + integrity audit post-verdict.
    - Session run is a single fresh DS session (this session). No session state carries in from prior work. Start timer at first file_open.
    - No emojis.
  </operational_notes>

  <closeout>
    On completion:
    - commit --only --author="1.3.0_DS_CompLearns &lt;1.3.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/**
    - push to CLOUD
    - flip TO status to complete with commit ref
    - MCP COMPLETE to 2.1.0_SA_COO — your ship triggers: (1) my manual inspection of first-task-family bundle; (2) .050 GO to 1.4.0_DS (unaided can now run)
    - session log with Compiler Tools section
  </closeout>
</task_order>
