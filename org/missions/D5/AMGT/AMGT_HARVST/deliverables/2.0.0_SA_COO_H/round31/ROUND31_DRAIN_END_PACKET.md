# AMGT_HARVST ROUND 31 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-10-01 ~04:4xZ

**Issuance:** `fa71ab063e`, three orders over `ROUND_ANALYSIS.round30.md` @`6adebef352` (decomp section 44, v3.11).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.
**Class: WORLD** (`ad-1` writes two Secrets; `ad-2` is sa vendor egress) **plus LOCAL** (`ad-3`, a read with no vendor call).

## 1. THREE ORDERS, ALL TERMINAL

| order | class | pair | drained | status |
|---|---|---|---|---|
| `ad-1` the token store: wsj/barrons session bundles into Secrets; sa `check()` reads the session's own `user_id` | WORLD | `14924ceffa` / `9cee6547df` | A0 `9e68057327`, B `3f7ff3daec` | complete (`29984dd835`) |
| `ad-2` sa batch 1, ten resolved names, `--no-sign-in` | WORLD | `14924ceffa` / `9cee6547df`; A2 re-signed `ed40d75777` / `288a4b254c` | A0 `93ddc953c1`, A `87661b48c6`, A2 `46469b1acf`, regrade `d3a9617c7e` | complete (`ee045297a9`) |
| `ad-3` residential-IP assignability read | LOCAL | -- | `cc8f3bddc2` | complete (`b1991be52c`) |

- **Close run** (`round31/close_run_round31.py`; outputs `round31/rerun/*.txt`; summary `close_run_round31.out.txt`):
  - **First pass at trunk `bc4f634248` (04:35Z): 5 of 6 rc 0.** `ad1_ac3` read 1 failed, 362 passed:
    `test_o1_run_record_reach.py::test_the_persisted_record_is_never_overwritten`.
  - **Cause (row `Z-S50`):** the test hardcodes `started_at` 2026-09-30, so it passes only on that UTC date. On 10-01 the
    second persist lands on a different `date=` key and no refusal is emitted. The product's conditional put is untouched.
  - **Issuer direct act (LOCAL, one line):** the test now takes `started_at` from the original key's own partition.
  - **Second pass at `089a39f74c` plus that repair (04:40Z): 6 of 6 rc 0**; collector suite 363 passed, 1 skipped; 0
    tracked files rewritten.

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades)

| FWD | this round |
|---|---|
| **7 / 1** | **The token store exists** (`ad-1`). `dowjones/wsj/session` and `dowjones/barrons/session` are in Secrets; the stored SHA-256 equals the local bundle on both (AC1 readback, PUBLISHER NETWORK CALLS: 0). sa `check()` reads the stored session's `user_id` and raises when it is absent, with no literal fallback (`Z-W85-S2` closed in code). **Nothing reads the two new secrets yet.** |
| **1 / 9** | **sa batch 1 on its working path** (`ad-2`). Pass 1 reached 0 names (`Z-S48`, the issuer's sorted plan; BA 502, then a cooldown skipped 9 with 0 requests). The A2 re-run: ASML 1 listing page + 8 articles, then a ProxyError; Adobe 2 pages + 20 articles, then a 502 STOP. 28 sa articles fetched, 31 objects uploaded, 0 sign-ins, sa only. **Measured 1.33 listing pages per name over 3 jobs; the re-based sa ceiling for the other 79 names is 105 pages** (DEFAULT 1,975). Every job ended on a late article transport/5xx error, never a challenge or the account. |
| **cloud phase 2** | **The Bright Data residential egress is ASSIGNABLE to an EC2 host** (`ad-3`). The hosts are proxy clients of the residential pool through `astn/brightdata/residential-proxy` (MEASURED). The BD-side allowlist is INFERRED. VENDOR CALLS: 0. |

## 3. ROWS THIS ROUND

- **Worker rows:** `Z-W87-S1` (ft's bundle keeps no expiry; NOT RECORDED), `Z-W87-S2` (the stored sa `user_id` is not the
  old literal), `Z-W87-S3` (secret names ruled `dowjones/{wsj,barrons}/session`); `Z-W88-S1..S4` (S3: an `error` status
  is not on the STOP list but sets a 15-minute cooldown, and the worker waited it out; S4: the issuer's AC2 format bug,
  fixed @`62c240853a`).
- **Issuer rows:** `Z-S48` (sorted plan file), `Z-S49` (a worker wrote into the shared tree), `Z-S50` (the date-bound
  test, repaired at this close).
- All INERT; none BLOCKING or ARMED.

## 4. FOR ROUND 32 (the CTO's list)

- sa per-name ceiling: 105 pages (MEASURED).
- sa jobs end on late article ProxyError or 502 (egress `existing-residential-proxy`); whether `error` joins the STOP
  list, or a per-article skip replaces the stop, is open (`Z-W88-S3`).
- ft's bundle keeps no cookie expiry (`Z-W87-S1`).
- **First light** (`OPAL_HARVST_first_light_20261001`, 09:00Z, armed by `4.0.0_SA_CRO~Z`) is graded by this seat after it
  fires, from `.runtime/harvest-first-light/<run_id>/summary.json`, with the brief's IV.4 confound stated. That grade
  decides in-tab REST versus page parsing per bbg/wsj/barrons, and goes to the CTO as round-32 input.
- PRD v0.13 (@`7d73abbe0e`) carries the Friday addendum. Its ratified-text half reads STALE (`prd-signoff.py status`,
  04:31Z), owed by `3.0.0_SA_CVO~Z`. The Friday round (placement section 3 step 3: the wrong-object repair first) is cut
  the tick that half is SIGNED.

## 5. FOR L9

- All criteria are mechanical.
- WORLD artifacts: the two Secrets (AC1 readback); sa bronze/silver for ASML and Adobe, and run records, under
  `opal-data-harvest` (`~88/ad2_runs.json`).
- **Disposable worktrees:** `wk-hvst-r29-81..83`, `wk-hvst-r30-84..86`, `wk-hvst-r31-87..89`. Removal needs Andrew's word.
