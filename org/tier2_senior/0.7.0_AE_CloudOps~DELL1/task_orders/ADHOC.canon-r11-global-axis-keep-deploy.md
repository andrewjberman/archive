# pipeline-override: MDPF_CANON round 11 (decomposition v11 amendment 3, cell CN-s-7); the round-11 issuance is closed to new order files (ONE ISSUER PER ROUND), so the gold-package deploy that ships CN-s-7 rides one CloudOps ADHOC order, on the precedent of ADHOC.canon-r11-global-axis-deploy (its legs apply with the substitutions below).
<task_order id="ADHOC.canon-r11-global-axis-keep-deploy">
<to_id>ADHOC.canon-r11-global-axis-keep-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-19</date>
<status>complete</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 11 of MDPF_CANON; target the 2026-10-20 13:30Z fire; BEHIND the CN-s-7 pair and the issuer's fresh written GO)</priority>

<title>MDPF_CANON CN-s-7 DEPLOY under its never-widen pair: the gold lambda package built from the code commit (one commit on the deployed pin 128fce3524) with its commit stamp; a no-write dry-run invoke BEFORE (the reference) and AFTER (the test), both RETURNING the built bodies, graded by the issuer; the emitter and everything else are NOT touched</title>
<context>
The 2026-10-19 13:30Z scheduled fire found all three staged legs ending 2026-10-16 with values, so CN-s-6's drop of that date holds Global at as_of 2026-10-15. The CTO ruled (ruling record `org/missions/D8/MDPF/MDPF_CANON/ledger/CTO_RULING_S36_EMPTY_GLOBAL_AXIS_DROP_20261019.md` @176378e74d) to empty the drop set as the 2026-10-20 13:30Z fire's one gold change. The worker's code commit (CN-s-7) empties one constant and replaces one test in `data/mdpf/scripts/gold/`. **The code commit (the pin of this deploy) is `3d3d5ed5b91069a68b77d2d26b1ca37ae6a8fd8a`**, a GRANDCHILD of the deployed pin `128fce3524a820c3c912a5f1e28ab149a68c5024` (its parent is the issuer's grant commit `bda12c93f5`, which adds only an order, the decomposition and a check; see `NEVER_WIDEN_PAIR_R11_CN_S_7_ADDENDUM_1_ANCESTRY.md`), on branch `wk-MDPF_CANON-34` (origin tip `6be83371a2`, two commits beyond the code commit): build from the SHA `3d3d5ed5b9...`, never from the branch tip.
**Read first:** the pair `org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round11/NEVER_WIDEN_PAIR_R11_CN_S_7.md` (sha256 `bb0120bb4412dd051b740ffe3cd9f5bb1fcda2233946cb5a9686653ebe36c3af`), its COO signature, and the CTO half (to be recorded at `org/missions/D8/MDPF/MDPF_CANON/ledger/`, binding that sha256). The live function you will move: `CodeSha256` `whMJ8Ei9g0ZUDFEUxSaEQAViS0kokkxt9CS+vlD7SGI=`, `MDPF_GOLD_COMMIT` `128fce3524...` (re-read at your start).
</context>

<scope>
1. **Legs.** Every leg of ADHOC.canon-r11-global-axis-deploy applies unchanged EXCEPT the following: the pin is the code commit above and not `128fce3524`; the `CodeSha256` and `MDPF_GOLD_COMMIT` rollback targets are the live values read at your start (expect `whMJ8Ei9g0ZUDFEUxSaEQAViS0kokkxt9CS+vlD7SGI=` and `128fce3524`); the baselines are the 16 latest-date served objects' ETag and VersionId read at your start; the response files go to `C:/dev/_deploy_artifacts/canon_s7/` (outside the repo, client-scale).
2. **PRECONDITIONS, any false means do nothing and report which:** (a) the issuer's written GO naming the code commit, sent after BOTH halves of the CN-s-7 pair are signed; without it this order WAITS as `staged`; (b) the first order's preconditions 2.b, 2.d (the clock: no act within 45 minutes before the 13:30Z fire), 2.e, 2.f; (c) **D2 and D4-new finish by 12:44Z on 2026-10-20**; (d) no other gold change is queued for this fire.
3. **ORDER OF ACTS.** (a) before print: whole `mdpf-code-equality.py`, the function's `CodeSha256`, `MDPF_GOLD_COMMIT`, the package object's current VersionId (the rollback target), the 16 served latest-date objects' ETag and VersionId; (b) **D4-ref, BEFORE any deploy:** ONE invoke of the currently deployed function with the schedule's recorded input plus exactly `"qa_local": true` and `"qa_return_bodies": true`, `--cli-read-timeout 0`, the response saved to `C:/dev/_deploy_artifacts/canon_s7/d4_ref_response.json` (print its size and sha256) (Global is expected to build at as_of 2026-10-15 over the live legs; that is the reference); (c) D2: `build_package.py --pin <code commit>`, the package read before upload, upload, the one `.tf` value to the full SHA, ONE targeted `safe-apply` whose plan moves only the function's code and `MDPF_GOLD_COMMIT`; read back; (d) **D4-new:** the same invoke on the new function, the response saved to `C:/dev/_deploy_artifacts/canon_s7/d4_new_response.json` (print size and sha256), then the same 16-object / overwrite-key / store / control-key VersionId reads as the first order's leg (d); (e) **WAIT for the issuer's `D4-PASS` or `D4-STOP`**; the issuer grades against the pair's section 2; (f) the emitter is read at the end: `CodeSha256` `GLQf6kv4nzRLGd53ONG4S5F4ikOso/2lkbq03U/+G9A=` unchanged; (g) after print; close the ledger.
4. **Rollback** exactly as the pair's section 2 says (the live values read in (a)), and at once on `D4-STOP`.
5. Close the ledger (NEVER-2: opened before (a), its close committed, every live worktree read at the drain). Report to `2.0.0_SA_COO~D1`, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
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
  <expect>only data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py differs from the pin's build and carries the code commit's sha256; the plan moves only the function's code and MDPF_GOLD_COMMIT; MDPF_GOLD_COMMIT equals the full code commit SHA and the package manifest's source_vintage.commit; CodeSha256 differs from whMJ8Ei9g0ZUDFEUxSaEQAViS0kokkxt9CS+vlD7SGI=</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the two invocations of mdpf-gold-lambda (D4-ref before the deploy, D4-new after) with the schedule's recorded input plus exactly qa_local true and qa_return_bodies true, both responses saved outside the repo, then the before and after reads of the 16 latest-date served objects, the overwrite keys, each tax-prelude store's existing object, the control key by VersionId and the emitter's CodeSha256; then the issuer's D4-PASS or D4-STOP</invocation>
  <expect>each invoke 200 with no FunctionError, status green, errors empty, a4_objects_built 16 and 16 bodies, both saved with their sha256 printed; every served object, overwrite key, store object and the control key read the same VersionId after each dry run; the emitter CodeSha256 unchanged; the issuer's D4-PASS received (D4-STOP means section 4 ran and was read back)</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the whole-tree print before and after, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger; the DIFFER names stated as known; this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
