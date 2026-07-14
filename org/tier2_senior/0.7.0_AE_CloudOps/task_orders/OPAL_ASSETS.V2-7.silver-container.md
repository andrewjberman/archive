# OPAL_ASSETS.V2-7 — the silver container (events + roles + sweep schedules + DLQ)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>staged</status>
<go>HARD GATE: the V2-5 certificate ACCEPTED by CTO (bronze categorically wrapped). COO dispatches the GO on that acceptance. Your V2-5 IAM-sweep half is separate and starts now under that TO.</go>
<project>OPAL_ASSETS — V2 Phase II silver conversion layer</project>
<prd>docs/architecture/OPAL_ASSETS_V2_PRD.md §3 rulings 22-25 + V2-7 (@ 53ba45c5f); inherits CONSOLIDATION_PRD v1.6.0 whole</prd>

## THE GOAL (ruling 22 — EVENT + SWEEP, verbatim)
"Silver converters fire on S3 `ObjectCreated` notifications on the monolith's `*/bronze/` prefixes
(monolith-side events are free under new-territory) — plus one daily reconciliation sweep (scheduled,
per channel) that computes bronze<->silver per-folder set-identity and converts anything the event path
missed. The event gives latency; the sweep is the conservation instrument — a per-object event model is
structurally blind to the object that never arrived (v1.2 doctrine), so the sweep is load-bearing, not
belt."

Build:
1. S3 notification wiring: bronze prefixes -> converter lambdas (nothing event-triggers on meta keys —
   ruling 21/25).
2. Converter execution roles: per-channel, monolith-scoped, never-widen + 22a exercised with fence
   negatives (firm buckets, Door-6 key, out-of-scope monolith prefixes).
3. The daily reconciliation-sweep schedules (per channel).
4. DLQ on the event path — an event lambda that dies silently is the 22b class; the DLQ is where its
   death becomes visible. NOT an alarm (no-alarms constraint): a queue + a sweep that reads it.

## <compiler_tools_mandate>
Pure to-add TF plan — a plan that is not pure "to add" is out of scope (new-territory rule). Apply gates
CTO (every apply). 22a per role: live simulate-principal-policy on EXACT ARNs, one --resource-arns per
call, positive controls separate, recorded outputs as evidence. comp-iam service as the necessary-not-
sufficient first pass. `.tools/commit-gate.sh` on every .py; Rule 15 futures import; TF via safe-apply.
</compiler_tools_mandate>

## <cross_domain_coordination>
Converter CODE is V2-8 (DS) — you build the container it runs in; coordinate the lambda names/handlers
with DS before the TF lands. Nothing writes `opal-data-inf/gold/meta/pipeline-complete.json` (Door 6).
The bucket's notification configuration is currently EMPTY (measured) — you are its first writer; keep
it monolith-only.
</cross_domain_coordination>

## <acceptance_criteria>
1. TF plan pure to-add, CTO-gated apply, 0-diff re-plan, tagged per deploy rules.
2. Event path exercised: a probe bronze object under a test prefix fires the converter (or its DLQ
   records the death) — the path that fails if the wiring is wrong.
3. Sweep schedules ENABLED + first natural fire verified on behavior (not config read).
4. Per-role 22a evidence committed. RAVC to COO; apply gate CTO.
</acceptance_criteria>
