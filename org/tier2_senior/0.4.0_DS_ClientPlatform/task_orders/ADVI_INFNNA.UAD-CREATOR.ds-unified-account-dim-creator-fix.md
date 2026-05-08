<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.UAD-CREATOR</id>
    <project>ADVI_INFNNA</project>
    <title>Fix create_unified_account_dim_query.py to clone Billing Dim verbose template (mirrors 4d99a1fb2 fix for tax)</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_to_fallback>0.4.0_DS_ClientPlatform~A</issued_to_fallback>
    <fallback_after>1h post-dispatch with no DS~B pickup</fallback_after>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>medium</priority>
    <estimated_effort>~1h fix + recreate query + verify</estimated_effort>
  </metadata>

  <references>
    <ref type="incident">INFNNA full-backfill 2026-05-07 — pull_unified_account_dim.py /Generate failed 400 'Could not find activity 1'. Same root cause as orion_tax_dim earlier today (commit 4d99a1fb2). The saved query in Orion catalog has empty `additionalOptions` but the schema's contextChange references activity options that need to be defined locally.</ref>
    <ref type="canonical_fix">commit 4d99a1fb2 — create_tax_dim_queries.py fix: load Billing Dim verbose schema, deep-copy, override only what's specific to the new dim. Preserves the full additionalOptions block so /Generate succeeds.</ref>
    <ref type="target_file">data/orion/manual_api/create_unified_account_dim_query.py — currently builds inline schema with `additionalOptions: []`</ref>
    <ref type="downstream_caller">data/orion/manual_api/pull_unified_account_dim.py — reads the saved query from catalog by name and POSTs to /Generate. COO already added `"additionalOptions": verbose.get("additionalOptions") or []` to its build_generate_body() but that fix doesn't help if the saved query's verbose response itself has empty additionalOptions.</ref>
  </references>

  <context>
    The unified_account_dim is one of the 9 Inflection bronze dims. It carries
    rep_id-to-account mapping critical for downstream silvers (especially the
    household_rep_mapping silver). Currently broken: the saved 'Unified Account Dim'
    query in Orion's catalog has empty additionalOptions, causing /Generate to fail 400
    "Could not find activity 1."

    Same bug class as tax dim creator before commit 4d99a1fb2 (Joe-attribution day).
    Fix: rewrite the creator to clone Billing Dim's full verbose schema, deep-copy it,
    and override ONLY what's specific to unified_account_dim (name, columns, costBasisOptionId
    if applicable, INFLECTION_REP_IDS).

    Also note: line 45 of create_unified_account_dim_query.py has
    `INFLECTION_REP_IDS = [3, 11, 12]` — same Joe-missing bug as transactions_v2 had.
    Update to `[3, 6, 11, 12]` while making the creator fix.
  </context>

  <scope>
    <step>
      Read create_tax_dim_queries.py for canonical fix pattern. Specifically:
        - _load_billing_dim_template(jwt) function (lines 173-193)
        - build_query_schema() function (lines 196-221) — clone + override pattern
    </step>
    <step>
      Rewrite create_unified_account_dim_query.py:
        - Add _load_billing_dim_template(jwt) (mirror tax's exactly)
        - Replace the inline schema construction in build_query_schema() (or equivalent function) with: deep copy Billing Dim verbose, then override:
          - name = "Unified Account Dim"
          - portfolio.name + portfolio.description
          - schema.workBook.controls[0].control.groupings[0]:
            - value = "Account" (per existing logic)
            - overallHeader.rows[0].columns = built from UAD_COLUMNS
            - body.rows[0].columns = built from UAD_COLUMNS
          - requiredOptions select-entity entityIds = INFLECTION_REP_IDS
        - Update INFLECTION_REP_IDS = [3, 6, 11, 12]
        - Update docstring comment line 26 if it mentions the old set
    </step>
    <step>
      Pre-commit gate: .tools/ds-commit-gate.sh data/orion/manual_api/create_unified_account_dim_query.py — exit 0.
    </step>
    <step>
      Commit via .tools/safe-commit.sh with --author "0.4.0_DS_ClientPlatform~B &lt;0.4.0_DS_ClientPlatform~B@opal.agent&gt;"
      -m "fix(ADVI_INFNNA.UAD-CREATOR): create_unified_account_dim_query clones Billing Dim verbose template (mirrors 4d99a1fb2 tax fix). Adds rep_id=6 to INFLECTION_REP_IDS."
      -- data/orion/manual_api/create_unified_account_dim_query.py
    </step>
    <step>git push origin CLOUD.</step>
    <step>S3 upload: aws s3 cp create_unified_account_dim_query.py s3://opal-data-inf/code/bronze-runner/manual_api/create_unified_account_dim_query.py</step>
    <step>
      Re-create the 'Unified Account Dim' saved query in Orion catalog:
        python data/orion/manual_api/create_unified_account_dim_query.py --force
      Verify new query id + schema includes additionalOptions.
    </step>
    <step>
      Test pull: python data/orion/manual_api/pull_unified_account_dim.py --upload-bronze
      Verify exit=0 + bronze CSV/JSON written + sample row counts match expected.
    </step>
    <step>
      Run silver build:
        python data/orion/scripts/silver/convert_orion_api_to_silver.py --dim household_rep_mapping --snapshot-date 2026-05-07 --upload
      (household_rep_mapping consumes unified_account_dim)
    </step>
    <step>
      RAVC to COO: commit hash + S3 ETag + new query id + bronze pull row count + silver build success.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-pipescript deployed create_unified_account_dim_query.py — MATCH</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Creator script clones Billing Dim verbose template (deep copy + override pattern), no inline `additionalOptions: []`.</criterion>
    <criterion id="AC2">INFLECTION_REP_IDS = [3, 6, 11, 12] (Joe Brandenburg added).</criterion>
    <criterion id="AC3">--force re-create succeeds; new query id verified in catalog.</criterion>
    <criterion id="AC4">pull_unified_account_dim.py exit=0 + bronze written.</criterion>
    <criterion id="AC5">silver/api_dims/household_rep_mapping/snapshot_date=2026-05-07/data.parquet exists.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent fix.</upstream>
    <downstream>INFNNA.SHAPE-VERIFY uses unified_account_dim silver. INFETL.LAMBDA-DIMS daily Lambda for UAD blocked until creator works.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. DS~B preferred. If session not registered within 1h, fallback to DS~A.</message>
  </go_signal>
</task_order>
