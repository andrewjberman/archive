# LGIC_ENFORCE.TO-EN-g-9-r3 -- target-split -- result

`0.9.0_WK_LGIC_ENFORCE~5` on cell `EN-g-9` (RULINGS R-16, R-26). Worktree
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-3-5`, branch
`wk-lgic-enforce-3-5`, base `24bae9d9da` (CLOUD). Artifact commit `c966ff460f`.

## What landed

`lib/opal_naming.py` gains a **read-only** `targets` subcommand:

```
python lib/opal_naming.py targets [--extra-target <path>]
```

New functions: `_sdc()` (loads `.tools/safe_deploy_core.py` by path), `_lambda_source_map()`
(reads `infra/aws/lambda/ci/lambda-source-map.json`'s `functions` dict), `_import_hit()`
(import-aware text match, never a bare substring), `lambda_plane_consumers()`,
`terraform_plane_consumers()`, `hash_pinned_census()`, `targets_report()` and `cmd_targets()`.
`main()` gains the `targets` subparser and its `--extra-target` argument. `generate()` and
every generated file are untouched -- `targets_report()` never calls `generate()` and writes
nothing (R-16: a re-render re-stamps every SHIP view).

`lib/tests/test_opal_naming.py` gains 8 tests for the new functions, including one that
pins the discrimination this cell had to build: a Lambda function's source file merely
**mentioning** a target's stem in a comment (`.tools/ds-precommit-check.py` cited by name
in `_orion_api_silver_lib.py:17`'s Rule-14 comment) must NOT be counted as a live import.

## Classification at the cut (real run, no fixture)

```
$ python lib/opal_naming.py targets
TARGETS: 10
SHIP lambda data/firm_registry.json measured: lambda-source-map.json (2 consumer(s): irpt-intake-poller, irpt-ycharts-generate)
SHIP lambda infra/aws/lambda-edge/_shared/firm-config.mjs measured: lambda-source-map.json (3 consumer(s): auth-validator-edge, shared-advisor-router, shared-advisor-router-response)
SHIP s3 data/assets/scripts/gold/investor_reporting/directory_runner.py measured: safe_deploy_core (file_to_s3_target/bundle_for_member)
SHIP s3 data/assets/scripts/gold/investor_reporting/holdings_snapshot.py measured: safe_deploy_core (file_to_s3_target/bundle_for_member)
SHIP lambda infra/aws/lambda/investor-reporting/_authz/loaders.py measured: lambda-source-map.json (7 consumer(s): irpt-directory-search, irpt-export-render, irpt-holdings, irpt-narrative, irpt-performance-adapter)
SHIP s3 data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py measured: safe_deploy_core (file_to_s3_target/bundle_for_member)
REPO-ONLY tools .tools/ds-precommit-check.py measured: no S3/Lambda/Terraform claim (repo-local gate script, never packaged)
SHIP terraform infra/aws/terraform/modules/opal_name/generated_locals.tf measured: consuming root(s) infra/aws/terraform/shared-infra (git grep modules/<name>)
REPO-ONLY terraform infra/aws/terraform/modules/opal_name/tests/vectors.json measured: comp-find root census (test fixture beside the module, not a deploy)
REPO-ONLY terraform infra/aws/terraform/modules/opal_name/tests/opal_name.tftest.hcl measured: comp-find root census (test fixture beside the module, not a deploy)
PLANE lambda: 3
PLANE s3: 3
PLANE terraform: 3
PLANE tools: 1
HASH-PINNED CONSUMERS: 1 of 94 scanned
```
`rc=0`. The `lambda-source-map.json` row for `infra/aws/lambda/investor-reporting/_authz/loaders.py`
prints 7 consumers, truncated to the first 5 in the row text (`consumer(s): N` states the true count);
the checker's `_ROW` regex does not require the list to be exhaustive on the line. All 3 S3/DS rows
match `.tools/safe_deploy_core.py`'s own claim exactly (`file_to_s3_target`/`bundle_for_member`),
matching the order's stated cut (3 claimed).

`--extra-target zz-unclaimed/probe.txt` adds an 11th row `UNCLASSIFIED - zz-unclaimed/probe.txt
measured: no plane claims it` and the command exits 1.

## Criteria

All five mechanical criteria PASS-by-output against the live tree (no fixture, no injected runner):

- `G9R3-AC1` (`g9-target-count`): `AST count of generate()'s known list: 10; printed TARGETS: 10;
  classified rows: 10` -> `PASS-G9-TARGET-COUNT-EQUALS-AST`.
- `G9R3-AC2` (`g9-s3-plane-agrees`): `DENOMINATOR: 10 printed row(s); safe_deploy_core claims 3;
  printed as measured by it 3 (SHIP 3)` -> `PASS-G9-S3-PLANE-EQUALS-GATE`.
- `G9R3-AC3` (`g9-unclassified-refuses`): `planted zz-unclaimed/probe.txt: rc=1; printed UNCLASSIFIED:
  True` -> `PASS-G9-UNCLASSIFIED-REFUSES`.
- `G9R3-AC4` (`g9-fixtures-repo-only`): `fixtures printed REPO-ONLY with a plane: 2 of 2` ->
  `PASS-G9-FIXTURES-REPO-ONLY`.
- `G9R3-AC5` (`g9-consumer-census`): `census line: HASH-PINNED CONSUMERS: 1 of 94 scanned` ->
  `PASS-G9-CONSUMER-CENSUS-PRINTED`.
- `G9R3-AC6`: `python -m pytest -q --color=no lib/tests/test_opal_naming.py` -> `90 passed in 8.74s`
  (82 pre-existing + 8 new).
- `G9R3-AC7`: JUDGMENT. Recorded `UNVERIFIABLE-BY-INSTRUMENT`, `status_reason` naming
  `3.0.0_SA_CVO`, per the order and Rule-27 (judgment criteria are graded at L9, never
  self-graded). For the CVO's read: the Lambda-plane rows resolve `data/firm_registry.json` to
  `irpt-intake-poller`/`irpt-ycharts-generate` (basename-in-files, no local copy),
  `_shared/firm-config.mjs` to the three lambda-edge functions that `import` it in their
  `index.mjs` (content-scan, import-aware), and `_authz/loaders.py` to the 7 functions whose
  `entry.py` carries `import loaders as _loaders`; the Terraform-plane row names its one
  consuming root, `infra/aws/terraform/shared-infra` (measured via `git grep modules/opal_name`
  outside the module directory itself).

## Instrument notes (for the record, not a criterion)

- `lambda_plane_consumers()` first checks whether a target's basename is a function's declared
  build input (`files`) with no physical copy at that function's own `source_dir` (the "packaged
  flat from a shared dir" case -- `loaders.py`, `firm_registry.json`). Only when that fails does it
  fall back to a content scan of the function's actual declared files, and that scan is
  **import-aware** (`_import_hit`): a bare substring match on `.tools/ds-precommit-check.py`'s stem
  false-matched three unrelated functions (`inf-api-positions`, `inf-api-reps`,
  `opal-smartx-ingestion-pipeline`) via one shared file's Rule-14 comment
  (`infra/aws/lambda/inf-pipeline/inf-api-positions/_orion_api_silver_lib.py:17`) -- caught before
  landing, fixed by requiring the stem to sit inside an actual `import`/`from ... import`/`require(...)`
  statement, never a comment or docstring mention.
- `terraform_plane_consumers()` runs `git grep -l modules/<name> -- infra/aws/terraform` and drops
  hits inside the module's own directory (its own `main.tf`, `generated_locals.tf` and the tftest
  fixture all self-reference `modules/opal_name` in comments/paths and are not consumers of
  themselves).
- `hash_pinned_census()` scans `.tools/*.py` (94 tracked files) for `sha_metadata_key` (the S3/DS
  plane's per-member sha256 pin, `safe_deploy_core.py:222-294`) or `index_md5` (the plane's
  solo-file md5/ETag pin, `safe_deploy_core.py:~700-715`) -- `.tools/safe_deploy_core.py` is the
  one file carrying either marker, so `1 of 94`.

## Not claimed

- Nothing live moves; no AWS read, no Terraform apply.
- `generate()` was never invoked and no generated carrier's bytes changed (`git status` after the
  build showed only the two files this cell owns).
- The exact wording of each row's `measured:` field is this worker's own phrasing, not a fixed
  vocabulary the order specifies beyond "names the instrument" -- `G9R3-AC7`'s judgment covers
  whether the instrument itself (not the prose) is sound.
