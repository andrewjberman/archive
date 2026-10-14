# MDPF_CANON round 7 -- never-widen pair for the ONE gold-package deploy that ships CN-h-1 (frontier account counts read the newest A4 account-distribution) and CN-l-1 (the Other Models dated carry)

**COO half SIGNED; CTO half OWED.** Drafted by a fork of `2.0.0_SA_COO~D1` on 2026-10-14 ~16:0xZ; read in full by the issuer, who re-measured the pin claims at signing (both commits
are ancestors of the pin; the pin is an ancestor of origin's `box/dell1`; the package-list line and the `legacy_address` call are in the pinned bytes). Nothing here is deployed. **SUPERSEDES `NEVER_WIDEN_PAIR_R7_CN_H_1.md`** (a CN-h-1-only draft written before the
cell was built; its numbers and its D1 are replaced by this file). The CN-j-1 publisher deploy is a different function and takes its own pair
(`NEVER_WIDEN_PAIR_R7_CN_J_1.md`); it does not touch `mdpf-gold-lambda` or `code/scripts/gold/`.

**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on `ADHOC.canon-r7-gold-deploy` (draft beside this file).
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1`, to be recorded at `ledger/NEVER_WIDEN_R7_GOLD_H1_L1_CTO_HALF.md`; COO half = this lane.
**Rulings this pair carries:** the CTO's round-5 ADDENDA 3-5 on the S5 disarm (msgs 4773, 4776, 4780, 4782: the frontier counts read the newest A4 at or before the axis, no
fallback to the staged object, name the per-scope moves, both branches, prior VersionIds); the CTO's naming route on call f6f8 / XA-c328 (msgs 5617, 5626, 5628: the loader's prefix is
the `legacy_addresses` row `mdpf-portal-gold-account-distribution`, registry commit `81453d51cf`); the round-6 analysis section 3 item 1 (msg 5589: a carried Other Models value
carries its date or is blank); and the lesson of the CN-f-1 CTO half, addendum 1: a store whose KEY carries a content hash is a CREATE on every run.
**Code:** CN-h-1 merged `9592daf75c` (order `task-orders/MDPF_CANON.TO-CN-h-1.frontier-counts-read-the-a4-distribution.md`, complete, AMENDMENT 1 = the registry-row prefix and the
package-list line); CN-l-1 merged `72ef4f8a3a` (order `task-orders/MDPF_CANON.TO-CN-l-1.other-models-dated-carry.md`, complete). The issuer re-ran the criteria on the merged tree: CN-h-1
reader 8 of 8, seams 6 of 6, comparator 5 of 5; CN-l-1 unit 8 of 8, seams 5 of 5, real 6 of 6. AC4 of CN-h-1 is a JUDGMENT criterion, ungraded.

## 1. Code

- **Pin:** `9592daf75c` (the CN-h-1 drain merge; it carries `72ef4f8a3a` and the registry row `81453d51cf` in its history, MEASURED by `merge-base --is-ancestor`), or a later commit
  that carries these five files byte-equal to it (read by content: `git show <pin>:<path>` against the merged blobs):
  `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`, `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`,
  `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py`, `infra/logic/registry/legacy_addresses.json`, `lib/opal_naming.py`.
  The pin is an ancestor of origin's `box/dell1` (MEASURED 2026-10-14 ~16:0xZ: `git ls-remote origin box/dell1` read `2366d7dd25...`; the three commits `81453d51cf`, `72ef4f8a3a` and
  `9592daf75c` are each an ancestor of it). The order re-reads this at its start.
- **What changes, CN-h-1** (`dim_mdpf_aggregate_aua_timeseries.py`, read at `9592daf75c`):
  - `load_account_dist_frontier_counts(firm_id, axis_date=None)`: the prefix is `legacy_address("mdpf-portal-gold-account-distribution", firm=firm_id).split("/", 3)[3]`, which resolves
    to `portal/gold/mdpf/<firm>/account-distribution/` in bucket `opal-data-assets` (MEASURED offline for `global`, `49financial` and `inflection`); it lists that prefix, selects the
    newest `<YYYY-MM-DD>.json` key at or before `axis_date`, reads and parses it, requires the object's `period` to be present and not after the axis, and returns
    `dict(meta.account_count_by_model_key)` plus the `__as_of__` sentinel. No axis, or no qualifying key, returns `{}` with a WARN; a listing, read or parse failure raises
    `C2-SIBLING FAIL-LOUD`; the staged `gold/mdpf_revamp/*/account_distribution.json` is no longer read by any path.
  - The two call sites (`build_firm_timeseries` for `49financial` and `inflection`, `build_global_artifact` for `global`) pass the last date of the series.
  - The module gains `from lib.opal_naming import legacy_address` at module scope, after the repo-root `sys.path` insert (the idiom `mdpf_gold_parquet.py` already uses in this lambda).
  - `data/mdpf/scripts/gold/tests/test_canplat_p1_1.py` and `test_global_fold_flag2.py`: one stub lambda each; `data/mdpf/tests/canon/test_frontier_counts_a4.py` (new, 7 tests; not shipped).
  - `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py`: ONE added package-list entry, `infra/logic/registry/legacy_addresses.json`.
- **What changes, CN-l-1** (`dim_mdpf_aum_metrics.py`, read at `72ef4f8a3a`): `OTHER_MODELS_KEY`, `OTHER_MODELS_CARRY_MAX_DAYS = 4`, `_dated_carry(dates, values, gi, max_days)`; in
  `build_aum_metrics` the `other_models` row, when its value at the as-of index is None, takes the last real pooled value within 4 calendar days (inclusive) and sets
  `as_of` = that date; its `account_count` is the count AT that date; beyond 4 days the row is absent. Every other model key keeps its existing last-real-value fallback. No new import.
  `data/mdpf/tests/canon/test_aum_metrics_dated_carry.py` (new, 8 tests; not shipped).
- **The rule as built (both cells):** the frontier cell of each overridden model line is the A4 map's value; a series key the A4 map does not carry (blends, the fold line `other_models`
  after CN-f-1) keeps its COMPOSED count; cottonwood never calls the loader; the pool-present day serves the Other Models row exactly as today, with no `as_of` key.
- **Evidence** (the issuer's checks, `round7/checks/`): `r6_cn_h_1.py` reader 8 of 8, seams 6 of 6 (S5: the loader calls `legacy_address` and types no `portal/gold/mdpf` literal; S6:
  `build_package.py` lists the registry file), comparator 5 of 5; `r7_cn_l_1.py` unit 8 of 8, seams 5 of 5, real 6 of 6. **The package-layout simulation (MEASURED offline, the issuer's
  fork, local Python, not the Lambda runtime):** the twelve members of `build_package.py`'s list that carry `lib/`, `infra/logic/registry/` and `org/standards/`, extracted from
  `9592daf75c` into a clean directory, resolve `legacy_address` for the three scopes; with `legacy_addresses.json` removed (the pre-amendment list) the same call raises
  `RegistryError: infra/logic/registry/legacy_addresses.json is absent from this package` (negative control). The Lambda runtime itself is exercised only by D4.

## 2. Deploy acts (one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | ONE named file, `dim_mdpf_aum_metrics.py`, through `safe-deploy.sh`; read back with `python .tools/mdpf-code-equality.py --files <it>` (exit 0) | `s3://opal-data-mdpf/code/scripts/gold/` | re-copy the key's prior VersionId, recorded before the copy (MEASURED now: ETag `201e85fd6fb817be2db2293d2cd4e775`, VersionId `QXLSI7ckDJQa.uzLD6_OK7h9RyVqC_F_`, written 2026-10-13T13:48:10Z) |
| D2 | `build_package.py --pin <pin>`, upload, ONE targeted `safe-apply` on `mdpf-gold-lambda` whose plan moves the function's code and the single environment value `MDPF_GOLD_COMMIT` (the full SHA of the pin built; edit `infra/aws/terraform/mdpf-pipeline/gold-lambda.tf`, the one value and its comment) and nothing else | the function | rebuild at the prior pin `51cfc93ea8`, restore `MDPF_GOLD_COMMIT` to the value printed before the act, apply the same target |
| D3 | NOT DEPLOYED: `dim_mdpf_aggregate_aua_timeseries.py` to `code/scripts/gold/` (see below); the emitter package; the staged runner objects; Stage 6; the publisher (CN-j-1's own order) | -- | none owed |
| D4 | the one on-demand `qa_local` invoke of `mdpf-gold-lambda`, after D2, graded on its response and a before/after read | the function | none: it writes no A4 object |

**Why D1 is ONE file and not the cell's two (the change from the round-6 shape).** `dim_mdpf_aggregate_aua_timeseries.py` is the runner's LIBRARY (`mdpf-daily-dispatch.sh:154-163`:
the spine imports it, both files are guarded at the sync) and, as of CN-h-1, it imports `lib.opal_naming` at module scope. The runner's code tree has six layers (`gold`, `backfill`,
`feeders`, `bronze`, `assets_gold`, `silver`, MEASURED from `safe_deploy_core.CODE_TREES["mdpf"]`), none of them `lib/`; the calendar reaches it as a flat `trading_calendar` sibling;
the round-7 code-sync read (`round7/CODE_SYNC_RUNNER_MEMBERS_READ.md` line 30) already keeps `taxsma_assets.py`, another `lib.opal_naming` importer, off the runner "only together with the
nine `lib/` and registry keys". Copying the new aggregate file to `code/scripts/gold/` would therefore make the runner's next dispatch fail at import (INFERRED from those facts;
**UNVERIFIED on the box**: the order's leg (a) records `/opt/mdpf` read-only to settle it). The gold LAMBDA does not need the runner copy: it runs from the package (D2). The consequence, stated:
`code/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` stays at its present bytes (ETag `eda145e92c44fc50f4bad6ff58a94c34`, VersionId `G8SX2Q15lLJNne61toc9OILO0CUyl6UI`, 2026-10-12T17:26:12Z) and
`mdpf-code-equality.py` keeps printing DIFFER for it; that is a listed fact of this deploy, not a defect to repair with a copy. `dim_mdpf_aum_metrics.py` adds no import, so its D1 is
safe on the runner by the file's own imports (MEASURED); the runner runs it as an entry (`--firm all --upload`, dispatch `:588`) over the STAGED artifacts, which carry no
`other_models` line (INFERRED from the round-6 acceptance item 5), so the new branch is not reached there.

**Sequencing.**
- Starts only on the issuer's written GO that today's (2026-10-14 13:30Z) fold fire was read and closed (the round-6 packet, `ROUND_ANALYSIS.round6.md`: FWD-3 REALIZED) and on both halves signed.
- Earliest start: now. Latest finish of D2 and D4: 12:44Z on 2026-10-15 (never within 45 minutes before the 13:30Z fire, never while the runner dispatch or the gold lambda runs: read the
  runner's status and the lambda's last invocation first). Today's fire has written its manifest (the fold's, 13:31:49Z, read by the issuer), so D4 has no wait.
- One change per scheduled fire: nothing else touches `mdpf-gold-lambda` or the `code/scripts/gold/` keys between this order's close and the 2026-10-15 13:30Z fire, which is the first fire
  that carries both cells and is attributable to this order alone. No sentinel under `org/critical_paths/.open_deploys/` names them (MEASURED by content search at drafting; the one
  filename match is `.unindexed_red_state.json`, a state record naming a 2026-08-19 completion, not a sentinel); the order re-reads at its start.
- In a gap between FIRMBKTS window acts (read `advi-firmbkts-*` first; `advi-firmbkts-fb-m-2-readiness-halt-deploy-20261014.json` is open at drafting). It touches none of the router, guard,
  CloudFront behaviours, `bronze_homes.json`, `firm-config.mjs` or the WAF rider (PRD v2.11 R2).

## 3. Writers of the properties

**P1: the frontier `account_count` of an overridden by_model line and the totals composed from it, in a served object. N = 7 distinct writer functions, recounted at `9592daf75c`:**

| # | writer | leaf it writes |
|---|---|---|
| W1 | `build_firm_timeseries` (`dim_mdpf_aggregate_aua_timeseries.py`; the override at the call to the loader) | ts `by_model[k].account_count[-1]` for 49financial and inflection |
| W2 | `build_global_artifact` (same file; the override) | the same leaf for global |
| W3 | `compose_count_total` (same file, called by W1 and W2) | ts `account_count_total` |
| W4 | `apply_global_min_firms_fold` (`mdpf_gold_consolidator.py`, CN-f-1) | the `other_models` count (the sum of the folded lines' counts) |
| W5 | `build_aum_metrics` (`dim_mdpf_aum_metrics.py`) | aum-metrics `by_model[].account_count` and `total.account_count` (global) |
| W6 | `build_firm_aum_metrics` (same file) | the same leaves for a firm scope |
| W7 | `emit_gold_parquet` / `mdpf_gold_parquet.records_for` | the gold parquet cells of the same fields (the long-form leaf projection) |

Each rule was read: W1 and W2 are the only ones whose INPUT changes; W3-W7 follow from them by the existing code. NOT writers of P1: `_shape_timeseries` (`mdpf_gold_consolidator.py:462-526`
sets `account_count_total` only when the artifact has none, which is the cottonwood path), `apply_sma_sleeve_overlay` and `_taxsma_by_model_entry` (the SMA and tax lines, not
overridden keys), `build_firm_distribution` (the A4 distribution itself: read here, never written), `build_partners` and `build_aum_timeseries` (the staged and the aum time-series objects).
A heuristic census over `data/mdpf/scripts/gold/*.py` flagged those functions as touching an `account_count` name; each was classified by its code, not by the census.

**P2: the Global aum-metrics `Other Models` row (`aum`, `account_count`, `q0..q3`, `as_of`). N = 2 builder functions:** `build_aum_metrics` (the only builder of that row: a firm scope never carries
`other_models`) and `records_for` (the long-form projection, which turns the new `as_of` key into one more `path/value` leaf, `by_model[i].as_of`, MEASURED by reading `_leaves`: no schema
change). The portal publisher then COPIES the gold body to the served plane (it compares sha256 of the served and gold bodies, `lambda_function.py:470`); it is not a writer of the row
(INFERRED from that read; **UNVERIFIED** for the platinum aum-metrics copy specifically).

## 4. Blast radius (what the act may touch)

- **Moves, from the first scheduled fire after D2 that mints a new date:**
  - CN-h-1, per scope: the last-date `account_count` of every overridden model line in the `aggregate-aua-timeseries` object (global 5 lines plus the composed `other_models`,
    49financial 5, inflection 6 of 7), its `account_count_total[-1]`, `meta.frontier_count.staleness` (as-of = the A4's own `period`; FRESH when equal to the frontier date), the aum-metrics rows'
    `account_count` and `total.account_count`, and the gold parquet cells of the same fields.
  - CN-l-1: only the Global aum-metrics `Other Models` row. On a pool-present day: NO change and NO `as_of` key. On a no-pool day within 4 calendar days: the row carries the last pooled
    day's value with `as_of`. Beyond 4 days: the row is absent.
- **Cannot move:** any dated object already served (write-once per key); any dollar or value field; cottonwood; category-views; the account-distribution objects (read here, not written);
  the SMA lines and `tax`; the staged `gold/mdpf_revamp/*` objects (the lambda no longer reads the staged distribution; the runner still writes the staged objects as before); the
  runner's behaviour (D1 is one file with no new import); the portal code (CN-i-1 and CN-l-2 are not landed).
- **State writes of a gold run (the C-S65 set):** the table in `round6/NEVER_WIDEN_PAIR_R6_CN_F_1.md` section 4 applies VERBATIM, as corrected at `@6d9ab2bd09`: the control key
  `mdpf/global/state/taxsma_control/current.json` is a plain overwrite (print its prior VersionId before D2); the staged aggregates are overwrites (prior VersionIds); the tax-prelude
  stores are creates or CAS appends keyed by knowledge date, EXCEPT the workbook snapshot, whose key carries the response sha256, so **D4 CREATES a new bronze and a new silver object under
  `gateway/global/{bronze,silver}/taxsma_workbook/date=<d>/` on every run** (two appeared on the round-6 dry run; additive, write-once, inert). The order lists them with VersionIds and treats their
  appearance as expected, and STOPS on a changed VersionId of any EXISTING object.
- **Measured baseline (read-only, 2026-10-14 ~16:0xZ):** function `mdpf-gold-lambda` `CodeSha256` `y69sfgPDowZbqwXAnE0XAA19+K2BMntmMjzqq5z3GdU=`, `LastModified` 2026-10-13T13:55:34Z, python3.11, timeout
  900 s, 3008 MB; `MDPF_GOLD_COMMIT` = `51cfc93ea84ac56ee6d14327125bfc53fc53c930`, equal to the value in `gold-lambda.tf:337`; environment keys `MDPF_GOLD_COMMIT`, `GOLD_WRITER_ROLE_ARN_{49FINANCIAL,
  COTTONWOOD,INFLECTION}`, `TAXSMA_CAPABILITY_SECRET_ID`, `TAXSMA_GATEWAY_BASE_URL`, `TAXSMA_PRELUDE_ROLE_ARN_{49FINANCIAL,COTTONWOOD}`; the package object
  `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` ETag `84fb7b0e7bfb129d76f36f864d3e595d`, VersionId `sZ6NZi49GhBLcekYxVfePaAgjHYn220H`, 1,842,371 bytes, 2026-10-13T13:51:35Z;
  schedule `mdpf-scheduled-floor` `cron(30 13 * * ? *)` ENABLED, input `{"floor":"mdpf-scheduled-floor","run_class":"production","source":"aws.events"}`.

## 5. Expected outcome, read from the rules (both branches of each)

**CN-h-1.**
- **An A4 exists at or before the axis** (measured today: 40 global, 47 49financial and 63 inflection dated keys; the newest of each is keyed 2026-10-14 with `period` 2026-10-14): for the
  2026-10-15 fire the axis is 2026-10-14, the loader selects the 2026-10-14 key, and each overridden key's frontier count equals that A4 map's value; `meta.frontier_count.staleness.as_of` is
  the A4's `period` and reads FRESH. If the newest qualifying key is older (a day whose own run wrote no A4) the verdict is STALE, never a refusal.
- **No A4 at or before the axis** (reachable only for an axis before 2026-07-28, a historical backfill; no live axis): the loader returns `{}`, the override does not run, the frontier count stays
  at its composed value. For 49financial that is the honest None it already carries; for global and inflection the cross-axis gate's clause (v) reads a None count beside a present value as a
  BUILD FAILURE, so that scope is refused whole by the existing gate and its prior object keeps being served. The CTO's "refuse the counts, honest absent" is, for global, the refusal of the
  Global scope that day by an existing gate, not a quiet None.
- **A failed read or an unparseable A4:** `C2-SIBLING FAIL-LOUD`: the scope's build raises and nothing is written for it. **An A4 whose `period` is absent or after the axis:** `{}` with a WARN, the
  no-A4 branch above.
- **The registry row or the package file is absent in the running package** (the failure class the amendment closed): `legacy_address` raises `RegistryError` inside the loader, which no C2 catch
  swallows, so every scope's timeseries build raises on the first fire. The offline simulation (section 1) shows the package list as built carries the row; **D4 is the only runtime proof
  before a scheduled fire**, and is kept for that reason.
- **The A4 map lacks a series key** (the blends and `other_models` after the fold): that line keeps its COMPOSED count.

**CN-l-1.**
- **The pool is present on the as-of** (the state on every fire so far since the fold; the pool is held by two firms): the row is served as today, no `as_of` key. This is the branch the first
  fire reads, so the first fire shows NO observable change from CN-l-1: its attribution is "key absent, row unchanged".
- **No pool on the as-of, a pooled date within 4 calendar days (inclusive):** the row carries that date's `aum`, its `account_count` at that date, the q-cells computed from the carried value
  unchanged, and `as_of` = that date. **No pooled date within 4 days, or never:** the row is absent from `by_model`, never a zero, never an older carried value.
- **A one-firm as-of** is CN-f-1's refusal: Global is refused whole before aum-metrics is built, so no Global aum-metrics object exists that day; the prior object keeps its own date.
  The QA drive of that branch (CN-n-1, merged `edd4f4f2f6`) read: Global refused whole with the `GLOBAL MIN-FIRMS FOLD REFUSED:` prefix, writes 0, 2886 served object-versions identical.
- **Branches (b) and (c) cannot be planted in production;** the offline arms (unit 8 of 8, real 6 of 6, which withholds the pool on the last 1, 2 and 5 dates of the real served object) are
  the exercised proof, and the organic no-pool day is the production negative arm.

## 6. Per-scope moves this pair accepts (priced; the first fire's own numbers are read from that fire)

MEASURED today, read-only: the 2026-10-14 A4 maps against the newest served timeseries (as-of 2026-10-13), over the keys the builder overrides.

| scope | overridden keys moved | frontier sum served -> A4 | the A4's own total |
|---|---|---|---|
| global | 5 of 5 (ultra_short 192 -> 215, short 841 -> 899, intermediate 2034 -> 2105, long_term_conservative 3476 -> 3717, long_term_aggressive 1431 -> 1469) | 7974 -> 8405 (+431) | 8430 (distinct accounts; the model counts overlap where an account holds two models) |
| 49financial | 5 of 5 | 7144 -> 7488 (+344) | 7488 (equal to the sum of the map) |
| inflection | 6 of 7 | 548 -> 565 (+17) | 565 (equal to the sum of the map) |

- **Two figures are NOT measured and are asked of the first fire:** (1) the Global `other_models` frontier count: the A4 reads 211 and the served timeseries 205, but the post-deploy value is
  the fold's own composition from the folded lines' counts, which the A4 map does not carry; (2) Global `account_count_total[-1]` (served 8264): the build's composition rule (section 7, F2) gives
  about 8264 + 431 = 8695 plus the `other_models` change, a PREDICTION, not a read. The comparator's earlier "8264 -> 8691 (+427)" was measured at axis 2026-10-13 against the unfolded 14-key A4 and is
  NOT the shape of the first fire.
- **Client-visible:** the per-model account counts and per-scope totals on the aggregate-aua-timeseries and aum-metrics objects: the Model Portfolios archetype cards' counts rise by the
  per-key deltas above; the Total Holdings headline reads the A4 distribution total and does not move; no dollar moves. `/portfolios` is partner-facing, so whether Andrew is told as information is
  the CTO's (he is told about the 2026-10-14 deltas in the round-6 analysis already).

## 7. Acceptance after the act (the issuer reads; never a leg of the CloudOps order)

On the first SCHEDULED fire after D2 that mints a new date (2026-10-15 13:30Z at the earliest), per scope, with denominators printed:
1. `python round7/checks/r7_frontier_readback.py read` (arms F1-F6): each overridden key's served `account_count[-1]` equals the newest A4 map keyed on or before the axis and none equals the
   stale staged value where the two differ (F1); `account_count_total[-1]` equals the composition the build defines, with the move and the A4-versus-staged delta printed (F2); every other date equals the
   prior object (F3); the staleness names the A4's own period and reads FRESH on equal dates (F4); the deployed loader's body names no staged key (F5); the headline arrays other than counts are equal (F6).
2. `python round7/checks/r7_cn_l_1.py real`: 6 of 6; and on the served Global aum-metrics object the `Other Models` row carries NO `as_of` key if the pool is present, else the carried date within 4
   days, else the row is absent.
3. The aum-metrics rows' `account_count` and `total.account_count` equal the timeseries' (the existing count-axis law).
4. The run manifest: `errors` empty, `a4_objects_built` 16, `run.code.commit` equals the pin (row D1-S18 read on this fire).
5. No staged `gold/mdpf_revamp/*/account_distribution.json` was requested by the run (the lambda log carries no read of it).
**S5 (MDPF_TAXSMA-S5) disarms on item 1; rows D1-W16-S2 and D1-W16-S4 disarm on item 2.** If a refused day occurs, `r7_frontier_readback.py refused --date D --expect-version V` reads the
prior object's VersionId before and after.

## 8. What the COO half asks the CTO half to read

1. Section 2, the change from the round-6 shape: D1 narrowed to `dim_mdpf_aum_metrics.py`, with the aggregate library kept off the runner. Is the runner-has-no-`lib/` reading right, and is
   leaving `code/` DIFFER for that file the ruling, or is the nine-key `lib/` sync window the route?
2. Section 5, the registry-row-absent branch and the no-A4 branch for global and inflection (a scope refusal by an existing gate, not a quiet None): is that the branch you ruled?
3. Section 6, the two unmeasured figures and the client-visible count deltas, and whether Andrew is told as information.
4. Section 3, N = 7 and N = 2, and that the staged object is unread; the stub-test grant (two one-line lambdas).
5. Section 2, D4: kept as the only pre-fire runtime proof that the package carries the registry row, with the workbook-snapshot creates named; or the order authorizes no on-demand run and the
   first fire is the first runtime.
6. The sequencing: one change per fire, the 12:44Z cutoff on 2026-10-15, and the FIRMBKTS gap.

## COO half -- SIGNED

`2.0.0_SA_COO~D1`, 2026-10-14 ~16:1xZ, on the bytes above: signed for the blast radius in section 4 (the per-scope frontier counts and the Global Other Models row from the first new-date
fire after D2; no dated object already served, no dollar field, no cottonwood, no category-views, no portal code), every branch in section 5 for both cells (the no-A4 branch is a scope
refusal by the existing cross-axis gate; a registry row or package file absent in the running package raises on the first fire and only D4 proves it before a scheduled fire; the
Other Models row is unchanged on a pool-present day), the rollback per key in sections 2 and 4 (each overwrite key's prior VersionId printed before the act; write-once keys are not
rolled back and nothing is deleted without a human), and the moves in section 6, with two figures stated as NOT measured (the Global `other_models` frontier count and
`account_count_total[-1]`, a prediction near 8695). On the conditions that the pin `9592daf75c` is an ancestor of origin's `box/dell1` before D1 (read 2026-10-14 ~16:1xZ: origin head
`2366d7dd25`), that the registry row `81453d51cf` and the package-list line are in the pin, and that the issuer's written GO precedes D1. D1 is narrowed to `dim_mdpf_aum_metrics.py`
on the issuer's reading that the runner has no `lib/` (INFERRED, UNVERIFIED on the box: the order's leg (a) records it read-only); that narrowing is put to the CTO half in section 8 item 1.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
