<task_order>
<id>NFRA_VELOCITY_ESTATE.WS-E2.trigger-graph-resequencing</id>
<project>NFRA_VELOCITY_ESTATE</project>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>active</status>

<priority>P2 -- THE CRITICAL PATH. NFRA_VELOCITY is the EXCLUSIVE work regime (Andrew GO 2026-07-31 ~0225Z). P1 is COMPLETE (E4.1 closed @c9cc2ea22a, E1 specimen landed @0bdca276e8, E3.0 safe slice executed @2da40ba711). WS-E2 is one of P2's two halves and it is UNGATED as of @e8c7a32fa2 (section-5.9 product baselines satisfied -- the BASELINE-BEFORE-TOUCH fence that held this workstream is DISCHARGED).</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_ESTATE_PRD.md -- WS-E2 (lines 79-93). Read the acceptance clause in full; it is four separate bars, not one.</ref>
  <ref type="spec">base CTO (1.0.0_SA_CTO) sequencing spec, msg 20260731T133230Z + the pinned-before trigger-census rider (143 rules + 11 schedulers at last measure). THE SPEC IS AUTHORITATIVE where it and this TO disagree -- route the disagreement to me, do not silently pick.</ref>
  <ref type="seed">docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md -- the seed map, NOT the denominator. It is a prior belief to be falsified, not a population to trust.</ref>
  <ref type="law">CLAUDE.md NEVER-rule: "A PRODUCTION PIPELINE MUST HAVE A SCHEDULE. A pipeline whose only trigger is another pipeline's success has no schedule and is a defect." The measured instance is `mdpf-daily-refresh-trigger` (ScheduleExpression: None) freezing the client-facing Model Portfolios product for six days when INF died 07-18.</ref>
  <ref type="conflict">0.7.0_AE_CloudOps~D @abb3ed61a6 + @4c8e65ed3e -- ~D recorded an "E2 blast-surface conflict" and an E2 process-defer characterized as a DELIBERATE OVER-APPROXIMATION THAT SHRINKS. Read both before you touch a shared surface; ~D is on an Andrew-flagged HOLD and cannot be asked live.</ref>
</references>

<objective>
Derive the full trigger graph with a TWO-SYSTEM denominator, type every edge against the declared D2
paths, and re-sequence the violations.

>> YOUR FIRST ARTIFACT IS THE CENSUS, AND IT IS THE ONLY THING I WANT BEFORE YOU REPORT BACK. <<

Not the full acceptance list. Not a plan. ONE artifact: **the two-system trigger census as a queryable
surface with BOTH denominators printed and independently re-derived live.** Land that, report, then we
iterate on typing and fixes. (This instruction is itself a lesson the CORE fabric bought this session:
a lane that sits on a full acceptance list before starting cost ~2h. Fast first artifact, then iterate.)

The census is done when it can answer, with a number and a provenance line: how many trigger edges
exist, in EACH system, and which of them fire against a pipeline that has no schedule floor.
</objective>

<constraints>
1. **TWO SYSTEMS OR IT IS NOT A DENOMINATOR.** `aws events list-rules` is STRUCTURALLY BLIND to
   EventBridge Scheduler -- this is the PRD's named specimen #2. A census that enumerates only Rules
   is not a smaller census, it is a DIFFERENT MEASUREMENT that reports healthy about a population it
   cannot see. You need `list-rules` AND `scheduler list-schedules`, each with its own count.
2. **143 + 11 IS A CARRIED NUMBER, NOT YOUR MEASUREMENT.** It is in the rider so you can detect
   drift, not so you can restate it. Re-derive both live and print what YOU got. If your number
   differs from the rider, that difference is a FINDING and I want it -- do not reconcile it silently
   in either direction.
3. **PRINT THE DENOMINATOR OF EVERY SCAN YOU REASON FROM** (Rule 22). A trigger census that reports
   "N violations" without "of M edges, enumerated at run time from both systems" is not actionable
   and I will send it back.
4. **NO ALARMS, NO MONITORS, NO FRESHNESS CHECKERS, NO SNS, NO SES.** Standing moratorium
   (Andrew-direct 2026-07-28), and it binds this workstream hard because a trigger census is the
   single most tempting place in the estate to reach for one. A finding lands as a GATE or an OWNED
   BLOCKING ITEM. **The correct deliverable here is a SCHEDULE, not a detector that notices its
   absence** -- and that is exactly what makes the moratorium right rather than merely restrictive.
5. **A FIX IS NOT LANDED UNTIL IT IS EXERCISED.** The PRD says the re-sequenced run must be observed
   firing in order FROM THE RUN'S OWN LOG. Never manufactured. An ad-hoc run is a legitimate QA
   instrument (NEVER-rule (a)) but its artifacts are NEVER production evidence.
6. Terraform is the only mechanism for any trigger change (`safe-apply`, never bare `terraform apply`).
   A deploy that begins FINISHES in-session or rolls back loud -- open a deploy-completion ledger entry
   in `org/critical_paths/change_management/` at deploy-start.
7. No emojis / non-ASCII anywhere.
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before the census">
    <step>
      <run>comp-which "what triggers fire the gold pipelines and what is their schedule"</run>
      <expect>Routes to the estate/trigger tool with dependency context. Establishes what the GRAPH believes before you measure what AWS holds -- the delta between them is itself a finding.</expect>
      <if_mismatch>If comp-which dead-ends, that is a coverage gap in the rail -- record it and report; a repeat override for one intent means the tool should be built.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="the census itself">
    <step>
      <run>aws events list-rules  AND  aws scheduler list-schedules -- separately, each count printed, paginated to exhaustion  # rail-checked: two-system live enumeration is the DENOMINATOR itself; comp-tools model the TF-DESIRED view and structurally cannot report what is APPLIED in Scheduler</run>
      <expect>Two independent counts. Paginate to exhaustion -- a truncated list is a silently-wrong denominator, which is more dangerous than a zero.</expect>
      <if_mismatch>A count that cannot be reconciled to the rider is a finding, not an error to hide.</if_mismatch>
    </step>
    <step>
      <run>Positive control: confirm the census FINDS a trigger you already know exists (mdpf-daily-refresh-trigger) and correctly reports its ScheduleExpression as absent</run>
      <expect>The known instance appears AND is flagged. A sweep that cannot find a known-present instance is a broken instrument reporting silence.</expect>
      <if_mismatch>Fix the instrument before trusting any count it produced.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="before any fix lands">
    <step>
      <run>comp-blast on the trigger/Lambda surface you intend to change</run>
      <expect>The consumer set of the thing you are re-sequencing. Rule 20: check the dependency graph BEFORE you change anything.</expect>
      <if_mismatch>An unexpected consumer is a STOP and a route to me.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
FIRST ARTIFACT (report on this ALONE, then iterate):
1. The two-system trigger census exists as a queryable surface, with the EventBridge Rules count and
   the EventBridge Scheduler count printed SEPARATELY, each re-derived live and paginated to
   exhaustion, each carrying its provenance (command + timestamp with a COMPUTED offset, never a
   hand-typed Z).
2. The positive control is stated: a known-present trigger the census found, run separately from the
   target.
3. Any drift from the carried 143+11 is named as a finding, in whichever direction it moved.

SUBSEQUENT (do NOT block artifact 1 on these; they are the workstream, not the first step):
4. Every trigger edge typed against the declared D2 paths.
5. The unscheduled-production-pipeline population enumerated with its denominator -- the
   schedule-floor violations. `mdpf-daily-refresh-trigger` is the known member; it is the seed of the
   population, not the extent of it.
6. Zero unscheduled production pipelines (the PRD bar), each fix landed through safe-apply + a closed
   deploy-completion ledger entry.
7. The specimen-class mis-sequence made structurally impossible without a loud typed violation.
8. Every fix EXERCISED -- the re-sequenced run observed firing in order from the run's OWN log.
9. Session log with a Compiler Tools section reproducing each run vs expect.
</acceptance_criteria>

<cross_domain_coordination>
- **base CTO (1.0.0_SA_CTO) is the ARCH-GATE.** The 133230Z spec sequences this work. Gate before land
  on anything that changes a live trigger. CTO is currently HELD at its own step 3 on a `locality`
  enum schema-gap -- that hold is on CORE vocabulary, NOT on your census, and does not gate artifact 1.
- **base CVO (3.0.0_SA_CVO) verifies.** Section-5.9 is already SATISFIED @e8c7a32fa2 -- that is what
  ungated you. Do not re-litigate it.
- **`0.7.0_AE_CloudOps~A` OWNS THE AUG-1 14:00Z ETFS MONTH-END FIRE -- HARD DEADLINE TOMORROW.** It
  shares your base serial's lane. **Do not touch the ETFS/inf trigger surface or the mdpf-daily-runner
  without routing to me first.** ~A has verified that fire READY at the runtime layer; a trigger
  re-sequence landing between now and 14:00Z tomorrow could silently unmake that. This is the single
  highest-consequence adjacency in this workstream: those CSVs are the ETFS_AVGCAP partner-rebate
  basis -- they decide what a partner is paid.
- **`~D` is on an ANDREW-FLAGGED HOLD** and recorded an unresolved E2 blast-surface conflict on
  mdpf-daily-runner. Read @abb3ed61a6 and @fbe90aeac0. Do not resolve that conflict unilaterally --
  it is held pending Andrew's scope steer.
</cross_domain_coordination>

<notes>
WHY THE TWO-SYSTEM DENOMINATOR IS THE WHOLE POINT AND NOT A DETAIL: the failure this workstream exists
to prevent is not "a trigger is missing." It is "an instrument reported the trigger population and was
structurally incapable of seeing half of it, and every downstream claim inherited that blindness while
reading confident." `list-rules` returning 143 clean rules is not evidence about the 11 schedulers --
it is silence about them, and silence renders as health. This is the same shape as comp-iam's
UNMAPPED-METHOD silence and the `grep -c` on an error message: the control belongs on the RETRIEVAL,
not on the pattern.

WHY THE SCHEDULE-FLOOR VIOLATION IS THE VALUABLE HALF: an event-driven-only pipeline does not fail
loudly. It freezes SILENTLY and INVISIBLY the moment its upstream breaks, with perfectly fresh inputs
sitting unused -- six days of a client-facing product, and no instrument in the estate reported it.
That is the defect class you are enumerating. Every edge you find that fires only on another
pipeline's success is a future six-day outage that nobody will be paged for, because there is nothing
to page.
</notes>
</task_order>
