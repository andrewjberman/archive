# pipeline-override: MDPF_CANON round 7 (decomposition v7, cells CN-h-1 drained @9592daf75c and CN-l-1 drained @72ef4f8a3a); the round-7 issuance @879feb7e99 is closed to new order files (ONE ISSUER PER ROUND), so the deploy of the one named gold script, the lambda package with the registry row it now ships and its environment stamp, and the one dry-run invoke ride one CloudOps ADHOC order, on the MDPF_CANON round-2, round-3, round-4 and round-6 precedents (ADHOC.canon-r2-publisher-layer-and-builder-grant, ADHOC.canon-r3-bronze-intake, ADHOC.canon-r4-code-deploy, ADHOC.canon-r6-fold-deploy).
<task_order id="ADHOC.canon-r7-gold-deploy">
<to_id>ADHOC.canon-r7-gold-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-14</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 7 of MDPF_CANON; BEHIND the signed pair and the issuer's written GO -- see PRECONDITIONS)</priority>

<title>MDPF_CANON CN-h-1 and CN-l-1: the frontier account counts read the newest A4 account-distribution, and the Other Models row carries its date or is blank -- one named script to code/, the gold lambda package with its commit stamp, one dry-run invoke; the aggregate library is NOT copied to code/ and the emitter package is NOT touched</title>
<context>
Two cells change the gold lambda's behaviour and ONE order deploys both, so the first scheduled fire after it carries both and is attributable to this order alone.
- Cell CN-h-1 (order `task-orders/MDPF_CANON.TO-CN-h-1.frontier-counts-read-the-a4-distribution.md`, merged `9592daf75c`): `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`
  now takes each firm's frontier per-model `account_count` from the newest A4 object `portal/gold/mdpf/<firm>/account-distribution/<date>.json` at or before the axis date (no fallback to
  the staged runner object), with the prefix built by `lib.opal_naming.legacy_address("mdpf-portal-gold-account-distribution", firm=<firm>)` (the registry row, commit `81453d51cf`); and
  `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py` gains ONE package-list entry, `infra/logic/registry/legacy_addresses.json`, because `legacy_address` raises
  `RegistryError` when that file is absent from the package.
- Cell CN-l-1 (order `task-orders/MDPF_CANON.TO-CN-l-1.other-models-dated-carry.md`, merged `72ef4f8a3a`): `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py` serves the Global `Other Models`
  row with its pooled value only within 4 calendar days of the as-of and stamps `as_of`, else blank. No new import.
The never-widen pair is written on both halves: the COO half in
`org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/NEVER_WIDEN_PAIR_R7_GOLD_H1_L1.md` and the CTO half in
`org/missions/D8/MDPF/MDPF_CANON/ledger/NEVER_WIDEN_R7_GOLD_H1_L1_CTO_HALF.md`. Read the pair first: sections 2, 4 and 5 are this order's acts, blast radius and every branch.

What this order carries beyond the round-6 shape (read these five lessons):
1. `ADHOC.canon-r4-code-deploy` AMENDMENT 3: the A4 writer is write-once per dated key, so no on-demand run lands a change on a date a scheduled fire already wrote. The served-key
   acceptance of THIS order is read by the issuer on the first scheduled fire that mints a new date (2026-10-15 13:30Z at the earliest), and is not a leg of this order.
2. The environment stamp (row D1-S18): `MDPF_GOLD_COMMIT` must equal the pin actually built; the function holds `51cfc93ea84ac56ee6d14327125bfc53fc53c930` today (the round-6 pin).
3. The CTO's C-S65 and its CORRECTION (`ADHOC.canon-r6-fold-deploy` AMENDMENT 1, row D1-S20): the workbook snapshot store's KEY carries the response sha256, so every acquisition CREATES a
   new bronze and silver object. D4 below will create two. They are expected, listed, and never a delta.
4. NEW: the dry run D4 is the ONLY runtime proof, before a scheduled fire, that the deployed package carries the registry row the loader now needs. The offline simulation
   (pair section 1) shows the package list as built resolves `legacy_address`; the Lambda runtime has not run it. A `RegistryError`, `ImportError`, `KeyError` or `ValueError` in D4's
   response is the failure class this order exists to catch before the fire.
5. NEW: the aggregate library is deliberately NOT copied to `code/scripts/gold/`. The runner imports it, and the runner's code tree carries no `lib/` package, so the module-scope
   `from lib.opal_naming import legacy_address` would fail at the runner's next import. `mdpf-code-equality.py` will keep printing DIFFER for that one name; that is stated here and is
   not repaired by a copy.
</context>

<scope>
1. Edit no source file EXCEPT `infra/aws/terraform/mdpf-pipeline/gold-lambda.tf`: the value of `MDPF_GOLD_COMMIT` in the function's environment block (line 337 at drafting) and the comment
   paragraph above it (the file's own rule: SET THIS FROM THE --pin YOU ACTUALLY BUILT WITH, with the zip's sha256 and the previous value as the rollback). No other line of that file moves.
   Open a deploy ledger (NEVER-2) BEFORE the first act; name in it the one key, the lambda `mdpf-gold-lambda`, the `.tf` value, and every consumer that reads a global served object.
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's written GO IS THIS ORDER'S ISSUANCE COMMIT: today's (2026-10-14 13:30Z) fold fire is read and closed (round-6 analysis `ledger/ROUND_ANALYSIS.round6.md`: FWD-3 REALIZED), both
      halves of the pair are signed (CTO half `8d6f9cdba3`), and the pin is `9592daf75c` (or the later commit named in b). A GO naming a different pin comes as a broker message from `2.0.0_SA_COO~D1`.
   b. The pin `9592daf75c`, or a later commit that carries `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`, `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`,
      `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py`, `infra/logic/registry/legacy_addresses.json` and `lib/opal_naming.py` unchanged (read by content:
      `git show <pin>:<path>` against the merged blobs), is an ancestor of origin's `box/dell1` (`git ls-remote` then `git merge-base --is-ancestor`). Read from the pin, both must hold:
      `legacy_addresses.json` carries the key `mdpf-portal-gold-account-distribution`, and `build_package.py` lists `infra/logic/registry/legacy_addresses.json`.
   c. Both halves of the pair are SIGNED, read from the two files named in the context (a signature is a line in a commit by that seat).
   d. The clock: no act of D1 or D2 starts within 45 minutes before the 13:30Z gold fire or while the runner dispatch or the gold lambda is running (read the runner's status and the
      lambda's last invocation first). D2 and D4 both finish by 12:44Z on 2026-10-15; if the order cannot, it WAITS until the 2026-10-15 fire has written its manifest and the issuer has
      read it, then starts. D4 starts only after D2.
   e. No FIRMBKTS window act is in flight: read its ledgers first (`org/critical_paths/.open_deploys/advi-firmbkts-*`) and start only in a gap between its acts. This order touches NONE of
      the R2 surfaces (`shared-advisor-router`, the guard, the CloudFront behaviours, `data/mdpf/config/bronze_homes.json`, `firm-config.mjs`, the portal-auth WAF rider).
   f. One change per scheduled fire: no open deploy sentinel names `mdpf-gold-lambda` or `code/scripts/gold/` other than this order's own, and nothing else is planned for them before the
      2026-10-15 13:30Z fire (read `org/critical_paths/.open_deploys/`). **SEQUENCE WITH THE PUBLISHER ORDER:** `ADHOC.canon-r7-publisher-deploy` is a different function and is STAGED behind this
      order: two acts never share one window, so you do not open the publisher order's ledger until this order's ledger is CLOSED, and its start comes only on the issuer's GO message.
   g. **MEASURE, read-only, the runner's layout, and print it** (an `ls` of `/opt/mdpf` and `/opt/mdpf/scripts/gold` and a `test -d /opt/mdpf/lib`, through the account's usual read path). THIS IS A
      CONDITION OF THE CTO HALF (D1 is narrowed on the reading that the runner has no `lib/`): (i) the read path is unavailable, or the result is "not read": STOP before D1, report, do nothing; (ii)
      `/opt/mdpf/lib` EXISTS: the narrowing's premise is false: STOP before D1, report the listing, do nothing (the issuer re-reads the pair with the CTO half); (iii) it reads ABSENT: record the
      listing in the ledger and continue. D1 excludes the aggregate library in every case.
3. **ORDER OF ACTS (the order is the safety):**
   a. **Before print.** `python .tools/mdpf-code-equality.py` whole; attach it to the ledger. Record, for the one D1 key `code/scripts/gold/dim_mdpf_aum_metrics.py` under
      `s3://opal-data-mdpf/`, the prior ETag and VersionId (rollback); for information record the same for `code/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` (NOT overwritten).
      Record the function's `CodeSha256`, `LastModified` and its environment (`MDPF_GOLD_COMMIT` prior value included), the deployed package's BUILD_MANIFEST `source_vintage.commit`,
      and the package object `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` ETag and VersionId. Record the EventBridge Scheduler schedule
      `mdpf-scheduled-floor`'s target input verbatim (`scheduler get-schedule`). Read, for the latest date present, every scope's four served artifact objects under
      `s3://opal-data-assets/portal/gold/mdpf/<scope>/` (4 scopes x 4 types = 16): keep ETag, VersionId and a body hash each (the baseline of leg d). Print, for `global`, `49financial` and
      `inflection`, the newest A4 `account-distribution` key and its `period` (the loader's input; read-only). Print the key of `taxsma_operational_control_key()` (from the pinned code, never typed)
      and every state-write key class of the pair's section 4 that is an OVERWRITE, each with its prior VersionId; for the tax prelude stores print the VersionId of each store's EXISTING
      object for today's knowledge date, and LIST every object under `gateway/global/{bronze,silver}/taxsma_workbook/date=<today>/` with its VersionId (the baseline for new snapshot objects).
      Record the emitter lambda's `CodeSha256` and `LastModified` (the leg-e control).
   b. **D1.** The ONE script, NAMED FILE ONLY, through `bash .tools/safe-deploy.sh data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`. Never "every differing file". Do NOT copy
      `dim_mdpf_aggregate_aua_timeseries.py` (context lesson 5). Read back with `python .tools/mdpf-code-equality.py --files data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`; exit 0 and
      `named_not_equal 0`.
   c. **D2.** `build_package.py --pin <the pin>` (the package's own procedure; it refuses a moving ref). Before the upload read the built package: its BUILD_MANIFEST `source_vintage.commit`
      is the full pin SHA; the zip lists `infra/logic/registry/legacy_addresses.json` and its sha256 equals `git show <pin>:infra/logic/registry/legacy_addresses.json`; the members
      `dim_mdpf_aggregate_aua_timeseries.py` and `dim_mdpf_aum_metrics.py` have the pin's sha256. Upload, edit the one `.tf` value to the FULL SHA the build resolved, commit that one file with
      `safe-commit.sh`, then ONE targeted `safe-apply` on `mdpf-gold-lambda`. The targeted plan must show the function's code change and the single environment value `MDPF_GOLD_COMMIT` and
      nothing else; any other attribute moving: STOP, report, do not apply. Read the deployed package's manifest back and the function's environment back: `MDPF_GOLD_COMMIT` equals the full pin
      SHA, which equals the package manifest's `source_vintage.commit`; the function's `CodeSha256` differs from the one recorded in (a).
   d. **The one dry run (D4).** Invoke the gold lambda ONCE, after D2. Read the schedule's input recorded in (a); the event is that input with exactly ONE key added, `"qa_local": true`
      (the handler's documented dry-run key, `mdpf_gold_consolidator.py` `lambda_handler`), and nothing else; do not set `qa_return_bodies`, do not type any other key; use
      `--cli-read-timeout 0`. Read the response. Then read the same 16 objects as in (a), each store's existing-object VersionId, the control key's VersionId, the workbook snapshot
      listing and the emitter's `CodeSha256`.
      The leg is met when: invoke 200 with no FunctionError; payload `status` green, `errors` empty, `a4_objects_built` 16; every one of the 16 baseline objects is byte-equal to its baseline
      (the dry run changed nothing served); the control key and every tax-prelude store's EXISTING object read the SAME VersionId as in (a); a changed VersionId is a finding: STOP, report, file a
      BLOCKING row naming the key. The workbook snapshot listing may carry NEW bronze and silver objects (expected: one of each, because the key carries the response sha256 and every run acquires
      afresh); list them with VersionIds and do not treat their appearance as a delta. The emitter's `CodeSha256` is unchanged.
      **If the response `errors` names a scope with `RegistryError`, `ImportError`, `KeyError`, `ValueError` or `C2-SIBLING FAIL-LOUD`: this is the failure class this order exists to catch.
      STOP, do not retry, run the rollback in section 4 (restore the prior package and the prior environment value), file a BLOCKING row quoting the exception class and the scope, and report.**
      If it lists `global` with a min-firms or served-identity refusal (not expected: today's pool is held by two firms): do NOT retry or loosen; file a BLOCKING row with the dates and the firm count
      the run names, and report.
      The first-fire acceptance (the served objects of a NEW as-of date carry the A4 counts; the Other Models row serves unchanged; `run.code.commit` equals the pin) is read by the ISSUER on the
      first scheduled fire after D2 that mints a new date (2026-10-15 13:30Z at the earliest) with `round7/checks/r7_frontier_readback.py read` and `round7/checks/r7_cn_l_1.py real`; it is not a
      leg of this order and no seat waits on it here.
   e. **The emitter is NOT an act.** Do not build, upload or apply `opal-assets-daily-emitter`. Read the emitter's `CodeSha256` and `LastModified` after the last act: unchanged (control).
   f. **After print.** `python .tools/mdpf-code-equality.py` whole again; attach it. The one D1 name reads EQUAL. Report every name whose status changed since the before print other than that one;
      deploy NOTHING from that list. The aggregate library's DIFFER is a stated fact of this order (context lesson 5), not a change.
4. **Rollback** if (c) shows an unexpected plan, or (d) shows any delta beyond what it names or any exception class named in (d): re-copy the D1 key from the recorded VersionId, rebuild at
   the prior pin `51cfc93ea8`, restore `MDPF_GOLD_COMMIT` to the value printed in (a) (`51cfc93ea84ac56ee6d14327125bfc53fc53c930` at drafting; and the `.tf` text), apply the same target, and
   report. A write-once key (a dated A4 object, a gold parquet partition, a manifest, the `_aggregate_aua` partition) has no prior version and is not rolled back: a bad first object is answered
   by the issuer's next-fire read and the pair's branches, never by a delete (a delete needs a human's word). The new workbook snapshot objects are inert creates and are not rolled back.
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
  <invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r6_cn_h_1.py" seams | tail -1 &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round7/checks/r7_cn_l_1.py" unit | tail -1</invocation>
  <expect>CN-H-1 SEAMS: 6 of 6 arms and ROUND 7 CN-L-1 UNIT: 8 of 8 arms (the source deployed is the source graded)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>python .tools/mdpf-code-equality.py --files data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py</invocation>
  <expect>exit 0 and `named 1 | named_not_equal 0`; the key's prior ETag and VersionId recorded in the ledger before the copy</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the built package read before upload, then the targeted plan on mdpf-gold-lambda, then safe-apply -target, then the deployed package manifest and the function environment read back</invocation>
  <expect>the zip lists infra/logic/registry/legacy_addresses.json with the pin's sha256 and the two changed gold modules carry the pin's sha256; the plan moves only the function's code and the environment value MDPF_GOLD_COMMIT; the function's MDPF_GOLD_COMMIT equals the full pin SHA and the package manifest's source_vintage.commit</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>the one invocation of mdpf-gold-lambda with the schedule's recorded input plus the single key qa_local true, then the before and after reads of the 16 latest-date served objects, each tax-prelude store's existing object, the control key by VersionId, the workbook snapshot listing and the emitter's CodeSha256</invocation>
  <expect>invoke 200 with no FunctionError, status green, errors empty, a4_objects_built 16; all 16 baseline objects byte-equal (objects compared, printed); the control key and every store's existing object read the same VersionId (new workbook snapshot objects listed); the emitter CodeSha256 unchanged</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>the whole-tree print before and after, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger; the one D1 name reads EQUAL and every other changed name listed with nothing deployed from it, the aggregate library's DIFFER stated as known; this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
