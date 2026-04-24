<task_order>
  <metadata>
    <id>ADVI_INFLEC.Q8</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- rerouted from ~A per Andrew 2026-04-24 directive (~A inactive; work goes to DS Base) -->
    <date>2026-04-24</date>
    <status>staged</status><!-- GO post-W4.13 AE completion; runs parallel or sequential with W4.14 at ~A discretion. COO fires on Andrew/COO priority call. -->
    <project_code>ADVI_INFLEC</project_code>
    <priority>P2 — silver-QA data-quality investigation; affects NNA attribution accuracy but not pipeline correctness</priority>
    <origin>
      INFLEC PRD §10 Q8 (docs/architecture/ADVI_INFLEC.md:514): "Journal In asymmetry ($58.8M net firm-wide) — investigate as external transfer pattern? OPEN — DS during silver QA. Blocks: W3 / W4 (data-quality flag)."
      Andrew directive 2026-04-24: convert Q8/Q9/Q10 to DS TOs.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md §10 Q8</ref>
    <ref type="data">Orion TRN silver partitions `s3://opal-data-inf/silver/trn/` — journal transaction types</ref>
    <ref type="precedent_concept">Orion TRN type_desc values include "Journal In" / "Journal Out" / "Internal Account Journal In" / etc. (per your W4.7 I_A03 Unit Classification table)</ref>
  </references>

  <objective>
    Investigate $58.8M Journal-In firm-wide net asymmetry in INFLEC silver TRN. Journal transactions should roughly net to zero firm-wide (internal transfers between INFLEC accounts). A non-zero net means either (a) external transfers mislabeled as Journals, or (b) genuine asymmetry from transfers crossing the firm boundary (in from other firms / out to other firms).

    Output: classification of the $58.8M as one of:
    - External transfer pattern (should be reclassified to Contribution/Distribution equivalents)
    - Firm-boundary genuine asymmetry (legitimate; no code change; document)
    - Upstream data-quality bug (Orion TRN miscoding; surface to Inflection for vendor action)
    - Mix (document component breakdown)

    Investigation-only TO — no pipeline code changes unless classification clearly points to a reclassification fix.

    **EXPLICIT SCOPE LOCK:**
    - NO portal changes
    - NO pipeline re-run unless reclassification implemented AND AE 0.6.1 authorizes
    - NO BD script modifications
    - Output IS the decision + optional code patch if reclassification warranted
  </objective>

  <scope>
    <files>
      <file action="investigate">silver/trn partitions (all available) — aggregate Journal-In vs Journal-Out firm-wide + per-account</file>
      <file action="investigate">data/orion/scripts/silver/ — journal type_desc classification logic</file>
      <file action="create">data/orion/diagnostics/INFLEC/journal_in_asymmetry_trace.md — investigation record</file>
      <file action="modify-if-reclassification">data/orion/scripts/silver/*.py OR data/orion/scripts/gold/I_A03.positions_cube.py — reclassify Journal-In → Contribution (or equivalent) IF external pattern confirmed</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="trace-doc">
      `data/orion/diagnostics/INFLEC/journal_in_asymmetry_trace.md` — firm-wide Journal-In sum + Journal-Out sum + net asymmetry figure (confirm $58.8M) + per-account breakdown of top 20 largest Journal-In contributors + classification of each (internal round-trip vs external receive vs ambiguous).
    </deliverable>
    <deliverable id="classification">
      Disposition: external-pattern OR firm-boundary OR upstream-bug OR mix (with component breakdown).
    </deliverable>
    <deliverable id="fix-if-warranted">
      If external-pattern confirmed: minimal reclassification in silver or gold (DS picks layer) reclassifying "Journal In" to Contribution when origin-account is absent from INFLEC accounts_dimension. Forward-emit only; no backfill unless trivially cheap.
    </deliverable>
    <deliverable id="inflection-ask-if-bug">
      If upstream-bug classification: draft one-paragraph Inflection-ask (for Andrew to relay) describing the Orion TRN coding issue + specific examples + ask ("can you correct going forward?").
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Trace doc ships with firm-wide Journal-In/Journal-Out sums + net asymmetry confirmed as ~$58.8M or document any drift from briefing figure.</ac>
    <ac id="2">Per-account top 20 Journal-In contributors enumerated; each classified as internal round-trip / external receive / ambiguous.</ac>
    <ac id="3">Final classification documented with rationale linking back to the 20-sample evidence.</ac>
    <ac id="4">If code-fix: py_compile + ds-commit-gate exit 0; comp-pipescript deployed MATCH on affected script.</ac>
    <ac id="5">If Inflection-ask: one-paragraph draft in session log ready for Andrew relay.</ac>
    <ac id="6">Session log Compiler Tools section + MCP COMPLETE to COO with classification + commit hash (if fix) + next-step (Inflection ask, or accept-as-documented).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>python3 -c "import pyarrow.parquet as pq, pandas as pd; df = pq.read_table('s3://opal-data-inf/silver/trn/').to_pandas(); j = df[df['type_desc'].str.contains('Journal', na=False)]; print(j.groupby('type_desc')['amount'].sum())"</run>
        <expect>Journal-In sum vs Journal-Out sum; confirm net ~$58.8M asymmetry direction + approximate magnitude.</expect>
        <if_mismatch>If net is trivially zero (< $1M), the briefing figure was stale; document + close TO early with "asymmetry resolved post-chain-fresh" finding.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Same df; top 20 Journal-In by magnitude; print account_id + amount + trade_date"</run>
        <expect>20 rows surfaced; use as classification sample.</expect>
        <if_mismatch>If top-20 is <$10M cumulative, $58.8M is spread across long tail — sampling strategy shifts to random 20 + top 5.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="classification">
      <step>
        <run>python3 -c "# Per-account Journal-In counter-join Journal-Out on same day ±7d window for round-trip detection"</run>
        <expect>Per-account round-trip-found / round-trip-missing flag for top-20 sample.</expect>
        <if_mismatch>Document window selection rationale; 7d is heuristic.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Cross-reference top-20 Journal-In account_ids against silver/accounts_dimension — are source accounts in INFLEC universe or external?"</run>
        <expect>Binary per-account: internal (sibling INFLEC account) vs external (no match in accounts_dim).</expect>
        <if_mismatch>If accounts_dim doesn't have source-account linkage field, this phase becomes inference-only (amounts/dates/counter-party name if present).</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit (if fix path)">
      <step>
        <run>python -m py_compile data/orion/scripts/silver/<affected>.py OR data/orion/scripts/gold/I_A03.positions_cube.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh <affected files></run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix AST.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <do_not>
    <rule>Do NOT retroactively reclassify historical Orion data. Forward-only if fix.</rule>
    <rule>Do NOT author an Inflection ask without Andrew review — session log draft only.</rule>
    <rule>Do NOT dispatch full INF chain from this TO unless reclassification is shipped AND AE 0.6.1 authorizes.</rule>
    <rule>Do NOT expand scope beyond Journal-In asymmetry (other TRN anomalies = separate TOs).</rule>
  </do_not>
</task_order>
