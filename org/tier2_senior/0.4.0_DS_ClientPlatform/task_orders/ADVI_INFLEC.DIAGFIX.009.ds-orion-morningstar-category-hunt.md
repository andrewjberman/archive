<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.009</id>
    <project>ADVI_INFLEC</project>
    <title>Hunt Orion Morningstar Category endpoint — HAR-assisted second-pass investigation (Andrew-coordinated)</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>2-4h (HAR-dependent)</estimated_effort>
  </metadata>

  <references>
    <ref type="evidence_andrew_provided">Orion UI snapshot for Inflection (2026-04-29): Large Blend $38.85M / Intermediate Core Bond $15.17M / Intermediate Core-Plus Bond $13.51M / Foreign Large Growth $11.29M / Diversified Emerging Mkts $11.19M / Mid-Cap Blend $10.71M / Nontraditional Bond $10.14M / Money Market-Taxable $9.87M / Foreign Large Value $9.78M / Other $52.03M. Sum = $182.55M (matches aum_snapshot exactly).</ref>
    <ref type="prior_investigation">DIAGFIX.008 STEP 0 RAVC (DS 20260429T212825Z) — searched 130+ paths in PATH_DISCOVERY.md, Asset.AssetClass + Asset.AssetCategory both FAIL. "Asset class / category" listed as #1 outstanding vendor research gap.</ref>
    <ref type="regex_v1_baseline">firm_composition.json post-17:21Z re-run wave: equity 70.29% / fixed_income 15.22% / cash 12.70% / alternatives 1.79%. Materially diverges from Orion truth (44.8% / 21.3% / 5.4% / 28.5%) — regex defaults bond ETFs (HTRB, BAGIX, BSIIX) to equity AND misses the entire 28% "Other" alternatives bucket.</ref>
    <ref type="bd_path_blocked">bd-securities DDB access nixed by Andrew per session 47 (regex-fallback only for INF). This investigation pursues an INF-native classification source instead.</ref>
  </references>

  <context>
    DIAGFIX.008 STEP 0 concluded "Orion API has no native asset classification" based on 130+
    probed paths. Andrew has now provided Orion UI evidence showing the data clearly DOES
    exist within Orion — specifically Morningstar Category-style names ("Large Blend",
    "Intermediate Core Bond", "Diversified Emerging Mkts", etc.) with full $182.55M coverage.

    The first-pass investigation searched generic terms (asset_class, asset_type,
    security_type, broad_category, style_box). The terms Andrew's UI is rendering are
    Morningstar nomenclature — DS likely missed the right field name. Target keywords for
    a second pass:

      MstarCategory, MorningstarCategory, MorningstarCategoryName, MstarCategoryName,
      Category (without the asset_ prefix), Style, MstarStyle, MorningstarRating,
      Snapshot.Category, Holding.Category, Position.Category, Insights, MstarSecurityID

    Andrew has offered to coordinate directly:
      1. Record HAR files from his Orion UI session showing the asset-class breakdown render.
      2. Hand HAR files to DS so the actual API calls + URL paths + headers are visible.
      3. DS reverse-engineers the request and reproduces it via the manual_api harness.

    This is the surest path. If we can capture the exact request the Orion UI fires for the
    asset-class breakdown, we have the endpoint. Otherwise, DS searches with the refined
    Morningstar-specific keywords.
  </context>

  <scope>
    STEP 1 — Refined keyword pass (do this first, in parallel with HAR coordination):
    Probe data/orion/manual_api/ + Orion API docs/Postman/SDK with the keyword list above
    (Morningstar-specific). Specifically check:
      - Holdings / Positions endpoints for Category, MstarCategory, Style fields
      - Snapshot endpoints (often where pre-aggregated insights live)
      - Insights / Analytics endpoints
      - Securities master / Asset master with Morningstar enrichment
      - Any DataView / query / report endpoint that returns Position-level data with category
    Test each candidate path with the same harness used in PATH_DISCOVERY.md. Document each
    hit/fail in a new PATH_DISCOVERY_MSTAR.md (or appended to existing).

    STEP 2 — HAR file analysis (Andrew-coordinated):
    Andrew will record one or more HAR files from Orion UI sessions that render the asset
    class breakdown for Inflection. Coordinate with Andrew on:
      - Which UI page he should record on (one that shows the same breakdown he provided —
        likely a holdings detail / firm summary / portfolio overview).
      - Drop location for HAR files (suggest data/orion/manual_api/har/ — gitignore the dir).
      - Andrew should redact session tokens / cookies before sharing if the workspace is
        committed; or DS works with the HAR files locally only and never commits raw HAR.

    From HAR, extract:
      - The exact URL path that returns the asset-class breakdown data.
      - The query parameters and request body shape.
      - The response JSON structure — specifically where the Morningstar Category name lives
        and at what granularity (per-position? per-account? aggregated?).

    Reproduce the request via the manual_api harness using DS's existing Orion API client.

    STEP 3 — Coverage + sample test:
    If a viable endpoint is found:
      - Pull asset class data for all Inflection holdings.
      - Verify the per-class sums match Andrew's screenshot ($38.85M Large Blend, etc.).
      - Document field name, schema, distinct values, coverage %, pull cost (request count,
        pagination, rate limits).
      - Map the Morningstar categories into our 4-bucket schema (equity / fixed_income /
        cash / alternatives) — the bucket mapping I've already drafted is below as starting
        reference, refine as needed:
          Equity: Large Blend, Mid-Cap Blend, Foreign Large Growth, Foreign Large Value,
                  Diversified Emerging Mkts, plus all other *Blend, *Growth, *Value variants
          Fixed Income: Intermediate Core Bond, Intermediate Core-Plus Bond, Nontraditional Bond,
                        plus all other *Bond, *Income, *Credit variants
          Cash: Money Market-Taxable, Money Market-Tax-Free, Cash
          Alternatives: REIT, Commodity, Multi-Asset, Target-Date, Allocation*, plus the
                        residual "Other" bucket from the Orion UI breakdown

    STEP 4 — VERDICT to COO:
      VERDICT A — endpoint found, coverage 100%, schema documented. RECOMMEND replacing
        regex classifier in INF_I_D03 with Orion-native source. COO routes follow-on TO.
      VERDICT B — endpoint found but partial coverage (e.g., < 80%). Document gap.
        Hybrid approach: Orion-native where available + regex for residual.
      VERDICT C — no endpoint discoverable even with HAR. Document conclusively. Accept
        regex V1 with documented caveats. Pursue vendor research per Orion's outstanding
        gaps list as a separate long-term task.

    NOTE: DIAGFIX.008 composer (INF_I_D02d.firm_mix_summary.py) proceeds in parallel. The
    composer reshapes whatever firm_composition.json contains. If this investigation lands
    VERDICT A and INF_I_D03 is later refactored to Orion-native, the composer picks up
    the corrected classifications automatically with NO change. Build the composer now.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="N/A — investigation only">
      <step>
        <run>N/A — this TO is read-only API exploration. No gold script writes.</run>
        <expect>Absence acknowledged.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      PATH_DISCOVERY_MSTAR.md (or appended section) documents every Morningstar-keyword
      path probed with hit/fail status.
      Evidence: file in data/orion/manual_api/ committed.
    </criterion>
    <criterion id="2">
      If HAR analysis is performed: HAR file findings documented (URL, query, response shape).
      HAR files NOT committed (treated as local-only artifacts).
      Evidence: notes in session log.
    </criterion>
    <criterion id="3">
      VERDICT A/B/C reported to COO with evidence. If A: endpoint name, schema, coverage %,
      sample sums matching Andrew's screenshot.
    </criterion>
    <criterion id="4">
      No commit needed for the investigation itself (read-only). Session log entry +
      RAVC to COO suffices.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="Andrew" status="active">
      HAR file recording on the Orion UI showing the asset-class breakdown. DS coordinates
      with Andrew directly on timing. STEP 1 (refined keyword pass) can proceed before
      HAR files are received — start there, layer in HAR findings as they arrive.
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" status="in_progress">
      DIAGFIX.008 composer build (INF_I_D02d.firm_mix_summary.py) proceeds in parallel.
      Does NOT block on this investigation. Composer ships V1 against current
      firm_composition.json regardless of investigation outcome.
    </dependency>
    Independent of DIAGFIX.002b/007 EC2 dispatch wave (AE 0.6.1 work).
  </dependencies>

  <cross_domain_coordination>
    <coordination>
      Andrew provides HAR files. DS reverse-engineers and reports.
      If VERDICT A lands, COO routes follow-on TO to refactor INF_I_D03's classifier
      to call the Orion-native endpoint instead of the keyword regex. That follow-on
      TO will be DIAGFIX.010 (or appropriate naming).
    </coordination>
  </cross_domain_coordination>

  <commit_identity>
    No script commit needed for the investigation itself.
    PATH_DISCOVERY_MSTAR.md commit (if created):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_A &lt;0.4.0_DS_ClientPlatform_A@opal.agent&gt;" \
      -m "docs(ADVI_INFLEC.DIAGFIX.009): Morningstar Category endpoint hunt — second-pass paths" \
      -- data/orion/manual_api/PATH_DISCOVERY_MSTAR.md
  </commit_identity>
</task_order>
