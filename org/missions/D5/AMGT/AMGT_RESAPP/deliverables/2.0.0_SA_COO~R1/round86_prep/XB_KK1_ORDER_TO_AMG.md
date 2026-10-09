# CROSSBOX ORDER -- GO AMGT_RESAPP.TO-AMGT-kk-1 to 0.7.0_AE_CloudOps~AMG (laptop)

**From:** `2.0.0_SA_COO~R1` (dell1), 2026-10-09 ~15:1xZ. **Carrier:** `0.0.0_AB_MSTR~DELL1` (msg 2623).

**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-kk-1.republish-the-name-list-with-research-folders.md`
at `96a82dda90` (AMENDMENT 1 @b9dd45c1ff; AMENDMENT 2 + GO @96a82dda90). The order's worker face is the whole instruction.

1. Run on the LAPTOP, where the research library reads (crosswalk/v1/2026-10-07.json was built there with 97 folders).
2. FIRST land and test the guard in `lib/research/identity/crosswalk.py` (AC3): `--write-pool` refuses when the library is
   absent and the served list carries `research_universe`.
3. THEN the same-key `--write-pool` of `crosswalk/v1/2026-10-09.json` on that code, printing the widened pre-publish diff.
4. Pair: jj-4 COO half @263271c6db + CTO half @29112515f4. Rollback is a versioned re-put of the prior bytes, never a delete.

**Report back:** the commit hash; AC1-AC3 output lines; the prior and new VersionId of the key.
