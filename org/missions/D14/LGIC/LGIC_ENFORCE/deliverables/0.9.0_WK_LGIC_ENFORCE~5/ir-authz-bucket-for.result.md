# LGIC_ENFORCE.TO-EN-v-4 -- IR authz `bucket_for` as a generated view: result

Worker `0.9.0_WK_LGIC_ENFORCE~5`, branch `wk-lgic-enforce-1-5-v4`, base `b02fdaa849`.

## What landed

`infra/aws/lambda/investor-reporting/_authz/loaders.py` was rewritten in place by
`python lib/opal_naming.py generate --out . --target infra/aws/lambda/investor-reporting/_authz/loaders.py`
at `registry@50e4fabd1cb6a150`. The diff against the base adds 4 lines, all of them comments:

- the GENERATED begin mark `[bucket_for]`;
- two lines saying `bucket_for` carries no registry row (it reads the env map Terraform sets from `local.firm_bucket_map`);
- `# END GENERATED [bucket_for]`.

The `bucket_for` body is byte-identical to the base. No consumer was repointed and nothing was deployed.

## Criteria (run under `timeout 120`, verbatim)

| id | verdict | deciding line | denominator |
|---|---|---|---|
| V4-AC1 | PASS-GENERATED-HEADER rc 0 | `WITHOUT A GENERATED MARK AT REGISTRY HASH 50e4fabd1cb6a150: []` | 1 of 1 carrier |
| V4-AC2 | PASS-DELTA0 rc 0 | `BASE: b02fdaa849  FILES: 1  EXPORTS EQUAL: 1  DIFFER: []` | 1 of 1 carrier, 11 of 11 probes |
| V4-AC3 | PASS-CONSUMER-TESTS rc 0 | `131 passed` | 131 of 131 tests |

## Controls

- **Mutant.** check_en.py's own `exports_of` compared the view against scratch mutants. With `IRPT_DIRECTORY_BUCKET_MAP`
  unset, which is the checker's own state:
  - a raise-class mutant reads DIFFER;
  - a return-path mutant reads EQUAL.

  With a map set, both read DIFFER. The view reads EQUAL under both arms.
- **Determinism.** Two runs of the three criteria gave identical output apart from pytest wall time.
- **Gates on the .py.** py_compile rc 0, ruff py39 clean, ds-precommit-check rc 0, 0 non-ASCII bytes, LF only.

## Rows

- `LGIC_ENFORCE-W5-S1` (OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO~G`). Under the checker's environment,
  V4-AC2 grades only `bucket_for`'s refusal branch, so it would also pass a view whose mapped branch changed.
  This generation is unaffected: the body is unchanged, and the view reads EQUAL with the map set.
- `LGIC_ENFORCE-W5-S2` (OBSERVATION, INERT). The pre-flip dry run of `proof-of-spec-check.py` refuses a tracked
  carrier that was modified in place as "ALREADY COMMITTED at HEAD" (CCX) until the carrier is staged:
  - unstaged: rc 1;
  - staged in a temporary index copy: rc 0.

  The real index was never pre-added.

## Not claimed

- Anything about the deployed Lambda.
- The other DEC-5 carriers.
- A fix to the checker, whose fixed inputs are read-only to this worker.
