<task_order>
  <metadata>
    <id>SSCN_DIVDEF.010-RD</id>
    <slug>factor-bank-group-relabel-color-polish</slug>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.4_RD_SecurityScanner</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <parent_to>org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/SSCN_DIVDEF.010.de-rd-factor-bank-group-ordering.md</parent_to>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct "focus SSCN today". GO is live. Begin immediately. ~15-20min RD wall.</priority>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md -- PRD v0.6 §6.9 TO-8.</prd>
    <re_scope_note>IMPORTANT: this RD TO is the COO-CONFIRMED RE-SCOPE of the parent TO. DE's Phase 1 empirical check found that `utils/categoryOrder.ts` ALREADY encodes the correct 18-group master taxonomy (migrated 2026-03-05; the parent TO's "wrong 11-category" premise was about the registry data, not this portal file -- COO confirmed the re-scope 2026-05-20). So: NO 11->18 change. The actual .010 work is the FactorBankTab relabel + a 4-color separability polish. Implement THIS spec, not the parent TO's categoryOrder.ts 11->18 bullet.</re_scope_note>
  </references>

  <scope>
    Two files, both in your SecurityScanner page dir.

    === FILE 1: tabs/FactorBankTab.tsx -- relabel 3 user-facing "Category" strings to "Group" ===
    AC2 requires NO user-facing "Category" label remains on the Factor Bank tab. Three sites:
    a. The sortable column header (~line 277): `<SortableTh label="Category" col="category" ... />`
       -> change ONLY the `label` prop to "Group". KEEP `col="category"` exactly -- that is the
       internal field name and per PRD v0.6 §D it must NOT be renamed.
    b. The filter dropdown label (~line 117): `<label ...>Category:</label>` -> `Group:`
    c. The filter "all" option text (~line 125): `{c === 'all' ? 'All Categories' : c}`
       -> `'All Groups'`.
    DO NOT touch the filter LOGIC -- `categoryFilter` state, the `categories` useMemo
    auto-derivation, `col="category"`, the `f.category` reads all stay. Label text only.

    === FILE 2: utils/categoryOrder.ts -- 4-color separability polish ===
    DO NOT change CANONICAL_CATEGORY_ORDER membership or order -- it already has the correct
    18 master groups. ONLY re-hue 4 entries in CATEGORY_COLORS.
    Problem: 4 groups cluster in a ~40deg green/teal hue band and are hard to tell apart --
      growth      '145, 70%, 55%'
      solvency    '160, 65%, 52%'
      efficiency  '175, 70%, 55%'
      liquidity   '185, 70%, 55%'
    (volatility '195, 75%, 58%' and management '85, 60%, 58%' sit just outside this band -- be
    aware of them as neighbors; do NOT change them.)
    Re-hue those 4 so all 18 CATEGORY_COLORS are mutually distinguishable on the dark factor
    table. Criteria:
      - Each of the 4 visually separable from the other 3 AND from neighbors volatility(195)
        and management(85): aim for >=25-30deg hue separation, OR clear saturation/lightness
        contrast where hues stay closer.
      - Do not collide with any of the other 14 existing colors (hues in use: 0, 12, 25, 40,
        48, 85, 195, 210, 220, 235, 265, 280, 320, 345 -- plus the 4 you are re-hueing).
      - Keep them legible on the dark bg (lightness ~48-64%, saturation >=55%).
      - growth reading as a green is fine to keep; spread solvency / efficiency / liquidity.
    Propose your 4 new HSL values; DE reviews the rendered result in the /frontend-dev smoke
    screenshot. If the first pass still looks crowded, iterate.
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Factor Bank renders all 18 master groups, each ordered + with a distinct color, no gray fallthrough. (Already true structurally; the 4-color polish makes the green/teal cluster legibly separable.)</ac>
    <ac id="AC2">No user-facing "Category" label remains on the Factor Bank tab -- column header, filter label, and "all" option all read "Group" / "All Groups". Filter logic unchanged.</ac>
    <ac id="AC3">`/frontend-dev` smoke green; `bun run typecheck` clean; `bun run lint` clean. Run typecheck + lint yourself before handing back; paste the transcript in your session log.</ac>
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT change the internal `category` field name or `col="category"` -- PRD v0.6 §D: field stays `category` internally, only the user-facing label changes.</rule>
    <rule>Do NOT change CANONICAL_CATEGORY_ORDER membership or order -- it is already the correct 18 master groups.</rule>
    <rule>Do NOT touch the filter dropdown LOGIC (state / useMemo / auto-derivation) -- label text only.</rule>
    <rule>Do NOT modify the DIVZ preset `group` field, ScannerHeaderPanel.tsx, or any other file. Exactly the 2 files above.</rule>
    <rule>Do NOT commit or push -- hand back to DE 0.3.0 (MCP when done) for compiler mandate + review + commit + RAVC2.</rule>
    <rule>No emojis in code or the session log.</rule>
  </do_not>

  <deliverables>
    - The 2-file change on the portal working tree (DEV branch, uncommitted -- DE commits after review).
    - `bun run typecheck` + `bun run lint` both exit 0; transcript in your session log.
    - Session log under org/tier3_junior/0.3.4_RD_SecurityScanner/logs/2026-05-20/.
    - MCP 0.3.0_DE_TradingOperations when ready: list the files changed, your 4 proposed HSL
      values + 1-line rationale, and your typecheck/lint result.
  </deliverables>

  <handback>
    MCP 0.3.0_DE_TradingOperations with "SSCN_DIVDEF.010 RD implementation ready". DE reviews
    the relabel + the 4 colors (visually, via the /frontend-dev render), runs the compiler
    mandate, commits, and RAVC2s to COO. Do NOT self-flip this TO -- DE closes the loop.
    Note: you are now on the .owned-paths.yaml ANY_POD list (CTO commit 13c6c0d37) -- a FRESH
    session commits your org-side deliverables cleanly without an override; the current
    session may still need it per per-session approval caching.
  </handback>
</task_order>
