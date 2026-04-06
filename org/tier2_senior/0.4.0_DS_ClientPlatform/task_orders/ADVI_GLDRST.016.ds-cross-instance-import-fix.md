<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-02-gldrst-016-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-02</date>
    <status>complete</status>
    <!-- Completed 2026-04-02. Commit aed6630d. 7 scripts fixed + config.py warning added. -->
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Fix 7 scripts outside `gold/` that import `from lib.config import S3_BUCKET`.
    These scripts run on the download instance where `gold/lib/config.py` does not
    exist, causing `ModuleNotFoundError`. Also commit the AE's inline fix for
    `merge-daily-incremental.py` which is currently only on S3 (not in the repo).
  </objective>

  <context>
    `lib/config.py` lives at `data/black_diamond/scripts/gold/lib/config.py` and
    is only present on the gold runner's filesystem. Scripts in `silver/` and
    `classification/` run on a different EC2 instance (the download instance).
    These imports fail with `ModuleNotFoundError` when the scripts are invoked
    on the download instance.

    AE fixed `merge-daily-incremental.py` on S3 (inline constant) but the fix
    is NOT committed locally. The other 6 scripts have the same latent bug.

    PRD: docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md (Work Stream B)
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/silver/merge-daily-incremental.py</file>
      <file action="modify">data/black_diamond/scripts/silver/merge-daily-allocation-incremental.py</file>
      <file action="modify">data/black_diamond/scripts/silver/build_canonical_prices_v2.py</file>
      <file action="modify">data/black_diamond/scripts/silver/inject_scoped_overrides.py</file>
      <file action="modify">data/black_diamond/scripts/silver/bd_price_update.py</file>
      <file action="modify">data/black_diamond/scripts/classification/resolve_tickers.py</file>
      <file action="modify">data/black_diamond/scripts/classification/backfill_name_aliases.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      In all 7 scripts, replace:
      ```python
      from lib.config import S3_BUCKET
      ```
      with:
      ```python
      S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')
      ```
      Ensure `import os` is present at the top of each file. The `lib.config`
      module provides exactly one value (`S3_BUCKET = 'opal-data-bd'`), so the
      inline constant with env-var override is functionally identical.
    </requirement>

    <requirement id="2">
      For `merge-daily-incremental.py`: match the AE's S3-deployed fix. Confirm
      the local committed version matches what is currently deployed on S3.
    </requirement>

    <requirement id="3">
      Add a comment to `data/black_diamond/scripts/gold/lib/config.py`:
      ```python
      # NOTE: This module is GOLD-ONLY. Scripts in silver/ and classification/
      # run on a different EC2 instance and MUST NOT import from here.
      # Use: S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')
      ```
    </requirement>

    <requirement id="4">
      Commit all 7 fixes + the config.py comment in a single commit.
      AE will upload the fixed scripts to S3 after DS commits.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero scripts in silver/ or classification/ contain `from lib.config import`</criterion>
    <criterion id="2">All 7 scripts use `os.environ.get('BD_S3_BUCKET', 'opal-data-bd')` for S3_BUCKET</criterion>
    <criterion id="3">lib/config.py has the gold-only warning comment</criterion>
    <criterion id="4">All changes committed on CLOUD branch</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify gold/ scripts -- they correctly use lib.config on the gold runner</constraint>
    <constraint>The env var name MUST be BD_S3_BUCKET with default 'opal-data-bd' -- no other name</constraint>
    <constraint>Do NOT delete lib/config.py -- gold scripts depend on it</constraint>
  </constraints>

  <dependencies>
    None -- this is independent of the S3 restructure TOs.
  </dependencies>

  <deliverables>
    <deliverable type="commit">7 scripts fixed + config.py comment</deliverable>
    <deliverable type="log">Session log listing each file changed with line numbers</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md</ref>
    <ref type="source">data/black_diamond/scripts/gold/lib/config.py</ref>
  </references>
</task_order>
