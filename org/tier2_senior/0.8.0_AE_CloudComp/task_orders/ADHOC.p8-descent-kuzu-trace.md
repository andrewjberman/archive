<task_order>
<to_id>ADHOC.p8-descent-kuzu-trace</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P2 (dial-program feed: both dials' P8 leg; CTO seat ask 153743Z, seat+trigger concurred 153944Z -- trigger FIRED on your F9+F1 closes)</priority>

<title>P8 independent descent, BOTH instruments in one session: comp-kuzu + comp-trace cold-use stumble capture (non-dialer seat)</title>

<context>
CVO's kuzu and trace dials each carry an open P8 leg: "independent descent -- by definition
needs a non-dialer" (DIAL_RECORD_comp-pipescript_20260804.md P8 row states the class; the kuzu
and trace dial records carry their own P8 rows). You are the concurred seat: comp-tool-fluent,
and your adjacency is comp-pipescript (which you BUILT), not the dialed instruments.

WHAT A DESCENT IS: you USE each tool cold on real questions and record where it stumbles you --
misleading output, dead ends, wrong-looking answers, provenance you could not trust, flags you
guessed wrong, results you had to double-check elsewhere. The stumbles ARE the deliverable;
CVO folds them into the dial records (their re-dial trigger class). A descent that reports
"everything fine" after N questions is a valid result ONLY with the questions + outputs shown.

INDEPENDENCE MECHANIC (load-bearing, order matters): run your descent BEFORE reading either
dial record. A descent conducted after reading the dialer's findings re-walks the dialer's
path -- that is a review, not a descent. Read the dial records ONLY in Phase 2, to diff your
stumbles against their findings.
</context>

<scope>
1. Per instrument (comp-kuzu, then comp-trace): derive 6-10 REAL questions from your own recent
   work (things you actually wanted to know this week -- estate structure, dependency reach,
   node lineage), not synthetic toys. Run them cold. Capture verbatim: invocation, output (or
   the relevant slice), your read of it, and any stumble -- classified {MISLEADING / DEAD-END /
   WRONG-FLAG-GUESS / UNTRUSTED-PROVENANCE / HAD-TO-VERIFY-ELSEWHERE / CLEAN}.
2. Where an output looks wrong, ground the truth independently (source/live state) before
   recording it as MISLEADING -- a stumble claim is itself a claim needing evidence.
3. Phase 2 ONLY: read both dial records; diff your stumble set against their findings -- what
   did the dial miss that cold use found, and what did the dial flag that cold use never hit.
4. No tool edits, no fixes -- findings only. Fix routing is CVO's fold.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="descent (BEFORE reading any dial record)">
    <step>
      <run>comp-kuzu / comp-trace on your derived question set (6-10 each), verbatim captures</run>
      <expect>Every question logged with invocation + output slice + classification; zero dial-record reads before this phase completes (state it explicitly in the log).</expect>
      <if_mismatch>If you have already read a dial record for one instrument, SAY SO -- that instrument's leg downgrades to REVIEW, not DESCENT; do not present it as independent.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="after descent">
    <step>
      <run>read both dial records; produce the diff (cold-found-vs-dial-found, both directions)</run>
      <expect>A stumble table + the two-direction diff, every MISLEADING claim grounded.</expect>
      <if_mismatch>An ungrounded MISLEADING claim is INFERRED -- label it or ground it.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="report">
    <step>
      <run>deliver to 3.0.0_SA_CVO (the fold owner) + 1.0.0_SA_CTO + me; commit the descent record under your folder</run>
      <expect>CVO can fold without a follow-up ask; the P8 rows in both dial records get their closure citation.</expect>
      <if_mismatch>REWORK per CVO's fold needs.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only on both instruments; no files shared with live builds. CVO's comp-blast re-dial is
event-armed on ~A's edits -- if a comp-blast question sneaks into your set, fine (it is not a
dialed-instrument read), but the P8 legs you close are kuzu + trace only.
</cross_domain_coordination>

<acceptance_criteria>
1. Stumble table per instrument (6-10 real questions each, verbatim invocations + outputs +
   classifications), with the explicit no-dial-record-read-before-Phase-2 statement.
2. Two-direction diff vs both dial records.
3. Every MISLEADING claim grounded or labeled INFERRED.
Plus: session log Compiler Tools section reproducing the runs. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ask">CTO 153743Z seat ask + 153944Z concur (seat=you, trigger=your F9/F1 closes -- FIRED 155259Z)</ref>
  <ref type="dials">CVO comp-kuzu dial record (@395aaf053 close) + comp-trace dial record (in flight at CVO -- confirm its close before starting that leg; kuzu leg can start now)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
