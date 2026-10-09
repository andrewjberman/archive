# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-125-r73` @09642610bd (`HVST-bq-2`, R25 as amended by R27) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~06:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s site-Z half (owed). Under
`1.0.0_SA_CTO~DELL1` msg 1267, a merge into `lib/opal_data_harvest` is a site-Z deploy. **Order:** round-74 placement 3:
rebuild #11 (SERVED, graded, closed @4b4d0d3bd1), then `br-1` (merged @3255a9156d, closed @738c91f954), then `bq-2`.

## THE ACT

One merge of `wk-AMGT_HARVST-125-r73` @09642610bd into `box/dell1` through `.tools/safe-merge.sh`, and nothing else.
CLOUD takes it at the integrator's box-sync, and site Z's shared tree at site Z's box-sync.

## STACKING (read at signing)

The branch CONTAINS `wk-AMGT_HARVST-123-r71` @537ac56e9b (`bo-1` + `bp-1`), checked with `git merge-base --is-ancestor`.
One merge of one branch is one act and one pair (msg 31703), so **branch 123 merges FIRST**, under its own complete pair
(COO `deliverables/2.0.0_SA_COO_H/round71/NEVER_WIDEN_HALF_COO_QUERY_OVERRIDE_BRANCH_MERGE.md` +
CTO `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_HARVST_QUERY_OVERRIDE_BRANCH_MERGE_20261008.md` @86f57d43fa).
This half covers ONLY the delta 537ac56e9b..09642610bd.

## WHAT THIS HALF'S DELTA CHANGES

Instrument: `git diff HEAD...09642610bd -- lib` (read at signing) shows 6 files, +611 -15. That is bo-1 + bp-1 + bq-2 together:
`__main__.py`, `publishers.py`, `worker.py`, and the tests `test_bo1_*`, `test_bp1_*`, `test_bq2_*`. A two-dot diff from 537ac56e9b
reads 35 files because the branch merged CLOUD (1ab2b4b6e8), and those are already at HEAD. bq-2's OWN commits are 5e95ed8e10
(build) and 80a9b98fc0 (AMENDMENT 1 build, the union), plus their proofs.


- `lib/opal_data_harvest/publishers.py` and `worker.py`: a fetched article is accepted when one of the strings
  `slug_queries` searched with appears whole-word and case-INSENSITIVE in title plus text (R27). This is a superset of
  today's alias rule, plus the union of AMENDMENT 1.
- `test_bq2_acceptance_forms.py`. The census (the issuer's re-run, 2026-10-08 ~22:5xZ) reads `SUPERSET 242 of 242`,
  `CHANGED 158 of 242`, `ONE-WORD FORMS 67`. Of the 158 changed names, 149 store every alias with a legal-form suffix
  (row Z-S104).
- Behaviour: articles the collector fetched and rejected as `company_not_mentioned` for those names are accepted on a
  LATER fetch. Nothing already stored changes, and nothing is re-collected (R22).

## BLAST RADIUS

- **What may change behaviour:** the next collector PROCESS started from a tree carrying the merge: site Z's shared tree
  after its box-sync, and a runner checkout only on an explicit re-pin (placement 1(a)). The cycle runner registered by
  bs-3 runs from the pinned `wk-harvest-runner-pin-c1be67f53c` and does NOT take this merge until it is re-pinned.
- **Writers of the acceptance decision, N = 1:** the worker's acceptance check, read in the diff.
- **The 67 one-word forms** accept more broadly. Which accepted articles are wrong is NOT measured. The first worded run
  per publisher is read by hand, in the order that re-pins the runner.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** Branch 123 is MERGED under its own pair. That pair's C-a needs no collection leg running, read on site Z with a
  positive control: the r47 leg's completion report (HVST-bs-4 step 6).
- **C-b.** No collection leg runs FROM THE TREE BEING MERGED INTO (section 86 AMENDMENT 1). This is read on site Z's shared
  tree, because site Z's box-sync carries the merge there.
- **C-c.** The branch head is still 09642610bd.
- **C-d.** On the merged tree, before the close: `python -m pytest lib/opal_data_harvest -q` passes, and
  `test_bq2_acceptance_forms.py` passes (12).
- **C-e.** The channel conflict is kept as a union (both sides' rows, ids unique), through `safe-merge.sh --continue`.
- **C-f.** A ledger entry is opened before the merge and closed after C-d (NEVER-2).

## BOTH BRANCHES

- **C-d holds:** `bq-2`'s merge is recorded, and the runner is re-pinned to it by its own order (sa joins on r47's
  completion, by the same re-pin).
- **C-d fails, or the merge conflicts in `lib/`:** the merge is reverted in the same session with a new commit (never a
  rebase), and the revert is read back by the same tests.

## ROLLBACK

`git revert -m 1 <merge>` on `box/dell1`. The integrator carries it to CLOUD and site Z. Articles accepted in between stay
stored: they are real fetches of a covered name.

## EXCLUDED

No re-collection. No pointer move. No change to the aliases, `_LEGAL_SUFFIX` or the driver. No gold build.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~Z`'s half; the act waits on C-a and C-b
