# TASK ORDER -- NFRA_COMPPROOF.D1 (COMPLEARN autonomy audit: is the loop REAL or a dead ratchet?)

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- verdict ACCUMULATES-BUT-INERT (NOT-GREEN); D2 stays fenced; COMPLEARN fix-charter</status>
<priority>MEDIUM-HIGH -- concurrent on live artifacts. Gates D2 (D2 is FENCED behind D1-GREEN). PRD SS2-D + SS6.</priority>
<date>2026-07-01</date>

## Context
COMPPROOF-D1: COMPLEARN (the TRAINS peer) is supposed to make the program smarter on its own. Is the loop REAL or a dead ratchet? Ground ENTIRELY on LIVE run-artifacts (never self-report or PRD Status:) -- did the scheduled EventBridge->Fargate refresh actually RUN, produce fresh tool_activity, update gap_heat, and DEMONSTRABLY change routing/agent behavior on a later cycle?

## Objective
An autonomy verdict -- learns / accumulates-but-inert / not-running -- grounded on live EventBridge->Fargate run-artifacts, with evidence. D1-GREEN is the gate that unfences D2.

## Scope (ground on LIVE, never self-report)
1. **Did it RUN:** the scheduled EventBridge->Fargate COMPLEARN refresh -- live run history (task invocations, exit status, timestamps). Ran on schedule, or dead?
2. **Did it PRODUCE:** fresh tool_activity artifacts + an updated gap_heat -- compare successive vintages (is the data actually refreshing, or frozen?).
3. **Did it CHANGE BEHAVIOR (the load-bearing test):** did a later cycle's routing/agent behavior DEMONSTRABLY shift because of the learned signal? (e.g. a gap_heat-driven affinity or a coverage-gap surfaced that changed a route/dispatch.) This is the difference between "learns" and "accumulates-but-inert."
4. **Verdict + evidence:** learns / accumulates-but-inert / not-running, each grounded on the live artifacts cited.

<compiler_tools_mandate>
  <phase id="1" when="verify">
    <step><run>live run-artifact grounding: EventBridge rule + Fargate task run-history (comp-which "is the COMPLEARN refresh running" / comp-freshness / live aws inspection via the right comp-tool); successive tool_activity + gap_heat vintages; the behavior-change evidence</run>
    <expect>Live run-history (ran/didn't); vintage-comparison (fresh/frozen); a concrete behavior-change instance (or its absence).</expect>
    <if_mismatch>could-not-verify is itself a finding (PHASE-2). If the loop isn't running / isn't changing behavior, that IS the D1 verdict (accumulates-but-inert / not-running) -- report it grounded, don't soften.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 1.0.0_SA_CTO: D1-GREEN gates D2 (the self-extension spike). Your verdict unfences (or holds) D2. CC.
- NFRA_COMPLEARN (CLOSED): D1 audits its live autonomy -- a not-running/inert verdict is a re-open charter, not a soft note.
- 2.0.0_SA_COO~B: on your D1 verdict, I sequence D2 (GREEN -> unfence to the DE/DS spike; not-GREEN -> D2 stays fenced + COMPLEARN gets a fix-charter).
</cross_domain_coordination>

<acceptance_criteria>
1. Autonomy verdict (learns / accumulates-but-inert / not-running) grounded on LIVE EventBridge->Fargate run-artifacts -- ran? refreshed? changed-behavior? -- each yes/no + cited evidence.
2. The behavior-change test is explicit (a concrete later-cycle behavior shift attributable to the learned signal, or its documented absence).
3. D1-GREEN/not-GREEN stated as the D2 gate. RAVC COO~B + CC CTO.
</acceptance_criteria>

## Note
D1 is the honest test of the program's central claim (self-improvement). Ground it hard on live artifacts -- "accumulates-but-inert" is the most likely and most important verdict to get right (a dead ratchet that looks alive is exactly the PHASE-2 finding).
