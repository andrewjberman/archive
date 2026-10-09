# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-126-r74` @c868d27d87 (`HVST-br-1`, R30) into `lib/research/harvest`

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~03:5xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (owed; asked when rebuild #11
closes). **Order:** round-74 placement 3 (`ledger/ROUND_ANALYSIS.round74.md`): rebuild #11 first, then `br-1`, then `bq-2`,
each under its own pair. **Which CTO:** this branch changes `lib/research/harvest/` only, gold's matcher, which is not a
site-Z producer path (census @6a308cd424). So no site-Z half is owed. The hand-over listed all four held branches under
`lib/opal_data_harvest`; for `br-1` that is not what `git diff` shows.

## THE ACT

One merge of `wk-AMGT_HARVST-126-r74` @c868d27d87 into `box/dell1` through `.tools/safe-merge.sh`, and nothing else. A merge
SERVES NOTHING by itself. Gold changes only at the next rebuild (#12), which is its own pair.

## WHAT THE BRANCH CHANGES (read at signing: `git diff 39889dd4d7 origin/wk-AMGT_HARVST-126-r74`, 11 files, +4,474 -12)

- `lib/research/harvest/publication_gold.py` +25/-: R30 (`1.0.0_SA_CTO~Z` msg 32004) plus the issuer's clause. An alias
  matches whole-word only where the matched text's first letter is upper-case, or where it equals the stored alias exactly
  (for "eBay"). Otherwise matching stays case-insensitive.
- New test `test_br1_capital_initial_alias.py`, and four existing gold tests adjusted to the rule.
- `deliverables/0.9.0_WK_AMGT_HARVST~126/`: the census script and its output, plus the proof. These are records only.
- The surprise channel: the worker's row. It is the only path that conflicts on a dry merge against HEAD
  (`git merge-tree`, 2026-10-09 ~03:5xZ). The code merges clean.

## WHAT THE CELL MEASURED (HVST-br-1, `1.0.0_SA_CTO~Z`'s round, graded)

- R30 REMOVES 280 of 46,066 tested pairs (280 of 48,358 served at that time), over 16 securities.
- R30 (b): `3.0.0_SA_CVO~Z` graded the 30 removed pairs 30 of 30 wrong, bar 27 MET (msg 32051, @c352f9f601).
- SENTENCE-INITIAL 3 of 40 kept pairs read (R30 (c), stated as a count).

## BLAST RADIUS

- **What may change behaviour:** any gold build run from dell1's tree after the merge (`publication_gold build-mention`
  and `build-daily`), and any site-Z build after its box-sync. No gold build runs on a schedule. The served parts do not
  change until rebuild #12 is acted.
- **Writers of the matcher, N = 1:** `publication_gold`'s alias match, read in the branch's diff.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a. Rebuild #11 is CLOSED** (its ledger closed, and the CVO's grade of the 22 rows accepted). If `br-1` merged first,
  rebuild #11 would build on R30's matcher, which its signed rule does not cover.
- **C-b. No gold build is alive** on dell1 at the merge (process list, positive control).
- **C-c. Branch head is still c868d27d87.**
- **C-d. On the merged tree, before the close:**
  `python -m pytest lib/research/harvest lib/opal_data_harvest/test_az1_alias_set.py -q` passes, and
  `test_br1_capital_initial_alias.py` passes (7).
- **C-e.** A ledger entry is opened before the merge and closed after C-d (NEVER-2).

## BOTH BRANCHES

- **C-d holds:** `br-1`'s merge is recorded. Rebuild #12, which serves R30, is cut as its own pair, with a dry run whose
  rule allows exactly the census's removal class. `bq-2` follows under its pair.
- **C-d fails, or the merge conflicts beyond the channel:** the merge is reverted in the same session with a new commit
  (never a rebase), and the revert is read back by the same tests.

## ROLLBACK

`git revert -m 1 <merge>` on `box/dell1`. No served key depends on the code until rebuild #12 is acted.

## EXCLUDED

No gold build. No served write. No change to `lib/opal_data_harvest`, the collector or the pointer.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half; the act waits on C-a
