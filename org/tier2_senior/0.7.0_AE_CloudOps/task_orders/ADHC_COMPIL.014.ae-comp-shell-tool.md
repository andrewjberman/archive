<task_order>
  <metadata>
    <id>ADHC_COMPIL.014.ae-comp-shell-tool</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-30</date>
    <status>complete</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>H (v3)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md §4.7</prd_ref>
    <effort>1 week</effort>
    <gates_on>None — parallelizable with all other v3 TOs</gates_on>
    <gates_for>v3 ship; pre-commit hook closes the shell-utility-regression gap end-to-end</gates_for>
  </metadata>

  <objective>
    Build `comp-shell`: a new compiler tool that detects bare references to
    forbidden Git Bash 3.6.7 utilities in local-runtime shell scripts before
    they cause silent guard fall-through. ADHC_BASHFIX.001 (2026-04-29)
    incident: org/mcp/inbox-watch.sh single-watcher guard fell through
    because bare `pgrep` produced empty result; three watchers ran
    concurrently for hours.

    The CTO explicitly flagged this as a candidate gap in
    `compiler-tools-log.md:1620`: *"no comp-* covers shell-script utility
    surface (candidate for future tooling, out of scope ADHC_BASHFIX)."*
    This TO closes it.

    AE 0.7 is the natural owner — owns .tools/, owns ds-commit-gate.sh,
    ran point on the ADHC_BASHFIX.002 fallback fix.
  </objective>

  <scope>
    Build .tools/comp-shell with the following surface:

    Subcommands:
    - `comp-shell scan [path]` — scan a single file or directory; default
      is the union of CLAUDE.md Rule 16 in-scope paths (.tools/, org/mcp/,
      org/threads/, infra/aws/lambda/ci/, infra/aws/terraform/)
    - `comp-shell scan --all` — scan every .sh file in workspace except
      EC2-side paths (infra/aws/ec2/ + data/*/scripts/*/ — these run on
      Amazon Linux where utilities are present)
    - `comp-shell list-forbidden` — print the forbidden-utility list +
      canonical fallback patterns
    - `comp-shell --help` — standard

    Forbidden utilities (per CLAUDE.md Rule 16):
    - pgrep, pkill, flock, pidof, setsid, wget

    Detection rules:
    - For each forbidden utility, find every line where the utility appears
      as a command. Filter out:
      - Lines starting with `#` (comments) outside a here-doc
      - Single-quoted string literals where the utility name is part of
        a string, not a command (regex distinguishable; if regex too
        fragile, accept WARN-level false positives in strings as
        acceptable noise)
      - Here-doc bodies (text inside `<<EOF ... EOF` blocks) — do NOT
        scan, these are typically literal output not commands
    - Within the surrounding function or block (default lookback 30 lines;
      configurable via `--guard-lookback N`), check for any of:
      - `command -v <util>` test
      - `if command -v <util>` guarded block
      - `which <util>` test (treat as guard-equivalent for backward compat)
    - Classify:
      - GUARDED: a guard exists in the lookback window → emit WARN
      - UNGUARDED: no guard found → emit ERROR

    Output format (one finding per line):
      `<file>:<line>:<severity>:<utility>:<guard-status>:<context-excerpt>`
    Where:
    - severity ∈ {WARN, ERROR}
    - guard-status ∈ {guarded, unguarded}
    - context-excerpt = the matched line trimmed to 80 chars

    Exit codes:
    - 0 — no ERROR-level findings (zero or more WARN OK; WARNs do not block)
    - 1 — at least one ERROR finding
    - 2 — config error (allowlist file unparseable, scan path doesn't
      exist, etc.)

    Optional allowlist file: workspace-root .compshellrc (yaml or
    line-delimited; pick yaml for consistency with other tools)
    - Allows file/path patterns to downgrade ERROR → WARN OR exempt
      entirely. Initial v1 should rely on path-based exemption (EC2-side
      paths) per PRD §7 Q2 — the per-file allowlist is for v2 if needed.
    - For v1 of this TO: implement the path-based exemption only. Stub
      the .compshellrc loader so v2 can extend without a tool rewrite.

    Pre-commit hook integration:
    - Extend .tools/ds-commit-gate.sh to additionally run `comp-shell
      scan` on every .sh file in the staged set whose path is in-scope per
      CLAUDE.md Rule 16. Out-of-scope paths (EC2-side) are not scanned.
    - Hook exits non-zero if any ERROR found in the staged set.
    - Hook output should mirror existing ds-commit-gate.sh format: clear
      OK/BLOCKED prefix + per-finding lines.

    Config additions:
    - Add comp-shell entry to org/modules/graph/comp-tools.yaml matching
      the existing tool-doc pattern.
    - Document the canonical fallback pattern (the `command -v pgrep ||
      ps -ef | awk` style) in --help and in the comp-tools.yaml note. Use
      org/mcp/inbox-watch.sh post-ADHC_BASHFIX.002 as the canonical
      reference (commit 045296b18).
  </scope>

  <acceptance_criteria>
    Tool behavior:
    1. `comp-shell scan org/mcp/inbox-watch.sh` against the pre-ADHC_BASHFIX
       commit (the buggy version with bare pgrep) emits ERROR with
       guard-status=unguarded. Use `git show <pre-fix-sha>:org/mcp/inbox-watch.sh`
       to get the bad version for the test.
    2. `comp-shell scan org/mcp/inbox-watch.sh` against the post-ADHC_BASHFIX
       commit emits WARN with guard-status=guarded (because the canonical
       fallback uses `command -v pgrep`).
    3. `comp-shell scan .tools/` scans every .sh file under .tools/ with
       no exclusions. Exit code reflects whether any ERROR found.
    4. `comp-shell scan --all` extends to the full workspace except
       infra/aws/ec2/ and data/*/scripts/*/.
    5. `comp-shell list-forbidden` prints the 6 utilities + canonical
       fallback for each (or at least for pgrep where the pattern is
       proven from ADHC_BASHFIX.002).

    Detection accuracy:
    6. Test fixture: 5 hand-written shell-script samples committed under
       tests/comp_shell/fixtures/ covering:
       - bare pgrep (ERROR)
       - pgrep guarded by `command -v pgrep` (WARN)
       - pgrep in a comment (no finding)
       - pgrep inside a single-quoted string (no finding OR WARN false
         positive — accept either, document the choice)
       - pgrep in a here-doc literal (no finding)
       Each sample includes the expected verdict in a comment header. Tool
       output matches expectations for all 5.

    Pre-commit hook:
    7. Pre-commit hook BLOCKS a commit that introduces a bare pgrep call
       in an in-scope path. Verify by attempting `git commit` with a test
       .sh file containing bare pgrep; commit fails non-zero.
    8. Pre-commit hook ALLOWS a commit when the call is guarded. Verify
       same flow with the guarded variant.
    9. Pre-commit hook does NOT scan EC2-side paths. Verify with a test
       .sh containing bare pgrep at infra/aws/ec2/test-script.sh; commit
       succeeds.

    Coverage:
    10. Run `comp-shell scan --all` on the current workspace. Document
        the count of ERROR findings (must be 0 — workspace is clean
        post-ADHC_BASHFIX). Document the count of WARN findings (any
        legitimately-guarded uses).
    11. If any ERROR fires unexpectedly: STOP and escalate to CTO before
        shipping the pre-commit hook — likely indicates a guard the tool
        misses, OR a real bug.

    Documentation:
    12. org/modules/graph/comp-tools.yaml has a new entry for comp-shell
        matching the existing schema (command, when, subcommands, cost,
        data_sources, replaces, note).

    Logging:
    13. Append one row per AC to org/compiler-tools-log.md.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT scan EC2-side paths (infra/aws/ec2/, data/*/scripts/*/) — those paths legitimately run on Amazon Linux per CLAUDE.md Rule 16. Path-based exemption is mandatory.</rule>
    <rule>Do NOT block on WARN-level findings — only ERROR (unguarded) blocks. WARN is informational.</rule>
    <rule>Do NOT extend the forbidden-utility list beyond CLAUDE.md Rule 16's six (pgrep/pkill/flock/pidof/setsid/wget). If ops finds a 7th utility missing in Git Bash, that's a CLAUDE.md Rule 16 amendment first; tool extension follows.</rule>
    <rule>Do NOT use emoji in tool output — CLAUDE.md "Code Quality" section. Plain ASCII OK/WARN/ERROR.</rule>
    <rule>Do NOT implement the per-file .compshellrc allowlist in v1 — path-based exemption only (PRD §7 Q2). Stub the loader so v2 can extend without rewrite.</rule>
    <rule>Do NOT proceed with the pre-commit hook integration if AC10 surfaces unexpected ERRORs — escalate to CTO first.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/comp-shell — Python entry point with subcommand dispatch + scan engine</deliverable>
    <deliverable type="code">.tools/ds-commit-gate.sh extended with comp-shell scan step on .sh files in staged set</deliverable>
    <deliverable type="code">tests/comp_shell/fixtures/ — 5 hand-written sample scripts + expected verdicts</deliverable>
    <deliverable type="document">org/modules/graph/comp-tools.yaml entry for comp-shell</deliverable>
    <deliverable type="document">Session log with AC1–AC13 verification + workspace ERROR/WARN count from AC10</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with: AC1+AC2 git-show evidence, fixture pass count, pre-commit hook BLOCK/ALLOW demonstrations, workspace baseline scan summary</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - Direct read of CLAUDE.md Rule 16 (utility availability table) to
      confirm the canonical forbidden-utility list
    - Direct read of org/mcp/inbox-watch.sh (HEAD + pre-ADHC_BASHFIX.002
      via `git show`) to ground the AC1 + AC2 fixtures in real history
    - Direct read of .tools/ds-commit-gate.sh to understand the existing
      hook structure for clean extension

    Phase 2 (before commit):
    - Run all 5 fixture cases; capture exit codes + stdout
    - Run AC10 baseline scan (`comp-shell scan --all`); document
      ERROR/WARN counts
    - Verify pre-commit hook AC7+AC8+AC9 with synthetic test files
      (do NOT keep the test files committed — clean up after verification)
    - bash -n on .tools/ds-commit-gate.sh to confirm syntax-clean post-edit

    Phase 3 (after commit):
    - Append one row per AC to org/compiler-tools-log.md
    - First-week observability: monitor for any AE/DS-side commit that
      gets unexpectedly blocked by the new hook. If false-positive blocks
      surface, gather specifics + escalate to CTO for tool tuning.
  </compiler_tools_mandate>
</task_order>
