# TASK ORDER -- NFRA_COMPPROOF.A1 (seam + process spot-check sweep: breadth; keeps B honest)

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>dispatched</status>
<priority>MEDIUM-HIGH -- concurrent on live; rides the wave-close (GRAPHUNI/GRAPHDEPTH already CLOSED, so no preempt concern). PRD SS2-A + SS6.</priority>
<date>2026-07-01</date>

## Context
COMPPROOF-A: a breadth spot-check that keeps B honest -- random-sample (NOT hand-picked happy-path) real /seams (3-axis: mechanical/declarative/semantic) + whole processes end-to-end across the COMP* program + live estate, grounded on DEPLOYED/SERVED/LIVE (never self-report or PRD Status:). /seams + the verify-channel is your discipline. Special attention to the JUST-CLOSED wave (COMPUNIFY V1, COMPDRIFT, COMPLEARN, COMPROUTE, GRAPHUNI, GRAPHDEPTH). COO~B scopes the sample size (below).

## Objective
Produce a spot-check ledger: a randomized 3-axis seam + whole-process sample, each verdicted on LIVE artifacts, with 100% of FAILs charted to a fix.

## Scope (COO~B-scoped sample)
- **Sample N = 12 seams** (randomized across the 3 axes -- ~4 mechanical / ~4 declarative / ~4 semantic; NOT hand-picked happy-path) + **M = 4 whole processes** end-to-end (suggest: a gold-run->served path, a Lambda deploy->parity path, a graph derive->marker-head->tool-read path, a portal serve->provenance path). Weight the sample toward the just-closed wave (>= half the seams from COMPUNIFY/COMPDRIFT/COMPLEARN/COMPROUTE/GRAPHUNI/GRAPHDEPTH).
- **Per-target:** 3-axis verdict (mechanical PASS/FAIL, declarative PASS/FAIL, semantic PASS/FAIL) + a knowledge-parity delta (does the graph/tool's answer match live) + residuals. Ground on DEPLOYED/SERVED/LIVE only.
- **Deliverable:** the spot-check ledger (one home, program ledger); 100% of FAILs charted to a fix (charter or owner).

<compiler_tools_mandate>
  <phase id="1" when="sample">
    <step><run>randomized seam selection (comp-which / /seams for the seam inventory; random-sample not happy-path) + confirm the live-grounding sources per target (served artifact / live AWS / marker-head)</run>
    <expect>12 seams + 4 processes selected randomly across the 3 axes; each has a LIVE grounding source (not PRD Status:).</expect>
    <if_mismatch>If a seam can't be live-grounded, that IS a finding (PHASE-2: could-not-verify is a finding) -- log it, don't skip.</if_mismatch></step>
  </phase>
  <phase id="2" when="verify">
    <step><run>3-axis verdict each vs LIVE; knowledge-parity delta; residuals -- exercise, never self-report</run>
    <expect>Each target 3-axis-verdicted on live; parity deltas measured; FAILs identified.</expect>
    <if_mismatch>A FAIL is a real finding -> chart it to a fix (100% of FAILs charted).</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 2.0.0_SA_COO~B: scoped the sample (N=12 seams / M=4 processes, wave-weighted); adjust with me if the seam inventory suggests a better cut. FAILs -> I route to owners.
- 1.0.0_SA_CTO: A keeps B honest (breadth vs B's depth); CC on the ledger.
- The just-closed-wave owners (~C/~D/~E): a FAIL on their closed work routes back to them for the fix-charter.
</cross_domain_coordination>

<acceptance_criteria>
1. >= 12 seams + >= 4 processes, randomly sampled (not happy-path), 3-axis-verdicted on LIVE/SERVED/DEPLOYED artifacts (never PRD Status:).
2. Per-target knowledge-parity delta + residuals; the just-closed wave >= half the seam sample.
3. 100% of FAILs charted to a fix (charter/owner). Ledger in the one program home. RAVC COO~B + CC CTO.
</acceptance_criteria>

## Note
A is the breadth that keeps B honest -- random-sample is the whole point (a hand-picked happy-path sweep proves nothing). Could-not-verify is itself a finding.
