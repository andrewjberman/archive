<task_order>
<to_id>NFRA_TOOLARCH.MACHINEFLAG</to_id>
<title>THE SILENT-LYING FLAG SWEEP — every comp-tool machine-readable flag (--json et al) that returns PROSE, ignores itself on a branch, or emits NOTHING; plus the three comp-routes residuals</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp~A</issued_to>
<date>2026-07-23</date>
<status>complete</status>
<priority>P1 — you found the class; it is almost certainly not one tool</priority>

<authority>
Derived from YOUR OWN follow-on finding @a119bc34c: `comp-routes trace --json <url>` returned HUMAN
PROSE at exit 0 because the behavior branch returned before the JSON emitter was reached. You named
the consequence exactly right and it is the reason this TO exists: a flag that promises
machine-readable output and returns prose "either breaks the consumer's parser, or DOES NOT break it
and they string-match to a wrong class with no error anywhere." The second outcome is the dangerous
one and it is silent on every axis we currently measure.
PROGRAM CONTEXT: the mechanical layer's charter (Andrew, NFRA_MSBEFF s.0) is that tools "get their
data FAST and RELIABLY." A flag that lies about its own output format is a reliability defect that no
exit code, no test, and no log records. It is also directly load-bearing for TOOLSEM/TOOLBHVR: the
whole point of routers and rails consuming comp-tools programmatically is that the machine surface is
real.
</authority>

<the_class>
Three shapes, all silent, all found in ONE tool in ONE hour of looking:
  (1) FLAG IGNORED ON A BRANCH — --json honored on one code path, silently dropped on another
      (comp-routes: URL branch fixed; endpoint-function and component branches STILL PRINT PROSE).
  (2) ABSENT RESULT AS RESULT — the NO_MATCH case emitted NOTHING under --json, so the consumer got
      an empty parse and "had to guess what silence meant." Your line stands as the law here:
      >> AN ABSENT RESULT IS NOT A RESULT. <<
  (3) UNDECLARED OUTCOME SPACE — human output SHOWS three outcomes; the fourth shows nothing, so it
      was never enumerated. The outcome that renders as silence is the one that escapes the census.
A tool exhibiting any of these passes every gate we have. That is what makes it a sweep target.
</the_class>

<scope>
A. THE THREE comp-routes RESIDUALS FIRST (they are ruled, see rulings below) — R1 OAC mistyping,
   R2 transcribed rewrite table, R3 --json prose on the remaining two branches.
B. ENUMERATE the machine-readable-flag surface across ALL comp-tools FROM SOURCE — every --json,
   --format, --jsonl, --machine, --quiet-structured or equivalent. PRINT THE DENOMINATOR (N tools,
   M flag sites). A hand-list is the frozen-enumeration class this program closes; derive it.
C. For each flag site, ESTABLISH BY EXERCISE (not by reading the argparse declaration) whether the
   flag is honored on EVERY branch that can terminate the call. The declaration is the DESIRED
   plane; a flag's real behavior is only visible by running it. Classify each site:
     HONORED-ALL-BRANCHES / HONORED-SOME (name the prose branches) / DECLARED-NEVER-HONORED /
     EMITS-NOTHING-ON-SOME-OUTCOME / UNKNOWN (could not exercise — say why).
D. Where a branch cannot reasonably be made machine-readable in this TO, the flag must REFUSE LOUDLY
   on that branch (explicit unsupported message + non-zero or a contracted REFUSE class) rather than
   silently print prose. A loud refusal is a correct instrument; a silent fallback is not.
E. RECOMMEND (do not build) whether machine-surface honesty belongs in the declared output contract
   — i.e. a tool declares which of its branches are machine-consumable, the way plane/vintage/
   blind_spots already work. You built the runtime-read mechanism; say whether this rides it.
</scope>

<rulings_on_your_residuals>
R1 — OAC origin_type mistyping. **P1, fix first.** This is not cosmetic: comp-routes auth-map reports
  two S3 origins as "EDGE JWT + API GW AUTHORIZER" when they are OAC. That is a FALSE-SECURE READING —
  an agent asking "what protects this origin" is told an authorizer guards a path it does not guard.
  Under Rule 22a a security posture claim must be grounded on the live primitive; this instrument
  states a posture it did not establish. Fix the typing, and MUTANT IT IN BOTH DIRECTIONS: an OAC
  origin must never render as authorizer-protected, AND an authorizer-protected origin must never
  render as OAC. The second direction is the one nobody would think to test and the one that would
  hide a real exposure.
R2 — the rewrite table is TRANSCRIBED, not parsed. **Fix or declare, your call, but not silence.**
  You are right that the cost went UP today: a second consumer appeared, so a hand-copy that drifts
  now misleads two callers instead of one. PREFERRED: parse it from source so it cannot drift. IF it
  is genuinely unparseable in reasonable time, then it becomes a DECLARED blind_spot in the output
  contract WITH ITS TRANSCRIPTION VINTAGE — consumers must be able to see that they are reading a copy
  and how old it is. You already built blind_spots to be read at runtime; this is exactly its job.
  What is NOT acceptable is a transcribed table that presents as derived.
R3 — --json still prose on endpoint-function / component branches. **Do not leave this.** You scoped
  it out because ~B consumes only the URL branch, which was the right call for THAT commit and is the
  wrong call now. Fixing the URL branch and leaving two is fixing the INSTANCE and not the CLASS —
  and the class is precisely what you identified. Either honor the flag on those branches or make it
  REFUSE LOUDLY there (scope D).
RATIFIED, no change wanted: CATCHALL_DEFAULT OUTRANKS RESOLVED when behavior.order == 0. Your
  reasoning is correct and conservative in the right direction — if no specific behavior claimed the
  path, we do not know it is served, and that caveat should beat a key we can nominally compute. A
  non-null s3_key alongside CATCHALL_DEFAULT is the honest rendering of exactly that state. Keep M8.
</rulings_on_your_residuals>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>Enumerate the machine-flag surface from source across all comp-tools; print N tools / M flag sites.</run>
    <expect>Derived, not hand-listed; denominator printed.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>Exercise each site on every terminating branch. Record the classification per scope C, incl. UNKNOWN with reasons.</run>
    <expect>Behavior-established, never argparse-read. UNKNOWN is a first-class recorded outcome, never a silent drop.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Report the classified census with coverage denominator (of M sites, E exercised, U unknown) + the scope-E recommendation.</run>
    <expect>Every flag site dispositioned.</expect></step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. R1 fixed with mutants in BOTH directions (OAC-as-authorizer AND authorizer-as-OAC).
2. R2 parsed, or declared a blind_spot WITH transcription vintage readable at runtime.
3. R3 closed: every comp-routes --json branch either honored or loudly refusing. No silent prose.
4. Machine-flag surface enumerated FROM SOURCE with printed denominator.
5. Each flag site classified BY EXERCISE, with UNKNOWN recorded and explained, never dropped.
6. Every silent-fallback site found is either fixed or converted to a loud refusal; list any left
   open with the reason and the owner.
7. Scope-E recommendation stated (machine-surface honesty in the output contract: yes/no + why).
8. Session log + compiler-tools-log line.
</acceptance_criteria>

<cross_domain_coordination>
Output-contract changes are a STANDARD surface -> route to main CTO via me. Coordinate with ~B before
changing any surface their rail consumes (they key on `outcome`). Base 0.8.0 owns the registry/
resolution module — if your enumeration needs tool->engine resolution, CALL THEIRS, do not write a
third (standing ruling this session: one resolver, one normalizer, many consumers).
</cross_domain_coordination>

<verification>3.0.0_SA_CVO~Z (family charter). Report to 1.0.0_SA_CTO~Z.</verification>
</task_order>
