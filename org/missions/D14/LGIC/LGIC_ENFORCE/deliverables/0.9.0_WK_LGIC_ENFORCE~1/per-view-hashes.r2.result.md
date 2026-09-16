# Result -- LGIC_ENFORCE.TO-EN-r-6-r2 (per-view hashes, every view regenerated)

Assignee: `0.9.0_WK_LGIC_ENFORCE~1` -- worktree `wk-lgic-enforce-2c-6`, cut from `CLOUD` @`1d519bff1b`.
Artifact commit: `39cbad4214`. Surprise-row commit: `fab704bdc4`.

## What changed

`lib/opal_naming.py`: `registry_hash(reg_dir=None, only=None)` now restricts its sha256 feeding to
`only` when given (still name order, still CRLF-as-LF). `TARGET_REGISTRY_KEYS` is a data table, one row
per generated target keyed by its repo-relative path, naming the registry KEYS (`scopes`, `tiers`,
`exemptions`, `systems`, `resources`) that target's renderer reads; `_target_registry_files(target)`
turns that into sorted `<key>.json` file names, and `_view_mark(h16, target)` builds the exact mark text
`MARK + h16 + " over " + ",".join(files)`. `_begin()`, `_render_view()`'s JSON branch, `_gen_locals()`,
`_gen_tftest()` and `generate()`'s `VECTORS_PATH` branch all build their mark through `_view_mark()`;
`generate()` computes `h16` per target inside its loop (`registry_hash(only=_target_registry_files(t))[:16]`)
instead of once globally for every target, which was round 1's bug (row W1-S14).

Nine of the ten targets' file sets were derived by INSTRUMENTING the actual registry-dict access each
renderer makes (a wrapping dict recording every `__getitem__`/`.get`, with the module's own registry
cache patched so indirect reads through `name()`/`_vocab()` are caught too, not just the `reg` parameter
each function receives directly) -- confirmed:

| target | registry files |
|---|---|
| `data/firm_registry.json` | `scopes.json` |
| `infra/aws/lambda-edge/_shared/firm-config.mjs` (`FIRM_CONFIG`) | `scopes.json` |
| `directory_runner.py`, `holdings_snapshot.py` (`firm_bucket_map`) | `scopes.json` |
| `perfrp_firm_pin.py` (`FIRM_TREES`) | `scopes.json,tiers.json` |
| `.tools/ds-precommit-check.py` (both tags) | `scopes.json` |
| `generated_locals.tf` | `exemptions.json,scopes.json` |
| `tests/vectors.json`, `tests/opal_name.tftest.hcl` | `exemptions.json,resources.json,scopes.json,systems.json` |

The tenth, `loaders.py`'s `bucket_for`, reads NO registry key at all -- its own pre-existing comment
already says so ("This definition carries no registry row"), and the instrumented probe confirms an
empty touched-key set. The mark format (`over <file>[,<file>...]`) and `check_en_r2.py`'s `PER_VIEW`
regex (`[A-Za-z0-9_.,-]+`, one or more) both require at least one declared file, so an empty declaration
is not mechanically expressible -- it would fail `require_per_view()` for ALL TEN generated files, not
just this one, since every `r6-*` subcommand calls it first. `scopes.json` is declared for `bucket_for`
instead, as its documented trust anchor (the same file `data/firm_registry.json` itself declares) rather
than a literal dict-key read. Filed as row `LGIC_ENFORCE-W1-S28` (class OBSERVATION, hazard_standing
INERT) for `3.0.0_SA_CVO` at L9 or a later round to confirm the attribution.

All 10 generated files were regenerated (`python lib/opal_naming.py generate --out .`); each diff against
the previously-committed bytes is exactly the mark line moving (two lines in `.tools/ds-precommit-check.py`,
one per tag) -- DELTA=0 on every carrier's content, confirmed both by `git diff` and by R6-AC4/R6-AC5.

## Acceptance -- 10 of 10 mechanical criteria PASS by output

| id | invocation (sub) | verdict |
|---|---|---|
| R6-AC1 | `r6-headers-current` | `PASS-PER-VIEW-HEADERS` |
| R6-AC2 | `r6-undeclared-inert` | `PASS-UNDECLARED-INERT` |
| R6-AC3 | `r6-declared-moves` | `PASS-DECLARED-MOVES` |
| R6-AC4 | `r6-delta0-ordered` | `PASS-DELTA0-IN-ORDER` |
| R6-AC5 | `r6-reproduces` | `PASS-GENERATE-REPRODUCES` |
| R6-AC6 | `r6-tests-v1` | `PASS-NO-NEW-FAILURE-V1` (14 pre-existing failures, 0 new) |
| R6-AC7 | `r6-tests-v2` | `PASS-NO-NEW-FAILURE-V2` |
| R6-AC8 | `r6-tests-v3` | `PASS-NO-NEW-FAILURE-V3` |
| R6-AC9 | `r6-tests-v4` | `PASS-NO-NEW-FAILURE-V4` |
| R6-AC10 | `r6-tests-v6` | `PASS-NO-NEW-FAILURE-V6` |

No criterion in this order carries `judgment="true"`; all ten are mechanical and graded by output.

## Controls

- **Mutant**: all ten `r6-*` subcommands run against a throwaway detached worktree at the spawn base
  `1d519bff1b` (pre-edit, old whole-registry mark, no `over` clause) -- `r6-headers-current` there prints
  `FAIL-NOT-YET-PER-VIEW`, rc=1, listing all 10 paths as carrying no per-view mark; every other subcommand
  shares the same `require_per_view()` gate, so the same FAIL is structural for all ten. FIRED-AS-EXPECTED.
- **Determinism**: all ten subcommands run twice at the same committed bytes (after `39cbad4214` and again
  after `fab704bdc4`, which touches no path this cell reads) -- identical verdicts both times; `git status`
  clean (only the untracked `.scratch/`) after every run. STABLE.

## Regression check

`lib/tests/test_opal_naming.py`: 80 passed, 2 failed
(`test_grade_agrees_with_every_worked_case[globgrph-serving|ECS_TASK_DEFINITION]`,
`[opal-globgrph|ECS_CLUSTER]`) -- matches the pre-stated RULING RED baseline exactly (the R-5 collision
named in this worker's prompt, unrelated to this cell); 0 new failures.

## Proof-of-spec validation

`python .tools/proof-of-spec-check.py org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/LGIC_ENFORCE.TO-EN-r-6-r2.per-view-hashes.proof_of_spec.json R6-AC1,R6-AC2,R6-AC3,R6-AC4,R6-AC5,R6-AC6,R6-AC7,R6-AC8,R6-AC9,R6-AC10`
-> `VALID (rc=0)`: structural=jsonschema, acceptance rows=10, violations=0; artifact-resolution 12
resolved at pin, 12 CONTENT-resolved; alignment-forward 10/10, backward 1/1; surprises-frame 1 entry
resolving to channel row `LGIC_ENFORCE-W1-S28`; invocation-alignment 10/10 comparable rows match modulo
placeholder expansion.

## Surprise row

`LGIC_ENFORCE-W1-S28` (class OBSERVATION, hazard_standing INERT, disposition UNDER_INVESTIGATION):
`loaders.py`'s `bucket_for` reads zero registry keys; the mark format needs at least one; resolved by
declaring `scopes.json` (its documented trust anchor). No remedy owed to reach PASS -- all ten criteria
pass under this resolution; filed for CVO/later-round confirmation of the judgment call.

## Status

`<status>` flips to `complete` in this same commit.
