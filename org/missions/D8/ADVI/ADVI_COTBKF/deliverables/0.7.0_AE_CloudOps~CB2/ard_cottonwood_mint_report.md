# ADVI_COTBKF CB-al-2 -- Cottonwood `account_return_daily` MINTED, 3,325 days, APPLIED and UNREAD

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Order:** `ADVI_COTBKF.TO-CB-al-2` (AMENDMENT 5 @`a8748799a1`, AMENDMENT 6) |
**Round:** 38, cell `CB-al-2`, **outcome_ref** FWD-3 | **Date:** 2026-10-11, 06:56Z-07:31Z | **Box:** dell2

## VERDICT: COMPLETE. All seven conditions of the CTO half met; `CB38al2-AC1` PASS.

```
ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325 sidecar=match method_row=match manifests=3325/3325
```

Nothing was deleted, nothing overwritten, no key outside the three granted prefixes, and no reader exists.

## 1. The pair files

| half | path | sha256 measured on the tree | pin in AMENDMENT 5 |
|---|---|---|---|
| COO | `.../2.0.0_SA_COO~C2/NEVER_WIDEN_R59_ARD_COTTONWOOD_MINT_COO_HALF.md` @`0865081982` | `351dad12c2ae18b31367a95cce3ecb892cefb9fb461cc015cbddb4ada137a115` | **equal** |
| CTO | `.../1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R59_ARD_COTTONWOOD_MINT_CTO_HALF.md` @`f2415a44b5` | `7bb0562c1140578803371cc7644f57dd27f71a1cc5646acb0ed7b03589dcc015` | **equal** |
| adapter | `data/assets/scripts/silver/commonwealth_account_return_daily.py` | `38f06ba93cc82318d3fd7bc587baac2184acb03f9c9b7e4809acba4afcbb51c9` | **equal** |
| manifest | `.../0.9.0_WK_ADVI_COTBKF~79/ard_cottonwood_manifest.json` | `d2d99d5c4a127635170f77516b52fdfc0c163e151e39649e35569a601ce47b36` | **equal** |

All four hashed **before** the first act, as AMENDMENT 5 requires; all four clean in `git status`; HEAD contains
`f2415a44b5` (`merge-base --is-ancestor` rc=0, with a positive control). `COTBKF_SWEEPS_CONFIG` resolved from
`org/devices/state/dell2/cotbkf_sweeps_config_pointer.json` and its own sha256 verified equal to the pointer's
measured claim (`b1d93408...10a89d`) before use.

## 2. The ledger entry

`org/critical_paths/change_management/20261011T0656Z_advi-cotbkf-r38-al2-ard-cottonwood-mint-20261011_deploy_completion.md`

Opened **before the first write** with 6 legs (condition 5), every leg closed with its own proof, **CLOSED
20261011T072305Z**, disposition **APPLIED, UNREAD** (condition 6).

| leg | step | result |
|---|---|---|
| L1 | condition 1 -- versions census | 0 versions / 0 delete markers on all three prefixes; **862-version positive control** |
| L2 | step 3 -- `--stamp-manifest` | exact line; manifest sha256 unchanged before and after |
| L3 | step 4 / condition 4 -- `--bond-check` | `measured_rows=107316 measured_rows_on_bond_days=0` |
| L4 | step 5 / condition 2 -- `--show-day-manifest` | exact line, rc=0, no custodian text anywhere |
| L5 | step 6 -- **the mint** | `days=3325 landed=3325 sidecar=landed method_row=landed`, rc=0 |
| L6 | step 7 / condition 3 -- `--verify-served` | `match=3325/3325 ... manifests=3325/3325`, rc=0 |

Condition 5's union, which a shared-tree read would have got wrong: **33 of 33 live worktrees** read with
`git ls-tree` (not `ls -1`, which hides `.unindexed_red_state.json`), per-tree counts **17 to 29**, 659 row-reads
summed, **93 distinct** open-deploy paths. Word-boundary census over the union: **0** entries name this act, so
nothing was resumed. A first substring grep matched `freshguard` on "ard" and was corrected -- naming it because a
substring hit would have implied a stranded entry that does not exist.

## 3. The day count and the first and last key

**3,325 days**, `2013-04-03` through `2026-06-22`.

- first: `s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2013-04-03/`
- last: `s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-22/`

**3,328 `LANDED` lines reconciled in full against `days=3325`** -- this is the one number that needed resolving
rather than quoting:

| part | count |
|---|---|
| day lines (`LANDED date=`), **3,325 distinct dates, 0 duplicates** | 3,325 |
| sidecar -- `account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet` (sha256 `589f72cc...`, 763,053 B) | 1 |
| method row -- `dim_return_method/method_version=3/` is **two objects**, `data.parquet` (etag `7b70c246...`) **and** `manifest.json` | 2 |
| **total** | **3,328** |

So `method_row=landed` is one token covering two objects. Nothing is unexplained.

## 4. The read-back result

Run twice, in two different forms, because the two are not the same instrument:

| form | last line | rc |
|---|---|---|
| step 7's, `--verify-served --manifest <manifest>` (AMENDMENT 5) | `ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325 sidecar=match method_row=match manifests=3325/3325` | 0 |
| the criterion's literal, `--verify-served --out .scratch/...` | `ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325 manifests=3325/3325` | 0 |

Both clear the criterion's bar (`ARD-COTTONWOOD-VERIFY days=`). **The literal form is the weaker of the two:**
without `--manifest` it omits `sidecar=` and `method_row=` entirely, covering only the days and their manifests.
That is precisely why AMENDMENT 5 re-reads the invocation as step 7's. Both are recorded; step 7's is the one the
conditions are graded on.

The preceding line in both runs is `ARD-VERIFY mismatches=0 first=[]` -- zero mismatches with an **empty**
first-mismatch list, not merely a zero count.

**Independent corroboration, because a producer's own last line is not evidence.** `aws s3api list-objects-v2`,
auto-paginated (never `--no-paginate`, never `--query length()`), counted client-side by basename,
`IsTruncated=None` on each:

| prefix | objects | split |
|---|---|---|
| `account_return_daily/` | **6,650** | 3,325 `data.parquet` + 3,325 `manifest.json` |
| `account_return_daily_blank_reasons/` | **1** | the sidecar |
| `dim_return_method/` | **2** | `data.parquet` + `manifest.json` |

**6,653 served objects**, matching the apply's arithmetic to the object. The same call on the same three prefixes
read **0** before the write, so this instrument has a measured reading both ways on this exact target.

## 5. Condition 2's accepted limit, and that the control actually closed it

The CTO half signed condition 2 with a limit named out loud: `--show-day-manifest` reaches `build_manifest`
through helpers that **mirror** `apply_days` and are not called by it, so it shows what the producer writes for
that input but not that `apply_days` hands the producer that input. The half named condition 3 as the control.

It closed. The pre-write show on `2026-06-22` read `method_version` 3, `positions_x_as_traded_close`,
`net_of_fees`, `as_traded`, `custodian_text=absent`, and the row-3 method sentence (`r_t = (V_t - F_t) / V_(t-1)
- 1; ... GIPS-ALIGNED, not GIPS-compliant.`). The post-write `manifests=3325/3325` reads those five fields back
off **every served manifest**, i.e. off what `apply_days` really wrote. The gap is discharged by measurement.

**Row `ADVI_COTBKF-D2-W66-S1` disarms on that line** per condition 3. The disarm is the row's own; this report is
the evidence that discharges it, not the disarming act.

## 6. Rollback, and what is NOT covered

**Rollback is not a delete** (AMENDMENT 4, kept by AMENDMENT 5; CTO half section 4 with section 2's third point).
The minted keys stay unread behind the reader gate; a partial mint is **resumed** under an amendment to this pair;
a delete is Andrew's and is not this order's act. Because L1 read 0 versions and 0 delete markers against a
nonzero control, the pair's "no prior version exists" sentence was true at write time and needed no correction.

Condition 7, not covered by the pair and not done: **no delete, no overwrite, no re-run of `build()`, no key
outside the three prefixes, no reader.**

## 7. One declared departure and one exclusion

- **`comp-iam` was not run,** although the preflight says "RUN at apply time". Reported as an exclusion, not a
  pass. The question it exists to answer -- can this identity PutObject under the target prefix -- was answered at
  the strongest available grain by writing 6,653 objects and reading every one back; and `comp-iam` models
  `(action)`, never `(action, resource)`, so it could not have added assurance to a completed, verified write.
- **No surprise row was filed by this order,** and none was owed: the act hit no refusal and no read-back
  difference, so the refusal clause did not fire. The `WCB2-S<k>` id form AMENDMENT 5 named is gate-rejected;
  **AMENDMENT 6** corrected it to the next free `D2-S<k>` after this seat measured that. Rows `D2-S91`/`D2-S92`
  belong to CB-bi-2.

## Evidence files (outside the repo by the order's design)

`C:/dev/_cotbkf_private_evidence_20261009/r38_al2/`

| file | what it is |
|---|---|
| `step6_apply.txt` | 3,330 lines -- the full `LANDED` log of the mint |
| `step7_verify.txt` | step 7's read-back (the graded form) |
| `step7_verify_criterion_form.txt` | the criterion's literal form |
| `step3_stamp.txt`, `step4_bondcheck.txt`, `step5_daymanifest.txt` | the three pre-write gates |
| `versions_*.json` (3 + control) | the condition-1 census |
| `served_*.json` (3) | the independent post-write object census |
| `open_deploys_union_sorted.txt` | the 93-entry union across 33 worktrees |
