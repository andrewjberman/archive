# MDPF_TAXSMA-S5 / Stage 6 -- read for the disarm (fork of 2.0.0_SA_COO~D1, 2026-10-13 ~11:2xZ)

Read-only. Input: CTO msg 4773 (round-5 ADDENDUM 3). Nothing here is a cell, an order or a commit. Anchors are file:line at HEAD or S3 key, read 2026-10-13.

## 0. Verdict in four lines

1. The import failure is real and is exactly as stated: `from lib.opal_naming import address` at `taxsma_assets.py:95` fails on the runner.
2. It is NOT the only thing that kills Stage 6. From 2026-08-19 to 2026-09-20 Stage 6 died on a different line: the runner role has no `s3:ListBucket`
   on `opal-data-assets` (`C2 FAIL-LOUD ... AccessDenied`), and from 2026-08-15 to 08-18 on `CROSS-AXIS COHERENCE GATE FAILED (global)`. The ImportError of
   09-21 masks the C2 failure. Fixing `lib.opal_naming` alone will move the first failure from line 95 to `load_served_account_count`
   (`dim_mdpf_aggregate_aua_timeseries.py:691`) and step 6d will still not be reached.
3. The last green Stage 6 was 2026-08-14 (marker `gold/mdpf_revamp/meta/cycle-complete.json` LastModified 2026-08-14 07:28:26Z). The row's "since 09-21"
   (MDPF_TAXSMA-S5, "measured on today's run only; earlier runs were not read") is the date the import began to fail, not the date Stage 6 stopped.
4. The gold lambda writes the aggregates, the Cottonwood family and non_model_assets itself; what is stale is the runner-only set: the three
   `account_distribution.json` (2026-08-18), the three `aum_metrics.json` (2026-08-14) and the marker.

## 1. The failure, proved from the runner's own logs

- Dispatch: `mdpf-daily-dispatch.sh:122-125` syncs `s3://opal-data-mdpf/code/scripts/` -> `/opt/mdpf/scripts/` and `code/config/` -> `/opt/mdpf/config/`,
  both `--delete`. Nothing outside those two prefixes reaches the runner. `PY` is the system python; `REVAMP_DIR=/opt/mdpf/scripts/gold` (`:480`).
- Step: `revamp_stage()` (`:496`) runs 6a `build_mdpf_spine.py --firm all` with `|| return 1`; any failure returns before 6b, 6c, 6d, 6e. The caller
  (`:606-643`) logs `Stage 6 REVAMP failed (rc>0) -- NON-FATAL ... no marker written`, sets `REVAMP_RC=1`, puts the CloudWatch metric
  `MDPF/DailyChain RevampParallelFailed=1` (`:657`), and exits 0 with `CHAIN_STATUS=complete`. Nothing else is skipped: 6b account_distribution, 6c
  non_model_assets, 6d the Cottonwood legs and the global re-stage, 6e aum_metrics, and the completion marker are the steps that never run.
- Logs: `s3://opal-data-mdpf/telemetry/mdpf-daily-runner/logs/<RUN_ID>.log` (133 objects, 2026-05-18 .. 2026-10-12; `:114`). 65 read from 2026-08-01:
  11 `Stage 6 REVAMP complete` (last 2026-08-14), 37 failed on a non-import error, 14 failed on the import (first 2026-09-21), 3 had no Stage 6 line.
- A real line, `mdpf_daily_20261012_125232.log`: `File "/opt/mdpf/scripts/gold/taxsma_assets.py", line 95 ... from lib.opal_naming import address` ->
  `ModuleNotFoundError: No module named 'lib.opal_naming'` -> `step STAGE6-REVAMP rc=1 dur=2s status=error`. Same lines on 10-09 and 10-11.
- Why the message says `lib.opal_naming` and not `lib`: `taxsma_assets.py:91-93` puts `_REPO_ROOT` (the gold dir four levels up, which on the runner
  resolves to `/`) on `sys.path`, and `/lib` is a directory on the host, so `lib` imports as a namespace package and only its submodule is missing.
  Consequence: a `lib/opal_naming.py` placed under the gold dir is found FIRST (the script dir is `sys.path[0]`) and merges with `/lib`; no `__init__.py`
  is needed, and none is shipped in the lambda zip either (`build_package.py:194-196`).
- The runner's `taxsma_assets.py` is an older copy than HEAD: its line 95 imports `address` only; HEAD imports `address, lookup` and calls `lookup()`
  at module scope (`:160`), which reads the registry at import. A sync of HEAD `taxsma_assets.py` therefore needs the registry files (section 2).

## 2. What must be in the runner tree

The import closure of Stage 6 (`build_mdpf_spine`, `dim_mdpf_aggregate_aua_timeseries`, `dim_mdpf_account_distribution`,
`dim_mdpf_non_model_assets`, `dim_mdpf_aum_metrics`; 11 local gold modules) was computed from the AST against the 39 objects under `code/scripts/gold/`:
every local module is present (`trading_calendar.py` included). The only unresolved import is `lib.opal_naming`, reached from `taxsma_assets.py:95` and
`taxsma_membership.py:68`.

`lib/opal_naming.py` (3,808 lines) imports only the stdlib; `REPO = dirname(dirname(__file__))` (`:48-49`); it reads the registry and the schema relative
to REPO (`:50-53`). The lambda zip ships exactly eight inputs (`build_package.py:205-213`): `lib/opal_naming.py`, `infra/logic/registry/{systems,
scopes,tiers,resources,exemptions,remediations,reporting_policies}.json`, `org/standards/NAMING_SCHEMA.json`. Optional registry files are read as None.

Destination keys that resolve with no dispatch change (REPO = the gold dir):
- `s3://opal-data-mdpf/code/scripts/gold/lib/opal_naming.py`
- `s3://opal-data-mdpf/code/scripts/gold/infra/logic/registry/{systems,scopes,tiers,resources,exemptions,remediations,reporting_policies}.json`
- `s3://opal-data-mdpf/code/scripts/gold/org/standards/NAMING_SCHEMA.json`
(nine objects). The alternative, a `PYTHONPATH=/opt/mdpf/scripts` in the dispatch, is a dispatch edit and is not needed.

## 3. Stage 6's write set, from code, with the current vintage of each key (head_object, 2026-10-13)

All in bucket `opal-data-assets`; every step is an overwrite. Written by the runner only unless the last column says the lambda also writes it.

| step | script | key | LastModified now | lambda also writes? |
|---|---|---|---|---|
| 6a | build_mdpf_spine.py --firm all, then `s3 cp` (`:503-514`) | `gold/mdpf_revamp/{49financial,inflection,global}/aggregate_aua_timeseries.json` | 2026-10-12 17:32:44Z | YES (`consolidator stage_put`; the 17:32Z write was the CN-d-1 on-demand run) |
| 6b | dim_mdpf_account_distribution.py --firm X --upload (`:518-520`) | `gold/mdpf_revamp/{49financial,inflection,global}/account_distribution.json` | **2026-08-18 12:47Z** | NO: the consolidator reads `global/account_distribution.json` for frontier counts (`load_account_dist_frontier_counts`) and never writes it |
| 6c | dim_mdpf_non_model_assets.py --upload (`:524`) | `gold/mdpf_revamp/global/non_model_assets.json` | 2026-10-12 17:32:46Z | YES (`nma.STAGING_KEY` via `_detail`) |
| 6d | assets_gold build_dim_model_portfolio / pair / slice --upload (`:554-556`) | Cottonwood family objects under `gold/mdpf_revamp/cottonwood/*` (script-owned keys; not enumerated here) | `cottonwood/*` current at 2026-10-12 17:32Z | YES (`run_cottonwood_family`) |
| 6d(3) | build_mdpf_spine.py --firm global, `s3 cp` (`:563-565`) | `gold/mdpf_revamp/global/aggregate_aua_timeseries.json` | as 6a | YES |
| 6e | dim_mdpf_aum_metrics.py --firm all --upload (`:588`, soft-fail) | `gold/mdpf_revamp/{49financial,inflection,global}/aum_metrics.json` (cottonwood's is current) | **2026-08-14 07:28Z** | NO for the three firm scopes |
| marker | python heredoc + `s3 cp` (`:608-637`) | `gold/mdpf_revamp/meta/cycle-complete.json` | **2026-08-14 07:28:26Z** | NO |

What changes the day Stage 6 resumes: the three `account_distribution.json` and three `aum_metrics.json` move from 6-8 weeks stale to fresh, and the
marker is rewritten. The staged global `account_distribution.json` is read by the gold lambda for its FRONTIER account counts, so the lambda has been
composing counts from an 8-week-old distribution; the first fresh object moves `account_count` at the frontier (the declared seam, 160 versus 162 on
the Int/Ltc blend in the CN-d-1 read) and that is a served-number change to be priced, not a side effect. Whether the `platinum/` publisher bridge
reads the staged aum_metrics (the dispatch comment `:577-580` says it does) was not read here.

## 4. The sync path

`docs/deployment/MDPF_RUNNER_CODE_SYNC.md`: named files only; `bash .tools/safe-deploy.sh <files>`; read back with
`python .tools/mdpf-code-equality.py --files <paths>`; whole-tree print before and after; rollback is each key's prior VersionId.
Two facts that make this NOT a plain named-file sync:
- `lib/opal_naming.py`, the registry JSON and the schema are outside `data/mdpf/scripts/`, so `.tools/safe_deploy_core.py`'s layer table
  (`:435-440`, `gold -> code/scripts/gold/`) does not map them. The tool's mechanism for a non-layer file is a declared ARTIFACT or bundle member
  (`:192-207` `partner_roster`, `:374` `lib/trading_calendar.py`). Declaring nine members is an edit of `.tools/safe_deploy_core.py` (a cell, and the
  file is shared by every runner product); the equality tool reads only the five declared trees, so these nine keys will show as EXTRA_ON_S3 in its
  whole-tree print and never as EQUAL. Their read-back instrument needs to be named (sha256 of each object against `git show`).
- The CloudOps classification of the 33 non-EQUAL names (ledger `mdpf-canon-r4-code-deploy-dell1-20261012`) does not mention `opal_naming`, the
  registry or the schema: they are outside the five trees, so the table could not have listed them.

## 5. The arm and its hazards

- The arm "the next dispatch reaches step 6d": a log line `[mdpf-dispatch] 6d COTTONWOOD legs complete (dim <date> + pair + slice + global re-stage)`
  in `s3://opal-data-mdpf/telemetry/mdpf-daily-runner/logs/<RUN_ID>.log`, and `STAGE6-REVAMP rc=0` in the run's `status.json` / `history/<RUN_ID>.json`,
  and the marker's LastModified moving.
- "Legacy outputs unchanged" is measurable on `platinum/mdpf/aggregate_aua/<date>.json` and `aggregate_aua_timeseries.json` (written by the legacy
  chain, not Stage 6) and on the 16 served gold objects of the date: byte-equal before and after the first resumed dispatch.
- Hazards, in the order they bite:
  1. **The C2 AccessDenied.** `mdpf-daily-runner-ec2-role` lacks `s3:ListBucket` on `opal-data-assets`
     (`dim_mdpf_aggregate_aua_timeseries.py:691`, AccessDenied on `ListObjectsV2`, prefix `portal/gold/mdpf/49financial/aggregate-aua-timeseries/`). This
     is an IAM change on the runner role (Terraform, its own pair), or a code change to the carry-vintage reader. Without it the arm cannot be met.
  2. **The cross-axis gate.** `CROSS-AXIS COHERENCE GATE FAILED (global)` failed Stage 6 on 08-15 .. 08-18; the lambda passes it today
     (`cross-axis gates PASS` on the 10-12 fire), but the runner's older code (`dim_mdpf_aggregate_aua_timeseries.py` EQUAL; `mdpf_gold_consolidator.py` not
     a runner member) was not re-exercised against today's inputs.
  3. **Version skew.** The runner's `taxsma_assets.py` is older than HEAD; syncing only the nine keys leaves it on `address` only, which is the lowest-risk
     state. Syncing HEAD `taxsma_assets.py` pulls a registry read at import and the `taxsma_membership`/`taxsma_snapshot` set with it: sync the nine
     keys and leave the taxsma modules as they are unless the classification table says otherwise.
  4. **Overwrites of lambda-written staged keys.** 6a and 6d(3) overwrite the staged aggregates the lambda writes; the dispatch's copy is built
     two hours before the 13:30Z fire and the lambda overwrites it; no served object reads the dispatch's copy. 6c overwrites `non_model_assets.json` the
     same way.
  5. **The fold and CN-d-1 interplay.** The fold deploy changes `dim_mdpf_account_distribution.py` and `dim_mdpf_aum_metrics.py`, both Stage 6
     members; syncing them (D1 of the fold order) while Stage 6 is dead changes nothing the runner executes. The CTO's order (the fold deploys first)
     holds: a resumed Stage 6 should run the fold's code from its first dispatch, not the pre-fold code, or the first fresh staged distribution is
     built twice.
  6. **6d writes Cottonwood.** The legs write the Cottonwood family under `gold/mdpf_revamp/cottonwood/*`, which the lambda also writes the same
     morning; the two producers have not both run since 08-14.
  7. **Moratorium.** Nothing here builds an alert; the metric `RevampParallelFailed` already exists and is not gated.

## 6. What was not read

Row MDPF_TAXSMA-S5's `disarm` text and notes were read in the file (INVESTIGATION_v1.md:349-372); the three Cottonwood scripts' own key lists
(`data/assets/scripts/gold/build_*.py`) were not enumerated; the IAM policy text of `mdpf-daily-runner-ec2-role` was not read (only the AccessDenied
message in the log); whether platinum reads the staged aum_metrics was not read.
