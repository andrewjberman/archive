# AMGT_HARVST ROUND 27 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~09:3xZ

**Issuance:** `0cfb3406bf`, seven orders over `ROUND_ANALYSIS.round26.md` @`ff4405d3d5` (decomp section 39).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.
**Class: WORLD** (`q-1`'s vendor run and its one S3 put) **plus LOCAL code.** No served gold moved this round.

## 1. SEVEN ORDERS, ALL TERMINAL

| order | class | drained | status |
|---|---|---|---|
| `q-1` `p-3(b)` span-bearing Lenovo run | WORLD, pair `dadba8badd` / `0af0a8a5ee` | `608cd4a257` (record) | **withdrawn** after its act (`3849afe124`) |
| `q-2` bbg as-received parses into silver (`Z-S44`) | LOCAL | `0e3952dcab` | complete, VALID |
| `q-3` FWD-7 eligibility census | LOCAL read | `a40b6d5493` | complete, VALID |
| `q-4` `C-HV-RANK-DECLARED-SET` in code | LOCAL | `906dbe0658` | complete, VALID |
| `q-5` `C-HV-COVERED-VS-FOUND` in code | LOCAL | `c6ebfc8b7a` | complete, VALID |
| `q-6` barrons B2 + ft F1, no request | LOCAL | `75db57b063` | complete, VALID |
| `q-7` the gold flip | WORLD | -- | **withdrawn** per CTO ruling (msg 27057) |

- **Ruling 6 held:** no code cell merged before `q-1` drained.
- **Close run** (`round27/close_run_round27.py`, at trunk `94301d5a9c`): **13 of 13 re-runs rc 0**, and 0 tracked files were
  rewritten. The withdrawn orders are excluded.
- **Trunk suites after all merges:** 657 passed, 1 skipped.

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades)

| FWD | this round |
|---|---|
| **7** | `q-4`'s declared-set rule is in the gold branch. `q-3`'s census over the served `chatter_daily` (window 09-01..09-30, COVERED only): **ELIGIBLE 0 of 191.** NOT_SEARCHED 190, and PARTIAL_COVERAGE 1 (992_HK: bbg every day, wsj not). Negative arms: found-set 0, any single publisher 1. **Below the floor of 10**, so `q-7` is withdrawn: a flip could only HOLD and would freeze the served legacy rank. FWD-7 is bound by collection reach. |
| **2** | `Z-S44` is fixed in code (`q-2`). bbg's as-received story is top-level, but the builder read `payload["story"]`; the fix is `silver_from_bronze.py:115`. 11 of 11 real held bbg objects now parse non-empty. The served rebuild is round 28. **Its pair must name the fate of the 11 hash-keyed empty rows** (row `Z-W71-S1`), because the fixed parse keys by story id. |
| **3** | `q-5`: `publishers_found_codes` is emitted and served on `/timeline` series rows (a LOCAL build: 992_HK 2026-02-12 covered=`[bbg]`, found=`[sa, wsj]`; 271 found-not-covered rows over 67 securities). **Not yet served:** it rides the next paired daily rebuild. `q-1`'s persisted run record carries `p-2`'s per-key outcomes (1 fetched key not stored, `keys_stored_join` empty, 26 skipped as held). |
| **1 / 9** | `q-6`: barrons may run its contracted repair once after a same-job reauth (bounded; barrons only). ft keeps its 403 body locally (64 KiB cap, credentials redacted). Replayed with 0 network calls. **Both runs remain Andrew's per-use word.** |

**`q-1`'s act** (both branches were named in the pair; neither was silent):
- ONE run record was persisted (`amgt/harvest/bronze/run_record/date=2026-09-30/20260930T084110Z-run-4ee47491.json`), and 0 other
  objects were written, so the pair held.
- **bbg** was `request_rejected`.
- **wsj** was `no_new_articles`, with `reached_span` NULL: its listing pages were served from same-day cached bronze. That is
  `o-1`'s reach gap: cached listings record no span.
- `build-daily` was withheld per the CTO's condition 3.

**The CTO's question -- why bbg refused a run `o-5` completed** (row `Z-S45`, from `events.jsonl`):
- `q-1`'s bbg job made **no listing request**, because its listings were served from same-day cache.
- Its first and only live request **re-fetched `bbg:NM5NLQ6K50XZ01`**. That is the key `p-2` records as rejected
  (`short_or_partial_body`), and `p-2`'s accepted limit re-fetches rejected keys every run.
- The request returned 403. The contracted press-and-hold repair saw no checkmark within 12s, so the job ended
  `request_rejected`.
- `o-5`'s bbg runs at 04:40Z-04:54Z made 4 listing requests, all 200, before any story fetch.

## 3. ROWS THIS ROUND

- **Issuer rows:**
  - `Z-S45`: the bbg refusal cause.
  - `Z-W71-S1`: ARMED, disarmed by the ruling that the round-28 rebuild's pair names the 11 hash-keyed rows.
- **`Z-W70-S1` (BLOCKING):** disarmed by `q-1`'s withdrawal. The fix carries to round 28.
- **INERT:** `Z-W70-S2`, `Z-W72-S1`, `Z-W73-S1`/`S2`, `Z-W74-S1`/`S2`, `Z-W75-S1`..`S3`.
- **Issuer authoring defects, named:**
  - `<expect>` `0 failed` is never printed by a clean pytest run (`Z-W74-S1`, `Z-W75-S3`).
  - `<expect>` with literal parentheses is read as a regex (`Z-W72-S1`, as `Z-W68-S1`).
  - Future expects use plain printed tokens only.

## 4. FOR ROUND 28 (the CTO's list; not cut here)

1. **Record reach from cached listing pages** (`o-1`'s gap), then a **fresh-day** span-bearing run under a re-signed pair.
   Decide whether a known-rejected key is held within a day (`Z-S45`).
2. **The served bbg silver rebuild** on `q-2`'s parse. The pair names the 11 hash-keyed rows.
3. **The paired daily rebuild** that serves `publishers_found_codes`.
4. **FWD-7:** eligible names need both declared publishers on every window day. Reach means the 190-name backfill, which waits
   on FWD-1 widening, and on ft and barrons (Andrew's runs).

## 5. FOR L9

All criteria are mechanical. **Disposable worktrees:** `wk-hvst-r27-70`..`-75`, `-72`, plus r24-r26. Removal waits on Andrew's
go.
