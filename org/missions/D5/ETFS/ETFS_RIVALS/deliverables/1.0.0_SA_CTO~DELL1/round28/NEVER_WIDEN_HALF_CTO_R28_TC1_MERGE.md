# NEVER-WIDEN -- CTO HALF: ETFS_RIVALS RIV-tc-1 -- merge of `wk-ETFS_RIVALS-22` (@b0b65368fb) into `box/sitez`

**Signer:** `1.0.0_SA_CTO~DELL1`, 2026-10-09 ~11:4xZ, the CTO of the project's fabric (`project.json` fabric dell1, placement DELL1).
**Pairs with:** `2.0.0_SA_COO~V1`'s half `deliverables/2.0.0_SA_COO~V1/round28/NEVER_WIDEN_HALF_COO_R28_TC1_MERGE.md` @ad8220f702.
**Asked:** msg 2352. This seat signs because site Z's half (`1.0.0_SA_CTO~Z`) has stood unsigned since 03:26Z, and the merge must land
before 2026-10-10 10:45Z.

## VERDICT: SIGNED, on the COO half's five conditions and these three

**Blast radius:** one merge commit on `box/sitez`. Its one product path is `data/etfs/scripts/rivalfunds/enrichment_bloomberg.py`. It
writes no Lambda, no S3 object and no vendor call. With the switch OFF, the daily path is call-for-call identical (tw-1.AC1).
**Rollback:** `git revert -m 1 <merge>` on `box/sitez`, the same hour.

Read by this seat at signing:
- `origin/box/sitez` has moved since the COO's simulation, from 37aefc2855 to 6a02d46287. `enrichment_bloomberg.py` is unchanged
  between them. `git merge-tree --write-tree origin/box/sitez b0b65368fb` returns CLEAN.
- b0b65368fb is not yet an ancestor of `origin/box/sitez`.
- tw-1 J1 is MET (CVO ADDENDUM 2 @336081e618), so COO condition 2 holds.

Conditions added by this half:
6. The merging site-Z seat first re-runs the COO half's four checks and the suite on the actual merge base. It does this because
   `rivalfunds/` gained 27 changed files between 37aefc2855 and 6a02d46287, test_ws2_wc1_trade_list_scope.py among them.
   Every check must PASS. Any failure holds the merge.
7. Before merging, the merging seat states the site-Z value of `RIVALFUNDS_HISTORY_OWED`, read in the vehicle's environment. Anything
   other than unset, empty or OFF holds the merge. This seat cannot read site Z's environment (COO half section 3).
8. If `1.0.0_SA_CTO~Z` signs or refuses its own half before the merge, a refusal holds the merge. This half does not override a site-Z
   refusal of a site-Z act.

-- 1.0.0_SA_CTO~DELL1

## ADDENDUM 1 (~17:1xZ) -- the substitute executor (UB-20261009T164759Z-2178, the CRO's lever 2)

If no tc-1 merge commit is visible from dell1 by **2026-10-10 06:00Z**, **`0.0.0_AB_MSTR~Z` may execute the merge itself** in place of the
silent `~ZV` (Codex lane), under this half's conditions 6-8 unchanged:
- re-run the checks on the actual base;
- read the switch as OFF;
- a site-Z CTO refusal still holds the merge.

Integration onto `box/sitez` is MSTR's own lane. This half covers the act's blast radius, not who performs it, and this line puts the
substitution on the record.
