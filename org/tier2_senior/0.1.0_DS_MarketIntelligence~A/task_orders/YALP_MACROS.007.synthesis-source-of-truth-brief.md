<task_order>
<metadata>
  <to_id>YALP_MACROS.007</to_id>
  <project>YALP_MACROS</project>
  <title>Phase 2b consolidated per-indicator source-of-truth synthesis brief (TO-006a-e fold-in + tie-breakers + cost/access optimization + architectural-call surface)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~A</assigned_to>
  <co_authors>0.1.0_DS_MarketIntelligence~B, 0.1.0_DS_MarketIntelligence~C, 0.1.0_DS_MarketIntelligence~D, 0.1.0_DS_MarketIntelligence~E</co_authors>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete — synthesis brief shipped 2026-05-26; 7/7 ACs met; standing for ws COO RAVC2 disposition + TO-008 harness build dispatch</status>
  <priority>HIGH (Phase 2b sequential follow-on to Phase 2a 5-of-5 SHIPPED; Andrew sovereign 2026-05-26T~21:00Z RE-OPEN Phase 2 mandate; ws CTO v0.5 7e781ea8c canonical Phase 2 charter §8 TO-007 scope)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.5 §8 line 179 — TO-007 canonical scope</ref>
    <ref type="phase2a_substrate_~A_fred">commit `da862a6c6` brief docs/briefs/yalp_macros_phase2a_fred_reconnaissance_2026-05-26.md (672 lines; 69.6% FRED single-source coverage; 4-of-5-lane convergence architectural lean)</ref>
    <ref type="phase2a_substrate_~B_bls">commit `be703b5b1` brief docs/briefs/yalp_macros_phase2a_bls_reconnaissance_2026-05-26.md (470 lines; 12.7% BLS narrow-but-deep authoritative; 4 architectural-class findings)</ref>
    <ref type="phase2a_substrate_~C_census">commit `ba147dbc5` brief (10/79 ~12.7% Census-PRIMARY; FRED-PRIMARY + Census-SECONDARY for cross-check)</ref>
    <ref type="phase2a_substrate_~D_treasury_fdic">commit `e48480c5e` brief + §9 corrections `6d3a75014` + `4f4901d34` (20/79 ~25.3% Treasury-PRIMARY; FRED v1 2-step pattern + AWS-Secrets FredApiKey + release_id catalog LIVE-VERIFIED)</ref>
    <ref type="phase2a_substrate_~E_aggregate_orphan">commit `8de9c10f7` brief docs/briefs/yalp_macros_phase2a_aggregate_orphan_reconnaissance_2026-05-26.md (581 lines; 100% FRED-GAP closure 24/24; 6-tier access-class taxonomy; 2 LIVE-VERIFIED OPEN-REST quick-wins ^MOVE + CNH=X)</ref>
    <ref type="andrew_sovereign">2026-05-26T~21:00Z RE-OPEN "we just add an addendum to the PRD that we have to go exploring and we parallelize a bunch of DS on it" + "Worst case, that data is pretty low frequency so if Yang has to update it once a month or something that doesnt really matter" (monthly-cadence-tolerance formalized + push-down-the-PRD-queue framing for indicators-without-RE-coverage)</ref>
  </references>
  <dependencies>
    <dependency>Phase 2a TO-006a-e all 5 RAVC2-ACCEPTED (CYCLE 111 ~21:23Z — 5/5 lanes shipped: ~A FRED + ~B BLS + ~C Census + ~D Treasury/FDIC + ~E Aggregate-orphan)</dependency>
  </dependencies>
</metadata>

<scope>
**Phase 2b consolidated source-of-truth synthesis** — fold TO-006a-e per-source reconnaissance into a single per-indicator best-source mapping across the 79-indicator Macroeconomics page universe. Output: structured decision-substrate for TO-008 multi-source RE harness build.

**Deliverable:** brief at `docs/briefs/yalp_macros_phase2b_source_of_truth_synthesis_2026-05-26.md` (~250-400 lines target).

**Required sections:**

**§1 Per-indicator source-of-truth mapping (79 rows)** — single table; columns: indicator-name + yang-slug + PRIMARY-source + PRIMARY-endpoint-pattern + PRIMARY-cadence + SECONDARY-cross-check-source + cost/access-tier + RE-verdict-preliminary-class (RE-MATCH/RE-REPRESENTATIVE/RE-GAP/RE-DRIFT/RE-DEFERRED).

**§2 Tie-breaker decisions for cross-source overlap indicators** — primary candidates: ~10 labor/inflation indicators where ~A FRED + ~B BLS both authoritative. Decision rubric: FRED-PRIMARY (mirror discipline + uniform harness + ~A's 4-of-5-lane convergence empirical lean) + BLS-CROSS-CHECK (revision-flag richness + upstream-authoritative-class). Document the rubric + per-indicator pick.

**§3 Cost/access optimization** — apply ~E's 6-tier access-class taxonomy across the 79; cluster by tier (OPEN-REST-API + OPEN-DOWNLOAD-WITH-HAR-AID + HAR-RE-CANDIDATE + PAID-SUBSCRIPTION + DISCONTINUED + YANG-INTERNAL-CLARIFY); recommend harness build-order (cheapest-first: OPEN-REST → HAR-aided → HAR-RE-Wave-2 → architectural-call decisions).

**§4 Architectural-call surface (5 PAID-SUBSCRIPTION indicators)** — ISM PMI×2 + ISM New Orders×2 + Wards + S&P Global PMI×2 net 5 per ~E §4. Frame 3-path decision (subscribe / substitute / RE-GAP acceptable-by-documentation) + COO+CTO+CVO recommendation default = **(c) RE-GAP acceptable-by-documentation** per Andrew sovereign 21:00Z "push those pages down" framing. Substitute candidates documented inline where available.

**§5 Cleanup-class findings** — Ted Spread DISCONTINUED LIBOR-retirement-2022 (recommend SOFR-3M-minus-T-Bill-3M substitute or deprecate) + Fed NLP Sentiment yang-internal-clarify (~A coordination) + ICSA/CCSA-mis-attribution-to-BLS (~B §6 row 5 finding; route to DT 0.1.0 yang-generate-macro audit) + PPI-modern-vs-legacy class-distinction (~B §6 row 3 finding; surface as architectural decision-point: which is yang's source-of-truth — Andrew/CTO call).

**§6 Verdict-taxonomy finalization** — per Andrew "finalized post-reconnaissance" v0.5 §3 carve-out: confirm or refine RE-MATCH / RE-REPRESENTATIVE / RE-GAP / RE-DRIFT classes; surface any RE-class boundary cases empirically. Note: RE-DEFERRED candidate for PAID-class indicators per §4 disposition.

**§7 TO-008 harness build sequence recommendation** — implementation-order recipe for the multi-source RE harness:
- Wave-1 today: FREDAdapter (per ~A §4) + YahooFinanceAdapter (per ~E §4; ^MOVE + CNH=X + AGG live-implementable)
- Wave-2 HAR-capture: 11 HAR-RE-CANDIDATE indicators per ~E §4 (4-session sequence ~2h per ~D §7 precedent)
- Wave-3 BLSAdapter v2 POST (per ~B §4) cross-check overlay for ~10 labor/inflation indicators
- Wave-4 Census + Treasury/FDIC adapters cross-check overlay (per ~C + ~D §4)
- Wave-5 architectural-call resolution

**§8 Coverage % summary** — combined PRIMARY-implementable-today (per ~E §5) + Wave-2 HAR-RE expansion + PAID-class architectural-call deferral; final coverage % per Andrew sovereign monthly-cadence-tolerance framing.

**§9 Memory candidates / banking** — consolidated list of memory candidates surfaced across TO-006a-e + this synthesis (deferred to MSTR /govern + Andrew sovereign per LD-0025 ALWAYS-PROCEED).
</scope>

<acceptance_criteria>
- AC1: §1 per-indicator source-of-truth mapping complete for all 79 indicators (PRIMARY + SECONDARY + cost/access + RE-class).
- AC2: §2 tie-breaker rubric + per-indicator pick for cross-source overlap indicators.
- AC3: §3 cost/access optimization + 6-tier-taxonomy clustering + harness build-order recommendation.
- AC4: §4 5-architectural-call surface framed with 3-path decision + recommendation default.
- AC5: §5+§6 cleanup-class findings + verdict-taxonomy finalization (or confirmation-as-PRELIMINARY-stands).
- AC6: §7 TO-008 harness build sequence recommendation (Wave-1 through Wave-5).
- AC7: §8 coverage % summary + §9 memory candidates consolidated.

**Pass requires all 7 ACs MET.**
</acceptance_criteria>

<compiler_tools_mandate>
N/A — synthesis-doc scope (no portal/Lambda code edits). Brief authoring + cross-reference consolidation.
</compiler_tools_mandate>

<cross_domain_coordination>
- **Co-author scope** — ~A primary author (Phase 2b synthesis), ~B + ~C + ~D + ~E co-authors. Per [[feedback_standby_prep_compress_to_delivery_when_context_sufficient]] gate: substrate is empirically rich; co-authors verify accuracy of their TO-006[bcde] sections + flag any source-of-truth mis-mappings. Single integrated commit by ~A primary; co-author MCPs OPTIONAL (no formal sub-RAVC2 required unless conflict surfaces).
- **PAID-class architectural-call → Andrew/ws CTO/CVO route at synthesis time** — §4 default recommendation is (c) RE-GAP acceptable-by-documentation per Andrew sovereign 21:00Z framing; if ~A primary author surfaces material reasons against the default, escalate via MCP to ws COO at synthesis-author-time (not after-the-fact).
- **ICSA/CCSA yang-side mis-attribution + PPI legacy/modern class-distinction** — surfaces to ws CTO + DT 0.1.0 (yang-generate-macro audit) at synthesis brief authoring time; flag in §5; do NOT block synthesis ship.
- **No YCharts coupling** — Phase 2 multi-source RE; no cookie-stale class concerns.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing commit hash + brief path + §1-§9 AC1-AC7 evidence.

**Target wall-time ETA:** ~2-3h per PRD §8 line 179 (substrate-rich; compressible if cascade-compression sister-lane substrate-reuse pattern repeats — ~A's 7min FRED + ~E's 25min Aggregate benchmarks suggest sub-2h plausible).

**Standing posture post-RAVC2-ACCEPT:** ~A continues to TO-008 multi-source RE harness build (next Phase 2b TO). Co-authors return to KEEP-EPHEMERAL standby until TO-008 dispatch.
</deliverable_disposition>

<notes>
- This TO closes Phase 2b §1 (synthesis) and unblocks TO-008 harness build.
- The empirical 4-of-5-lane convergence on FRED-PRIMARY + sister-CROSS-CHECK is the architectural lean confirmed bottom-up. Synthesis should formalize this as the v1 harness architecture decision.
- ~E's 6-tier access-class taxonomy + 100% FRED-GAP routing closure provides the cost/access framework. Synthesis inherits verbatim.
- LD-31 [[feedback_api_catalog_live_verify_before_committing_ids]] discipline already applied across all 5 Phase 2a lanes — no re-verify needed at synthesis stage; cite source-verification dates per sister-brief.
- Cascade-compression pattern + sibling-lane shipped-substrate-reuse compounds throughput on multi-lane synthesis (post-RAVC2-ACCEPT [[substrate-reuse-when-sister-lane-shipped]] banking candidate carried forward).
</notes>
</task_order>
