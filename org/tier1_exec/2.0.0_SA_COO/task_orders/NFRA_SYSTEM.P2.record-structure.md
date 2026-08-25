# Task Order: NFRA_SYSTEM P2 -- RECORD & STRUCTURE (the /system tree + static per-layer docs + the center-of-gravity README)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-system-p2-record</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps or 0.8.0_AE_CloudComp~D (AE-LANE -- infra/ is CLOUD_OPS_OR_ETL owned-paths; CTO is gate-blocked from writing there, correctly) + 1.0.0_SA_CTO (arch-gate the structure; CTO drafted the README in PRD SS5/SS6)</issued_to>
    <date>2026-07-08</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_SYSTEM is complete; this TO was last touched 2026-07-08, predating the project close 2026-07-09. Closed as a record act, not a work verdict. Prior status: staged -- GO after P1 audit lands (CTO-arch-gated). DOUBLE-GATED: (a) on P1 (the structure is refined once P1's interaction map is grounded); (b) on NFRA_LOCALROOT-P2 (base COO) -- the /infra PARENT structure that /infra/system SLOTS INTO. CTO HOLDS the P2 arch-gate until LOCALROOT-P2 settles (so /infra/system lands in its FINAL home per the LOCALROOT taxonomy, not a spot that moves). Coordinate base COO on placement + naming/index constraints (172332Z trilogy: LOCALROOT=structure / TERRAFORM=cloud-resources / SYSTEM=content).</status>
    <prd_ref>docs/architecture/NFRA_SYSTEM_PRD.md (SS4 Part-2, SS5 tree, SS6 principles)</prd_ref>
    <dispatch_state>STAGED. AE-lane executes (infra/ owned-paths); CTO arch-gates + supplied the README content (PRD SS5 tree + SS6 principles).</dispatch_state>
    <gate_note>infra/system/ is a NEW tree under infra/ (CLOUD_OPS_OR_ETL lane). CONSOLIDATE-don't-duplicate: reference the ~313 docs as deep source; /system is the synthesis + entry point, not a re-copy.</gate_note>
  </metadata>

  <objective>Create the infra/system/ tree (PRD SS5) + populate it with P1 findings -- the STATIC architecture (the stable how-it-works, per layer + the synthesis) + the center-of-gravity README (entry point + routing index).</objective>

  <requirements>
    <requirement id="1">Create the infra/system/ tree (PRD SS5): README.md + 00_synthesis/ + 01_substrate/ + 02_graph/ + 03_comp_tools/ + 04_federated/ + 05_learning/ + 06_current_state/ + 07_maturity/ (refined per P1's grounded interaction map).</requirement>
    <requirement id="2">Per-layer STATIC architecture docs (01-05 + 00_synthesis) -- the stable how-it-works, grounded on P1 findings, CONSOLIDATING (indexing the deep-source docs) not re-copying.</requirement>
    <requirement id="3">The top-level README.md = the center of gravity: entry point + routing index (which layer answers what) -- routes an agent to the right layer in ONE read. CTO drafted content in PRD SS5/SS6; the AE executor authors the real one.</requirement>
  </requirements>

  <acceptance_criteria>
    1. The /system tree exists; each layer has its static doc; the README routes to the right layer in one read.
    2. Every doc grounded on P1 findings; consolidates (indexes) the existing corpus, does NOT fork truth by re-copying. CTO arch-gate (structure).
  </acceptance_criteria>
</task_order>
```
