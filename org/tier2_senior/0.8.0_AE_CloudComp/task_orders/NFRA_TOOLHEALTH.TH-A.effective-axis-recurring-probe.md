# TASK ORDER -- NFRA_TOOLHEALTH.TH-A (the EFFECTIVE axis: a RECURRING per-tool blind-run probe)

<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete</status>
<!-- STARTED 2026-07-02 by 0.8.0_AE_CloudComp~D per COO~B GO (224348Z). Flipped staged->pending. -->
<!-- COMPLETED 2026-07-06 by 0.8.0_AE_CloudComp (base) -- picked up the ~D build stranded uncommitted by
     the 07-03..07-06 holiday dormancy. tool_probe.py (per-tool EFFECTIVE probe, isolation-gated) +
     tool_corpus.py (sealed corpus) landed; self-test 13-assert PASS; LIVE run demonstrated the FIX-catch
     (comp-freshness KEEP->FIX flip via --effective-feed, grounded Rule 22). AC1-3 met. En route, fixed a
     LIVE regression: parse_rail/parse_rolling_log/parse_telemetry crashed on a non-UTF-8 byte (truncated
     em-dash, comp-which-rail.log line 3445) -> hardened all 3 unguarded opens with errors="replace"
     (comp_learns_score.py + open#390 were already hardened; these 3 were missed) -- had been bricking
     COMPLEARN corpus load fabric-wide since ~07-02. FOLLOW-ON (RAVC'd, CTO/COO~B call): the recurring
     TRIGGER cadence/host (same decision-class as the emit-wiring cloud-vs-local pick) -- probe is
     recurring-CAPABLE (append-only) but no auto-schedule wired (blind-runs are cost-heavy). RAVC COO~B CC CTO+CVO~B. -->

<!-- GO FIRED 2026-07-02T~22:40Z (COO~B) to 0.8.0_AE_CloudComp~D (MSTR REUSE-ruling, NO new spawn -- ~D built the B1 harness + knows the REACHxUSABILITY data that IS this EFFECTIVE feed; TH-A is a TOOLHEALTH BUILD not a COMPPROOF solve, so ~D's isolation-bar does NOT apply). GATE CLEARED: COMPPROOF-B1 blind-run + judge + aggregate DONE (report.json 6e28d8768, 55.6%, CVO~B-reproduced). ~D's cot-C_00 filler YIELDS to this. On landing -> feeds TH-B Phase-B's pre-wired --effective-feed join = full 4-verdict. Flip staged->pending on start; RAVC COO~B CC CTO+CVO~B. -->

<priority>HIGH -- the EFFECTIVE axis is the genuinely-NEW capability of TOOLHEALTH (deliverable a). GATED on COMPPROOF-B1 harness. PRD docs/architecture/NFRA_TOOLHEALTH_PRD.md SS2/SS3 + arch-gate SS5.2.</priority>
<date>2026-07-02</date>

## Context
NFRA_TOOLHEALTH fuses three axes into a per-tool health verdict. USED + RAIL-CONSISTENT already exist (COMPLEARN-LIVE). The EFFECTIVE axis is NEW: log-mining alone (used + low-rail-escape) CANNOT tell you a tool actually *reaches the answer* -- only a blind-run can. COMPPROOF-B1 (`org/modules/graph/compproof/`, same fleet) already built a blind-run REACH x USABILITY harness for the top-20 INCIDENT corpus. **TH-A generalizes that harness from per-INCIDENT to per-TOOL/per-CLASS: does running comp-tool X actually reach a usable answer for the class of question it claims to serve?** REUSE B1's harness + isolation gate un-forked -- do NOT re-invent blind-run.

## Objective
Stand up a RECURRING per-tool/per-class EFFECTIVE probe (REACH x USABILITY, isolation-gated) that emits, per tool, a periodic effectiveness verdict into the tool_activity substrate as a new probe stream that TH-B's health query reads.

## Scope
1. **Per-tool probe design (extend B1, do NOT fork):** for each comp-tool (or tool-class), define a small set of representative blind questions the tool claims to answer; run the B1 blind-solver (fresh agent, symptom/question-only, answer sealed) against the LIVE estate; score REACH (did the tool reach the answer) x USABILITY (usable-in-the-moment -- a >150s-under-load timeout / fell-back-to-raw = FUNCTIONAL PARTIAL, not EFFECTIVE). One home `org/modules/graph/compproof/` (shared with B1) -- no scatter.
2. **Isolation carry-over (HARD gate, VOID-on-violation):** author != solver != judge; the probe payload PROVABLY excludes the answer (the B1 diff-gate pattern). A tool tuned on its own eval = a void EFFECTIVE verdict.
3. **Recurring cadence + emit:** the probe runs on a schedule (not one-shot); emit `{tool, class, reach, usability, effective in [yes|no|unknown], probe_ts, isolation_ok}` into the tool_activity substrate as a NEW probe stream (append, do NOT mutate COMPLEARN's owned tables/scorer).
4. **Demonstrate FIX-surfacing on >=1 real tool:** show a tool that is heavily USED + rarely-bypassed yet scores EFFECTIVE=no (the load-bearing FIX catch only this axis surfaces).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-which "how do I run the COMPPROOF blind-run harness against a comp-tool"; read org/modules/graph/compproof/ + the NFRA_COMPPROOF.B1 harness + docs/architecture/NFRA_COMPPROOF_B_HARNESS_DESIGN.md; confirm the tool_activity write path (COMPLEARN-owned) that a NEW probe stream can append to WITHOUT forking the scorer</run>
    <expect>The B1 harness + isolation mechanism understood; the tool_activity append surface identified as ADD-a-stream (not modify COMPLEARN's tables/scorer). One home confirmed.</expect>
    <if_mismatch>STOP. If the only write path mutates a COMPLEARN-owned table, coordinate the substrate extension with the COMPLEARN owner + COO~B before writing -- do NOT fork the substrate.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>self-test the per-tool probe on >=2 tools (>=1 expected-effective, >=1 expected-FIX): load -> strip -> assert solver payload has NO answer field (isolation gate structurally holds) -> REACH x USABILITY scorer emits effective yes/no -> row appended to the probe stream; ds-commit-gate + non-ASCII + `from __future__ import annotations`</run>
    <expect>Both probes run end-to-end; the isolation gate PROVABLY holds per tool; a used-but-ineffective tool surfaces EFFECTIVE=no (the FIX catch).</expect>
    <if_mismatch>STOP. If the solver payload can see the answer, the EFFECTIVE axis measures nothing (same failure mode B1 guards). Fix before any recurring run.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>run the recurring probe across the live comp-tool set -> per-tool EFFECTIVE verdict appended to tool_activity; hand the EFFECTIVE stream schema to TH-B (health query consumer) + CVO~B (TH-V honesty judge)</run>
    <expect>Per-tool EFFECTIVE rows present in the probe stream on the live substrate; TH-B can join them by tool; isolation held on EVERY probe or that row is VOID.</expect>
    <if_mismatch>A skipped tool or an isolation-broken probe = incomplete. Ground on the LIVE emitted rows (Rule 22), never a self-report the probe ran.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp (same fleet): COMPPROOF-B1 harness is the REUSED input -- generalize per-incident -> per-tool INSIDE the one home org/modules/graph/compproof/; do NOT fork the harness or the isolation gate.
- COMPLEARN owner: tool_activity substrate is COMPLEARN-owned. TH-A ADDS a probe stream (append-only); it MUST NOT mutate COMPLEARN's tables or comp_learns_score.py. Any schema touch = coordinate + COO~B sign-off.
- NFRA_AGENTBUS-S3 (0.4.0_DE): also writes tool_activity (cross-employee meter). The substrate is a 2-project shared surface -- coordinate any schema evolution.
- 3.0.0_SA_CVO~B (TH-V): independently judges EFFECTIVE-verdict honesty (isolation-preserved, not tuned-on-the-eval). Your isolation gate is what makes her scoring meaningful.
- 1.0.0_SA_CTO: arch-gates EFFECTIVE-probe honesty (SS5.2). RAVC him on the REACH x USABILITY rubric binding.
</cross_domain_coordination>

<acceptance_criteria>
1. A recurring per-tool/per-class EFFECTIVE probe exists in org/modules/graph/compproof/, reusing the B1 blind-run harness + isolation gate un-forked; the probe payload PROVABLY excludes the answer (isolation structurally enforced).
2. The probe emits `{tool, class, reach, usability, effective, probe_ts, isolation_ok}` into tool_activity as an APPEND-only NEW stream -- COMPLEARN's tables + scorer are untouched (grep-proof: no diff to comp_learns_score.py or COMPLEARN-owned tables).
3. A used-but-ineffective tool surfaces EFFECTIVE=no (the FIX catch) on >=1 real tool, demonstrated on LIVE (Rule 22).
4. Session-log Compiler Tools section reproduces every `<run>` + observed result + pass/fail vs `<expect>`. RAVC COO~B + CC CTO + CVO~B.
</acceptance_criteria>

## Note
This is the axis that makes TOOLHEALTH more than COMPLEARN. Its entire honesty rests on the blind-solver isolation gate inherited from B1 -- structurally enforced, not by convention. GATED on COMPPROOF-B1 harness being built (it is, per B1 PROGRESS 2026-07-01, self-tested + committed 51196d3a9); the blind-RUN execution phase is the sequencing dependency. Do NOT start until COO~B fires the GO (fleet + gate confirmed).
