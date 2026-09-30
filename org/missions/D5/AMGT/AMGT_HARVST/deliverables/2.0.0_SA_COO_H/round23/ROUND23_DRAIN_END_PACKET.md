# AMGT_HARVST ROUND 23 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~02:0xZ

**Issuance:** `1682817d89` (three independent read-only cells over `ROUND_ANALYSIS.round22.md` @`9d7bd0e4f9`; decomp
section 35). **L8-L10 route:** `3.0.0_SA_CVO~Z`. **Class:** LOCAL. Every cell read the served store and wrote nothing
served. **Purpose:** measure the seven FWDs ungraded since round 10, for the CTO's grade. The cells MEASURED and graded
nothing.

## 1. THREE ORDERS, TERMINAL, VALID

| order | deliver | drained | instance |
|---|---|---|---|
| `HVST-m-1` FWD-1/2/3 | `48cd894f9e` | `5191e4b63a` | VALID rc=0 |
| `HVST-m-2` FWD-4/7 | `d63e6ffd08` | `4e1d998178` | VALID rc=0 |
| `HVST-m-3` FWD-8/9 | `22393addc4` | `253b88bcce` | VALID rc=0 |

**Close run** (`round23/close_run_round23.out.txt`, trunk `253b88bcce`): all 7 scripts were re-run, each rc 0, and 0
tracked files were touched.
- Six outputs are content-identical to the workers' (m-1's three differ only in line endings).
- `m3_ac2` differs on ONE informational line: its repo-text scan grew from 340 to 361 files as the other cells merged.
  The measured result on that line is unchanged (a plan record exists for Lenovo only).

## 2. THE SEVEN FWDs, MEASURED (the CTO grades; nothing here is a grade)

| FWD | DONE WHEN (short) | measured |
|---|---|---|
| **1** re-readable as sent | every article and its listing page re-opened byte-for-byte | Bronze matches the RECORDED sha256 on **126 of 126**. **But 104 of 126 are `normalised_record`**, so the match is against the stored rebuild, not the publisher's response; that original is NOT MEASURABLE HERE. Listing pages are stored for wsj (2) and sa (2) only, and **no article record links a listing object (0 of 120)**. |
| **2** every sent field kept, typed | every received field typed in the table, queryable | Missing bronze fields in silver: barrons 0/15, bbg 0/19, ft 0/14, **sa 5/46**, wsj 0/15 JSON. **6 sa bronze articles have no silver row.** For barrons, bbg and ft the named fields read NOT SENT, but bronze is already a rebuild, so "not sent" cannot be shown. A query by company and date works (Lenovo 09-23: 14 rows). |
| **3** how found; no re-fetch | list-or-search, words and position; a same-day re-run fetches nothing held | Kind and words are present for all publishers (sa words 25/46). **Rank and page are present only for sa (5) and wsj (11).** Duplicate keys 0/120. The same-day re-run is NOT MEASURABLE HERE: no run records exist. |
| **4** strength per pair | six carriers per pair, grade re-derived from stored text | **6 of 6 carriers on 304/304 pairs; re-derived from stored silver text 304/304 match.** A negative control mismatches 52, and 0 silver pairs are missing from gold. |
| **7** rank uses strength | page ranks computed from the graded daily table | **`CHATTER_AXIS_SOURCE=legacy`:** the served rank (lead-panel rankings route, `read_rankings`) is computed from RAW pool publication counts, not the graded table. It serves 2 rows, so served vs graded is NOT MEASURABLE (n=2). Raw vs graded windows correlate 0.83 over 36; 6 companies rank 5 or more places higher on raw counts. |
| **8** undelivered reach the store | everything held only on the collecting desktop is in the store, none duplicated | The desktop `progress.sqlite3` (gitignored; the only inventory) holds 120 bodies and 121 links. **120/120 bodies are in bronze and silver by key, 121/121 links are in silver, 0 duplicates.** The legacy `upload_outbox`'s 241 `pending` rows are not a delivery signal. |
| **9** history since 2026-01-01 | per listed security, backfill from 01-01, plan printed first, no missing days, re-run adds nothing | **Of 191 covered:** 11 on or before the floor (**Lenovo's first article is 2025-05-22**), **54 start after it, 126 have no article.** The daily series is dense 191/191 by construction, so it is not evidence of history. **A pre-run plan exists for Lenovo only** (5 publishers x 25 pages). Duplicate keys 0. |

## 3. ROWS THIS ROUND (all INERT)

- **`Z-W53-S1`:** no article record links its listing object.
- **`Z-W53-S2`:** 104 of 126 bronze objects are normalised records.
- **`Z-W53-S3`:** 6 unlabelled sa bronze objects have no silver row.
- **`Z-W53-S4`:** sa rows tagged `992_HK_Equity` include titles not about Lenovo.
- **`Z-W54-S1`:** the served rank list holds 2 rows (n=2).
- **`Z-W55-S1`:** the only undelivered-article inventory is the gitignored desktop SQLite.
- **`Z-W55-S2`:** the orders' prose `<expect>` is searched as a regex by the checker.

## 4. CARRIED INTO ROUND 24 (not graded here)

- **From the DSGN_AMGTV1 round-7 analysis** (`0c498ee766`, ruling 2, msg 26843): `/timeline/day` answers in about 5.5 s,
  warm, for a day with articles (CVO v9 section 2). Profile it, then fix it under a HARVST pair.

## 5. FOR L9

There are no judgment criteria this round; it is measurement only. The grade of the seven FWDs is the CTO's at L10.

**Worktrees now DISPOSABLE:** `wk-hvst-r23-53`, `-54`, `-55` (and the seven listed earlier). Branches are kept; removal
is on Andrew's go.
