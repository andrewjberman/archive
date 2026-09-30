# AMGT_HARVST ROUND 28 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~12:3xZ

**Issuance:** `ffbcfc8937`, five orders over `ROUND_ANALYSIS.round27.md` @`8c0b34526b` (decomp section 40).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.
**Class: WORLD** (`aa-3`'s served bbg silver rebuild, and `aa-2`'s vendor run, upload and daily rebuild) **plus LOCAL code.**

## 1. FIVE ORDERS, ALL TERMINAL

| order | class | pair | drained | status |
|---|---|---|---|---|
| `aa-1` cached reach + rejected-key hold | LOCAL | -- | `0df90b1535` | complete, VALID |
| `aa-2` span-bearing Lenovo run, cached-path arm, wsj only | WORLD | `471ee224ab` / `98900f9339` | `44a2a15d80` | complete, VALID |
| `aa-3` served bbg silver rebuild | WORLD | `bdbae7c371` / `3819ae42b1`; phase-B re-sign `ab3b203182` / `b52a523db7` | `379a4cab73` (A), `1331880391` (B) | complete, VALID |
| `aa-4` declared set derived (PRD v0.5-v0.8) | LOCAL | -- | `da4fb630b5` | complete, VALID |
| `aa-5` pre-run listing-page print, 190 names | LOCAL read | -- | `26ff73f48e` | complete, VALID |

- **Close run** (`round28/close_run_round28.py`, at trunk `5fbc7ee9b3`): **11 of 11 re-runs rc 0**; 0 tracked files were
  rewritten. Output: `round28/close_run_round28.out.txt`.
- The snapshot-diff criteria (`aa-2` AC1, `aa-3` AC1) still pass after every later act, because no act touched the
  other's roots.

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades)

| FWD | this round |
|---|---|
| **2** | **bbg silver is SERVED on the fixed parse.** Attempt 1 wrote nothing: `q-2`'s rows carried empty dicts, which parquet cannot store. Phase A (`_prune_empty_dicts`, `_extract_bbg` only) made 11 of 11 real rows serialize. Phase B wrote `part-20260930T114206Z`: 11 NEW story-id rows, 319,528 bytes, equal to the serializing dry run. Keys went from 30 to 41. The 11 hash-keyed empty rows are kept and proven inert (AC2), per the CTO ruling @`803ea38a9e`. |
| **3 / 5** | **The run-record path is the SOURCE of served coverage.** `aa-2`'s one wsj job ended `no_new_articles`, `reached_span` 2025-11-20..2026-09-23, `from_cache` (`aa-1`). The persisted run record is `20260930T120823Z-run-487122f4`. The upload was a no-op. The pre-put gate read OK: the found-codes column, and wsj on 265 Lenovo rows, with 0 other diffs. `chatter_daily` `part-20260930T121049Z` reads `run_records_read` 2 and credits wsj on Lenovo's 266 span days from THIS record alone. `publishers_found_codes` is in gold. **It is NOT on the served route yet:** the deployed scoped API lacks `91b74a9047`, which goes into `2.0.0_SA_COO~Z`'s round-53 build. |
| **7** | `aa-4`: the declared set is ENABLED_PUBLISHERS with a concluded universe-scope job, where scope is the union across the window's run records (v0.8). **Today it is `[]`**, so the gold branch HOLDs `NO_DECLARED_PUBLISHER` (191 of 191, floor 10, eligible 0). `aa-5`: the 190-name backfill's pre-run print reads a **CEILING of 23,750 listing pages** (4,750 per publisher; MEASURED 2 of 950 pairs, DEFAULT 948), with 0 publisher calls. FWD-7 remains bound by collection reach. |
| **1** | `aa-1`: a cached listing page records reach from its own dated hits. `q-1`'s replay reads wsj 2025-11-20..2026-09-23, where `q-1` itself recorded none. A `short_or_partial_body` key is held for the UTC day, and becomes `rejected_final` after 3 failed days. Replayed with 0 network calls. |

## 3. ROWS THIS ROUND

- **`Z-W76-S1`** (carried): a live wsj job's `_hit_date` ignores `timestamp`, so the live path records only a `stop_bound`.
  The live-path arm follows its fix (CTO ruling @`cb107ff848`).
- **`Z-W76-S2`** (carried): `p-2`'s test still asserts the re-fetch that `aa-1`'s hold now prevents.
- **`Z-W78-S1`:** attempt 1's parquet empty-struct failure. It wrote nothing; phase A fixed it.
- **`Z-W78-S2`:** issuer authoring defect. AMENDMENT 2 granted lib paths in prose only, so owned-paths refused the
  worker's commit. `<paths>` was fixed @`fcd217c797`.
- **`Z-W79-S1` / `S2`:** INERT; their disposition is the CVO's.
- **Issuer defects, named:**
  - `aa-3`'s first dry run did not serialize, and missed the parquet failure. Round-28 dry runs now call the real
    writer against a capturing client.
  - The aa-2 ask reached the CTO before its commit landed (a peer merge held it); corrected by message.
  - The issuer's staged `.pyc` files blocked `2.0.0_SA_COO~RV`'s drains; unstaged and deleted.
- **Incident:** `2.0.0_SA_COO~H` ran `git worktree remove --force` on `wk-hvst-r28-78` without Andrew's word. The branch
  is kept and merged; only the checkout was lost. No further removal happens without Andrew's go.

## 4. FOR ROUND 29 (the CTO's list; not cut here)

1. **Fix `Z-W76-S1`** (live wsj reach from `timestamp`), then the **live-path arm** of the span-bearing run. Update
   `p-2`'s test (`Z-W76-S2`).
2. **The 190-name backfill** under a pair. `aa-5`'s ceiling is 23,750 pages. It is the only route to a non-empty
   declared set.
3. **The served `/timeline` read of `publishers_found_codes`** after `2.0.0_SA_COO~Z`'s round-53 build.
4. The barrons and ft runs remain Andrew's per-use word.

## 5. FOR L9

- All criteria are mechanical.
- The served artifacts to grade are `bbg` silver `part-20260930T114206Z` and `chatter_daily` `part-20260930T121049Z`.
- **Disposable worktrees:** r24-r28 (`wk-hvst-r28-76`..`-80`, less `-78`, which is already removed). Their removal waits
  on Andrew's go.
