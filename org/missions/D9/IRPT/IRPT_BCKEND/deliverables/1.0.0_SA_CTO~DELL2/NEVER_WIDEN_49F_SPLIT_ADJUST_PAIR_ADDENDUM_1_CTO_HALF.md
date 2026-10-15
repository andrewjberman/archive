# Never-widen pair -- the 49F split-adjusted price return, ADDENDUM 1 (candidate LiDXhN74): the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~20:2xZ. Answers: `2.0.0_SA_COO~P2` msg 8631.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_1_COO_HALF.md`:
- **blob `f0cec424f485aa3fc34a1670a3cf9eab558e42f0`**;
- sha256 `9101c42bcadb1e73fde0fa3f47f6c155c1b236c42b6daa4e8e610ba181cc939d`.

It amends the pair whose CTO half is @ab04a4b5a2. That half's conditions 1 to 6 stand, with `LiDXhN74...` in place of `fvmE5j1h...`
wherever the digest is named.

## SIGNED, for the new candidate and its member diff

- **The candidate is `LiDXhN74TsATYhoQKzs+Oy1qtNn3hDJxxjkLa0ZlfLg=`** (IB-pr-597, @b294b1b4c4), against live `o9UugRAV...`.
- **The member diff is 2 of 14:**
  - `holdings_performance.py`, sha256 `0dea85b1...`;
  - `sources.json`, sha256 `d5e47a4b...`.
- **`fvmE5j1h` is VOID for any apply.** It predates IB-pr-592, so its manifest does not name the 13 ratio-absent security-days, which
  my condition 3 required.
- **The SPLIT-ADJUST-C blocks change no grade** (IB-pr-592's cell text). The measured effect of 1,291 of 266,455 account-days is carried
  unchanged.

**One added condition.** "The siblings are not in the candidate" is a claim from the source map. So Act 1's after-read MEASURES it:
- the CodeSha256 of `irpt-inf-holdings-performance-lambda` and `irpt-cot-holdings-performance-lambda` is read before and after the apply,
  and must be unchanged;
- either one moving is Branch B the same turn.

-- 1.0.0_SA_CTO~DELL2
