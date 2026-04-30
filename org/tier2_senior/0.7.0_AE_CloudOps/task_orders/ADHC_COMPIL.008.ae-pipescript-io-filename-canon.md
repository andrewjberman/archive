<task_order>
  <metadata>
    <id>ADHC_COMPIL.008.ae-pipescript-io-filename-canon</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-30</date>
    <status>complete</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>F.1 (v3)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md §4.1</prd_ref>
    <effort>2–3 days</effort>
    <gates_on>None</gates_on>
    <gates_for>None — bundle candidate with .009 + .010 (single AE owner, common file-set in .tools/)</gates_for>
    <bundle_recommendation>Ship .008 + .009 + .010 as a single shipping unit (4–6d total). All three are contained edits to .tools/ argparse + input-canonicalization layers.</bundle_recommendation>
  </metadata>

  <objective>
    Make `comp-pipescript io B_01.holdings_lots.py` succeed identically to
    `comp-pipescript io B_01`. The filename-form FAIL is the highest-frequency
    friction point in the corpus — every session, every agent, 30+ FAIL→retry
    pairs in the past two weeks (PRD §2.2 #1, log lines 820, 826, 838, 860,
    862, 1077, 1080, 1082, 1101, 1139, 1416 representative). The fix is a
    contained input-canonicalizer addition; no graph schema change.
  </objective>

  <scope>
    Modify .tools/comp-pipescript (or the underlying script-resolver layer it
    calls) to canonicalize input before resolution:

    1. If argument matches `<ID>.<name>.py` pattern (e.g. B_01.holdings_lots.py,
       D_00c.portal_leaderboard.py, INF_D_04.client_portal_summary.py):
       - Strip `.py` and the `.<name>` suffix; resolve by `<ID>` first
    2. If argument is a full path under
       `data/{black_diamond,orion,schwab}/scripts/{gold,silver,bronze}/`:
       - Extract the filename, then apply rule 1
    3. If still no match after canonicalization, exit 1 with an error message
       using `difflib.get_close_matches`:
       `Script not found: <input>. Did you mean: <closest-matching-ID>?`

    Apply the same canonicalization to all `comp-pipescript` subcommands that
    accept a script identifier: `io`, `feeds`, `consumers`, `deployed`,
    `postdeps`, `overlap` (both args), `chain`. Do NOT modify `dag` or `stats`
    (no script identifier).

    The canonicalizer is a single helper function called from each subcommand
    handler; do not duplicate logic.
  </scope>

  <acceptance_criteria>
    1. `comp-pipescript io B_01.holdings_lots.py` produces stdout byte-identical
       to `comp-pipescript io B_01`.
    2. `comp-pipescript io data/black_diamond/scripts/gold/B_01.holdings_lots.py`
       produces stdout byte-identical to `comp-pipescript io B_01`.
    3. `comp-pipescript io B_01.bogus.py` exits 1 with stderr containing
       `Did you mean: B_01`.
    4. Test fixture: 5 representative scripts (B_01, D_00c, C_08, INF_D_04,
       I_C00) × 3 input forms (ID, filename, full-path) = 15 cases. Commit the
       fixture under `tests/comp_pipescript/test_filename_canonicalization.sh`
       (or equivalent path). All 15 PASS.
    5. Existing test suite for comp-pipescript passes unchanged (no regression
       on ID-form invocations across BD + INF gold corpora).
    6. Same canonicalization verified on `feeds`, `consumers`, `deployed`,
       `postdeps`, `overlap` (one spot-check each).
    7. Append one row per AC verification to `org/compiler-tools-log.md`.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT change the output format of any subcommand — canonicalization is upstream of formatting.</rule>
    <rule>Do NOT silently fall back to bare-name resolution when the filename form is given but the script doesn't exist — emit the explicit "Did you mean" error so operators see the miss.</rule>
    <rule>Do NOT canonicalize for `dag` or `stats` (no script identifier; would be wasted work).</rule>
    <rule>Do NOT introduce a `--strict` flag or any mode that disables canonicalization — the goal is to make the friendly form work, not to add a knob.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/comp-pipescript with input canonicalizer applied to all script-identifier subcommands</deliverable>
    <deliverable type="code">tests/comp_pipescript/test_filename_canonicalization.sh fixture (15 cases)</deliverable>
    <deliverable type="document">Session log with AC1–AC7 verification output</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with stdout-diff confirmation for AC1+AC2 + fixture pass count + log-row links</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - `comp-build` if cache older than HEAD
    - Direct read of .tools/comp-pipescript to locate the input-handling layer
    - `comp-blast .tools/comp-pipescript` (now possible post v1 Theme A path-form resolution) to confirm no other tool depends on the input-parser shape

    Phase 2 (before commit):
    - Run all 15 fixture cases; capture exit codes + stdout diffs
    - Run a sample of existing ID-form invocations (B_01, D_00c, INF_D_04, I_C00) on `io`, `feeds`, `consumers` to confirm no regression
    - `.tools/ds-commit-gate.sh` on any .py file in the change set

    Phase 3 (after commit):
    - Append one row per AC to `org/compiler-tools-log.md`
    - Confirm in next session window that the FAIL→retry pattern for `<ID>.<name>.py` form has dropped to zero
  </compiler_tools_mandate>
</task_order>
