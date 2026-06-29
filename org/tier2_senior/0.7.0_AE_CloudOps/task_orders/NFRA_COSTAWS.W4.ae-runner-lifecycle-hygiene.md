<to_id>NFRA_COSTAWS.W4</to_id>
<project>NFRA_COSTAWS</project>
<title>Runner lifecycle/hygiene (idle-cap guardrail generalization)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 Andrew-direct NFRA staffing; decomposition per CTO dispatch list 174053Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete</status>

Generalize the idle-cap guardrail (the i-0ed5 inf-gold ~$30 idle incident class) across runners; lifecycle hygiene rules. BINDING: never modify System tags on bd-gold-layer-runner / inf-gold-layer-runner. RAVC2 to COO.

<closeout author="0.7.0_AE_CloudOps~B" date="2026-06-29" reviewer="2.0.0_SA_COO (ACCEPT 135727Z)">
CORE DONE + SUPERSEDED (grounded at source): the idle-cap generalization was achieved 2026-06-05 by the UNIVERSAL idle-ceiling enforcer redesign (Andrew "everything on the 3hr kill") -- ec2-auto-shutdown-enforcer/lambda_function.py:1-43 replaced the per-ID EXCLUDED/IDLE_CEILING_INSTANCES allowlist (the exact i-0ed5 class) with one universal rule on EVERY instance, idle-aware, exempt only by AutoShutdown=disabled. Idle-burn class structurally closed, no list maintenance.
HYGIENE CENSUS FILED (read-only, 0 mutations): docs/briefs/nfra-costaws-w4-runner-lifecycle-hygiene-census-20260629.md (fb35565cd). Estate clean -- 0 unattached volumes, ~30d-bounded snapshot retention, 1 trivial gp2.
2 MINOR FOLLOW-ONS (tracked separately, NOT AE-unilateral): W4-S1 = 10 orphaned daily snapshots (~$4/mo; daily-snapshot orphan-reap gap) -> Andrew minor-queue (COO); W4-S2 = live IDLE_CPU_THRESHOLD=1.0 vs code-default 3.0 -> CTO/Andrew tuning call. Neither blocks W4.
</closeout>
