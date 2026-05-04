<task_order>
  <metadata>
    <id>ADVI_INFLEC.S7SUMFIX</id>
    <project>ADVI_INFLEC</project>
    <title>INF_D_04 advisor summary.json emit — port BD D_04 build_advisor_summaries() pattern to Inflection</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>complete</status>
    <priority>P1 — unblocks S7 books-l4 account modal PROD smoke (Inflection)</priority>
    <estimated_effort>0.5d (port existing BD pattern; mirror schema; one script edit + S3 verify)</estimated_effort>
  </metadata>

  <context>
    DE 0.4.0 Wave D V1 smoke re-validation 2026-05-04 (RAVC4 13:15Z) found:

    **S7 books-l4 DATA-GATE:** L3 advisor drilldown opens (Peter Lee panel renders) but book data
    fails — `404 Not Found platinum/advisors/peter_lee/summary.json does not exist in s3://opal-data-inf`.

    Only `book.json` + `composition.json` + `top_holdings.json` are published for Inflection
    advisors. `summary.json` (consumed by `getPlatinumAdvisorSummary` → `getAdvisorBook` endpoint)
    is missing from the Inflection platinum emit.

    **BD has it:** `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:534`
    `build_advisor_summaries()` reads from D_02 + D_03 outputs (book/mix/composition/timeseries)
    and writes `platinum/advisors/{aid}/summary.json` (~20 files). BD has shipped this pattern
    since the original ADVI_PROFIL portal sweep.

    **INF doesn't:** `data/orion/scripts/gold/INF_D_04.client_portal_summary.py` (94KB) — grep for
    "summary.json" returns only references to BOOK output (line 14), no advisor summary emit logic.

    Andrew GO 2026-05-04: routing option (a) — author TO + dispatch to DS~A (Inflection lane
    historical context). Re-engagement from standing-down state.
  </context>

  <objective>
    Port the BD `build_advisor_summaries()` pattern to `INF_D_04.client_portal_summary.py` so it
    emits `platinum/advisors/{advisor_key}/summary.json` for every Inflection advisor (Peter Lee,
    Patrick Scanlan, Inflection Wealth Management firm-stub, etc.).
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>INF_D_04 publishes advisor summary.json</title>
      <detail>
        Port `build_advisor_summaries(upload)` function from `data/black_diamond/scripts/gold/D_04.client_portal_summary.py:530+` to `data/orion/scripts/gold/INF_D_04.client_portal_summary.py`.

        - Read INF-equivalent inputs (INF_D_02 book.json + INF_I_D03 composition outputs + INF_D_03 mix if present) — match the source pattern, naming-substitute INF_-prefixed scripts where needed
        - Build summary structure mirroring BD output schema (DE/RD consume same shape via shared `getPlatinumAdvisorSummary` endpoint — schema MUST match)
        - Write to `s3://opal-data-inf/platinum/advisors/{advisor_key}/summary.json`
        - Hook into INF_D_04's main() build sequence + register as Step (probably Step 3 mirroring BD's labeling)
        - Match BD's stale-cleanup logic (delete orphan summary.json for advisors no longer present)
      </detail>
    </ac>
    <ac id="2">
      <title>Schema parity with BD summary.json</title>
      <detail>
        Output JSON schema MUST match BD's `platinum/advisors/{aid}/summary.json` structurally so the FE consumer (`getAdvisorBook` endpoint via `getPlatinumAdvisorSummary`) reads identical shapes for both firms. Spot-check: pull a BD advisor summary.json from `s3://opal-data-bd/platinum/advisors/{any_aid}/summary.json`, schema-diff against your INF emit. Document deltas in session log.

        Inflection-specific fields that don't apply (e.g., BD-specific fee tiers): document as `null` or omit per existing INF_D_04 conventions; do NOT invent placeholder data.
      </detail>
    </ac>
    <ac id="3">
      <title>Bell-curve distribution data (BD parity)</title>
      <detail>
        BD's `build_advisor_summaries` includes per-advisor account-AUA bell-curve distribution
        prep (`advisor_aua_by_name` from ACCOUNT_PERFORMANCE + ACCOUNT_TEAM). Port the equivalent
        for Inflection — read `gold/timeseries/account_performance` + `gold/views/account_team`
        from the Inflection bucket. If Inflection lacks one of these inputs, emit empty
        distribution block with WARN log (not fatal).
      </detail>
    </ac>
    <ac id="4">
      <title>S3 verification</title>
      <detail>
        After dispatch, verify S3 contents:
        - `aws s3 ls s3://opal-data-inf/platinum/advisors/peter_lee/summary.json` returns object
        - `aws s3 ls s3://opal-data-inf/platinum/advisors/patrick_scanlan/summary.json` returns object
        - `aws s3 ls s3://opal-data-inf/platinum/advisors/inflection-wealth-management/summary.json` (or whatever the IWM firm-stub key is) returns object
        - File counts match advisor count (~3-9 advisors per the Inflection roster)

        Capture `aws s3 ls` output in session log.
      </detail>
    </ac>
    <ac id="5">
      <title>FE smoke unblock — DE re-runs S7</title>
      <detail>
        After dispatch, MCP DE 0.4.0 to re-run S7 books-l4 smoke. Expected: account modal loads
        for Peter Lee with summary panel populated (no more 404). If DE confirms PASS, this AC
        closes; if DE finds residual issues (schema mismatch, missing field), iterate before
        marking complete.
      </detail>
    </ac>
    <ac id="6">
      <title>Session log + RAVC4</title>
      <detail>
        Session log under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-04/`. Compiler
        Tools section reproduces every `<run>` in mandate. RAVC4 to me with: INF_D_04 commit hash
        + S3 sample paths + DE smoke confirm.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_writing_code">
      <step>
        <run>comp-pipescript io INF_D_04</run>
        <expect>Lists current INF_D_04 reads + writes; identifies gap (no `platinum/advisors/.../summary.json` writes today)</expect>
        <if_mismatch>If INF_D_04 already emits summary.json, surface to COO before authoring duplicate code</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_04</run>
        <expect>BD reference; line ~722 confirms `platinum/advisors/{*}/summary.json` HARDCODED write</expect>
        <if_mismatch>If BD pattern has shifted since this TO authored, update port logic to match current BD reference</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse platinum/advisors/peter_lee/summary.json</run>
        <expect>FE consumer enumeration — confirms `getPlatinumAdvisorSummary` / `getAdvisorBook` is the consumer (matches DE finding)</expect>
        <if_mismatch>Multiple consumers OK; document all in session log</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_04.client_portal_summary.py</run>
        <expect>py_compile + ds-precommit-check + ruff all exit 0</expect>
        <if_mismatch>Fix per CLAUDE.md Rule 14 — do NOT bypass</if_mismatch>
      </step>
      <step>
        <run>head -1 data/orion/scripts/gold/INF_D_04.client_portal_summary.py</run>
        <expect>`from __future__ import annotations` present (CLAUDE.md Rule 15)</expect>
        <if_mismatch>Add the import as first import statement</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after_commit">
      <step>
        <run>aws s3 cp data/orion/scripts/gold/INF_D_04.client_portal_summary.py s3://opal-data-inf/code/gold/INF_D_04.client_portal_summary.py</run>
        <expect>S3 upload success (DS-owned upload per CLAUDE.md Rule 13)</expect>
        <if_mismatch>Investigate IAM or credentials</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed INF_D_04</run>
        <expect>MATCH on inf-gold-runner</expect>
        <if_mismatch>STALE = re-upload; investigate divergence</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-inf/platinum/advisors/ --recursive | grep summary.json</run>
        <expect>One summary.json per advisor after gold run; counts match advisor roster</expect>
        <if_mismatch>Run failed or skipped emit; check INF_D_04 logs</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <resource>
      <path>data/orion/scripts/gold/INF_D_04.client_portal_summary.py</path>
      <owners>0.4.0_DS_ClientPlatform~A (this TO); no concurrent active TO touches INF_D_04</owners>
      <coordination>None — sole-owner edit window. DS~D on HISTBF.004 silver backfill (different scripts); DS~B on 49FRECN.003 D_04 (BD-side, different pipeline); DS~C on 49FRECN E_25.</coordination>
    </resource>
    <resource>
      <path>s3://opal-data-inf/platinum/advisors/{advisor_key}/summary.json</path>
      <owners>DS~A (this TO produces); DE 0.4.0 consumes via `getAdvisorBook` Lambda endpoint</owners>
      <coordination>Schema MUST match BD `platinum/advisors/{aid}/summary.json` for FE shape parity. DE will re-run S7 smoke post-ship (AC#5).</coordination>
    </resource>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: gold-tier emit addition; downstream FE reads latest snapshot only. No silver/bronze
      changes. Historical data semantically unchanged. Forward-only emit.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>INF_D_04 commit (DS~A author; POD4 lane) with build_advisor_summaries() port</item>
    <item>S3 upload to s3://opal-data-inf/code/gold/ + comp-pipescript deployed MATCH</item>
    <item>Inflection gold run dispatch (via AE 0.6.1 if dispatch lane needed; small script run can be ad-hoc on inf-gold-qa-runner)</item>
    <item>S3 verification: 3+ summary.json files at platinum/advisors/{id}/ listed</item>
    <item>DE 0.4.0 S7 smoke re-run PASS confirmation (MCP exchange)</item>
    <item>Session log with Compiler Tools section + schema-diff vs BD reference + S3 sample paths</item>
    <item>RAVC4 MCP to COO with commit hash + S3 paths + DE smoke confirm</item>
  </deliverables>
</task_order>
