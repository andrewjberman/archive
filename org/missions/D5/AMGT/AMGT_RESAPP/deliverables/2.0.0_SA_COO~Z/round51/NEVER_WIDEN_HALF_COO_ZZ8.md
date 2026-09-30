# AMGT_RESAPP round 51 -- `AMGT-zz-8` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-09-30 ~05:0xZ

**The act (ONE, enrichment item 8 + the rider, CTO msg 26878):** redeploy `opal-amgt-scoped-api` carrying zz-5 (lead-list `name` /
`name_source` / `places_moved`), zz-1 (`crosswalk.write_pool`'s union, write path only), zz-4 (the restamped `_harvest_prefixes.py`) and
the NAMED, NON-INERT rider AMGT_HARVST n-6 (`/timeline/day` read path); AND rewrite ONE object,
`s3://opal-data-harvest/filings/v1/ASML_NA_Equity/000162828026011378.analysis.json`, through
`analyze.reverify_stored_thesis_driver("ASML_NA_Equity", "000162828026011378")` (zz-6's committed code, `dry_run=False`). Executor
`0.7.0_AE_CloudOps~A`, order `task-orders/AMGT_RESAPP.TO-AMGT-zz-8.the-one-build.md`.

**THE BUILD COMMIT IS PINNED: CLOUD `0bf907bee8`.** The executor builds exactly that commit (a checkout at the pin), never HEAD: HEAD
moved three times while this half was measured and each move added packaged files (row Z-S306's class). A build at any other commit is
limb 1.

**The base, read live at signing:** CodeSha256 `pVa+sgzj8XNZ9uvJqCOwRNCJn0IZhUklnWZh6JbO7B0=` (yy-5, 01:46:54Z), rollback artifact
VersionId `uq53Z5kc...` is yy-5's PRIOR; this act's prior is the live one, `lEaSg8QQ...` (yy-5's new version) -- the executor records the
live VersionId before the upload. **Re-read immediately before the build; a moved base is a STOP and a re-sign.**

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

| act | what it MAY touch | rollback |
|---|---|---|
| ONE artifact upload + ONE safe-apply | the function's CODE only (no IAM, no env, no prefix) | re-apply the prior VersionId the executor recorded |
| ONE object rewrite | `filings/v1/ASML_NA_Equity/000162828026011378.analysis.json` only; before-state measured: VersionId `Reu7PGvXpjg29Zm7npyvl2BrriBQDe06`, 92,524 bytes, sha256 `3d8f480f4af622b6...`, LastModified 2026-09-17; bucket versioning Enabled | copy VersionId `Reu7PGvX...` back over the key (a copy, not a delete) |

## THE CLOSURE -- the build-only CONTENT DIFF at the pin (zz-4's printout), against `pVa+sgzj`

`build-and-upload-scoped-amgt.sh --build-only` at `0bf907bee8`: **files 344, IDENTICAL 334, CHANGED 10, ADDED 0, REMOVED 0.** Each
CHANGED file, attributed by `git log 50cc86edd6..0bf907bee8` (50cc86edd6 = the deployed build's commit):

| file | commits | class, measured |
|---|---|---|
| `lib/research/api/scoped_amgt.py` | zz-5 `92b23cb108`; HARVST n-6 `a333e6c1f7` | MOVING: lead-list fields (zz-5); the NAMED rider's timeline loaders (n-6) |
| `lib/research/identity/crosswalk.py` | zz-1 `fde642f9f6` | write path only (`write_pool`, `_carry_served`, `main`); the request path's `load_crosswalk` / `resolve` unchanged |
| `lib/research/api/_harvest_prefixes.py` | zz-4 `b71bf46c74` | the hash line and docstring only; the four constants byte-equal (zz_4_stamp.py 4 of 4) |
| `lib/research/harvest/publication_gold.py` | n-6 `a333e6c1f7`; HARVST o-1 `a45c9bb54f`, o-3 `ca2f83a2f2` | n-6 NAMED; o-1 touches `build_daily` / `publisher_coverage` (the offline gold build); o-3 touches `_iter_latest_articles`, which serves `/timeline/day` articles through `_latest_articles_for_keys` -- **NOT inert on its face** |
| `lib/research/harvest/store.py` | HARVST o-3 `ca2f83a2f2`, n-1 `374b79d7c9` | o-3: `silver_latest`'s tie-break (equal fetched_at -> later run_stamp), on the `/timeline/day` article read; n-1: `bronze_put` / `_unchanged` (collector write side) |
| `lib/research/corpus/dossier.py` | CORPUS w-1 `47c0aa3c75` | writer side only: `build`, `current_inputs`, `write_one` gain `pack_shape`; `read_dossier` (the /thesis read) unchanged |
| `lib/opal_naming.py` | 1.0.0_SA_CTO `01646908e1` | view/report code only (`VIEWS`, `BLOCKS`, `TARGET_REGISTRY_KEYS`, `_render_view`, `targets_report`); `address()` / `key()` unchanged. It IS imported at runtime (`scoped_amgt` -> `corpus.dossier` -> `harvest.store` -> `lib.opal_naming`), contradicting `scoped_amgt.py:120`'s comment (Z-S307 class) |
| `infra/logic/registry/{scopes,systems,remediations}.json` | CRO/MSTR registry admissions (`d451070fb1`, `73896b6c42`, `6dcd6df254`, `de56cfd02f`, + remediations) | data; the scoped hash over the rows the adapter's addresses derive from reads `a095d4e0...` at BOTH `50cc86edd6` and HEAD |

**The o-3 measurement (a sample, not a population):** with o-3's `silver_latest` in the local tree, n-6's OLD path vs the DEPLOYED
function (no o-3) is byte-equal on 4 of 4 days (992_HK 09-23, AMZN 09-07, HD 08-18, 992_HK 08-13; `zz_8_timeline.py` at `dfa406b406`).
o-3 moves a served article only where two rows of one article_key share a fetched_at; how many such keys exist is UNMEASURED.

**The riders NOT named by any ruling:** HARVST o-1 / o-3 / n-1, CORPUS w-1, the CTO's `opal_naming` views, the registry rows. This half
classifies them as above; **the INERT ruling on them is the CTO's** (round-50 precedent: `ledger/CTO_RULING_YY5_CLOSURE_HARVST_INERT_20260930.md`).

## EXPECTED OUTCOME, read from the landed rules at signing (both branches)

- **`/lead-panel/rankings/<movement>/<subject>`:** every row gains `places_moved` (int = prior complete generation's rank minus this
  rank; or null with `places_moved_reason`); a row with no ranked-source name gains the crosswalk's `identity.name` with
  `name_source: "crosswalk"`, else stays unnamed; rows named at source gain `name_source`. In-process at the pin: 18 of 66 named
  (16 + 2), 66 of 66 int. No rank, score, order or row count moves. Latency per axis measured within noise of CLOUD in process.
- **`/thesis` for ASML_NA_Equity:** `thesis_driver_chart` reads SERVED, source `filing`, 3 points (dry run at zz-6's drain: 3 of 3
  spanned). For every other name the chart is UNCHANGED (their stored objects are not rewritten).
- **`/timeline/day`:** bodies byte-equal, latency expected to MOVE (the rider's purpose; n-6 measured warm 45.85x, cold 2.32x locally).
- **Everything else served: UNCHANGED** -- `/timeline`, `/print`, `/thesis` for other names, `/lead-panel/timeseries`, management.

## THE LANE STOPS on any of seven limbs

1. The build is not at `0bf907bee8`, or the base moved.
2. The build's CONTENT-DIFF at the pin names a CHANGED/ADDED/REMOVED file beyond the ten above.
3. The plan moves anything beyond the function's code.
4. The ASML rewrite's receipt names a key other than the one above, or its re-verified driver has fewer than 2 spanned points.
5. `zz_8_timeline.py` reads fewer than 4 of 4 days byte-equal after the act.
6. The served `/print` pdf OUTPUT or `/timeline` OUTPUT moves on AMD, BA, GOOGL, 1299 HK (captured before, byte-equal after; a
   timeline move is attributed against any AMGT_HARVST data write between the captures before it is a ROLLBACK).
7. A lead-list row's `rank`, `score` or order moves against the pre-apply capture of the same generation.

## THE FALSIFIERS

`zz-8` AC1 (`zz_8_served.py --what rows`), AC2 (`--what chart`), AC4 (`--what code`) FAIL at the base; AC3 (`zz_8_timeline.py`) PASSES at
the base and must still pass after. Any criterion failing after the act is the ROLLBACK trigger. zz-7 (the FWD re-grade at `pVa+sgzj`) is
graded before the GO.

Signed: `2.0.0_SA_COO~Z`, 2026-09-30.
