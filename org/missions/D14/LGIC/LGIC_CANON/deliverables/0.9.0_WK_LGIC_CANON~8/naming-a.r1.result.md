# LGIC_CANON.TO-CN-n-1 -- naming worker A, round 1 result

**Worker:** 0.9.0_WK_LGIC_CANON~8 | **Branch:** wk-lgic-canon-1-8 | **Base:** f95470f38400da6d2a40eeaa7469651e32ddb95e
**Answer file:** `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/naming-a.tsv` @69f406a696

## Answers (6 of 6 items in CN_NAMING_JOB.json)

Every item takes the firm's spelling from `infra/logic/registry/scopes.json` row `49financial`: long `49financial`, short `49f`, bucket `opal-data-49financial`. Each value below is the output of the builder named beside it, run in this worktree at the base.

| id | answer | source |
|---|---|---|
| n1 | `opal-data-49financial` | scopes.json row 49financial `bucket` (= NAMING_SCHEMA bucket.data_bucket `opal-data-{scope}`, LONG form) |
| n2 | `mdpf/49financial/gold/category_views/date=2026-09-15` | `key('mdpf','49financial','gold','category_views','date=2026-09-15')` |
| n3 | `s3://opal-data-49financial/advi/49financial/platinum/advisors/advisor_id=A123` | `address('advi','49financial','platinum','advisors','advisor_id=A123')` (the FIRM-tenancy platinum home is the scope's bucket, tiers.json) |
| n4 | `advi-49f-dashboard-publish-lambda` | `name('advi','49financial','dashboard-publish','lambda')` |
| n5 | `irpt-49f-export-dlq` | `name('irpt','49financial','export','dlq')` |
| n6 | `blackdiamond-49f-session-runner-role` | `name('blackdiamond','49financial','session-runner','role')` |

The systems are `mdpf` (Model Portfolios), `advi` (Advisor Intelligence), `irpt` (Investor Reporting) and `blackdiamond` (the Black Diamond vendor integration), all from systems.json.

## Criteria

- **N1-AC1** PASS by output: `ITEMS: 6  NAMED FROM A CITED REGISTRY ROW: 6` / `VERDICT: PASS-NA-NAMES-CITED`, rc=0.
- **N1-AC2** PASS by output: `BASE: f95470f38400da6d2a40eeaa7469651e32ddb95e  resolves to a commit: True` / `VERDICT: PASS-NA-BASE-STATED`, rc=0.

## Controls

- **Mutant:** a scratch copy in which n1 cites `scopes.json#49finance` gives `ITEMS: 6  NAMED FROM A CITED REGISTRY ROW: 5` / `VERDICT: FAIL-NA-NAMES-UNCITED`. FIRED-AS-EXPECTED.
- **Determinism:** each criterion was run twice, and each pair of outputs is byte-identical (cmp). STABLE.

## Surprise

- **LGIC_CANON-W8-S1** (OBSERVATION, ARMED, disarm owner 1.0.0_SA_CTO), @69f406a696: `grade()` calls address()'s own n3 key OUT-OF-PATTERN and gives `advisor-id=a123` as canonical. The cause is `lib/opal_naming.py:1102-1111` `_new_served` @f95470f384: when a key has no object leaf, it reads a trailing entity partition as the file leaf. The same key graded CONFORMANT once a trailing `/` or `/profile.json` was added. The answer carries the builder's output, as the order directs.

## Blindness

This worker did not open CN_NAMING_KEY.json, CN_JUDGE_NAMING_KEY.json, naming-b.tsv or naming-compare.md. In check_canon_r1.py it read only the n1 functions and the file-path constants.
