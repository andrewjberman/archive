# MDPF_CANON round 6 -- never-widen pair for CN-f-1: the Global min-firms fold (a per-model Global line is shown on a date only where at least two firms hold it)

**COO half SIGNED** by `2.0.0_SA_COO~D1` at the foot of this file; **CTO half OWED**. Drafted by a fork of the issuer on 2026-10-12 ~19:0xZ and read
in full by the issuer before signing (the Code, Deploy, Writers, Blast radius, Branches, Deltas and Acceptance sections). Nothing here is deployed.

**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on `ADHOC.canon-r6-fold-deploy` (draft beside this file), which the issuer cuts after this pair is signed on both
halves and after its own written GO that W8-S4 is closed.
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1` (MDPF_CANON owner), to be recorded at `ledger/NEVER_WIDEN_R6_CN_F_1_CTO_HALF.md`; COO half = this lane.
**Status:** COO half SIGNED (issuer); CTO half OWED.
**Rulings this pair carries (all in `org/tier1_exec/1.0.0_SA_CTO/deliverables/RECORD_FE9B_RULED_BY_CLUSTER_LEAD_20261012.md`):** the cluster lead's ruling (A)
and ADDENDA 1-6; the round-5 analysis `ledger/ROUND_ANALYSIS.round5.md` section 2 (C-S65) and section 3 item 3 (D1-S18).
**Code:** CN-f-1 is merged on box/dell1 at `51cfc93ea8` (order `task-orders/MDPF_CANON.TO-CN-f-1.global-min-firms-fold.md`, status complete, AMENDMENT 1 =
ADDENDUM 6). The issuer re-ran the three criteria on the merged tree: contract 13 of 13, comparator 11 of 11, seams 6 of 6.

## 1. Code

- **Pin:** `51cfc93ea8` (the drain merge), or a later commit that carries the five files below byte-equal to it. The pin is LOCAL until box-sync carries
  it: it must be an ancestor of origin's `box/dell1` (`git ls-remote`, then `git merge-base --is-ancestor`) before D1.
- **What changes** (all under the cell's grant):
  - `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`: `apply_global_min_firms_fold(arts, firm_scopes, min_firms=2)` and
    `guard_global_min_firms_fold(arts, isolated)`, called in `build_all` directly after `guard_global_served_identity` (`:2942-2943`):
    `arts, fold_report = guard_global_min_firms_fold(arts, _isolated)`. A refusal sets `arts["global"]` to None and records `manifest["errors"]["global"]`.
  - `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py`: `build_firm_distribution(..., fold_keys=None, fold_emit=True)`; the global call passes the
    fold set. The CLI the runner executes passes no fold, so the STAGED global account-distribution stays unfolded.
  - `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`: `other_models` last in `MODEL_ORDER` and in `SERVED_MODEL_NAME`.
  - `data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py` and its byte-equal twin
    `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/mdpf_revamp_model_crosswalk.py`: one `CANONICAL_MODELS` row and one
    `GLOBAL_ACCOUNT_DIST_DISPLAY` entry for `other_models` (no model id, no eclipse id, not served, not core).
  - `data/mdpf/tests/canon/test_global_min_firms_fold.py` (new; not shipped).
- **The rule as built (ADDENDA 1-6):**
  - held = a firm's own `model_value > 0` on that date; the fold set is computed from the firm scopes' objects on every run, never a list;
  - per date, a model-class line held by fewer than two firms goes to the pool; the pool is emitted as `other_models` only where two or more firms
    hold it; the dollars that leave are suppressed, never redistributed (D1 = (b), per date);
  - the differential identity `(model_aua - sum(model-class lines))` after minus before equals the suppressed dollars, to the cent, on every valued
    date, fail closed; the 208 of 485 dates that already carry a $0.01-0.02 rounding residual are carried, not tripped over;
  - flips are REPORTED and never refused on; every emitted line, the fold line included, is held by two or more firms on its date;
  - the SMA lines (`opal_div_sma`, `opal_growth_sma`, `pfde`) and `tax` are untouched (D2);
  - a day whose as-of pool is held by fewer than two firms refuses Global WHOLE (ADDENDUM 6): views, aum-metrics and distribution together, never
    partially; the firm scopes build; the prior Global object keeps its own `as_of`; the refusal is printed in the build output with no alarm.
- **Measured on the real objects, 2026-10-09 as-of (issuer's comparator, read-only):** fold set 11 model-class lines (9 held by one firm, 2 by none);
  5 of 5 kept lines carried; `other_models` emitted on the as-of and on 47 dates, not shown on 438 of 485 valued dates; per-model detail begins 2026-05-15;
  identity checked on 485 dates, 0 gaps.
- **Evidence:** `r6_cn_f_1.py contract` 13 of 13 (C11 a planted one-firm as-of refuses Global while the firm scopes are the same objects; C12 a two-firm
  as-of builds and a no-pool as-of builds; C13 a refused day hands back no Global document and does not mutate the input), `seams` 6 of 6,
  `r6_cn_f_1_comparator.py` 11 of 11 (K1-K10 on the real served objects). C11-C13 grade the functions `build_all` calls, not `build_all` itself, as the
  CN-d-1 arm A6 did.

## 2. Deploy acts (one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | the four gold scripts, NAMED FILES ONLY, through `safe-deploy.sh`; read back with `python .tools/mdpf-code-equality.py --files <the four>` (exit 0) | `s3://opal-data-mdpf/code/scripts/gold/` | re-copy each key's prior VersionId, recorded before the copy |
| D2 | `build_package.py --pin <pin>`, upload, then ONE targeted `safe-apply` on `mdpf-gold-lambda` whose plan moves the function's code and the single environment value `MDPF_GOLD_COMMIT` (set to the full SHA of the pin actually built; row D1-S18), nothing else; read back the deployed package's BUILD_MANIFEST (four sha256 equal the pin's) and the function's environment | `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` -> `mdpf-gold-lambda` | rebuild at the prior pin `0d39789fdf`, restore the prior environment value printed before the act, apply the same target |
| D3 | NOT DEPLOYED: the emitter package `opal-assets-daily-emitter` is not touched. Its crosswalk twin lands as repo parity (committed != deployed, the 650df7371e precedent) | -- | none owed |
| D4 | the one on-demand `qa_local` invoke of `mdpf-gold-lambda` (the handler's documented dry-run key, `mdpf_gold_consolidator.py:3318`), AFTER the same day's scheduled fire has completed; graded on its response and a before/after read | the function | none: it writes no A4 object (see section 4) |

**Why the emitter is not an act.** `channel_sources.py` uses the vendored crosswalk for the rmid bridge, the eclipse-id map and `CORE_MODEL_KEYS`
(`:45`, `:297`, `:314-318`, `:415`); the new row is id-less and not core, so none of those inputs move. The emitter reads
`gold/mdpf_revamp/_aggregate_aua/{date}.json` (`emitter.tf:225-231`), never a served Global object. `mdpf_category_registry.py`, whose import-time check
is the reason the row exists, is not in the emitter package (`BUILD_MANIFEST.json` package_modules). The gold package's crosswalk is the
`data/mdpf` copy (`build_package.py:142`). A later emitter deploy carries the twin and changes no emitter output; the order reads the emitter's
`CodeSha256` before and after as a control.

**Sequencing.**
- Starts only on the issuer's written GO that W8-S4 (CN-d-1's served-key read on the 2026-10-13 13:30Z fire) is closed. CN-d-1's ledger
  `mdpf-canon-r4-code-deploy-dell1-20261012` already reads CLOSED; both orders name `mdpf_gold_consolidator.py`, and two acts never copy one key in
  one window.
- Never within 45 minutes before the 13:30Z fire, never while the runner dispatch or the gold lambda is running, and D4 only after that day's fire has
  written its manifest.
- One change per scheduled fire: nothing else touches `mdpf-gold-lambda` or the `code/scripts/gold/` keys between this order's close and the next
  13:30Z fire, so the first folded fire is 2026-10-14 13:30Z at the earliest and is attributable to this order alone.
- In a gap between FIRMBKTS window acts (read its ledgers first). The order touches none of the router, guard, CloudFront behaviours,
  `data/mdpf/config/bronze_homes.json`, `firm-config.mjs` or the portal-auth WAF rider (PRD v2.11 R2).

## 3. Writers of the property (N = 8, recounted at HEAD @51cfc93ea8)

The property is a model-line leaf of a Global served object. Eight distinct writer functions across seven leaf classes:

| # | writer | leaf class it writes |
|---|---|---|
| W1 | `build_global_artifact` (`dim_mdpf_aggregate_aua_timeseries.py`, iterates `GLOBAL_MODEL_KEYS`) | ts `by_model`; ts `meta.by_model_channels` |
| W2 | `apply_taxsma_overlay` (`mdpf_gold_consolidator.py:1757-1818`) | ts `by_model` (the `tax` line) |
| W3 | `apply_sma_sleeve_overlay` (`:1995-1996`) | ts `by_model` (sleeve members); ts `sma_additive_withheld[]` |
| W4 | `apply_global_min_firms_fold` (`:2227-2249`) -- NEW | ts `by_model` (removes folded lines, adds `other_models`); ts `meta.by_model_channels`; ts `meta.by_model_fold` |
| W5 | `build_aum_metrics` (`dim_mdpf_aum_metrics.py:514-607`) | aum-metrics `by_model[]` |
| W6 | `build_firm_distribution("global", ...)` (`dim_mdpf_account_distribution.py:484-547`) | account-distribution `by_model{}`; `meta.account_count_by_model_key`; `meta.cottonwood_fold.by_model_folded` |
| W7 | `_shape_category_views` -> `registry.build_category_views` | category-views Models > Custom and SMA members |
| W8 | `emit_gold_parquet` / `mdpf_gold_parquet.records_for` | the global gold parquet partitions (wide ts, long others) |

Each rule was read: W1-W3 are unchanged and run BEFORE the fold; W4 is the only writer this cell adds; W5-W8 are downstream readers of the folded
document and shape it by the existing code (W5 and W6 gain the fold arguments, W7 is unchanged). The earlier design read's "N = 8" counted the
writer-by-leaf pairs of the pre-fold tree; this count is distinct functions at HEAD, with the fold the eighth. Not a Global-labelled leaf:
`mdpf_aggregate_aua.py` (`_aggregate_aua`) keys `by_model` under each partner by `firm_id`; the ruling's property is the Global label.

## 4. Blast radius (what the act may touch)

- **Moves, from the first NEW-DATE scheduled fire after D2 onward:** the four global served objects of that date
  (`portal/gold/mdpf/global/{aggregate-aua-timeseries,aum-metrics,account-distribution,category-views}/<date>.json`) and the global gold parquet
  partitions of that date. Per object: `by_model` loses the folded lines and gains `other_models` (where held by two firms); `meta` gains
  `by_model_fold` and the folded `by_model_channels`; every top-level key set is equal to the prior object's; no new top-level key.
- **Cannot move:** any firm scope's object; the staged `gold/mdpf_revamp/*` aggregates and distributions (they are written UNFOLDED by design, row
  `D1-W16-S5`: the staging write precedes the guard and the runner's CLI passes no fold); the headline arrays (`model_aua`, `non_model_aua`,
  `tax_additive_aua`, `sma_additive_aua`, `opal_aggregate_aua`, `account_count_total`, `count_as_of`, `point_class`); any dated key already served
  (the A4 writer is write-once per key: the 135 served global objects keep their one-firm lines, no retro-fold, the reader read found no served reader
  of a pre-fold dated object); the SMA lines; `tax`.
- **Does not move:** the portal code, the emitter lambda, the runner schedule, the router/guard/behaviours.
- **The on-demand invoke (D4) is a dry run, not a zero-write run.** `qa_local` skips the A4 puts, the manifest, the A7 partition, the staging writes, the
  parquet and the tax control (`mdpf_gold_consolidator.py:2817`, `:2837`, `:2847`, `:2928`, `:3188`, `:3240`). It does NOT pass `dry_run` into the tax
  prelude (`_taxsma`, `:2884-2909`), whose four durable stores are S3 conditional creates or a CAS append keyed by knowledge date
  (`taxsma_snapshot.py:166`, `taxsma_workbook.py:184`, `taxsma_membership.py:626`, `taxsma_assets.py:707`). Run after the same day's fire, each store
  already holds that date, so the writes are no-ops; the order reads each store's VersionId before and after and stops on any change.
  **CORRECTION (2026-10-13, issuer, after the dry run):** "each store already holds that date, so the writes are no-ops" was wrong for the workbook
  snapshot. Its object key carries the response sha256, so each acquisition writes a NEW bronze and silver object under
  `gateway/global/{bronze,silver}/taxsma_workbook/date=<d>/`; the dry run created two at 2026-10-13T13:58:14Z (row D1-S20), as the fire (13:31:42Z)
  and CN-d-1's real run (2026-10-12 17:32:49Z, on the code before this order) did. They are additive, write-once and nothing served reads them
  differently; the existing objects, the dispositions, the gold assets and the control key kept their VersionIds. The blast radius is unchanged.
- **STATE WRITES OF A GOLD RUN, named per the CTO's C-S65 ruling** (every pair that authorizes an on-demand run names them; this is the first and closes
  C-S65). A scheduled or non-dry-run gold run writes these; D4 does not, except where marked:
  | key class | writer | write rule | rollback |
  |---|---|---|---|
  | `mdpf/global/state/taxsma_control/current.json` (address from `taxsma_operational_control_key()`; printed by the order, never typed) | `taxsma_put_control` (`:1203`) | plain overwrite each run when Tax ran; `process_time` moves | prior VersionId printed before D2 |
  | `gold/mdpf_revamp/{49financial,inflection,global}/aggregate_aua_timeseries.json` | `stage_put` (`:2821`, `:2838`) | overwrite | prior VersionId |
  | `gold/mdpf_revamp/cottonwood/*` family objects and `nma.STAGING_KEY` | `run_cottonwood_family`, `_detail` (`:2874`) | overwrite | prior VersionId |
  | `gold/mdpf_revamp/_aggregate_aua/<date>.json` | `agg.write_s3` (`:2852`) | write once per date; skipped on a reconciliation ERROR | none (write-once) |
  | tax prelude stores: bronze snapshot, silver, disposition history, gold assets | the four S3 stores (D4 touches these) | create-if-absent / CAS append | none for creates; the disposition history's prior VersionId |
  | taxsma category gold parquet | `write_taxsma_category_gold` (`:2292`) | write once per knowledge date | none (write-once) |
  | A4 objects, gold parquet partitions, run manifest `_manifests/<as_of>/<ts>.json` | `conditional_put`, `emit_gold_parquet`, `put_object` | write once per key | none (write-once); a conflict is recorded, never overwritten |
  The order prints every key it can read from the run manifest and the prior VersionId of each overwrite key before D2; where a key is write-once there
  is no prior version and the rollback is not to run again.

## 5. Expected outcome, read from the rules (all branches)

- **A two-firm as-of, identity holds** (the measured state of the 2026-10-09 objects): the run completes; each global object differs from a
  hypothetical unfolded build of the same date by exactly the folded lines, the `other_models` line and the `meta` keys named in section 4; headline
  arrays equal; `manifest["errors"]` empty; 16 of 16 A4 objects built.
- **The as-of pool is held by fewer than two firms** (not seen on any served object; the pool is held by two today): `apply_global_min_firms_fold`
  raises `GLOBAL MIN-FIRMS FOLD REFUSED:` naming the as-of date and the firm count, no level; Global is refused whole; the three firm scopes build and
  write exactly as in a control run; no Global object of any type is written that run; the prior Global object stays served with its own `as_of`; the
  refusal is printed in the build output; `manifest["errors"]["global"]` carries it; no alarm, no notifier (moratorium). The next day that holds two
  firms builds normally. The issuer files a row; the guard is not loosened.
- **The differential identity fails on a date** (not seen): the same refusal, naming up to five dates and a difference to the cent.
- **A malformed line array or an unclassified line:** the same refusal, naming the key and the fact.
- **A fault inside the fold:** the isolation records it and refuses Global alone; siblings unchanged.
- **The sidecar older than the declared window or the cross-axis gate refuses Global (CN-d-1's guards):** unchanged from today; the fold is not reached.

## 6. Client-visible deltas this pair accepts (ADDENDA 3, 4 and 5; Andrew is told as information, `/portfolios` is partner-facing)

- The Model Portfolios page: Total Holdings -185 and the archetype cards -$43.16M in all (the two inflection blends no longer roll into the cards);
  no new JSON key is added (the page's "durable fix" is not made).
- Per-model trend lines begin 2026-05-15 on the core lines; before it Global carries no per-model lines, only its headline, and says why in band
  (`meta.by_model_fold.statement`, which names no model).
- The `other_models` line is suppressed on 55 dates where inflection alone holds it ($26.1M to $58.6M, at most 2.79% of the headline).
- 10 of the 20 core-model aum-metrics quarter cells on the 2026-10-09 object are absent (q2 2026-03-31, q3 2025-12-31): the existing honest-None
  state, the same history the trend loses.
- The SMA tree keeps serving `by_firm` per member by Andrew-direct ruling; the fold does not touch it.

## 7. Acceptance after the act (the issuer reads; never a leg of the CloudOps order)

On the first SCHEDULED fire after D2 that mints a new date (2026-10-14 13:30Z at the earliest), read the four served global objects of that date and
the global parquet partitions, with the denominators printed:
1. no model-class `by_model` line, `other_models` included, is held by fewer than two firms on any date it carries a value (read from the firm scopes'
   objects of the same date);
2. headline arrays equal the same date's firm-composed expectation and equal the prior served object on every shared date; every top-level key set equal
   to the prior object's;
3. the differential identity holds on every valued date, with the pre-existing residual printed against its denominator (208 of 485 on the
   2026-10-09 object);
4. `meta.by_model_fold` is present, states the first per-model date, and names no model; no folded line's key or display name survives anywhere in
   the global objects;
5. the three firm scopes' objects of that date are unchanged from a control; the staged `gold/mdpf_revamp/*` objects carry no `other_models` key;
6. the run manifest: `errors` empty, `run.code.commit` equals the pin (row D1-S18 read on this fire), the gold parquet status carries no new error;
7. **the CTO's third arm (ADDENDUM 6 item 4) as a read-back, only if a refused day occurs:** the prior Global object's VersionId read before and after
   that run is the same, and its `as_of_last` is the prior date. A refusal cannot be planted in production; the offline arms C11-C13 are the exercised
   proof and the read-back is the negative arm's, graded when the organic case arrives.
The issuer's read-back script is `round6/checks/r6_fold_readback.py` (`read --date D`, `refused --date D --expect-version V`, `selftest`): nine arms R1-R9 over items 1-6 above; its selftest folds the real 2026-10-09 objects offline with the merged fold function and reads R1-R6 PASS, with three planted defects each RED on the arm named; its live read on today's unfolded objects fails R1, R2, R7 (as expected), R3 (the unidentified_strategies padding drift between 10-08 and 10-09, which the 10-13 object already carries) and R9 (D1-S18, the stamp mismatch). R7 and the `refused` arm are exercised only live. The comparator's real-object arm (`r6_cn_f_1_comparator.py`) is a PRE-deploy instrument: it applies the fold to today's
unfolded served objects; run on a folded object it would fold the fold line again.

## 8. What the COO half asks the CTO half to read

1. This file, sections 3 and 4: the N = 8 recount at `51cfc93ea8` and the named state writes (C-S65), including that D4 is a dry run and not a
   zero-write run.
2. `mdpf_gold_consolidator.py` from `apply_global_min_firms_fold` to `guard_global_min_firms_fold` and the call at `:2943`: the refusal at the as-of
   happens before any output is built.
3. `ledger/ROUND_ANALYSIS.round5.md` section 2 and ADDENDUM 6: whether D4 as written (one `qa_local` invoke after the day's fire, stores read before and
   after) satisfies "every pair that authorizes an on-demand gold run names every routine state write", or whether the order should authorize no
   on-demand run at all and rely on the scheduled fire alone.
4. Section 7 item 7 and section 6: the refusal branch's read-back and the deltas.
5. The sequencing in section 2 (W8-S4 closed first; one change per fire).

## COO half -- SIGNED

`2.0.0_SA_COO~D1`, 2026-10-12 ~19:4xZ, on the bytes above: signed for the blast radius in section 4 (the four global served objects and the global gold
parquet partitions from the first new-date fire; no firm scope, no staged object, no dated key already served), every branch in section 5 (a one-firm
as-of refuses Global whole, a fault or an identity miss refuses Global alone, flips are reported and never refused on), the rollback per key in
sections 2 and 4 (each overwrite key's prior VersionId printed before D2; write-once keys are not rolled back and nothing is deleted without a human),
and the deltas in section 6, on the conditions that the pin 51cfc93ea8 is on origin before D1 (ls-remote read 2026-10-12 ~18:5xZ: origin box/dell1 head
51cfc93ea8) and that the issuer's written GO that W8-S4 is closed precedes D1. One change per scheduled fire: the first folded fire is 2026-10-14 13:30Z
at the earliest.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
