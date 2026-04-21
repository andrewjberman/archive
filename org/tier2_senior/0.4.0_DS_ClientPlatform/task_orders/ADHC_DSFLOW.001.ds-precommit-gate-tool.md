<task_order>
  <metadata>
    <id>ADHC_DSFLOW.001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>pending</status>
    <project_code>ADHC_DSFLOW</project_code>
    <priority>P1 (closes same-class 081223b5 + 035352c3 latent-PROD-crash pattern; 2 incidents in 2 days)</priority>
    <sla>2h from GO</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DSFLOW.md (sections 6.1 + 7 TO-1 + 9 + 10)</ref>
    <ref type="incident_1">commit 081223b5 (2026-04-20 19:02Z) B_00.canonical_holdings.py — missing `from collections import defaultdict`; fix 1a54d46a; surfaced on PROD nightly 23:00Z + 04:00Z canonical-prices daily = ~14h PROD-freeze</ref>
    <ref type="incident_2">commit 035352c3 (2026-04-20 19:39Z) D_02.advisor_client_detail.py — KeyError on ['first_date','last_date']; fix 048a6fa3; surfaced on QA runner ~1h post-upload</ref>
    <ref type="spike_evidence">PRD §5 + §6.1 — 25-line ast.walk spike run against .runtmp/B_00_prefix.py CATCHES `defaultdict` at L428 statically; `python -m py_compile` alone PASSES (doesn't catch function-body undefined names)</ref>
    <ref type="precedent">HLOT2 Phase 2 smoke-gate (ast.parse + importlib exec_module) 2026-04-21 — catches module-level import bugs but not function-body undefined-names; DSFLOW gate is tighter (catches function-body too)</ref>
    <ref type="memory">memory/feedback_ds_commits_ae_deploys.md — DS owns full commit→deploy cycle (this TO materializes the tool that makes enforcement tractable)</ref>
    <ref type="project_json">org/projects/ADHC_DSFLOW.json</ref>
    <ref type="target_files">.tools/ds-precommit-check.py (NEW) + .tools/ds-commit-gate.sh (NEW) + tests/ds_precommit_check_test.py (NEW)</ref>
  </references>

  <objective>
    Build a ~60-LOC stdlib-only AST undefined-name scanner + shell wrapper that DS runs before every gold-script commit. Together with `python -m py_compile`, these form the BLOCKING pre-commit gate that catches Class A (undefined-name + syntax) latent bugs before they reach S3 / qa-runner / PROD.

    **Key property:** stdlib-only, zero dependencies. Runs on any Python 3.10+ interpreter without pip install. ~60 LOC total + ~25 LOC tests + ~10 LOC shell wrapper.

    **What it catches (Class A, ~50pct of observed incidents):** missing imports used in function bodies (defaultdict, deepcopy, etc.); typos in function/variable names; names referenced after rename without caller updates; syntax / indentation / malformed-import errors (via py_compile).

    **What it does NOT catch (Class B, ~50pct, explicitly deferred):** DataFrame column-contract drift (035352c3 class) — requires pandas schema inference; cross-file undefined names; runtime-only errors. Class B handled via PRD §6.3 code-hygiene assert-at-boundary pattern.
  </objective>

  <scope>
    <files>
      <file action="create">.tools/ds-precommit-check.py — pure-AST undefined-name scanner, stdlib-only</file>
      <file action="create">.tools/ds-commit-gate.sh — wrapper invoking py_compile + ds-precommit-check.py, blocks on either failure</file>
      <file action="create">tests/ds_precommit_check_test.py — unit tests with positive + negative cases (including .runtmp/B_00_prefix.py reproducer)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="ast-scanner-tool">
      **.tools/ds-precommit-check.py** (~60 LOC, stdlib-only):
      1. Accept one or more .py file paths as CLI args.
      2. For each file: `ast.parse(open(path).read())` into a module tree.
      3. Walk the AST collecting a "defined" set: all imports (Import + ImportFrom), module-level Assign targets, FunctionDef + AsyncFunctionDef names, ClassDef names. Include `__name__` / `__file__` / standard module dunders.
      4. Walk function bodies collecting every `ast.Name` with Load context. For each, check: is it in `defined` + Python builtins (via `builtins.__dict__`) + its function's local scope (recursive walk collecting `FunctionDef.args` + nested Assign targets + for-target + comprehension-target names)?
      5. Exit 0 if all Names resolve; exit 1 + stderr line per unresolved Name (format: `{file}:{lineno}: undefined name '{name}'`).
      6. CLI flags: `--verbose` to show defined set + scanned function count; default output is silent-on-pass, line-per-miss-on-fail.
      7. Edge cases: `from foo import *` → whitelist (don't scan that file until star-imports deprecated; flag via `--strict`); global() / setattr() / eval() / exec() usage in function body → warn not error; lambda bodies scan same as functions; walrus operator (`:=`) treated as Assign target.
    </deliverable>
    <deliverable id="wrapper-script">
      **.tools/ds-commit-gate.sh** (~10 LOC):
      ```bash
      #!/bin/bash
      # Usage: ds-commit-gate.sh <file1> [file2 ...]
      # Blocks commit on py_compile OR AST scan failure.
      set -e
      for f in "$@"; do
        if [[ "$f" != data/black_diamond/scripts/gold/* ]]; then continue; fi
        python -m py_compile "$f" || { echo "BLOCKED: py_compile failed on $f"; exit 1; }
        python .tools/ds-precommit-check.py "$f" || { echo "BLOCKED: undefined-name scan failed on $f"; exit 1; }
      done
      echo "OK: pre-commit gate clean for $# file(s)"
      ```
      Make executable (`chmod +x .tools/ds-commit-gate.sh`).
    </deliverable>
    <deliverable id="unit-tests">
      **tests/ds_precommit_check_test.py** with:
      1. Positive case: well-formed Python file (all Names resolve) → exit 0, empty stderr.
      2. Negative case A — undefined in function body: `def f(): return defaultdict(int)` without import → exit 1, stderr flags `defaultdict`.
      3. Negative case B — typo: `def f(x): return lenght(x)` without `lenght` defined → exit 1.
      4. Reproducer case: run against `.runtmp/B_00_prefix.py` → exit 1 with `defaultdict at L428` flagged.
      5. Edge case A — lambda body: `lambda x: sorte(x)` without `sorte` → exit 1.
      6. Edge case B — comprehension scope: `[x for x in items]` → exit 0 (x is comprehension-local).
      7. Edge case C — star import: `from foo import *` + use of unknown name → exit 0 (whitelisted unless `--strict`).
      8. Edge case D — walrus operator: `if (n := len(x)) > 0: return n` → exit 0 (n is walrus-defined in enclosing scope).
      Test harness: pure pytest-compatible (or unittest if stdlib-only preferred per zero-deps guidance — adjust).
    </deliverable>
    <deliverable id="integration-self-verify">
      Run both new files through each other:
      1. `python -m py_compile .tools/ds-precommit-check.py` → exit 0
      2. `python .tools/ds-precommit-check.py .tools/ds-precommit-check.py` → exit 0 (tool self-scans clean)
      3. `python -m py_compile .tools/ds-commit-gate.sh` — N/A, bash file; skip
      4. Run `.tools/ds-commit-gate.sh` against all HEAD gold scripts (`find data/black_diamond/scripts/gold -name "*.py"`) → all exit 0 (no false positives on current state). If any fire, TRIAGE before commit: either fix the file (rare — real undefined name in production) or add a whitelist mechanism.
    </deliverable>
    <deliverable id="commit-and-push">
      `git commit --only --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"` with paths:
      - .tools/ds-precommit-check.py
      - .tools/ds-commit-gate.sh
      - tests/ds_precommit_check_test.py
      - org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-21/dsflow_001_precommit_gate_tool.md
      - org/compiler-tools-log.md

      `git push origin CLOUD` per DS lane authority clarification (DSFLOW.002 will formalize this in DS README, but TO 1 itself executes under existing push-via-DT discipline if DS push authority not yet updated; coordinate with DT if so).
    </deliverable>
  </deliverables>

  <wire_contract>
    Zero runtime delta on any existing pipeline. Pure tooling addition. Gate is opt-in via shell wrapper invocation — no git-hook integration in v1. DS invokes manually per DSFLOW.002 prompt.md step.

    No AWS touch. No TF touch. No Lambda touch. No portal touch. No gold-script touch.
  </wire_contract>

  <acceptance_criteria>
    1. `.tools/ds-precommit-check.py` + `.tools/ds-commit-gate.sh` + `tests/ds_precommit_check_test.py` exist in repo.
    2. All 8 test cases in `tests/ds_precommit_check_test.py` PASS (`python -m pytest tests/ds_precommit_check_test.py -v` or unittest equivalent exit 0).
    3. `.tools/ds-commit-gate.sh $(find data/black_diamond/scripts/gold -name "*.py" | tr '\n' ' ')` exits 0 on all HEAD gold scripts — no false positives on current state. Any fire triaged: either fix the actual bug or whitelist the pattern. Document any whitelisted patterns in session log.
    4. `.tools/ds-commit-gate.sh .runtmp/B_00_prefix.py` exits 1 with `defaultdict` flagged (081223b5 reproducer — definitive evidence gate catches the class of bug).
    5. `ds-precommit-check.py` is stdlib-only (no pip installs required). Confirm via `python -c "import sys; ...; [f for f in deps if f not in sys.stdlib_module_names]"` returns empty list (or equivalent check).
    6. Tool self-scans clean: `python .tools/ds-precommit-check.py .tools/ds-precommit-check.py` exits 0.
    7. `ds-commit-gate.sh` is executable (`ls -l` shows `x` bit).
    8. Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-21/dsflow_001_precommit_gate_tool.md` reproducing every `<run>` + observed output + pass/fail vs `<expect>`.
    9. MCP COMPLETE to COO with commit hash + test output + self-scan output + any triaged-whitelist-pattern notes.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m ast .runtmp/B_00_prefix.py 2>&amp;1 | head -5; python -c "import sys; print(sys.version_info)"</run>
        <expect>Python version ≥3.10 (needed for walrus + match-statement handling). AST module dumps the parse tree — baseline that .runtmp/B_00_prefix.py parses cleanly (ast.parse exit 0; pre-check against which the new tool will be tested).</expect>
        <if_mismatch>If Python &lt;3.10, flag to COO — target runtime needs upgrade before gate ships. Unlikely.</if_mismatch>
      </step>
      <step>
        <run>Read the 25-line ast.walk spike referenced in PRD §6.1 (search `.runtmp/` for any prior spike script, or reproduce per PRD spec)</run>
        <expect>Baseline evidence: walking Name nodes in function bodies catches `defaultdict` at L428 of B_00_prefix.py. If a prior spike script exists, use it as starting point; if not, implement the 25-line core per PRD spec and verify catches `defaultdict` before expanding to ~60 LOC.</expect>
        <if_mismatch>If the core ast.walk approach doesn't catch the known miss, re-design before coding. Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>Enumerate HEAD gold scripts: `find data/black_diamond/scripts/gold -name "*.py" | wc -l` + list first 5 filenames</run>
        <expect>Capture baseline count of gold scripts (~30 per PRD). These all get the no-false-positives check post-implementation.</expect>
        <if_mismatch>If count is 0, repo layout changed — surface. If count > 50, scope creep; verify the filter catches only gold scripts (not vendor/legacy).</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile .tools/ds-precommit-check.py + python .tools/ds-precommit-check.py .tools/ds-precommit-check.py</run>
        <expect>Both exit 0. Tool is syntactically clean + self-scans clean.</expect>
        <if_mismatch>STOP. If tool doesn't self-scan clean, there's a real bug in it.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest tests/ds_precommit_check_test.py -v (or unittest equivalent)</run>
        <expect>All 8 test cases PASS (positive + 4 negative + 3 edge cases). pytest output shows 8 passed, 0 failed.</expect>
        <if_mismatch>Any test failure = fix tool before commit. Do not commit partial coverage.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh $(find data/black_diamond/scripts/gold -name "*.py")</run>
        <expect>Exit 0, "OK: pre-commit gate clean for N file(s)" printed. No false positives on HEAD gold scripts.</expect>
        <if_mismatch>If false positive fires: triage. Either the "undefined" name is legitimately undefined (latent bug the gate found — file fix-forward TO) OR the scanner is too aggressive (add surgical whitelist + document). DO NOT disable gate wholesale — exemptions are surgical.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh .runtmp/B_00_prefix.py</run>
        <expect>Exit 1. stderr: `defaultdict at L428: undefined name`. Proves gate catches the specific incident class.</expect>
        <if_mismatch>If the reproducer doesn't flag, tool is broken. Fix + re-run all tests.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>Verify repo state post-commit: `git log --oneline -3 .tools/`</run>
        <expect>Commit visible; author = 0.4.0_DS_ClientPlatform.</expect>
        <if_mismatch>Commit identity wrong = re-author (feedback_selective_staging_only + commit_only_flag + agent commit identity rules).</if_mismatch>
      </step>
      <step>
        <run>Append to org/compiler-tools-log.md via auto-hook (SERIAL=0.4.0_DS_ClientPlatform, TO_ID=ADHC_DSFLOW.001 — set via .comp-graph/.agent_context)</run>
        <expect>Auto-append fires for comp-* invocations in this TO (if any). This TO mostly uses py_compile + pytest which aren't comp-* tools, so auto-append may be minimal — OK.</expect>
        <if_mismatch>If no append rows for this TO: acceptable (few comp-* invocations used). Document manually in session log Compiler Tools section.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>No cross-pod touch. DSFLOW.001 is isolated DS tooling work.</item>
    <item>DSFLOW.002 (my-lane org-docs update) parallel-authorized per CTO handoff MCP 20260421T125319Z — can ship concurrently. When both land, DS startup surfaces the gate + authority change together.</item>
    <item>DSFLOW.003 (passive training run) fires on next gold-script commit post-DSFLOW.001+002. HLOT2 `5f5d0319` is already committed pre-gate (non-retroactive per PRD §13); next candidate is next BFIX iteration or any subsequent DS gold-script work.</item>
    <item>DS IAM expansion (PRD §11 Q4): `s3:PutObject` on `opal-bd-gold-code/gold/*` may already be provisioned for DS role; if not, AE 0.7 micro-TO. Verification happens in DSFLOW.002 prep, not here — DSFLOW.001 is pure tooling build + test, no S3 touch.</item>
    <item>No AE 0.6 / BD pipeline conflict. AE 0.6 is executing HLOT2 qa-runner emergency ship (per Andrew 12:42Z + DS~A MCP 20260421T133407Z) + BFIX1/2 batch. Both orthogonal to DSFLOW.001.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency>None upstream. This TO is self-contained.</dependency>
    <dependency_downstream>DSFLOW.002 (org-docs) — references `.tools/ds-commit-gate.sh` path in CLAUDE.md Rule 13 + DS prompt.md; ship order doesn't matter strictly but DSFLOW.002 text assumes the tool exists by the time it lands.</dependency_downstream>
    <dependency_downstream>DSFLOW.003 (training run) — requires both DSFLOW.001 + DSFLOW.002 complete before firing.</dependency_downstream>
  </dependencies>

  <next>On commit + push + tests-pass: MCP COMPLETE to COO with commit hash + test output + self-scan + whitelist notes. COO flips status pending→complete, verifies DSFLOW.002 co-ships, sets DSFLOW.003 trigger-ready.</next>
</task_order>
