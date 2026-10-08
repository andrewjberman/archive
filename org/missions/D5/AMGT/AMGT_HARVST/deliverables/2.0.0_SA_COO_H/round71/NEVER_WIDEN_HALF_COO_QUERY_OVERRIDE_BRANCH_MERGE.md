# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-123-r71` @537ac56e9b (`HVST-bo-1` and `HVST-bp-1`) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~H`, 2026-10-08 ~11:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed; it signs on its own read of the
bp-1 diff, msg 31703).
**Replaces:** the COO half `round70/NEVER_WIDEN_HALF_COO_BO1_QUERY_OVERRIDE_MERGE.md` @ca5cb29676 on branch head 419dc9b1fc.
That pair is SPENT WITHOUT AN ACT (msg 31703: "One merge of one branch is one act and one pair").
**Why a pair for a merge:** on this box the collector runs from the shared working tree, so a merge into
`lib/opal_data_harvest` is a deploy to whatever the driver runs next (R23).

## THE ACT

One merge of branch `wk-AMGT_HARVST-123-r71` @537ac56e9b into CLOUD through `.tools/safe-merge.sh`, and nothing else. The
branch is CLOUD @fbeed81cc8 (which holds the round-71 issuance c735bc6be8) with `wk-AMGT_HARVST-122-r70` @419dc9b1fc merged in
at 92345fb83d (`bo-1`) and two commits on top
(`bp-1`: d7c3347e6e, 537ac56e9b).

## WHAT THE BRANCH CHANGES UNDER `lib/` (read by this seat as two diffs: bo-1 against its issuance, bp-1 against bo-1's head)

| file | change |
|---|---|
| `publishers.py` | **bo-1:** `_query_override(security)` validates a stored override; `slug_queries` returns the override's strings when the security carries `query_override`, else runs its loop as before. **bp-1:** the validator raises `QueryOverrideMalformed`, a subclass of `ValueError`; `listing_label(security)`; the three sitemap helpers name their listing by `listing_label`, not by `slug_query(company)` |
| `__main__.py` | **bo-1:** `universe()` copies `query_override` from an identity record onto the security when the record carries it |
| `worker.py` | **bp-1:** `Worker.run_job` catches `QueryOverrideMalformed` before `RequestRejected` and before the generic catch: status `query_override_malformed`, `detail` the validator's message, no cooldown, nothing fetched |
| `test_bo1_query_override.py`, `test_bp1_malformed_override.py` | new: 15 and 9 tests |

Five files, +459 -10. NOT in either diff: `publishers._LEGAL_SUFFIX`, `slug_query`, `discovery._matches`,
`backfill_driver.py`, `lib/opal_data_harvest/config.json`. Outside `lib/`: the new, unpointed identity file gains the override
on `AIG_US_Equity` (an OBJECT `{"value": ["American International Group"], "reason", "source"}`), the one builder sets it, and
the two cells' deliverables and rows. The two round-47 files the config names are unchanged.

## THE RULE THIS HALF SIGNS

**After the merge, every security the collector can be asked for today derives exactly the queries it derived before, and is
stored under exactly the listing label it was stored under before.**
- Queries: `bp1_query_table_rerun.out` on the branch: over the 234 records of the round-47 identity file, `CHANGED 0 of 234`;
  over the 242 records of the new unpointed file, `CHANGED 1` (`AIG_US_Equity`), `IDENTICAL 241`.
- Labels: test iii asserts, for all 234 round-47 records, that `listing_label` equals `slug_query(company)`.
- `slug_queries` is still the one writer of what is searched (one call, in `_sitemap_items`).
- Suite on the branch: `lib/opal_data_harvest` 787 passed, 3 skipped; the two cells' 15 of 15 and 9 of 9.

So both the override and its label are INERT until the config pointer moves to the new file, and the pointer waits on Andrew's
word (R22).

## THE TWO THINGS MSG 31703 ASKS THIS HALF TO STATE

**1. The 900-second cooldown is not set on the new path.** Before `bp-1` (shown by test on `bo-1`'s code, kept in
`deliverables/0.9.0_WK_AMGT_HARVST~123/bp1_today_output.txt`): a malformed override on the second of three securities ended
that job `error`, dropped the validator's message, set a 900-second cooldown on the whole publisher, and the driver, which
treats `error` as a stop, ended the Bloomberg leg, so the third security never ran. After `bp-1`:
`test_i_the_malformed_second_security_ends_with_a_named_status_and_jobs_one_and_three_run` runs three securities with a
malformed second; jobs one and three run, job two ends `query_override_malformed` with the message, and the test asserts
the publisher's cooldown row is `None`. `test_v`, the mutant with the containment removed, asserts the cooldown IS set and
the third job does not run, so the first test is shown to bite.

**2. Where an override does nothing** (row AMGT_HARVST-Z-W123-S1), in the words a reader of the identity file will meet:
**a `query_override` on a security is read only when that security is collected from Bloomberg or the Wall Street Journal
through their sitemaps. For a security collected only through Seeking Alpha, Barron's or the FT, a `query_override` changes
nothing: it is not read, whether it is well formed or malformed, and no error is raised for it.** The same holds for a
Bloomberg or WSJ session that does not go through the sitemap. `AIG_US_Equity` is collected from Bloomberg and WSJ, so its
override is read there and nowhere else.

## OTHER BOUNDS, stated

- The new query "American International Group" matches 0 of 20,500 held titles. That it finds AIG's articles at a publisher is
  NOT shown, and cannot be without a run; the first worded run's AIG result is read by hand (CTO half C2).
- `query_override_malformed` is outside the driver's stop set and its concluded set: the driver goes on past it and keeps the
  pair for retry up to 3 attempts, then `gave_up`. It is never recorded as done. `backfill_driver.py` is not changed.
- `QueryOverrideMalformed` is a `ValueError`, so any handler of the earlier refusal still catches it.

## BLAST RADIUS

- **What may change behaviour:** the next collector PROCESS started from the shared tree after the merge loads the new
  `publishers.py`, `__main__.py` and `worker.py`. With the round-47 inputs no record carries the field, so neither new path is
  taken and the label is the string it was.
- **Writers of the queries a sitemap job sends, N = 1:** `publishers.slug_queries`. **Writers of the listing label, N = 1:**
  `publishers.listing_label`, read by the three sitemap helpers. Both read at signing in the branch's diff.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a. No collection leg is running.** Read at the act: no `backfill_driver` process, with a positive control on the process
  list, and the Seeking Alpha leg's last line is its `PAIRS` completion or a stop this seat did not cause. At signing the leg
  is LIVE (pid 29240, 70 jobs this run, about 125 names left), so the merge does NOT happen now.
- **C-b. The table and the two cells' tests are re-run on the merged tree** before the close: `CHANGED 0 of 234` on the
  round-47 file by the same script, and both test files pass.
- **C-c. A ledger entry** is opened before the merge and closed after C-b (NEVER-2).

## BOTH BRANCHES

- **C-b reads 0 of 234 and the tests pass:** done; orders `bo-1` and `bp-1` close.
- **C-b reads anything else, or the package suite fails on the merged tree:** the merge commit is reverted in the same
  session with a new commit (never a rebase), and the revert is read back by the same table.
- **A leg is found running at the act:** nothing is merged.

## EXCLUDED

No pointer move. No run of any job. No change to `_LEGAL_SUFFIX`, `slug_query`, the matcher or the driver. No gold, silver
or bronze write. No deploy outside this box's working tree.

## VERDICT: SIGNED (COO), pending the CTO half; the act waits on C-a
