<task_order>
<metadata>
  <to_id>YALP_MACROS.009</to_id>
  <project>YALP_MACROS</project>
  <title>Phase 2c — empirical RE test-pulls + Level-2 side-by-side comparison vs yang-Bloomberg per 79-indicator universe (gates clear post TO-008 + TO-008b RAVC2-ACCEPT cycle 114/115)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~A</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete — Phase 2c empirical RE test-pulls + 79-indicator side-by-side comparison shipped 2026-05-26 ~23:?Z; 5/5 ACs met; 77% high-confidence MATCH + 5% REPRESENTATIVE + 11% DEFERRED + 9% Wave-2-pending; ZERO true-DRIFT post §3 sub-classification
  <priority>HIGH (Andrew /goal sovereign 2026-05-26T~22:42Z "drive YALP projects all the way through mapping and data/endpoint ID and side by side comparison"; gates clear post TO-008 + TO-008b RAVC2-ACCEPT)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.6 §8 line 183 — TO-009 canonical scope (ws CTO v0.6 amendment `244bea599` 6-shape verdict-taxonomy with SUBSTITUTE-FOUND class)</ref>
    <ref type="upstream">TO-008 multi-source RE harness `30bd38cf0` RAVC2-ACCEPTED + TO-008b Wave 2 partial `1b0ca2b24` RAVC2-ACCEPTED + TO-007 synthesis `59ab271de` ratified</ref>
    <ref type="substitute_doctrine">SUBSTITUTE_SECURITY_DOCTRINE.md v0.1 (`244bea599`) + Andrew sovereign substitute-security ruling + family-probe-method canonical (~D `0c2a48a0c`)</ref>
    <ref type="andrew_goal">2026-05-26T~22:42Z /goal: "Drive YALP projects all the way through mapping and data/endpoint ID and side by side comparison. That means running a project for every single portal page and figuring out side by side what data we can get from Ycharts/smartx/etc raw and what we have to derive to get to the same numbers Yang has from BBG/yang-pipeline."</ref>
  </references>
  <dependencies>
    <dependency>TO-008 RAVC2-ACCEPTED `30bd38cf0` (cycle 114)</dependency>
    <dependency>TO-008b RAVC2-ACCEPTED `1b0ca2b24` (cycle 115)</dependency>
  </dependencies>
</metadata>

<scope>
**Phase 2c — empirical RE test-pulls + per-indicator side-by-side comparison vs yang-Bloomberg per Andrew /goal directive.**

For each of the 79 indicators in the Macroeconomics page universe, execute live test-pull via the multi-source RE harness (TO-008 + TO-008b adapters) + side-by-side comparison against yang-Bloomberg current value, classify per 6-shape verdict-taxonomy (RE-MATCH / RE-MATCH-DERIVED / RE-REPRESENTATIVE / RE-GAP / RE-DRIFT / RE-DEFERRED / SUBSTITUTE-FOUND).

**Deliverable:** brief at `docs/briefs/yalp_macros_phase2c_re_test_pulls_20260526.md` (~300-500 lines):
- §1 Test-pull execution per-indicator (use FREDAdapter primary; sister-CROSS-CHECK overlay where applicable per TO-007 §7 build-order)
- §2 Per-indicator side-by-side table: indicator-name + yang-Bloomberg current value + RE current value + delta + verdict-class
- §3 SUBSTITUTE-FOUND application: any persistent-failure indicators get family-probe-method + substitute-security-search (closest-to-underlying first per Andrew sovereign doctrine)
- §4 Per-class summary: ~40 RE-MATCH + ~12 RE-MATCH-DERIVED + ~10 RE-REPRESENTATIVE + ~11 RE-GAP + 0 RE-DRIFT expected + ~7 RE-DEFERRED (PAID-no-substitute incl. Fed NLP per §12 amendment) + any new SUBSTITUTE-FOUND
- §5 79-indicator coverage final-confidence assessment per Andrew /goal completion
- §6 RAVC2 packet citing all test-pull artifacts + brief commit hash

**Apply substitute-security-discipline binding across ALL test-pulls per Andrew sovereign 2026-05-26T~22:27Z + ~22:28Z ruling.**

**Per CLAUDE.md Rules 13, 14, 14a, 15 binding.**
</scope>

<acceptance_criteria>
- AC1: All 79 indicators test-pulled via TO-008 + TO-008b harness (or substitute via Andrew sovereign discipline for persistent failures).
- AC2: Side-by-side comparison table populated per indicator (yang-Bloomberg current vs RE current vs delta + verdict-class).
- AC3: SUBSTITUTE-FOUND class applied for any persistent-failures via family-probe-method.
- AC4: Coverage final-confidence assessment per Andrew /goal completion (per-class breakdown + cumulative %).
- AC5: RAVC2 packet citing brief commit + per-indicator test-pull artifacts.

**Pass requires all 5 ACs MET. Multi-cycle scope per PRD §8 ~3-5h target.**
</acceptance_criteria>

<compiler_tools_mandate>
- `comp-validate` post-test-pull per adapter category
- LD-31 catalog-live-verify discipline for any new series ID before commitment
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-008c carry-forward** for remaining 9 HAR-RE-CANDIDATE indicators (NAHB + NAR + UMich + NFIB + TIC + AAII AssetAlloc ×3 + sister) when Andrew completes additional HAR captures — those indicators classify RE-DEFERRED-pending-HAR until then OR best-effort SUBSTITUTE-FOUND via existing harness
- **Sister Phase 2c lanes:** YALP_VALUAT/CORREL/POSITN/FACTOR all firing Phase 2 in parallel this cycle; pattern alignment helps cross-project consistency (same 6-shape taxonomy + same substitute-discipline)
- **No formal sub-RAVC2 required** — single integrated commit + RAVC2-Request
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing brief commit + AC1-AC5 evidence + per-indicator verdict-class breakdown.

**Target wall-time ETA:** ~3-5h per PRD §8 line 183. Sub-3h plausible per cascade-compression amplifier sustained (your session record: 6 ships in ~4h).

**Post-RAVC2-ACCEPT:** TO-010 Phase 2 spreadsheet finalize (~1-2h) + TO-VAL-v2 consolidated RAVC2 (~1-2h) + project-close 3-step atomic OR Phase 3 dispatch.
</deliverable_disposition>
</task_order>
