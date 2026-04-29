<task_order>
  <metadata>
    <id>ADHC_DSFLOW.004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-24</date>
    <status>complete</status><!-- SHIPPED 2026-04-24: ruff 0.15.11 + FA102 + from __future__ annotations backfill 93 scripts. Commits: 6156d428+a5ac27a2+9bffa7e6. CLAUDE.md Rule 15 + canary gate verified. TO closed 2026-04-29 by ~D per COO status correction (REGISTRY confirmed). -->
    <project_code>ADHC_DSFLOW</project_code>
    <priority>P1 — closes same latent-bug class as original .001 motivators (081223b5 defaultdict + 035352c3 KeyError). AE 0.6.1 caught pre-dispatch PEP-604 today (SCOPEFIX INFLEC 2d3de276) — structural gate prevents recurrence.</priority>
    <origin>
      Andrew 3-decision batch 2026-04-24 (CTO MCP 20260424T16xxxxZ): PEP-604 ds-commit-gate hardening approved. CTO scoped as ADHC_DSFLOW Phase 2 TO 4 rather than new project. Two coordinated changes: (a) ruff target-version=py39 pass in ds-commit-gate, (b) CLAUDE.md Rule 15 mandatory `from __future__ import annotations` line 1 on silver/gold/bronze scripts.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DSFLOW.md §7 TO 4 (commit d8875b42 — Phase 2 scope authoring)</ref>
    <ref type="prd_amendment_commit">d8875b42 — CTO authoring of §7 TO 4 block + ADHC_DSFLOW.json phase update</ref>
    <ref type="predecessor_to">ADHC_DSFLOW.001 ds-precommit-gate-tool (complete `b6e0c154`+`7b7381ac`) — the tool this TO hardens</ref>
    <ref type="predecessor_to">ADHC_DSFLOW.002 org-docs-update (complete `1e9d9dc3`) — Rules 13+14 precedent for Rule 15 addition</ref>
    <ref type="triggering_incident">AE 0.6.1 MCP 20260424T160xxxxZ — W4.13b silver re-ingest crash on inf-gold-runner Py 3.9 from SCOPEFIX commit 2d3de276 (PEP-604 `str | None` at 3 sites). Fix shipped as `6c1362de` (`from __future__ import annotations`). This TO structurally prevents the class.</ref>
    <ref type="similar_class_incidents">081223b5 (NameError: defaultdict, B_00) + 035352c3 (KeyError, D_02) — same gate-passes-at-commit-runtime-fails-on-runner pattern</ref>
    <ref type="out_of_scope">ADHC_PYUPGR (candidate code, not yet registered) — runner Python upgrade 3.9→3.11+. Andrew call if prioritized later.</ref>
  </references>

  <objective>
    Harden `.tools/ds-commit-gate.sh` + `.tools/ds-precommit-check.py` to be runner-version-aware by (a) adding a `ruff check --target-version py39` pass and (b) enforcing mandatory `from __future__ import annotations` line 1 on every `data/*/scripts/{gold,silver,bronze}/*.py`. Backfill-sweep the 71 existing gold scripts + affected silver + bronze; add `CLAUDE.md` Rule 15; canary-reproduce the SCOPEFIX PEP-604 failure to confirm the new gate exits 1.

    **EXPLICIT SCOPE LOCK:**
    - ruff integration: `ruff check --target-version py39` added to ds-commit-gate. Zero pip deps (ruff ships standalone via pip install ruff OR single-binary). Existing py_compile + AST scanner stay unchanged as belt-and-suspenders.
    - `from __future__ import annotations` enforcement: targeted check in ds-precommit-check.py for paths matching `data/*/scripts/{gold,silver,bronze}/*.py`. Clear error message with fix instruction on miss.
    - CLAUDE.md Rule 15 mandate text added (CTO's exact wording per §7 scope).
    - Backfill sweep: all 71 existing gold scripts must pass ruff --target-version py39 clean OR have documented + whitelisted exceptions. Treat as informational sweep, not a retroactive gate against prior commits.
    - Canary test: reproduce SCOPEFIX `2d3de276` pre-fix state locally; new `ds-commit-gate.sh` must exit 1 with PEP-604 finding cited.
    - NO runner Python upgrade (orthogonal; ADHC_PYUPGR candidate if Andrew prioritizes).
    - NO containerizing the gate (overkill per PRD §7 line 328).
    - NO new pip deps beyond ruff itself.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/ds-commit-gate.sh — add `ruff check --target-version py39` step for staged .py files; exit 1 on ruff non-zero; preserve existing py_compile + ds-precommit-check.py passes</file>
      <file action="modify">.tools/ds-precommit-check.py — add targeted check: for paths matching `data/*/scripts/{gold,silver,bronze}/*.py`, require `from __future__ import annotations` at or near line 1 (after optional docstring/shebang). Clear error message on miss with exact fix instruction.</file>
      <file action="modify">CLAUDE.md — add Rule 15 mandate: "Every `data/*/scripts/gold/*.py`, `data/*/scripts/silver/*.py`, and `data/*/scripts/bronze/*.py` MUST begin with `from __future__ import annotations` as its first import statement. Enables PEP-604 union syntax on 3.9+ runners without runtime parse failure."</file>
      <file action="modify_batch">Backfill sweep — all 71 gold scripts + any silver/bronze scripts that lack `from __future__ import annotations` at line 1. Single batch commit per file pattern; document exceptions if any script legitimately cannot adopt (rare).</file>
      <file action="create">tests/ds_commit_gate/test_pep604_canary.sh (or inline in session log) — canary reproduction: copy SCOPEFIX 2d3de276 pre-fix state to /tmp/, run new ds-commit-gate, assert exit 1 with PEP-604 finding in output.</file>
      <file action="read-only">data/orion/scripts/silver/convert_orion_to_silver.py at commit 2d3de276 — canary source state (pre-fix, has `str | None` at L168 + L288-289)</file>
      <file action="read-only">data/black_diamond/scripts/gold/*.py — backfill sweep target set (71 scripts per .001 inventory)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="ruff-integration">
      .tools/ds-commit-gate.sh runs `ruff check --target-version py39` against staged .py files; non-zero exit blocks commit. Installation step documented in .tools/README or inline in gate script header (ruff install via `pip install ruff` or standalone binary).
    </deliverable>
    <deliverable id="future-annotations-check">
      .tools/ds-precommit-check.py flags any `data/*/scripts/{gold,silver,bronze}/*.py` missing `from __future__ import annotations` near line 1 with clear fix-instruction error message. 8+ unit tests added covering: (a) compliant script passes, (b) missing import fails, (c) import-not-at-top fails, (d) non-data path exempt.
    </deliverable>
    <deliverable id="claude-md-rule-15">
      CLAUDE.md Rule 15 added under existing Rules 13-14 block (ADHC_DSFLOW precedent). Exact text matches CTO §7 scope. Applies to all future silver/gold/bronze script commits.
    </deliverable>
    <deliverable id="backfill-sweep">
      All 71 gold scripts + affected silver + bronze scripts updated to include `from __future__ import annotations` at line 1 (single or small-batch commits; author DS). Exception list (if any) documented in session log with reasoning.
    </deliverable>
    <deliverable id="canary-test">
      Canary reproduction: SCOPEFIX 2d3de276 pre-fix state → new `ds-commit-gate.sh` → exits 1 with PEP-604 finding cited in output. Evidence captured in session log (full command + full output).
    </deliverable>
    <deliverable id="session-log-compiler-section">
      Session log Compiler Tools section reproduces every `<run>` from mandate triad + observed + pass/fail vs `<expect>`. Append 5+ rows to `org/compiler-tools-log.md`.
    </deliverable>
    <deliverable id="ravc4-mcp">
      RAVC4 to COO + CTO with commit SHA(s), tool version(s), backfill-sweep results (file count + any exceptions), canary test exit-code evidence, and CLAUDE.md Rule 15 diff citation.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">`ruff check --target-version py39` integrated into `.tools/ds-commit-gate.sh` — commit blocked on non-zero exit. Ruff install path documented.</ac>
    <ac id="2">All 71 existing gold scripts pass `ruff --target-version py39` clean OR have documented + whitelisted exceptions (informational backfill, not retroactive gate).</ac>
    <ac id="3">`CLAUDE.md` Rule 15 added: mandatory `from __future__ import annotations` line 1 on `data/*/scripts/{gold,silver,bronze}/*.py`. Exact text matches CTO §7 scope.</ac>
    <ac id="4">`.tools/ds-precommit-check.py` fails with clear error message on any silver/gold/bronze script missing `from __future__ import annotations` near line 1. 8+ new unit tests covering compliant / missing / mislocated / non-data-path cases.</ac>
    <ac id="5">Canary test: reproduce SCOPEFIX `2d3de276` pre-fix state → run new `ds-commit-gate.sh` → exits 1 with PEP-604 finding cited. Output captured in session log verbatim.</ac>
    <ac id="6">Backfill sweep: all 71 gold scripts + affected silver/bronze scripts have `from __future__ import annotations` at line 1 post-sweep. Exception count + reasoning documented.</ac>
    <ac id="7">py_compile + ds-commit-gate.sh (the new version, self-gated) exit 0 on the backfill sweep commit(s) per CLAUDE.md Rule 14.</ac>
    <ac id="8">`comp-pipescript io` on any gold script touched by the sweep — no COLUMN GAPS introduced by the defensive `__future__` import (defensive check per PRD §7 mandate).</ac>
    <ac id="9">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>`.</ac>
    <ac id="10">RAVC4 MCP to COO + CTO with commit SHAs, tool version, backfill-sweep results, canary exit-code evidence, CLAUDE.md Rule 15 diff.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before commit (backfill sweep + gate upgrade)">
      <step>
        <run>ruff --version</run>
        <expect>Ruff installed; version reported. Document install method (pip vs standalone binary) in session log.</expect>
        <if_mismatch>If ruff not installed, install via `pip install ruff` (preferred: pin to a specific version for reproducibility). Document version pin in gate script header.</if_mismatch>
      </step>
      <step>
        <run>ruff check --target-version py39 data/black_diamond/scripts/gold/</run>
        <expect>Pre-sweep: non-zero (PEP-604 hits in any gold script using `str | None` syntax, or other 3.10+ constructs). Enumerate all hits in session log.</expect>
        <if_mismatch>If exit 0 (all scripts already compatible), backfill sweep scope narrows to just `from __future__ import annotations` additions for the Rule 15 mandate.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_04</run>
        <expect>Baseline READS + WRITES captured pre-sweep for D_04 (exemplar) to detect any accidental COLUMN GAPS introduced by the defensive __future__ import. Do the same for one silver + one bronze script touched.</expect>
        <if_mismatch>If COLUMN GAPS appear post-sweep that weren't there pre-sweep, the __future__ import somehow affects runtime column resolution — investigate (should be impossible since __future__ only affects annotations, but belt-and-suspenders).</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile .tools/ds-commit-gate.sh.new .tools/ds-precommit-check.py.new</run>
        <expect>Exit 0. (Note: gate.sh is bash, use `bash -n` instead; py_compile for the .py only.)</expect>
        <if_mismatch>STOP. Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh (new version, self-applied on the gate tool commits)</run>
        <expect>Exit 0 on the gate tool's own .sh + .py files.</expect>
        <if_mismatch>STOP. Fix the gate before commit — dogfooding check is mandatory.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit (8+ unit tests on ds-precommit-check.py)">
      <step>
        <run>python -m pytest tests/ds_commit_gate/ -v</run>
        <expect>All unit tests pass: (a) compliant script passes, (b) missing __future__ fails, (c) __future__ not at top fails, (d) non-data path exempt, (e) 4+ additional edge cases.</expect>
        <if_mismatch>STOP. Fix gate logic until all tests pass.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit (canary + full-sweep verification)">
      <step>
        <run>bash -c "git show 2d3de276:data/orion/scripts/silver/convert_orion_to_silver.py > /tmp/canary_scopefix_prefix.py && .tools/ds-commit-gate.sh /tmp/canary_scopefix_prefix.py"</run>
        <expect>Exit 1 with ruff output citing PEP-604 `str | None` hits at line 168 + line 288-289. Stdout/stderr captured in session log.</expect>
        <if_mismatch>Canary missed the class — gate logic incomplete. STOP and iterate.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/*.py (full 71-script sweep post-backfill)</run>
        <expect>Exit 0 on all 71 scripts (backfill sweep already brought them compliant). If exceptions exist, they're whitelisted + documented.</expect>
        <if_mismatch>Post-sweep gate still fails: either backfill incomplete or legitimate exception not whitelisted. Iterate.</if_mismatch>
      </step>
      <step>
        <run>git log --oneline --since="backfill-sweep-start" data/black_diamond/scripts/gold/ data/orion/scripts/silver/ data/orion/scripts/bronze/</run>
        <expect>Backfill sweep commits visible under 0.4.0_DS author; scope-limited to `__future__` import additions; no unintended semantic changes in diffs.</expect>
        <if_mismatch>If sweep commits contain more than `__future__` additions, scope crept — surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Per Compiler Mandate Auto-Rule 4. This TO modifies `.tools/*` (gate infrastructure) + `CLAUDE.md` (org docs) + adds `from __future__ import annotations` line 1 to existing silver/gold/bronze scripts (no semantic logic change, no data-flow change). The `__future__` import is a Python language directive that converts annotations to lazy strings — it has ZERO effect on runtime script behavior for the data-processing code paths. Downstream consumers continue reading the same silver/gold/bronze artifacts with identical semantics. No silver/bronze re-ingestion required; no gold re-run required.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    <shared_resource file=".tools/ds-commit-gate.sh">
      Sole writer: this TO. No other active TO touches gate scripts.
    </shared_resource>
    <shared_resource file=".tools/ds-precommit-check.py">
      Sole writer: this TO.
    </shared_resource>
    <shared_resource file="CLAUDE.md">
      Sole writer: this TO for Rule 15 addition. Coordinate with CTO if any concurrent CLAUDE.md edit is in flight (none known at dispatch time).
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/gold/*.py (71 files)">
      Backfill sweep affects all 71. Must coordinate with active gold-script TOs:
      - TOPPOSOPAL (D_04 extension — in flight today; commit early to avoid merge conflict OR merge into existing TOPPOSOPAL branch)
      - POSITIONS (D_04 extension — in flight today; same coordination)
      - ASSETCLASSc / BDPLNNASCHEMA (staged; will wait behind this sweep)
      Recommended sequencing: author ds-commit-gate + ds-precommit-check + CLAUDE.md edits FIRST; ship backfill sweep AFTER TOPPOSOPAL + POSITIONS land (their commits can use the new gate; backfill rolls through cleanly). If coordination becomes painful, surface to COO for sequencing adjustment.
    </shared_resource>
    <shared_resource file="data/orion/scripts/silver/*.py">
      Recently active: SCOPEFIX (shipped `2d3de276` + compat `6c1362de`). Backfill sweep adds `from __future__ import annotations` — already present post-`6c1362de` fix on convert_orion_to_silver.py. Sweep is a no-op or near-no-op on this path.
    </shared_resource>
    <shared_resource file="tests/ds_commit_gate/">
      New test directory. No existing collision. Parallel to existing tests/ subdirs.
    </shared_resource>
    <downstream_pending>
      None. Closure of this TO satisfies ADHC_DSFLOW Phase 2; Phase 3 is any future class-of-bug extensions (not scoped today).
    </downstream_pending>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT upgrade runner Python to 3.11+. Orthogonal infra work; register as ADHC_PYUPGR candidate if Andrew prioritizes.</rule>
    <rule>Do NOT containerize the gate. Overkill per PRD §7 line 328.</rule>
    <rule>Do NOT add new pip deps beyond ruff itself.</rule>
    <rule>Do NOT modify existing py_compile + AST scanner passes in ds-commit-gate. Preserve as belt-and-suspenders.</rule>
    <rule>Do NOT scope-creep the backfill sweep to include any semantic script changes. ADD `from __future__ import annotations` ONLY — any other edits belong in their own TO.</rule>
    <rule>Do NOT retroactively audit commits pre-`b6e0c154` (.001 ship). Gate is forward-looking; the sweep is informational backfill, not a retroactive violation scan.</rule>
    <rule>Do NOT modify `data/*/scripts/*.sh` in the backfill sweep — Rule 15 applies to `.py` only per CTO §7 scope. Bash scripts follow `bash -n` discipline separately (existing).</rule>
  </do_not>
</task_order>
