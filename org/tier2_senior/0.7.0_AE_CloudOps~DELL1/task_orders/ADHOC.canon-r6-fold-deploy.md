# pipeline-override: MDPF_CANON round 6 (decomposition v6, cell CN-f-1, drained @51cfc93ea8); the round-6 issuance @64def41849 is closed to new order files (ONE ISSUER PER ROUND), so the deploy of CN-f-1's four gold scripts, the lambda package and its environment stamp, and the one dry-run invoke ride one CloudOps ADHOC order, on the MDPF_CANON round-2, round-3 and round-4 precedents (ADHOC.canon-r2-publisher-layer-and-builder-grant, ADHOC.canon-r3-bronze-intake, ADHOC.canon-r4-code-deploy).
<task_order id="ADHOC.canon-r6-fold-deploy">
<to_id>ADHOC.canon-r6-fold-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-13</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 6 of MDPF_CANON; BEHIND the issuer's written GO that W8-S4 is closed -- see PRECONDITIONS)</priority>

<title>MDPF_CANON CN-f-1: Global per-model lines are shown on a date only where at least two firms hold them -- four named scripts to code/, the gold lambda package with its commit stamp, one dry-run invoke; the emitter package is NOT touched</title>
<context>
Cell CN-f-1 (order `task-orders/MDPF_CANON.TO-CN-f-1.global-min-firms-fold.md`, merged `51cfc93ea8`, AMENDMENT 1 = the CTO's ADDENDUM 6) changes four
gold scripts, one byte-equal twin and one test:
- `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`: `apply_global_min_firms_fold` and `guard_global_min_firms_fold(arts, isolated)`, called in
  `build_all` directly after `guard_global_served_identity` (`arts, fold_report = guard_global_min_firms_fold(arts, _isolated)`). A refusal, including a
  one-firm as-of pool, sets global to None and records it under `manifest["errors"]["global"]`; the three firm scopes build as before.
- `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py`: `fold_keys` / `fold_emit` on `build_firm_distribution`; the runner's CLI passes none.
- `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`: `other_models` in `MODEL_ORDER` and `SERVED_MODEL_NAME`.
- `data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py` (+ the byte-equal twin under `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/`): the
  `other_models` row. The twin is repo parity ONLY, see leg 3e.
All four gold scripts are in the gold lambda package closure (`infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py` :135-142), so the served
bytes change only after D2 below. The never-widen pair is written on both halves: the COO half in
`org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round6/NEVER_WIDEN_PAIR_R6_CN_F_1.md` and the CTO half in
`org/missions/D8/MDPF/MDPF_CANON/ledger/NEVER_WIDEN_R6_CN_F_1_CTO_HALF.md`. Read the pair first: sections 2, 4 and 5 are this order's acts, blast
radius and every branch.

What the order carries beyond CN-d-1's shape (read these three lessons of `ADHOC.canon-r4-code-deploy`):
1. AMENDMENT 3 there: the A4 writer is write-once per dated key, so no on-demand run lands a change on a date a scheduled fire already wrote. The
   served-key acceptance of THIS order is read by the issuer on the first scheduled fire that mints a new date, and is not a leg of this order.
2. The environment stamp (row D1-S18): `MDPF_GOLD_COMMIT` must equal the pin actually built; `gold-lambda.tf` says so and CN-d-1's D2 left it at
   `88e974ca10`. This order sets it in the same apply, and is the one order authorized to move an environment attribute.
3. The CTO's C-S65: an on-demand gold run writes state beyond the A4 objects; the pair section 4 names them all, and leg 3d reads each store's
   VersionId before and after.
</context>

<scope>
1. Edit no source file EXCEPT `infra/aws/terraform/mdpf-pipeline/gold-lambda.tf`: the value of `MDPF_GOLD_COMMIT` in the function's environment block and
   the comment paragraph above it (the file's own rule: SET THIS FROM THE --pin YOU ACTUALLY BUILT WITH, with the zip's sha256 and the previous value as
   the rollback). No other line of that file moves. Open a deploy ledger (NEVER-2) BEFORE the first act; name in it the four keys, the lambda
   `mdpf-gold-lambda`, the `.tf` value, and every consumer that reads a global served object.
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's written GO that W8-S4 is closed: CN-d-1's served-key read on the 2026-10-13 13:30Z scheduled fire (global account-distribution of a
      new date carries `meta.cottonwood_fold.value_date` and `age_trading_days`, every other key equal). CN-d-1's ledger
      `mdpf-canon-r4-code-deploy-dell1-20261012` reads CLOSED (two acts never copy one key in one window). The GO is a committed line or a broker
      message from `2.0.0_SA_COO~D1`; without it this order WAITS.
   b. The pin `51cfc93ea8` (or a later commit that carries `mdpf_gold_consolidator.py`, `dim_mdpf_account_distribution.py`, `dim_mdpf_aum_metrics.py`
      and `mdpf_revamp_model_crosswalk.py` unchanged -- read by content: `git show <pin>:<path>` against the merged blobs) is an ancestor of origin's
      `box/dell1` (`git ls-remote` then `git merge-base --is-ancestor`).
   c. Both halves of the pair are SIGNED, read from the two files named in the context (a signature is a line in a commit by that seat).
   d. The clock: no act of D1 or D2 starts within 45 minutes before the 13:30Z gold fire or while the runner dispatch or the gold lambda is running
      (read the runner's status and the lambda's last invocation first); D4 (leg 3d) starts only after that day's fire has written its manifest
      (read `_manifests/<as_of>/` for a manifest newer than 13:30Z today).
   e. No FIRMBKTS window act is in flight: read its ledgers first (`org/critical_paths/.open_deploys/advi-firmbkts-*`) and start only in a gap between
      its acts. This order touches NONE of the R2 surfaces (`shared-advisor-router`, the guard, the CloudFront behaviours,
      `data/mdpf/config/bronze_homes.json`, `firm-config.mjs`, the portal-auth WAF rider): D1 names four scripts, D2 is the lambda package and one
      environment value. If a FIRMBKTS act regenerates `bronze_homes.json` while this order is open, the equality print reports it as that act's fact.
   f. One change per scheduled fire: no open deploy sentinel names `mdpf-gold-lambda` or `code/scripts/gold/` other than this order's own, and nothing
      else is planned for them before the next 13:30Z fire (read `org/critical_paths/.open_deploys/`).
3. **ORDER OF ACTS (the order is the safety):**
   a. **Before print.** `python .tools/mdpf-code-equality.py` whole; attach it to the ledger. Record, for each of the four keys under
      `s3://opal-data-mdpf/code/scripts/gold/`, the prior ETag and VersionId (rollback). Record the function's `CodeSha256`, `LastModified` and its
      environment (`MDPF_GOLD_COMMIT` prior value included) and the deployed package's BUILD_MANIFEST `source_vintage.commit`. Record the EventBridge
      Scheduler schedule `mdpf-scheduled-floor`'s target input verbatim (`scheduler get-schedule`). Read, for the latest date present, every scope's
      four served artifact objects under `s3://opal-data-assets/portal/gold/mdpf/<scope>/` (4 scopes x 4 types = 16): keep ETag, VersionId and a body
      hash each (the baseline of leg d). Print the key of `taxsma_operational_control_key()` (from the pinned code, never typed) and every state-write
      key class of the pair's section 4 that is an OVERWRITE, each with its prior VersionId; for the tax prelude stores print the VersionId of each
      store's object for today's knowledge date. Record the emitter lambda's `CodeSha256` and `LastModified` (the leg-e control).
   b. **D1.** The four scripts, NAMED FILES ONLY, through `bash .tools/safe-deploy.sh <the four files>`. Never "every differing file". Read back with
      `python .tools/mdpf-code-equality.py --files <the four>`; exit 0 and `named_not_equal 0`.
   c. **D2.** `build_package.py --pin <the pin>` (the package's own procedure; it refuses a moving ref), upload, edit the one `.tf` value to the FULL
      SHA the build resolved (`BUILD_MANIFEST.json` `source_vintage.commit`), commit that one file with `safe-commit.sh`, then ONE targeted `safe-apply`
      on `mdpf-gold-lambda`. The targeted plan must show the function's code change and the single environment value `MDPF_GOLD_COMMIT` and
      nothing else; any other attribute moving: STOP, report, do not apply. Read the deployed package's manifest back: the sha256 of the four files
      equal the pin's; read the function's environment back: `MDPF_GOLD_COMMIT` equals the full pin SHA, which equals the package manifest's
      `source_vintage.commit`.
   d. **The one dry run (D4).** Invoke the gold lambda ONCE. Read the schedule's input recorded in (a); the event is that input with exactly ONE key
      added, `"qa_local": true` (the handler's documented dry-run key, `mdpf_gold_consolidator.py` `lambda_handler`), and nothing else; do not set
      `qa_return_bodies`, do not type any other key; use `--cli-read-timeout 0`. Read the response. Then read the same 16 objects as in (a), each
      store VersionId of the tax prelude, the control key's VersionId and the emitter's `CodeSha256`.
      The leg is met when: invoke 200 with no FunctionError; payload `status` green, `errors` empty, `a4_objects_built` 16; every one of the 16
      baseline objects is byte-equal to its baseline (the dry run changed nothing served); the control key and every tax-prelude store's EXISTING object read the SAME
      VersionId as in (a); a changed VersionId is a finding: STOP, report, file a BLOCKING row naming the key. (AMENDMENT 1, 2026-10-13: a NEW
      workbook snapshot object under `gateway/global/{bronze,silver}/taxsma_workbook/date=<d>/` is EXPECTED from any acquisition, because the key
      carries the response sha256 and every run acquires afresh; the day's fire and CN-d-1's on-demand run each wrote one. List them, with
      VersionIds, and do not treat their appearance as a delta; the first draft's "a conditional create is a no-op" was the issuer's wrong premise,
      row D1-S20.); the emitter's `CodeSha256` is unchanged. If the response `errors` lists `global`: the fold refused Global on
      today's real inputs (the ADDENDUM 6 branch): do NOT retry or loosen; file a BLOCKING row with the dates and the firm count the run names, and
      report. If it raises `GLOBAL SERVED IDENTITY REFUSED` or `GLOBAL MIN-FIRMS FOLD REFUSED`: the same.
      The first-fold acceptance (the global objects of a NEW as-of date carry no model line held by fewer than two firms; identity differential;
      `run.code.commit` equals the pin) is read by the ISSUER on the first scheduled fire after D2 that mints a new date (2026-10-14 13:30Z at the
      earliest); it is not a leg of this order and no seat waits on it here.
   e. **The emitter is NOT an act.** Do not build, upload or apply `opal-assets-daily-emitter`. Its crosswalk twin lands as repo parity (committed !=
      deployed). Read the emitter's `CodeSha256` and `LastModified` after the last act: unchanged (control). The reason, measured: it uses the crosswalk
      for the rmid bridge, the eclipse-id map and `CORE_MODEL_KEYS` only, reads the staged `_aggregate_aua` partition and never a served Global object,
      and the registry whose import check needs the row is not in its package (pair section 2).
   f. **After print.** `python .tools/mdpf-code-equality.py` whole again; attach it. The four D1 names read EQUAL. Report every name whose status
      changed since the before print other than those four; deploy NOTHING from that list (a differing runner member takes its own pair and the
      separate `code/` sync window).
4. **Rollback** if (c) shows an unexpected plan, or (d) shows any delta beyond what it names: re-copy the four keys from the recorded VersionIds,
   rebuild at the prior pin `0d39789fdf`, restore `MDPF_GOLD_COMMIT` to the value printed in (a) (and the `.tf` text), apply the same target, and report.
   A write-once key (a dated A4 object, a gold parquet partition, a manifest, the `_aggregate_aua` partition) has no prior version and is not rolled
   back: a bad first folded object is answered by the issuer's next-fire read and the pair's branches, never by a delete (a delete needs a human's
   word). Nothing else moved.
5. Close the ledger. Report to `2.0.0_SA_COO~D1` with each criterion's output, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
infra/aws/terraform/mdpf-pipeline/gold-lambda.tf
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round6/checks/r6_cn_f_1.py" contract | tail -1 &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round6/checks/r6_cn_f_1.py" seams | tail -1</invocation>
  <expect>ROUND 6 CONTRACT: 13 of 13 arms and ROUND 6 SEAMS: 6 of 6 arms (the source deployed is the source graded)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>python .tools/mdpf-code-equality.py --files data/mdpf/scripts/gold/mdpf_gold_consolidator.py data/mdpf/scripts/gold/dim_mdpf_account_distribution.py data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py</invocation>
  <expect>exit 0 and `named 4 | named_not_equal 0`; each key's prior ETag and VersionId recorded in the ledger before the copy</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the targeted plan on mdpf-gold-lambda, then safe-apply -target, then the deployed package manifest and the function environment read back</invocation>
  <expect>the plan moves only the function's code and the environment value MDPF_GOLD_COMMIT; the four files' sha256 in the deployed package equal the pin's; the function's MDPF_GOLD_COMMIT equals the full pin SHA and the package manifest's source_vintage.commit</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>the one invocation of mdpf-gold-lambda with the schedule's recorded input plus the single key qa_local true, then the before and after reads of the 16 latest-date served objects, each tax-prelude store and the control key by VersionId, and the emitter's CodeSha256</invocation>
  <expect>invoke 200 with no FunctionError, status green, errors empty, a4_objects_built 16; all 16 baseline objects byte-equal (objects compared, printed); the control key and every store's existing object read the same VersionId (new workbook snapshot objects listed, AMENDMENT 1); the emitter CodeSha256 unchanged</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>the whole-tree print before and after, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger; the four D1 names read EQUAL and every other changed name listed with nothing deployed from it; this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
