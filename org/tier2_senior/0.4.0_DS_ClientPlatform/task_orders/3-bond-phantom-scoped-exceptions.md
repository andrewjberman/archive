<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-3-bond-scoped-exceptions</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status><!-- GO sent 2026-04-14T19:10Z; DS flips to pending on receipt -->
    <project_code>ad-hoc</project_code>
    <priority>URGENT — must land before Yahoo's next run</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (Tactical Fix section)</ref>
    <ref type="directive">Andrew 2026-04-14 — CUSIP-keyed scoped-exceptions blocklist, not ticker re-route</ref>
  </references>

  <objective>
    Add a persistent CUSIP-keyed scoped-exceptions blocklist that force-overrides canonical
    prices for the 3 phantom bonds (BNP, WFC, NEWMONT). Prevents Yahoo from silently
    re-breaking these tomorrow. This is a BLOCK ("never-Yahoo for this CUSIP"), not a
    re-route — orthogonal to ticker_overrides.json.
  </objective>

  <scope>
    <file>data/black_diamond/scripts/silver/scoped_price_exceptions.json (new)</file>
    <file>data/black_diamond/scripts/silver/inject_scoped_overrides.py (update to consume blocklist)</file>
    <seed_entries>
      - BNP: CUSIP 05613L3H2, force_source='bd_txn_price'
      - WFC 4.15% 2029: CUSIP TBD (DS resolves from silver/fees before writing)
      - NEWMONT 2.8% 2029: CUSIP TBD (DS resolves from silver/fees before writing)
    </seed_entries>
  </scope>

  <acceptance_criteria>
    1. `scoped_price_exceptions.json` committed with all 3 CUSIPs verified correct
    2. `inject_scoped_overrides.py` consumes the blocklist; hard-overrides canonical prices output for listed CUSIPs
    3. Next daily canonical prices run shows all 3 CUSIPs with non-yahoo price_source
    4. 49F AUA drops ~$24.3M on next run (expected forward correction)
    5. MCP COMPLETE to COO with commit hash + S3 artifact + next-run AUA delta once observed
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io inject_scoped_overrides.py`; `comp-pipescript consumers canonical_prices` (enumerate downstream readers so we know what to validate after the override lands — added 2026-04-14 per CTO audit).
    Phase 2: `python -m py_compile inject_scoped_overrides.py`.
    Phase 3: `comp-pipescript deployed inject_scoped_overrides.py` — MATCH.
  </compiler_tools_mandate>

  <longevity>
    This file lives forever. BDPL_CNPRCS WP-6 later absorbs the blocklist into the
    append-only classification ledger as rows with source='custodial_override'.
    Until then, this JSON is the durable guard.
  </longevity>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
