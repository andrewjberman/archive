<to_id>MDPF_ASSETS.FREEZE-DX</to_id>
<project>MDPF_ASSETS</project>
<title>MDPF_ASSETS FREEZE-DX -- investigate the MDPF (Opal Aggregate AUA) SERVED FREEZE: trace the aggregate pipeline, localize the stuck stage, ground the root-cause MECHANISM</title>
<assigned_to>0.5.0_AE_OpalETL (role-fit: OpalETL owns the MDPF aggregate pipeline; MDPF_ASSETS pod 0.5)</assigned_to>
<verify>3.0.0_SA_CVO (root-cause grounding + served-freeze characterization)</verify>
<issued_by>2.0.0_SA_COO (Andrew-direct 2026-06-25: "MDPF has been frozen for days -- investigate what is going on")</issued_by>
<issued_date>2026-06-25</issued_date>
<status>dx-delivered-pending-verify</status>
<!-- 2026-06-25 0.5.0_AE: DIAGNOSIS COMPLETE + RAVC'd to COO (Rule-22 grounded: source mdpf-daily-trigger/lambda_function.py:54-179,222-236 + runtime CloudWatch gate decisions + s3 partition ground-truth). ROOT = MDPF convergence gate correctly DEFERS on stale BD silver/fees (latest 06-18, frozen since 06-19 BD-49F break); NOT an MDPF-side break. Cross-link CONFIRMED: downstream victim, fees is a separate scrape feed (bd_fees EC2, COO-EXEMPT) NOT covered by 0.6.0's DataMining-REST P1 (which fixed allocations). FIX routes to BD lane (CVO/0.6.0 restore bd-fees); MDPF auto-recovers forward once fees <=2 trading-days fresh; interior gap-day backfill optional+manual. No MDPF code change. dx report: logs/2026-06-25/MDPF_ASSETS.FREEZE-DX_diagnosis.md. <verify> = 3.0.0_SA_CVO (grounding citations handed). Standing by on MDPF re-run/verify. -->

<!-- GO: Andrew-direct 2026-06-25 (COO spawning 0.5.0_AE FOR this). INVESTIGATION/DIAGNOSIS TO -- find + ground the root cause; PROPOSE the fix; do NOT self-authorize a fix-deploy (RAVC the dx + proposed fix to COO first; a fix-TO follows). -->

<objective>
Andrew reports the MDPF served output (Opal Aggregate AUA -- Multi-Partner Model Portfolio Asset Tracking) has been FROZEN for DAYS. INVESTIGATE: localize WHERE the freeze is in the MDPF aggregate pipeline (smartx + inf-pipeline/Eclipse + etfs + portal -> aggregate-AUA), and GROUND the root-cause MECHANISM (not just the symptom). Deliver a diagnosis + a proposed fix. This is the same class as the cot-AUA + BD-49F freezes seen this week (a served-output freeze on a completed pipeline) -- apply the banked freeze-diagnosis discipline.
</objective>

<the_work>
1. CHARACTERIZE the freeze (symptom, served-grounded): WHICH MDPF served artifact(s) are stale, the exact frozen-as-of date, and how many days (comp-freshness on the MDPF served + each upstream stage). Confirm Andrew's "frozen days" against the live/served artifact.
2. LOCALIZE the stuck stage: trace the aggregate pipeline (pipescript / comp-pipescript) -- smartx, inf-pipeline (Eclipse), etfs, and the aggregation/portal-serve step. WHICH stage froze first (the others may be downstream-stale off it)? Use comp-freshness per-stage to find the first-frozen upstream (the same "selective freeze localizes the break" method that pinned the BD-49F ingest).
3. GROUND the root-cause MECHANISM (Rule 22 -- not a hypothesis): read the SOURCE/producer + the dependency graph for the stuck stage. Is it an ingest break (a partner feed died -- cf. BD-49F SS&C-MFA), a sentinel/cadence stall (cf. cot silver-merge-freeze -> sentinel-never-fires), a scheduler/cron failure, an IAM/secret expiry, or a consumer-edge issue? CITE the grounding (file:line or comp-tool output). Mechanism = INFERRED until source+graph-confirmed.
4. CHECK for shared causes: MDPF aggregates partner pipelines -- if a partner ingest (BD-49F, cot, inf-Eclipse) is the frozen upstream, note the cross-link (the BD-49F freeze + the cot/inf work are live this session; MDPF may be a downstream-victim of one of them, NOT an independent break).
</the_work>

<compiler_tools_mandate>
- comp-freshness on the MDPF served + each upstream stage (smartx/inf/etfs/aggregate) -- localize the first-frozen stage.
- pipescript <mdpf/aggregate name> + comp-pipescript io/deployed -- trace the aggregate pipeline producers->served + find the stuck producer.
- comp-blast on the stuck producer -- consumer/blast radius (what else the freeze degrades).
- Source-read (Read) the stuck producer + comp-iam if a secret/role expiry is suspected. Rail-grounded, NOT raw grep. Log every comp run + the org/compiler-tools-log.md line.
</compiler_tools_mandate>

<cross_domain_coordination>
MDPF aggregates partner pipelines (pods 0.4/0.5/0.6/0.7). If the frozen upstream is a partner ingest already under active investigation this session -- the BD-49F DataMining freeze (CVO/0.6.0_AE lane, ADVI_BDAPIMIG) or the cot/inf work (DS canonize-gold) -- DO NOT duplicate; flag the cross-link to COO + coordinate with that lane's owner (MDPF may be a downstream victim, not an independent break). The aggregate may simply inherit a partner-feed freeze. cc COO on the localization.
</cross_domain_coordination>

<acceptance_criteria>
1. The freeze CHARACTERIZED: which MDPF served artifact(s), exact frozen-as-of date, days-stale -- served-grounded (comp-freshness), confirming/correcting Andrew's "frozen days".
2. The stuck stage LOCALIZED: the first-frozen stage in the aggregate pipeline (smartx/inf-Eclipse/etfs/aggregate), with the per-stage freshness evidence.
3. The root-cause MECHANISM GROUNDED (Rule 22): source+graph-confirmed (file:line / comp-tool output), not an ungrounded hypothesis. Cross-link flagged if it inherits a partner-feed freeze.
4. A PROPOSED FIX (scoped, not yet deployed) + RAVC the dx to COO. Rail-grounded. Session log + Compiler Tools section.
</acceptance_criteria>
