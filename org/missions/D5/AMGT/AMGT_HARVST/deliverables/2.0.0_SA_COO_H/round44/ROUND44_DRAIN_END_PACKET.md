# AMGT_HARVST -- ROUND 44 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-04 ~19:4xZ

**Round:** the round-43 analysis enrichment list (`ledger/ROUND_ANALYSIS.round43.md` @9cacf32e54). Decomposition section 57,
issued @834ac9f9c8. Four READ cells. **Class: LOCAL and SERVED reads only.** No collection, no vendor call, no S3 write, no
publisher request, and no served write.

The reads ran 17:58Z-18:41Z, before the site-Z crash at 18:58Z. They were committed on relaunch @02217a491f. Nothing was re-run.
No repair cell was cut: every repair below either needs a served write under a pair, or a ruling, or collection held on Andrew's
word. They are offered for the round-44 analysis's enrichment list.

## 1. The cells

| cell | FWD | read verdict | evidence |
|---|---|---|---|
| `HVST-aq-1` | FWD-2 | **FAIL.** sa PASSES: 50 of 50 sampled, 0 article fields lost. barrons, bbg, ft and wsj each lose named fields. barrons loses ticker tags, paywall flags, topics and summary. bbg loses page-level language and keywords. ft loses `html_lang` and the JSON-LD publisher block. wsj loses language, `isAccessibleForFree`, keywords and description. 3 of 50 sampled wsj originals (fetched 2026-10-02) have no silver row. | `round44/aq-1.READ.md`, `aq-1.field_census.{py,out,json}` |
| `HVST-aq-2` | FWD-5 | **PASS (graded as judgment at L9).** 6 days were read on BA and NVDA: 0 order violations, served count = gold rows on every day, 0 exact-key ties. The order key is `_dissection_sort_key` = (signal tier A<B<C<D, mention_count DESC, published_utc ASC). | `round44/aq-2.READ.md`, `aq-2.timeline_order.{py,out,json}` |
| `HVST-aq-3` | FWD-7 | **FAIL.** The served rank reads the RAW article count: `CHATTER_AXIS_SOURCE=legacy`, and DESIRED (`chatter-axis-schedule.tf:70`) equals APPLIED. In the planted pair through `compute_chatter_axis`, the passing mention ranks 1 under legacy and 2 under gold. The served chatter rankings are EMPTY today (NO_SIGNAL_IN_WINDOW 191 of 191). A `--source gold` dry run HOLDS because the declared publisher set is empty: no universe-scope collection concluded in the window. | `round44/aq-3.READ.md`, `aq-3.rank_basis.{py,out,json}`, `aq-3.gold_dryrun.out` |
| `HVST-aq-4` | FWD-12 | **FAIL on limb (c) only.** (a) PASS: 33 quarantined keys equal the round-32 set. (b) PASS: 0 `/api/v3/articles/` requests in code. (d) PASS: 11,210 stored sa rows re-checked, 0 mismatches outside the quarantine. (c) FAIL: `config.json` `max_listing_pages.sa = 25` overrides the code default of 200 on the worker path. Storage agrees: the maximum `search_page` is 25 over 23,364 listing hits. | `round44/aq-4.READ.md`, `aq-4.sa_integrity.{py,out,json}` |

## 2. For the CVO

- **To grade:**
  - FWD-5, as judgment: "clicking any day shows the articles behind that day, strongest first". Is (tier, mention count) the right
    meaning of "strongest"?
  - The three FAIL verdicts, read against their FWD text.
- **A contradiction placed, not resolved by the cell itself:** aq-1's limits note calls `sa:3793704` (2022-01-31, attached to
  AMD) the FWD-12 wrong-article class. aq-4 (d) and row Z-S82 read it as a real multi-name article (AMD, NOVN, REGN), with 0
  wrong-article mismatches outside the quarantine. The aq-4 reading rests on the independent classifier over every row and is the
  one this packet carries.
- **Surprise rows this round:** `AMGT_HARVST-Z-S82` (OBSERVATION, INERT, disarm owner COO~H). 19,967 of the 31,042 served gold
  mention rows (64%) were published before 2026-01-01, while FWD-9 and `STORE_START` declare 2026-01-01. Windows are unaffected.
  Whether those rows are served, trimmed at gold or kept as context is the CTO's scope call.

## 3. Repairs offered for the round-44 analysis (none cut)

| FWD | repair | class | blocker |
|---|---|---|---|
| FWD-2 | Type the lost fields in `lib/opal_data_harvest/silver_from_bronze.py` and the publisher field maps, barrons first; find why 3 wsj originals have no silver row; rebuild silver from the stored originals. | SERVED (never-widen pair) | none |
| FWD-12 (c) | Raise `config.json` `max_listing_pages.sa` past 25, or stop the worker overriding the publisher default; plant that the worker path's effective sa cap is > 25. | LOCAL | Proving depth past page 25 needs a new sa backfill, which is collection held on Andrew's word. |
| FWD-7 | Flip `chatter_axis_source` to `gold` (one env flip + apply). | SERVED (pair) | The flip HOLDS until either a universe-scope collection run lands (held) or the CTO re-rules C-HV-RANK-DECLARED-SET for a backfilled store. |

Board as the COO reads it: REALIZED 5 of 17; FWD-5 is a REALIZED candidate at L9; 3 open without new collection (FWD-2, 7, 12);
8 open needing new collection (held).

Push: read at send time.
