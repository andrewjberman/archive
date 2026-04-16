<task_order>
  <metadata>
    <id>ADVI_FNTEND.B3.fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- ~B shipped 2026-04-15 22:53Z. D_02 L358: added 'relationship_id' to _load_account_team column list (root-cause patch, latent since 2026-04-09 8ff74fdb9). L2272: replaced single-conditional silent-skip with two-branch WARN-LOUD ERROR log — future schema drift will fire CloudWatch-visible ERROR instead of silently emptying team_attribution. ~A RCA f49aa9bd confirmed account_team.parquet has relationship_id 100% populated; defect was this loader. py_compile PASS. Scope expansion per COO 00:17Z acknowledged. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A (followup, defense-in-depth)</wave>
    <priority>P2 (correctness-lie prevention; gates B3 final close alongside C07-T1)</priority>
  </metadata>

  <references>
    <ref type="parent">ADVI_FNTEND.B3.ds-fee-summary-team-attribution (HOLD pending this fix + C07-T1)</ref>
    <ref type="trigger">CTO ruling 2026-04-15 22:28Z "Silent team_attribution=[] is indistinguishable from no team attribution — correctness lie to consumers"</ref>
    <ref type="related_rca">ADVI_ROLLUP.C07-T1 (root cause of account_team unavailable post-rerun)</ref>
  </references>

  <objective>
    Replace D_02 L2272-2296 silent-skip with **WARN-LOUD** when `account_team` is unavailable (None / empty / missing relationship_id). Silent empty arrays lie to consumers ("no team attribution exists") when the real answer is "data source unavailable."

    **Changes:**
    1. CloudWatch metric emission: `D02TeamAttributionDegraded` increment on every skip.
    2. Log ERROR level with structured payload: `{"event": "team_attribution_degraded", "reason": "account_team_none|empty|missing_column", "advisor_id": "...", "clients_affected": N}`.
    3. Keep runtime behavior: still emit `team_attribution = []` for the client (don't break consumers) BUT surface the degradation.
    4. Optional: add a sentinel value to the artifact like `team_attribution_status: "degraded"` so FE can differentiate "no team" from "data unavailable". Decide this in path-choice (see below).

    **Path choice within TO:**
    - **Path (a):** Add sentinel field `team_attribution_status: "ok" | "degraded"` to schema. FE can show a banner on degraded. Coord with DE.
    - **Path (b):** Emit-side signals only (CloudWatch + logs). FE shape unchanged. Degradation invisible to FE but observable to oncall.

    Recommend path (b) for v1 (minimum-surface change); path (a) is a larger FE contract change worth a dedicated TO if/when product wants user-visible messaging.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py (L2272-2296)</file>
    </files>
  </scope>

  <wire_contract>
    D_02 emits CloudWatch metric + ERROR log when account_team unavailable. Runtime-shape of `team_attribution` unchanged (still empty array). Path (a) adds `team_attribution_status` field.
  </wire_contract>

  <acceptance_criteria>
    1. CloudWatch metric `D02TeamAttributionDegraded` emitted on every skip path.
    2. ERROR log with structured payload visible in CW log group.
    3. Synthetic test: artificially set `account_team = None` before invoking D_02; verify metric increments + log appears.
    4. Path decision (a vs b) documented in commit body.
    5. py_compile clean.
    6. Rule 7 pre-flag before S3 upload.
    7. Parent B3 TO flipped complete AFTER both B3.fix (this) AND C07-T1 root-cause resolution.
    8. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    9. MCP COMPLETE to COO + CTO with commit hash + synthetic test transcript + CW metric/log sample.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>sed -n '2265,2300p' data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>L2272-2296 silent-skip block visible.</expect>
        <if_mismatch>Re-baseline line refs.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service D_02 (or bd-gold-layer-runner role) | grep -i cloudwatch</run>
        <expect>`cloudwatch:PutMetricData` present on runner role.</expect>
        <if_mismatch>Need IAM addition (AE coord). Small scope — flag if missing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>{D_02 synthetic test — force account_team=None, invoke team_attribution block, capture stdout/stderr + mock CW metric call}</run>
        <expect>ERROR log emitted + mock CW metric call observed; empty array still returned for runtime compat.</expect>
        <if_mismatch>Patch logic.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency description="No hard gate — defense-in-depth parallel with C07-T1" status="none"/>
  </dependencies>
</task_order>
