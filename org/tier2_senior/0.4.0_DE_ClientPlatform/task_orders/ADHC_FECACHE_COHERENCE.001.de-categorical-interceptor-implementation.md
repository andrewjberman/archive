<task_order>
  <metadata>
    <id>ADHC_FECACHE_COHERENCE.001</id>
    <slug>de-categorical-interceptor-implementation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO. All gates met: (1) PRD v0.2.1 canonical at `docs/architecture/ADHC_FECACHE_COHERENCE.md` per CTO `37ea514b7` git mv; (2) All 5 implementation choices CTO RATIFIED 2026-05-14 17:54Z + Option A multi-key normalization 18:05Z; (3) Phase 2a per-callsite ship LANDED `d0bbc856` (14 P1 callsites disarmed); (4) Census complete (28 canonical / 3 aliases / 7 flags); (5) defense-in-depth pair with ADHC_LEDGEH structurally ratified.</dispatch_unblock_condition>
    <project_code>ADHC_FECACHE_COHERENCE</project_code>
    <priority>P1 — categorical FE-cache coherence invariant; Cottonwood SOFT-GATE beneficiary; defense-in-depth pair with ADHC_LEDGEH</priority>
    <sla>~1-1.5h wall implementation (~112 LOC new + ~2 LOC modified across 4 files)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_FECACHE_COHERENCE.md (v0.2.1; CTO RATIFIED all 5 choices + multi-key normalization)</ref>
    <ref type="companion_brief">docs/briefs/fe_cache_freshness_audit_design_20260514.md (DE 0.4 ebce828ac; 23-callsite enumeration; P1/P2/P3 risk-tier)</ref>
    <ref type="empirical_anchor">Andrew 2026-05-14 13:27Z four-screenshot — Inflection Segment Analytics Annual + Monthly + Quarterly intervals diverge ($202M/$203M with mixed data_as_of footers); S3 truth canonical; FE-cache resident</ref>
    <ref type="phase2a_precursor">DE 0.4 `d0bbc856` portal/DEV (14 P1 callsite refetchOnMount drops; pre-categorical landmine defusal) — defense-in-depth pair</ref>
    <ref type="defense_in_depth_sister">ADHC_LEDGEH `5362d0295` (origin-response L@E structured JSON error envelope) + ADHC_BPMVH `823c3e74b` (bronze-pmv hybrid headline-fresh) — 3-project ADHC defense-in-depth corpus</ref>
    <ref type="cotton_soft_gate">Andrew product-strategy ratify pending — CTO + COO lean Option (a) ship-before-Cottonwood per FIRMSEP.10 risk-window beneficiary framing</ref>
    <ref type="wire_boundary_normalizer">Multi-key normalization pattern per [[feedback-bidirectional-translator-pattern]] sister; absorbs same-semantic-different-name pathology (data_as_of / as_of_date / snapshot_date)</ref>
  </references>

  <context>
    Andrew empirical 2026-05-14 13:27Z: Monthly view shows $203M / May 14 footer; Quarterly view shows $202M / May 13 footer in same browser session. S3 truth canonical (all interval artifacts $203M / 2026-05-14). Divergence is FE-cache-resident — Quarterly's queryKey was localStorage-persisted from yesterday via PersistQueryClientProvider 12h maxAge; Monthly was cache miss → fresh fetch.

    **The structural gap:** AdvisorIntelligence has ZERO `queryClient.invalidateQueries` calls (grep-confirmed). Cache lives until `staleTime` expiry (Infinity globally + 5min per-callsite), `gcTime` expiry (Infinity), 12h `maxAge` localStorage prune, OR `queryClient.clear()` on logout. None tied to chain emission boundaries.

    Andrew framing: "When we update portal files, we need to update ALL of them. This outcome should never happen. We need to identify where in our process we allow for this dispersion and fix it categorically."

    Per CTO 5-choice ratify: implement categorical interceptor at `apiRequest()` body level (single point of enforcement) + module-singleton `dataAsOfCanonicalStore` + hardcoded queryKey prefix allowlist for scope predicate (fail-closed) + lazy `invalidateQueries` refetch + single cache-buster retry on older data_as_of.

    Multi-key normalization (CTO ratified 18:05Z): `extractChainTimestamp` reads `data_as_of` || `as_of_date` || `snapshot_date` → captures all 3 field aliases (including `HeaderSummary.as_of_date` that Andrew's $202M screenshot footer literally read). 5 LOC at wire boundary vs ~3h DS-side rename across 3 gold scripts.
  </context>

  <objective>
    Implement categorical FE-cache coherence invariant: every view rendered in the same session that observes a `data_as_of`-bearing response triggers invalidation of all AdvisorIntelligence-scope queries with older `data_as_of` (or aliases). Single point of enforcement at `apiRequest()` body. Multi-key normalization absorbs `data_as_of` / `as_of_date` / `snapshot_date` aliases. `buster:v1→v2` atomic bump clears existing localStorage poisoning simultaneously.
  </objective>

  <scope>
    <files>
      <file action="create">portal/src/lib/dataAsOfCanonicalStore.ts (~45 LOC; module-singleton with get/set/clear; sessionStorage persistence)</file>
      <file action="create">portal/src/lib/isAdvisorIntelligenceScope.ts (~30 LOC; predicate helper; hardcoded queryKey prefix allowlist; fail-closed)</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts (~35 LOC; interceptor logic post-JSON.parse in apiRequest body; multi-key extractChainTimestamp helper)</file>
      <file action="modify">portal/src/contexts/AuthContext.tsx (~2 LOC in logout; `dataAsOfCanonicalStore.clear()` paired with `queryClient.clear()`)</file>
      <file action="modify">portal/src/main.tsx (1 LOC; buster:v1→v2 bump at line 70 ATOMIC with categorical PR per CTO R4 ratify — clears existing localStorage poisoning)</file>
      <file action="create">portal/src/lib/__tests__/dataAsOfCanonicalStore.test.ts (unit tests per PRD test plan)</file>
      <file action="create">portal/src/lib/__tests__/isAdvisorIntelligenceScope.test.ts (predicate unit tests)</file>
    </files>
  </scope>

  <phase id="1" when="before implementation">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit 2>&1 | tail -3</run>
      <expect>0 errors baseline (post-NMCOHT foundation dcab7fe6 + RD 219a4b5e). If errors surface, surface to COO + DT 0.4 — concurrent commit drift candidate.</expect>
    </step>
    <step>
      <run>grep -rn "invalidateQueries" portal/src/pages/AdvisorIntelligence/ portal/src/contexts/ portal/src/api/endpoints/advisor-intelligence.ts</run>
      <expect>Confirms ZERO `invalidateQueries` calls in AdvI scope per PRD §"Why the current architecture allows this" census. Implementation introduces FIRST instance.</expect>
      <if_mismatch>If matches surface, document inline — may indicate parallel work or stale grep cache.</if_mismatch>
    </step>
    <step>
      <run>grep -rn "data_as_of\|as_of_date\|snapshot_date" portal/src/types/ portal/src/api/endpoints/advisor-intelligence.ts | wc -l</run>
      <expect>Confirms 3-key field census per PRD §"data_as_of universality census": 28 canonical + 3 aliases. Multi-key normalization captures all.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Create `portal/src/lib/dataAsOfCanonicalStore.ts` — module-singleton; `get()` reads sessionStorage on cold-init; `set(d)` updates internal + persists; `clear()` on logout. ~45 LOC.</run>
      <expect>Standalone util; no React Query dependency at module level (decouples store from QueryClient).</expect>
    </step>
    <step>
      <run>Create `portal/src/lib/isAdvisorIntelligenceScope.ts` — predicate helper; queryKey[0] starts-with allowlist of 13 known prefixes per PRD §"Component architecture" diagram. Fail-closed default. ~30 LOC.</run>
      <expect>Greppable allowlist; new AdvI endpoint without prefix added → silent fall-out-of-scope visible.</expect>
    </step>
    <step>
      <run>Modify `portal/src/api/endpoints/advisor-intelligence.ts` — add `extractChainTimestamp` multi-key helper + interceptor logic post-JSON.parse in apiRequest body per PRD §"Component architecture". Single cache-buster retry on older `data_as_of` (bounded budget=1; log on second failure). ~35 LOC + multi-key helper 5 LOC.</run>
      <expect>Multi-key helper absorbs `data_as_of` / `as_of_date` / `snapshot_date` aliases per Option A normalization. Interceptor lazy invalidates via `queryClient.invalidateQueries({ predicate })`.</expect>
      <if_mismatch>If existing apiRequest body has tight closure on response shape, consider extracting interceptor to `lib/dataAsOfInterceptor.ts` for cleaner separation.</if_mismatch>
    </step>
    <step>
      <run>Modify `portal/src/contexts/AuthContext.tsx` — add `dataAsOfCanonicalStore.clear()` paired with `queryClient.clear()` in logout. ~2 LOC.</run>
      <expect>Idempotent clear; logout drops both query cache + canonical store simultaneously.</expect>
    </step>
    <step>
      <run>Modify `portal/src/main.tsx` line 70 — buster:v1→v2 bump per CTO R4 ratify (atomic with categorical PR).</run>
      <expect>1-LOC bump. Clears existing localStorage poisoning on first user load post-deploy. Critical: must ship ATOMIC with interceptor (not separate commits).</expect>
    </step>
    <step>
      <run>Author unit tests in `portal/src/lib/__tests__/` per PRD test plan §"Unit tests".</run>
      <expect>Coverage: dataAsOfCanonicalStore set/get/clear + isAdvisorIntelligenceScope predicate true/false + interceptor invalidation behavior on newer/older/same data_as_of.</expect>
    </step>
  </phase>

  <phase id="3" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors.</expect>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | tail -5</run>
      <expect>≤9 warnings (matches RD .007 close baseline; no new lint warnings introduced).</expect>
      <if_mismatch>If new lint warnings, address before commit.</if_mismatch>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run build 2>&1 | tail -5</run>
      <expect>0 errors; no chunk-graph perturbation (new files in lib/ should land in vendor chunk).</expect>
    </step>
    <step>
      <run>Unit test suite: bun test portal/src/lib/__tests__/dataAsOfCanonicalStore.test.ts portal/src/lib/__tests__/isAdvisorIntelligenceScope.test.ts</run>
      <expect>All tests PASS.</expect>
    </step>
    <step>
      <run>Manual empirical reproduction harness per PRD test plan — DevTools localStorage edit to reproduce $202M / May 13 quarterly; verify fix auto-invalidates Quarterly to $203M / May 14 on next access.</run>
      <expect>WITH FIX: Quarterly auto-invalidates + re-fetches on next access OR navigation. WITHOUT FIX: Quarterly stays $202M / May 13.</expect>
      <if_mismatch>If manual repro fails, investigate interceptor predicate scope OR multi-key extraction.</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="after commit">
    <step>
      <run>git push origin DEV (portal submodule) — single PR atomic ship per PRD §"Rollback plan"</run>
      <expect>portal DEV advances by 1 commit; ~112 LOC new + ~2 LOC modified across 4 files (5 if counting main.tsx buster bump).</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.7 (LEDGEH co-coord)</run>
      <expect>Evidence-bearing close: commit SHA + tsc+lint+build empirical + unit test pass + manual repro empirical.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `portal/src/lib/dataAsOfCanonicalStore.ts` created with module-singleton + sessionStorage persistence (~45 LOC)
    AC2: `portal/src/lib/isAdvisorIntelligenceScope.ts` created with hardcoded queryKey prefix allowlist (~30 LOC; fail-closed)
    AC3: `portal/src/api/endpoints/advisor-intelligence.ts` apiRequest body augmented with interceptor + multi-key extractChainTimestamp helper
    AC4: `portal/src/contexts/AuthContext.tsx` logout adds `dataAsOfCanonicalStore.clear()` paired with `queryClient.clear()`
    AC5: `portal/src/main.tsx:70` buster:v1→v2 bump ATOMIC with categorical PR per CTO R4
    AC6: Unit tests cover dataAsOfCanonicalStore + isAdvisorIntelligenceScope + interceptor invalidation behavior; all PASS
    AC7: Multi-key normalization captures `data_as_of` || `as_of_date` || `snapshot_date` (per Option A)
    AC8: Single cache-buster retry on older `data_as_of` (bounded budget=1; log on second failure)
    AC9: Scope predicate fail-closed (any new AdvI endpoint without prefix added → silent fall-out-of-scope; visible omission)
    AC10: tsc 0 errors + lint ≤9 warnings (matches .007 baseline) + bun build clean (no chunk-graph perturbation)
    AC11: Manual empirical reproduction harness PASS (DevTools localStorage edit reproduces bug; fix auto-invalidates)
    AC12: Single PR atomic ship; revert via `git revert` if regression detected (no schema migrations; no data writes)
    AC13: RAVC2 evidence to COO + CC CTO + AE 0.7
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 baseline grep + tsc baseline. Phase 3 tsc + lint + bun build + unit test suite. Phase 4 portal push.</compiler_tools_mandate>

  <cross_domain_coordination>
    DEFENSE-IN-DEPTH PAIR: ADHC_LEDGEH (AE 0.7 TO-001 dispatch_held=false) addresses wire-boundary error states; ADHC_FECACHE_COHERENCE (this TO) tightens consumer-side queryKey coherence. Sister ships; bundle if landing close together. CC AE 0.7 on RAVC2.
    BENCH-STATE COORD: DE 0.4 currently NMCOHT 5 consumer rewires (~2-3h). Context-switch trigger: this TO authored. Smaller scope (~1-1.5h vs NMCOHT remaining ~2-3h) — DE judgment on context-switch cost. Recommend: ship this TO mid-NMCOHT-rewires if timing aligns; defense-in-depth value high.
    NMCOHT FE FOUNDATION ALREADY SHIPPED `dcab7fe6` — no conflict.
    PORTAL SUBMODULE: DE pushes to portal/DEV; DT 0.4 promotes to PROD per cadence.
    COTTONWOOD SOFT-GATE: ship-before-Cottonwood per CTO + COO lean; awaiting Andrew product-strategy ratify on sequencing.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE-side implementation only. buster:v1→v2 bump clears existing localStorage on first user load post-deploy; no data writes.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. New lib modules `dataAsOfCanonicalStore.ts` + `isAdvisorIntelligenceScope.ts`
    2. apiRequest body interceptor + multi-key extractChainTimestamp helper
    3. AuthContext logout paired clear
    4. main.tsx buster:v1→v2 atomic bump
    5. Unit tests passing
    6. Manual empirical reproduction harness PASS evidence
    7. RAVC2 to COO + CC CTO + AE 0.7
  </deliverables>

  <ravc>DE 0.4 RAVC2 to COO + CC CTO + AE 0.7 on AC1-13 PASS. Andrew empirical confirm on Inflection cross-interval coherence post portal/DEV → portal/PROD promote.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.

    **No emojis per CLAUDE.md.** Inline comments documenting buster:v1→v2 bump + multi-key normalization lineage to [[feedback-bidirectional-translator-pattern]] + interceptor design rationale per CTO 5-choice ratify.

    **Test isolation discipline:** unit tests use module-singleton reset pattern (`__resetStoreForTesting`) since module state persists across test files in bun test default config. Defensive pattern; documented inline.

    **Backwards compatibility note:** if DS-side renames `as_of_date` → `data_as_of` on `HeaderSummary` + `FeeEfficiencyResponse` + renames `snapshot_date` → `data_as_of` on `CohortASummaryResponse` at any future point, the alias branches in extractChainTimestamp become unreachable dead code. Opportunistic deletion on next maintenance touch (NOT in this TO scope).

    **4 DS-side flagged types** (AdvisorNnaClientsResponse + ConcentrationResponse + AdvisorDrilldownSummary + InflecTimeseriesChartResponse) lack chain-bound freshness markers — CTO routed as opportunistic SLA non-gating P3 follow-on TOs (will batch into ADVI_INFFIN.017 per CTO route). NOT gating this TO.

    **Banking opportunity:** if implementation surfaces a structural pattern that generalizes (e.g., "any interceptor at wire-boundary with QueryClient invalidation must observe response BEFORE React Query consumes; QueryClient global onSuccess is post-consumption + leaks scope across pages"), worth banking as `feedback_wire_boundary_interceptor_pre_consumption.md` or similar.

    **Andrew Cottonwood ratify**: this TO ships independently of Andrew ratify on Cottonwood sequencing. Worst case: defense lands post-Cottonwood live ship (Option b path); ships anyway as defense-in-depth.
  </notes>
</task_order>
