<task_order>
<to_id>ADHOC.graph-tests-hygiene-f10</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P2 (dial F10 + the tests-outside-the-instruments family; originally morning-wave -- pulled forward on Andrew "Proceed" 1706Z + your lane going IDLE post-descent; the not-~D wall applied only WHILE you held the descent, which is complete @150dd98d7)</priority>

<title>Graph-tests hygiene: repair the stale hold-era suite (F10) + enroll it in the F9 gate + the predicate-not-roster sweep of tests/ vs watch globs</title>

<context>
CVO re-dial finding F10 (@37bf63f4a): org/modules/graph/tests/test_extract_column_gaps_bd_hold.py
-- 3 tests RED since the 07-14 sovereign-hold retraction, unobserved because the file predates
your F9 gate's test_pipescript_* auto-enroll glob. THE ENGINE IS RIGHT (SOVEREIGN_HELD_PATHS=()
is the correct post-retraction state per Andrew's verbatim + CTO's 07-22 predicate split); the
TESTS are stale hold-era assertions -- the same superseded-contract class as the four the dial
repaired, in a 5th file the gate cannot see. The F9 rot class survives wherever the glob cannot
see. Composes with your own routed finding: test_adapter_audit.py is COLLECTION-BROKEN at HEAD
(imports deleted adapter_audit_cli.py) -- that half is with CTO~B's RCG lane; your sweep NAMES
it in the census but does not fix it (lane boundary).
</context>

<scope>
Per CVO's recommended shape, verbatim intent:
1. Repair the 3 tests to post-lift truth: assert the bd read HAPPENS now, and test the guard
   MECHANISM against INJECTED held values rather than the lifted governance set -- the mechanism
   stays testable while correctly holding nothing.
2. Enroll-or-rename the file so the F9 gate watches it (your own gate; the watch list derives in
   ONE place -- extend the derivation, never a second list).
3. The predicate-not-roster sweep: enumerate tests/ vs the watch globs + pytest collection
   health; emit the census (every test file -> watched/unwatched + collects/broken). Findings
   route: unwatched-repairable -> this TO fixes or names; collection-broken from mass-deletion
   -> NAMED to CTO~B's RCG lane, not fixed here.
4. No engine edits. CVO verifies the repaired tests on landing (their standing dial scope).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>python -m pytest org/modules/graph/tests/test_extract_column_gaps_bd_hold.py -q (pipe-free rc)</run>
      <expect>3 red reproduced (pre-fix control), captured verbatim.</expect>
      <if_mismatch>STOP -- if green, someone repaired it since the dial; re-ground with CVO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>repaired tests: green at post-lift truth AND the injected-held-values mechanism case shown DISCRIMINATING (a mutant injection that the guard must catch, captured failing-then-passing)</run>
      <expect>Both directions captured; the suite green at its new denominator; the F9 gate FIRES on this file when staged (its enrollment proven by the gate's own audit line, not by reading the glob).</expect>
      <if_mismatch>STOP. An enrolled-by-glob claim is proven by a fire, not a read.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>the tests/ census (denominator printed: N files, watched/unwatched, collects/broken); report to COO + CTO + CVO (their fold + verify)</run>
      <expect>Census complete with zero silent drops; CTO~B items NAMED not fixed; CVO can verify the repairs against the dial record without a follow-up ask.</expect>
      <if_mismatch>REWORK per CVO's verify.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
The F9 gate + its watch derivation are YOUR OWN build -- no cross-seat file contention. The
adapter_audit half stays CTO~B's (RCG mass-deletion residue); your census cites it, hands off,
never edits. CVO's comp-depth dial is OPEN -- if your sweep touches comp-depth test files, note
them in the census but defer any repair to the dial's own findings (no mid-dial fixes).
</cross_domain_coordination>

<acceptance_criteria>
1. Pre-fix 3-red control + post-fix green + the injected-values mechanism case discriminating,
   all captured.
2. F9-gate enrollment proven by an observed FIRE on the staged file (audit-log line cited).
3. tests/ census with full denominator; RCG items named-not-fixed; zero silent drops.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="finding">DIAL_RECORD_comp-pipescript_20260804.md F10 (@37bf63f4a); CVO routing 161131Z + my disposition 162148Z (morning-wave, superseded by Andrew Proceed + your idle lane)</ref>
  <ref type="family">your adapter_audit finding 155259Z (CTO~B half); F9 gate @783d508 (your build -- the watch derivation to extend)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
