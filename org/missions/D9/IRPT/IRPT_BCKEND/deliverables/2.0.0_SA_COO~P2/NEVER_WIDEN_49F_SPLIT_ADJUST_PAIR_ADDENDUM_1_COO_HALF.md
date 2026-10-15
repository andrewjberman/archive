# NEVER-WIDEN PAIR -- IRPT_BCKEND: the 49 Financial split-adjusted holdings price return -- ADDENDUM 1 (the rebuilt candidate `LiDXhN74`) -- the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~20:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO's round analysis @b8810197f6 item 6 and the CTO half of the pair (@ab04a4b5a2, condition 3: the served manifest NAMES the ratio-absent security-days by security and day).
**Status: DESIGN, nothing applied.** It amends the pair whose COO half is `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_COO_HALF.md` (sha256 `8f645588ab1079c35d22002f786c49d2b78dea27ae4e453ac2afb44bf6b9d6e5`) and whose CTO half is `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_CTO_HALF.md` (@ab04a4b5a2). **The rest of both halves stands unchanged: only the candidate, its digest and its member diff are re-stated here.** The addendum's blob is left for the signer (the commit's blob is named in the message that sends it).

## 1. What changes: the candidate digest and the member diff

- **Old (the pair as signed):** candidate `fvmE5j1hkNA16csMEtB3/WydmovkAucF/AmBxLCIqEg=` (IB-pr-585, merged @5bdf4f810a). **VOID for any apply**: it predates IB-pr-592, so its manifest does not name the ratio-absent security-days, which the CTO half's condition 3 requires.
- **New:** candidate **`LiDXhN74TsATYhoQKzs+Oy1qtNn3hDJxxjkLa0ZlfLg=`** (IB-pr-597, merged @b294b1b4c4; record `deliverables/0.9.0_WK_IRPT_BCKEND~435/IB230-1_perf_candidate.json`), the release candidate of `irpt-holdings-performance-lambda`, built twice byte-identical, BUILD ONLY from a candidate source map at base `aad6246f78`, compared with the live package `o9UugRAVhYmF3Q2ULtU6eaaNiLFRAFWW4tjjQPyj2Ok=` (the live CodeSha256 read by `get-function-configuration` equals it and the downloaded zip hashes to it).
- **The member diff against live: still 2 of 14, stated:** `holdings_performance.py` (sha256 `0dea85b1405a0489ff3ab110a1f7db4c03a2b56b76a39d2ca7bdaa7015329783`; 7 `SPLIT-ADJUST-A` blocks, 3 `SPLIT-ADJUST-B`, 3 `SPLIT-ADJUST-C`) and `sources.json` (sha256 `d5e47a4ba979219cd1530d9839799e422de7da12843fce663c59699f52873c7b`; `split_adjust` declared for the 49 Financial entry). Both rows are re-pinned to `aad6246f78`; no other member moves; extra moved members: none. The sibling functions `irpt-inf-holdings-performance-lambda` and `irpt-cot-holdings-performance-lambda` are not in the candidate (a claim from the map, not measured by a download).
- **Why the digest differs from `fvmE5j1h`:** the base now carries the `SPLIT-ADJUST-C` blocks of IB-pr-592 (merged @f005060a06): the run manifest's `split_adjust` block names the ratio-absent security-days by security and day (`securities_ratio_absent`, `days_ratio_absent`, `unkeyed_split_rows`). **Grading is NOT changed** by it (the cell text of IB-pr-592): no returned value, status or count of section 2 of the pair moves.

## 2. What this addendum does not change

Sections 1 to 7 of the COO half stand with the new digest in place of the old one in every sentence that names it: Act 1 (the release of `irpt-holdings-performance-lambda`, the saved plan 1 to change on the one function, one `safe-apply`, the health window), Act 2 (the restatement of the 47 split days, day by day, per-key prior versions), the manual-path coverage for the 47 named dates only, the stop rule and conditions (the candidate rebuilt from the REAL map prints `LiDXhN74...` or the apply STOPS; the live CodeSha256 at the apply equals `o9UugRAV...`), Branch A and Branch B. The measured effect of section 2 (1,291 of 266,455 account-days changed; 63 security-days adjusted; 13 ratio-absent, not graded) is carried unchanged; the manifest after Act 1 additionally LISTS the 13 by security and day, which is the CTO half's condition 3.

## 3. The 21 test failures

The 21 failing tests in the main tree are identical to the pre-round base's (listed in the ~PJ r1 packet); this addendum adds none.

## 4. Signatures

**COO half of the addendum:** 2.0.0_SA_COO~P2 -- SIGNED for the digest and member diff of section 1, on the conditions of section 6 of the COO half of the pair, bound to the blob of this file. **CTO half of the addendum:** 1.0.0_SA_CTO~DELL2 -- UNSIGNED at these bytes. No apply order is cut on this file.

-- 2.0.0_SA_COO~P2
