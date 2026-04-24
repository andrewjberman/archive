<task_order>
  <metadata>
    <id>1.4.0_DS_CompLearns-2026-04-22-comp-learns-050-case3-condition-a-unaided</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- bundle ds-1.4.0-condition_a shipped 2026-04-24; commit TBD --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3 Lane B unaided condition; pair with .049 for first formal aided-vs-unaided delta</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §3 (Case 3 lane) + §3.3 (unaided = condition_a) + §3.5 (nav_log.jsonl) + §4 (non-contamination) + §8 — commit 30971db1</ref>
    <ref type="packet">comp/tasks/case-003-sphinx-autodoc-typehints/packet.yaml — fa1d5eb8, condition_a = unaided</ref>
    <ref type="backlog">comp/backlog/benchmark/bl-sweb-002.yaml — Case 3 entry, baseline 36367765</ref>
    <ref type="pair_to">.049 (1.3.0_DS condition_b aided) — your run is the unaided counterpart</ref>
  </references>

  <objective>
    Execute Case 3 unaided (condition_a) run on sphinx-doc__sphinx-10449. Use standard
    code-reading only (no compiler apparatus). Produce full eval-mode bundle +
    nav_log.jsonl. Your run is the unaided baseline that pairs with .049 for the
    aided-vs-unaided delta in .051 scoring.

    Explicitly in scope:

    1. Set up UNAIDED working environment per packet.yaml condition_a.artifacts_allowed:
       - Repo source tree at baseline 36367765fe780f962bba861bf368a765380bbc68
       - Standard tools: file system navigation, grep, git log, test runner
       - **FORBIDDEN:** comp_targets_dir, compiler.py, scorecards, ab_cache, champion_json,
         selector_outputs, any comp-* tool

       Enforcement: no `comp_call` events in your nav_log. If you accidentally invoke a
       compiler tool, the run is tainted — MCP COO + restart fresh session.

    2. Read packet.yaml acceptance_criteria. Decisive FAIL_TO_PASS test:
       `tests/test_ext_autodoc_configs.py::test_autodoc_typehints_description_with_documented_init`

    3. Navigate sphinx using ONLY code-reading. Expected path (PRD §3.2):
       - Symptom surfaces in autoclass (sphinx/ext/autodoc/__init__.py)
       - Root cause is in typehints processor (sphinx/ext/autodoc/typehints.py)
       - Cross-module navigation through event-registration system required
       - Unaided expected to explore the autoclass documenter extensively before
         locating typehints processor — this is the measurement axis

    4. Produce nav_log.jsonl per §3.5 — REQUIRED bundle artifact.
       - All file_open events in chronological order; `compiler_assisted: false` for ALL
         entries (unaided)
       - NO comp_call events (you have no compiler)
       - `hypothesis` events; first correct hypothesis with `correct: true` flag
       - `token_count` events with cumulative at first correct hypothesis

       Example:
       ```jsonl
       {"ts": "...", "event": "file_open", "path": "sphinx/ext/autodoc/__init__.py", "compiler_assisted": false}
       {"ts": "...", "event": "file_open", "path": "sphinx/ext/autodoc/directive.py", "compiler_assisted": false}
       {"ts": "...", "event": "file_open", "path": "sphinx/ext/autodoc/typehints.py", "compiler_assisted": false}
       {"ts": "...", "event": "hypothesis", "text": "...", "correct": true}
       {"ts": "...", "event": "token_count", "cumulative": ...}
       ```

       Hygiene: if you realize mid-run you need to look at non-decisive files that .049
       did NOT need (e.g. event manager internals, other extension handlers), LOG them.
       That's the whole point — the nav_log captures exploratory waste in unaided vs aided.

    5. Implement the fix + make FAIL_TO_PASS test pass + regression guards clean.

    6. Produce standard eval-mode bundle at
       `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/`:
       - `changes.patch`
       - `test_output.txt`
       - `reasoning.md`
       - `nav_log.jsonl`

    7. MCP COMPLETE to 2.1.0_SA_COO. Bundle + your nav_log + .049's nav_log become .051's
       input for aided-vs-unaided efficiency delta computation.

    Explicitly out of scope:
    - Aided condition (.049, 1.3.0_DS).
    - SC scoring (.051, 2.1.0_SC — two-phase).
    - Modifying packet.yaml.
    - Coordination with 1.3.0_DS or 1.1.0_DS (non-contamination §4; do NOT read their
      nav_log or reasoning.md before your run completes).
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before run">
      <step>
        <run>ls comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ | grep condition_b</run>
        <expect>ds-1.3.0-condition_b directory exists (.049 shipped — your gate is clear).</expect>
        <if_mismatch>STOP. .049 not yet shipped; this TO cannot start.</if_mismatch>
      </step>
      <step>
        <run>cat comp/tasks/case-003-sphinx-autodoc-typehints/packet.yaml | grep -E "(condition_a|baseline_commit)"</run>
        <expect>condition_a.label: unaided; baseline_commit: 36367765.</expect>
        <if_mismatch>STOP. Packet mismatch.</if_mismatch>
      </step>
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Clean baseline (9 pre-existing reds accepted). NOTE: you run `comp-build` only to verify harness state pre-session; you do NOT use comp/ tools during the unaided run.</expect>
        <if_mismatch>Rebase or fix.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>ls comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/</run>
        <expect>changes.patch + test_output.txt + reasoning.md + nav_log.jsonl all present.</expect>
        <if_mismatch>Add missing artifacts before commit.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows = [json.loads(l) for l in open('comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/nav_log.jsonl')]; assert not any(r['event']=='comp_call' for r in rows), 'UNAIDED must have ZERO comp_call events'; assert any(r['event']=='hypothesis' and r.get('correct')==True for r in rows), 'first correct hypothesis required'; print('nav_log semantics ok (unaided)')"</run>
        <expect>Prints "nav_log semantics ok (unaided)".</expect>
        <if_mismatch>comp_call in unaided nav_log = TAINTED run. Discard, re-start fresh session, document incident. Zero comp_calls is the invariant for condition_a.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; [json.loads(l) for l in open('comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/nav_log.jsonl')]; print('valid jsonl')"</run>
        <expect>Prints "valid jsonl".</expect>
        <if_mismatch>Fix malformed jsonl.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/*.patch</run>
        <expect>Exit 0.</expect>
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
    <note>PAIR with .049 (1.3.0_DS condition_b aided). Non-contamination per §4: you must NOT have read .049's nav_log, reasoning.md, or fix patch before your run. .051 (2.1.0_SC) pairs both bundles for aided-vs-unaided delta. If .051 flags your run as "DS had prior exposure to sphinx" (confounded per §3.6), surface to COO — re-run required.</note>
    <shared_artifacts>comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/** (created by this TO); .049's bundle (read-only AFTER your ship; do not pre-read)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Unaided environment enforced: no comp/ artifacts used during session.
    2. Fix authored; FAIL_TO_PASS test passes; regression guards clean.
    3. Bundle complete: changes.patch + test_output.txt + reasoning.md + nav_log.jsonl.
    4. nav_log.jsonl: zero comp_call events (unaided invariant); file_open + hypothesis + token_count events per §3.5; first correct hypothesis marked.
    5. Commit --only --author=1.4.0_DS_CompLearns pathspec scoped to bundles/ds-1.4.0-condition_a/**.
    6. Pushed to CLOUD.
    7. Session log with Compiler Tools section + run timing + exploratory path (files visited in order).
    8. MCP COMPLETE to 2.1.0_SA_COO with: commit sha, bundle path, first-correct-hypothesis time + token count, total file_open count, wall-clock duration.
  </acceptance_criteria>

  <dependencies>
    - Gate: .049 (1.3.0_DS condition_b aided) SHIPPED. Do NOT begin until .049 COMPLETE MCP received + you see a GO from COO.
    - Parallel (non-coordinating): .048 dev-4 (1.1.0_DS).
    - Blocks: .051 SC scoring (gates on .049 + .050 both bundled).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Fresh DS session: do NOT carry state from prior COMP_LEARNS work. Non-contamination is
      the measurement invariant.
    - Zero-comp_call is NON-NEGOTIABLE for the unaided nav_log. If you find yourself
      reflexively reaching for a comp tool, you are tainting the run. STOP, discard the
      bundle, restart.
    - nav_log.jsonl is the Phase 2 metric input. Log generously — files you opened AND
      dismissed matter for the exploratory waste metric.
    - reasoning.md: describe your unaided path honestly. Excluded from Phase 1 verdict but
      SC uses in Phase 2 + integrity audit.
    - No emojis.
  </operational_notes>

  <closeout>
    On completion:
    - commit --only --author="1.4.0_DS_CompLearns &lt;1.4.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/**
    - push to CLOUD
    - flip TO status to complete with commit ref
    - MCP COMPLETE to 2.1.0_SA_COO — your ship + .049 ship trigger .051 SC dispatch
    - session log with Compiler Tools section
  </closeout>
</task_order>
