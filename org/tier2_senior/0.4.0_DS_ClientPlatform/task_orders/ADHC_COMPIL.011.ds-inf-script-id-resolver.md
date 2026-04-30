<task_order>
  <metadata>
    <id>ADHC_COMPIL.011.ds-inf-script-id-resolver</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <lane_rationale>~C lane — resolver/AST/disambiguation work is compiler-internals heavy; matches ~C historical strength on graph-builder + tooling extensions (RA-P0 / ROUTER.T1 / nested-key indexing precedent).</lane_rationale>
    <coordination>.012 reassigned ~D → ~A 2026-04-30 PM per Andrew direction; .011 already COMPLETE at reassignment time. Historical: ran parallel with ~D's pre-reassignment work on .012; independent file-sets, no merge conflict surfaced.</coordination>
    <date>2026-04-30</date>
    <status>COMPLETE</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>F.5 (v3)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md §4.5</prd_ref>
    <effort>3–5 days</effort>
    <gates_on>None — parallelizable with .008–.010 + .012–.014</gates_on>
    <gates_for>Theme G acceptance criterion 2 (`comp-freshness chain inf` form depends on this for `script <id>` lookups). G can ship the `chain` and `artifact` forms first; `script <id>` form gates on .011.</gates_for>
  </metadata>

  <objective>
    v1 Theme A (.001) extended `comp-pipescript` graph indexing to INF gold
    + BD silver + INF silver scripts (path-form). The ID-form resolver was
    NOT extended. Operators hitting `comp-pipescript io INF_B_00`,
    `comp-pipescript io inf-gold-dispatch`, `comp-pipescript io
    convert_orion_to_silver` get FAIL despite the underlying scripts being
    indexed (PRD §2.2 #5; log lines 1449, 1508, 1605, 1613, 1795 across
    last 3 days alone, growing as INFLEC matures).

    Close the ID-resolver gap so all forms work. This is a pure resolver
    extension, not a graph extension — the nodes already exist; the
    user-facing lookup just doesn't reach them.
  </objective>

  <scope>
    Modify the script-resolver layer that backs `comp-pipescript` (and any
    other tool that calls into the same resolver — `comp-blast`,
    `comp-trace` script-node lookups should benefit transparently).

    The resolver must accept all of:

    1. INF prefix scripts:
       - `INF_A_00`, `INF_A_01`, …, `INF_A_*` (any INF accounts-dim/etc.)
       - `INF_B_00`, …, `INF_B_*` (INF holdings-layer scripts if/when present)
       - `INF_C_00`, …, `INF_C_*` (INF performance/canonical-layer)
       - `INF_D_00c`, `INF_D_04`, `INF_D_05`, `INF_D_06`, `INF_D_07`, `INF_09`
       - Any other `INF_*` files present under data/orion/scripts/{gold,silver,bronze}/

       Audit data/orion/scripts/ at TO-start time for the actual file list;
       hardcoding a list defeats the purpose. Resolver should walk the dir +
       ID-extract once and cache.

    2. Hyphenated dispatcher names:
       - `inf-gold-dispatch`, `bd-gold-dispatch`, `orion-gold-dispatch`
       - These should be queryable nodes for `io` (returns the chain
         declaration) and `deployed` (returns runner-side checksum status)

    3. Bare silver-script names (any file under data/{black_diamond,orion}/scripts/silver/
       resolved by stripping `.py` and matching against the bare filename):
       - `convert_orion_to_silver`
       - `bd_price_update`
       - `inject_scoped_overrides`
       - All current siblings — audit silver dirs at TO-start time.

    4. Disambiguation when collision exists:
       - If bare ID `B_00` matches both `data/black_diamond/scripts/gold/B_00*.py`
         AND `data/orion/scripts/gold/B_00*.py` (if INF ever adds B_00):
         - Reject with explicit error listing both candidates
         - Suggest `--pipeline bd` or `--pipeline inf` (new optional flag)
         - Add `--pipeline {bd|inf}` argparse arg to all comp-pipescript
           subcommands; pass through to the resolver

    5. The closest-match suggestion behavior from .008 should still work for
       genuine misses (e.g. `INF_X_99` → `Did you mean: INF_D_07?`).

    Implementation notes:
    - INF scripts hardcode `S3_BUCKET = 'opal-data-inf'` (vs BD's
      `from lib.config import S3_BUCKET`). The AST walker that builds the
      script-resolver must already handle this from .001's work — verify and
      extend if needed.
    - Dispatcher scripts (`*-gold-dispatch.sh`) are bash, not Python. They
      should be indexed as nodes with their chain declaration as
      "READS/WRITES" via shell parsing of the chain definition section, OR
      via a sidecar manifest. Whichever is simpler; document the choice in
      the session log.
  </scope>

  <acceptance_criteria>
    1. `comp-pipescript io INF_B_00` returns READS/WRITES if the script exists.
       If `INF_B_00` does NOT exist on disk, exit 1 with
       `Script not found: INF_B_00. Did you mean: <closest-matching-INF-or-BD-script>?`
    2. `comp-pipescript io INF_D_04` returns READS/WRITES (this script DOES
       exist; verify against current data/orion/scripts/gold/).
    3. `comp-pipescript io inf-gold-dispatch` returns the dispatcher's chain
       declaration. Same for `bd-gold-dispatch`, `orion-gold-dispatch`.
    4. `comp-pipescript io convert_orion_to_silver` returns silver-script
       READS/WRITES (verify this script exists at data/orion/scripts/silver/).
    5. `comp-pipescript io bd_price_update` returns silver-script READS/WRITES.
    6. Ambiguous bare ID (synthetic test: temporarily add a placeholder file
       at data/orion/scripts/gold/B_00.placeholder.py, then revert) emits
       disambiguation error listing both BD and INF candidates with
       `--pipeline {bd|inf}` suggestion.
    7. `comp-pipescript --pipeline inf io B_00` resolves unambiguously to
       the INF candidate (using the same synthetic test). Same for
       `--pipeline bd`.
    8. Existing single-pipeline IDs unchanged: `comp-pipescript io B_01`,
       `io D_04`, `io C_08` etc. all work as today.
    9. `comp-blast` and `comp-trace` script-node lookups against `INF_D_04`
       (or any INF prefix) work transparently — confirms the resolver
       extension reaches all callers.
    10. Test fixture: ≥10 cases covering: INF prefix (3 cases), hyphenated
        dispatcher (3 cases), bare silver name (2 cases), ambiguous + disambiguation
        (1 case), genuine miss + closest-match (1 case). All committed under
        `tests/comp_pipescript/test_inf_id_resolver.sh`.
    11. Append one row per AC to `org/compiler-tools-log.md`.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT modify the underlying graph schema or re-index BD scripts — this is a resolver-layer extension only. All INF nodes already exist from .001's work.</rule>
    <rule>Do NOT hardcode the INF script list — walk data/orion/scripts/ at resolver init. List drift will otherwise re-create the same gap.</rule>
    <rule>Do NOT make `--pipeline` a required flag — only required when an ID is ambiguous. Bare BD/INF-unique IDs must still work without it.</rule>
    <rule>Do NOT regress existing BD-gold-only behavior. The ds-commit-gate + the existing comp-pipescript test suite must pass unchanged.</rule>
    <rule>Do NOT take on COMP_LEARNS scope — this TO is workspace-side only (per Andrew's directive 2026-04-29; DS_ClientPlatform has no COMP_LEARNS authority).</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">Extended script-resolver under .tools/ supporting INF prefix + hyphenated dispatcher + bare silver-name forms</deliverable>
    <deliverable type="code">--pipeline {bd|inf} argparse flag added to comp-pipescript subcommands</deliverable>
    <deliverable type="code">tests/comp_pipescript/test_inf_id_resolver.sh fixture (≥10 cases)</deliverable>
    <deliverable type="document">Session log documenting: file-list audit (INF + silver), dispatcher-indexing implementation choice (shell parse vs sidecar manifest), AC verification</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1–AC10 verification output, regression-guard summary, file-count audit (how many INF + silver scripts now resolve via ID form)</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - `comp-build` if cache older than HEAD (likely, given v1/v2 churn)
    - Direct read of the resolver layer (touched by .001) to confirm where ID-form lookup happens
    - Walk data/orion/scripts/{gold,silver,bronze}/ + data/black_diamond/scripts/silver/ to enumerate the actual file-set the resolver must cover. Capture in session log.
    - `comp-pipescript io INF_D_04` baseline (FAIL today; confirm before fix)

    Phase 2 (before commit):
    - Run all 10 fixture cases; capture exit codes + sample stdout
    - Run existing test suite; confirm zero regressions
    - Spot-check `comp-blast INF_D_04` and `comp-trace INF_D_04 --direction both` to confirm AC9 (resolver extension reaches all callers transparently)
    - `.tools/ds-commit-gate.sh` on every .py file in change set — Rule 14 mandatory

    Phase 3 (after commit):
    - Append one row per AC to `org/compiler-tools-log.md`
    - Confirm in next session window that INF-ID-form FAIL rate drops to zero
  </compiler_tools_mandate>
</task_order>
