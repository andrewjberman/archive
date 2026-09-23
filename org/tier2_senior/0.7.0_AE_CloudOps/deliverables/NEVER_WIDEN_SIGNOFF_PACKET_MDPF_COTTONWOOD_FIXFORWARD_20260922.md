# NEVER-WIDEN SIGN-OFF PACKET -- mdpf-gold-lambda Cottonwood auto-custom FIX-FORWARD (pin 5991626d4f), THREE LEGS

**For:** `1.0.0_SA_CTO` and `4.0.0_SA_CRO` (both LIVE at write time, roster read 14:4xZ; `2.0.0_SA_COO~F` signs the
CRO half in its stead only if the CRO goes dark -- Andrew-direct 2026-09-11 ~05:3xZ).
**Prepared by:** `0.7.0_AE_CloudOps~V`, 2026-09-22 ~14:5xZ. **Nothing is applied by this packet.**
**Authority:** Andrew-direct at the `0.7.0_AE_CloudOps~V` terminal 2026-09-22 ~13:4xZ, verbatim: *"Then yes, we need
to fix forward, we need to identify the source of the break. If it is a float issue, or if it is a wrongly structured
pull with regard to the counts, or if it is something to do with how the custom models (the unexpected "Opal*" model
additions) are being processed. Whatever the case may be, we need to render the necessary fix/fixes, deploy, and issue
a manual run. When this is done, ping me, I will visual smoke, and return with feedback."* Prior authority for the
Cottonwood deploy itself: MSTR records @`0b46309ec2` / @`1ab93ec740` (*"~V Does work, CRO and CTO signs off"*, *"Sign
first, then push"*). The CTO's stated requirements for its half: msg 99490 items (1)-(3); the CRO/CTO LEG B card
(99492/99494) is answered by the fix-forward direction above unless Andrew's relayed word says otherwise.
**Method:** MINIMAL PIN over the running vintage `48b8671569` (08-26 doctrine), never HEAD. The pin branch
`hotfix/mdpf-cottonwood-autocustom-20260921-cto` is RETAINED (the tf stamp cites it).

A half signs the BLAST RADIUS and the rollback per key, BOTH branches of every named outcome -- never an intention.

**AMENDED ~15:2xZ on `4.0.0_SA_CRO`'s refusal of s.6 (@`3a9e95a335`, s.1/s.3/s.7 sign-ready):** s.6 now carries the
THREE in-process Cottonwood staging writers the real invoke runs before any portal key (C-stage rows, with the
`adate` the invoke writes and the current VersionId of every key they rewrite, all read at ~15:1xZ); the reachability
sentence is corrected to FOUR prefixes; s.3 names the CRO's third reachable branch (cottonwood `category-views`
ABSENT); s.7 step 4 reports per-scope ABSENTs by name. No other section changed. Both halves are asked against the
NEW blob.

---

## 0. THE THREE LEGS, EXACTLY

| leg | act | who performs it | what it writes |
|---|---|---|---|
| **A** | upload the pin-built zip; commit `MDPF_GOLD_COMMIT`; `safe-apply -target=aws_lambda_function.mdpf_gold` | `0.7.0_AE_CloudOps~V` | 1 S3 object version + 1 Lambda (code + one env var) + 1 repo literal |
| **B** | the CLOUD push of `ac571ef0c7`; its safe-deploy pre-push hook syncs the ONE changed `data/*/scripts/gold/*.py` to its S3 code prefix | `0.0.0_AB_MSTR` pushes (shared-branch law), the hook syncs | 1 key on `opal-data-mdpf` (s.5) |
| **C** | ONE real (non-qa_local) manual invoke of `mdpf-gold-lambda`, then ONE manual invoke of `opal-assets-mdpf-portal-publisher` -- Andrew's *"issue a manual run"* for his visual smoke | `0.7.0_AE_CloudOps~V` | gold keys under `s3://opal-data-assets/portal/gold/mdpf/` and the serve keys under `s3://opal-data-portal-v2/platinum/mdpf/` (s.7) |

LEG C is a SERVED-OUTPUT act and is why this packet exists as a never-widen sign-off rather than a deploy note. The
2026-09-23 13:30Z scheduled fire then runs the same pin; it is the standing acceptance and is covered by the same halves.

---

## 1. WHAT BROKE, WHAT WAS MISREAD, WHAT THE FIX IS

**The 12:53Z qa_local crash on the 74d7efe144 build was a DRY-RUN VINTAGE-PIN ARTIFACT, not a production-fire
prediction.** `run_cottonwood_family`'s `dry_run` branch reads back the newest LANDED gold dim partition (09-18) instead
of staging today's, so under an axis that runs to 09-21 the cottonwood value series carries a trailing `None`. Two
LATENT readers then failed on that shape; the production branch stages today's partition first and does not produce it.
This seat recommended the rollback on that crash (99479) and it was executed 13:25Z on Andrew's *"Go"*; the 13:30Z fire
on the restored `48b8671569` wrote 8 of 16 -- the pre-deploy behaviour, not a recovery. Owned to Andrew and to the CTO /
COO~B (99513/99514); surprise row `MDPF_COTREMEDIATION-S20` carries the full record. **Custom (`Opal*`) model
processing is NOT a cause** -- the crosswalk WARNs for the candidate-NEW name (`eclipse_id=31`) fold it to non_model
exactly as designed, on every build read.

**Reader (1) -- the float issue Andrew named.** `_shape_category_views` did `float(v[-1])` on the trailing `None` and
raised, taking the whole run down before any S3 write. **Andrew's own 2026-09-11 null-tail guard already fixes this on
CLOUD (`1465fd3f7d`: `_last` returns `None`, the scope is WITHHELD, never zero-filled) -- but the Lambda has never run
it:** `git merge-base --is-ancestor 1465fd3f7d 48b8671569` -> not an ancestor, so the 09-15 pin predates it, and the
09-21 minimal pin inherited the gap. The fix-forward pin carries it (cherry-pick @`3756c846a4`, conflict resolved to
the 09-11 text verbatim). Battery `tests/test_category_views_null_tail_guard.py` (6 arms incl. mutant + positive
control) **6 of 6 on the pin.** NEW INFORMATION for both signers: the deployed plane has lacked this guard for a week.

**Reader (2) -- the count-structure issue Andrew named.** `_cot_roll_forward_map` skipped every date in `cot_covered`
unconditionally. A date whose COUNT partition has landed but whose VALUE has not (the measured 09-21 shape) was left
`value=None` beside a real count, and the global fold's cross-axis coherence gate (v) refused GLOBAL. Fixed to skip a
covered date only when its value is present, otherwise roll forward from the latest measured-with-value source exactly
as an uncovered gap does; counts are never carried (Andrew-ruled semantics unchanged). Hotfix `47e00fa9ad`; on CLOUD
`ebd2370ee9`, drained @`ac571ef0c7`. `tests/test_frontier_lag_trailing_none.py` arm 2: 4 cases with the OLD loop
inline as the negative control, **5 of 5** (arm 1 asserts the measured shape WITHHOLDS under reader (1)'s guard).

Regression on the pin: `test_cross_axis_membership_domain.py` all pass; `test_global_fold_flag2.py` **21 of 24 -- the 3
failures reproduce identically on the UNMODIFIED `74d7efe144` spine** (stale windowed-carry expectations:
`test_carry_within_window_carries_and_labels`, `test_carry_beyond_window_absent_for_real`,
`test_carry_source_is_measured_never_interpolated`). Pre-existing, not touched, disclosed so nobody reads them as new.

---

## 2. LEG A -- THE PIN AND ITS DELTA AGAINST THE RUNNING BUNDLE (CTO item 1 for the Lambda)

**RUNNING, measured this turn (14:3xZ), not carried from the rollback ledger:**
```
mdpf-gold-lambda  CodeSha256 evIYCXURor4V++Ci4HsgwE8zIPZva/BAL+ICaLJIiAE=  CodeSize 835,383
                  LastModified 2026-09-22T13:25:35Z  MDPF_GOLD_COMMIT 48b8671569b72efb4eca64ef41ded4de9c54e84c
                  State Active / LastUpdateStatus Successful  timeout 900 s  memory 3008 MB  python3.11
artifact  s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip
          latest VersionId uYOduyR_y0a0IH8bEnA8Lukn4qQRzcAR (835,383 B, 13:22:47Z -- the rollback copy of
          9GsracvIPvfBMzF1dttMpew0TkQtt.qg, sha256 7af218097511a2be15fbe0a2e07b20c04f3320f66f6bf0402fe20268b2488801)
          prior: D2JGWfiLUUYQ8Tczmz_BktSrYHV_koZe (868,952 B, the 09-21 Phase A+B upload, now non-latest)
```

**BUILD PIN `5991626d4f4e583383a2dba09927c2a319463fec`** = the 09-21 pin `74d7efe144` (signed by both of you, packet blob
`2c59f07389`) **+ 4 commits**, on the same retained branch:

| pin commit | what | CLOUD equivalent |
|---|---|---|
| `47e00fa9ad` | reader (2) fix in the spine; first cut of the arm tests | `ebd2370ee9` (spine hunk byte-identical) |
| `3756c846a4` | cherry-pick of Andrew's 09-11 null-tail guard (reader 1) + its test file | `1465fd3f7d` |
| `5991626d4f` | arm tests retargeted onto the carried guard (tests only; not packaged) | `ebd2370ee9` |

**THE BUILT ZIP:** `build_package.py --pin 5991626d4f` -> **872,699 B, sha256
`e5a28d1f9581bda84c43cddf63425a34c8ce96aa2aea90803491d588b445c194`**, import-closure gate PASS (19 `.py`), in-zip
`source_vintage.commit` = `5991626d4f...`, config hashes == running. File: `.scratch/mdpf_cot/built_fix2.zip`. **This
exact file uploads; it is not rebuilt between signing and upload.**

**MEMBER-BY-MEMBER vs the RUNNING (rolled-back) bundle:** 24 vs 23 members. ADDED 1 `mdpf_name_discovery.py` (as in
the signed 09-21 pin); REMOVED 0; UNCHANGED 17; CHANGED 6:

| member | vs running | what |
|---|---|---|
| `build_cottonwood_mdpf_slice.py` | +128 / -8 | Phase A+B, unchanged from the signed 09-21 pin |
| `build_cottonwood_mdpf_pair.py` | +46 / -6 | Phase A+B, unchanged from the signed 09-21 pin |
| `mdpf_revamp_model_crosswalk.py` | +19 / -29 | Phase B, unchanged from the signed 09-21 pin |
| `dim_mdpf_aggregate_aua_timeseries.py` | +23 / -6 | Phase B (+17/-6, signed) **+ reader (2) fix (+6 / 0)** |
| `mdpf_gold_consolidator.py` | +50 / -5 | Phase B (+4/-1, signed) **+ reader (1) guard, the 09-11 text (+46 / -4)** |
| `BUILD_MANIFEST.json` | +17 / -12 | vintage stamp |

vs the superseded fix build `47e00fa9ad`: only `mdpf_gold_consolidator.py` and the manifest differ. Both spine and
consolidator in the zip are byte-equal to `git show 5991626d4f:<path>` (checked, 2 of 2).

---

## 3. OFFLINE DRY-RUN OF THE BUILT BYTES (outside the repo tree, zero S3 writes)

`lambda_handler({"qa_local": true, "qa_return_bodies": true})` on the extracted `built_fix2.zip`, 14:25Z-14:27Z, 83 s:
**15 of 16 A4 objects, bodies returned for 49financial / inflection / cottonwood (4 of 4 each) and global (3 of 4).**
The 16th, `global/account-distribution`, is refused by the `COTTONWOOD SIDECAR STALE -> ABSENT` gate because
`gold/mdpf_revamp/cottonwood/account_units.json` reads value_date 09-15 -- and under dry_run the pair never refreshes
that sidecar (it writes it only under `--upload`). Both readers pass on the measured shape: cottonwood's
`category-views` is EMITTED (the 09-11 guard withholds only when the LATEST cell is null, and the offline vintage pins
one behind, so it is not) and GLOBAL `aggregate-aua-timeseries` is EMITTED (reader 2's carry lets the fold cohere).

⛔ **qa_local IS NOT VINTAGE-FAITHFUL FOR COTTONWOOD** (row S20): it cannot show what the production branch will write
for cottonwood on a day whose partition has not landed, and it cannot refresh the sidecar. So LEG C's real invoke has
TWO reachable outcomes and the halves cover both: **16 of 16** if the pair's `--upload` lands a sidecar inside
cottonwood's 3-trading-day window (its holdings value_date is 09-18 = 2 trading days behind 09-22), or **15 of 16** with
`global/account-distribution` ABSENT if it does not -- the gate refusing as designed, a wider window never the fix.

**THIRD REACHABLE BRANCH (CRO NOTE, adopted):** reader (1)'s guard WITHHOLDS a scope's `category-views` when its LATEST
cell is null. On production vintage cottonwood's values can lag its axis (09-18 vs 09-21 was the measured shape), and
reader (2)'s roll-forward fills the GLOBAL fold, not the scope's own cross-section read. So **cottonwood
`category-views` ABSENT (withheld, never zero-filled) is reachable** -- inside the blast radius (an ABSENT writes
nothing), and Andrew's smoke is told so in advance rather than meeting it as a surprise. The three outcomes are
therefore 16/16, 15/16 (global account-distribution absent), or 14/16 (both); the step-4 ping names every ABSENT.

---

## 4. LEG B -- THE FIVE SYNCED KEYS BY NAME, CURRENT AND TARGET BYTES (CTO item 1)

The pre-push hook syncs `data/*/scripts/{gold,silver,bronze}/*.py` changed by the push. CLOUD HEAD `ac571ef0c7` changes
exactly ONE such file relative to what the 09-21 20:30Z push landed. Current state read this turn (head-object, 14:3xZ):

| key on `opal-data-mdpf` | CURRENT VersionId / size / md5 | == CLOUD HEAD? | TARGET after the push |
|---|---|---|---|
| `code/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | `FjrdsfCycvPskUPoDXPsBdDggc1WMsy.` / 194,495 / `3d775af9…` (20:30:12Z) | **NO** -- HEAD is 195,258 B, md5 `a2b5f5980e9f66c9b1cfc2f67c8586dd`, blob `c9e47f964f` | **CHANGES** to HEAD's bytes (reader 2 fix, +6 lines) |
| `code/scripts/gold/mdpf_gold_consolidator.py` | `TNenG8tFUziU9A8FXZbjsMMxFNcb9YQq` / 127,929 / `5dbc7a53…` | yes | unchanged |
| `code/scripts/gold/mdpf_revamp_model_crosswalk.py` | `pRpzwLP69Qono_aA5Drslbe3M92PEX0q` / 20,213 / `10de5b15…` | yes | unchanged |
| `code/scripts/assets_gold/build_cottonwood_mdpf_slice.py` | `misXby7frL9LITjH7ZwLsyhWwfbu4oS0` / 68,188 / `b811bae1…` | yes | unchanged |
| `code/scripts/assets_gold/build_cottonwood_mdpf_pair.py` | `6M6Vt9o.S28RcOtgYjSWlZeW7vgqaqGT` / 51,726 / `245d9b59…` | yes | unchanged |

(md5 = the S3 ETag on these single-part objects; compared to `git show HEAD:<path> | md5sum`, 5 of 5 read.) The EC2
plane runs CLOUD HEAD's FULL files; the Lambda runs the MINIMAL pin -- the two planes differ by design (HEAD's spine is
195,258 B vs the pin's 179,962 B) and only the reader-(2) hunk is common to both. LEG B is **not restored** to the
pre-09-21 versions: the fix-forward direction keeps Phase A+B on the EC2 path and adds the fix.

---

## 5. EC2 REACHABILITY, RE-MEASURED TODAY (CTO item 2) -- NOT carried from the 09-21 packet

- `i-02448edb624a7a7cf` (mdpf-daily-runner): **state `running`, LaunchTime 2026-09-22T13:40:23Z**; SSM `PingStatus
  Online`, last ping 14:31:23Z, agent 3.3.4108.0. (Its normal state is stopped-between-runs; this is a SECOND boot today
  -- the daily chain's own run was 12:52Z.)
- Today's chain log `telemetry/mdpf-daily-runner/logs/mdpf_daily_20260922_125237.log` (28,299 B, 12:54:29Z): stages
  0/WS-D/WS-C/WS-B/WS-E/LEG2/WS-A all `rc=0`, then **`STAGE6-REVAMP rc=1 dur=1s status=error` on
  `ModuleNotFoundError: No module named 'lib.opal_naming'`** (log :245-247) -- identical to 09-21 (row
  `MDPF_TAXSMA-S5`, disarm owner `2.0.0_SA_COO~T`). **So the EC2 path still cannot reach ANY Cottonwood or spine code
  today; LEG B's changed key is inert there until TAXSMA's import is fixed.** The exposure the CTO recorded (99490) is
  unchanged in shape and, after this push, carries the fixed spine rather than the unfixed one.
- The 13:40Z boot has produced NO telemetry log yet (newest of 4 listed is the 12:52Z one) and no SSM command is behind
  it (newest SSM command on the instance is 09-20). Not this deploy's act; stated because a signer reading "runner
  running" would otherwise infer the chain is mid-run. Nothing here touches the instance.

---

## 6. ROLLBACK VERSIONIDS, LEG A AND LEG B ALIKE (CTO item 3), AND PER-KEY ROLLBACK FOR LEG C

| leg | key | rollback to | how |
|---|---|---|---|
| A | `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` | VersionId **`uYOduyR_y0a0IH8bEnA8Lukn4qQRzcAR`** (sha256 `7af2180975…`) | `copy-object` that version onto the key (new latest), literal back to `48b8671569…`, gated targeted `safe-apply`, read-back `CodeSha256 == evIYCXUR…` -- the exact sequence exercised at 13:2xZ today |
| B | `s3://opal-data-mdpf/code/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` | VersionId **`FjrdsfCycvPskUPoDXPsBdDggc1WMsy.`** (194,495 B) | `copy-object` that version onto the key; the next runner boot syncs it |
| C-gold | `s3://opal-data-assets/portal/gold/mdpf/{49financial,inflection,cottonwood,global}/{aum-metrics,account-distribution,category-views,aggregate-aua-timeseries}/<date>.json` + `_manifests/` | bucket versioning **Enabled** (read this turn): each key's prior version | per-key `copy-object` of the prior VersionId; the 13:30Z fire tomorrow rewrites them regardless |
| C-serve | `s3://opal-data-portal-v2/platinum/mdpf/*` (publisher `SERVE_BUCKET`/`SERVE_ROOT`, read from the applied plane) | bucket versioning **Enabled** (read this turn): each key's prior version | per-key `copy-object`; or re-run the publisher after a C-gold rollback |
| **C-stage 1** (bdmp) | `s3://opal-data-assets/blackdiamond/cottonwood/gold/dim_model_portfolio/date=2026-09-22/data.parquet` -- `bdmp.main(["--date", adate, "--upload"])` @`:1206`, `GOLD_PREFIX` `build_dim_model_portfolio.py:72`, put `:535`. **adate = 2026-09-22** (newest `fact_model_assignment` partition, read 15:1xZ; newest three 09-20/21/22). The partition ALREADY EXISTS: written 13:30:40Z today by the running pin's own bdmp call (1 version) | VersionId **`Ck8Yka0YkB5T8YS_VWOGChjbmzAYNfLD`** (8,783 B) | `copy-object` that version onto the key (idempotent writer keyed by assignment date; same silver partitions -> same content expected) |
| **C-stage 2** (slice) | `s3://opal-data-assets/gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` -- `slice_mod.main(["--upload"])` @`:1212`, `SLICE_KEY` `build_cottonwood_mdpf_slice.py:123`, put `:1153` | VersionId **`T7zvya5jX28HzwQNsupKRgWrc84ibPkL`** (99,652 B, 2026-09-16 13:30:50Z) | `copy-object` that version onto the key |
| **C-stage 3** (pair) | `s3://opal-data-assets/gold/mdpf_revamp/cottonwood/{account_distribution,aum_metrics,account_units}.json` -- `pair_mod.main(["--date", adate, "--upload"])` @`:1216`, `STAGING_PREFIX` `build_cottonwood_mdpf_pair.py:134`, `_stage_upload` `:738-755` (put + listing verify) | VersionIds **`5PdffIm_dfJnwagwlzd9.OxEqjWPG63j`** (9,291 B) / **`6X6tPnaxWcQ9c.ow3cuqJAU6DpVmYcm1`** (5,087 B) / **`JAYwgtMDl5HRUwwDAVGxgw91RFaQjy0v`** (8,268 B), all 2026-09-16 13:30:51Z | `copy-object` each version onto its key |

The three staging writers run IN-PROCESS on the production branch before any portal key (`run_cottonwood_family`
@`5991626d4f:1206-1218`), same three calls as the running pin (a completeness row, not new exposure). What is new is
the code producing them: slice and pair are Phase A+B bytes. **The staged cottonwood keys were last written
2026-09-16 13:30Z** -- the family has not completed on any fire since, which is the 8-of-16 the estate has served
daily; only the dim partition (bdmp runs first) has kept landing. The invoke therefore REWRITES 5 staged keys and the
dim partition; consumers of the staged keys are this same run's `spine.load_cottonwood_slice` and the global fold's
sidecar read (both in-process) and the EC2 Stage 6 path (dead at import today, s.5). A staging rollback is the FULL
rollback: restoring the portal keys while leaving fix-forward content in these six keys is a half rollback.

Blast radius of LEG C, all branches: the gold invoke writes only what `build_all` builds (per-scope, per-type keys
dated by the scope's data_as_of; a scope that fails is ABSENT, never zero-filled -- the 13:30Z fire today already wrote
8 of these 16 keys on the old pin, so the invoke REWRITES 8 and ADDS up to 8) plus the six staged keys above. The
publisher projects changed gold to `platinum/mdpf/*` on the EGRESS role, its declared read/write prefixes only. Worst
reachable branch: a crash mid-build on the real vintage -> partial gold writes and/or partially rewritten staged keys
-> rollback per key by version (every key above is on a versioning-Enabled bucket), and tomorrow's scheduled fire
supersedes. **No key outside these FOUR prefixes -- `opal-data-assets/portal/gold/mdpf/`,
`opal-data-assets/gold/mdpf_revamp/cottonwood/`, `opal-data-assets/blackdiamond/cottonwood/gold/dim_model_portfolio/`,
`opal-data-portal-v2/platinum/mdpf/` -- is reachable by either function's role.**

---

## 7. THE SEQUENCE THIS SEAT WILL RUN AFTER BOTH HALVES, AND WHAT IT WILL NOT DO

1. Open ledger `mdpf-cottonwood-fixforward-20260922` (legs: A1 artifact, A2 literal, A3 apply, A4 running-plane proof,
   B push-sync, C1 gold invoke, C2 publisher invoke, C3 served read); `.open_deploys/` sentinel.
2. LEG A: upload `built_fix2.zip` (metadata `content-sha256 = e5a28d1f…`), re-download and compare; commit the literal
   `MDPF_GOLD_COMMIT = "5991626d4f4e583383a2dba09927c2a319463fec"` with this packet's blob in its comment; targeted plan
   gated in code to exactly `aws_lambda_function.mdpf_gold` with the env diff exactly this var; `safe-apply`; read back
   `CodeSha256 == b64(e5a28d1f…)`, `CodeSize 872,699`, `MDPF_GOLD_COMMIT 5991626d4f…`; re-download the live bundle and
   compare the in-zip vintage.
3. LEG C: `aws lambda invoke mdpf-gold-lambda` with `{}` (production path, `kind=manual`; NOT qa_local), read the run
   manifest (`a4_objects_built`, `data_as_of`, per-scope errors); then `aws lambda invoke opal-assets-mdpf-portal-publisher`
   with `{}`; read its publish manifest; head the served keys.
4. Ping Andrew with the numbers (which scopes, which dates, 16/15/14, and EVERY per-scope ABSENT by name -- the three
   branches of s.3) for his visual smoke.
5. LEG B closes when MSTR's push lands and the key's ETag reads `a2b5f5980e9f66c9b1cfc2f67c8586dd`; the ledger stays
   OPEN on that leg until then (it is not this seat's push).

**WILL NOT:** build from HEAD; rebuild between signing and upload; touch the EC2 instance or `mdpf-daily-dispatch.sh`;
restore LEG B; widen cottonwood's sidecar window; run a qa_local as the acceptance; invoke anything twice "to be sure".

---

## 8. WHAT EACH HALF SIGNS

- **`1.0.0_SA_CTO` half:** s.2 (the pin's delta and the exact bytes), s.4 + s.5 + s.6 (LEG B by key with current/target
  bytes, EC2 reachability today, rollback VersionIds A and B -- 99490 items 1-3), s.6 C-rows (the served-output blast
  radius and per-key rollback, both branches of s.3).
- **`4.0.0_SA_CRO` half** (or `2.0.0_SA_COO~F` in stead if the CRO is dark): s.1 (the misread owned and the 1465fd3f7d
  finding), s.3 (the two reachable outcomes of the real invoke), s.6 (never-widen: no key outside the named prefixes),
  s.7 (the sequence and the will-nots).

Sign as before: a commit naming this packet's blob hash (printed in the request message), or a refusal naming the section.
