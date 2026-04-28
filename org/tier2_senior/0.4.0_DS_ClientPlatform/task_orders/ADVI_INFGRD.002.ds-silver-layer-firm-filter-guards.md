# Task Order: ADVI_INFGRD.002 — DS Phase 1: Silver-Layer Firm Filter + Guards

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-infgrd-002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <completed_date>2026-04-27</completed_date>
    <completed_by>0.4.0_DS_ClientPlatform~A</completed_by>
    <close_summary>
      Shipped in commit 7ecc140a (silver/convert_orion_to_silver.py + gold/D_04.client_portal_summary.py):
      - PARTNER_FIRM_TAGS dict + INFLECTION_ADVISOR_FIRM_TAG constant + INFLECTION_REP_IDS = {3, 11, 12}
      - _advisor_firm(rep_id) helper + _apply_scopefix() rewritten to allowlist-based filter
      - Guard A (raise on missing rep_id col / all-NaN advisor_firm post-derive) IMPLEMENTED in _apply_scopefix
      - Guard B (raise if filtered AUA outside [$50M, $400M] sanity bounds) IMPLEMENTED in _apply_aua_guard,
        called from build_aum_silver
      - Guard C (pre-filter structured per-firm diagnostic — advisor_firm tag x rep_id list breakdown)
        IMPLEMENTED in _apply_scopefix
      - advisor_firm column added to all 3 silver write paths (TRN normalize_trn, AUM normalize_aum,
        accounts_dim build_accounts_dim)
      - D_04 NMEC lifecycle helper (_compute_hh_lifecycle) added — was hardcoded to 0 per RD finding
        2026-04-27; now properly computed (NMNC/NMEC/Existing 3-segment radial_12m + partner_analytics views.aua)
      Gate: ds-commit-gate.sh PASS (py_compile + AST + ruff) for both files.
      INFGRD.003 (AE chain rerun) stays HOLD per Andrew "better solution" direction; superseded by
      ADVI_INFSHIP feeding silver from ORIAPI per CTO 34d2b757 PRD.
      Authority: COO ACK 20260428T0344Z (after RAVC2 ownership flag).
    </close_summary>
    <priority>HIGH — gates .003 (AE chain rerun) and Inflection production sign-off</priority>
  </metadata>

  <objective>
    Implement the silver-layer advisor-scope guard in convert_orion_to_silver.py.
    The current `_apply_scopefix()` bug keeps ALL individual advisors regardless of firm.
    Fix: add `advisor_firm` column derived from the source field identified in .001,
    tighten the predicate to Inflection-only, and add three defensive guards.
    Also generalize the constant structure to support future partner firms (§5.4).
  </objective>

  <scope>
    <file action="modify">data/orion/scripts/silver/convert_orion_to_silver.py</file>
    <file action="modify">docs/architecture/advi_inflec_silver_schema_spec.md</file>

    <task id="1" label="Add advisor_firm column derivation">
      Using the source field confirmed by .001 (e.g., `office`, `firm_name`, etc.):
        - Read the source column in TRN, AUM, SlickGrid CSVs (whichever applies)
        - Derive normalized `advisor_firm` column: lowercase, slug-style
          Example: "Inflection Wealth Management" → "inflection_wealth_management"
        - Match the existing `_advisor_key()` normalization pattern
        - If source field is absent from a given export type, LEFT JOIN to the dimension
          export that carries it (document join key in code comment)

      Add constants at module top:
        PARTNER_FIRM_TAGS = {
            'inflection': 'inflection_wealth_management',
            # Future: 'keil': 'keil_financial_partners', etc.
        }
        INFLECTION_ADVISOR_FIRM_TAG = PARTNER_FIRM_TAGS['inflection']
    </task>

    <task id="2" label="Fix _apply_scopefix() predicate">
      Replace the current bug:
        cohort_mask = firm_mask | indiv_mask  # WRONG -- includes all firms' individuals

      With:
        firm_scope_mask = (
            (df['advisor_firm'] == INFLECTION_ADVISOR_FIRM_TAG)
            | (df['rep_bucket'] == 'firm')  # firm-placeholder rows always in scope
        )
        cohort_mask = firm_scope_mask

      Comment block must include:
        # INFLEC SCOPEFIX-2 / ADVI_INFGRD.002: Inflection-only advisor allowlist
        # TEMP measure until BRONZERUN_V2 upstream filter (ADVI_INFLEC_BRONZERUN_V2 PRD W3.B)
    </task>

    <task id="3" label="Add three defensive guards">
      Immediately after advisor_firm column derivation, before cohort_mask application:

      Guard A — schema regression:
        if 'advisor_firm' not in df.columns:
            raise ValueError("INFGRD: advisor_firm column missing post-derivation -- schema regression")

      Guard B — AUA sanity bounds (runs post-filter):
        filtered_aua = df_filtered['market_value'].sum()  # or equivalent AUA column
        if filtered_aua < 50_000_000 or filtered_aua > 400_000_000:
            raise ValueError(
                f"INFGRD: filtered AUA ${filtered_aua:,.0f} outside expected range "
                f"[$50M, $400M] -- possible multi-firm regression"
            )

      Guard C — diagnostic print (pre-filter visibility, runs BEFORE filter):
        firm_counts = df.groupby('advisor_firm').agg(
            advisor_count=('rep_name', 'nunique'),
            aua=('market_value', 'sum')  # or equivalent
        ).reset_index()
        for _, row in firm_counts.iterrows():
            print(f"INFGRD pre-filter: firm={row['advisor_firm']} "
                  f"advisors={row['advisor_count']} aua=${row['aua']:,.0f}")

      (All print statements use plain ASCII — no emojis, no Unicode above U+007F)
    </task>

    <task id="4" label="Include advisor_firm in silver writes">
      Update the three silver write paths (transactions, aum_snapshot, accounts_dim) to
      include `advisor_firm` in the output dataframes so downstream gold scripts can
      access it if needed.
    </task>

    <task id="5" label="Update silver schema spec">
      In docs/architecture/advi_inflec_silver_schema_spec.md:
        - Add `advisor_firm` column entry: type=string, source=[confirmed field from .001],
          values=[inflection_wealth_management, keil_financial_partners, ...],
          notes="ADVI_INFGRD.002 addition; used by _apply_scopefix() firm filter"
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Pre-commit gate passes: .tools/ds-commit-gate.sh data/orion/scripts/silver/convert_orion_to_silver.py
      (py_compile + ds-precommit-check.py + ruff check --target-version py39 all exit 0)
    </criterion>
    <criterion id="2">
      Guard A fires when advisor_firm column is deliberately absent from a test dataframe.
    </criterion>
    <criterion id="3">
      Guard B fires when a test dataframe with filtered_aua = $30M is passed (below $50M floor).
    </criterion>
    <criterion id="4">
      Guard C prints firm breakdown table before filter runs (visible in SSM logs).
    </criterion>
    <criterion id="5">
      Commit uses --only pathspec (CLAUDE.md Rule 14a). Exactly:
        git add data/orion/scripts/silver/convert_orion_to_silver.py [schema doc if modified]
        git commit --only [same paths] --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"
      No COMP_LEARNS or unrelated files swept.
    </criterion>
    <criterion id="6">
      from __future__ import annotations remains first import (CLAUDE.md Rule 15).
    </criterion>
    <criterion id="7">
      RAVC sent to 2.0.0_SA_COO + 0.6.1_AE_PartnerETL with commit hash. Subject:
      RAVC — ADVI_INFGRD.002 COMPLETE | silver guard committed [hash]
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Fail-closed (raise ValueError) on all three guards — not fail-warn. Per
    ADVI_INFGRD PRD §5.3 recommendation and existing SCOPEFIX pattern.</constraint>
    <constraint>No emojis in code, logs, or print statements (CloudWatch ASCII rule).</constraint>
    <constraint>from __future__ import annotations must be first import.</constraint>
    <constraint>Do NOT run the silver rebuild yourself — that is .003 (AE 0.6.1 scope).
    Deliver the commit and send RAVC to AE.</constraint>
    <constraint>Constants must be extractable for future partner generalization — use
    PARTNER_FIRM_TAGS dict structure even if only one partner is wired now.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_INFGRD.001"
                status="open"
                note="Phase 0 audit must confirm: (a) exact source field name, (b) normalized
                value for Inflection tag, (c) Andrew advisor-list confirm. All three required
                before writing the filter. Do not begin .002 until .001 RAVC received."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">convert_orion_to_silver.py — advisor_firm column + tightened
    _apply_scopefix() predicate + three guards. Silver schema spec updated.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO + 0.6.1_AE_PartnerETL with commit hash.
    This is the go-signal for AE .003.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRD.md §3 + §5</ref>
    <ref type="prior_fix">SCOPEFIX-1 in convert_orion_to_silver.py:105-144 (_apply_scopefix)</ref>
    <ref type="gate">ADVI_INFGRD.001 — Phase 0 audit output</ref>
  </references>
</task_order>
```
