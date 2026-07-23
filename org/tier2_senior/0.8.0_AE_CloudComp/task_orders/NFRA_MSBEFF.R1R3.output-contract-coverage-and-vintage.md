<task_order>
<to_id>NFRA_MSBEFF.R1R3</to_id>
<title>THE OUTPUT CONTRACT — one shared helper giving every comp-tool answer a COVERAGE denominator (+ what it structurally cannot see) and a PLANE/VINTAGE header; folds in the M3 verdict-set derivation and comp-validate's frozen BD/INF/COT tree registry</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp</issued_to>
<date>2026-07-23</date>
<status>pending</status>
<priority>P1 — the highest-leverage cell in the MSBEFF audit; gate-approved, conditions attached</priority>

<authority>
Andrew-direct at the ~Z terminal 2026-07-23, VERBATIM: "lET'S GET 0.8.0 WORKING ON ALL OF THESE, YOU
CAN WRITE THE TOs AND JUST DELIVER THEM DIRECT" (TO authoring + direct dispatch authorized to ~Z for
this batch; the COO decomposition step is bypassed by his word).
GATE: main CTO ruling relayed via MSTR 165823Z — R1+R3 APPROVED as ONE combined output-contract
change. His reasoning, carried: both are existing estate doctrine generalized (print-the-denominator,
comp-kuzu's provenance header, Rule 20's read-the-header law) — this is CODIFYING PRACTICE, not new
law. Charter: NFRA_MSBEFF (Andrew 2026-07-23), PRD docs/architecture/NFRA_MSBEFF_PRD.md.
</authority>

<evidence_base>
718 verified NL findings (0 fabricated quotes) + telemetry. FAILED_COVERAGE is the top failure class
at 253/718 (35%); true mechanical crash rate is only ~0.87%. Agent-verbatim exhibits:
"comp-pipescript deployed is bd-tree/.py-scoped -- inf gold .sh dispatch scripts are UNCOVERED" ·
"the graph indexes only 23 COMPONENT nodes, missing the whole market-performance dir" ·
"comp-iam parses TF = DESIRED only and is structurally blind to AWS-managed and unmanaged grants --
which is the finding under test" · "missed the dynamic-prefix holdings read".
Full corpus: org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_MSBEFF/nl_structured/findings_merged.jsonl
</evidence_base>

<scope>
BUILD ONE SHARED HELPER, consumed by N tools — never per-tool copies (gate condition c).

A. COVERAGE LINE (R1): every tool answer states its denominator AND what it structurally cannot see.
   Shape (yours to finalize; the semantics are the contract): what was scanned (N of what population,
   from which source), and the named blind spots for that invocation class (e.g. "AST-parsed .py only
   — dynamically-keyed I/O and .sh dispatch not visible"). The generalization target is the
   already-proven convention in .tools/mdpf-preflip-check + your item-7 --complete-over denominators.

B. PLANE / VINTAGE HEADER (R3): every tool states the plane it read — DESIRED (parsed TF/config) vs
   APPLIED (live primitive), graph vintage, source-vs-projection. comp-kuzu's provenance header is the
   estate's own proven pattern and the reference implementation to generalize.

C. FOLD-IN 1 — M3 verdict-set derivation (already queued in your tail behind the landed interim
   @b62b3a894): VERDICT_EXIT_TOOLS derives from the comp-tools.yaml exit contracts. It shares this
   TO's registration invariant, so land it inside this batch.

D. FOLD-IN 2 — main CTO's addition (his 164237Z ruling, relayed 165823Z): comp-validate's hardcoded
   BD/INF/COT tree registry (validate_cli.py:47-55, DS-flagged 07-23) is the SAME frozen-enumeration
   class — derive it from the registry rather than patching separately.

OUT OF SCOPE: retrofitting every tool's internals to WIDEN coverage. This TO makes coverage and
vintage HONEST AND VISIBLE; widening specific tools is R2/R5 and later cells.
</scope>

<gate_conditions>
Verbatim from main CTO's ruling (the M3 pattern) — all three load-bearing, none optional:
(a) REGISTRATION-INVARIANT: a tool cannot register/re-register without declaring its coverage + plane
    semantics for the helper — else the contract silently under-covers new tools. Wire into
    comp-manifest-check's completeness gate, as the M3 exit-contract declaration does.
(b) UNKNOWN-IS-NOT-A-VERDICT: a tool that cannot state its coverage/vintage renders that line as
    UNKNOWN, LOUDLY — never omits it. (The no-channel-for-I-don't-know law at the output layer.)
(c) ONE IMPLEMENTATION consumed by N tools, never per-tool copies.
</gate_conditions>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-manifest-check (registration surface) + comp-blast on the helper's call sites; enumerate the tool population that will consume the contract</run>
      <expect>The consuming-tool denominator is enumerated AT RUN TIME from the registry, never a hand-listed set (this TO's own subject applied to itself).</expect>
      <if_mismatch>STOP and surface to ~Z: a hand-listed consumer set would make this fix the very class it closes.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>The required MUTANTS: (1) a tool with deliberately undeclared coverage/plane must render UNKNOWN, not a silent omission and not a false clean; (2) a tool whose coverage is 0% of the queried target must say so LOUD, never return a clean empty.</run>
      <expect>Both mutants on the record in the commit. A passing assertion never mutated has never been tested.</expect>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Exercise on the audit's own named exhibits: comp-pipescript against an .sh dispatch script; comp-iam against an AWS-managed grant; comp-blast against a component outside the indexed set.</run>
      <expect>Each now emits a coverage line naming the blind spot instead of a confident empty. Paste the three outputs in the report.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Shared surface with the M3 interim you already landed (@b62b3a894) and with comp-manifest-check's
registration invariant (also touched by item-7's exit-contract declaration). No main-fabric coupling —
MDPF/consolidation untouched. If any change would alter a tool's ANSWER (not its output framing),
STOP and route to ~Z: this contract is additive framing by design.
</cross_domain_coordination>

<acceptance_criteria>
1. ONE helper module; consumer count derived from the registry at run time, denominator printed.
2. Both gate mutants exercised and on the record (undeclared -> loud UNKNOWN; zero-coverage -> loud).
3. Registration invariant live in comp-manifest-check: a tool registering without coverage/plane
   semantics FAILS the gate (mutant-proven).
4. M3 derivation landed (verdict set derived from comp-tools.yaml contracts, frozen list retired) +
   the supersession-history note preserved so no future reader re-freezes it.
5. comp-validate's BD/INF/COT tree registry derived, not hardcoded (validate_cli.py:47-55).
6. Telemetry RE-BASELINE per the M3 ruling: historical rows re-verdicted under derived contracts so
   MSBEFF's own numbers stand on the corrected appender.
7. Session log with a Compiler Tools section + the org/compiler-tools-log.md line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z (one verify for the PSTMRT/MSBEFF family). Report to 1.0.0_SA_CTO~Z; CC main CTO on the standard-change landing (his gate).</verification>
</task_order>
