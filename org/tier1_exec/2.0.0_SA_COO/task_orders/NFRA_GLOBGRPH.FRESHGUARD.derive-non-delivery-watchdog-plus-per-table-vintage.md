# Task Order: NFRA_GLOBGRPH FRESHGUARD -- derive-non-delivery watchdog + per-table-vintage oracle (the silent-edge-freeze systemic fix)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-globgrph-freshguard</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps (build both) + 1.0.0_SA_CTO (arch-gate both) + 3.0.0_SA_CVO (I3 red-fixture verify)</issued_to>
    <date>2026-07-08</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_GLOBGRPH is complete; this TO was last touched 2026-07-08, predating the project close 2026-07-09. Closed as a record act, not a work verdict. Prior status: dispatched</status>
    <prd_ref>docs/architecture/NFRA_GLOBGRPH_PRD.md (freshness contract / marker-HEAD-oracle) + NFRA_SEMCTL_HONESTY_INVARIANTS.md (I1 false-freshness, I3 fires-when-exercised)</prd_ref>
    <dispatch_state>DISPATCHED 2026-07-08 by COO~B. Andrew-directed finding (0.7.0_AE surfaced live-grounded). CTO arch-RULED both fixes (025559Z). Non-P0 for loop-close (0.7.0's controlled derive run unblocks MOTIF-P0/INFRPT now); a fast systemic follow-on.</dispatch_state>
    <gate_note>THE FINDING: the nightly Fargate derive_runner (SOLE writer of graph_edges) did NOT deliver tonight; the marker-HEAD-oracle read FRESH because node/cse writers re-stamp the marker with graph_edges' EXISTING snapshot -> SILENT 23h edge-freeze (canonical GOV-A I1 false-freshness). Root of the MOTIF-P0 clusters-not-live + INFRPT-P3 L3-never-refreshed. Two SYSTEMIC guards (defense-in-depth), needed regardless of the RC 0.7.0 is isolating (schedule-fault vs broken-derive = the SPECIFIC repair, separate).</gate_note>
  </metadata>

  <objective>Convert the silent-edge-freeze CLASS from silent-freeze to loud-catch + oracle-visible, per CTO's arch ruling. Deliverables (defense in depth): (1) a derive-non-delivery WATCHDOG [leg-3, DONE + red/green-verified]; (2) a PER-TABLE VINTAGE dimension on the marker-HEAD-oracle [leg-4, GO'd]; (3) LEG-5 (CTO arch-ruled 2026-07-08, generalization) = a per-PRODUCER freshness-alarm CLASS -- a producer REGISTRY (each substrate producer feeding a critical/served surface -> its cadence -> a standard fail-closed alarm extending leg-3's pattern), POPULATED FROM the NFRA_SYSTEM producer audit, so a stale producer (fail-closed/absent-trigger/stuck) ALARMS LOUD by construction + coverage is tracked-by-construction (closes the flagged-not-tracked fell-through class). code_heat = the FIRST registry instance (its alarm is the leg-5 template). Owner 0.7.0_AE_CloudOps~B; CTO arch-gates the registry schema + standard-alarm module. Ties to leg-4 (vintage=how-stale / leg-5-alarm=loudly-when). The recurring-TRIGGER (host-scheduler vs hook vs manual) is a SEPARATE Andrew decision -- leg-5 alarms regardless of trigger.

  <requirements>
    <requirement id="1" owner="0.7.0_AE">DERIVE-NON-DELIVERY WATCHDOG: a daily derive that does NOT deliver a FRESH graph_edges snapshot (new snapshots/YYYYMMDD/ + latest.txt advance) by a deadline (~04:00Z, 2h past the 02:00Z cron) -> SNS ALARM LOUD, payload {expected_date, latest_actual, staleness_hours, sole_writer=derive_runner}. REUSE an existing SNS topic (INFRPT absence-guard / cot L4-detection pattern -- NO new-topic sprawl).</requirement>
    <requirement id="2" owner="0.7.0_AE + 3.0.0_SA_CVO">I3 RED-FIXTURE (do NOT ship un-exercised): the watchdog must be PROVEN to FIRE on a real non-delivery -- a deliberately-skipped/late derive -> the alarm fires (+ a green-fixture: a fresh derive -> no alarm). "The watchdog exists" != "the watchdog fires" (the comp-honesty bar). CVO exercise-verifies the red-test.</requirement>
    <requirement id="3" owner="0.7.0_AE (graph-platform/globgrph lane)">PER-TABLE VINTAGE: PRESERVE the one-marker-HEAD (version-consistency contract, CSE rides it -- do NOT break it) AND ADD a per-table vintage dimension to the oracle's provenance header -- each table's ACTUAL last-write (graph_edges last-derived / nodes last-incremental / cse last-append). A table past its writer's expected cadence flags per-table-STALE in the header ("graph_edges: 23h stale -- sole-writer derive stalled"). So a stalled sole-writer can NEVER be masked by node/cse HEAD-advances. Analogous to comp-kuzu/comp-fedobs vintage discipline, extended per-table-aware.</requirement>
    <requirement id="4">Both designs routed to 1.0.0_SA_CTO for arch-gate BEFORE build/land (CTO owns the freshness contract per NFRA_GLOBGRPH / Rule 20).</requirement>
  </requirements>

  <cross_domain_coordination>
    - The SPECIFIC repair (why the nightly didn't run: EventBridge schedule-target fault vs broken-derive) = 0.7.0's controlled-run RC isolation, SEPARATE from these systemic guards -- but the watchdog covers it going forward regardless.
    - Shared-surface rules: any globgrph TF apply is TARGETED (-target); derive-image changes route through 0.7.0's rebuild-from-HEAD serialization.
    - NFRA_CSE rides the one-marker-HEAD (version-consistency) -- the per-table-vintage ADD must not alter the shared marker semantics.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Watchdog: LIVE + CTO-arch-gated + the I3 red-fixture PROVEN to fire (CVO exercise-verified), green-fixture clean. Reuses an existing SNS topic.
    2. Per-table vintage: the oracle provenance header carries each table's actual last-write + a cadence-vs-vintage staleness flag; a stalled sole-writer table reads per-table-STALE (not masked by the shared marker); CTO-arch-gated; the one-marker-HEAD version-consistency UNBROKEN (CSE still rides it).
    3. Ground on live state (Rule 22a: the alarm actually fires on a real skip; the header actually flags a real stale table). RAVC COO~B + CTO; CVO verifies the red-test + the staleness-flag honesty.
  </acceptance_criteria>
</task_order>
```
