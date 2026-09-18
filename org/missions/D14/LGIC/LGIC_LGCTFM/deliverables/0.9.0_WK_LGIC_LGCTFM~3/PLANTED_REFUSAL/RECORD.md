# PLANTED_REFUSAL -- LT-x-2 (LGIC_LGCTFM.TO-LT-x-2-r1), 0.9.0_WK_LGIC_LGCTFM~3

## What was run

A practice worktree was created off this branch's HEAD (`ea26e21bc1`), never pushed, and deleted
before this report: `git worktree add <scratch>/wk3-practice -b wk3-practice-plant HEAD`, with
`org/mcp/naming-gate.enforce` created IN THAT WORKTREE ONLY (touch, empty file).

Target file: `data/black_diamond/scripts/gold/gold_freshness_config.yaml` (a declaration-tree `.yaml`
the gate grades; not under `org/`, `docs/`, `infra/logic/registry/`, `*/tests/*`, or a run-artifact
directory; carries no GENERATED mark). Pre-image at both the practice worktree's HEAD and this
worktree's HEAD is identical: blob `4f72d6e533` (`git rev-parse HEAD:data/black_diamond/scripts/gold/gold_freshness_config.yaml`
prints `4f72d6e53333ed50a0d9369f0eac07afe8e30270` in this worktree).

The marked location used is the ADVI_FIRMBKTS surface `{"kind": "s3-prefix", "bucket": "opal-data-bd",
"prefix": "gold/"}` (`infra/logic/registry/remediations.json` remediations[0].surfaces[4]), exercised
through the file's existing hand-kept literal `s3://opal-data-bd/gold/dimensions/accounts_dimension_latest.parquet`
(line 181, artifact_id `bd_gold_accounts_dimension`, the A_00 gate artifact every downstream BD gold
script depends on).

### ADD (add.diff)

Staged a new list entry, `bd_gold_accounts_dimension_e12_strict` (a second, tighter freshness watch on
the same A_00 gate artifact for an `E_12` reconciliation diagnostic that would fail hard on staleness
the main chain only warns on -- the same shape of entry as every other artifact_id already in this
file, naming the identical existing `s3_key_prefix` string as line 181's). Because that literal string
is byte-identical to the one already present in the file's pre-image, `naming-gate.py`'s `judge()`
grades it EXISTING (not NEW), so `remediation_of()` fires and names the live remediation.

```
$ python .tools/naming-gate.py --diff add.diff --enforce
DENOMINATOR: 1 path(s) in this diff; declaration-tree domain = 1 MINUS EXCLUDED(org/, docs/, run-artifact dirs ...) 0 = 1 path(s) [of the excluded, 0 are run artifacts and 0 are org//docs/]
COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set and not .gitattributes); 1 seen
NAMING REFUSE data/black_diamond/scripts/gold/gold_freshness_config.yaml:442 bd_gold_accounts_dimension_e12_strict -> lookup('49financial')
  why: NEW hand-kept carrier (context rule); hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial')
NAMING REFUSE data/black_diamond/scripts/gold/gold_freshness_config.yaml:443 s3://opal-data-bd/gold/dimensions/accounts_dimension_latest.parquet -> {source}/49financial/gold/dimensions/accounts_dimension_latest.parquet
  why: EXISTING and OUT-OF-PATTERN as S3Key in a surface remediations.json assigns to the live remediation ADVI_FIRMBKTS: REFUSE unless the diff removes it; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial')
NAMING-GATE: REFUSE 2 graded
```
rc=1. The refusal names `ADVI_FIRMBKTS` (second REFUSE line). Run twice, byte-identically: once in
the (now-deleted) practice worktree, once in this worktree against the same diff file -- both refuse
and both name ADVI_FIRMBKTS.

### REMOVE (remove.diff)

Staged the deletion of the ENTIRE pre-existing `bd_gold_accounts_dimension` entry (lines 180-188 of the
pre-image, including its blank trailing line) -- an existing hand-kept use of the same ADVI_FIRMBKTS
surface, removed outright.

```
$ python .tools/naming-gate.py --diff remove.diff --enforce
DENOMINATOR: 1 path(s) in this diff; declaration-tree domain = 1 MINUS EXCLUDED(org/, docs/, run-artifact dirs ...) 0 = 1 path(s) [of the excluded, 0 are run artifacts and 0 are org//docs/]
COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set and not .gitattributes); 1 seen
NAMING-GATE: PASS 0 graded
```
rc=0. A diff that only removes lines grades nothing (`grade_file` only extracts literals from ADDED
lines), so there is nothing to refuse -- confirmed both in the practice worktree and again in this
worktree against the same diff file.

### Estate flag

`org/mcp/naming-gate.enforce` was created only inside the deleted practice worktree, never in this
worktree or committed on this branch. `git log --oneline <base>..HEAD -- org/mcp/naming-gate.enforce`
and `git status --porcelain -- org/mcp/naming-gate.enforce` in this worktree are both empty (read by
X2R1-AC3 / `x2_flag_untouched`).

## Neither change was committed

`git status --porcelain -- data/black_diamond/scripts/gold/gold_freshness_config.yaml` in this
worktree is empty: the file was never edited here, only in the deleted practice worktree. The practice
worktree and its branch `wk3-practice-plant` were removed (`git worktree remove --force` +
`git branch -D`) before this report.
