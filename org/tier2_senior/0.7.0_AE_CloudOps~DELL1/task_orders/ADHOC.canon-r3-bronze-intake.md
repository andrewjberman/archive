# pipeline-override: MDPF_CANON round 3 (decomposition v3, cells CN-c-2 and CN-c-3, drained @86755fa58b and @d437b0648f); the round-3 issuance @335258e392 is closed to new order files (ONE ISSUER PER ROUND), so the apply, the three file deploys, the history copy and the one real run ride one CloudOps ADHOC order, on the MDPF_CANON round-2 precedent (ADHOC.canon-r2-publisher-layer-and-builder-grant).
<task_order id="ADHOC.canon-r3-bronze-intake">
<to_id>ADHOC.canon-r3-bronze-intake</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-11</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 3 of MDPF_CANON; the next scheduled runner start is the deadline -- see ORDER OF ACTS)</priority>

<title>MDPF_CANON CN-c-2 + CN-c-3: the Orion model-composition bronze moves to the builder's address -- runner grant, three file deploys, the history copied, one on-demand pull and one local feeder read</title>

<context>
PRD DEC-8 (FWD-7). The Stage-0 pull `pull_orion_model_composition.py` and its only reader, the Inflection feeder, are repointed from
`s3://opal-data-mdpf/mdpf/bronze/orion_model_composition/{date}/` to the builder's address:

```
s3://opal-data-assets/mdpf/inflection/bronze/orion_model_composition/date={date}/model_{orion_id}.json
s3://opal-data-assets/mdpf/inflection/bronze/orion_model_composition/date={date}/_meta/pull_complete.json
```

Both scripts read the generated file `data/mdpf/config/bronze_homes.json` (from `lib/opal_naming.py`, registry row
`infra/logic/registry/feeds.json`); the runner has no `lib/`. **A missing config file makes both scripts RAISE: the feeder reading the
new home with no partition on-or-before its date fails the chain.** So the order of acts below is the whole safety, and the old
bronze is NOT deleted (DEC-8: an S3 delete needs a human's confirmation; not this order).

Source at `box/dell1` HEAD (`d437b0648f` or later):
- `infra/aws/terraform/mdpf-pipeline/iam.tf` -- two statements added in `aws_iam_role_policy.mdpf_runner` (PutObject/GetObject on
  the bronze prefix and ListBucket with an `s3:prefix` condition), bucket and prefix from `module.<m>.bronze_homes[...]`;
- `infra/aws/terraform/modules/opal_name/generated_locals.tf` and `main.tf` -- the `bronze_homes` local and module output (generator
  bytes). Row `MDPF_CANON-D1-W9-S6`: regenerating also added four `"4698"` lines (the inflection masters) that HEAD did not carry;
  they predate this order and were kept as the generator wrote them;
- `data/mdpf/config/bronze_homes.json`, `data/mdpf/scripts/bronze/pull_orion_model_composition.py`,
  `data/mdpf/scripts/gold/build_mdpf_wsc_inflection_feeder.py`.
Row `MDPF_CANON-D1-W9-S7` (ARMED, your leg disarms it): nothing in the repo copies these three files to the runner's `code/` prefix;
the copy is a hand step, and it is this order's.
</context>

<scope>
1. Edit no source file. Open a deploy ledger (NEVER-2) BEFORE the first act; name in it the runner and every consumer that reads the
   three files you deploy. `code/` is ~20 commits behind HEAD (iam.tf comment): do NOT tree-sync, deploy EXACTLY the three files.
2. **ORDER OF ACTS (the order is the safety):**
   a. READ the daily runner's next scheduled start (its EventBridge rule or the runner's own scheduler). If it is within 2 hours of
      now, do acts (b)-(e) only up to the history copy, do NOT deploy the scripts, and report.
   b. **The grant.** Targeted plan in `infra/aws/terraform/mdpf-pipeline` on `aws_iam_role_policy.mdpf_runner`: expect 0 to add / 1 to
      change / 0 to destroy, the change being exactly the two added statements and nothing else in the rendered JSON. Any other
      change: STOP, report, do not apply. Then `safe-apply -target`. Read the live policy back.
   c. **The history.** Copy (never move, never delete) every object under the old prefix
      `opal-data-mdpf/mdpf/bronze/orion_model_composition/` to the new key
      `opal-data-assets/mdpf/inflection/bronze/orion_model_composition/date=<D>/<rest>`, where `<D>` is the old key's date segment and
      `<rest>` is the remainder. Compose the destination from `data/mdpf/config/bronze_homes.json` (`bucket`, `key_prefix`,
      `partition`), never typed. Print the denominators: objects at the source, objects copied, objects now under the new prefix; the
      two counts for the source prefix must match the new prefix's count (the new prefix holds only these).
   d. **The three files**, in this order: `bronze_homes.json` to `s3://opal-data-mdpf/code/config/`, then the writer to
      `code/scripts/bronze/`, then the feeder to `code/scripts/gold/`. Record the object's prior ETag/version for each BEFORE the put
      (rollback). Read each back and compare to the repo bytes.
   e. **The one real pull.** On the runner, run Stage 0 once, ad hoc, for the current date:
      `python /opt/mdpf/scripts/bronze/pull_orion_model_composition.py --date <D> --upload` (the runner's own Python and role).
      Read where it landed: list the new prefix's `date=<D>/` and print the object count (the nine `model_<id>.json` and
      `_meta/pull_complete.json`). If the pull fails on AccessDenied, the grant (b) did not take: report, do not widen it.
   f. **The feeder's local read.** Run the feeder once with `--bronze-source s3` and NO `--upload` (local `--out-dir` only), for the
      latest date whose feeder parquet exists in `s3://opal-data-mdpf/mdpf/feeds/`; compare the produced rows' data-bearing values with
      the live feed parquet for the same date. Expect value-equality (DELTA=0). The feeder writes nothing to S3 in this leg.
3. **Rollback** if (e) or (f) shows a failure or a delta: put the three prior objects back from the recorded ETags/versions in the
   same session (the old bronze is untouched, the old scripts read it), apply the prior policy, and report. The history copy stays.
4. Close the ledger. Report to `2.0.0_SA_COO~D1` with each criterion's output, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5,C6</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; for s in writer reader homes libs; do python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round3/checks/r3_checks.py" $s | tail -1; done</invocation>
  <expect>ROUND 3 WRITER: 3 of 3 arms, ROUND 3 READER: 3 of 3 arms, ROUND 3 HOMES: 3 of 3 arms and ROUND 3 LIBS: 5 of 5 arms (the source deployed is the source graded)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the targeted plan on aws_iam_role_policy.mdpf_runner in infra/aws/terraform/mdpf-pipeline, then safe-apply -target, then the live policy read back</invocation>
  <expect>plan 0 to add, 1 to change, 0 to destroy, the diff being exactly the two added bronze statements; the live policy then carries them</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the copy of opal-data-mdpf/mdpf/bronze/orion_model_composition/ to the builder's keys, with the three counts printed</invocation>
  <expect>objects at the source equals objects under the new prefix (denominator printed); nothing deleted at the source</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>the three puts and their read-backs: s3://opal-data-mdpf/code/config/bronze_homes.json, code/scripts/bronze/pull_orion_model_composition.py, code/scripts/gold/build_mdpf_wsc_inflection_feeder.py</invocation>
  <expect>each object's bytes equal the repo file at the deployed commit; each prior ETag/version recorded</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>the one on-demand run of pull_orion_model_composition.py --date &lt;D&gt; --upload on the runner, then the listing of the new prefix's date=&lt;D&gt;/</invocation>
  <expect>exit 0; the listing holds the nine model_&lt;id&gt;.json and _meta/pull_complete.json at the builder's keys (count printed)</expect>
</criterion>
<criterion id="C6" judgment="false">
  <invocation>the feeder run with --bronze-source s3 and no --upload, compared with the live s3://opal-data-mdpf/mdpf/feeds/ parquet for the same date; then python .tools/deploy_ledger.py check</invocation>
  <expect>DELTA=0 on the data-bearing values (rows compared, printed); this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
