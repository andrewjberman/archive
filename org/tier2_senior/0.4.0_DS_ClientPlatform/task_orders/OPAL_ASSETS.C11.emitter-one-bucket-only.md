# OPAL_ASSETS.C11 — Emitter reads ONLY `opal-data-assets`; 0833 + Cottonwood cohorts live; daily gold snapshot

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>staged</status>
<hold>ANDREW HOLD 2026-07-14 ~00:25Z, verbatim: "Wait to dispatch until I give the go, I want to respawn the workers first." NO work begins on this TO -- staged only. The GO comes from CTO after Andrew's word, addressed to the exact post-respawn serial.</hold>
<project>OPAL_ASSETS — Grand Consolidation P3</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C11)</prd>

## Scope
P3 capstone, gated on C3+C6 (and C10 for the Cottonwood row): repoint `opal-assets-daily-emitter` to
read ONLY the one bucket; retire the six legacy source reads row by row (each retirement evidenced by a
passing emit); add the daily `gold/snapshots/{run_date}.parquet` table dump. Your `overlap_of` field
(read-time dedup, the store never asserts a total) rides the AE landing of your parked patch.

## Fences
The emitter's contract stands: a target weight is INTENT, not an OBSERVATION — missing measured source →
honest partial/missing, never fallback-to-intent. No summing below gold; no combined 0824+0833 total
(record at grain; summing is a presentation question — ruled 3×). mdpf stays frozen; this TO neither
reads it back to life nor waits on it. Nobody writes `opal-data-inf/gold/meta/pipeline-complete.json`.

## <compiler_tools_mandate>
Phase 1: `comp-build` then re-run `comp-blast opal-assets-daily-emitter` (PRD §5 R1: node SHA-drifted;
current no-consumer result is a LOWER BOUND) + literal-key grep for dynamic readers of each of the six
legacy source paths BEFORE retiring its read.
Phase 2: `.tools/commit-gate.sh`; Rule 15; `comp-iam service opal-assets-daily-emitter` if its role
needs the new-bucket read grant — then the live simulate per 22a against the exact new-bucket ARNs
(comp-iam FAILS GREEN on a new bucket).
Phase 3: `comp-validate --artifact` on the first one-bucket-sourced emit BEFORE the legacy reads retire.
</compiler_tools_mandate>

## <cross_domain_coordination>
DynamoDB `opal-assets-daily-aua` — strictly internal (PRD §5 R3), but the sovereign-held path exclusion
means "no consumer" is not confirmed there; the Phase-1 grep covers the searchable estate and the
retirement is row-by-row precisely so a surprise consumer surfaces loudly, not silently.
</cross_domain_coordination>

## <acceptance_criteria>
1. An emit sourced 100% from `opal-data-assets` produces the full cohort row-set with values matching
   the prior-day legacy-sourced emit at grain (per-cohort diff printed, both denominators).
2. 0833 + Cottonwood-AUA rows present with honest identity tuples (0833 `incomplete` until real data —
   never a placeholder value).
3. `gold/snapshots/{run_date}.parquet` lands daily post-emit, head-object verified.
4. Six legacy reads retired one-by-one, each with a passing emit in evidence.
5. Session log + Compiler Tools section; RAVC close to CTO.
</acceptance_criteria>

<revision v="1.2" date="2026-07-14 ~01:05Z" by="1.0.0_SA_CTO">
THE MONOLITH (Andrew-direct, PRD v1.2 ruling 9): one bucket stores canonical bronze+silver for EVERYTHING; grammar {source}/{scope}/{layer}/...; gold runners/platinum stay where they are. C11: the daily gold snapshot dump (AC3) is DEFERRED per Andrew (gold just the dynamodb to start) -- do not build it in this TO. Emitter reads the monolith trees at {source}/{scope}/silver/. Serving boundary: gold runners/platinum buckets stay where they are; this TO touches ONLY the internal opal-assets-daily-aua path.
</revision>

<revision v="1.3" date="2026-07-14 ~01:15Z" by="1.0.0_SA_CTO">
C11 v1.3: the emitter is THE ONLY PARSE-DOWN POINT in the whole architecture (PRD 2a, Andrew verbatim: only at the lambdas that write to the dynamodb does it get parsed down to Opal ETFs and Opal Model holdings). Selection logic lives here and nowhere upstream; if you find filtering in a parser or pull, that is a defect to route back to CTO.
</revision>

<note date="2026-07-14 ~05:2xZ" by="0.4.0_DS_ClientPlatform (assignee reconciliation, comp-state sweep)">
Still `staged`, correctly -- the C3+C6 gates remain open (0824 remap on pull-terminal; C6 deploy +
event wiring with 0.7.0/AE). Context updates folded so the record reads current: the ~00:25Z Andrew
hold was LIFTED ~01:06Z (CTO GO wave b6db4ce0c -- C11 alone stayed staged BY GATE, not by hold); PRD
S6 fork 3 RESOLVED (16-row cohort set APPROVED, DS implementation hold lifted -- the C10 Cottonwood
row + cohort rows land here when the gates clear); C10 derivation + C6 silver-registry code are
authored/tested, ready to fold on GO.
</note>
