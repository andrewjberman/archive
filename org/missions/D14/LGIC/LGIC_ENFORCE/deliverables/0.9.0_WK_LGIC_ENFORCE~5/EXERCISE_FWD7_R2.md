# EXERCISE_FWD7_R2 -- firm N+1 is one row, again after RULING ONE (LGIC_ENFORCE EN-d-1, round 2)

Worker `0.9.0_WK_LGIC_ENFORCE~5`, task order `LGIC_ENFORCE.TO-EN-d-1-r2.fwd7-demo-firm.md`. Round 1's
`EXERCISE_FWD7.md` stays as its own record; this file is round 2's and replaces nothing.

The work was done on a PRACTICE COPY
(`git worktree add -b prac-lgic-enforce-d1-r2 <WS>/../prac-lgic-enforce-d1-r2 HEAD`, cut at CLOUD @2a2b853f79)
on scratch branch `prac-lgic-enforce-d1-r2`. `git ls-remote --heads origin prac-lgic-enforce-d1-r2` printed
0 lines, so the branch has never been pushed; it is never merged. The practice worktree was removed clean at
the end and the branch left in place (deleting an unmerged branch is destructive git).

The firm is the FIXED fictitious one: long form `quillwater`, short form `qwt`. It is a `client`-kind tenant
held `enabled: false`, and it is never `demo`.

## The commit chain on the scratch branch

| commit | what |
|---|---|
| `529b5c39fb` | **expected_set**: `deliverables/0.9.0_WK_LGIC_ENFORCE~5/expected_diff.r2.txt`, written and committed BEFORE the row existed |
| `ed8771f9e8` | **generated**: one `scopes.json` row, then `python lib/opal_naming.py generate --out .`, committed unedited |

`git merge-base --is-ancestor 529b5c39fb ed8771f9e8` exits 0.

## 1. How the expected set was derived, before the row

By SUBTRACTION from the generator's own denominator, never from a forward list. `generate()`'s known targets
are `[v[0] for v in VIEWS] + [LOCALS_PATH, VECTORS_PATH, TFTEST_PATH]` (`lib/opal_naming.py:1649-1650`
@2a2b853f79) -- **10** files. Round 1 read 9: `opal_name.tftest.hcl` is generated now and was not then.

EN-r-6 replaced round 1's one global hash with a PER-VIEW hash: `generate()` stamps each target with
`_view_mark(h16, target)` where `h16 = registry_hash(only=_target_registry_files(t))[:16]`
(`:1657-1659`, `:117-120`), and `_target_registry_files` reads `TARGET_REGISTRY_KEYS` (`:97-109`), the table
that DECLARES, per target, exactly the registry files that target's renderer reads. So the question "which
generated files must move when one `scopes.json` row is added?" is answered by that table, not by inspecting
the rendered bytes:

    denominator                                  10 known targets
    minus the targets NOT declaring 'scopes'      0
    expected                                     10

All 10 declare `scopes.json`, so all 10 move -- their mark at minimum, their body where the row renders.
Three move ONLY in the mark: `loaders.py`, `perfrp_firm_pin.py` and `ds-precommit-check.py` wrote the same
byte counts as before (6934 / 7114 / 43360), since the row adds no pipeline tree, no advi tree and no row
that `bucket_for` carries. `infra/logic/registry/scopes.json` is the INPUT and is outside the set.

**Control run before the row.** In the practice copy at HEAD, `generate --out .` wrote 10 files and
`git diff --name-only` printed 0 paths: the generator's output at the base registry (registry@254d4e9ece847acb)
equals the committed bytes for all 10, byte for byte (verified on a second instrument by comparing each
`git cat-file -p HEAD:<path>` blob to the worktree file: 10 of 10 equal, 0 CR bytes on either side).
`git status --porcelain` listed 3 of those 10 as ` M` while `git diff --name-only` printed none -- a
stat-dirty, content-clean index state, not drift.

## 2. The row, and the generator's actual diff

ONE row inserted into `infra/logic/registry/scopes.json` (17 inserted lines; nothing else hand-edited):
class `FIRM`, key/long `quillwater`, short `qwt`, tenancy `FIRM`, bucket `opal-data-quillwater`,
`bucket_provisioned` false, a `note` recording that it is fictitious, and a disabled `client` tenant. No
aliases, no masters, no pipeline tree.

`python lib/opal_naming.py validate` at `generated`: rc 0,
`VALIDATE: OK 24 system row(s), 10 scope row(s), 16 warning(s) at registry@4ca3c0b550ccb1b7`. **0 refusals,
and the same 16 warnings as at `expected_set`, none of which names `quillwater` or `qwt`.** Round 1's
`WARN scopes.json[3].key: firm 'quillwater' is not in NAMING_SCHEMA.json firm_forms` (row W8-S2) is GONE,
and gone by construction: after RULING ONE the schema is v1.9 and carries no `firm_forms` key, and the only
`warnings.append` site left in `validate()` is `lib/opal_naming.py:425`, inside the `systems.json` loop --
**a scopes row has no reachable warning site.**

`python lib/opal_naming.py generate --out .`: `GENERATE: 10 written, 0 skipped, into . at
registry@4ca3c0b550ccb1b7`, committed unedited. `git diff --name-only 529b5c39fb ed8771f9e8` prints 11
paths; less `infra/logic/registry/scopes.json` the 10 that remain are the expected set exactly -- 0
only-expected, 0 only-actual.

## 3 and 4. A hand-typed carrier of the firm is refused

Each arm is a `--- /dev/null` new-file patch run in the PRACTICE COPY (the registry that carries the row)
with `python .tools/naming-gate.py --enforce --diff <patch>`. Both exit 1.

- **ADDRESS** (`hand_address.patch`: `SILVER_POSITIONS = "opal-data-quillwater/silver/x"` in
  `data/quillwater/config.py`) -- `NAMING REFUSE ... opal-data-quillwater/silver/x -> {source}/quillwater/silver/x`,
  `NAMING-GATE: REFUSE 1 graded`, rc 1.
- **NAME as a dict key** (`hand_name.patch`: `FIRM_SETTINGS` with both `"quillwater"` and `"qwt"` as keys, in
  `data/quillwater/firm_settings.py`) -- two refusals, `quillwater -> lookup('quillwater')` and
  `qwt -> lookup('quillwater')`, `NAMING-GATE: REFUSE 2 graded`, rc 1.

**Control arm, the discriminator.** The same two patches run in the SLOT worktree, whose registry has no
such row: the address grades `NAMING RAISE ... K1: segment 1 'opal-data-quillwater' is neither a source nor
a tier`, `NAMING-GATE: WARN 1 graded`, rc 0; the name file grades `NAMING-GATE: PASS 0 graded`, rc 0. So
both refusals are produced by the ONE row and by nothing else.

Saved outputs are in `deliverables/0.9.0_WK_LGIC_ENFORCE~5/`: `hand_address.refused.out.txt`,
`hand_name.refused.out.txt`, `control_before_row_address.out.txt`, `control_before_row_name.out.txt`,
`validate_at_generated.out.txt`, `generate_at_generated.out.txt`, both patches, and `expected_diff.r2.txt`.

## Nothing live moved

Nothing was written to AWS and no Terraform command ran. The practice worktree was removed clean; the
scratch branch is left in place and was never pushed.

```json
{
  "scratch_branch": "prac-lgic-enforce-d1-r2",
  "firm": {
    "long": "quillwater",
    "short": "qwt"
  },
  "commits": {
    "expected_set": "529b5c39fb7ee5ba0f71a601ffde53e4bc7c35ac",
    "generated": "ed8771f9e8fcc913488741a553bf8f69afa28e3c"
  },
  "expected_files": [
    ".tools/ds-precommit-check.py",
    "data/assets/scripts/gold/investor_reporting/directory_runner.py",
    "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py",
    "data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py",
    "data/firm_registry.json",
    "infra/aws/lambda-edge/_shared/firm-config.mjs",
    "infra/aws/lambda/investor-reporting/_authz/loaders.py",
    "infra/aws/terraform/modules/opal_name/generated_locals.tf",
    "infra/aws/terraform/modules/opal_name/tests/opal_name.tftest.hcl",
    "infra/aws/terraform/modules/opal_name/tests/vectors.json"
  ],
  "actual_files": [
    ".tools/ds-precommit-check.py",
    "data/assets/scripts/gold/investor_reporting/directory_runner.py",
    "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py",
    "data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py",
    "data/firm_registry.json",
    "infra/aws/lambda-edge/_shared/firm-config.mjs",
    "infra/aws/lambda/investor-reporting/_authz/loaders.py",
    "infra/aws/terraform/modules/opal_name/generated_locals.tf",
    "infra/aws/terraform/modules/opal_name/tests/opal_name.tftest.hcl",
    "infra/aws/terraform/modules/opal_name/tests/vectors.json"
  ],
  "outputs": {
    "hand_address_refused": "NAMING REFUSE data/quillwater/config.py:3 opal-data-quillwater/silver/x -> {source}/quillwater/silver/x\n  why: NEW and OUT-OF-PATTERN as S3Key: REFUSE; hand-kept carrier of 'quillwater' outside every permitted context: read it through lookup('quillwater')\nNAMING-GATE: REFUSE 1 graded",
    "hand_name_refused": "NAMING REFUSE data/quillwater/firm_settings.py:3 quillwater -> lookup('quillwater')\n  why: NEW hand-kept carrier (context rule); hand-kept carrier of 'quillwater' outside every permitted context: read it through lookup('quillwater')\nNAMING REFUSE data/quillwater/firm_settings.py:3 qwt -> lookup('quillwater')\n  why: NEW hand-kept carrier (context rule); hand-kept carrier of 'qwt' outside every permitted context: read it through lookup('quillwater')\nNAMING-GATE: REFUSE 2 graded",
    "validate": "VALIDATE: OK 24 system row(s), 10 scope row(s), 16 warning(s) at registry@4ca3c0b550ccb1b7"
  }
}
```
