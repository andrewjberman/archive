# NEVER-WIDEN -- COO HALF: the merge of `HVST-bo-1` (a stored per-security query override) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~H`, 2026-10-08 ~10:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Why a pair for a merge:** `1.0.0_SA_CTO~Z` msg 31664 (R23): "on this box a merge into lib/opal_data_harvest is a deploy to
whatever the driver runs next." The collector runs from the shared working tree.

## THE ACT

One merge of branch `wk-AMGT_HARVST-122-r70` @419dc9b1fc into CLOUD through `.tools/safe-merge.sh`, and nothing else.

## WHAT THE BRANCH CHANGES (read by this seat as a diff against the issuance commit c92e860791)

| file | change |
|---|---|
| `lib/opal_data_harvest/publishers.py` | new `_query_override(security)`; `slug_queries` returns the override's strings when the security carries `query_override`, else runs its loop as before |
| `lib/opal_data_harvest/__main__.py` | `universe()` copies `query_override` from an identity record onto the security when the record carries it |
| `lib/opal_data_harvest/test_bo1_query_override.py` | new, 15 tests |
| `deliverables/0.9.0_WK_AMGT_HARVST~120/rank_universe_identity_20261008.json` | the NEW, UNPOINTED identity file: `AIG_US_Equity` gains `query_override`, an OBJECT `{"value": ["American International Group"], "reason": ..., "source": ...}` (corrected, see C1 below) |
| `deliverables/0.9.0_WK_AMGT_HARVST~121/bn1_names_made_whole.py` and `.out` | the one builder sets that field |
| `deliverables/0.9.0_WK_AMGT_HARVST~122/` | the table, its script, the frozen titles, the proof |
| the surprise channel | row Z-W122-S1 |

NOT changed, by the worker's own check and this seat's diff: `publishers._LEGAL_SUFFIX`, `slug_query`, `discovery._matches`,
`lib/opal_data_harvest/config.json`, and the two round-47 files the config names.

## THE RULE THIS HALF SIGNS

**After the merge, every security the collector can be asked for today derives exactly the queries it derived before.**
- Measured on the branch (`deliverables/0.9.0_WK_AMGT_HARVST~122/bo1_query_table.out`): over the 234 records of the round-47
  identity file, the file `config.json` points at, `CHANGED 0 of 234`.
- Over the 242 records of the new unpointed file: `CHANGED 1` (`AIG_US_Equity`: `["AMERICAN INTERNATIONAL"]` to
  `["American International Group"]`), `IDENTICAL 241`; exactly 1 record carries the field.
- The two American Airlines titles the old query matched are excluded by the new one; the new query matches 0 of 20,500 held
  titles (no held article carries AIG's name, so that it finds AIG's articles at a publisher is NOT shown and cannot be
  without a run).
- Suite on the branch: `lib/opal_data_harvest` 778 passed, 3 skipped; the cell's 15 of 15.

So the override is INERT until the config pointer moves to the new file, and the pointer waits on Andrew's word (R22).

## BLAST RADIUS

- **What may change behaviour:** the next collector PROCESS started from the shared tree after the merge loads the new
  `publishers.py` and `__main__.py`. With the round-47 inputs no record carries the field, so the new branch of
  `slug_queries` is never taken.
- **Writers of the property (the queries a sitemap job sends), N = 1:** `publishers.slug_queries`, called once, in
  `_sitemap_items` (`publishers.py:731` at the base, `:754` on the branch), which `_bloomberg_sitemap` and `_dow_jones_sitemap` both read. Read at signing by a
  search of the package for both function names.
- **What the override does NOT reach:** a leg that does not list through the sitemap. This seat read the two sitemap helpers
  only; how the Seeking Alpha and Barron's legs form their request for a name was not read for this half, so the override is
  claimed for the Bloomberg and WSJ legs and for no other.
- **Stated bound, row Z-W122-S1:** three sitemap helpers still label their stored provenance with `slug_query(company)`. For a
  security with an override the SEARCH uses the override and the provenance label would still read the derived string. Inert
  today for the same reason; it is a defect to fix before the pointer moves.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a. No collection leg is running.** Read at the act: no `backfill_driver` process (with a positive control on the
  process list), and the Seeking Alpha leg's last line is its `PAIRS` completion or a stop this seat did not cause. At
  signing the leg is LIVE (pid 29240, 68 jobs this run), so the merge does NOT happen now.
- **C-b. The table is re-read on the merged tree** before the close: `CHANGED 0 of 234` on the round-47 file, by the same
  script.
- **C-c. A ledger entry** is opened before the merge and closed after C-b (NEVER-2).

## C1 OF THE CTO HALF (@d6ea0eff2f) -- THE FIELD'S SHAPE, PRINTED 2026-10-08 ~10:5xZ

This half first wrote the field as a bare list. That was this seat's wording and it was WRONG; the record and the code agree
with each other. Printed with the branch's own code (`git archive wk-AMGT_HARVST-122-r70` @419dc9b1fc into a scratch folder,
the validator called on the stored record):

- records 242; carrying `query_override` 1, `AIG_US_Equity`;
- the stored field is an OBJECT with keys `value` (a list holding the one string `American International Group`), `reason`
  and `source`;
- validator on the record as stored: ACCEPTS, returns `['American International Group']`;
- validator on a bare list (what this half wrote): RAISES "query_override of AIG_US_Equity is not an object {value, reason,
  source}";
- validator on an empty `value` list: RAISES; on a string: RAISES.

Nothing in the record or the code is changed by this correction. The CTO half's C2 (whether a malformed override stops one
job or the whole run; row Z-W122-S1; the first worded run's AIG result read by hand) stands before the pointer ever moves.

## BOTH BRANCHES

- **C-b reads 0 of 234:** done; the order `bo-1` closes.
- **C-b reads anything else, or the package suite fails on the merged tree:** the merge commit is reverted in the same
  session with a new commit (never a rebase), and the revert is read back by the same table.
- **A leg is found running at the act:** nothing is merged.

## EXCLUDED

No pointer move. No run of any job. No change to `_LEGAL_SUFFIX`. No gold, silver or bronze write. No deploy outside this
box's working tree.

## VERDICT: SIGNED (COO), pending the CTO half; the act waits on C-a
