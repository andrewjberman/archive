# pipeline-override: MDPF_CANON round 11 (decomposition v11, cell CN-s-1 drained @66ae82d62d); the round-11 issuance is closed to new order files (ONE ISSUER PER ROUND), so the redeploy of the gold package after the D4-STOP and the V2 never-widen pair rides one CloudOps ADHOC order, on the precedent of ADHOC.canon-r11-muni-custom-deploy (its legs apply with the substitutions below).
<task_order id="ADHOC.canon-r11-muni-custom-redeploy">
<to_id>ADHOC.canon-r11-muni-custom-redeploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-16</date>
<status>complete</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 11 of MDPF_CANON; target the 2026-10-17 13:30Z fire; BEHIND the V2 pair and the issuer's fresh written GO)</priority>

<title>MDPF_CANON CN-s-1 REDEPLOY under the V2 never-widen pair: the gold lambda package at pin 66ae82d62d with its commit stamp, one dry-run invoke that RETURNS the built bodies, graded by the issuer against the V2 leaf set; the emitter and everything else are NOT touched</title>
<context>
The first deploy (ADHOC.canon-r11-muni-custom-deploy) landed D2 at 16:22Z and D4 at 16:24Z; the issuer's D4-STOP (16:32Z) fired because the Global headline rose by the account's value, which the first pair had predicted equal. You rolled back (16:32-16:36Z) and I read it live (CodeSha256 `vNRXwWymIRmgptYv8+PEyFWH73IpIVHOpdT5mL/B7uk=`, MDPF_GOLD_COMMIT `b6352de8f843f3726ad5c51c650d9035ca8336db`). The CTO ruled (msg 6876) that the Global rise is the fold's own rule and that a NEW pair names it. This order redoes the SAME D2 and D4 under that pair. **Nothing about the code changes: the pin is `66ae82d62d7eac16d64a812ab41dc36cd51a2c30`.**
**Read first:** the V2 pair `org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round11/NEVER_WIDEN_PAIR_R11_CN_S_1_V2.md` (sha256 `bccb55392486e83f0e0bda35994216f015baaa79f13c7b8d037c4fe5c1e602b1`), its COO signature `..._V2_COO_SIGN.md`, and the CTO half (to be recorded at `org/missions/D8/MDPF/MDPF_CANON/ledger/`, binding that sha256).
</context>

<scope>
1. **Legs.** Every leg of ADHOC.canon-r11-muni-custom-deploy applies unchanged EXCEPT the following. You reuse the facts you already measured today (the identity flag, the SMArtX inputs, the runner layout read: **D1 stays NOT DONE under 2.g(ii)**) only if they are re-read at your start (a stated minute, flags and counts only); the baselines are the 16 `baseline/<scope>__<type>.json` you saved before the first D2, and you re-read the 16 latest-date served objects' ETag and VersionId to confirm nothing wrote since (a changed object means a new baseline is saved and reported).
2. **PRECONDITIONS, any false means do nothing and report which:** (a) the issuer's written GO naming the pin, sent after BOTH V2 halves are signed; without it this order WAITS as `staged`; (b) the first order's preconditions 2.b, 2.d (the clock: no act within 45 minutes before the 13:30Z fire), 2.e, 2.f; (c) **D2 and D4 finish by 12:44Z on 2026-10-17.**
3. **ORDER OF ACTS.** (a) before print: whole `mdpf-code-equality.py`, the function's `CodeSha256` (expect `vNRXwWymIRmgptYv8+PEyFWH73IpIVHOpdT5mL/B7uk=`), `MDPF_GOLD_COMMIT`, the package object's current VersionId (the rollback target); (b) D2 exactly as the first order's leg (c): `build_package.py --pin 66ae82d62d`, the package read before upload (seven members differ from `b6352de8f8`'s build, carrying the pin's sha256), upload, the one `.tf` value to the full SHA, ONE targeted `safe-apply` whose plan moves only the function's code and `MDPF_GOLD_COMMIT`; read back; (c) D4: ONE invoke with the schedule's recorded input plus exactly `"qa_local": true` and `"qa_return_bodies": true`, `--cli-read-timeout 0`, the response saved to `C:/dev/_deploy_artifacts/canon_r11_muni/d4b_response.json` (outside the repo; print its size and sha256), then the same 16-object / overwrite-key / store / control-key reads as the first order's leg (d); (d) **WAIT for the issuer's `D4-PASS` or `D4-STOP`**; the issuer diffs the bodies against the V2 pair's section 1, not against the first pair; (e) the emitter is read at the end: `CodeSha256` `GLQf6kv4nzRLGd53ONG4S5F4ikOso/2lkbq03U/+G9A=` unchanged; (f) after print; close the ledger.
4. **Rollback** exactly as in the first order's section 4, and on `D4-STOP` at once.
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
  <expect>exactly seven members differ from the round-10 build and carry the pin's sha256; the plan moves only the function's code and MDPF_GOLD_COMMIT; MDPF_GOLD_COMMIT equals the full pin SHA and the package manifest's source_vintage.commit; CodeSha256 differs from vNRXwWymIRmgptYv8+PEyFWH73IpIVHOpdT5mL/B7uk=</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the one invocation of mdpf-gold-lambda with the schedule's recorded input plus exactly qa_local true and qa_return_bodies true, the response saved outside the repo, then the before and after reads of the 16 latest-date served objects, the overwrite keys, each tax-prelude store's existing object, the control key by VersionId and the emitter's CodeSha256; then the issuer's D4-PASS or D4-STOP</invocation>
  <expect>invoke 200 with no FunctionError, status green, errors empty, a4_objects_built 16, 16 bodies returned and saved with their sha256 printed; every baseline object, overwrite key, store object and the control key read the same VersionId after the dry run; the emitter CodeSha256 unchanged; the issuer's D4-PASS received (D4-STOP means section 4 ran and was read back)</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the whole-tree print before and after, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger; the DIFFER names stated as known (D1 NOT DONE under 2.g(ii)); this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
