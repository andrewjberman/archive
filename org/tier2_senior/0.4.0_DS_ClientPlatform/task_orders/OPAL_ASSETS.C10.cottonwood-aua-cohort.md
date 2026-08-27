# OPAL_ASSETS.C10 — Cottonwood AUA figure sourced from the cot positions cube → new cohort row

<issued_to>0.4.0_DS_ClientPlatform (+ AE if infra needed — join to staffing fork)</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "OPAL_ASSETS — Grand Consolidation P2" to OPAL_ASSETS, which is complete-as-superseded. Closed as a record act, not a work verdict. Prior status: pending</status>
<hold>ANDREW HOLD 2026-07-14 ~00:25Z, verbatim: "Wait to dispatch until I give the go, I want to respawn the workers first." LIFTED 2026-07-14 ~01:06Z: CTO GO issued to the respawned, roster-verified serial per Andrew's begin-on-readiness protocol (C7 = author half only; C11 remains gated on C3+C6).</hold>
<project>OPAL_ASSETS</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C10)</prd>

## Scope
There is NO Cottonwood partner-total anywhere in the estate (measured). Source one from
`opal-data-cot/gold/positions_cube/` → a Cottonwood-AUA cohort row in the gold table, carrying the full
v0.21 identity tuple (as_of · state · scope · basis · valuation source · presentation case).

## Fences + the landmine this row must not arm
- The cube is POSITIONS-grain; the cohort row is partner-day grain; **the sum happens AT GOLD only.**
- **AC14 (CTO~B, measured):** Cottonwood's source is positions-based with NO target_weight rows anywhere
  — on the day Cottonwood is onboarded into any decomposition, a missing measured source MUST emit an
  honest partial/missing, NEVER a fallback to intent. The emitter already states this contract at
  `opal-assets-daily-emitter` (lines ~611-613). This row ships with `state` honest from day one.
- cot is one-way fan-in (READ only, never the reverse); cot↔bd complete separation binds.
- Cohort COUNT is Andrew's (the 14→16 question is being re-asked) — this TO adds the row's PRODUCTION,
  and its inclusion in any served row-set waits on his taxonomy ruling if it would change the count.

## <compiler_tools_mandate>
Phase 1: `comp-pipescript io` on the emitter (column gaps + consumers) before adding the cohort; grain
check written into the code path (positions → partner-day, sum at gold only).
Phase 2: `.tools/commit-gate.sh`; Rule 15.
Phase 3: `comp-validate --artifact` on the first emitted row before signaling it live.
</compiler_tools_mandate>

## <cross_domain_coordination>
Reads `opal-data-cot` gold only. MCP 0.6.x/cot lane owners before touching any cot-adjacent config.
Nobody writes `opal-data-inf/gold/meta/pipeline-complete.json`.
</cross_domain_coordination>

## <acceptance_criteria>
1. A `cottonwood_aua` (naming per v0.21 taxonomy) row exists in `opal-assets-daily-aua` for a real
   run_date with value derived from the cube, full identity tuple populated, `state` honest.
2. The derivation prints its denominator (accounts/positions counted, none sampled).
3. No decomposition/remainder path absorbs this row's absence (AC14 exercised: withhold the source,
   confirm honest missing — in a test, never a served write).
4. Session log + Compiler Tools section; RAVC close to CTO.
</acceptance_criteria>

<note date="2026-07-14 ~05:2xZ" by="0.4.0_DS_ClientPlatform (assignee reconciliation, comp-state sweep)">
Derivation LANDED (`9380707b6`): refuses a complete-looking total while cot's cash source reports
$0.00 over ZERO accounts against its own ~$34.3M note — honest `state` per AC14, exercised. The
cohort-count gate is now CLOSED: PRD §6 fork 3 RESOLVED (Andrew ~01:5xZ, "I accept your
recommendations on the open items" — the 16-row set APPROVED, DS implementation hold lifted); rows
land with the C11 emitter work. Remaining before AC1: cot cash-source grounding + first emitted row
on a real run_date (C11-adjacent; C11 staged on C3+C6). Status stays `pending`, correctly.
</note>
