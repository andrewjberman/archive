# Task Order: NFRA_PROMOTE P3 -- the reversibility loop (post-promotion monitoring + auto-demote-on-degradation)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-07-nfra-promote-p3</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~Z (the STANDING MONITOR leg -- REDIRECTED 2026-07-14 per SOVEREIGN REDIRECT @ 14c2aeeba row "NFRA_PROMOTE.P3 (standing monitor leg)" + AMENDMENT-1 @ 552667ccd) + 0.5.0_AE_OpalETL (the in-VPC cse_coevolution measure + frontend-co-occurrence gap -- NOT moved by the redirect table) + 0.8.0_AE_CloudComp~D (demote seam -- dead lane, NOT moved by the table; surface at next staffing pass) + 0.4.0_DS_ClientPlatform~B (reallocated from the down DS~A -- NOT moved)</issued_to>
    <date>2026-07-07</date>
    <status>staged -- GO on PROMOTE-P2 + FEDOBS-P3 both. REDIRECT-ACK FOLD (per CVO~Z 072211Z, 2026-07-14): agent-side ACK landed 071744Z (orphan-recovered handoff); 22b caveat CLOSED. FIRST-TOUCH SURVEY (0.8.0~Z): the standing-monitor CODE substantially EXISTS -- promote_monitor.py (0.5.0-authored 07-08, fedobs/): detect+propose default, CTO-governed --arm with the 3 conditions (flapping guard >= persistence, NOTIFY+audit, recovery->RE-PROPOSE-never-auto-re-promote), self-test; my leg = exercise + wire the MONITORED tail into the governed lifecycle + the scheduled standing tick (cadence ride-along is 0.7.0-apply-gated). !! RECONCILIATION FINDING (surfaced 2026-07-14 ~084xZ to CTO~Z for arch ruling): TWO P1 lifecycle implementations exist -- DS~B's NFRA_PROMOTE_P1_promotion_engine.py (07-08, deliverables-side; DROPPED state; invariant-2 as a co_sessions signal-vs-noise measurement floor; FEDOBS_RATIO_FLOOR=0.15 consumed by promote_monitor) AND 0.8.0~Z's comp_promote_lifecycle.py (07-14, org/modules/graph, CVO-certed 1952bb774; governed @0.4 CSE emission per transition; receipt-exercise gates). Parallel-built unknowingly (deliverables dir missed in the pre-build sweep); BOTH kept until CTO~Z rules the canonical home; promote_monitor is NOT rewired unilaterally. PRIOR: 0.5.0 respawn requested (FEDOBS monitor + the in-VPC measure that closes the CANDIDATE->MEASURED gate).</status>
    <prd_ref>docs/architecture/NFRA_PROMOTE_PRD.md (P3 + AC4/AC5)</prd_ref>
    <dispatch_state>STAGED -- GO at Wave-4, AFTER PROMOTE-P2 (materializers) + FEDOBS-P3 (post-promotion measure). Authored by COO~B on the NFRA full-program completion drive. This is what makes promotion SAFE to do at all.</dispatch_state>
    <gate_note>Gated on PROMOTE-P2 + FEDOBS-P3. The LAST arm -- closes the Feedback Contract loop (promote -> monitor -> demote-if-degraded). This is the acceptance-run's reversibility leg.</gate_note>
  </metadata>

  <objective>Wire post-promotion monitoring (FEDOBS measures each LIVE promotion on an interval) + the auto-demote-on-degradation path (reversal, evidence-logged). This is the invariant that makes promotion safe: every promoted directive can be un-done if it later degrades.</objective>

  <requirements>
    <requirement id="1">POST-PROMOTION MONITORING (AC4): FEDOBS measures each live promotion's effect on an interval (the MONITORED state of the lifecycle state machine).</requirement>
    <requirement id="2">AUTO-DEMOTE demonstrated END-TO-END (AC4): promote -> FEDOBS-measured degradation -> auto-demote (reversal), with the degradation evidence logged.</requirement>
    <requirement id="3">INSPECTABLE (AC5): every promotion AND demotion is CSE-logged + cites its observed evidence + measured effect + decompression chain. No promotion/demotion without a full provenance trail.</requirement>
  </requirements>

  <cross_domain_coordination>
    - NFRA_PROMOTE.P2: the materializers whose outputs this monitors + demotes. HARD PREREQUISITE.
    - NFRA_FEDOBS.P2/P3: the directive-effectiveness measurement + standing surface that drives the monitor. HARD PREREQUISITE.
    - NFRA_CSE: the CSE log where every promotion/demotion state-transition is recorded.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. A promoted directive that degrades is AUTO-DEMOTED, exercised end-to-end (promote -> degrade -> auto-demote) with evidence, on live state (Rule 22).
    2. The full promotion lifecycle (CANDIDATE->MEASURED->PROPOSED->RATIFIED->MATERIALIZED->MONITORED->SUSTAINED|DEMOTED) is CSE-logged + inspectable.
    3. This is the loop-close reversibility leg -- feeds the program's end-to-end acceptance run. RAVC COO~B + CC CTO; CVO verifies the auto-demote actually fires on a real degradation (exercise, not config).
  </acceptance_criteria>
</task_order>
```
