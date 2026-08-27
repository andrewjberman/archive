# Task Order: NFRA_TOOLCHECK P1 -- FUNCTIONAL VERIFICATION (real-invocation + log-ground-truth; telemetry-substrate fix FIRST)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-toolcheck-p1-verify</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~D (comp-tool verification + the telemetry-substrate hook fix) + 0.4.0_DS_ClientPlatform~B (org/modules/graph tools) | CTO arch-gate + CVO real-use-grounding cert</issued_to>
    <date>2026-07-08</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_TOOLCHECK, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: dispatched -- Andrew-direct (via CTO 181353Z) decomp. Matters (the shared cognition every agent reasons from) but NOT a fire -- sequenced into the NFRA cadence, non-urgent. Part-0 pre-flight DONE (CTO, baked into PRD SS2 as the grounded starting inventory).</status>
    <prd_ref>docs/architecture/NFRA_TOOLCHECK_PRD.md (SS2 pre-flight findings, SS4 P1, SS5 principles, SS8 Q1)</prd_ref>
    <dispatch_state>DISPATCHED 2026-07-08 by COO~B on Andrew's decomp directive. CTO holds 3 detailed pre-flight agent reports (per-tool evidence) -- ping CTO if the executors want them.</dispatch_state>
    <gate_note>THE METHOD LESSON (Part 0, load-bearing): --help is a FALSE-GREEN (52/53 pass --help, but comp-drift FAILS 50% of REAL invocations). VERIFY ON REAL REPRESENTATIVE INVOCATIONS cross-checked against the usage-log (14,295 rows) ground truth -- NEVER --help.</gate_note>
  </metadata>

  <objective>Verify each of the ~55 comp-tools is FUNCTIONAL on REAL invocations (not --help) cross-checked vs the usage-log ground truth. Classify each: WORKS / BROKEN / DISCOVERABILITY-FRICTION / RETIRE-CANDIDATE. Surface the break list (for P2) + the coverage-gap list + the optimization/retire list.</objective>

  <requirements>
    <requirement id="1" owner="0.8.0~D or AE-lane" priority="PREREQUISITE -- DO FIRST">FIX THE TELEMETRY SUBSTRATE before classifying anything: TELEMETRY_HOOK_NO_JQ x252 across 82 sessions (jq not a Git-Bash default, the PostToolUse hook has NO guarded fallback -- CLAUDE.md r16) -> those runs never land in agent_telemetry -> STARVES comp-tool-health's USED axis. Add the guarded-jq-fallback (canonical pattern org/mcp/inbox-watch.sh) + address the hook-install-drift (x6) per Q1 scope. A starved USED-axis makes EVERY "unused->retire" verdict untrustworthy -- so this gates all retire/health classification.</requirement>
    <requirement id="2">PER-TOOL VERIFICATION MATRIX: exercise each tool on a REAL representative invocation + cross-check vs the usage log. Classify WORKS / BROKEN / DISCOVERABILITY-FRICTION / RETIRE-CANDIDATE. Distinguish a real BREAK from a GATE-FIRING-CORRECTLY (comp-validate/comp-manifest-check exit nonzero on a real violation = working) from DISCOVERABILITY-FRICTION (high fail-count from surface, not a break -- comp-pipescript token-resolution, comp-kuzu Cypher-dialect).</requirement>
    <requirement id="3">THE BREAK LIST (pre-populated from Part 0, confirm+extend on real use): comp-drift (50% real break, top) / comp-learns-run (No module comp.framework.run) / comp-constants (52%) / comp-tooltip (46% + mojibake). Feed to P2.</requirement>
    <requirement id="4">THE COVERAGE-GAP LIST (66 no-rich-tool rail escapes): symbol/file-outline (comp-symbols may exist-but-not-route) / source-of-record "where is X" (largest cluster) / type-def (comp-types may exist-but-not-route) / live-AWS-verify (maybe off-graph by design) / live-progress+staged-diff. Flag ROUTE-vs-BUILD per gap (resolved in P3 routing before any new tool -- Q4).</requirement>
    <requirement id="5">THE SYNTHETIC-MARKER problem: the (SYNTHETIC TEST FIXTURE) marker is effectively UNUSED (1/1302 FAILs marked) -> synthetic tests are indistinguishable from real fails in the log. Note it (the fix is a P2 gate/lint) -- it currently blocks a clean automated works/broken filter.</requirement>
  </requirements>

  <acceptance_criteria>
    1. TELEMETRY SUBSTRATE FIXED (jq guarded-fallback lands; USED-axis un-starved) -- verified (a real invocation now lands in agent_telemetry).
    2. Every tool exercised on a REAL invocation + cross-checked vs the logs (NOT --help). The break list complete + grounded-on-real-use; coverage-gap + optimization/retire lists delivered.
    3. CTO arch-gate (verification-completeness) + CVO cert (real-use-grounded, not --help-green). RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
