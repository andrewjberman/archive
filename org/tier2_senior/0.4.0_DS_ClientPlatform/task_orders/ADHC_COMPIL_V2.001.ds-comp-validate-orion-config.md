# Task Order: ADHC_COMPIL_V2.001 — DS: comp-validate CLI Orion pipeline config support

```xml
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V2.001.ds-comp-validate-orion-config</id>
    <issued_by>0.4.0_DS_ClientPlatform~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-30</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- standing-low; no GO yet; authored per COO bundle GO 20260430 -->
    <priority>LOW — standing backlog under ADHC_COMPIL v2 deferred themes</priority>
  </metadata>

  <objective>
    comp-validate CLI currently loads only data/black_diamond/scripts/gold/gold_validate_config.yaml
    (BD pipeline). Inflection/Orion pipeline has its own config at
    data/orion/scripts/gold/gold_validate_config.yaml with 6 script entries
    (convert_orion_to_silver, INF_09, INF_D_00c, INF_D_02, INF_D_04, INF_B_01).

    Running comp-validate on Orion script IDs (e.g. INF_09, INF_D_04) returns
    "No validate config found" because the CLI is hardcoded to the BD config path.

    This TO extends the CLI to support Orion pipeline checks.
  </objective>

  <context>
    Surfaced by DS~B during INFLV2.002 explicit validation pass (2026-04-30) when
    comp-validate INF_09 returned SKIP: "No validate config found for 'INF_09'".
    Manual validation was run against the Orion config checks as a workaround.

    Root cause in .tools/comp-validate (wrapper -> org/modules/graph/validate_cli.py):
    - STANDALONE_VALIDATORS_DIR hardcoded to data/black_diamond/scripts/validators/
    - load_validate_config called without a config path argument (uses default BD path)
    - No --config or --pipeline flag exposed

    See: org/modules/graph/validate_cli.py (top docstring references BD config only)
  </context>

  <scope>
    <task id="1" label="Add --pipeline flag (bd | inf | all) to comp-validate CLI">
      - Flag selects which gold_validate_config.yaml is loaded
      - Default: bd (backward-compatible with existing usage)
      - inf: loads data/orion/scripts/gold/gold_validate_config.yaml
      - all: loads both configs; script_id must be unique or error out
    </task>

    <task id="2" label="Update standalone validators path for Orion">
      - STANDALONE_VALIDATORS_DIR currently BD-only
      - For --pipeline inf: point to data/orion/scripts/validators/ (or create if needed)
    </task>

    <task id="3" label="Update comp-validate --list output to show pipeline source">
      - --list should show which config each script comes from
      - --list --pipeline inf shows only Orion checks
    </task>

    <task id="4" label="Update validate_cli.py docstring and CLAUDE.md compiler tools table">
      - Docstring: document --pipeline flag
      - CLAUDE.md table: update comp-validate row to note --pipeline flag for Orion
    </task>

    <task id="5" label="Verify comp-validate INF_09 --artifact ... exits 0 post-fix">
      - Run comp-validate --pipeline inf INF_09 --artifact /tmp/partner_analytics.json
      - Must exit 0 (total_aua field present and in SCOPEFIX band)
    </task>
  </scope>

  <acceptance>
    - comp-validate --pipeline inf INF_09 --artifact {path} exits 0 (all-pass or advisory)
    - comp-validate --pipeline inf INF_D_04 --artifact {path} exits 0 against clients_tab.json
    - comp-validate --list --pipeline bd unchanged (backward compat)
    - CLAUDE.md compiler tools table updated
    - .tools/ds-commit-gate.sh passes on any .py files edited
  </acceptance>

  <notes>
    Estimated effort: ~1 day DS (CLI extension + tests).
    Not blocking any current work. Orion validation is done manually today.
    Priority: LOW. Promote to MEDIUM if Orion chain runrate increases to multiple
    runs/week (manual validation becomes a recurring friction point).

    Related: ADHC_COMPIL.007 (AE 0.7.0 comp-validate non-zero exit pointer) --
    once Orion CLI support ships, AE 0.7's comp-validate gate hints apply to INF
    scripts too.
  </notes>
</task_order>
```
