<task_order>
<to_id>MDPF_GLOBAL.T2A.truncation-diagnosis</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-03</date>
<status>complete</status>
<!-- COMPLETE 2026-08-03T2059Z: CTO ACCEPTED (RAVC-4, msg 205937Z). Diagnosis @0b5acf3148 --
     convergence-truncation candidate REFUTED (accrual = ungated content-derived copy; global axis
     = UNION on the 49F frontier); real mechanism = T-1 input frontier at Friday's run (07-30
     measured) + INF pipeline-failed froze Stage 6 + accrual/publisher propagated the frozen
     vintage. Counterfactual exercised on real inputs (scratch as_of_last=2026-07-31 n=454, zero
     production writes, 13 producer HOLDs respected). Acceptance item 2 closed by CTO landing the
     DS patch @440d16e018 (owned-paths lane held). T2.B ruling issued same-window @440d16e018. -->

<priority>P1 (Andrew-direct GO 2026-08-03 ~20:15Z @3e2b23ebb3; this WS gates the CTO's T2.B producer-unification ruling -- the whole T2/T1.C/T2.C arm of the spine waits on your evidence)</priority>

<title>T2.A: Truncation diagnosis -- source-confirm WHY the accrual/hyphen global series ends 07-30 while the runner/underscore plane reached 07-31</title>

<context>
MDPF_GLOBAL PRD Addendum C (docs/architecture/MDPF_GLOBAL_PRD.md s.C.2 T2 + s.C.4 T2.A row).

THE MEASURED STATE (CTO content-grounded 08-03): the scheduled accrual family
(`mdpf-accrual-bridge-daily` cron(45 15 UTC) -> `mdpf-accrual-trigger`) RAN 08-03 12:15 ET and wrote
all four scopes -- but its global series ends 07-30 (Thursday), one trading day behind the Friday
07-31 frontier. The runner/underscore plane (`mdpf_aggregate_aua.py`, event-gated, did NOT run 08-03
because INF wrote pipeline-failed.json) last wrote Friday 07-31 with data through 07-31. The portal
serves the HYPHEN plane (COO comp-routes confirm 08-03: /api/general/mdpf/* -> platinum/mdpf/*,
S3 key platinum/mdpf/aggregate-aua-timeseries.json) -- so the 07-30-ending file IS what clients see.
Andrew's "appears to be delayed somehow" is confirmed at content level.

THE CANDIDATE MECHANISM (currently INFERRED, Addendum C says so explicitly): convergence truncation
on the failed INF leg -- the accrual writer truncates its global emission at the last date ALL
feeders converge, and the failed INF leg pins that at 07-30. YOUR JOB: retire the INFERRED label --
confirm, or refute and name the real mechanism. Both outcomes are wins; an unconfirmed candidate
dressed as a diagnosis is the only failure mode.

HOLD NOTE (COO comp-blast 08-03): `dim_mdpf_aggregate_aua_timeseries.py` carries 13 corpus HOLD
claims (DO_NOT_DECOMMISSION + CI-R11 frontier-guard critical-path docs). This WS is DIAGNOSIS ONLY:
read + replay, ZERO producer edits. Any fix lands in T2.B/T2.C under the CTO ruling, not here.
Also banked (MEMORY): the same file's :567 bare `except -> {}` fails silent -- if your trace crosses
it, note whether it participated; do not fix it here (it is T5.B's enumerated pre-kill fix).
</context>

<scope>
1. Trace the accrual-family emission path at source, pinned at a stated commit: which script writes
   `platinum/mdpf/global/aggregate-aua-timeseries.json` (and the four scopes), and WHAT bounds the
   last emitted date. Cite file:line @ commit for the bounding mechanism.
2. EXERCISE the mechanism: reproduce on the real inputs or a controlled replay -- show that the
   08-03 scheduled run's inputs + the cited code path produce a 07-30-ending global series, and
   (if the convergence candidate holds) that a converged INF leg would have produced 07-31.
   Ad-hoc runs are a legitimate QA instrument here (NEVER#4a) -- but SCRATCH OUTPUTS ONLY: nothing
   writes to any production platinum/json key; replay artifacts are never production evidence.
3. Deliverable: a diagnosis note (your deliverables folder) with the INFERRED label retired --
   CONFIRMED-with-cite-and-exercise, or REFUTED-with-the-real-mechanism (same evidence bar).
4. Follow-up commit editing docs/architecture/MDPF_GLOBAL_PRD.md Addendum C to remove the INFERRED
   label, citing this WS (the s.C.4 acceptance names this commit explicitly).
5. Route the evidence to CTO (1.0.0_SA_CTO) by MCP THE MOMENT IT LANDS -- CTO owes the T2.B
   producer-unification ruling on your diagnosis and is waiting on it. CC COO.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before trace">
    <step>
      <run>comp-estate mdpf</run>
      <expect>2 chains; the accrual/scheduled family + event-gated runner chain both present -- confirms which chain you are diagnosing (the accrual one) and its feeder set.</expect>
      <if_mismatch>STOP. Surface to COO -- the producer map changed under the PRD.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io dim_mdpf_aggregate_aua_timeseries</run>
      <expect>READS/WRITES enumerated; WRITES include the platinum timeseries family; column gaps + portal consumers listed (ModelPortfolios page).</expect>
      <if_mismatch>If the tool cannot resolve the script name, run comp-pipescript io on the actual accrual-family gold script your Phase-1 trace identifies, and note the name mismatch to COO.</if_mismatch>
    </step>
    <step>
      <run>comp-blast dim_mdpf_aggregate_aua_timeseries</run>
      <expect>HOLD claims present (critical-path docs). Confirms the no-edit posture for this WS.</expect>
      <if_mismatch>If HOLDs are absent, still no edits -- the TO scope, not the corpus, is the binding constraint here.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="exercise, before commit">
    <step>
      <run>controlled replay of the bounding mechanism on the 08-03 real inputs (scratch outputs only)</run>
      <expect>The 07-30 truncation REPRODUCES via the cited code path; the counterfactual (converged INF leg -> 07-31) demonstrated or argued from the same cited mechanism.</expect>
      <if_mismatch>The candidate is REFUTED or the mechanism is elsewhere: keep tracing until the reproducing mechanism is found, or deliver REFUTED + best-evidence state and route to CTO -- do NOT ship an unexercised confirmation.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>MCP evidence package to 1.0.0_SA_CTO (cc 2.0.0_SA_COO): mechanism cite file:line @ commit + exercise evidence + diagnosis-note path + PRD label-retirement commit hash</run>
      <expect>CTO ACK -- T2.B ruling proceeds on your evidence.</expect>
      <if_mismatch>Chase per RAVC; silence &gt;1 working window escalates to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only vs production surfaces (scratch replay only). T1.A (0.7.0_AE_CloudOps) is censusing the
triggers of the same chains concurrently -- read-only both sides, no gate. Your diagnosis is the
DIRECT input to CTO's T2.B ruling; T1.C and T2.C are staged behind that ruling. The producer file
carries corpus HOLDs -- no edits from any lane until T2.B rules.
</cross_domain_coordination>

<acceptance_criteria>
Verbatim s.C.4 (CTO validates at close):
1. Mechanism cited file:line @ commit AND exercised (reproduce on the real inputs or a controlled
   replay).
2. The Addendum-C INFERRED label removed by follow-up commit citing this WS.
Plus standing norms: scheduled-run evidence only for any production claim (your replay is QA
evidence for the MECHANISM, never production evidence for the DATA); every causal claim cites
file:line @ commit or is labeled INFERRED and blocks nothing; no new alarms/monitors.
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/MDPF_GLOBAL_PRD.md (Addendum C s.C.2 T2, s.C.3, s.C.4 T2.A row)</ref>
  <ref type="memo">docs/references/MDPF_ARCH_CLEANUP_ANDREW_MEMO_20260803.md</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3 (memo-doc s.5); CTO relay 20260803T200329Z</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
