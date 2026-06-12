<to_id>NFRA_GRAPHS.D7-FIX.T4</to_id>
<project>NFRA_GRAPHS</project>
<title>D7-FIX T4 — BD nna_clients.json gold script attribution investigation (prefix-match D_04 name mismatch)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (D7 real_bug candidate #4, 164849Z RAVC2)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete</status> -- VERDICT (read-only, no code change): comp-platinum's prefix-match to D_04::build_firm_mix_summary() is WRONG for all 3, in 2 ways. (1) nna_clients.json: D_04 IS the producer but via build_advisor_nna_clients() (writes L2653), NOT build_firm_mix_summary (which writes only platinum/firm/mix_summary.json L482) -> right SCRIPT, WRONG FUNCTION. (2) timeseries.json: D_04 producer via build_advisor_summaries() (writes L687) -> right SCRIPT, WRONG FUNCTION. (3) exec_summary.json: D_04 does NOT write it (only a stale-cleanup comment L708); REAL producer = the exec_summary_generator LAMBDA (aws_lambda_function.exec_summary_generator, infra/aws/lambda/exec-summary-generator/exec_summary/; nightly batch reads platinum/advisors/{id}/summary.json -> writes exec_summary.json; portal advisor-intelligence.ts:1352 confirms "nightly batch artifact") -> WRONG SCRIPT entirely (Lambda, not gold tree). Root cause: comp-platinum resolves by platinum/advisors/{id}/ PREFIX to the earliest D_04 function, not by full key->actual-writer; and it has no Lambda producers in its graph so Lambda-produced platinum artifacts get swept onto a prefix-sharing gold script. RAVC2 -> COO.
<priority>medium — potential producer gap if D_04 is the wrong gold script for these per-advisor artifacts</priority>

<scope>
comp-platinum resolves BD `platinum/advisors/{id}/nna_clients.json` via prefix-match to `D_04 :: build_firm_mix_summary()`. The artifact name (`nna_clients`) doesn't align with the script name (`build_firm_MIX_summary`). Same prefix-match issue appears for `platinum/advisors/{id}/exec_summary.json` and `platinum/advisors/{id}/timeseries.json` on AdvisorPublicProfile (all matching `build_firm_mix_summary`).

Investigation question: does `D_04 :: build_firm_mix_summary()` actually write `platinum/advisors/{id}/nna_clients.json`, `exec_summary.json`, and `timeseries.json`? Or is comp-platinum's prefix-match misleading and the real producer is a different script?

Steps:
1. Read `data/black_diamond/scripts/gold/D_04.py` — check what S3 keys it actually writes
2. If D_04 writes those keys: prefix-match is correct, mark as `false_positive` in your RAVC2 note (the name mismatch is cosmetic)
3. If D_04 does NOT write those keys: identify the real producer script; this is a prod visibility gap (comp-platinum can't resolve the chain, AND we don't know which gold script to watch for breakage). RAVC2 with the correct producer + request a comp-pipescript consumers fix TO if needed.

Acceptance: RAVC2 to COO with verdict (D_04 is/is not the real producer) + evidence (S3 write calls found/not found in the script).
</scope>
