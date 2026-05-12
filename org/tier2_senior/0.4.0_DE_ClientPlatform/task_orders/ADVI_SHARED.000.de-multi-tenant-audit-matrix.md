<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_SHARED.000</id>
    <project>ADVI_SHARED</project>
    <title>Phase 0 — comprehensive multi-tenant audit matrix at docs/architecture/ADVI_SHARED_AUDIT.md</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-12</issued_date>
    <status>pending</status>
    <priority>P0 — Phase 1 critical-path upstream</priority>
    <estimated_effort>~1d</estimated_effort>
    <dispatch_held>false</dispatch_held>
    <dispatch_note>Independent of Andrew's pending Q2 (asset class taxonomy authority) and Q5 (sequencing) decisions — audit is pure read-and-document work. Phase 1 TOs (SHARED.001-.008) authoring waits on Q5 sequencing ratification + Q2 if applicable. DE 0.4 can start immediately.</dispatch_note>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §4.1 (Phase 0 audit) + §2 (Current State Audit) + §3 (Target Architecture)</ref>
    <ref type="project">org/projects/ADVI_SHARED.json</ref>
    <ref type="prd_source_brief">org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/briefs/ADVI_SHARED_brief_to_cto.md (DT 0.4 commit cd0847d1d)</ref>
    <ref type="prd_compiler_evidence">PRD §5 — 4 cache-key collisions empirically surfaced; 22 inline isInflectionFirm sites; 4-layer firmId namespace</ref>
    <ref type="parent_project">ADVI_INFLEC (sibling), ADVI_FIRMSEP (Phase 4 .11 model_portfolios may interact)</ref>
  </references>

  <context>
    The PRD identifies the AdvisorIntelligence portal as half-migrated to the `useTenantLayout(firmId) → TenantLayoutConfig` primitive: 4 call-sites adopted, 3 files (PartnerAnalytics 15 + AdvisorBookView 5 + ClientsTab 5) still carrying inline `firmId === ...` / `isInflectionFirm` branches. 102 architectural lint warnings cluster around (a) Category A — react-refresh/only-export-components (~75 warnings from co-located helpers in component files) and (b) Category B — react-hooks/static-components (~12 warnings from inner components rendered inside parent component bodies). 4 cache-key collisions surfaced empirically via `comp-cache collisions` showing `firmOverride='inf'` vs `firmOverride='inflection'` hash divergence on shared React Query keys.

    Phase 0 produces the migration matrix that Phase 1 TOs (SHARED.001 type extension → .008 DEV smoke gate) reference verbatim. Without this matrix, Phase 1 authoring degenerates into per-TO discovery work and risks missing cross-cutting touch sites.
  </context>

  <objective>
    Produce `docs/architecture/ADVI_SHARED_AUDIT.md` — a comprehensive migration matrix that enumerates every site Phase 1 will touch, classified by treatment category. Output is a write-once, read-many document; Phase 1 TOs reference it as their authoritative inventory.
  </objective>

  <scope>
    <files_read>
      <file>portal/src/pages/AdvisorIntelligence/_partners/**/*.tsx</file>
      <file>portal/src/pages/AdvisorIntelligence/_partners/**/*.ts</file>
      <file>portal/src/pages/AdvisorIntelligence/_shared/**/*.tsx</file>
      <file>portal/src/pages/AdvisorIntelligence/_shared/**/*.ts</file>
      <file>portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts</file>
      <file>portal/src/pages/AdvisorIntelligence/index.tsx (dispatcher)</file>
      <file>portal/src/lib/firmAccess.ts (L1 canonical reference)</file>
      <file>portal/src/api/endpoints/advisor-intelligence.ts (LAMBDA_FIRM_ID)</file>
    </files_read>
    <files_written>
      <file action="create">docs/architecture/ADVI_SHARED_AUDIT.md</file>
    </files_written>
    <files_not_touched>
      All other portal/src/** files (Phase 0 is audit-only; refactor lands in Phase 1).
    </files_not_touched>
  </scope>

  <requirements>
    <requirement id="1">
      Produce the migration matrix at `docs/architecture/ADVI_SHARED_AUDIT.md` covering EVERY dimension listed in PRD §4.1. Sections required:

      **§A. firmId-conditional branch inventory:**
      Every inline `firmId === ...` and `isInflectionFirm` branch. Table columns:
      - File + line number
      - Current behavior (one-sentence description of the branch's effect)
      - Proposed `TenantLayoutConfig` field name + semantics (from PRD §3.2 or new-field proposal)
      - Treatment: REPLACE-WITH-CONFIG / KEEP-AT-DISPATCHER / OTHER (justify each OTHER)
      - Target Phase 1 TO: SHARED.002 (PartnerAnalytics) / SHARED.003 (BookView+ClientsTab) / SHARED.006 (canonicalization) / SHARED.007 (residual mop-up)

      Expected count: ~22 sites + dispatcher allowlist + 1 type-file comment + 1 ProtectedRoute reference per PRD §5.2.

      **§B. Per-firm component override inventory:**
      Every component under `_partners/{firm}/` that overrides or augments a `_shared/*` counterpart. Table columns:
      - Partner component path
      - Shared counterpart (if any)
      - Replacement / augmentation classification
      - Whether the divergence is config-extractable (lifts to TenantLayoutConfig) or genuinely component-distinct (stays as partner override)

      **§C. Per-firm constants inventory:**
      Every constant in `_partners/{firm}/constants.ts`. Table columns:
      - Constant name + value
      - Move target per PRD §3.2 sections (Identity / Data sources / Asset classes / Roles / Features / Source attribution / Numeric defaults / etc.)
      - Sentinel-keep classification (some constants are infra-implementation details and stay at partner level — call out which)

      **§D. Cache-key collision resolution:**
      The 4 empirically-surfaced collisions from `comp-cache collisions`:
      - `['advisor-book-view', 'advisorId', 'firmOverride']` — AdvisorBookView L102 + AdvisorPublicProfile L1734
      - `['advisor-intelligence', 'timeseries-overview', 'firmOverride']` — PartnerAnalytics L225 + DistributionTab L805
      - `['firm-leaderboard', 'firmOverride']` — 49F-index L90 + AdvisorsTab L217 + ClientsTab L145
      - `['partner-analytics', 'granularity', 'firmOverride']` — PartnerAnalytics L116 + DistributionTab L744

      For each, document:
      - All call sites + the firmOverride literal each currently passes (look for actual values like 'inf' / 'inflection' / '49f' / '49financial')
      - Whether resolution = canonicalize firmOverride upstream (SHARED.006 scope) OR namespace-split keys (SHARED.001 scope — extend TenantLayoutConfig with `cacheKeyNamespace` field)
      - Recommendation per collision (the four may resolve differently)

      **§E. TenantLayoutConfig field-gap analysis:**
      Every cohort / feature / mode / numeric default that currently lives inline (not yet in TenantLayoutConfig). Table columns:
      - Current location (file + line)
      - Proposed field name in extended TenantLayoutConfig (per PRD §3.2)
      - Default semantics (matters for new-firm scaffolding)
      - 49F value + INF value (empirical from current code)
      - Notes on whether semantics differ subtly between firms (PRD §3.2 calls out a few — e.g. `auaDonut.source` cash inclusion rule)

      **§F. 102-warning lint enumeration:**
      One row per file with warnings. Columns:
      - File path
      - Warning count + categories (A=react-refresh/only-export-components, B=react-hooks/static-components, OTHER=enumerate type)
      - Proposed treatment (SHARED.004 co-location refactor / SHARED.005 component extraction / SHARED.007 one-off resolution)

      **§G. firmId namespace literal census (4-layer):**
      Per PRD §2.2 / §3.1. Enumerate every literal:
      - L1 firmAccess.ts: `'49financial'` / `'inflection'` / `'cottonwood'`
      - L2 PARTNER_VIEWS keys in `index.tsx`: `'bd'` / `'inflection'`
      - L3 `_partners/{firm}/constants.ts` FIRM_ID: `'bd'` / `'inf'`
      - L4 LAMBDA_FIRM_ID map in `api/endpoints/advisor-intelligence.ts`

      For each L2/L3/L4 site, note the rename target (per PRD §3.1 canonical L1 convergence). SHARED.006 consumes this section as its scope inventory.

      **§H. Cross-project overlap risks:**
      Every file in scope that ADVI_INFTGT or ADVI_INFGRO active TOs would also touch. Reference the PRD Q5 sequencing concern. Output: file-level overlap table so COO can plan parallel-vs-serialize per Andrew's Q5 ruling.
    </requirement>

    <requirement id="2">
      The audit document MUST cite specific file+line numbers throughout. Hand-waving like "PartnerAnalytics has several inline branches" is rejected. Every entry has a concrete pointer. Use `Grep` (NOT manual scanning) to enumerate; capture the line-number output verbatim in the matrix tables.
    </requirement>

    <requirement id="3">
      Where the PRD already provides a field name (§3.2 TenantLayoutConfig extension), USE that exact field name. Don't invent parallel names. If the audit surfaces a real gap in §3.2's coverage, ADD the gap to a "PRD §3.2 supplement" section at the bottom — that section is your contract to CTO that the type extension TO (SHARED.001) needs to expand beyond §3.2.

      No silent renames. Either match PRD or surface the gap.
    </requirement>

    <requirement id="4">
      The audit is READ-ONLY on portal/src/**. Do not refactor anything in Phase 0. Even fixing an obvious typo or moving a single import is forbidden — Phase 0 is pure documentation. Refactoring happens in Phase 1 TOs.
    </requirement>

    <requirement id="5">
      Surface ANY scope ambiguity to COO before completing the audit. Examples:
      - File you can't classify as Category A vs B (e.g., a warning that's actually category C "other" not enumerated in PRD §2.4)
      - Constant in `_partners/{firm}/constants.ts` that doesn't fit any §3.2 target category
      - firmId-conditional branch that's actually correct-as-inline (e.g., a one-off if/else for a dead code path)
      - Cross-project overlap that materially blocks SHARED.002/003 from running parallel with INFTGT-P1/P2 or INFGRO Stage 1

      MCP to COO with a "QUESTION/AMBIGUITY:" subject prefix. Don't block on a single ambiguity — keep going on unrelated sections and surface the question while continuing.
    </requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase id="1" when="before-write">
      <step>
        <run>comp-build</run>
        <expect>Cache freshness confirmed; node count consistent with PRD §5.2 (1590/1663 file-backed nodes). If cache is stale, rebuild forces a fresh scan against today's portal state. No exit-code-failing output.</expect>
        <if_mismatch>STOP. Cache rebuild required before audit; otherwise §B/§C/§F counts may not reflect today's state.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions</run>
        <expect>Same 4 collisions surfaced in PRD §5.2 OR more (cache state may have evolved since PRD-time). Capture full output for §D verbatim.</expect>
        <if_mismatch>If fewer collisions surface, someone has already partially canonicalized — document which AND continue audit. If new collisions surface, expand §D scope and note in PRD §3.2 supplement.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check InflectionAdvisorIntelligence</run>
        <expect>Schema enumerated; field count + MISSING/UNUSED documented. Per PRD §5.3 the dispatcher wrapper doesn't resolve — target leaf component instead.</expect>
        <if_mismatch>If still "Component not found", document in §H and proceed with manual Grep. Not blocking.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check FortyNineFinancialAdvisorIntelligence</run>
        <expect>Same — leaf component schema documented.</expect>
        <if_mismatch>If schema differs materially between INF + 49F leaves, document the asymmetry in §E (most likely candidate for TenantLayoutConfig extension).</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before-commit">
      <step>
        <run>Grep "<status>pending|staged</status>" on docs/architecture/ADVI_SHARED_AUDIT.md</run>
        <expect>The audit doc is a deliverable, not a TO — should NOT contain task-order status tags. Self-check.</expect>
        <if_mismatch>Remove any accidental status tags; document is pure read-and-record.</if_mismatch>
      </step>
      <step>
        <run>wc -l docs/architecture/ADVI_SHARED_AUDIT.md</run>
        <expect>Substantive document — expect ≥300 lines given §A-§H coverage. If significantly smaller, sections are under-populated.</expect>
        <if_mismatch>Review each section vs Requirement 1; expand thin sections before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after-commit">
      <step>
        <run>comp-build</run>
        <expect>New file `docs/architecture/ADVI_SHARED_AUDIT.md` indexed as new node; downstream Phase 1 TOs can reference it by name.</expect>
        <if_mismatch>If comp-build doesn't pick up the new file, that's a comp-build limitation (doc files may not be graph-indexed); not blocking, but flag for ADHC_COMPIL_V4 backlog.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none_required>
      Phase 0 is audit-only (read-only on portal/src/**, creates new doc at docs/architecture/ADVI_SHARED_AUDIT.md). No shared S3 keys, no shared scripts, no portal components touched. Zero blast radius outside the new doc file.

      Active projects sharing portal scope but NOT in conflict with Phase 0 (because Phase 0 doesn't write to portal):
      - ADVI_INFLEC (chain marathon + 4-panel-gap closure complete 2026-05-12)
      - ADVI_INFTGT (P0 wave closed; P1/P2 HOLD pending RD scope reconciliation)
      - ADVI_INFGRO (Stage 1 dispatch_held pending Andrew Q decisions)

      Phase 0 audit data WILL inform overlap-risk planning for SHARED.002 / SHARED.003 / SHARED.006 — that's §H output, captured for COO's downstream sequencing decision.
    </none_required>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="1">`docs/architecture/ADVI_SHARED_AUDIT.md` exists on CLOUD branch with sections §A through §H each populated per Requirement 1.</criterion>
    <criterion id="2">Every entry across §A / §C / §F cites file+line. Zero hand-wavy entries. Spot-checkable.</criterion>
    <criterion id="3">§D documents all 4 known cache-key collisions plus any new ones surfaced by Phase 1 `comp-cache collisions`. Per-collision resolution recommendation present (canonicalize-upstream vs namespace-split).</criterion>
    <criterion id="4">§E TenantLayoutConfig field-gap analysis enumerates ALL inline divergence points found in §A; cross-references §3.2 field-name proposals; flags any §3.2 gaps in a "PRD §3.2 supplement" subsection.</criterion>
    <criterion id="5">§G enumerates every L2/L3/L4 firmId literal site + rename target. SHARED.006 will use this section as its scope; if entries are missing here, SHARED.006 will miss touch-sites.</criterion>
    <criterion id="6">§H cross-project overlap surfaces all files where ADVI_INFTGT-P1/P2 or ADVI_INFGRO Stage 1 active TOs would also write. Empty section = explicitly confirms no overlap (not silently skipped).</criterion>
    <criterion id="7">Session log under `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/<YYYY-MM-DD>/` includes the Compiler Tools section reproducing each `<run>` + observed output + pass/fail vs `<expect>` per `<compiler_tools_mandate>`. Missing rows = REWORK.</criterion>
    <criterion id="8">Commit attribution: `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`. Via `.tools/safe-commit.sh --only -- docs/architecture/ADVI_SHARED_AUDIT.md <session-log-path>`.</criterion>
  </acceptance_criteria>

  <ravc_protocol>
    <ravc1>ACK receipt of this TO. Confirm DE 0.4 has the bandwidth to start. ETA estimate (~1d per PRD §4.1).</ravc1>
    <ravc2>Audit committed. Cite commit hash + `wc -l` output + section coverage summary (§A through §H present with N entries each).</ravc2>
    <ravc3>(if applicable) Any QUESTION/AMBIGUITY MCPs received from DE 0.4 during the audit, with my (COO) response.</ravc3>
    <ravc4_close>COO accepts after spot-checking §A and §D entries against the portal/src tree. Acceptance unlocks Phase 1 TO authoring (SHARED.001 type extension).</ravc4_close>
  </ravc_protocol>

  <notes>
    <note>SHARED.001-.013 are NOT yet authored as individual TO files. Authoring waits on (a) Andrew Q2 (asset class taxonomy authority — portal-only vs DS-mirrored), (b) Andrew Q5 (sequencing — split-Phase-1 vs full-Phase-1-first), and (c) this Phase 0 audit completion. Phase 0 doesn't depend on Q2 or Q5; you can start immediately.</note>
    <note>If DE 0.4 needs lane help (the audit is breadth-first across many files), MCP COO to route DT 0.4 + RD 0.4.2 in support roles. PRD §4.2 anticipates Phase 1 parallelization across DE/DT/RD; Phase 0 lane assistance is a smaller-scale extension of that.</note>
    <note>Andrew Q2/Q5 surfacing in progress (COO user-facing text 2026-05-12 ~22:35Z). Andrew rulings will arrive async; Phase 0 audit shouldn't wait.</note>
  </notes>
</task_order>
