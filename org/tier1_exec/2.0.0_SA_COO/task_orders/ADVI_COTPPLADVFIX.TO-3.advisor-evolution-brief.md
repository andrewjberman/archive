# Task Order: ADVI_COTPPLADVFIX TO-3 (doc-only) -- record the cot advisor-matching evolution path

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-advi-cotppladvfix-to3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project ADVI_COTPPLADVFIX is complete; this TO was last touched 2026-07-07, predating the project close 2026-07-20. Closed as a record act, not a work verdict. Prior status: staged</status>
    <dispatch_state>STAGED, LOW-priority, NON-gating. Doc-only; not a gate on TO-1 or TO-2. Author when convenient AFTER TO-1's build lands (DS holds the role-assignment + rep-code data knowledge). CTO arch-reviews the evolution framing (PRD assigns TO-3 to 1.0.0_SA_CTO / 0.4.0_DS jointly). PRD docs/architecture/ADVI_COTPPLADVFIX_PRD.md S6 TO-3.</dispatch_state>
    <gate_note>Gates: none. Effort <1h.</gate_note>
  </metadata>

  <objective>Write a short brief pinning the real-advisor-matching evolution path so this PRD's single-synthetic-advisor bridge is knowingly temporary and its self-disable guard (TO-1 req 3) has a documented successor: single synthetic advisor (this PRD) -> 2 founder rep-code advisors (Cottonwood's ~96% AUA sits on 2 founder joint-coverage rep codes) -> full rep/team/relationship advisor matching using the Team/Rep/Relationship dims already present in the allocations BD template. No build -- captures intent + the raw material (the 2 founder rep codes; the allocations-template dims).</objective>

  <requirements>
    <requirement id="1">Brief committed under docs/briefs/ (e.g. cot-advisor-matching-evolution-brief-20260707.md).</requirement>
    <requirement id="2">Names the 3 stages, the data source for each (synthetic literal -> founder rep codes -> allocations-template Team/Rep/Relationship dims), and the self-disable condition (TO-1's guard triggers off when a real role dimension appears).</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase name="before_write">none required (doc-only) -- one sentence in the session log noting doc-only if no comp tool run.</phase>
    <phase name="before_commit">commit-gate not applicable (no .py); safe-commit under your author line.</phase>
    <phase name="after_commit">n/a.</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>None (doc-only). Informational input to any future real-advisor-matching project (the successor to this bridge).</item>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion>Brief exists under docs/briefs/, names the 3 evolution stages + each stage's data source + the self-disable condition.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="prd">docs/architecture/ADVI_COTPPLADVFIX_PRD.md S6 TO-3 (commit 11f6bd3c2)</ref>
    <ref type="project">org/projects/ADVI_COTPPLADVFIX.json</ref>
  </references>
</task_order>
```
