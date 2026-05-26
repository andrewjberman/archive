<task_order>
<metadata>
  <to_id>YALP_MACROS.006a</to_id>
  <project>YALP_MACROS</project>
  <title>FRED multi-source authoritative-source RE reconnaissance (Phase 2a parallel lane A)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~A</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete — brief shipped 2026-05-26; 5/5 ACs met; standing for ws COO RAVC2 disposition</status>
  <priority>HIGH (Andrew sovereign direct ~21:00Z + ~21:05Z RE-OPEN Phase 2; "we just add an addendum to the PRD that we have to go exploring and we parallelize a bunch of DS on it to go chekc out FRED, BLS, any govt source"; ws CTO v0.5 7e781ea8c canonical Phase 2 charter)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.5 RE-OPENED `7e781ea8c` Phase 2 charter (supersedes v0.4 retraction; v0.3 substantive content re-canonicalized as Phase 2 scope).</ref>
    <ref type="phase1_artifacts">cascade `c50c59399` (Path X Phase 1 closure) + TO-001 brief `3effd8667` + TO-002 PARTIAL `e6321011b`. Phase 1 stands as completed-phase artifact.</ref>
    <ref type="andrew_quote">"we just add an addendum to the PRD that we have to go exploring and we parallelize a bunch of DS on it to go chekc out FRED, BLS, any govt source that might have those data fields/indicators from the Macroeconomics page"</ref>
    <ref type="andrew_cadence">"Worst case, that data is pretty low frequency so if Yang has to update it once a month or something that doesnt really matter" — monthly-cadence-acceptable formalized per v0.5 §5 AC-CADENCE-TOLERANCE.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT exploratory reconnaissance class. Phase 2a parallel lanes ~A/~B/~C/~D/~E all independent.</dependency>
  </dependencies>
</metadata>

<scope>
**FRED exploration lane** per CTO v0.5 §8 TO surface enumeration. Per Andrew direct "go exploring" framing — reconnaissance class (discover what's there + match against macro indicators), NOT strict identify-then-RE.

**Scope:** enumerate FRED endpoints + dataset coverage relevant to the 79-indicator universe from Phase 1 §5.1. Match per-indicator authoritative-source candidates from FRED for each yang macro_data.json indicator + per-series timeseries slug. Document coverage breadth + cadence per FRED series.

**Deliverable:** brief at `docs/briefs/yalp_macros_phase2a_fred_reconnaissance_2026-05-26.md` (compact reconnaissance doc; ~150-200 lines):
- §1 FRED API surface enumeration (base endpoint + series-search + observations endpoint + categories tree)
- §2 Per-indicator match-set: for each of the 79 yang macro indicators, identify FRED series ID(s) that authoritatively source the indicator (or `n/a — not-in-FRED` with explicit reason)
- §3 Cadence per FRED series (daily / weekly / monthly / quarterly per series metadata)
- §4 RE harness sketch: how the FRED API → indicator-mapping → comparison-against-yang-value would work at TO-008 implementation time
- §5 Coverage assessment: % of 79 indicators sourced via FRED + gaps that route to TO-006b/c/d/e sister lanes
- §6 Reconnaissance findings + sister-lane handoffs (any indicator clearly NOT in FRED routes to sibling reconnaissance lane)

**Reconnaissance class, NOT strict identify-then-RE.** Discovery + match-set are the deliverable; actual RE harness implementation deferred to TO-008.

**Sister Phase 2a lanes (parallel; independent):**
- TO-006b BLS (DS 0.1.0~B)
- TO-006c Census Bureau (DS 0.1.0~C; lane pending MSTR spawn)
- TO-006d Treasury/FDIC/other federal-source (DS 0.1.0~D; lane pending MSTR spawn)
- TO-006e Aggregate-class + orphan-indicator (DS 0.1.0~E)
</scope>

<acceptance_criteria>
- AC1: FRED API surface enumerated (base endpoint + key APIs documented).
- AC2: Per-indicator match-set populated for all 79 yang macro indicators (FRED series ID OR `n/a — <reason>`).
- AC3: Cadence per FRED series documented.
- AC4: RE harness sketch documented for TO-008 follow-on (NOT implementation; design-level).
- AC5: Coverage % + sister-lane handoffs documented (which indicators clearly NOT in FRED route to sibling reconnaissance lanes).
</acceptance_criteria>

<compiler_tools_mandate>
N/A — reconnaissance scope (no portal/Lambda code edits). Standard FRED API exploration + brief authoring.
</compiler_tools_mandate>

<cross_domain_coordination>
- **Phase 1 artifacts inherit:** Phase 1 TO-001 brief §5.1 (79-indicator universe enumeration) + L1 lineage map §6.4 are the indicator inventory inputs.
- **Sister lanes coordinate via TO-007 synthesis** (Phase 2b; sequential post-2a): consolidated source-of-truth brief authored by ~A primary + ~B/~C/~D/~E co-author.
- **RE verdict taxonomy preliminary** per v0.3 substantive content (now Phase 2 canonical): RE-MATCH / RE-REPRESENTATIVE / RE-GAP / RE-DRIFT — finalize post-reconnaissance per Andrew direct "go exploring" framing.
- **No YCharts coupling** — Phase 2 is RE doctrine multi-source; FRED is one authoritative source. No cookie-stale class concerns this lane.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for brief doc creation
- Brief doc at `docs/briefs/yalp_macros_phase2a_fred_reconnaissance_2026-05-26.md`
- 79-indicator match-set populated
- Cadence table populated
- RE harness sketch documented
- Coverage % + sister-lane handoffs flagged
</expected_evidence>

<notes>
**Andrew "go exploring" framing absorbed** — reconnaissance class. Don't over-engineer; discover what's there + match against indicators + flag gaps.

**ETA per CTO Phase 2a estimate:** ~2-4h wall per lane. Fast-trajectory regime endorsed by Andrew "the pace today was fantastic, more of that please thanks" via MSTR LD-0104; STANDBY-PREP compression may apply if you absorb FRED API surface fast.

**~A advantage:** Phase 1 lead-author on YALP_MACROS; you know the 79-indicator universe + yang upstream context cold. Methodology-template inheritance from Phase 1 brief.

**Phase 2b synthesis:** you're primary author on TO-007 source-of-truth synthesis brief (post all 5 Phase 2a lanes ship). Treat your Phase 2a brief as substrate for that synthesis.

**No need to wait** for sister lanes — your FRED reconnaissance can proceed independent. Sister-lane gaps surfaced in your §5 hand off to siblings at TO-007 synthesis time.
</notes>
</task_order>
