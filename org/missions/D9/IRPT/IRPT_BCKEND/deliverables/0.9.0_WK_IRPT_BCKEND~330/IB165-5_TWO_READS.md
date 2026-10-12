# IB165-5 -- two reads at base 2d923d0564 (IRPT_BCKEND.TO-IB-pr-475, worker 0.9.0_WK_IRPT_BCKEND~330)

**Verdict 1 -- `commentary_ref`: HEAD_READS_SIBLING.** The mismatch the row described at an older base is still there at HEAD.
**Verdict 2 -- the landed prices store: WRITER_UNSCHEDULED** (`retired_as_source` false). A writer exists; nothing found runs it on a schedule.

Both are of the code and the declared infrastructure. No live read was made. Record: `IB165-5_two_reads.json`.

## 1. commentary_ref

- Write: `reports/commentary_draft_store.py:205-232` sets `commentary_ref` on the request ITEM by a conditional update (`:228`), beside the immutable `record`.
- Read: `ycharts/research/opal_packager.py:153` reads `record.get('commentary_ref')` from `ports['acceptance'].get(...)` (`:147`).
- The live port is a plain `DynamoAcceptance` (`reports/resident_installed.py:393-394`, given to `make_packager` at `:433`, bound at `:334`); its `get` returns only the parsed `record` attribute (`ycharts/generate/acceptance.py:68-71`).
- `commentary_ref` appears 0 times in `ycharts/generate` and in `resident_installed.py`; `git log -S` finds no commit that put it in `acceptance.py` or `resident_installed.py`. No commit made the two agree.
- By the code, a packager run on an item with the sibling attribute raises `COMMENTARY_REF_ABSENT`. Unmeasured live.
- Test crossing: none. The packager tests hand the packager a fake whose record holds `commentary_ref` inside it (`test_opal_packager.py:58-64`); the draft store tests never hand their item to the packager. 6 packager test files, 10 draft-store test files, 0 in both.

## 2. The prices store (`opal-data-cot`, `silver/prices/canonical_prices.parquet`)

- Writer: `data/cot/scripts/gold/build_canonical_prices_v2.py:907` (S_00 in `data/cot/scripts/gold/gold_dispatch.sh:78`). It runs only through `gold_dispatch.sh` (`--chain full` auto-runs it, `:1070-1081`; or `--chain silver-prep` / `--single S_00`), started by an operator.
- The scheduled cot gold path is silver sentinel rule (`cot-pipeline/eventbridge.tf:219-244`) -> `cot-bd-session-trigger` mode `gold-run` (`lambda_function.py:329`) -> SSM document `opal-cot-gold-run`. Its 18 `run_gold` lines (`ssm.tf:375-404`) do not name the writer.
- Census: `infra/aws`, 7343 files scanned, 4 with `build_canonical_prices`, all the bd firm's pipeline (0 cot). Second census, `infra/aws/terraform/cot-pipeline`: 19 files, 0 hits for the five terms; the same directory returns `ssm.tf` for `run_gold` (positive control). Graph: 2923 nodes, 10 hits for `cot.*gold`, one SSM document, no other dispatcher. The bd twin's daily rule (`bd-pipeline/eventbridge.tf:384`) shows a schedule of this kind is findable.
- The 2026-10-09 last-write is a one-time put, not the writer: the key is one of the 38 keys of the price rewrite (ledger `20261009T1320Z_..._cb-aj-2_deploy_completion.md`, W1 closed 13:43Z; preflight recorded writers=7 scheduled=0). The older version, 2026-06-09, matches the max date in the row, so it is probably the writer's last run (inferred).

## Not established

Live rule/document state; any hand run since 2026-06-09; the new VersionId; the live table; the deployed packager bundle against HEAD; tests were not run. Detail in the JSON `not_established`.

## Bounds

AWS reads: `comp-find --corpus aws` only (the served graph). Functions invoked, sign-ins, AWS writes, accounts, figures, vendor requests: 0.
