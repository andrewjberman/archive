# Task Order: NFRA_TOOLCHECK P2 -- FIXES FIRST, THEN OPTIMIZATIONS (Andrew's explicit order)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-toolcheck-p2-fixes</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~D + 0.4.0_DS_ClientPlatform~B (comp-tool/graph builders) | CTO arch-gate + CVO fixes-re-verified cert</issued_to>
    <date>2026-07-08</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_TOOLCHECK, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged -- GO after P1 (the verification matrix + confirmed break list). FIXES BEFORE OPTIMIZATIONS (Andrew's explicit order).</status>
    <prd_ref>docs/architecture/NFRA_TOOLCHECK_PRD.md (SS4 P2, SS5 fixes-before-optimizations, SS8 Q2/Q4)</prd_ref>
    <dispatch_state>STAGED. Gated on P1's real-use-grounded break list. The fixes are pre-populated + severity-ordered from Part 0.</dispatch_state>
    <gate_note>FIXES BEFORE OPTIMIZATIONS (Andrew's order). Do NOT retire a tool on starved telemetry -- the retire pass runs ONLY after the telemetry substrate is fixed (P1 req#1) + usage re-confirmed.</gate_note>
  </metadata>

  <objective>Implement the FIXES first (make every tool functional), THEN the optimizations. Each fix re-verified on a REAL invocation + the logs (not --help); no fix regresses another tool.</objective>

  <requirements>
    <requirement id="1" priority="FIXES -- severity-ordered">FIX (in order): (a) comp-drift -- the 50% real break (top); (b) comp-learns-run -- absent comp.framework.run module (install/packaging); (c) telemetry substrate -- jq guarded-fallback + hook-install-drift (also the P1 prereq -- if P1 didn't fully close it, close here); (d) comp-constants (52% fail) + comp-tooltip (46% fail + mojibake -> ASCII, CLAUDE.md no-non-ASCII); (e) comp-to (no --help handler / sloppy arg-parse); (f) THE SYNTHETIC-MARKER gate/lint -- so synthetic tests are distinguishable from real fails (unblocks automated works/broken verification).</requirement>
    <requirement id="2" priority="OPTIMIZATIONS -- only after the fixes land">OPTIMIZE: (a) comp-pipescript discoverability (canonical-token alias / --list-resources / fuzzy token-match); (b) comp-kuzu schema-surface (make the CloudNode/CloudEdge-with-properties schema discoverable at the prompt -> stop the Cypher-guessing); (c) the coverage-gap tools -- ROUTE-vs-BUILD (comp-symbols/comp-types may already cover -> the gap may be routing, resolve in P3 BEFORE authorizing any new tool, Q4); (d) RETIRE truly-unused (comp-dups/secrets/dispatch) -- ONLY after telemetry fixed + usage re-confirmed (Q2 threshold, CTO-ratified).</requirement>
    <requirement id="3">Each fix RE-VERIFIED on a REAL invocation + the usage log (the P1 method -- not --help). No fix regresses another tool (re-run the affected tools' real invocations).</requirement>
  </requirements>

  <acceptance_criteria>
    1. The break list at 0 -- each fix re-verified on real use; the optimizations landed; no regression.
    2. RETIRE decisions made ONLY on un-starved telemetry (post-P1-req#1) at the Q2-ratified threshold. CTO arch-gate + CVO fixes-re-verified cert. RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
