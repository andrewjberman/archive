# Task Order: NFRA_FEDOBS P2 -- the observation/measurement library (the MEASURE arm of the Feedback Contract)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-07-nfra-fedobs-p2</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-07-07</date>
    <status>staged</status>
    <prd_ref>docs/architecture/NFRA_FEDOBS_PRD.md (P2 + AC3/AC4/AC5)</prd_ref>
    <dispatch_state>STAGED -- authored by COO~B on the NFRA full-program completion drive (Andrew-direct, plan approved). GO at Wave-2, AFTER NFRA_CSE.P2's append-only event log lands + is CVO-certed (this TO's co-evolution signal is 0-rows until that log exists).</dispatch_state>
    <gate_note>HARD-GATED on NFRA_CSE.P2 event log. FEDOBS-P1 (federation substrate + read-only boundary) is COMPLETE + CVO-certed. This is the load-bearing MEASURE arm that MOTIF (co-occurrence) + PROMOTE (measured effect) both depend on -- without it the federated learning loop cannot close.</gate_note>
  </metadata>

  <objective>Implement the observation/measurement library (FEDOBS PRD S4.2): correlations over the federated CSE stream that each emit a MEASURED, inspectable, provenance-linked signal (not a dashboard). Prioritize the three that directly feed the Feedback Contract: directive-effectiveness, compiler-coverage, co-evolution. Trino over the Iceberg CSE log + the runtime graph; read-only on semantic truth (never writes it back -- only PROMOTE materializes).</objective>

  <requirements>
    <requirement id="1" priority="LOAD-BEARING">DIRECTIVE-EFFECTIVENESS (AC4): given a promoted directive, quantify whether it MEASURABLY reduced the churn/pattern it targeted -- the input to promotion-validate + demotion (reversibility). This is the warrant PROMOTE gates on.</requirement>
    <requirement id="2">COMPILER-COVERAGE (AC5): surface the `Concept(untyped) + confidence:low` CSE rate per artifact class -> where recognizers are missing (feeds COMPILERKIT recognizer gaps + a new-primitive PROMOTE candidate).</requirement>
    <requirement id="3">CO-EVOLUTION: which artifacts/systems consistently change together (CSEs co-occurring in producer sessions) -> the coupling/blast-radius signal MOTIF composes into C2. (0-rows until CSE-P2's event log exists -- the reason this TO is CSE-P2-gated.)</requirement>
    <requirement id="4">Each signal is MEASURED + inspectable + the decompression chain holds THROUGH the analytics (AC3): every aggregated signal traces back to the CSEs it aggregated.</requirement>
    <requirement id="5">Read-only boundary preserved (AC2, inherited from P1): FEDOBS produces signals, it cannot mutate the algebra/graph.</requirement>
  </requirements>

  <cross_domain_coordination>
    - NFRA_CSE.P2 (0.5.0_AE store-writer + 0.4.0_DS~B): the append-only CSE event log this TO queries. HARD PREREQUISITE.
    - NFRA_MOTIF (0.4.0_DS~A): consumes this TO's co-occurrence signal (P1 c2-detect + P3 candidates).
    - NFRA_PROMOTE (Wave-4): consumes this TO's directive-effectiveness measurement (the measure-before-promote warrant) + post-promotion monitoring (PROMOTE-P3).
    - NFRA_COMPILERKIT: consumes the compiler-coverage signal (recognizer gaps).
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All three measured signals (directive-effectiveness, compiler-coverage, co-evolution) emit REAL rows over the live CSE log + runtime graph (not stubs); ground on live Trino query results, never self-report (Rule 22).
    2. Each signal is provenance-linked: pick any signal row, trace it to the source CSEs it aggregated (AC3 decompression through analytics).
    3. Directive-effectiveness demonstrated on a REAL promoted directive (measurable reduction of its target pattern).
    4. Read-only boundary exercised (AC2): a write-attempt on semantic truth fails closed.
    5. RAVC COO~B + CC CTO; hand CVO for independent measure-honesty verification (TH-V-style: does the signal move when the underlying reality moves, and only then).
  </acceptance_criteria>
</task_order>
```
