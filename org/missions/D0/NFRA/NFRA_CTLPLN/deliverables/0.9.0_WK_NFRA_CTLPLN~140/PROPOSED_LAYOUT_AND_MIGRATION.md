# PROPOSED LAYOUT AND MIGRATION -- Lambda source map (CT-bb-1, stage 1)

Worker 0.9.0_WK_NFRA_CTLPLN~140, read at HEAD 833181d311. Read-only: nothing here applies anything, no `terraform` command was run, and for every Terraform step a plan (never an apply) is the check. Counts come from `LAMBDA_SOURCE_MAP_CONSUMER_CENSUS.md` in this folder.

Census in one line (at HEAD 76890af416): 2524 files name the map; classes read_whole=175, write=6, test=21, doc=2322, read_one=0, other=0; 240 function entries; the deploy script has 27 commits, 13 by non-owners (12 CODE, 1 DATA).

## (a) Folder, file names, one real entry

- Folder: `infra/aws/lambda/ci/function-map/`. The name drops the old string, so after the split a search for the old name finds only history and documents.
- One file per function: `function-map/<function-name>.json`, 240 files. Each file holds the entry object itself (no wrapper and no `functions` key). The file name is the key; a reader takes the stem.
- Top-level metadata `_description`, `_note` and `_updated` moves into `function-map/README.md` (documentation, read by no consumer).
- `_last_deploy_recorded` has no function home. Proposed: drop it in the split (a CTO decision). Its writers are in surprise rows NFRA_CTLPLN-W140-S5.
- No aggregate file is stored (round-28 ruling 2).

Real entry, `functions["mdpf-gold-lambda"]` at 833181d311, stored as `function-map/mdpf-gold-lambda.json`:

```json
{
  "source_dir": "infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda",
  "files": [
    "build_package.py"
  ],
  "tf_file": "infra/aws/terraform/mdpf-pipeline/gold-lambda.tf",
  "tf_resource": "aws_lambda_function.mdpf_gold",
  "iam_role": "mdpf-gold-lambda-role",
  "_build_note": "MDPF_CANPLAT.P1-2: package is ASSEMBLED FROM A PINNED COMMIT by build_package.py (git show <pin>:<path> per module; 22 entries at the 70a0828226 pin: 18 modules incl. validate_interpolated_backfill + mdpf_category_registry.py + lib/trading_calendar.py AS trading_calendar.py, 3 configs, + r7_comparator.py/sectionB_field_paths.json (count corrected 2026-08-28: the note said 19 while PACKAGE declared 22), FLAT at zip root; BUILD_MANIFEST.json inside carries per-module sha256 + config hashes). source_dir holds the BUILDER, not the runtime source -- the runtime source is the pinned repo commit recorded below and inside BUILD_MANIFEST.json. Deps: pandas-pyarrow-requests-layer (existing) + mdpf-gold-calendar-deps (pmc<5 pin, load-bearing). DEPLOYED UNWIRED (zero triggers) until the floor re-point act.",
  "artifact_s3_key": "portal/gold/mdpf/_code/mdpf-gold-lambda.zip",
  "artifact_s3_bucket": "opal-data-assets",
  "artifact_sha256": "bnpYayh00uIIIlZEMjc3pKmKz6bFcuHGY6F2DI4HZTY=",
  "last_deployed_commit": "70a08282269217b3ccae4bb2776372690201743f",
  "last_deployed_at": "2026-08-28T17:28:29Z"
}
```

## (b) Readers

Terraform. The three roots that read the whole map (`infra/aws/terraform/investor-reporting/{account-return-daily,reporting-gold-iso,reporting-publish-iso}/locals.tf`) each use `jsondecode(file(...))`. Replace it with:

```hcl
locals {
  function_map = { for f in fileset("${path.module}/../../../lambda/ci/function-map", "*.json") :
    trimsuffix(f, ".json") => jsondecode(file("${path.module}/../../../lambda/ci/function-map/${f}")) }
}
```

- All three need the `fileset` form, because each looks up one key among 240. Each root's lookup changes from the `functions` path to `local.function_map[<name>]`.
- No Terraform consumer CANNOT work without an aggregate. The `for` expression builds the map in memory at plan time and nothing is stored. A `file()` per function would need a literal list of names and is not needed.
- Caveat: `fileset` resolves against the module path, as the existing `file()` calls already do, so CI must run from the checkout.

Python. One shared reader, stdlib only, in a new file `lib/opal_lambda_map.py`:

- `load_entry(name)` reads `function-map/<name>.json` and raises on a missing file (loud).
- `load_all()` returns `{name: entry}` built from the folder, sorted. It is never written back.
- Callers that need the full set: `lib/opal_naming.py` (`_lambda_source_map`), `lib/opal_naming_scope.py` and `lib/opal_lgctfm.py` use `load_all`. Callers that need one entry use `load_entry`.

Shell and node. No shared shell helper is proposed. `jq . function-map/<name>.json` reads one entry; node uses `fs.readFileSync` on one file. Each change is two or three lines.

## (c) Migration order, by consumer class, with risk

- Step 0, additive, no consumer changes. Generate the 240 files from HEAD's map; check each file equals `functions[stem]` and that the count is 240. The map stays. Terraform plan change: none. Risk: low. The real risk is a writer that updates one copy only (see (e)).
- Step 1, the atomic commit in (d). Live readers switch to the folder, live writers write one file, and the map is deleted, all in one commit. Terraform plan change: the three `locals.tf` roots change expression, not resources. The check is `terraform plan` on each root showing zero resource diffs. Risk: high. It touches every live reader, the commit-time naming gate and the deploy path.
- Step 2, closed-round deliverables: 131 readers and writers under `org/missions/` (129 read, 2 write; the census script is one of the 129). Not migrated. A re-run after the split fails loud on the missing file, except `battery_ib_rtf_1.py`, which would re-create the aggregate; retire that file in Step 1. Terraform plan change: none. Risk: low at run time.
- Step 3, documents: 2322 DOC files, text only. Terraform plan change: none. Risk: none at run time.

Only Step 1 changes a Terraform plan.

## (d) The atomic set and what can follow

Atomic set: each member reads or writes the map on a live path (a gate, the deploy, a plan, or a shared import), or fails silently when the file is missing. All must change in the same commit as the removal.

- Terraform: the three `locals.tf` roots above (`file()` on a missing map fails the plan).
- Deploy path: `infra/aws/lambda/ci/build-and-upload.sh` (write), `infra/aws/lambda/ci/record-terraform-deploy.sh` (write; owner `0.7.0_AE_CloudOps` only), `infra/aws/lambda/ci/build-nodejs-lambda.sh`, `infra/aws/lambda/verify-local.sh`, `.github/workflows/lambda-deploy.yml`, `.tools/deploy_ledger.py`, `.tools/check-lambda-layer-deps`, and the ci tools `deployed-drift-classify.py`, `record-deploy-scope.py`, `release-census.py`, `source-map-staleness-census.py`.
- Gates and shared imports: `.tools/naming-gate.py` (returns an empty citation set when unreadable), `.tools/parity-gates.sh` (P9 warns and returns), `lib/opal_naming.py`, `lib/opal_naming_scope.py`, `lib/opal_lgctfm.py`.
- Silent readers: `org/modules/graph/extract_iam.py` (returns `[]` when absent), `org/modules/graph/extract_s3.py` (skips when absent), `org/modules/graph/extract_eventbridge.py`.
- Writers: `.tools/backfill-lambda-iam-mapping.py`, and `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/live_walk/repin_source_map_rows.py` (the re-pin writer of record).
- Lane grant: `.owned-paths.yaml` (line 2800 names the map path; it must name the folder, or the grant lapses).
- Routing: `infra/aws/lambda/investor-reporting/_authz/routetable.py` (reads the map for the route table).

Can follow, because each fails loudly and sits in a manual tool or a record: `org/modules/graph/lambdamap_cli.py`, `comp_closure.py`, `extract_lambda_routes.py`; `rcg/bin/lexicon.py`, `rcg/bin/mark.py`; `infra/aws/ec2/estate-report-runner/estate_report_runner.py` (its hop degrades with a WARN, and its checkout line must change in the same commit or the hop stays disabled); the closed-round files in (c) Step 2; and the remaining readers under `org/tier1_exec/` and `org/tier2_senior/`, which are closed-round deliverables too.

## (e) What a deploy does while the map is half-split

- Step 0 window (folder and map both present). Readers still read the map. A writer that updates one copy only leaves the other stale with no error. Rule: no deploy between Step 0 and Step 1; land both under a deploy freeze.
- Map removed before a reader changes. Where the reader raises, the failure is loud: `build-and-upload.sh` throws before the upload, so nothing is served, and Terraform `file()` fails at plan, so nothing applies. The silent readers in (d) (`naming-gate`, P9, `extract_iam`, `extract_s3`) report a clean result on nothing. The split commit must make all four fail loud.
- A writer still pointed at the old path after the split re-creates the aggregate file, and the readers split again. `battery_ib_rtf_1.py` is the known case; retire it in Step 1.
- After Step 1, a deploy records one function file. `record-terraform-deploy.sh` writes only the deployed function's file, so two deploys of different functions no longer write the same file. The same-file overlap the census measured is removed by the layout, not by ordering.

BLIND: the census reads this repository only. A reader outside it (an external CI configuration, a second repository, or a runtime S3 reader) is not seen. The repository's documents name no such reader; none is proposed here.
