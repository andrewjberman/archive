<task_order>
  <metadata>
    <id>ADVI_INFLEC.Q10</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to><!-- ~A lane per Andrew 2026-04-22 INFLEC DS reassignment -->
    <date>2026-04-24</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- GO post-W4.13 + W4.14 ship; INVESTIGATION-ONLY; lower priority than Q8/Q9 -->
    <project_code>ADVI_INFLEC</project_code>
    <priority>P3 — investigation-only; recommends defer; not blocking platinum LIVE</priority>
    <origin>
      INFLEC PRD §10 Q10 (docs/architecture/ADVI_INFLEC.md:516): "Inflection Fidelity integration — do we need Fidelity API for enrichment (CUSIPs, corporate actions) or is TRN-only sufficient? OPEN — CTO + DS. Blocks: W4 (deferred if TRN-only suffices)."
      Andrew directive 2026-04-24 + COO recommendation: **defer Q10** until a specific gap surfaces (bond pricing, corporate action that TRN doesn't capture). W4.12 PASS shows TRN-only produces $429M platinum LIVE with 9 advisors + 997 clients + 6 timeseries windows — pipeline works.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md §10 Q10</ref>
    <ref type="precedent">W4.12 validation (2026-04-22T22:16:10Z, commit 8cc69bab-ish) — TRN-only gold chain PASS on pipeline correctness</ref>
    <ref type="bd_precedent">BD pipeline uses Yahoo + CUSIP feeds for bond-pricing enrichment — INF needs same coverage eventually</ref>
    <ref type="candidate_gaps">bond-pricing (INF only has what's in Orion TRN nav_price; likely sparse for illiquid bonds), corporate actions (stock splits, mergers, spinoffs — BD uses tiered-cap + canonical-prices v2 architecture), CUSIP-level linkage (INF currently ticker-keyed)</ref>
  </references>

  <objective>
    Assess whether Fidelity API enrichment is needed for INF pipeline correctness OR defer indefinitely. Deliverable: one-page assessment + recommendation.

    Recommended outcome: **DEFER.** W4.12 PASS demonstrates TRN-only is sufficient for platinum LIVE. Revisit when a specific observed gap surfaces (e.g., bond pricing mismatch, corporate-action miss, CUSIP-linkage requirement from a new portal feature).

    Investigation-only — NO Fidelity API integration work in this TO. If recommendation is INTEGRATE, follow-on TO authored for the actual integration work (substantial scope).

    **EXPLICIT SCOPE LOCK:**
    - NO code changes (investigation + recommendation only)
    - NO Fidelity API credentials setup
    - NO BD enrichment pattern replication (out of scope until recommendation approved)
    - Output: assessment doc + recommendation memo for Andrew review
  </objective>

  <scope>
    <files>
      <file action="investigate">data/orion/scripts/gold/*.py — inventory what INF currently derives from TRN only (pricing, corporate actions, CUSIPs)</file>
      <file action="investigate">BD precedent: data/black_diamond/scripts/gold/B_01.holdings_lots.py + backfill_yahoo_prices.py + build_canonical_prices.py — what BD gets from non-TRN sources</file>
      <file action="investigate">platinum/firm/*.json + platinum/advisors/*/*.json — current INF artifacts + what fields would benefit from Fidelity enrichment</file>
      <file action="create">data/orion/diagnostics/INFLEC/fidelity_api_enrichment_assessment.md — assessment record + recommendation</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="gap-inventory">
      Enumerate candidate enrichment gaps: (a) bond-pricing coverage in current INF, (b) corporate-action handling, (c) CUSIP-level linkage usage, (d) other. For each: current-state + Fidelity-delta + business-impact.
    </deliverable>
    <deliverable id="recommendation-memo">
      One-page memo with 3 paths: **DEFER** (status quo; revisit on observed gap), **PILOT** (integrate Fidelity for one specific gap, low-scope), **INTEGRATE** (full Fidelity API integration matching BD pattern, large scope).
      Recommended default: DEFER pending observed gap.
    </deliverable>
    <deliverable id="trigger-criteria">
      Define trigger criteria for revisiting Q10: (a) portal bug class that Fidelity would solve, (b) user-reported data quality issue traceable to TRN-only limit, (c) new INFLEC product feature requiring Fidelity data, (d) cost-of-manual-workaround exceeds integration cost.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Assessment doc ships with gap inventory covering bond-pricing + corporate actions + CUSIP-linkage + other candidates.</ac>
    <ac id="2">3-path recommendation memo written (DEFER / PILOT / INTEGRATE) with default DEFER unless evidence surfaces specific gap.</ac>
    <ac id="3">Trigger criteria defined (at least 4 specific triggers that would reopen Q10).</ac>
    <ac id="4">BD precedent documented: what BD gets from Yahoo + CUSIP feeds that TRN alone does not provide; map to INF-would-benefit items.</ac>
    <ac id="5">W4.12 PASS evidence cited: TRN-only $429M platinum LIVE demonstrates current sufficiency for baseline.</ac>
    <ac id="6">Session log Compiler Tools section (minimal — this is pure investigation).</ac>
    <ac id="7">MCP COMPLETE to COO + CTO with recommendation + memo path for Andrew review.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>comp-pipescript io I_B01 (once shipped via W4.14) OR B_01 (BD precedent)</run>
        <expect>Identify READS for price fields + enrichment sources; map INF's TRN-only vs BD's multi-source.</expect>
        <if_mismatch>If I_B01 not yet shipped (W4.14 pending), use BD B_01 as analog + note in assessment.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "import pyarrow.parquet as pq; df = pq.read_table('s3://opal-data-inf/gold/canonical_prices/<latest>.parquet').to_pandas(); print(df['source'].value_counts() if 'source' in df.columns else 'single-source')"</run>
        <expect>Price-source distribution; identify if INF canonical_prices is already multi-source or single-source.</expect>
        <if_mismatch>Informs whether Fidelity would be an ADDITIONAL source or the SECOND source.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Identify bonds/illiquid tickers in INF holdings; spot-check price coverage; flag any zero-or-stale prices"</run>
        <expect>Coverage ratio per asset_class; flag bond coverage specifically (most common enrichment ask).</expect>
        <if_mismatch>If bond coverage is <50%, that's a specific observed gap worth noting in assessment.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <do_not>
    <rule>Do NOT integrate Fidelity API in this TO. Investigation + recommendation only.</rule>
    <rule>Do NOT request Fidelity credentials or contract terms — that's Andrew scope if PILOT/INTEGRATE path chosen later.</rule>
    <rule>Do NOT expand scope to other vendor enrichment APIs beyond Fidelity (Bloomberg, Morningstar, etc. = separate TOs if ever surfaced).</rule>
    <rule>Do NOT recommend DEFER without explicit trigger-criteria documentation (Acceptance Criterion #3).</rule>
  </do_not>
</task_order>
