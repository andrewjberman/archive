<task_order>
<to_id>MDPF_GLOBAL.C2.dim-aggregate-567-fail-loud</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-03</date>
<status>complete</status>
<status_note>Flipped pending->complete 2026-08-04T1545Z by assignee (stale-line reconciliation, evidence-cited): :567 bare-except goes FAIL-LOUD @0f0f173351 (exercised BOTH directions, raise path traced to STAGE6-REVAMP per-stage status, CTO gate grant 221736Z); deploy-completion ledger @0273788ff6 (MATCH). Sibling :621 finding routed and closed as C2b.</status_note>
<priority>P1-small (T5.B precondition C2, CTO dispatch concurrence 221736Z: "author it NOW, pre-T5.B" -- a live silent-fail defect on a carry-read whose urgency does not depend on retirement timing)</priority>

<title>C2: dim_mdpf_aggregate_aua_timeseries.py:567 -- the bare except swallowing the json/mdpf carry-read to {} goes FAIL-LOUD; fix EXERCISED, not asserted</title>

<context>
The banked json/mdpf retire blocker (MEMORY standing; annotated on every json/mdpf row of ~F's
T5.A kill-list @b877dbc0f5): dim_mdpf_aggregate_aua_timeseries.py:567 wraps the legacy-mirror
carry-read (:569) in a bare except that swallows to {} -- so a frozen, corrupted, or absent
mirror read FAILS SILENT and the output simply loses whatever the carry contributed, with no
error surfaced anywhere. T5.B cannot retire the json/mdpf plane safely until this read fails
LOUD instead of empty.

CTO GATE GRANTED FOR THIS EXACT SCOPE (221736Z): the producer file carries 13 corpus HOLD claims
-- the grant covers the :567 bare-except ONLY; NO other change to that file rides along. One
hunk, surgical.

CTO'S ACCEPTANCE REQUIREMENT, VERBATIM CLASS: "a bare except swallowing to {} is the archetype
of a defect whose fix passes review while remaining untested; a passing assertion never mutated
has never been tested." The fix must be EXERCISED: force the failing path and prove the error
now SURFACES.

DESIGN NOTE (yours to finalize): fail-loud means the failure is OBSERVABLE where the chain reads
it -- per today's CANON-PROVEN sharpening, a per-stage status=error that the chain telemetry
carries (not merely a raised exception that some outer handler re-swallows -- TRACE the exception
path outward before choosing the mechanism; another swallow above :567 would reproduce the
defect one layer up).
</context>

<scope>
1. Replace the :567 bare except with explicit, narrow handling that surfaces the failure loudly
   into the chain's per-stage status (mechanism per your outward trace). The carry-read's
   SUCCESS behavior is byte-identical -- this changes only the failure path.
2. EXERCISE both directions in scratch (zero production writes): (a) failing path FORCED (absent
   key / malformed body against the read) -> the error SURFACES observably, captured verbatim;
   (b) success path on real inputs -> output identical to pre-fix (hash-compare).
3. Deploy per Rule 13 (commit-gate, safe-deploy, comp-pipescript deployed MATCH -- note the tool
   needs --pipeline mdpf per your own T2.A finding), change-management ledger entry.
4. NOTHING else in the file changes. If the outward trace reveals a second swallow above :567,
   that is a FINDING routed to CTO -- not an in-scope fix.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read :560-580 + outward exception-path trace at pinned commit; comp-blast dim_mdpf_aggregate_aua_timeseries</run>
      <expect>The bare except + swallow-to-{} confirmed at vintage; exception path to the chain status writer traced; HOLD claims re-read (the CTO grant is your authorization, cite it in the commit).</expect>
      <if_mismatch>STOP. If :567 has moved or been fixed, re-ground before any edit.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="exercise, before deploy">
    <step>
      <run>scratch exercise: forced-failure (absent/malformed mirror) + success-parity (real inputs, hash-compare)</run>
      <expect>Failure SURFACES observably in per-stage status; success output byte-identical pre/post.</expect>
      <if_mismatch>STOP. A fix that cannot demonstrate its own failure-surfacing is unproven -- keep working or route the design question to CTO.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>comp-pipescript deployed --pipeline mdpf MATCH verify + ledger entry + report to COO + CTO with both exercise captures</run>
      <expect>MATCH; ledger closed same-session; report carries the forced-failure evidence verbatim.</expect>
      <if_mismatch>An unexercised close is REWORK per the CTO acceptance requirement.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Same producer file as the T2.B-ruled canonical chain -- the CTO grant scopes this to one hunk;
your own T1.C work does not touch this file. T5.B consumes this fix as precondition C2; ~F's
kill-list rows reference it. Tonight's scheduled cycle: if your deploy lands before the cycle,
say so in the report so the cycle read attributes any new loud error correctly (a surfaced
error on a frozen mirror would be the fix WORKING).
</cross_domain_coordination>

<acceptance_criteria>
1. The :567 bare-except replaced, one hunk, nothing else in the file (diff shows exactly one
   logical change); commit cites the CTO gate grant 221736Z.
2. EXERCISED both directions: forced-failure capture showing the error surfacing observably +
   success-parity hash-compare -- both verbatim in the session log and the report.
3. Deployed with MATCH verify + same-session ledger.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260803T221736Z item (b) -- dispatch concurrence + gate grant + exercise requirement</ref>
  <ref type="kill-list">~F T5.A @b877dbc0f5 (C2 = T5.B precondition; :567 annotated on every json/mdpf row)</ref>
  <ref type="memory">MEMORY standing: json/mdpf retire BLOCKED behind :567</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
