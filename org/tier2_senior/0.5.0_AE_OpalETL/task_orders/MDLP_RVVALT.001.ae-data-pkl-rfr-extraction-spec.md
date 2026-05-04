<task_order>
  <metadata>
    <id>MDLP_RVVALT.001</id>
    <project>MDLP_RVVALT</project>
    <title>data.pkl 10Y Treasury RFR extraction spec — author MDLP_RVVALT_RFR_SPEC.md</title>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>complete</status>
    <!-- COO closure 2026-05-04: shipped earlier today — AE 0.5 commits `697e29e7e`+`80250df90` MDLP_RVVALT_RFR_SPEC.md; RAVC4 already exchanged. Status flag was stale per AE session log. Project closed end-to-end via 2c6839707 + c39f14a04. -->

    <priority>P2 — gates TO-3 (Lambda emit); does NOT gate TO-2 (DE stub-driven parallel)</priority>
    <estimated_effort>0.5d (read existing Lambda + sample data.pkl + spec doc)</estimated_effort>
  </metadata>

  <context>
    PRD: `docs/architecture/MDLP_RVVALT.md` (CTO commit `7e520d4bf`). Andrew GO 2026-05-04 option (a) full-dispatch.

    PRD §3 (Compute spec) requires daily 10Y Treasury yield to compute rolling Sharpe. data.pkl (loaded by `yang-model-portfolio-benchmarks` Lambda) carries `return_daily` series including market indices. DS-spec ownership originally suggested in PRD §6 TO-1, but yang-pipeline is your lane (`0.5.0_AE_OpalETL`); routing this TO to you directly avoids a DS round-trip when you have native data.pkl access.

    Output is a small spec doc that AE TO-3 (you again) consumes when extending the Lambda emit. PRD §7.1 risk: 10Y coverage may be shorter than INCEPTION_DATE 2024-04-30 — surface if so.
  </context>

  <objective>
    Identify exact `index_name` in `data.pkl → return_daily` for the 10Y Treasury yield, document its unit (annualized %, daily fraction, or other), and characterize historical coverage relative to INCEPTION_DATE = 2024-04-30. Output: `docs/architecture/MDLP_RVVALT_RFR_SPEC.md`.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>RFR index identification</title>
      <detail>
        Sample data.pkl `return_daily` keys; identify the canonical 10Y Treasury yield series. Likely `"US 10Y Treasury Yield"` or similar — verify the actual index_name string and document. If multiple candidates exist (e.g., 10Y + 10Y-real + on-the-run), pick the one matching `Andrew chose 10Y` directive (nominal yield, on-the-run); document alternatives as backlog.
      </detail>
    </ac>
    <ac id="2">
      <title>Unit characterization</title>
      <detail>
        Sample 10 rows of the 10Y series. Determine unit:
        - **Annualized percent** (e.g., 4.25 means 4.25%): divide by 100 then by 252 for daily decomposition
        - **Annualized fraction** (e.g., 0.0425 means 4.25%): divide by 252 directly
        - **Daily fraction** already decomposed: use as-is

        Document with example: `"unit: annualized %, daily decomposition = value / 100 / 252"`.
      </detail>
    </ac>
    <ac id="3">
      <title>Coverage range</title>
      <detail>
        Identify earliest and latest dates where the 10Y series has non-null values. Compare against INCEPTION_DATE = 2024-04-30:
        - **Coverage ≥ INCEPTION_DATE**: clean — full SI Drawdown supported
        - **Coverage starts after INCEPTION_DATE**: surface gap; document fallback recommendation per PRD §7.1 risk (constant-RFR approximation for missing dates with footer note)
      </detail>
    </ac>
    <ac id="4">
      <title>Spec doc</title>
      <detail>
        Author `docs/architecture/MDLP_RVVALT_RFR_SPEC.md` containing:
        - Index name (verbatim string for AE TO-3 wiring)
        - Unit + decomposition formula
        - Coverage range + gap analysis vs INCEPTION_DATE
        - Sample 10-row data block (date + raw value + decomposed daily fraction)
        - Risk notes (PRD §7.1 if gap exists)

        Commit under your AE 0.5 author. Path lane: `docs/architecture/` requires ANY_CTO override — you'll need `GIT_COMMIT_AUTHOR_OVERRIDE=ANY_CTO` env var on the safe-commit per workflow precedent (e.g., AE 0.5 commit `8595e0c67` ADHC_OWNPTH 48h scan doc used this pattern).
      </detail>
    </ac>
    <ac id="5">
      <title>Session log + RAVC4</title>
      <detail>
        Session log under `org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-04/`. RAVC4 to me with: spec doc commit hash + AE-readable summary of the 3 spec items (index_name + unit + coverage). I then signal TO-3 unblock.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_writing_spec">
      <step>
        <run>grep -rn "return_daily\|US 10Y\|Treasury" infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py</run>
        <expect>Existing references to data.pkl key + index_name patterns; locate where `return_daily` is loaded</expect>
        <if_mismatch>If grep returns nothing, the Lambda may not currently reference 10Y at all — treat as new key entirely; sample data.pkl directly via deployed Lambda console or local pkl read</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>head -3 docs/architecture/MDLP_RVVALT_RFR_SPEC.md</run>
        <expect>Status line + author + date present; spec doc structurally formed</expect>
        <if_mismatch>Add missing fields per PRD authoring conventions</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: pure spec-doc authoring; no data semantics change; no script/Lambda modification.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>`docs/architecture/MDLP_RVVALT_RFR_SPEC.md` (new)</item>
    <item>Session log with Compiler Tools section</item>
    <item>RAVC4 MCP to COO with spec doc commit hash + 3-item summary (index_name + unit + coverage)</item>
  </deliverables>
</task_order>
