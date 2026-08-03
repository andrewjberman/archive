<task_order>
<to_id>MDPF_GLOBAL.T2C.synchronized-cadence</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<date>2026-08-03</date>
<status>pending</status>
<priority>P1 (second wave on the s.C.4 spine; unblocked by the T2.B ruling @440d16e018. SEQUENCING: begin AFTER your T1.A census commits -- T1.A stays first; this TO is your queued next.)</priority>

<title>T2.C: The canonical MDPF clock -- one declared, implemented, and proven daily cadence (silver-close -> revamp rebuild -> accrual -> publisher -> invalidation)</title>

<context>
MDPF_GLOBAL PRD Addendum C s.C.4 T2.C row, unblocked 2026-08-03 20:59Z by the CTO T2.B ruling
@440d16e018 (full text PRD s.C.3). Binding terms:
(1) canonical serving lineage = revamp/hyphen family (opal-data-assets silver -> revamp gold ->
    accrual bridge -> publisher -> platinum/mdpf/{scope}/);
(2) canonical frontier = T-1 settled close, declared in served _provenance;
(3) THE FREEZE FIX -- THE CORE OF THIS TO: a dedicated daily schedule on the PRODUCING tree (the
    revamp rebuild) timed after T-1 silver close, with the INF completion event demoted to
    ACCELERATOR-ONLY. This is NEVER#4 implemented: a production pipeline must have a schedule;
    event-driven is fine as an accelerator. The 08-03 live incident (INF pipeline-failed froze the
    only producer; accrual+publisher faithfully re-served the frozen vintage -- T2.A diagnosis
    @0b5acf3148) is the exact failure this schedule floor closes.

DELIVERABLE SHAPE: one declared cadence (time + tz + DST posture) for ingest->gold->publish, all
four scopes + global, documented as the canonical MDPF clock -- AND implemented (the schedule
exists and runs) -- AND proven (3 consecutive trading days at frontier).

YOUR T1.A CENSUS IS THE PRECONDITION IN PRACTICE: the trigger map tells you what exists before you
add or re-point anything. Do not begin until your census is committed.
</context>

<scope>
1. DECLARE the clock: end-to-end timing chain (T-1 silver close -> revamp rebuild -> accrual
   bridge -> publisher -> cache invalidation window), explicit tz + DST posture, all four scopes +
   global, documented in your deliverables folder as the canonical MDPF clock doc. Coordinate the
   invalidation slot with T3.A/T3.B (~F) and the cottonwood leg with T1.C (0.2.0_DS) -- their
   schedule values come FROM your declaration.
2. IMPLEMENT: dedicated daily schedule on the revamp rebuild (EventBridge Scheduler), timed per
   the declaration; INF completion event demoted to accelerator-only (the event edge stays as an
   accelerator, the schedule is the floor). ALL deploy law binds: Terraform only, commit-before-
   apply, .tools/safe-apply.sh, 0-diff, tag + push --follow-tags (integrator-push discipline --
   coordinate the push with MSTR), comp-iam service + live simulate-principal-policy
   (one --resource-arns per call, positive control as a separate invocation) for any new
   resource access, lambda-source-map updated if any Lambda changes.
3. PROVE: 3 consecutive trading days -- all four scopes' served artifacts advance to the SAME
   expected frontier within the declared window (timestamps read LIVE, compared to
   lib/trading_calendar.py frontier); NO hand-runs in the evidence window.
4. NO alarms/monitors/SNS/SES (standing moratorium). The schedule and its run logs ARE the
   mechanism; verification uses existing logs + read-side probes.
5. OUT OF SCOPE: retiring the runner chain or underscore plane (T5, gated on CANON PROVEN + the
   delta census); the cache invalidation IMPLEMENTATION (T3.B, behind this TO + T3.A).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>your own T1.A census (committed) + comp-estate mdpf</run>
      <expect>Every existing trigger on the MDPF chains known and dispositioned; the census IS the baseline this TO mutates against.</expect>
      <if_mismatch>STOP. No schedule work on an uncensused trigger surface.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on every fn/artifact the schedule touches; comp-iam service on any Lambda whose triggers change</run>
      <expect>Consumers + IAM posture enumerated BEFORE the TF change; comp-iam treated as floor, not sufficiency (Rule 22a).</expect>
      <if_mismatch>STOP. Route gaps before apply.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>terraform plan via .tools/safe-apply.sh flow (commit-before-apply); live aws iam simulate-principal-policy for any new (action, resource) pair -- one resource per call, separate positive control</run>
      <expect>Plan matches the declared clock exactly; IAM verified on the live primitive; HALTGT checkpoint honored.</expect>
      <if_mismatch>STOP. A plan that does more than the declaration is scope creep at the apply boundary.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>0-diff re-plan + tag + push --follow-tags (with MSTR for the push leg); then the 3-day live frontier evidence collection (timestamps live vs lib/trading_calendar.py)</run>
      <expect>0-diff clean; 3 consecutive trading days all-scope frontier-advance within the declared window; zero hand-runs.</expect>
      <if_mismatch>A missed cycle = diagnose the mechanism before restarting the 3-day clock; report to COO+CTO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
YOU OWN THE CLOCK; THREE CONSUMERS WAIT ON ITS VALUES: T1.C (0.2.0_DS, cottonwood schedule
timing), T3.B (~F, invalidation slot), and the T5 retirement sequencing. Declare EARLY (scope item
1 needs no infra) and MCP the declaration to 0.2.0_DS_PortfolioAnalytics + 0.7.0_AE_CloudOps~F +
COO + CTO before implementing. Your lane-sibling ~F is censusing serve-path caches concurrently
(read-only, no conflict). The mdpf-daily-refresh-trigger demotion touches the trigger your own
T1.A census dispositions -- census first, mutate second. deploy-completion ledger entry per
NEVER#7 (a begun deploy finishes in-session or rolls back loud).
</cross_domain_coordination>

<acceptance_criteria>
Verbatim s.C.4 (CTO validates at close):
1. 3 consecutive trading days: all four scopes' served artifacts advance to the SAME expected
   frontier within the declared window (timestamps read live, compared to lib/trading_calendar.py
   frontier).
2. No hand-runs in the evidence window.
Plus the T2.B ruling terms implemented: schedule floor on the producing tree; INF event =
accelerator-only (s.C.3 @440d16e018).
Plus the CTO CLOCK-V2 MANDATE (213314Z, superseding the 212557Z discretionary form): v1 is
FACTUALLY CONTRADICTED by measurement (declared 13:00Z close vs inputs measurably landing
~14:16Z) and is the contract T1.C/T3.B consume -- RE-DECLARE v2 BEFORE anything implements
against v1. Binding form: whole clock ET-anchored (America/New_York); the declared close DERIVED
from the measured per-input landing table (both DST regimes represented); floor placed off that
close; double-fire proof unchanged. v2 is a doc commit to the same consumer set (0.2.0_DS + ~F +
COO + CTO); content within that form remains yours.
Plus the CTO CANON-PROVEN sharpening (212847Z, forced by the 6c find -- PRD amendment in CTO's
lane): a green cycle is evidenced by PER-STAGE status reads (every stage rc + every scope's
artifact advancing), NEVER by the chain's terminal completion marker alone -- STAGE6-REVAMP
errored five straight days while the chain reported complete. A cycle whose terminal marker says
complete while any canonical stage errored is a RED cycle. Design your 3-day evidence collection
on per-stage reads from day one.
Plus the CTO inflection carry-window pre-rule (221952Z direct to assignee, folded 2226Z):
2 TRADING DAYS on the BD_MAX_LAG precedent, roster-declared, with three labeling requirements --
every carried point LABELED as carried; the transition to None VISIBLE (never a silent
carry-forever); the window value STATED in served meta.
Plus standing norms: every causal claim cites file:line @ commit or is labeled INFERRED; no new
alarms/monitors.
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/MDPF_GLOBAL_PRD.md (s.C.3 T2.B ruling @440d16e018 + s.C.4 T2.C row)</ref>
  <ref type="evidence">T2.A diagnosis @0b5acf3148 (the freeze mechanism this schedule closes)</ref>
  <ref type="census">Your MDPF_GLOBAL.T1A deliverable (precondition baseline)</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3; CTO T2.B ruling msg 20260803T205937Z</ref>
</references>

<dependencies>
  <dependency agent="1.0.0_SA_CTO" task="T2.B producer-unification ruling" status="complete"/>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_GLOBAL.T1A.trigger-route-census" status="pending"/>
</dependencies>
</task_order>
