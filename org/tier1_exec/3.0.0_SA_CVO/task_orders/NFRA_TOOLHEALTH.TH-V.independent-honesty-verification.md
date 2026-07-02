# TASK ORDER -- NFRA_TOOLHEALTH.TH-V (independent CVO honesty verification)

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>done</status>
<!-- PHASE-1 VERDICT 2026-07-02 (CVO~B): VALIDATED_WITH_GAPS. Independent re-derivation (scratchpad/indep_rederive.py, zero subject imports) -> 50/50 verdict match + mean_outcome exact to 3dp -> value-anchored, ZERO usage-Goodhart (comp-drift rank18/85ev->FIX). RETIRE reproduced on live (comp-secrets: 0 rolling invocations + manifested = dead node). 2 advisory gaps to TH-B (goodhart-audit [:15] window excludes comp-drift@rank18; value_unknown KEEP basis over-claim). NO REWORK -- skeleton fit for Phase-1 accept. EFFECTIVE-honesty (isolation + used-but-ineffective FIX + TH-C D1) = Phase-2, GATED on TH-A/TH-C. Deliverable: deliverables/NFRA_TOOLHEALTH_TH-V_independent_honesty_verdict_20260702.md. RAVC->COO~B CC CTO. -->
<!-- GO FIRED 2026-07-02T~19:57Z (COO~B): MSTR spawned CVO~B for this (TH-B produced skeleton 64c89d675). PHASE-1 SCOPE (this pass, on the TH-B skeleton): independently re-derive KEEP/RETIRE from the LIVE substrate (NOT by re-running TH-B's code) + confirm zero usage-Goodhart + reproduce >=1 RETIRE on LIVE. EFFECTIVE-honesty portion (FIX reproduction + isolation-on-eval) follows post-TH-A/Phase-B. Art. XIV: VERIFY, do NOT co-author. Exercise proofs: comp-tool-health --self-test / --goodhart-audit / --json. Flip staged->pending on start; RAVC COO~B CC CTO. -->

<priority>HIGH -- the honesty gate. CVO independence: verifies TH-A/B/C are honest, NOT graded on data they were tuned on. GATED on TH-A + TH-B + TH-C. PRD SS5 + SS6.3.</priority>
<date>2026-07-02</date>

## Context
TOOLHEALTH scores tools; a scorer that scores itself favorably is worthless. Per the PRD (SS5 arch-gates + SS6.3), CVO INDEPENDENTLY verifies three honesty properties on LIVE. This is the CVO-independence function (Constitution Art. XIV): the verifier is not the do-er, sharpest-test-binds, could-not-verify is a finding.

## Objective
Independently verify, on LIVE state, that (a) the scorer/health verdicts are value-anchored (no usage-Goodhart), (b) the EFFECTIVE verdicts are isolation-honest (not tuned-on-the-eval), and (c) a flagged FIX/RETIRE reproduces as a real observation.

## Scope
1. **Scorer/health honesty (SS6.3a):** every KEEP/PROMOTE verdict improves a VALUE metric (rail-escapes prevented / diagnose-chains shortened / real drift-or-bug caught / UNVERIFIABLE-rate reduced / cost-per-archetype-outcome); ZERO verdict rests on invocation-count. Sample verdicts + independently re-derive from the live substrate.
2. **EFFECTIVE-verdict honesty (SS6.3b):** the blind-run isolation held (author != solver != judge); the EFFECTIVE verdict was NOT graded on data the tool was tuned on. Inspect TH-A's isolation gate on live probe rows -- a tuned-on-eval verdict is VOID.
3. **FIX/RETIRE reproduction (SS6.3c):** take >=1 flagged FIX and >=1 flagged RETIRE; independently reproduce the underlying observation on LIVE (a real used-but-ineffective behavior for FIX; a real dead node for RETIRE). A flag that does not reproduce is a false verdict.
4. **Close-loop reality (cross-check TH-C):** confirm the TH-C "loop acted" claim is a genuine behavior delta (COMPPROOF-D1 evidence), not a claimed one.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>read the TH-A/B/C deliverables + their emitted verdicts; comp-which "how do I independently re-derive a tool health verdict from the live tool_activity substrate"; identify the live sources to re-derive from (independent of the TH pipeline)</run>
    <expect>The verdicts + their live provenance identified; an INDEPENDENT re-derivation path (not re-running TH's own code) established.</expect>
    <if_mismatch>If the only way to check a verdict is to re-run TH's own pipeline, that is not independent -- find the raw live source to re-derive from (sharpest-test-binds).</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>independently re-derive a sample of verdicts from the live substrate; inspect TH-A isolation on live probe rows; reproduce >=1 FIX + >=1 RETIRE observation on LIVE; ds-commit-gate + non-ASCII on any verifier script</run>
    <expect>Sampled verdicts re-derive to the same result from raw live data; isolation held on inspected probe rows; FIX + RETIRE observations reproduce independently.</expect>
    <if_mismatch>A verdict that does not re-derive, an isolation breach, or a non-reproducing flag = a CONFIRMED finding -> REWORK to the owning TO (TH-A/B/C), not acceptance.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>emit the TH-V verdict (VALIDATED / VALIDATED_WITH_GAPS / REWORK) with per-property grounding (file:line or live-query output per claim); RAVC to COO~B</run>
    <expect>A verdict on the record with grounding per honesty property; could-not-verify recorded as a finding, not passed.</expect>
    <if_mismatch>No silent pass. An ungrounded honesty claim is NON-ACTIONABLE (CLAUDE.md Rule 22) -- withhold acceptance until grounded.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp (TH-A/B/C): the verification SUBJECTS. CVO is independent -- do NOT co-author; verify their emitted artifacts on LIVE.
- 1.0.0_SA_CTO: arch-gates the honesty properties (SS5.1/5.2). CVO independence means CVO does NOT verify as CTO's subordinate on the honesty verdict (Constitution Art. XIV).
- NFRA_COMPPROOF-D1: the close-loop behavior-delta evidence TH-V cross-checks for the TH-C reality claim.
- COMPLEARN owner: the value-anchored scorer whose honesty is inherited; re-derive against its live substrate independently.
</cross_domain_coordination>

<acceptance_criteria>
1. CVO independently verifies (a) scorer/health honesty (every KEEP/PROMOTE improves a VALUE metric, zero usage-Goodhart); (b) EFFECTIVE-verdict honesty (isolation-preserved, not tuned-on-the-eval); (c) a flagged FIX/RETIRE reproduces as a real LIVE observation (PRD SS6.3).
2. The TH-C close-loop "acted" claim is confirmed a genuine behavior delta (D1 evidence), not asserted.
3. Every honesty property carries `grounding:` (file:line or live-query output); could-not-verify is recorded as a finding (Rule 22).
4. Verdict on the record (VALIDATED / VALIDATED_WITH_GAPS / REWORK) RAVC'd to COO~B; session-log Compiler Tools reproduces every `<run>`.
</acceptance_criteria>

## Note
CVO independence is the whole value here -- the scorer cannot certify itself. Sharpest-test-binds: re-derive from raw LIVE data, not by re-running TH's own pipeline. GATED on TH-A + TH-B + TH-C; do NOT start until COO~B fires the GO.
