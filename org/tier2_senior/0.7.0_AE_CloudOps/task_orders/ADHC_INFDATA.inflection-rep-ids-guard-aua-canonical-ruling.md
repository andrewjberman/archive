<to_id>ADHC_INFDATA.REPIDS</to_id>
<project>ADHC_INFDATA (inf-data-cleanup, NEW low-pri)</project>
<title>Resolve 7 pre-existing inf comp-constants drifts: INFLECTION_REP_IDS [3,11,12] vs [3,6,11,12] (is rep 6 in scope?) + GUARD_B_AUA threshold drift — needs inf-data RULING before fixing</title>
<assigned_to>0.7.0_AE_CloudOps (pending inf-data ruling)</assigned_to>
<issued_by>2.0.0_SA_COO (deferred from AE TO-6 RAVC2 disclosure 171929Z; DS flagged at P1-DS 162016Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADHC_INFDATA (inf-data-cleanup, NEW low-" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending-ruling -- LOW-PRI, NOT blocking (pre-existing drift, inf pipeline runs fine, comp-constants check rc=1 on these only). Do NOT touch canonical or sites until an inf-data ruling. Surfaces to Andrew/inf-data when worked.</status>

7 PRE-EXISTING inf-lane comp-constants drifts (surfaced by AE TO-6 comp-build, NOT introduced by cot registration):
1. INFLECTION_REP_IDS (5 sites): registered canonical = [3,11,12] (3 ids); 5 LIVE sites use [3,6,11,12] (4 ids, includes rep 6). Sites: data/inf/manual_api/pull_inflection_{assets,representatives,transactions}.py + infra inf-pipeline inf-api-reps + inf-api-txn copies.
2. GUARD_B_AUA_LOWER/UPPER (2 sites): infra/.../inf-api-txn/_orion_api_silver_lib.py:38-39 — numeric-threshold drift vs canonical (likely stale canonical).

RULING NEEDED (inf-business-data, not code-drift): is rep id 6 an in-scope Inflection rep? If YES -> fix the canonical to [3,6,11,12]. If NO -> fix the 5 sites to [3,11,12]. This is a DATA-correctness call (which reps are in scope) -> Andrew/inf-data, NOT a unilateral agent fix. GUARD_B_AUA = investigate whether canonical or sites are stale, fold into the same ruling. Also folds the 5 manual_api debt files DS excluded from P1-DS (Rule-14 debt + this data decision).

When ruled: AE fixes whichever side (canonical config OR the sites) under the ruling, Rule 14, comp-build 0-drift, RAVC2 -> COO+CTO.
