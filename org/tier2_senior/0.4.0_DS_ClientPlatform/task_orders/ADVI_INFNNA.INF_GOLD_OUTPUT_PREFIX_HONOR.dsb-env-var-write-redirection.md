<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.INF_GOLD_OUTPUT_PREFIX_HONOR</id>
    <project>ADVI_INFNNA</project>
    <title>INF gold scripts — read OUTPUT_PREFIX env var so QA runner can write to qa/ prefix without IAM AccessDenied</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>DRAFT-2026-05-11</issued_date>
    <status>staged</status>
    <priority>medium</priority>
    <estimated_effort>~2-3h (cross-cutting refactor across ~30 INF gold scripts + verify on QA runner)</estimated_effort>
    <authorized_by>DRAFT — pending COO ratification per INF_A_03_PARALLEL-EXPAND RAVC4 finding 2026-05-11</authorized_by>
  </metadata>

  <references>
    <ref type="parent_finding">DS~B 2026-05-11 INF_A_03_PARALLEL-EXPAND SSM run — `eef1ff91-328a-41fb-8033-a613e9f4d0bd` AccessDenied on `s3://opal-data-inf/gold/positions_cube/2020-05-26.parquet` from QA runner role</ref>
    <ref type="manifest_dependency">infra/aws/ec2/EC2_MANIFEST.json — services.inf-gold-qa-runner.notes: "DS dependency: gold scripts at data/inf/scripts/gold/*.py need OUTPUT_PREFIX env var honor before QA runs produce qa/ artifacts."</ref>
    <ref type="memory_cross_ref">memory/feedback_ssm_output_prefix_env.md (2026-05-04) — dispatch-side rule "always export OUTPUT_PREFIX=qa/ inline in any SSM dispatch". This TO is the script-side complement.</ref>
    <ref type="affected_scripts">data/orion/scripts/gold/INF_*.py (~30 files); each one hardcodes OUTPUT_PREFIX or equivalent constant</ref>
  </references>

  <context>
    INF gold scripts hardcode their write prefix as a module-level constant (e.g., INF_A_03 uses `OUTPUT_PREFIX = 'gold/positions_cube/'`). The QA runner IAM (`inf-gold-qa-runner-ec2-role`) is scoped to `qa/*` writes only as a defense-in-depth boundary against accidental PROD overwrite. Result: any QA-runner SSM dispatch that doesn't somehow redirect output through OUTPUT_PREFIX env var FAILS on AccessDenied.

    The dispatch side already has the rule (`export OUTPUT_PREFIX=qa/` inline before invoking python). The script side is missing — scripts ignore the env var.

    **Standard pattern to port (per CLAUDE.md feedback memory):**

    ```python
    OUTPUT_PREFIX_BASE = 'gold/positions_cube/'
    _ENV_PREFIX = os.environ.get('OUTPUT_PREFIX', '').strip()
    OUTPUT_PREFIX = f"{_ENV_PREFIX}{OUTPUT_PREFIX_BASE}" if _ENV_PREFIX else OUTPUT_PREFIX_BASE
    ```

    With `OUTPUT_PREFIX=qa/` set: writes go to `qa/gold/positions_cube/{date}.parquet`.
    With no env var (default — PROD runner): writes go to `gold/positions_cube/{date}.parquet`.

    **Cross-cutting nature:** ~30 INF gold scripts (A/B/C/D layers + INF_09) all need the same shape change. This is a bulk-edit refactor + verification cycle, not a per-script TO.

    **Why medium not high:** PROD runs work fine today (PROD IAM allows gold/* writes). Only QA cycle is broken. The blast radius is the QA validation pattern, not data correctness. But QA validation is exactly what AE 0.7.0 + DS workflows depend on for safe deploys, so it's not low.
  </context>

  <scope>
    <step>
      Identify the canonical pattern. Either:
      (a) inline `OUTPUT_PREFIX = os.environ.get('OUTPUT_PREFIX', '') + 'gold/...'` per-script, OR
      (b) shared `lib/output_prefix.py` helper imported by all gold scripts.

      Recommend (b) for consistency + single-point-of-fix if pattern needs evolution. Helper signature:

      ```python
      # lib/output_prefix.py
      import os
      def with_qa_redirect(base_prefix: str) -> str:
          env = os.environ.get('OUTPUT_PREFIX', '').strip()
          return f"{env}{base_prefix}" if env else base_prefix
      ```

      Then per-script:
      ```python
      from output_prefix import with_qa_redirect
      OUTPUT_PREFIX = with_qa_redirect('gold/positions_cube/')
      ```
    </step>

    <step>
      Enumerate all INF gold scripts that write to S3 (likely all ~30, but a few stub/validator scripts may not). Check for:
      - `OUTPUT_PREFIX = ` pattern
      - `OUTPUT_KEY = ` pattern (for single-key writes like A_00, A_01, A_04)
      - Direct `s3.put_object(Key='gold/...')` literal strings without an intermediate constant

      Document via `grep -rEn "(OUTPUT_PREFIX|OUTPUT_KEY|put_object.*Key=).*gold" data/orion/scripts/gold/`
    </step>

    <step>
      Apply the helper import + redirect call to every identified write site. Single bulk-edit commit per script grouping (A-layer / B-layer / C-layer / D-layer / 09).

      Pre-commit gate per script edited.
    </step>

    <step>
      Deploy `lib/output_prefix.py` to S3 + each modified gold script. SHA256 MATCH verify each.
    </step>

    <step>
      Validation cycle on QA runner:
      - Start `inf-gold-qa-runner` (i-04373615f03fbf9a9)
      - SSM dispatch with `--from INF_A_03 --single` (or scoped subset)
      - SSM command must `export OUTPUT_PREFIX=qa/` inline before `bash orion-gold-dispatch.sh ...`
      - Verify writes land at `s3://opal-data-inf/qa/gold/positions_cube/{date}.parquet` (NOT `gold/...`)
      - Verify no AccessDenied
      - Stop EC2
    </step>

    <step>
      Bonus / complementary: extend the dispatch script `orion-gold-dispatch.sh` to optionally include `OUTPUT_PREFIX=qa/` in the env it passes to python3. Currently SSM caller has to set it; if dispatch script knows it's running on a QA-tagged instance (per `Tier=qa` tag visible in user-data.sh), it could auto-set. Out of scope for this TO unless trivial; flag as a follow-up.
    </step>

    <step>
      Documentation update: add a "QA cycle verification" section to wherever the canonical INF deploy pattern lives (likely `docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md` or a new INF-specific doc).
    </step>
  </scope>

  <acceptance_criteria>
    1. `lib/output_prefix.py` (or equivalent helper) authored + deployed.
    2. All INF gold scripts that write to S3 read OUTPUT_PREFIX env var (or use the helper).
    3. Pre-commit gate exits 0 on every edited file.
    4. SHA256 MATCH on every deployed script (manual until INF_COMP_PIPESCRIPT_DEPLOYED_COVERAGE lands).
    5. QA runner SSM cascade with `OUTPUT_PREFIX=qa/` writes to `qa/gold/...` and produces no AccessDenied.
    6. PROD runner SSM cascade (no env var) writes to `gold/...` (unchanged behavior).
    7. Session log captures: helper design + per-script enumeration + QA validation result.
    8. RAVC to COO with QA validation evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>`grep -rEn "(OUTPUT_PREFIX|OUTPUT_KEY|put_object.*Key=).*gold" data/orion/scripts/gold/`</run><expect>Enumerated list of every write site needing the pattern.</expect></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>`.tools/ds-commit-gate.sh` on every .py edited</run><expect>Exit 0 each.</expect></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>QA runner SSM dispatch with `export OUTPUT_PREFIX=qa/`</run><expect>No AccessDenied; outputs land at qa/gold/...</expect></step>
      <step><run>PROD runner SSM dispatch (no OUTPUT_PREFIX) — only if AE 0.7.0 owns this validation</run><expect>Outputs land at gold/... unchanged.</expect></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None code-wise. Loosely dependent on COO routing — runs after current 4-INF_A_* sequence (INF_A_LAYER_TXN-CACHE → INF_A_02_RETIRE → INF_A_03_STALE-PURGE) closes, OR in parallel if COO routes early.

    Cross-references but does not block:
    - `INF_COMP_PIPESCRIPT_DEPLOYED_COVERAGE` (helps verify SHA MATCH automated)
    - `SAFE-DEPLOY-GATE-EXTENSION` (CTO ratified — could fold the QA-write-redirect verify into the same atomic safe-deploy gate)
  </dependencies>

  <next>On ship: QA cycle becomes fully usable for INF gold script validation. Unblocks PARALLEL-EXPAND-class TOs from needing PROD-runner-only validation.</next>

  <draft_note>
    Authored DRAFT by 0.4.0_DS_ClientPlatform~B 2026-05-11 per COO Option A decision on INF_A_03_PARALLEL-EXPAND RAVC4. Awaiting COO ratification + dispatch.
  </draft_note>
</task_order>
