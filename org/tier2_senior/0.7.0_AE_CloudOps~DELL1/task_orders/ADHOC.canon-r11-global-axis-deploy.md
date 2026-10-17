# pipeline-override: MDPF_CANON round 11 (decomposition v11 amendment 2, cell CN-s-6); the round-11 issuance is closed to new order files (ONE ISSUER PER ROUND), so the gold-package deploy that ships CN-s-6 rides one CloudOps ADHOC order, on the precedent of ADHOC.canon-r11-muni-custom-redeploy (its legs apply with the substitutions below).
<task_order id="ADHOC.canon-r11-global-axis-deploy">
<to_id>ADHOC.canon-r11-global-axis-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-17</date>
<status>complete</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 11 of MDPF_CANON; target the 2026-10-18 13:30Z fire; BEHIND the CN-s-6 pair and the issuer's fresh written GO)</priority>

<title>MDPF_CANON CN-s-6 DEPLOY under its never-widen pair: the gold lambda package built from the code commit (one commit on the deployed pin d2f734fbac) with its commit stamp; a no-write dry-run invoke BEFORE (the reference) and AFTER (the test), both RETURNING the built bodies, graded by the issuer; the emitter and everything else are NOT touched</title>
<context>
The 2026-10-17 13:30Z scheduled fire refused to build Global (gate (v), 2026-10-16). The CTO ruled (msgs 7594, 7600) that Global's axis drops the enumerated date 2026-10-16, as the 2026-10-18 13:30Z fire's one gold change. The worker's code commit (CN-s-6) is one frozenset constant and one subtraction in `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` plus one test. **The code commit (the pin of this deploy) is `128fce3524a820c3c912a5f1e28ab149a68c5024`**, a child of the deployed pin `d2f734fbac0f25ea6bee0749b02c4ea0a6fcc3fe`, on branch `wk-MDPF_CANON-33` in this repository (visible to you without a push; build from that SHA).
**Read first:** the pair `org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round11/NEVER_WIDEN_PAIR_R11_CN_S_6.md` (sha256 `9e7b1930e0536e6a0eef0209b91c6add44f6005ec9d002d8a2806e5f310cad61`), its COO signature, and the CTO half (to be recorded at `org/missions/D8/MDPF/MDPF_CANON/ledger/`, binding that sha256). The live function you will move: `CodeSha256` `fAXZ4gdLPspZepxmR9J8l3BfJROkppYOyf3qC2dAd40=`, `MDPF_GOLD_COMMIT` `d2f734fbac...` (re-read at your start).
</context>

<scope>
1. **Legs.** Every leg of ADHOC.canon-r11-muni-custom-redeploy (and, through it, ADHOC.canon-r11-muni-custom-deploy) applies unchanged EXCEPT the following: the pin is the code commit above and not `66ae82d62d`; the `CodeSha256` and `MDPF_GOLD_COMMIT` rollback targets are the live values read at your start (expect `fAXZ4gdLPspZepxmR9J8l3BfJROkppYOyf3qC2dAd40=` and `d2f734fbac`); the baselines are the 16 latest-date served objects' ETag and VersionId read at your start (not the round-11 baseline directory).
2. **PRECONDITIONS, any false means do nothing and report which:** (a) the issuer's written GO naming the code commit, sent after BOTH halves of the CN-s-6 pair are signed; without it this order WAITS as `staged`; (b) the first order's preconditions 2.b, 2.d (the clock: no act within 45 minutes before the 13:30Z fire), 2.e, 2.f; (c) **D2 and D4-new finish by 12:44Z on 2026-10-18**; (d) no other gold change is queued for this fire (the CRO~DDD S34 silver fix and the 7-day carrier re-pull ride a different fire).
3. **ORDER OF ACTS.** (a) before print: whole `mdpf-code-equality.py`, the function's `CodeSha256`, `MDPF_GOLD_COMMIT`, the package object's current VersionId (the rollback target), the 16 served latest-date objects' ETag and VersionId; (b) **D4-ref, BEFORE any deploy:** ONE invoke of the currently deployed function with the schedule's recorded input plus exactly `"qa_local": true` and `"qa_return_bodies": true`, `--cli-read-timeout 0`, the response saved to `C:/dev/_deploy_artifacts/canon_s6/d4_ref_response.json` (outside the repo; print its size and sha256) (Global is expected refused: `errors` {global}, 12 bodies; that is the reference, not a failure); (c) D2: `build_package.py --pin <code commit>`, the package read before upload, upload, the one `.tf` value to the full SHA, ONE targeted `safe-apply` whose plan moves only the function's code and `MDPF_GOLD_COMMIT`; read back; (d) **D4-new:** the same invoke on the new function, the response saved to `C:/dev/_deploy_artifacts/canon_s6/d4_new_response.json` (print size and sha256), then the same 16-object / overwrite-key / store / control-key VersionId reads as the first order's leg (d); (e) **WAIT for the issuer's `D4-PASS` or `D4-STOP`**; the issuer grades against the pair's section 3; (f) the emitter is read at the end: `CodeSha256` `GLQf6kv4nzRLGd53ONG4S5F4ikOso/2lkbq03U/+G9A=` unchanged; (g) after print; close the ledger.
4. **Rollback** exactly as the pair's section 3 says (the live values read in (a)), and at once on `D4-STOP`.
5. Close the ledger. Report to `2.0.0_SA_COO~D1`, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
infra/aws/terraform/mdpf-pipeline/gold-lambda.tf
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the built package read before upload, then the targeted plan on mdpf-gold-lambda, then safe-apply -target, then the deployed package manifest and the function environment read back</invocation>
  <expect>the package members that differ from the pin's build carry the code commit's sha256 and only data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py differs; the plan moves only the function's code and MDPF_GOLD_COMMIT; MDPF_GOLD_COMMIT equals the full code commit SHA and the package manifest's source_vintage.commit; CodeSha256 differs from fAXZ4gdLPspZepxmR9J8l3BfJROkppYOyf3qC2dAd40=</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the two invocations of mdpf-gold-lambda (D4-ref before the deploy, D4-new after) with the schedule's recorded input plus exactly qa_local true and qa_return_bodies true, both responses saved outside the repo, then the before and after reads of the 16 latest-date served objects, the overwrite keys, each tax-prelude store's existing object, the control key by VersionId and the emitter's CodeSha256; then the issuer's D4-PASS or D4-STOP</invocation>
  <expect>each invoke 200 with no FunctionError; D4-ref errors {global} and 12 bodies, D4-new status green, errors empty, a4_objects_built 16 and 16 bodies, both saved with their sha256 printed; every served object, overwrite key, store object and the control key read the same VersionId after each dry run; the emitter CodeSha256 unchanged; the issuer's D4-PASS received (D4-STOP means section 4 ran and was read back)</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the whole-tree print before and after, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger; the DIFFER names stated as known; this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
