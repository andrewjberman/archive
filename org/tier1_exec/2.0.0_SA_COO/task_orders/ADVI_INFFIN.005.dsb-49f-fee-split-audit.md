<task_order>
  <metadata>
    <id>ADVI_INFFIN.005</id>
    <slug>dsb-49f-fee-split-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — parallel investigation feeding .003 DS~C INF emit shape normalization (Surfaces #6 + #8); audit deliverable + shape inventory; not blocking .003 first ship but feeds normalization round-trip</priority>
    <sla>~2-3h wall; ships standalone audit deliverable; output feeds .003 schema normalization decisions</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief §Surface #6 + §Surface #8 + §Cross-Cutting Theme 2 + §Open Questions #3)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough 2026-05-13 + Andrew verbatim: "DS can look into implementation for 49 as well to try and keep shapes similar" + "Look at 49 Financial ADVI page for reference, we had figured it out mostly for their book"</ref>
    <ref type="cross_link">Sibling: .003 DS~C INF emit batch (consumes this audit shape for INF schema normalization to 49F)</ref>
  </references>

  <context>
    Andrew's directive: cross-firm parity between 49Financial and Inflection partner portals. Surfaces #6 (per-account fee emit + null-elimination) and #8 (fee-paying / no-fee toggle reactivity) are partner-portal-wide product features, not Inflection-isolated. 49F has "mostly figured this out for their book" per Andrew; Inflection should mirror the same emit shape so:

    1. **Schema parity:** 49F + Inflection share field names for per-account fee fields + per-period fee-split parallel fields
    2. **Shared FE accessor:** the FeeSummary panel + AdvisorPublicProfile toggle wiring becomes ONE accessor consumed by both partners (vs separate adapters per partner)
    3. **Future-proof:** new partners inherit the same fee-split schema by default

    DS~B's role: audit 49F's BD-pipeline emit shape — what field names does 49F use? What's the per-period partition pattern? What's the null-elimination state on BD side? Produce shape inventory deliverable that feeds .003 DS~C normalization.

    BD pipeline scripts live at `data/bd/scripts/gold/*.py` (separate from inf-pipeline). DS~B has lane authority for BD-pipeline scripts per general DS routing.

    This is an investigation-deliverable TO (not code ship). Output: brief at `docs/briefs/inffin-49f-fee-split-audit-20260513.md` (or similar) with shape inventory + gap analysis + normalization recommendations for .003 DS~C.
  </context>

  <objective>
    Produce 49F BD-pipeline fee-split emit shape audit deliverable for DS~C INF schema normalization:

    1. Enumerate 49F per-account fee field names + types in BD-pipeline gold emit (advisor book.json equivalent + L3 per-account view)
    2. Enumerate 49F per-period fee-split parallel fields (e.g., does 49F have `aua_fee_paying` + `aua_no_fee`? or different naming?)
    3. Document 49F null-elimination state (does BD pipeline ever emit `null` for fee fields? what sentinel does it use for legitimate absences?)
    4. Document 49F red-flag account handling (does BD have similar structural-absence cases? how surfaced?)
    5. Recommend Inflection schema field names that share with 49F where semantic matches; identify divergences that warrant FE adapter vs upstream rename

    Output: shape inventory + recommendation brief at `docs/briefs/inffin-49f-fee-split-audit-20260513.md` (or similar canonical path).

    No code ship from this TO — investigation + brief authoring only.
  </objective>

  <scope>
    <surfaces>
      <surface id="6">Cross-firm parity informer (per-account fee field naming + null-elimination)</surface>
      <surface id="8">Cross-firm parity informer (fee-paying split parallel fields + Lifetime Activity split bars)</surface>
    </surfaces>
    <files>
      <file action="investigate">data/bd/scripts/gold/*.py — 49F BD-pipeline gold emit scripts; find per-account fee emit + per-period fee-split emit</file>
      <file action="investigate">s3://opal-data-bd/platinum/advisors/{id}/book.json (or equivalent path) — 49F advisor book schema for per-account fields</file>
      <file action="investigate">s3://opal-data-bd/platinum/advisors/{id}/composition.json or summary.json — 49F per-period fee-split fields</file>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_partners/49financial/ — FE accessors consuming 49F shape (FeeSummary panel + AdvisorPublicProfile toggle)</file>
      <file action="output">docs/briefs/inffin-49f-fee-split-audit-20260513.md (or similar) — shape inventory + gap analysis + normalization recommendations</file>
    </files>
  </scope>

  <phase id="1" when="investigation">
    <step>
      <description>Locate 49F BD-pipeline gold scripts emitting per-account fee fields. Likely candidates: `data/bd/scripts/gold/BD_D_*` advisor book builder + L3 per-account JSON emit. `grep -rn "fee_\|is_fee_paying\|fee_structure" data/bd/scripts/gold/ --include="*.py"` to enumerate.</description>
      <expect>Script(s) identified; per-account fee field names + types + null-handling enumerated.</expect>
    </step>
    <step>
      <description>Empirical S3 inspect: pull a sample 49F advisor book.json + composition.json + L3 per-account view. Document field names + types + sample values + null-state.</description>
      <expect>49F shape documented from empirical S3 artifacts.</expect>
    </step>
    <step>
      <description>Locate 49F per-period fee-split fields. Does 49F have `aua_fee_paying / aua_no_fee` parallel emit? Or filterable view? Or different naming (e.g., `fee_earning_aua / non_fee_aua`)?</description>
      <expect>49F per-period fee-split shape documented.</expect>
    </step>
    <step>
      <description>Investigate 49F red-flag account handling. Does BD pipeline emit a `fee_structure` sentinel? What values? How do red-flag accounts surface in 49F book.json?</description>
      <expect>49F red-flag handling pattern documented.</expect>
    </step>
    <step>
      <description>Investigate 49F FE accessor: `portal/src/pages/AdvisorIntelligence/_partners/49financial/FeeSummaryPanel.tsx` (or similar) — what field shape does FE consume? Single source of truth for 49F → identifies the canonical schema FE expects.</description>
      <expect>FE accessor field expectations enumerated; canonical 49F schema identified.</expect>
    </step>
    <step>
      <description>Cross-firm divergence analysis: compare 49F field names + types to current Inflection field names + types (from INF_D_02 + INF_D_05* current state). Categorize each field as:
- IDENTICAL (share name + semantic; reuse 49F name for INF)
- DIVERGENT-NAME-SAME-SEMANTIC (different names, same meaning — recommend INF rename to 49F name)
- DIVERGENT-SEMANTIC (different meanings — fork; document FE adapter requirement)
- 49F-ONLY (49F has, INF doesn't yet — INF adds with 49F name)
- INF-ONLY (INF has, 49F doesn't — propose 49F add via separate TO later)</description>
      <expect>Cross-firm field-by-field categorization complete.</expect>
    </step>
    <step>
      <description>Null-elimination audit: does 49F emit `null` for fee fields anywhere? If yes, document where + recommend fix (likely BD-pipeline cleanup TO follow-on). If no, document the null-elimination discipline that 49F applies (literal 0 vs sentinel pattern).</description>
      <expect>49F null-state documented; deviation from Andrew rule flagged if any.</expect>
    </step>
  </phase>

  <phase id="2" when="brief-authoring">
    <step>
      <description>Author audit brief at `docs/briefs/inffin-49f-fee-split-audit-20260513.md`. Sections:
1. Executive Summary (2-3 paragraph)
2. 49F Per-Account Fee Field Inventory (script + S3 path + field names + types + null-state)
3. 49F Per-Period Fee-Split Field Inventory (script + S3 path + field names + types + sample values)
4. 49F Red-Flag Account Handling (sentinel pattern + structural-condition examples)
5. 49F FE Accessor Shape (canonical schema FE expects)
6. Cross-Firm Field Categorization (IDENTICAL / DIVERGENT-NAME / DIVERGENT-SEMANTIC / 49F-ONLY / INF-ONLY)
7. Normalization Recommendations for DS~C INF schema (specific field names to align; specific renames; specific adapter needs)
8. 49F Null-Elimination State (gaps if any; flag for future BD-pipeline cleanup)
9. Open Questions (anything unclear from audit — for COO/Andrew clarification)</description>
      <expect>Brief shipped; clear actionable recommendations for .003 DS~C.</expect>
    </step>
    <step>
      <description>MCP DS~C with audit brief link + key recommendations summary. Coordinate via COO so DS~C can normalize INF schema in-flight if their .003 ship hasn't completed yet, OR follow-on commit if .003 already shipped with native naming.</description>
      <expect>DS~C aware of recommendations; routing decision logged.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Audit brief shipped at `docs/briefs/inffin-49f-fee-split-audit-20260513.md` with sections 1-9 complete.
    AC2: 49F per-account fee field inventory documented (script + S3 path + field names + types + null-state).
    AC3: 49F per-period fee-split field inventory documented.
    AC4: 49F red-flag account handling pattern documented.
    AC5: 49F FE accessor canonical shape documented.
    AC6: Cross-firm field categorization complete (IDENTICAL / DIVERGENT / 49F-ONLY / INF-ONLY).
    AC7: Normalization recommendations for DS~C INF schema (specific actionable field names + renames).
    AC8: 49F null-elimination state audit (any gaps flagged for future BD-pipeline cleanup).
    AC9: MCP to DS~C with key recommendations + brief link.
    AC10: MCP RAVC2 to COO with brief commit hash + recommendations summary.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>grep enumeration; comp-pipescript io on identified BD scripts; S3 empirical pulls</phase_1>
    <phase_2>brief authoring; no code edits; no ds-commit-gate (markdown only)</phase_2>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    NO UPSTREAM DEPS: independent investigation; ships standalone audit deliverable.

    DOWNSTREAM CONSUMER:
    - .003 DS~C INF emit batch — consumes this audit's normalization recommendations. If .005 ships before .003 first ship, DS~C aligns naming on first emit. If .005 ships after .003 first ship, DS~C does follow-on rename commit.

    BD-PIPELINE OWNERSHIP:
    - This TO is INVESTIGATION ONLY on BD pipeline. No BD code edits. Any BD-pipeline cleanup recommendations (e.g., null-elimination fixes) flagged for future TO authoring; not in scope for this audit.

    NO PORTAL: investigation + brief authoring only.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Investigation-only TO. No code edits, no data emit changes, no chain fires, no Lambda redeploys.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Audit brief at `docs/briefs/inffin-49f-fee-split-audit-20260513.md` (sections 1-9 complete)
    2. Single commit under 0.4.0_DS_ClientPlatform~B author for the brief markdown
    3. MCP to DS~C with key recommendations + brief link
    4. MCP RAVC2 to COO with brief commit hash + recommendations summary
  </deliverables>

  <ravc>
    DS~B RAVC2 to COO post-AC1-10 PASS. COO relays normalization recommendations to DS~C (if .003 still in flight, DS~C aligns; if .003 already shipped, DS~C does follow-on rename commit per recommendations). 49F null-elimination gaps (if any surfaced) → flagged for future TO.
  </ravc>

  <notes>
    **Per Andrew session-scope override:** DS~B explicitly authorized for INFFIN scope (overrides "base DS only" session-scope directive). DS~B's 49F-side audit lane is the natural fit.

    **Investigation discipline:** this is ONE-SHOT audit; no iterative discovery. Surface ONE comprehensive brief with all 9 sections complete. If something is unclear, document in section 9 (Open Questions) rather than half-shipping.

    **Cross-firm parity directive:** Andrew's vision is shared FE accessor across 49F + Inflection. Output of this audit is the canonical schema spec for that shared accessor. .003 DS~C consumes; future partners inherit.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~B <0.4.0_DS_ClientPlatform~B@opal.agent>"` per agent commit identity protocol.

    **Brief output location:** `docs/briefs/inffin-49f-fee-split-audit-20260513.md` is the canonical path. If a different location is preferred (e.g., `docs/audits/`), use your discretion — but link from this TO's RAVC2 message clearly.
  </notes>
</task_order>
