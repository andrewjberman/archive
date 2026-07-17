<task_order>
<to_id>OPAL_STNDRD.Z1</to_id>
<title>Execute the ratified standardization program (brief @ 20b52be25, all six axes CTO-ratified) — phases 2-7 + the sec-4 gap queue</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<status>complete</status>
<!-- RETIRED complete-as-superseded 2026-07-17 ~20:1xZ by 2.0.0_SA_COO (records-reconciliation, CC CTO).
     OPAL_STNDRD is superseded-into OPAL_TAXONOMY (@567b4c374, Andrew-direct ~18:5xZ; CTO fold ruling
     200246Z). This TO's DONE phases (ph2 trigger-map+CI gate, ph5 EC2 manifest-lint, ph6/7 TERRAFORM_PROTOCOL
     + INDEX) are the 4 LIVE hooks TAXONOMY's DC-lints now ride; its OPEN scope (ph3 absence-twin, ph4 renames)
     folded into OPAL_TAXONOMY as DC-D (DEFER per alert-suspension) + the DC-disposition batch (0.8.0~B → CTO
     ruling-20). Assignee 0.7.0~Z is dead; 0.7.0-base stood down from picking it up (200722Z). No further
     execution under this TO — TAXONOMY is the live program. -->

<project>OPAL_STNDRD (synergistic with OPAL_CONSOLIDATION per Andrew verbatim)</project>
<provenance>Andrew-direct mandate 2026-07-15 ~18:4xZ (verbatim in the brief's sec-0) + spawn word
~19:1xZ ("I have spawned 0.7.0_AE_CloudOps~Z which will be responsible for the project OPAL_STNDRD
which is detailed in a brief from 0.6.2"). Lane Andrew-spawned.</provenance>

<the_spec>org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/BRIEF_CONSOLIDATION_RESOURCE_STANDARDIZATION_20260715.md
@ 20b52be25 — READ IT WHOLE FIRST. It carries the mandate verbatim, the measured current state
(incl. the load-bearing finding: the estate runs TWO scheduling services — any census instrument
you build MUST sweep both), the six proposed axes, and the phase plan. CTO RATIFICATION (all six,
recorded in OPAL_STNDRD.json): A as-written · B with the open call MADE (EventBridge SCHEDULER for
all NEW cron-class; Rules for event-PATTERN only; grammar {unit}-{function}-{cadence}; absence-twin
REQUIRED per daily producer; trigger-map.json lives at infra/aws/lambda/ci/ beside the source-map,
CI drift gate same class) · C as-written (renames NATURAL TOUCHES ONLY; memory_mb = TF-desired;
chunking law canonical on the n=2 AC-1 number, landing tomorrow AM) · D as-written (telemetry AT
PROVISION; autoshutdown DEFAULT, exceptions manifest-declared) · E as-written (mechanism to
docs/deployment/TERRAFORM_PROTOCOL.md VERBATIM, law stays CLAUDE.md) · F with the home fixed =
infra/aws/lambda/ci/ (ONE machine-readable registry home; never a second).</the_spec>

<execution_order>Brief sec-5 phases 2-7, with the sec-4 gap list as the opening queue:
(2) the two-service trigger-map census script + the first committed trigger-map.json + its CI
drift gate — 0.6.2 volunteered their half-written census script: take the HANDOFF (bounded
contribution, you own from there; coordinate directly, their queue is full); (3) absence-twin
rollout on the 4-unit list (ingest-mirror x2, bd49f, schwab-si2, etfs-netassets); (4) natural-touch
renames only — NO big-bang rename wave, ever; (5) EC2 telemetry/right-sizing standard doc + si2 as
pilot; (6) TERRAFORM_PROTOCOL.md consolidation (verbatim moves, a CLAUDE.md pointer edit routes
through CTO — ANY_CTO surface); (7) docs/architecture/INDEX.md keyed by resource type. Sec-4 gaps
1-2 (pathfinder feeder owner-claim; the DISABLED smartx-model-monthly-pull-daily Scheduler entry —
verify intended + the name smell) fold into phase 2's census work.</execution_order>

<gates>EVERY TF diff/apply at CTO's safe-apply gate (plan-shape RAVC first). Every new gate/lint
ships announce-then-enforce (WARN first) per NFRA_COMPRAIL precedent. New standards bind NEW builds
immediately + existing resources on natural touches — retroactive sweeps are findings lists, never
auto-edits. Tonight's binding window: touch NOTHING on the parity path before the 22:00Z fire
clears (your base lane holds those motions; stay off their surfaces).</gates>
<compiler_tools_mandate>comp-aws/comp-iam for topology; raw aws INSPECTION rail-marked; census
scripts print denominators (both scheduling services, every sweep). Commit-gate per law.</compiler_tools_mandate>
<cross_domain_coordination>0.6.2 (census-script handoff + their schwab/chunking-adjacent pieces);
base 0.7.0 (their box/manifest work must land conformant — coordinate the BUILD_MANIFEST semantics
fix with their AC-1 motion); 0.8.0~Z (GRAPHFEED registries — one registry-home convention, do not
fork); CTO (all applies + the CLAUDE.md pointer).</cross_domain_coordination>
<acceptance_criteria>Per phase: the artifact (map/gate/doc) committed + its drift instrument LIVE
+ exercised (a seeded drift FAILS loud — an instrument that cannot fail is not an instrument);
denominators printed on every census; the sec-4 gap list each closed-or-owned with evidence.</acceptance_criteria>
<session_log>Required, Compiler Tools section mandatory.</session_log>
</task_order>
