# pipeline-override: MDPF_CANON round 4 (decomposition v4, cells CN-d-1 and CN-d-5, drained @0d39789fdf and @0468b6c8ba); the round-4 issuance @73fdbf8d0a is closed to new order files (ONE ISSUER PER ROUND), so the deploy of CN-d-1's three scripts, the lambda package and the one real run ride one CloudOps ADHOC order, on the MDPF_CANON round-2 and round-3 precedents (ADHOC.canon-r2-publisher-layer-and-builder-grant, ADHOC.canon-r3-bronze-intake).
<task_order id="ADHOC.canon-r4-code-deploy">
<to_id>ADHOC.canon-r4-code-deploy</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-11</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 4 of MDPF_CANON; BEHIND MDPF_STRATID.TO-APPLY-R2 -- see PRECONDITIONS)</priority>

<title>MDPF_CANON CN-d-1: the global account-distribution names the cottonwood leg's vintage and the served global total is asserted after the folds -- three named scripts to code/, the gold lambda package, one on-demand run; and CN-d-5's equality step run</title>
<context>
Cell CN-d-1 (order `task-orders/MDPF_CANON.TO-CN-d-1.served-identity-and-cottonwood-vintage.md`, merged `0d39789fdf`) changes three scripts:
- `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`: `assert_global_served_identity` and `guard_global_served_identity(arts, isolated)`, called in
  `build_all` as `arts = guard_global_served_identity(arts, _isolated)`. A refusal sets global to None and records it under
  `manifest["errors"]["global"]`; the three firm scopes build as before.
- `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py`: `meta.cottonwood_fold` gains `value_date` and `age_trading_days`.
- `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`: docstrings only.
All three are in the gold lambda package closure (`infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py` :135-137), so the served
bytes change only after D2 below. The never-widen pair is signed on both halves: the COO half in
`org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round4/NEVER_WIDEN_PAIR_R4_CN_D_1.md` and the CTO half RE-SIGNED in
`org/missions/D8/MDPF/MDPF_CANON/ledger/NEVER_WIDEN_R4_CN_D_1_CTO_HALF.md` @8a01e43ab0. Read the pair first: sections 2, 4 and 5 are this order's
acts, blast radius and both branches.

Cell CN-d-5 (merged `0468b6c8ba`) landed the read-only tool `.tools/mdpf-code-equality.py` and the written step
`docs/deployment/MDPF_RUNNER_CODE_SYNC.md`. Measured 2026-10-11 ~06:3xZ, whole tree: 5 trees, 77 files, 48 equal, 29 not equal
(scripts gold 33 of 48 local equal, backfill 7 of 11, feeders 4 of 5, bronze 2 of 2; config 2 of 4). Most non-equal names are not runner members.
</context>

<scope>
1. Edit no source file. Open a deploy ledger (NEVER-2) BEFORE the first act; name in it the three keys, the lambda `mdpf-gold-lambda`, and every
   consumer that reads the global account-distribution object.
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. `MDPF_STRATID.TO-APPLY-R2` reads `complete` and its ledger `mdpf-stratid-r2-global-fold` reads CLOSED (it names `mdpf_gold_consolidator.py`
      too; two acts never copy one key in one window). While it is open, this order WAITS: do not start D1.
   b. The pin `0d39789fdf` (or a later commit that carries the three files unchanged) is an ancestor of origin's `box/dell1`
      (`git ls-remote` then `git merge-base --is-ancestor`). Measured at issue: yes.
   c. Both halves of the pair are signed, read from the two files above.
   d. The clock: no act of D1 or D2 starts within 45 minutes before the 13:30Z gold fire or while the runner dispatch or the gold lambda is
      running (read the runner's status and the lambda's last invocation first).
3. **ORDER OF ACTS (the order is the safety):**
   a. **Before print.** `python .tools/mdpf-code-equality.py` whole; attach it to the ledger. Record, for each of the three keys under
      `s3://opal-data-mdpf/code/scripts/gold/`, the prior ETag and VersionId (rollback). Read, for the latest date present, the global
      account-distribution object and every firm scope's four artifact objects under `s3://opal-data-assets/portal/gold/mdpf/<scope>/`: keep
      their ETags and a body hash each (the baseline of leg d).
   b. **D1.** The three scripts, NAMED FILES ONLY, through `bash .tools/safe-deploy.sh <the three files>`. Never "every differing file".
      Read back with `python .tools/mdpf-code-equality.py --files <the three>`; exit 0 and `named_not_equal 0`.
   c. **D2.** `build_package.py --pin 0d39789fdf` (the package's own procedure), upload, then a targeted `safe-apply` on `mdpf-gold-lambda`. The
      targeted plan must show only the function's code change; any other attribute moving: STOP, report, do not apply. Read the deployed
      package's manifest back: the sha256 of the three files must equal the pin's.
   d. **The one real run.** Invoke the gold lambda ONCE, in the exact event shape its EventBridge schedule sends (read the schedule's input;
      do not type one). Read the run's manifest. Then read the same objects as in (a): the global account-distribution object differs from
      the baseline by exactly `meta.cottonwood_fold.value_date` and `meta.cottonwood_fold.age_trading_days` (parse both, ignore `generated_at`
      and provenance write stamps); every other object of every scope and type for that date is value-equal (DELTA=0, objects compared
      printed). If the run raises `GLOBAL SERVED IDENTITY REFUSED`: do NOT retry or loosen; the run's manifest carries it under
      `errors.global`, the firm scopes wrote as before, and you file a BLOCKING row with the dates the message names and report.
   e. **The classification (CN-d-5's step; read only).** From the after-print, classify EVERY non-EQUAL name as RUNNER MEMBER (the dispatch
      chain executes or reads it, from `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh` and the imports of what it runs) or NOT A
      MEMBER (a test, a QA tool, a file a bundle ships, a non-code data file), each with its reason in one line. Deploy NOTHING from this
      table in this order: a differing runner member is a deploy of its own, possibly moving served output, and takes its own pair. Report the
      table; the issuer carries it to the CTO.
   f. **After print.** `python .tools/mdpf-code-equality.py` whole again; attach it. The three D1 names read EQUAL.
4. **Rollback** if (c) shows an unexpected plan, or (d) shows any delta beyond the two keys: re-copy the three keys from the recorded VersionIds,
   rebuild at the prior pin and apply the same target, and report. Nothing else moved.
5. Close the ledger. Report to `2.0.0_SA_COO~D1` with each criterion's output, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round4/checks/r4_cn_d_1.py" | tail -1 &amp;&amp; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round4/checks/r4_cn_d_1_vintage.py" | tail -1</invocation>
  <expect>ROUND 4 IDENTITY: 6 of 6 arms and ROUND 4 VINTAGE: 3 of 3 arms (the source deployed is the source graded)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>python .tools/mdpf-code-equality.py --files data/mdpf/scripts/gold/mdpf_gold_consolidator.py data/mdpf/scripts/gold/dim_mdpf_account_distribution.py data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py</invocation>
  <expect>exit 0 and `named 3 | named_not_equal 0`; each key's prior ETag and VersionId recorded in the ledger before the copy</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the targeted plan on mdpf-gold-lambda, then safe-apply -target, then the deployed package manifest read back</invocation>
  <expect>the plan moves only the function's code; the three files' sha256 in the deployed package equal the pin's</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>the one invocation of mdpf-gold-lambda in its schedule's own event shape, then the before and after reads of the latest date's global account-distribution and every firm scope's four artifact objects</invocation>
  <expect>the global account-distribution gains exactly meta.cottonwood_fold.value_date and .age_trading_days; every other object value-equal (objects compared, printed); the run's manifest errors empty</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>the whole-tree print before and after, the classification table, then python .tools/deploy_ledger.py check</invocation>
  <expect>both prints attached to the ledger; every non-EQUAL name classified with its reason and nothing deployed from the table; this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
