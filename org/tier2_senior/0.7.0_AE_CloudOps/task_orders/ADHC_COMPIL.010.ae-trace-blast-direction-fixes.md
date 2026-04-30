<task_order>
  <metadata>
    <id>ADHC_COMPIL.010.ae-trace-blast-direction-fixes</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-30</date>
    <status>complete</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>F.3 + F.4 (v3) — bundled (both are direction-flag fixes)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md §4.3 + §4.4</prd_ref>
    <effort>1–2 days</effort>
    <gates_on>None</gates_on>
    <bundle_recommendation>Bundle with .008 + .009 — same AE owner, common .tools/ argparse layer.</bundle_recommendation>
  </metadata>

  <objective>
    Two contained argparse fixes:

    F.3: Accept `upstream` and `downstream` as drop-in synonyms for `up`
    and `down` in `comp-trace --direction`. Hit at log line 1768
    (ADVI_INFLEC.DIAGFIX.007 2026-04-29).

    F.4: Allow `--direction` flags on prefix-qualified `comp-blast` queries
    (e.g. `lambda:opal-partners-data --direction both`). Hit at log line 887
    (ADVI_ROLGAT.DT1 2026-04-17).

    Both are wiring defects in argparse / direction-flag forwarding. Bundled
    because they touch adjacent code and are too small to be separate TOs.
  </objective>

  <scope>
    F.3 — comp-trace direction aliases (.tools/comp-trace):
    1. Extend argparse `choices=['up', 'down', 'both']` to
       `choices=['up', 'upstream', 'down', 'downstream', 'both']`.
    2. Normalize before traversal: `upstream → up`, `downstream → down`.
    3. Update --help string to list both forms (alias documentation).

    F.4 — comp-blast direction-flag wiring (.tools/comp-blast):
    1. Audit the prefix-qualified resolver path (`lambda:`, `gold:`,
       `silver:`, `component:`) — currently the `--direction` flag is not
       passed through to the traversal call when the prefix form is used.
    2. Restructure so the direction flag is read once at the top of the
       handler and passed uniformly to all resolver branches (bare names,
       prefix-qualified, full file paths).
    3. Update --help if the prefix-qualified-with-direction combination is
       not currently documented.
  </scope>

  <acceptance_criteria>
    F.3:
    1. `comp-trace <node> --direction upstream` produces stdout byte-identical
       to `comp-trace <node> --direction up`.
    2. `comp-trace <node> --direction downstream` produces stdout byte-identical
       to `comp-trace <node> --direction down`.
    3. `comp-trace <node> --direction both` unchanged.
    4. `comp-trace <node> --direction sideways` exits 2 with argparse
       "invalid choice" error listing all 5 valid values.

    F.4:
    5. `comp-blast lambda:opal-partners-data --direction both` produces the
       same node set as `comp-blast opal-partners-data --direction both`
       (when bare name resolves uniquely).
    6. `comp-blast gold:D_04 --direction up` works — returns upstream
       producers of D_04's outputs.
    7. `comp-blast component:portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx --direction down`
       works — returns downstream consumers / API endpoints.
    8. Existing prefix-qualified blast queries WITHOUT `--direction` flag
       behavior unchanged.

    Both:
    9. Append one row per AC to `org/compiler-tools-log.md`.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT change comp-trace traversal semantics — `up`/`down`/`both` already work; aliases are pure normalization.</rule>
    <rule>Do NOT change the default direction (currently `both` for comp-trace, blast-radius for comp-blast).</rule>
    <rule>Do NOT add new prefix kinds beyond what comp-blast already supports — F.4 is wiring-only, not feature expansion.</rule>
    <rule>Do NOT split this into two TOs — the fixes are too small; bundling is intentional.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/comp-trace with direction-alias support</deliverable>
    <deliverable type="code">.tools/comp-blast with prefix-qualified direction-flag wiring</deliverable>
    <deliverable type="document">Session log with AC1–AC9 verification output</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with: stdout-diff confirmation for AC1–AC3 + AC5, error message for AC4, sample output for AC6+AC7</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - Direct read of .tools/comp-trace and .tools/comp-blast to locate argparse + direction-handling layers
    - Confirm the bare-name comp-blast invocations against `opal-partners-data`, `D_04`, and a sample component still work as baseline before edits

    Phase 2 (before commit):
    - Run AC1–AC8 fixture cases; capture exit codes + stdout/stderr
    - One spot-check that direction-flag-less `comp-blast lambda:foo` still works (regression guard)

    Phase 3 (after commit):
    - Append one row per AC to `org/compiler-tools-log.md`
  </compiler_tools_mandate>
</task_order>
