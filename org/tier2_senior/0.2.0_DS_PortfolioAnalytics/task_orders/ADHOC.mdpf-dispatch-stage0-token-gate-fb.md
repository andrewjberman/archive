<task_order>
<to_id>ADHOC.mdpf-dispatch-stage0-token-gate-fb</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
<date>2026-08-04</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADHOC" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending</status>
<priority>P2 (the F-B class-closer from the Orion-401 root cause; F-A (AE's schedule fix) covers the daily race -- this closes the CLASS for any future token/schedule drift; sequence AFTER your benchmarks-mapping TO)</priority>

<title>MDPF dispatch stage-0: pre-pull token gate -- decode exp locally, bounded SM re-poll near expiry, else fail LOUD named TOKEN-EXPIRED (a gate in the flow, not an alarm)</title>

<context>
Root cause (AE 154737Z, every link source-confirmed): the Orion JWT lives 10h and dies 07:02Z
daily; clock v3 put the floor at the refresher's exact minute; today's pull read the dead token
12 SECONDS before the fresh one landed -- 401 x9, stages 2-5 skipped, the 1-of-4 served plane.
The failure was NONDETERMINISTIC (warm exporter box wins, cold loses): a daily coin flip.

F-A (AE, landing now) moves the refresher to 12:15Z -- that fixes TODAY'S geometry. THIS TO is
the class-closer: the chain itself must never again spend a cycle on a token it could have
KNOWN was dead before pulling. AE's proposed shape, adopted: stage-0 decodes the token's exp
LOCALLY before the first pull; if expired or near-expiry, poll Secrets Manager for advancement
bounded <=5min; if no fresh token arrives, FAIL LOUD with a named TOKEN-EXPIRED error -- so the
run log says WHY in one line, instead of 401 x9 and a skipped chain.

MORATORIUM NOTE: this is a GATE IN THE FLOW -- a chain refusing to run on a provably-dead
credential and saying so -- NOT an alert/monitor/notification. No SNS, no SES, no CloudWatch
alarm ships with this.
</context>

<scope>
<!-- AMENDED 1947Z per 0.2.0_DS's surfaced lane fact: the GATE SCRIPT is DS-lane (landed
     @572e40f2f5, deployed via the new mdpf gate); the DISPATCH WIRING (infra/aws/ec2) is
     CLOUD_OPS_OR_ETL -- owned-paths correctly refused the DS author; that edit sits in-tree
     for AE's author line + runner deploy. "Your runner lane" below reads as this split. -->
1. Stage-0 of the mdpf daily dispatch (your runner lane): before the first Orion pull, decode
   the JWT exp from the secret (local decode -- no network validation call needed; exp is in
   the token). Ground the insertion point file:line first.
2. Decision ladder: exp comfortably ahead (define the margin from pull-duration reality, derive
   it, state it) -> proceed. Expired/near-expiry -> re-read the secret every 30-60s bounded
   <=5min total; a fresh token (new exp ahead of margin) -> proceed with it. Bound exhausted ->
   FAIL LOUD: named TOKEN-EXPIRED error carrying the exp read + the wait spent, chain stops
   BEFORE any pull (prior-state-stays semantics -- no partial bronze, no _meta/-only poisoned
   prefix from a doomed pull).
3. The poisoned-prefix interaction is part of the win: failing BEFORE the pull means no
   _meta/-only partition gets written by a dead-token run (0.4.0's roll-forward fix closes the
   read side; this closes the write side of the same class).
4. NO alarm/notification machinery. NO change to pull logic itself, stages 1+, or the emitters.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>ground the insertion point + the token read path at source (dispatch runner file:line @ commit); comp-pipescript postdeps &lt;the dispatch entry script&gt; --firm mdpf if applicable</run>
      <expect>Stage-0's exact pull-precondition seam named; the secret-read call identified; no other consumer of that read breaks if a gate precedes it.</expect>
      <if_mismatch>STOP. Surface to me + AE if the seam is not where AE's proposal assumed.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>EXERCISE both directions with controlled tokens: an expired-exp fixture -> the gate REFUSES loud with TOKEN-EXPIRED naming exp + wait; a valid-exp fixture -> proceeds untouched</run>
      <expect>Both captured verbatim, separate invocations; the refusal path writes NOTHING to bronze (listing check).</expect>
      <if_mismatch>STOP. A gate that cannot demonstrate its refusal is not a gate.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit + deploy">
    <step>
      <run>deploy per your Rule-13 cycle; report to me + CTO + AE with captures + commit + deployed verify (ETag==md5 class)</run>
      <expect>AE folds it into the 401 close-out record; acceptance rides the next scheduled cycle's clean stage-0 line (observed, per the green-run law -- state it OPEN until observed).</expect>
      <if_mismatch>REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
F-A (AE's refresher move + T2C member-table addition) is landing in parallel -- no shared
files, but the MARGIN you derive in Scope-2 should assume F-A's 12:15Z refresh geometry
(coordinate the number with AE, one message). Your benchmarks-mapping TO sequences FIRST at
your seat. 0.4.0_DS's roll-forward fix is the read-side sibling -- no shared files, shared
class; cite each other in close-outs.
</cross_domain_coordination>

<acceptance_criteria>
1. Insertion point + secret-read path cited file:line @ commit; margin DERIVED and stated.
2. Both-direction exercise captures (refusal writes nothing -- listing evidence; pass-through
   untouched).
3. Deployed verify; scheduled-cycle observation explicitly OPEN until the next real fire prints
   the clean stage-0 line.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="root-cause">AE 154737Z (the 12-second race, source-confirmed chain); CTO 155020Z words (F-B = COO routing)</ref>
  <ref type="sibling">0.4.0_DS roll-forward fix (read-side of the poisoned-prefix class); AE F-A (schedule geometry)</ref>
  <ref type="law">CLAUDE.md moratorium (gate-in-flow is the sanctioned shape); memory/feedback_gate_accepted_on_observed_green_run_never_authoring_commit.md</ref>
</references>

<dependencies>
  <dependency agent="0.2.0_DS_PortfolioAnalytics" task="ADHOC.benchmarks-model-code-mapping-fix" status="sequence-first at your seat (Andrew-active thread outranks)"/>
</dependencies>
</task_order>
