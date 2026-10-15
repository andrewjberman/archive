# MDPF_CANON round 10 -- never-widen pair for the ONE gold-package deploy that ships CN-r-1 (the Global Trend groups carry a missing Dividend, Growth or sleeve leg at its last known value ONLY where the carried row still partitions the served Total), for the 2026-10-16 13:30Z fire

**COO half SIGNED (see the end); CTO half OWED.** Drafted by a fork of `2.0.0_SA_COO~D1` on 2026-10-15 ~15:5xZ; every claim is MEASURED (read or run by the drafter in this session), INFERRED (read from code or a record, not run) or UNVERIFIED. Nothing here is deployed.
**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on `ADHOC.canon-r10-gold-carry-deploy` (draft beside this file).
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1`, to be recorded at `ledger/NEVER_WIDEN_R10_GOLD_CN_R_1_CTO_HALF.md`; COO half = this lane.
**Reused by reference, unchanged since the round-9 pair (`round9/NEVER_WIDEN_PAIR_R9_CN_P_1.md`):** the SMArtX loader and its three branches (present / absent in 10 days / denied -> Global refused alone), the state-write table of `round6/NEVER_WIDEN_PAIR_R6_CN_F_1.md` section 4 (as corrected at `@6d9ab2bd09`), the leaf list of a gold run (21 writes), the gold parquet families, and the CN-h-1/CN-l-1 field sets of the round-7 pair sections 3, 4 and 6. This file states only what CN-r-1 changes.
**Rulings this pair carries:** PRD v2.22 overrides (c) and (d); the CTO's msg 6047 (one generalized rule: a missing leg carries its last known value ONLY IF the carried row still partitions the served Total within 0.011; the date joins `carried_dates` only when a leg actually carried); the CTO's round-9 condition (msg 5934) restated for this change: a leaf-by-leaf table, the combined blast radius and the rollback per change (section 4).
**Code:** CN-r-1 merged `b6352de8f8` (the drain merge of `wk-MDPF_CANON-29`; worker commit `7606f9b678`; order `task-orders/MDPF_CANON.TO-CN-r-1.producer-carry-missing-trend-legs.md`, complete). Issuer's criteria re-run by the drafter on the merged tree: `round10/checks/r10_cn_r_1.py` pure 11 of 11, seams 4 of 4, oracle 11 of 11; `round9/checks/r9_cn_p_1.py` pure 7 of 7, seams 7 of 7, oracle 7 of 7 (CN-p-1 stays green); `pytest data/mdpf/tests/canon` + the stratid test: 53 passed. AC4 is a JUDGMENT criterion, ungraded.
**Pin:** `b6352de8f843f3726ad5c51c650d9035ca8336db` (`b6352de8f8`, the CN-r-1 drain merge), or a descendant carrying the 46 package members below byte-equal to it. **Push state: at the drafter's read (~15:4xZ) it was LOCAL only; RE-MEASURED by the issuer at signing (fetch, `merge-base --is-ancestor`): `b6352de8f8` is an ancestor of origin's `box/dell1` `4339774d12`: on origin @4339774d12 (ls-remote read).** The order's precondition (b) can hold.

## 1. Code

- **What CN-r-1 changes** (`data/mdpf/scripts/gold/mdpf_gold_consolidator.py`, +59/-9, hunks only at the `SMARTX_LOOKBACK_DAYS` constants and `compute_trend_groups`; MEASURED by `git diff -U0 8e2dd0fb36 b6352de8f8`):
  - New constants `TREND_CARRY_LEGS = ("div", "growth", "sma")`, `TREND_IDENTITY_TOL = 0.011`; three pure helpers `_leg_present` (None and NaN are absence; 0.0 is a value), `_partitions(row, key, cand)` (true when `total - model_aua - (Client Supervised + ETF + ALT) - gaetr` is within the tolerance with leg `key` at `cand` and every other leg at its own value, 0.0 when absent; no `model_aua` -> false), `_leg_carry(last, key, raw, row)`.
  - `compute_trend_groups`: on a TOTAL-BEARING row a missing Dividend, Growth or `sma_additive_aua` carries its last known value only if the carried row still partitions the served Total; the Total is READ, never recomposed; each leg is decided alone; forward only (never before a leg's first value); `gaetr` is never carried; one memory per leg across the 2026-05-18 boundary; a pre-boundary date with no SMArtX row is skipped as before; a row with no `model_aua` carries nothing; the date joins `carried_dates` only when a leg actually carried. ETF now adds the decided sleeve value, not `sma[i] or 0.0`. Rows with no total keep today's group-level roll-forward; ALT is unchanged.
  - NOT changed: `apply_global_trend_groups`, `load_smartx_sma_legs`, `build_all` (so the Global-refused-alone branch is as in round 9), the key set, `meta.trend_groups`, `point_class`, any existing key.
  - `data/mdpf/tests/canon/test_global_trend_groups.py`: +78 lines (the eight CN-p-1 tests untouched; not shipped).
- **The package (`build_package.py`, unchanged since the round-9 pin: blob-equal) carries 46 members; between the round-9 pin `8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f` and `b6352de8f8` THREE differ (MEASURED, blob compare of every member path):**

| member | change | class |
|---|---|---|
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | CN-r-1 | the cell |
| `infra/logic/registry/legacy_addresses.json` | 169 -> 179 rows: +10 (all reader `NFRA_OPLGTW`), **0 removed, 0 changed** by `key`; none concerns MDPF or SMArtX | ADDITIVE DATA; no row the lambda reads moved |
| `infra/logic/registry/reporting_policies.json` | one policy gains the `FILLED_REPORT` family (`filled_report.json`, from `df2468cbc8`, IRPT_BCKEND) | ADDITIVE DATA, read by the naming library only (INFERRED: nothing in the gold path reads `reporting_policies`) |

  The other 43 members, including `lib/opal_naming.py`, `exemptions.json` and `mdpf_category_registry.py`, are blob-equal to the round-9 pin. MEASURED at HEAD (which contains `b6352de8f8`): `lib.opal_naming.validate()` returns `([], [])`. The order's leg (b) re-reads all of this at the pin.
- **PROBE D (the DELTA on the REAL served object, MEASURED 2026-10-15 ~15:3xZ; `pair_r10_cnr1/delta_probe.py`, read-only AWS GET of one SMArtX partition):** the round-9 `compute_trend_groups` (`8e2dd0fb36`) and the merged one (`b6352de8f8`) were run over the SAME real inputs: the served Global `aggregate-aua-timeseries/2026-10-14.json` (VersionId `NjIWJXhM2mzItcQje9le3ys_9T6KQA5s`, 497 dates, last 2026-10-14, written by the 2026-10-15 13:31Z fire at commit `8e2dd0fb36`) and the SMArtX partition `2026-10-15` (1,285 dates, the partition that fire read: `meta.trend_groups.smartx_partition`). Result: **each of the three arrays differs from the SERVED array in 0 of 497 cells for BOTH versions, and `carried_dates` equals the served list (the 9 no-total dates) for both: DELTA = 0. The full Global object `apply_global_trend_groups` returns (every key, `meta.trend_groups` included) is equal to the served Global object, and the old and new outputs are equal to each other. `compute_trend_groups` does not mutate its input (asserted).** Why nothing moves: the sleeve has its first value 2026-08-26 and is missing on 7 total-bearing dates (2026-08-31, 09-01, 09-02, 09-03, 09-04, 09-08, 09-09); the Total excludes it there (the issuer's O1 and my run agree), so the sleeve stays absent and those dates are NOT named in `carried_dates`. Dividend and Growth have no gap in the series.
- **The first-fire readback on today's served objects (MEASURED):** `round10/checks/r9_trend_groups_readback.py read --pin 8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f` reads **11 of 11 arms PASS** against the real newest objects (R11: no leg lost on 2026-10-14 vs 2026-10-13).

## 2. Deploy acts (one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | the ONE named file `mdpf_gold_consolidator.py` through `safe-deploy.sh`, ONLY IF the order's leg (g) reads the runner has no `lib/` and no runner module imports it; else NOT deployed and `mdpf-code-equality` keeps printing DIFFER for it (a stated fact) | `s3://opal-data-mdpf/code/scripts/gold/` | re-copy the key's prior VersionId |
| D2 | `build_package.py --pin <pin>`, upload, ONE targeted `safe-apply` on `mdpf-gold-lambda` whose plan moves the function's code and the single environment value `MDPF_GOLD_COMMIT` and nothing else | the function | section 4 |
| D3 | NOT DEPLOYED: every other `code/` name; the emitter; the publisher | -- | none owed |
| D4 | the one on-demand `qa_local` invoke of `mdpf-gold-lambda`, after D2, graded on `errors` empty and `a4_objects_built` 16, and on the 16 served objects and 5 overwrite keys byte-equal to their baseline | the function | none: it writes no served object |

- **D1 precedent (MEASURED in the round-9 ledger `20261014T2242Z_mdpf-canon-r9-gold-trend-groups-deploy-dell1-20261014_deploy_completion.md`, leg L2):** D1 was NOT DONE under leg (g)(i) (the runner `i-02448edb624a7a7cf` was STOPPED; the read path unavailable). `mdpf-code-equality` reads DIFFER for `mdpf_gold_consolidator.py` and `mdpf_category_registry.py` today (MEASURED 2026-10-15); this order expects the same outcome and may not "repair" it with a copy unless leg (g)(iii) clears.
- **Sequencing.**
  - Starts only on (i) the CTO half signed, (ii) the COO half signed, (iii) the issuer's written GO naming a pin that is ON ORIGIN and carries `b6352de8f8`.
  - **Window: D2 and D4 finish by 12:44Z on 2026-10-16** (never within 45 minutes before the 13:30Z fire, never while the runner dispatch or the gold lambda runs). The 2026-10-15 fire has run (manifest `_manifests/2026-10-14/20261015T133154Z.json`: `errors` {}, `a4_objects_built` 16, `run.code.commit` `8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f`, MEASURED), so the 2026-10-16 13:30Z fire is the FIRST fire to carry CN-r-1 and is attributable to this order alone.
  - **One change per fire holds.** CN-r-2's deploy (`ADHOC.canon-r10-publisher-latest-read-deploy`, DRAFT) is an IAM policy on the publisher's role (`opal-assets-mdpf-egress-publisher-role`, Terraform root `opal-assets`): it touches neither `mdpf-gold-lambda`, nor a gold-package member, nor a gold object, nor `code/scripts/gold/`; it first acts at the 13:50Z publisher run, which only COPIES the gold bodies this order's fire writes. The two orders share no surface and take separate ledgers and windows (the round-7 lesson: two acts never share one window). The E4 reader order is read-only.
  - No open deploy sentinel names `mdpf-gold-lambda` or `code/scripts/gold/` (the order re-reads `org/critical_paths/.open_deploys/` in every live worktree at its start).

## 3. Writers of the property (classified by reading the code at `b6352de8f8`)

**P1: the keys `client_supervised_aua`, `etf_strategies_aua`, `alt_strategies_aua` and `carried_dates` of the Global `aggregate-aua-timeseries` object. N = 3 writers, unchanged from round 9 (2 rules, 1 projection):**

| # | writer | what it writes |
|---|---|---|
| W1 | `compute_trend_groups` (`mdpf_gold_consolidator.py`) | the VALUES of the three arrays and `carried_dates`, Global only. **The ONLY writer of the moved values**; CN-r-1 changes its body |
| W2 | `apply_global_trend_groups` (same file) | creates the keys on every scope (all-None / `[]`) and merges W1's output into Global (unchanged) |
| W3 | `emit_gold_parquet` -> `mdpf_gold_parquet.records_for` | the three arrays as parquet columns (`carried_dates` is not projected) (unchanged) |

The new helpers `_leg_present`, `_partitions` and `_leg_carry` are pure predicates and a pure selector: they return values into W1 and write nothing. NOT writers: `_shape_timeseries` (pass-through), the dated put, the staged runner objects (written before the wiring), the publisher. **MEASURED recount at HEAD:** a search of `data/`, `infra/`, `lib/` and `.tools/` for the four key names finds the consolidator, its test, and `infra/aws/ec2/opal-gateway/app/etfs_ownership.py`, which defines an unrelated `_carried_dates` helper and a `carried_dates` field in an ETF-ownership response body (a different service and object): no second producer of the MDPF keys. N = 3 as before.

## 4. Leaf-by-leaf disjointness vs everything else in flight, the combined blast radius, rollback per change

Leaves a gold run writes (21, MEASURED in the newest manifest): per scope `account-distribution`, `aggregate-aua-timeseries`, `aum-metrics`, `category-views`; the four staged `gold/mdpf_revamp/*` objects; the control key; plus the gold parquet families `account_distribution`, `account_units`, `aggregate_aua_timeseries`, `aum_metrics`.

| leaf / surface | CN-r-1 can move | what else is in flight on that leaf | intersection |
|---|---|---|---|
| Global `aggregate-aua-timeseries` | the VALUES of `client_supervised_aua`, `etf_strategies_aua`, `alt_strategies_aua` and the membership of `carried_dates`, on a date with a leg gap only. **On today's data: nothing (PROBE D, 0 of 497 cells)** | nothing: CN-h-1/CN-l-1 (count fields) and CN-p-1 (the key set) are deployed and fired on 2026-10-15; CN-r-1 adds no key, so the round-9 table (R10: the four keys share no top-level key with the count fields) holds unchanged | EMPTY |
| 49financial / inflection / cottonwood `aggregate-aua-timeseries` | nothing (all-None / `[]`, set by W2, unchanged) | nothing | EMPTY |
| `aum-metrics`, `account-distribution`, `category-views` (4 scopes each) | nothing: they do not read the four keys (round-9 PROBES A and C, MEASURED then; `compute_trend_groups` is the only changed function and `build_all` is unchanged) | nothing | EMPTY |
| gold parquet `aggregate_aua_timeseries` (Global) | the same three columns' cells on a gap date; carried_dates is not a column | nothing | EMPTY |
| other parquet families, staged `gold/mdpf_revamp/*`, control key, tax-prelude stores | nothing (staged objects are written before the wiring) | nothing | EMPTY |
| the publisher role / publisher run (CN-r-2) | nothing | an IAM policy on `opal-assets-mdpf-egress-publisher-role` (Terraform `opal-assets`), first acts at the 13:50Z publisher run | no shared surface |
| edge `auth-validator-edge` (CN-q-1), portal (CN-p-2), E4 reader measure | nothing | other functions or read-only | no shared surface |
| run manifest | `run.code.commit` | the same stamp field moves with any deploy | not a content leaf; one writer |

**Verdict: the CN-r-1 field set is disjoint from every other change in flight on every leaf, and on today's data CN-r-1 moves no byte at all.**
**Combined blast radius at the 2026-10-16 13:30Z fire:** with no leg gap in the 2026-10-16 inputs, NOTHING served changes (DELTA = 0, PROBE D) beyond the new as-of date's ordinary append and `run.code.commit`. With a leg gap on a total-bearing row, only the Global three arrays' cells of THAT row and `carried_dates` can differ from the round-9 rule; the three firm scopes, aum-metrics, category-views, account-distribution and every headline field (`opal_aggregate_aua`, `model_aua`, `non_model_aua`, `point_class`, every `by_model` value) cannot move.
**Cannot move:** any dated object already served (write-once per key); any dollar or headline field; any other scope; the portal, publisher, emitter, edge.

**Rollback PER CHANGE.**
- **CN-r-1 only** (round 7 and round 9 stay): (1) edit `gold-lambda.tf` `MDPF_GOLD_COMMIT` back to **`8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f`** (the round-9 pin: it carries CN-p-1 and CN-h-1/CN-l-1 and NOT CN-r-1: `7606f9b678` is not an ancestor of it, MEASURED both ways); (2) restore the package object `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` to VersionId **`EUjzb4a1tilUgNty3PZKo5D6ISVFlyFY`** (ETag `24e4303b3c518ea9aa050c2151ec256d`, 1,943,696 B, written 2026-10-14T22:46:30Z, MEASURED live now; the round-9 package: zip sha256 `00452e5b288c1fb8da5eaf0f09bc490810832dfff3738227304ef79a8567ee43`, 45 modules, 46 members per the `.tf` comment) as the CURRENT version (copy-object by version id onto the same key, or `build_package.py --pin 8e2dd0fb36`); (3) plan + ONE targeted `safe-apply` on `mdpf-gold-lambda`; the function's `CodeSha256` returns to **`AEUuWyiMH7jaXq8PCbxJCBCDLf/zc4InME73moVn7kM=`** (the pre-D2 value, MEASURED live now); (4) re-copy the D1 key from its recorded VersionId if D1 ran.
- **Further back** (not this order's step unless the issuer's message names it): CN-p-1 as well = `9592daf75c7469d212242cd63850c735f6f53238` with package VersionId `ueXrxiM.u9Fves_JXUJO037JmTm9Yj.R`; rounds 7 and 9 = `51cfc93ea84ac56ee6d14327125bfc53fc53c930` with `sZ6NZi49GhBLcekYxVfePaAgjHYn220H`.
- **Write-once objects** (every dated served object, every parquet partition, the manifest) have no prior version and are not rolled back. A bad first object is answered by the issuer's readback, the code revert above and the next fire's new date; never a delete. The overwrite keys' prior VersionIds are in section 6.

## 5. Expected outcome, read from the rule (both branches, plus the SMArtX branch)

- **Branch A, a leg is missing on a total-bearing row AND the Total contains it** (the carried row partitions within 0.011): the leg carries its last known value; the groups are computed from the carried leg; the row's date joins `carried_dates`. For Dividend and Growth the test always passes while the sleeve is right (they cancel between Client Supervised and ETF), so they carry whenever they have had a value.
- **Branch B, the leg is missing AND the Total excludes it** (or the carried value is too far from the leg's true value on that row): the leg stays ABSENT (reads 0.0 as before), the date is NOT named. This is today's real state for the sleeve on 2026-08-31..09-09.
- **No `model_aua` on the row:** nothing carries (fail closed). **A leg that never had a value:** never carried. **`gaetr`:** never carried.
- **SMArtX branches (unchanged from round 9):** partition present -> the pre-2026-05-18 legs from it; none in 10 days -> `({}, None)`, a WARN, pre-boundary groups stay None, green; denied or failed -> `C2-SIBLING FAIL-LOUD`, Global refused ALONE. A pre-boundary date with no SMArtX row is skipped as before.
- **PLANTED-gap statement (MEASURED on the real 2026-10-14 object, copies only, `delta_probe.py`):** (1) a Dividend deletion on the newest dated row, the Total unchanged (it contains the Dividend): round-9 rule dips Client Supervised and ETF by **$17,166,726.07** each; the CN-r-1 rule carries the previous day's Dividend, the groups differ from the true values by only **$22,869.74** (the Dividend's day-over-day move; the two errors cancel, the Total still partitions), and `2026-10-14` joins `carried_dates`. (2) A sleeve deletion on the same row, the Total unchanged: the carried (yesterday's) sleeve differs from the true one by **$355,920.93**, far outside 0.011, so the carry is REFUSED, ETF dips by the whole sleeve (**$765,078.34**, same as round 9) and no date is added. (3) The sleeve deleted AND removed from the Total: absent, same dip, no date. **On the first fire the readback therefore shows:** with no gap, R5 equal and R11 "no leg lost" (today's reading); with a carried Dividend/Growth gap, R11 PASS "CARRIED by the producer" naming the date, R3, R4 PASS; with a refused gap R11 reads FAIL "Branch B for CN-p-1/CN-r-1" and names the leg: that is the designed alarm for a leg lost, not a producer defect.
- **The limit stated (the ruling as worded, section 8 item 1):** because the Total contains the day's TRUE sleeve value, a stale carried sleeve passes the 0.011 test only if the sleeve did not move; real sleeve values move daily, so the sleeve almost never carries (planted case 2). The rule's practical effect is on Dividend and Growth, for which the test is a guard that cannot fail.

## 6. Per-scope moves this pair accepts (priced) and the baselines

**Moves: none on today's data (PROBE D).** No scope's served bytes change because of CN-r-1; the new as-of date's own append and `run.code.commit` move regardless of this order.
**Baseline of the latest served objects (MEASURED 2026-10-15 ~15:3xZ; the order re-reads them in leg (a)).** `VersionId` under `s3://opal-data-assets/portal/gold/mdpf/`:

| scope | aggregate-aua-timeseries | category-views | aum-metrics | account-distribution |
|---|---|---|---|---|
| global | `2026-10-14` `NjIWJXhM2mzItcQje9le3ys_9T6KQA5s` | `2026-10-14` `Ymz0SOWjuaLsIy7AJ.D6_sUav9Y7yxfi` | `2026-10-14` `IDjO5TszYeEW4BzY9gGSonmf2dhIgEoj` | `2026-10-15` `THTt9LuIRIMwc0Jfi2s7zlOQy7EvljxW` |
| 49financial | `2026-10-14` `5x__ienTHagiUofeTN.WJNELrJyruWSd` | `2026-10-14` `c3OJLM2.MejmXi3Xf8oxn7Gfmaxf2Zlk` | `2026-10-14` `Er.4q6zEd.JjLkXJmuGAhxqhiTlUOgU9` | `2026-10-15` `b2WfV40v06G4eGYrsp7E1tv6LicmO8Z.` |
| inflection | `2026-10-14` `YQJJZypsgIjl839oEzIlCibi7O1LM2eN` | `2026-10-14` `6yohfAmf9vHGeqqSU95JcT3mpBPM7r_P` | `2026-10-14` `ZCfq7F.o7Xfv5BtV9s2rhiVhITFz23LG` | `2026-10-15` `b3MnSEQMSJqj5AqbCprGrhFDZvu7uwmE` |
| cottonwood | `2026-10-14` `ZddlHckHDbRRcROx6aaIZQH76Lm5xd3T` | `2026-10-14` `SO6hfPjk2_Fg9l5ioWPTM2Y0Y25_Wax.` | `2026-10-14` `qKECAhmAFFPgK5TuaVyDLIhGCW86E2Qw` | `2026-10-14` `ZfCmbTfMQshQp8AvjdqwUnjngk4u4Ekg` |

**Overwrite keys of a gold run and their prior VersionIds (MEASURED, last written 2026-10-15T13:31Z; they move at the next scheduled fire regardless of this order):** `opal-data-assets/gold/mdpf_revamp/global/aggregate_aua_timeseries.json` `hp.Il_pELvOefdBZ8weug8vf1dmv0B4W`; `.../49financial/aggregate_aua_timeseries.json` `klZStrAS5T6_xygOn.j44CcC07B1uzma`; `.../inflection/aggregate_aua_timeseries.json` `T4tnzVock8CNFxT7moO9TGahbonfUXmW`; `.../global/non_model_assets.json` `G7gZG5plEkRJ00iRcR_tqbhym3PB3fGH`; `opal-data-mdpf/mdpf/global/state/taxsma_control/current.json` `Ss7ckX5S9FvnU7keHFwhGcCRTYN3f3zh`. The round-6 C-S65 table applies verbatim; D4 writes none of them.
**Measured baseline of the function (2026-10-15 ~15:3xZ):** `mdpf-gold-lambda` `CodeSha256` `AEUuWyiMH7jaXq8PCbxJCBCDLf/zc4InME73moVn7kM=`, `LastModified` 2026-10-14T22:49:55Z (the round-9 deploy), python3.11, timeout 900 s, 3008 MB; `MDPF_GOLD_COMMIT` `8e2dd0fb369043d5f23dca2d02dba7d51cfabd6f` (equal to `gold-lambda.tf:357`); package object ETag `24e4303b3c518ea9aa050c2151ec256d`, VersionId `EUjzb4a1tilUgNty3PZKo5D6ISVFlyFY`; schedule `mdpf-scheduled-floor` `cron(30 13 * * ? *)` ENABLED, input `{"floor":"mdpf-scheduled-floor","run_class":"production","source":"aws.events"}`. The SMArtX read has now run in the real runtime under the lambda role: the 2026-10-15 13:31Z fire read the `2026-10-15` partition (`meta.trend_groups`), `errors` {} (MEASURED), so the round-9 IAM simulation is confirmed by an exercised read.

## 7. Acceptance after the act (the issuer reads; never a leg of the CloudOps order)

On the first SCHEDULED fire after D2 (2026-10-16 13:30Z), denominators printed:
1. `python round10/checks/r9_trend_groups_readback.py read --pin <pin>` (11 arms). **Read-before-use finding (MEASURED):** the committed copy's R5 still requires `carried_dates` to EQUAL the no-total dates, so a CORRECT carry (Branch A) makes R5 FAIL (planted Dividend gap on the real object carried by the merged code: R3, R4, R6, R11 PASS, **R5 FAIL**, 9 of 11 with the local-mode R9). A drafted amendment is beside this file: `r9_trend_groups_readback.R5_amended.py` (`r5_check`: carried_dates must contain every no-total date and may add only total-bearing dates on which a leg is missing after its first value; a refused gap adds nothing and is not required). Tested: the real 2026-10-14 object 11 of 11; the planted carried gap R5 PASS and R11 PASS; a negative plant (an extra carried date with no leg gap) R5 FAIL. The issuer replaces the committed copy with it before the fire.
2. The aggregate-timeseries Global object: the three arrays equal the round-9 rule's reading of the same inputs unless a leg gap is named in `carried_dates`; every pre-existing key equals the prior day's rule; `opal_aggregate_aua`, `model_aua`, `point_class` byte-equal on the shared dates.
3. The run manifest: `errors` empty, `a4_objects_built` 16, `run.code.commit` equals the pin.
4. `/seams` on the producer-to-served seam for AC4 (JUDGMENT).

## 8. What the COO half asks the CTO half to read

1. **Section 5, the limit:** the sleeve carry is almost inoperative under the ruling's test (a stale sleeve fails 0.011 whenever the sleeve moved; measured $355,920.93 day-over-day on 2026-10-14). The ruling's intent ("carry where the Total contains the leg") and its mechanism (carry where the carried value reproduces the Total) coincide only for Dividend and Growth. Accept as built, or order the enrichment that compares the Total's implied sleeve (the residual `total - model_aua - non_model...`) rather than the stale value.
2. **Section 7 item 1:** the R5 amendment.
3. **Pin:** `b6352de8f8` is on origin (`4339774d12`, re-measured at signing); the GO can name it.
4. **Section 1, the package:** two riders (`legacy_addresses.json` +10 rows of another reader, `reporting_policies.json` +1 family), both additive; `validate()` clean.
5. **Section 2:** one change per fire holds (CN-r-2 is the publisher role, not the gold lambda).

## COO half -- SIGNED by 2.0.0_SA_COO~D1, 2026-10-15 ~16:0xZ

Read in full. Re-measured by the issuer at signing: `b6352de8f8` is an ancestor of origin `box/dell1` `4339774d12` (rc 0); live `mdpf-gold-lambda` CodeSha256 `AEUuWyiMH7jaXq8PCbxJCBCDLf/zc4InME73moVn7kM=`, `MDPF_GOLD_COMMIT` `8e2dd0fb36...`, LastModified 2026-10-14T22:49:55Z; DELTA probe re-read by the issuer in the drafter's output; readback on today's objects with the amended R5: 11 of 11. Signature is this line in the commit by `2.0.0_SA_COO~D1`.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
